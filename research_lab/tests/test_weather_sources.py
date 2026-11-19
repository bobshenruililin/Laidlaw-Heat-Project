import unittest
from datetime import date

from research_lab import weather_sources as sources


class DailySourceTests(unittest.TestCase):
    def test_inclusive_thresholds_and_unrounded_monthly_means(self):
        a, b, c = (date(2020, 1, day) for day in (1, 2, 3))
        # Integer tenths of °C, as in the archived station files.
        series = {
            "mean_temp": {a: 220, b: 290, c: 260},
            "mean_tmax": {a: 329, b: 330, c: 331},
            "mean_tmin": {a: 120, b: 280, c: 279},
        }
        month = sources._monthly(series, [a, b, c])
        self.assertEqual((month["cold_days"], month["hot_nights"], month["very_hot_days"]), (1, 1, 2))
        self.assertAlmostEqual(month["mean_temp"], 77 / 3)
        self.assertAlmostEqual(month["mean_tmin"], 67.9 / 3)

    def test_station_title_completeness_precision_and_uniqueness(self):
        header = ("Chinese title\nDaily Mean Temperature (°C) at the Hong Kong Observatory\n"
                  "年/Year,月/Month,日/Day,數值/Value,數據完整性/data Completeness\n")
        row = "2020,1,1,12.0,C\n"
        self.assertEqual(sources._station_series(header + row, "Mean"), {date(2020, 1, 1): 120})
        for bad in (row + row, row.replace(",C", ","), row.replace("12.0", "12.05")):
            with self.subTest(row=bad), self.assertRaises(ValueError):
                sources._station_series(header + bad, "Mean")
        with self.assertRaises(ValueError):
            sources._station_series(header + row, "Maximum")


if __name__ == "__main__":
    unittest.main()
