#!/usr/bin/env python3
"""Tests for the same-night three-thermometer scrubber. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "59_same_night_three_thermometers.py"
JSON_PATH = ROOT / "outputs" / "threshold_demo" / "nights_28.json"
JS_PATH = ROOT / "docs" / "demo" / "nights_28.js"
HTML_PATH = ROOT / "docs" / "demo" / "index.html"
FIG = ROOT / "figures" / "threshold_demo" / "same_night_three_thermometers.svg"


class SameNightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())
        cls.html = HTML_PATH.read_text()
        cls.js = JS_PATH.read_text()

    def test_union_counts_match_script_53_anchors(self) -> None:
        c = self.p["counts"]
        self.assertEqual(c["hko_only"], 435)
        self.assertEqual(c["both"], 14)
        self.assertEqual(c["era5_only"], 3)
        self.assertEqual(c["union"], 452)
        self.assertEqual(c["hko_total"], 449)
        self.assertEqual(c["era5_total"], 17)
        self.assertEqual(len(self.p["nights"]), 452)
        self.assertEqual(self.p["window"]["n_days"], 4017)

    def test_featured_nights_are_real_cache_dates(self) -> None:
        by_date = {n["date"]: n for n in self.p["nights"]}
        both = by_date[self.p["featured"]["hottest_both"]]
        self.assertEqual(both["date"], "2015-08-08")
        self.assertEqual(both["tag"], "both")
        self.assertEqual(both["hko_tmin"], 30.0)
        miss = by_date[self.p["featured"]["hottest_hko_miss"]]
        self.assertEqual(miss["date"], "2022-09-14")
        self.assertEqual(miss["hko_tmin"], 29.6)
        self.assertEqual(miss["era5_tmin"], 25.6)
        self.assertEqual(miss["tag"], "hko")
        gap = by_date[self.p["featured"]["widest_gap"]]
        self.assertEqual(gap["date"], "2023-09-22")
        self.assertGreaterEqual(gap["gap_hko_minus_era5"], 5.0)
        self.assertEqual(self.p["featured"]["era5_only"], [
            "2014-07-24", "2015-08-09", "2016-07-09",
        ])
        self.assertEqual(self.p["counts"]["n_hko_ge29_era5_below_28"], 71)

    def test_does_not_dump_4017_day_blob(self) -> None:
        self.assertLess(len(self.p["nights"]), 500)
        self.assertNotIn("hko_tmin_tenths", self.js)

    def test_page_has_scrubber_and_hash(self) -> None:
        self.assertIn("id=\"scrubber\"", self.html)
        self.assertIn("nights_28.js", self.html)
        self.assertIn("NIGHTS_28", self.html)
        self.assertIn("#d=", self.html)
        self.assertIn("three thermometers", self.html.lower())
        self.assertIn("not form 2a", self.html.lower())

    def test_no_health_or_harm_ranking(self) -> None:
        blob = (json.dumps(self.p) + self.html).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "dangerous-night"):
            self.assertNotIn(banned, blob)
        self.assertIn("do not rank these nights by harm", json.dumps(self.p).lower())

    def test_figure_names_the_night(self) -> None:
        self.assertTrue(FIG.exists())
        svg = FIG.read_text()
        self.assertIn("2015-08-08", svg)
        self.assertIn("30.0°C", svg)
        self.assertIn("Not a health finding", svg)


if __name__ == "__main__":
    unittest.main()
