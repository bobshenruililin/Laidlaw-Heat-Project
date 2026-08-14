#!/usr/bin/env python3
"""Tests for the identification laboratory. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "60_identification_laboratory.py"
JSON_PATH = ROOT / "outputs" / "identification_lab" / "identification_lab.json"
HTML_PATH = ROOT / "docs" / "id" / "index.html"
HEAT = ROOT / "figures" / "identification_lab" / "hot_night_year_month.svg"
REL = ROOT / "figures" / "identification_lab" / "era5_reliability_given_hko.svg"
FIGD = ROOT / "figures" / "live_identification" / "figure_D_hot_night_identification.svg"


class IdentificationLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())
        cls.html = HTML_PATH.read_text()

    def test_anchors_match_script_53(self) -> None:
        a = self.p["anchors"]
        self.assertEqual(a["hko_hn"], 449)
        self.assertEqual(a["era5_hn"], 17)
        self.assertEqual(a["both"], 14)
        self.assertEqual(a["hko_only"], 435)
        self.assertEqual(a["era5_only"], 3)
        self.assertEqual(self.p["window"]["n_days"], 4017)

    def test_calibration_is_near_zero_until_29(self) -> None:
        t = self.p["tail"]
        self.assertEqual(t["n_hko_28_to_29"], 365)
        self.assertEqual(t["n_era5_in_28_to_29"], 1)
        self.assertLess(t["rate_28_to_29"], 0.01)
        self.assertEqual(t["n_hko_ge29_5"], 16)
        self.assertAlmostEqual(t["rate_ge29_5"], 0.4375, places=3)
        self.assertGreater(t["rate_ge29_5"], t["rate_28_to_29"])

    def test_always_on_months_hold_most_nights(self) -> None:
        ao = self.p["always_on"]
        self.assertEqual(ao["n_hko_hn_jun_sep"], 400)
        self.assertAlmostEqual(ao["share_jun_sep"], 0.8909, places=3)
        self.assertTrue(set(ao["both_nights_calendar_months"]).issubset({6, 7, 8}))
        self.assertNotIn(5, ao["both_nights_calendar_months"])
        self.assertNotIn(10, ao["both_nights_calendar_months"])

    def test_most_hot_night_months_are_invisible_to_era5(self) -> None:
        m = self.p["monthly_containment"]
        self.assertEqual(m["n_hko_positive_months"], 57)
        self.assertEqual(m["n_those_with_any_era5_hn"], 9)
        self.assertEqual(m["n_hko_positive_without_era5"], 48)

    def test_both_nights_mostly_sit_inside_spells(self) -> None:
        spells = self.p["spells_of_both_nights"]
        self.assertEqual(len(spells), 14)
        isolated = [s for s in spells if s["place"] == "isolated"]
        self.assertEqual(len(isolated), 1)
        self.assertEqual(isolated[0]["date"], "2014-07-23")
        july2022 = [s for s in spells if s["date"].startswith("2022-07")]
        self.assertTrue(all(s["run_length"] == 21 for s in july2022))

    def test_figures_keep_captions_in_the_margin(self) -> None:
        for path in (HEAT, REL, FIGD):
            self.assertTrue(path.exists(), path)
            svg = path.read_text()
            self.assertIn("Not a health finding", svg)
            self.assertIn("viewBox", svg)
        self.assertIn("always ≥1 night", HEAT.read_text())
        self.assertIn("Caption sits under the plot, not on it", REL.read_text())

    def test_page_layout_contract(self) -> None:
        self.assertIn("identification laboratory", self.html.lower())
        self.assertIn("figcaption", self.html)
        self.assertIn("not form 2a", self.html.lower())
        self.assertIn("id_embed.js", self.html)
        self.assertIn("./era5_reliability_given_hko_web.svg", self.html)
        self.assertTrue((ROOT / "docs" / "id" / "era5_reliability_given_hko_web.svg").exists())
        # Overlap law: plot captions are HTML, not absolutely stacked on the SVG.
        self.assertNotIn("position:absolute", self.html.split("/* plots */")[-1] if "/* plots */" in self.html else self.html)
        self.assertIn("class=\"caption\"", self.html)

    def test_identification_profile_has_six_encodings(self) -> None:
        profile = self.p["identification_profile"]
        self.assertEqual(len(profile), 6)
        by = {r["encoding"]: r for r in profile}
        self.assertAlmostEqual(by["mean_temp"]["identifying_share"], 0.0422, places=3)
        self.assertAlmostEqual(by["hot_nights"]["identifying_share"], 0.2883, places=3)
        self.assertAlmostEqual(by["hot_nights"]["share_intensive"], 0.9541, places=3)
        self.assertAlmostEqual(by["cold_days"]["share_extensive"], 0.3881, places=3)
        self.assertEqual(by["hot_nights"]["family"], "official heat-count")
        self.assertIn("Headquarters-only", by["hot_nights"]["instrument"])
        self.assertEqual(self.p["heatmap_vmax"], 25)
        self.assertGreater(self.p["cold_analogue"]["rate"], 0.95)

    def test_no_health_coefficients(self) -> None:
        blob = (json.dumps(self.p) + self.html).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "1.073"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure descriptives only", self.p["provenance"].lower())


if __name__ == "__main__":
    unittest.main()
