#!/usr/bin/env python3
"""Tests for first-wave HM/CM effective rank. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "58_hm_cm_effective_rank.py"
JSON_PATH = ROOT / "outputs" / "hm_cm_rank" / "hm_cm_effective_rank.json"
FIG = ROOT / "figures" / "hm_cm_rank" / "hm_cm_scree.svg"


class HmCmRankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())

    def test_file_is_twelve_binaries_not_ninety_eight(self) -> None:
        self.assertEqual(self.p["window"]["n_months"], 132)
        self.assertEqual(self.p["n_named_binaries_on_disk"], 12)
        self.assertEqual(self.p["n_nondegenerate"], 11)
        self.assertEqual(self.p["degenerate"], ["CM05"])
        self.assertIn("not 98 tests", self.p["punchline"])

    def test_cm05_is_the_zero_column(self) -> None:
        cm05 = next(f for f in self.p["flags"] if f["name"] == "CM05")
        self.assertEqual(cm05["n_months_on"], 0)
        self.assertTrue(cm05["degenerate"])

    def test_effective_rank_is_about_four(self) -> None:
        self.assertAlmostEqual(self.p["effective_rank"], 3.92, places=2)
        self.assertGreater(self.p["effective_rank"], 3.5)
        self.assertLess(self.p["effective_rank"], 5.0)
        self.assertGreater(self.p["pc1_pc2_share"], 0.60)
        self.assertLess(self.p["pc1_pc2_share"], 0.75)
        self.assertEqual(len(self.p["eigenvalues"]), 11)

    def test_heat_never_cofires_with_cold(self) -> None:
        self.assertEqual(self.p["max_heat_cold_jaccard"], 0.0)
        self.assertEqual(len(self.p["heat_names"]), 7)
        self.assertEqual(len(self.p["cold_names"]), 4)

    def test_known_nested_subsets(self) -> None:
        pairs = {(s["inner"], s["outer"]) for s in self.p["nested_subsets"]}
        self.assertIn(("HM15", "HM08"), pairs)
        self.assertIn(("CM08", "CM03"), pairs)
        self.assertIn(("CM15", "CM30"), pairs)
        self.assertIn(("HM08", "HM32"), pairs)

    def test_hm23_event_starts_are_not_in_the_rank(self) -> None:
        self.assertEqual(self.p["hm23_event_starts"]["n_months_with_start"], 30)
        self.assertEqual(self.p["hm23_event_starts"]["n_event_starts_total"], 38)
        self.assertEqual(self.p["hm23_event_starts"]["max_starts_in_a_month"], 3)
        self.assertNotIn("HM23_event_starts", self.p["live_names"])

    def test_no_health_coefficients_and_no_licence_to_refit(self) -> None:
        blob = json.dumps(self.p).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "1.073"):
            self.assertNotIn(banned, blob)
        self.assertIn("do not reopen the outcome panel", blob)
        self.assertIn("exposure descriptives only", self.p["provenance"].lower())

    def test_figure_exists(self) -> None:
        self.assertTrue(FIG.exists())
        svg = FIG.read_text()
        self.assertIn("Eleven flags, about four dimensions", svg)
        self.assertIn("Heat never co-fires with cold", svg)


if __name__ == "__main__":
    unittest.main()
