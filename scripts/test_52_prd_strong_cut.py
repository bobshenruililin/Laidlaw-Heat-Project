#!/usr/bin/env python3
"""Tests for the PRD strong-cut diagnostics. No network. No health claims."""
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
SCRIPT = ROOT / "scripts" / "52_prd_strong_cut.py"
JSON_PATH = ROOT / "outputs" / "prd_field" / "prd_strong_cut.json"


def load_mod():
    spec = importlib.util.spec_from_file_location("cut52", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class StrongCutMathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = load_mod()

    def test_bh_keeps_the_smallest_p(self) -> None:
        p = np.array([0.001, 0.2, 0.3, 0.4, 0.5])
        keep = self.m.benjamini_hochberg(p, q=0.10)
        self.assertTrue(keep[0])
        self.assertFalse(keep[1:].any())

    def test_circular_mean_of_aligned_phases(self) -> None:
        doy = np.full(20, 200.0)
        s = self.m.circular_stats(doy)
        self.assertLess(abs(s["mean_doy"] - 200.0), 0.5)
        self.assertLess(s["sd_days"], 0.5)
        self.assertGreater(s["resultant_length"], 0.99)

    def test_odds_ratio_independence_near_one(self) -> None:
        rng = np.random.default_rng(0)
        hn = rng.integers(0, 2, size=8000)
        vhd = rng.integers(0, 2, size=8000)
        or_ = self.m.odds_ratio(hn, vhd)
        self.assertGreater(or_["odds_ratio"], 0.7)
        self.assertLess(or_["odds_ratio"], 1.4)

    def test_odds_ratio_identical_is_large(self) -> None:
        x = np.array([1, 1, 1, 0, 0, 0, 1, 0] * 50)
        or_ = self.m.odds_ratio(x, x)
        self.assertEqual(or_["odds_ratio"], "inf")

    def test_mann_kendall_trend_has_small_p(self) -> None:
        y = np.arange(11.0)
        s, z, p = self.m.mann_kendall_p(y)
        self.assertGreater(s, 0)
        self.assertLess(p, 0.01)

    def test_xcorr_peak_at_true_lag(self) -> None:
        rng = np.random.default_rng(1)
        a = rng.normal(size=400)
        b = np.zeros(400)
        b[2:] = a[:-2]
        lags = self.m.xcorr_lags(a, b, 3)
        peak = max(lags, key=lambda d: d["r"])
        self.assertEqual(peak["lag_days"], 2)
        self.assertGreater(peak["r"], 0.8)


class StrongCutRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.payload = json.loads(JSON_PATH.read_text())

    def test_eof_survives_year_holdout(self) -> None:
        h = self.payload["eof_year_holdout"]
        self.assertGreater(h["pattern_r_min"], 0.95)
        self.assertGreater(h["var_frac_min"], 0.85)
        self.assertEqual(len(h["by_year"]), 11)

    def test_block_bootstrap_keeps_eof1_dominant(self) -> None:
        b = self.payload["eof_block_bootstrap"]
        self.assertGreater(b["var1_p05"], 0.80)
        self.assertLess(b["var1_p95"], 0.99)

    def test_fdr_is_stricter_than_raw_or_ci_count(self) -> None:
        f = self.payload["mann_kendall_fdr"]
        self.assertLessEqual(f["n_fdr_q_0_10"], f["n_raw_p_lt_0_10"])
        if f["script51_n_ci_excludes_zero"] is not None:
            self.assertLessEqual(f["n_fdr_q_0_10"], f["script51_n_ci_excludes_zero"])
        self.assertGreater(f["min_p"], 0.001)
        self.assertEqual(f["n_fdr_q_0_10"], 0)

    def test_inland_hot_night_is_almost_always_a_hot_day(self) -> None:
        gz = self.payload["compound_extremes"]["guangzhou"]
        marine = self.payload["compound_extremes"]["marine_south"]
        self.assertGreater(gz["p_vhd_given_hn"], 0.9)
        self.assertLess(marine["p_vhd_given_hn"], 0.05)

    def test_phase_is_locked_to_july(self) -> None:
        d = self.payload["circular_phase"]["marine_minus_guangzhou_days"]
        self.assertLess(d, 5.0)
        mean = self.payload["circular_phase"]["all"]["mean_doy"]
        self.assertTrue(190 <= mean <= 215)

    def test_network_collapses_after_removing_eof1(self) -> None:
        n = self.payload["network_after_eof1"]
        self.assertGreater(n["n_edges_raw"], 1000)
        self.assertLess(n["n_edges_after_removing_eof1"], 0.1 * n["n_edges_raw"])

    def test_no_health_coefficients(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure only", self.payload["provenance"].lower())


if __name__ == "__main__":
    unittest.main()
