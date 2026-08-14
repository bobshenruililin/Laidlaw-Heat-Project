#!/usr/bin/env python3
"""Tests for the monthly station–grid bridge. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "54_monthly_station_grid_bridge.py"
JSON_PATH = ROOT / "outputs" / "monthly_bridge" / "monthly_station_grid_bridge.json"


class MonthlyBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())

    def test_window(self) -> None:
        self.assertEqual(self.p["window"]["n_months"], 132)
        self.assertEqual(self.p["window"]["n_days"], 4017)

    def test_mean_tmin_travels_and_hot_nights_do_not(self) -> None:
        tm = self.p["fits"]["era5_tmin_on_hko_tmin"]
        hn = self.p["fits"]["era5_hn_on_hko_hn"]
        self.assertGreater(tm["r"], 0.95)
        self.assertGreater(tm["slope"], 0.9)
        self.assertLess(tm["slope"], 1.2)
        self.assertLess(hn["slope"], 0.15)
        self.assertLess(hn["r"], 0.6)

    def test_era5_hot_nights_are_rare_months(self) -> None:
        f = self.p["month_flags"]
        self.assertGreater(f["hko_hn_positive"], 40)
        self.assertLess(f["era5_hn_positive"], 20)
        self.assertEqual(f["both_hn_positive"], f["era5_hn_positive"])

    def test_identifying_variation_is_a_minority(self) -> None:
        s = self.p["identification_hko_hn"]["share_identifying_within_month"]
        self.assertGreater(s, 0.15)
        self.assertLess(s, 0.45)
        self.assertEqual(self.p["identification_hko_hn"]["n_calendar_months_with_sd"], 6)

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.p).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure descriptives only", self.p["provenance"].lower())

    def test_figures_exist(self) -> None:
        fig = ROOT / "figures" / "monthly_bridge"
        self.assertTrue((fig / "monthly_hot_nights_hko_vs_era5.svg").exists())
        self.assertTrue((fig / "monthly_tmin_hko_vs_era5.svg").exists())


if __name__ == "__main__":
    unittest.main()
