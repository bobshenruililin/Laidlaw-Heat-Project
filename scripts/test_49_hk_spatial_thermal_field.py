#!/usr/bin/env python3
"""Tests for the Hong Kong spatial thermal field. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "49_hk_spatial_thermal_field.py"
JSON_PATH = ROOT / "outputs" / "hk_spatial" / "hk_spatial_field.json"
HTML_PATH = ROOT / "docs" / "geo" / "index.html"


class HkSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT), "--skip-fetch"], cwd=ROOT)
        cls.payload = json.loads(JSON_PATH.read_text())
        cls.model = cls.payload["model"]
        cls.cells = {c["id"]: c for c in cls.payload["cells"]}

    def test_window_and_counts(self) -> None:
        self.assertEqual(self.payload["window"]["start"], "2013-01-01")
        self.assertGreaterEqual(len(self.payload["cells"]), 35)
        for c in self.payload["cells"]:
            self.assertEqual(c["n_days"], 4017)

    def test_headquarters_exists(self) -> None:
        self.assertIn("hko_hq", self.cells)
        self.assertEqual(self.cells["hko_hq"]["kind"], "station")

    def test_waglan_has_more_hot_nights_than_headquarters(self) -> None:
        self.assertGreater(self.cells["waglan"]["hn_total"], 5 * self.cells["hko_hq"]["hn_total"])

    def test_peak_is_cooler_at_night(self) -> None:
        self.assertLess(self.cells["the_peak"]["mean_tmin"], self.cells["hko_hq"]["mean_tmin"] - 1.0)
        self.assertEqual(self.cells["the_peak"]["hn_total"], 0)

    def test_ta_kwu_ling_has_more_cold_days(self) -> None:
        self.assertGreater(self.cells["ta_kwu_ling"]["cd_total"], self.cells["hko_hq"]["cd_total"])

    def test_unique_fingerprints_are_mostly_distinct(self) -> None:
        self.assertGreaterEqual(self.model["unique_fingerprints"], 30)
        self.assertFalse(self.model["peak_same_cell_as_hq"])

    def test_monthly_hot_nights_are_summer_weighted(self) -> None:
        hq = self.cells["hko_hq"]
        self.assertEqual(len(hq["hn_by_month"]), 12)
        self.assertGreaterEqual(hq["jja_hn"], max(1, int(0.6 * hq["hn_total"])))
        self.assertIn("months", self.payload)

    def test_spatial_model_fit(self) -> None:
        self.assertGreater(self.model["r2"], 0.4)
        self.assertLess(self.model["coefficients"]["elevation_m"]["beta"], 0)
        self.assertGreater(self.model["trend_model"]["r2"], self.model["r2"])
        self.assertLess(self.model["trend_model"]["beta"]["lat"], 0)

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "gate 3 freeze"):
            self.assertNotIn(banned, blob)
        self.assertIn("no health", self.payload["provenance"].lower())
        html = HTML_PATH.read_text()
        self.assertIn("Exposure only", html)
        self.assertIn("leaflet", html.lower())
        self.assertIn("hn_month", html)
        self.assertNotRegex(html, r"q\s*=\s*0\.")


if __name__ == "__main__":
    unittest.main()
