#!/usr/bin/env python3
"""Tests for the PRD field laboratory. No network. No health claims."""
from __future__ import annotations

import importlib.util
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "51_prd_field_laboratory.py"
JSON_PATH = ROOT / "outputs" / "prd_field" / "prd_field.json"
HTML_PATH = ROOT / "docs" / "field" / "index.html"


def load_mod():
    spec = importlib.util.spec_from_file_location("field51", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FieldMathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = load_mod()
        cls.rng = np.random.default_rng(0)

    def test_theil_sen_recovers_slope(self) -> None:
        x = np.arange(11.0)
        y = 2.5 * x + 10.0
        self.assertAlmostEqual(self.m.theil_sen_slope(x, y), 2.5, places=9)
        self.assertEqual(self.m.mann_kendall_s(y), 55)

    def test_harmonic_phase_near_known_peak(self) -> None:
        t = np.arange(365 * 3, dtype=float)
        omega = 2.0 * math.pi / 365.25
        peak = 200.0
        y = 20.0 + 5.0 * np.cos(omega * t - peak * omega)
        amp, t_peak, a0 = self.m.harmonic_amp_phase(y, t)
        self.assertAlmostEqual(amp, 5.0, places=2)
        self.assertAlmostEqual(a0, 20.0, places=2)
        err = min(abs(t_peak - peak), abs(t_peak - peak + 365.25), abs(t_peak - peak - 365.25))
        self.assertLess(err, 2.0)

    def test_eof_recovers_rank1(self) -> None:
        rng = np.random.default_rng(1)
        true = np.linspace(-1.0, 1.0, 20)
        pc = rng.normal(size=300)
        x = np.outer(pc, true) + 0.01 * rng.normal(size=(300, 20))
        eofs, pcs, var, _ = self.m.eof_svd(x, np.full(20, 22.3))
        self.assertGreater(abs(np.corrcoef(eofs[0], true)[0, 1]), 0.99)
        self.assertGreater(var[0], 0.95)
        self.assertAlmostEqual(float(var.sum()), 1.0, places=6)

    def test_kmeans_separates_blobs(self) -> None:
        rng = np.random.default_rng(2)
        a = rng.normal(size=(40, 2))
        b = rng.normal(size=(40, 2)) + 6.0
        x = np.vstack([a, b])
        labels, _, inertia = self.m.kmeans(x, 2, rng)
        self.assertEqual(len(set(labels[:40])), 1)
        self.assertEqual(len(set(labels[40:])), 1)
        self.assertNotEqual(labels[0], labels[40])
        self.assertGreater(inertia, 0.0)

    def test_mutual_info_identical_gt_independent(self) -> None:
        rng = np.random.default_rng(3)
        x = rng.integers(0, 2, size=4000)
        y = rng.integers(0, 2, size=4000)
        self.assertGreater(self.m.binary_mi(x, x), 0.9)
        self.assertGreater(self.m.binary_mi(x, x), self.m.binary_mi(x, y) + 0.7)

    def test_spell_and_wasserstein(self) -> None:
        flag = np.array([1, 1, 1, 0, 0, 1, 1, 0])
        s = self.m.spell_stats(flag)
        self.assertEqual(s["n_spells"], 2)
        self.assertEqual(s["max"], 3)
        self.assertAlmostEqual(s["mean"], 2.5)
        a = np.array([0.0, 1.0, 2.0, 3.0])
        b = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(self.m.wasserstein1(a, b), 1.0, places=9)
        ev = self.m.shannon_evenness(np.array([1.0, 0.0, 0.0, 0.0]))
        self.assertLess(ev["evenness"], 0.05)
        ev2 = self.m.shannon_evenness(np.ones(8))
        self.assertGreater(ev2["evenness"], 0.99)


class FieldRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.payload = json.loads(JSON_PATH.read_text())
        cls.model = cls.payload["model"]
        cls.cells = cls.payload["cells"]

    def test_window_and_lattice(self) -> None:
        self.assertEqual(self.payload["window"]["start"], "2013-01-01")
        self.assertEqual(len(self.cells), 90)
        self.assertEqual(self.payload["window"]["n_days"], 4017)
        self.assertEqual(len(self.payload["methods"]), 8)
        self.assertEqual(len(self.model["monthly_pc"]), 132)
        self.assertEqual(len(self.cells[0]["harmonic_by_month"]), 12)
        self.assertLessEqual(self.model["trend"]["n_ci_excludes_zero"], 90)

    def test_eof_is_a_real_decomposition(self) -> None:
        var = self.model["eof"]["variance_frac"]
        self.assertGreater(var[0], 0.15)
        self.assertGreater(self.model["eof"]["cumulative_3"], 0.4)
        self.assertGreater(sum(var), 0.95)
        self.assertTrue(-1.0 <= self.model["eof"]["eof1_lat_corr"] <= 1.0)

    def test_clusters_cover_the_grid(self) -> None:
        names = {c["cluster_name"] for c in self.cells}
        self.assertIn("marine", names)
        self.assertEqual(sum(s["n"] for s in self.model["clusters"]["summary"]), 90)

    def test_hot_nights_are_spatially_uneven(self) -> None:
        self.assertLess(self.model["entropy"]["evenness"], 0.95)
        marine = [c for c in self.cells if c["region"] == "marine south"]
        inland = [c for c in self.cells if c["region"] == "Guangzhou"]
        self.assertGreater(
            np.mean([c["hn_total"] for c in marine]),
            8 * max(1.0, float(np.mean([c["hn_total"] for c in inland]))),
        )

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "gate 3 freeze"):
            self.assertNotIn(banned, blob)
        self.assertIn("no health", self.payload["provenance"].lower())
        html = HTML_PATH.read_text()
        self.assertIn("Exposure only", html)
        self.assertIn("exploratory page", html)
        self.assertNotIn("A human PhD usually ships", html)
        self.assertIn("strong_cut_embed.js", html)
        self.assertIn("harder cut", html.lower())
        self.assertIn("leaflet", html.lower())
        self.assertNotRegex(html, r"q\s*=\s*0\.")
        self.assertIn("transport Hong Kong", html)


if __name__ == "__main__":
    unittest.main()
