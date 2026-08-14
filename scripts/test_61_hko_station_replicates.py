#!/usr/bin/env python3
"""Tests for public HKO station replicates. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "61_hko_station_replicates.py"
JSON_PATH = ROOT / "outputs" / "station_replicates" / "station_replicates.json"
SVG = ROOT / "docs" / "id" / "hko_station_hot_nights.svg"


class StationReplicateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())

    def test_hko_anchors_hold(self) -> None:
        hko = self.p["stations"]["HKO"]["complete"]
        self.assertEqual(hko["hot_nights"], 449)
        self.assertEqual(hko["cold_days"], 145)
        self.assertEqual(self.p["window"]["n_days"], 4017)

    def test_kings_park_is_not_headquarters(self) -> None:
        kp = self.p["stations"]["KP"]["complete"]
        pair = self.p["pairs"]["HKO_vs_KP_hot_nights"]
        self.assertLess(kp["hot_nights"], 449)
        self.assertEqual(pair["n_b_only"], 0)
        self.assertGreater(pair["n_a_only"], 100)
        self.assertGreater(pair["jaccard"], 0.4)
        self.assertLess(pair["jaccard"], 0.6)

    def test_waglan_is_public_hko_not_era5(self) -> None:
        wgl = self.p["stations"]["WGL"]["complete"]
        pair = self.p["pairs"]["HKO_vs_WGL_hot_nights"]
        self.assertLess(wgl["hot_nights"], 200)
        self.assertNotEqual(wgl["hot_nights"], 252)
        self.assertLess(pair["jaccard"], 0.3)

    def test_boundaries(self) -> None:
        blob = json.dumps(self.p).lower()
        self.assertIn("not era5", blob)
        self.assertIn("not a substitute", blob)
        self.assertNotIn("1.022", blob)
        self.assertTrue(SVG.exists())
        self.assertIn("Not ERA5", SVG.read_text())


if __name__ == "__main__":
    unittest.main()
