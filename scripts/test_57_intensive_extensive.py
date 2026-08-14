#!/usr/bin/env python3
"""Tests for intensive vs extensive identification. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "57_intensive_extensive_identification.py"
JSON_PATH = ROOT / "outputs" / "identifying_months" / "intensive_extensive.json"
FIG = ROOT / "figures" / "identifying_months" / "intensive_extensive.svg"


class IntensiveExtensiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())
        cls.by = {e["encoding"]: e for e in cls.p["encodings"]}

    def test_window_and_six_encodings(self) -> None:
        self.assertEqual(self.p["window"]["n_months"], 132)
        self.assertEqual(self.p["window"]["n_years"], 11)
        self.assertEqual(len(self.p["encodings"]), 6)

    def test_continuous_encodings_have_no_extensive_margin(self) -> None:
        for col in ("mean_temp", "mean_tmax", "mean_tmin"):
            e = self.by[col]
            self.assertEqual(e["kind"], "continuous")
            self.assertEqual(e["share_extensive_of_identifying"], 0.0)
            self.assertEqual(e["share_intensive_of_identifying"], 1.0)
            self.assertEqual(e["always_on_months"], [])
            self.assertTrue(all(row["class"] == "intensity_only" for row in e["by_month"]))

    def test_hot_nights_june_to_september_always_on(self) -> None:
        hn = self.by["hot_nights"]
        self.assertEqual(hn["always_on_months"], [6, 7, 8, 9])
        self.assertEqual(hn["mixed_months"], [5, 10])
        self.assertEqual(hn["never_months"], [1, 2, 3, 4, 11, 12])
        self.assertAlmostEqual(hn["share_intensive_of_identifying"], 0.9541, places=3)
        self.assertAlmostEqual(hn["share_extensive_of_identifying"], 0.0459, places=3)
        self.assertGreater(hn["share_intensive_of_identifying"], 0.90)
        jun = next(r for r in hn["by_month"] if r["month"] == 6)
        jul = next(r for r in hn["by_month"] if r["month"] == 7)
        self.assertEqual(jun["n_positive_years"], 11)
        self.assertEqual(jun["min_when_positive"], 6.0)
        self.assertEqual(jul["min"], 1.0)
        self.assertEqual(jul["max"], 25.0)
        self.assertGreater(hn["july_share_of_identifying"], 0.40)
        self.assertLess(hn["july_share_of_identifying"], 0.50)

    def test_very_hot_days_june_july_august_always_on(self) -> None:
        vhd = self.by["very_hot_days"]
        self.assertEqual(vhd["always_on_months"], [6, 7, 8])
        self.assertEqual(vhd["mixed_months"], [5, 9, 10])
        self.assertGreater(vhd["share_intensive_of_identifying"], 0.80)

    def test_cold_days_have_no_always_on_month(self) -> None:
        cd = self.by["cold_days"]
        self.assertEqual(cd["always_on_months"], [])
        self.assertEqual(cd["mixed_months"], [1, 2, 3, 12])
        self.assertGreater(cd["share_extensive_of_identifying"], 0.30)
        self.assertLess(cd["share_extensive_of_identifying"], 0.45)
        self.assertAlmostEqual(cd["share_extensive_of_identifying"], 0.3881, places=3)

    def test_extensive_plus_intensive_recovers_identifying_ss(self) -> None:
        for e in self.p["encodings"]:
            recovered = e["ss_extensive"] + e["ss_intensive"]
            self.assertAlmostEqual(recovered, e["ss_identifying"], places=2)

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.p).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "1.073"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure descriptives only", self.p["provenance"].lower())

    def test_figure_states_the_always_on_fact(self) -> None:
        self.assertTrue(FIG.exists())
        svg = FIG.read_text()
        self.assertIn("June–September always had", svg)
        self.assertIn("July 2013 had 1 night", svg)
        self.assertIn("Not a health finding", svg)


if __name__ == "__main__":
    unittest.main()
