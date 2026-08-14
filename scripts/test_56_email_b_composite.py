#!/usr/bin/env python3
"""Tests for the Email B composite figure. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "56_email_b_composite.py"
SVG = ROOT / "figures" / "monthly_bridge" / "email_b_composite.svg"
META = ROOT / "outputs" / "monthly_bridge" / "email_b_composite.json"


class EmailBCompositeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.svg = SVG.read_text()
        cls.meta = json.loads(META.read_text())

    def test_three_panels_and_banner(self) -> None:
        self.assertIn("A. Monthly mean Tmin travels", self.svg)
        self.assertIn("B. Monthly 28°C-night counts do not", self.svg)
        self.assertIn("C. Daily Jaccard collapses at 28°C", self.svg)
        self.assertIn("No hospital counts", self.svg)
        self.assertIn("Live paper stays on Headquarters", self.svg)

    def test_key_numbers_present(self) -> None:
        self.assertIn("0.045", self.svg)
        self.assertIn("0.031", self.svg)
        self.assertIn("26.3", self.svg)
        self.assertIn("26.4", self.svg)

    def test_no_health_coefficients(self) -> None:
        blob = (self.svg + json.dumps(self.meta)).lower()
        for banned in ("1.022", "1.073", "q =", "incidence"):
            self.assertNotIn(banned, blob)
        self.assertIn("do not treat 0.045 as a health attenuation factor", blob)

    def test_not_form_2a(self) -> None:
        self.assertIn("Not form 2a", self.svg)
        self.assertIn("not_to_send_until", self.meta)


if __name__ == "__main__":
    unittest.main()
