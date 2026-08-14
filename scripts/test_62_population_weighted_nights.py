#!/usr/bin/env python3
"""Tests for WorldPop-weighted ERA5 nights. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "62_population_weighted_nights.py"
JSON_PATH = ROOT / "outputs" / "population_weighted_nights" / "population_weighted_nights.json"
SVG = ROOT / "docs" / "id" / "population_weighted_south_share.svg"


class PopulationWeightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())

    def test_grid_and_worldpop_anchors(self) -> None:
        self.assertEqual(self.p["grid"]["n_cells"], 30)
        self.assertEqual(self.p["grid"]["hn_total"], 2935)
        self.assertGreater(self.p["worldpop"]["n_pixels"], 1000)
        self.assertGreater(self.p["worldpop"]["sum_people_in_file"], 6_000_000)
        self.assertLess(self.p["worldpop"]["sum_people_in_file"], 10_000_000)

    def test_people_are_not_where_the_marine_flag_is(self) -> None:
        s = self.p["shares"]
        self.assertGreater(s["unweighted_hn_south"], 0.55)
        self.assertLess(s["population_weighted_hn_south"], s["unweighted_hn_south"])
        self.assertLess(s["population_share_south"], 0.35)

    def test_boundaries(self) -> None:
        blob = json.dumps(self.p).lower()
        self.assertIn("exposure descriptives only", blob)
        self.assertIn("not a marmot", blob)
        self.assertNotIn("1.022", blob)
        self.assertTrue(SVG.exists())
        self.assertIn("Not a hospital map", SVG.read_text())


if __name__ == "__main__":
    unittest.main()
