#!/usr/bin/env python3
"""Tests for the Pearl River Delta thermal mosaic. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "50_prd_thermal_mosaic.py"
JSON_PATH = ROOT / "outputs" / "prd_spatial" / "prd_spatial_field.json"
HTML_PATH = ROOT / "docs" / "prd" / "index.html"


class PrdSpatialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT), "--skip-fetch"], cwd=ROOT)
        cls.payload = json.loads(JSON_PATH.read_text())
        cls.model = cls.payload["model"]
        cls.cells = {c["id"]: c for c in cls.payload["cells"]}
        cls.grid = [c for c in cls.payload["cells"] if c["kind"] == "grid"]
        cls.cities = [c for c in cls.payload["cells"] if c["kind"] == "city"]

    def test_window_and_lattice(self) -> None:
        self.assertEqual(self.payload["window"]["start"], "2013-01-01")
        self.assertEqual(self.payload["step_deg"], 0.2)
        self.assertEqual(len(self.grid), 90)
        self.assertEqual(len(self.cities), 10)
        for c in self.payload["cells"]:
            self.assertEqual(c["n_days"], 4017)
            self.assertEqual(len(c["hn_by_month"]), 12)

    def test_named_cities_exist(self) -> None:
        for cid in ("hong_kong", "shenzhen", "guangzhou", "dongguan", "macau"):
            self.assertIn(cid, self.cells)
            self.assertEqual(self.cells[cid]["kind"], "city")

    def test_unique_fingerprints(self) -> None:
        self.assertGreaterEqual(self.model["unique_fingerprints"], 70)

    def test_nested_spatial_models(self) -> None:
        ols_r2 = self.model["ols"]["r2"]
        slx_r2 = self.model["slx"]["r2"]
        sar = self.model["sar_2sls"]
        self.assertGreater(ols_r2, 0.3)
        self.assertGreaterEqual(slx_r2, ols_r2 - 1e-6)
        self.assertGreater(slx_r2, 0.4)
        self.assertTrue(-1.0 < sar["rho"] < 1.5)
        self.assertLess(self.model["ols"]["beta"]["lat"]["beta"], 0)
        self.assertLess(self.model["ols"]["beta"]["elevation_m"]["beta"], 0.05)

    def test_spatial_dependence_is_present(self) -> None:
        self.assertGreater(self.model["moran_raw_tmin"]["I"], 0.2)
        self.assertGreater(self.model["moran_hn"]["I"], 0.1)

    def test_getis_ord_and_transect(self) -> None:
        gi = self.model["getis_ord_hn"]
        self.assertGreaterEqual(gi["n_hotspot_z_gt_1_96"] + gi["n_coldspot_z_lt_m1_96"], 1)
        transect = self.model["transect"]
        self.assertEqual(len(transect), 5)
        self.assertEqual(transect[0]["name"], "Waglan Island")
        self.assertEqual(transect[-1]["name"], "Guangzhou")

    def test_shenzhen_city_is_not_inside_the_hong_kong_box(self) -> None:
        self.assertEqual(self.cells["shenzhen"]["region"], "Shenzhen")
        self.assertEqual(self.cells["hong_kong"]["region"], "Hong Kong")
        self.assertEqual(self.cells["guangzhou"]["region"], "Guangzhou")

    def test_marine_south_holds_the_hot_nights(self) -> None:
        marine = self.model["regional_means"]["marine south"]["hn_mean"]
        inland = self.model["regional_means"]["Guangzhou"]["hn_mean"]
        self.assertGreater(marine, 8 * max(inland, 1))

    def test_jja_is_the_hot_night_season(self) -> None:
        hk = self.cells["hong_kong"]
        self.assertGreaterEqual(hk["jja_hn"], max(1, int(0.6 * hk["hn_total"])))

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "gate 3 freeze"):
            self.assertNotIn(banned, blob)
        self.assertIn("no health", self.payload["provenance"].lower())
        html = HTML_PATH.read_text()
        self.assertIn("Exposure only", html)
        self.assertIn("leaflet", html.lower())
        self.assertIn("month", html.lower())
        self.assertNotRegex(html, r"q\s*=\s*0\.")
        self.assertIn("transport Hong Kong", html)


if __name__ == "__main__":
    unittest.main()
