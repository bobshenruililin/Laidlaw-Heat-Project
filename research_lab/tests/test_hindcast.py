"""Synthetic checks for one-year-ahead annual burden benchmarks."""

import unittest

from research_lab.hindcast import BENCHMARKS, _point_benchmark, benchmark_rows


def series():
    return {
        "chd": {year: 500 + (year - 2013) ** 2 for year in range(2013, 2021)},
        "hf": {year: 20 * 2 ** (year - 2013) for year in range(2013, 2021)},
    }


class HindcastTests(unittest.TestCase):
    def test_all_targets_endpoints_and_windows_are_retained(self):
        rows = benchmark_rows(series())
        expected = [
            (target, outcome, benchmark)
            for target in (2017, 2018, 2019, 2020)
            for outcome in ("chd", "hf")
            for benchmark in BENCHMARKS
        ]
        self.assertEqual(
            [(r["target_year"], r["outcome"], r["benchmark"]) for r in rows], expected
        )
        for row in rows:
            target = row["target_year"]
            self.assertEqual(row["training_end"], target - 1)
            start = {
                "last_observation": target - 1,
                "expanding_log_linear": 2013,
                "trailing_3_log_linear": target - 3,
            }[row["benchmark"]]
            self.assertEqual(row["training_start"], start)
            self.assertEqual(row["training_years"], target - start)
            expected_phase = "2020_stress_case" if target == 2020 else "pre_2020_validation"
            self.assertEqual(row["phase"], expected_phase)

    def test_known_exponential_growth_and_percentage_error_denominator(self):
        for row in benchmark_rows(series()):
            if row["outcome"] != "hf":
                continue
            error = 100.0 if row["benchmark"] == "last_observation" else 0.0
            self.assertEqual(row["observed_minus_benchmark_pct"], error)
            expected = row["observed_count"] / (1.0 + error / 100)
            self.assertEqual(row["benchmark_count"], expected)

    def test_target_and_subsequent_counts_cannot_change_earlier_predictions(self):
        baseline = benchmark_rows(series())
        for origin in (2017, 2018, 2019, 2020):
            changed = series()
            for values in changed.values():
                for year in range(origin, 2021):
                    values[year] = values[year] * 10 + 77
            revised = benchmark_rows(changed)
            for old, new in zip(baseline, revised):
                if old["target_year"] < origin:
                    self.assertEqual(old, new)
                elif old["target_year"] == origin:
                    self.assertEqual(old["benchmark_count"], new["benchmark_count"])
                    self.assertNotEqual(old["observed_count"], new["observed_count"])

    def test_three_point_formula_with_irregular_counts(self):
        history = [(2016, 99), (2017, 108), (2018, 83)]
        # Log-OLS weights for a fourth equally spaced point are (-2, 1, 4)/3.
        expected = (108 * 83**4 / 99**2) ** (1 / 3)
        self.assertAlmostEqual(_point_benchmark(history, 2019, "trailing_3_log_linear"), expected)

    def test_rejects_future_or_skipped_training_year_and_nonpositive_count(self):
        for history in (
            [(2019, 2), (2020, 3), (2021, 3)],
            [(2016, 2), (2018, 3), (2019, 3)],
            [(2017, 2), (2018, 0), (2019, 3)],
        ):
            with self.subTest(history=history), self.assertRaises(ValueError):
                _point_benchmark(history, 2020, "trailing_3_log_linear")


if __name__ == "__main__":
    unittest.main()
