#!/usr/bin/env python3
"""Tests for the year-shift teaching object. No invented HA rows."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "63_year_shift_negative_control.py"
JSON_PATH = ROOT / "outputs" / "year_shift" / "year_shift_negative_control.json"
R_STATUS = ROOT / "outputs" / "year_shift" / "health_refit_status.json"


class YearShiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.p = json.loads(JSON_PATH.read_text())

    def test_identifying_share_does_not_collapse(self) -> None:
        by = {e["encoding"]: e for e in self.p["encodings"]}
        hn = by["hot_nights"]
        self.assertAlmostEqual(hn["identifying_share_original"], 0.2883, places=3)
        self.assertIsNotNone(hn["identifying_share_year_shifted"])
        self.assertLess(abs(hn["delta"]), 0.05)
        self.assertEqual(hn["n_months_shifted"], 132)

    def test_health_refit_is_parked_without_panels(self) -> None:
        health = self.p["health_refit"]
        panels = (ROOT / "data_processed" / "chd_analysis_panel.csv").exists()
        if panels:
            self.assertIn(health["status"], {"PANELS_PRESENT", "RAN", "HOOK_FAILED"})
        else:
            self.assertEqual(health["status"], "PARKED_NO_PANEL")
            self.assertTrue(R_STATUS.exists())
            status = json.loads(R_STATUS.read_text())
            self.assertEqual(status["status"], "PARKED_NO_PANEL")
            self.assertFalse(status["headline"])
            self.assertEqual(status["gate3"], "open")

    def test_boundaries(self) -> None:
        blob = json.dumps(self.p).lower()
        self.assertIn("calendar-month", blob)
        self.assertIn("gate 3 stays open", blob)
        self.assertIn("do not chase 1.022", blob)
        self.assertNotIn("confirmatory", blob)
        self.assertIsNone(self.p["health_refit"].get("rr"))


if __name__ == "__main__":
    unittest.main()
