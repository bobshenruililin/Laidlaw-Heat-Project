#!/usr/bin/env python3
"""Tests for the peer-city thermal atlas. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "48_peer_cities_thermal_atlas.py"
JSON_PATH = ROOT / "outputs" / "peer_cities" / "peer_atlas.json"
JS_PATH = ROOT / "docs" / "peers" / "peers_embed.js"
HTML_PATH = ROOT / "docs" / "peers" / "index.html"


class PeerAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call(
            [sys.executable, str(SCRIPT), "--skip-fetch"],
            cwd=ROOT,
        )
        cls.payload = json.loads(JSON_PATH.read_text())

    def test_window_and_city_count(self) -> None:
        self.assertEqual(self.payload["window"]["start"], "2013-01-01")
        self.assertEqual(self.payload["window"]["DATA_START"], "2013-01-01")
        self.assertEqual(self.payload["window"]["DATA_END"], "2023-12-31")
        self.assertEqual(len(self.payload["cities"]), 16)
        for city in self.payload["cities"]:
            self.assertEqual(city["n_days"], 4017)

    def test_hong_kong_is_origin(self) -> None:
        hk = next(c for c in self.payload["cities"] if c["id"] == "hong_kong")
        self.assertEqual(hk["distance_to_hk_openmeteo"], 0.0)
        self.assertEqual(self.payload["distance_rank"][0]["id"], "hong_kong")

    def test_nearest_peers_are_taipei_or_pearl_river(self) -> None:
        near = {row["id"] for row in self.payload["distance_rank"][1:4]}
        self.assertTrue(near <= {"taipei", "shenzhen", "guangzhou", "hanoi", "haikou"})
        self.assertIn("shenzhen", near)
        self.assertIn(self.payload["distance_rank"][1]["id"], {"taipei", "shenzhen"})

    def test_singapore_never_crosses_hko_cold_or_hot_night(self) -> None:
        sg = next(c for c in self.payload["cities"] if c["id"] == "singapore")
        self.assertEqual(sg["cd_hko_total"], 0)
        self.assertEqual(sg["hn_hko_total"], 0)
        self.assertLess(sg["seasonal_amp"], 3)

    def test_phoenix_is_a_dry_heat_contrast(self) -> None:
        px = next(c for c in self.payload["cities"] if c["id"] == "phoenix")
        hk = next(c for c in self.payload["cities"] if c["id"] == "hong_kong")
        self.assertGreater(px["vhd_hko_total"], hk["vhd_hko_total"])
        self.assertLess(px["precip_mm_year"], hk["precip_mm_year"] / 2)
        self.assertGreater(px["distance_to_hk_openmeteo"], 2)

    def test_absolute_hko_flags_collapse_on_reanalysis(self) -> None:
        cal = self.payload["calibration"]
        self.assertEqual(cal["n_matched_days"], 4017)
        self.assertLess(cal["rmse_tmin"], 3)
        self.assertLess(cal["openmeteo_hn_total"], 50)
        self.assertGreater(cal["hko_hn_total"], 400)
        self.assertLess(cal["jaccard_hn"], 0.1)
        self.assertGreater(cal["bias_adjusted_openmeteo_hn"], 200)
        self.assertGreater(cal["openmeteo_apparent_hn_total"], cal["openmeteo_hn_total"])
        self.assertGreater(cal["openmeteo_apparent_hn_total"], cal["hko_hn_total"])

    def test_brisbane_winter_is_jja(self) -> None:
        july = [
            m for m in self.payload["months"]
            if m["city_id"] == "brisbane" and m["month"] == 7
        ]
        jan = [
            m for m in self.payload["months"]
            if m["city_id"] == "brisbane" and m["month"] == 1
        ]
        self.assertTrue(all(m["is_local_winter"] == 1 for m in july))
        self.assertTrue(all(m["is_local_winter"] == 0 for m in jan))

    def test_no_project_health_coefficients(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "gate 3 freeze"):
            self.assertNotIn(banned, blob)
        self.assertIn("no health", self.payload["provenance"].lower())
        self.assertGreaterEqual(len(self.payload["claim_boundaries"]), 4)

    def test_literature_has_real_dois_and_jingesi(self) -> None:
        cards = self.payload["literature"]
        dois = [card["doi"] for card in cards]
        self.assertTrue(all(d.startswith("10.") for d in dois))
        self.assertIn("10.1016/j.scs.2020.102131", dois)
        self.assertIn("10.1186/s12889-024-20144-1", dois)
        citations = " ".join(card["citation"] for card in cards)
        self.assertIn("Jingesi", citations)
        self.assertNotIn("Zhan et al", citations)

    def test_public_embed_exists(self) -> None:
        js = JS_PATH.read_text()
        self.assertTrue(js.startswith("window.PEER_ATLAS"))
        self.assertTrue(HTML_PATH.exists())
        html = HTML_PATH.read_text()
        self.assertIn("Exposure only", html)
        self.assertNotRegex(html, r"q\s*=\s*0\.")
        self.assertTrue((ROOT / "figures" / "peer_cities" / "climate_space_2013_2023.svg").exists())


if __name__ == "__main__":
    unittest.main()
