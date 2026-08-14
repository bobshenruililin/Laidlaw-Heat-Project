#!/usr/bin/env python3
"""Tests for the six-encoding identifying-month table. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "55_identifying_months_six_encodings.py"
JSON_PATH = ROOT / "outputs" / "identifying_months" / "hko_six_encodings.json"


class IdentifyingMonthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())
        cls.by = {e["encoding"]: e for e in cls.p["encodings"]}

    def test_six_encodings_and_window(self) -> None:
        self.assertEqual(self.p["window"]["n_months"], 132)
        self.assertEqual(len(self.p["encodings"]), 6)
        self.assertEqual(
            set(self.by),
            {"mean_temp", "mean_tmax", "mean_tmin", "hot_nights", "very_hot_days", "cold_days"},
        )

    def test_means_are_almost_entirely_seasonal(self) -> None:
        for col in ("mean_temp", "mean_tmax", "mean_tmin"):
            self.assertLess(self.by[col]["share_identifying_within_month"], 0.10)
            self.assertEqual(self.by[col]["n_calendar_months_with_sd"], 12)

    def test_hot_nights_six_summer_months(self) -> None:
        hn = self.by["hot_nights"]
        self.assertAlmostEqual(hn["share_identifying_within_month"], 0.2883, places=3)
        self.assertEqual(hn["n_calendar_months_with_sd"], 6)
        self.assertEqual(hn["months_with_sd"], [5, 6, 7, 8, 9, 10])
        self.assertEqual(hn["n_months_positive"], 57)

    def test_cold_days_four_winter_months(self) -> None:
        cd = self.by["cold_days"]
        self.assertAlmostEqual(cd["share_identifying_within_month"], 0.4688, places=3)
        self.assertEqual(cd["n_calendar_months_with_sd"], 4)
        self.assertEqual(cd["months_with_sd"], [1, 2, 3, 12])
        self.assertEqual(cd["months_with_sd_abbr"], "Dec–Mar")
        self.assertEqual(cd["n_months_positive"], 29)

    def test_very_hot_days_track_hot_nights_calendar(self) -> None:
        vhd = self.by["very_hot_days"]
        self.assertEqual(vhd["months_with_sd"], [5, 6, 7, 8, 9, 10])
        self.assertGreater(vhd["share_identifying_within_month"], 0.25)
        self.assertLess(vhd["share_identifying_within_month"], 0.45)

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.p).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "1.073"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure descriptives only", self.p["provenance"].lower())

    def test_figure_exists(self) -> None:
        self.assertTrue((ROOT / "figures" / "identifying_months" / "hko_six_encodings.svg").exists())


if __name__ == "__main__":
    unittest.main()
