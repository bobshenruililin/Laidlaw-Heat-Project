import csv
from pathlib import Path
import tempfile
import unittest

from research_lab import service_context as context


def write_rows(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class ServiceContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.annual = self.directory / "fixture.csv"
        # Synthetic rows exercise the receipt and coverage checks on an approved-format table.
        self.cases = [
            dict(outcome=outcome, year=year, data_status="HA_APPROVED_AGGREGATE",
                 n_months=12, total_events=year - offset)
            for outcome, offset in (("chd", 1700), ("hf", 1900))
            for year in reversed(context.YEARS)
        ]
        write_rows(self.annual, self.cases)

    def test_within_series_indices_and_cross_publication_anchors(self):
        rows = context.analyse(self.annual)
        self.assertEqual([r["year"] for r in rows], list(context.YEARS))
        by_year = {r["year"]: r for r in rows}
        for key in (*context.OUTCOMES, *context.CONTEXT):
            self.assertEqual(by_year[2019][f"{key}_index"], 100)
            self.assertAlmostEqual(by_year[2020][f"{key}_index"], 100 * by_year[2020][key] / by_year[2019][key])
        self.assertEqual(by_year[2019]["circulatory_episodes"], 171331)
        self.assertEqual(by_year[2020]["all_hospital_episodes"], 1887178)
        self.assertEqual(by_year[2023]["ha_episodes"], 1905905)

    def test_rejects_invalid_health_rows(self):
        for replacement in ({"outcome": "stroke"}, {"data_status": "SYNTHETIC"}, {"year": 2024},
                            {"n_months": 11}, {"total_events": ""}, {"total_events": -1}):
            with self.subTest(replacement=replacement):
                write_rows(self.annual, [dict(self.cases[0], **replacement), *self.cases[1:]])
                with self.assertRaises(ValueError):
                    context.analyse(self.annual)
        for cases in (self.cases[1:], [*self.cases, self.cases[0]]):
            write_rows(self.annual, cases)
            with self.assertRaises(ValueError):
                context.load_annual_counts(self.annual)

    def test_rejects_zero_reference_even_when_other_years_are_valid(self):
        for row in self.cases:
            if row["year"] == 2019 and row["outcome"] == "chd":
                row["total_events"] = 0
        write_rows(self.annual, self.cases)
        with self.assertRaisesRegex(ValueError, "zero 2019"):
            context.analyse(self.annual)

    def test_rejects_cross_table_and_cross_edition_differences(self):
        snapshot = Path(context.__file__).with_name("sources") / context.SOURCE_FILE
        with snapshot.open(newline="", encoding="utf-8") as stream:
            original = list(csv.DictReader(stream))
        altered = self.directory / context.SOURCE_FILE
        for cases, error in (
            ([dict(original[0], private_episodes="1"), *original[1:]], "provider sum"),
            ([dict(original[0], circulatory_episodes="1"), *original[1:]], "disagree across editions"),
            (original[1:], "two distinct digest editions"),
            ([*original, original[0]], "Duplicate digest row"),
        ):
            with self.subTest(error=error):
                write_rows(altered, cases)
                with self.assertRaisesRegex(ValueError, error):
                    context.analyse(self.annual, self.directory)


if __name__ == "__main__":
    unittest.main()
