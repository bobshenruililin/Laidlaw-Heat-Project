#!/usr/bin/env python3
"""Tests for the threshold-does-not-travel demo. No network. No health claims."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "53_threshold_does_not_travel.py"
JSON_PATH = ROOT / "outputs" / "threshold_demo" / "threshold_does_not_travel.json"
HTML_PATH = ROOT / "docs" / "demo" / "index.html"
JS_PATH = ROOT / "docs" / "demo" / "demo_embed.js"


class ThresholdDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(SCRIPT)], cwd=ROOT)
        cls.payload = json.loads(JSON_PATH.read_text())
        cls.html = HTML_PATH.read_text()
        cls.js = JS_PATH.read_text()

    def test_window(self) -> None:
        self.assertEqual(self.payload["window"]["n_days"], 4017)
        self.assertEqual(len(self.payload["thresholds_c"]), 25)
        self.assertEqual(self.payload["thresholds_c"][0], 20.0)
        self.assertEqual(self.payload["thresholds_c"][-1], 32.0)
        self.assertIn(28.0, self.payload["thresholds_c"])

    def test_three_objects_at_28(self) -> None:
        a = self.payload["anchors_at_28"]
        self.assertEqual(a["hko_tmin"], 449)
        self.assertEqual(a["era5_hk_tmin"], 17)
        self.assertEqual(a["era5_hk_atmin"], 1453)
        self.assertAlmostEqual(a["jaccard"], 0.031, places=3)
        self.assertLess(a["bias_openmeteo_minus_hko_tmin"], -1.0)

    def test_jaccard_is_a_function_of_threshold(self) -> None:
        jac = self.payload["overlap_hko_vs_era5_hk"]["jaccard"]
        t = self.payload["thresholds_c"]
        i24 = t.index(24.0)
        i28 = t.index(28.0)
        self.assertIsNotNone(jac[i24])
        self.assertIsNotNone(jac[i28])
        self.assertGreater(jac[i24], jac[i28])
        self.assertGreater(jac[i24], 0.7)
        self.assertLess(jac[i28], 0.05)

    def test_silent_union_is_not_perfect_agreement(self) -> None:
        jac = self.payload["overlap_hko_vs_era5_hk"]["jaccard"]
        unions = self.payload["overlap_hko_vs_era5_hk"]["union"]
        for j, u in zip(jac, unions):
            if u == 0:
                self.assertIsNone(j)

    def test_equivalent_threshold_is_below_28(self) -> None:
        eq = self.payload["equivalent_thresholds"]["era5_tmin_matching_hko_449"]
        self.assertLess(eq["threshold_c"], 28.0)
        self.assertGreater(eq["threshold_c"], 25.0)
        self.assertLess(eq["abs_err"], 80)

    def test_marine_share_rises_toward_28(self) -> None:
        t = self.payload["thresholds_c"]
        share = self.payload["series"]["marine_share_cellnights"]
        s24, s28 = share[t.index(24.0)], share[t.index(28.0)]
        self.assertIsNotNone(s24)
        self.assertIsNotNone(s28)
        self.assertGreater(s28, s24)
        self.assertGreater(s28, 0.5)

    def test_field_has_ninety_cells(self) -> None:
        self.assertEqual(self.payload["grid"]["n_cells"], 90)
        self.assertEqual(len(self.payload["grid"]["cells"]), 90)
        self.assertEqual(self.payload["grid"]["hq_cell"], "p_22.3_114.1")
        self.assertEqual(len(self.payload["grid"]["cells"][0]["counts"]), 25)

    def test_daily_series_length(self) -> None:
        d = self.payload["daily"]
        self.assertEqual(len(d["hko_tmin_tenths"]), 4017)
        self.assertEqual(len(d["era5_hk_tmin_tenths"]), 4017)
        self.assertEqual(len(d["year"]), 4017)

    def test_page_is_not_a_programme_substitute(self) -> None:
        blob = self.html.lower()
        self.assertIn("exposure descriptives only", blob)
        self.assertIn("not", blob)
        self.assertIn("form 2a", blob)
        self.assertIn("bishai", blob)
        self.assertNotIn("q_value", blob)
        self.assertNotIn("hospitalisation ratio", blob)
        self.assertIn("THRESHOLD_DEMO", self.js)
        hub = (ROOT / "docs" / "index.html").read_text().lower()
        self.assertIn("./demo/", hub)

    def test_max_jaccard_against_fixed_station_set(self) -> None:
        mx = self.payload["max_jaccard_hko28_vs_era5_t"]
        self.assertGreater(mx["jaccard"], 0.40)
        self.assertLess(mx["jaccard"], 0.60)
        self.assertLess(mx["threshold_c"], 28.0)
        a = self.payload["anchors_at_28"]
        self.assertLess(a["jaccard"], 0.05)
        self.assertGreater(a["ppv_era5_vs_hko28"], 0.7)
        self.assertEqual(a["intersection"], 14)
        rec = self.payload["bias_adjusted_hko28"]
        self.assertEqual(rec["n_pred"], 378)
        self.assertGreater(rec["jaccard"], 0.40)
        self.assertGreater(rec["jaccard"], a["jaccard"])
        fig = ROOT / "figures" / "threshold_demo" / "exceedance_and_agreement.svg"
        self.assertTrue(fig.exists())
        self.assertIn("Max Jaccard", fig.read_text())

    def test_no_health_coefficients_in_payload(self) -> None:
        blob = json.dumps(self.payload).lower()
        for banned in ("q_value", "incidence_rate_ratio", "1.022", "stroke coefficient"):
            self.assertNotIn(banned, blob)
        self.assertIn("exposure descriptives only", self.payload["provenance"].lower())

    def test_jaccard_helper_empty_union(self) -> None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("t53", SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        import numpy as np
        out = mod.jaccard_vs_threshold(
            np.array([10.0, 11.0]),
            np.array([10.5, 11.5]),
            np.array([40.0]),
        )
        self.assertEqual(out["union"], [0])
        self.assertIsNone(out["jaccard"][0])


if __name__ == "__main__":
    unittest.main()
