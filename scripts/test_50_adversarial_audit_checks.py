#!/usr/bin/env python3
"""Invariant checks for scripts/50_adversarial_audit_checks.py.

Binds the audit's load-bearing kills to rebuildable numbers. No governed
monthly counts. No new health model.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "adversarial_audit" / "adversarial_audit_checks.json"


def main() -> int:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "50_adversarial_audit_checks.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    d = json.loads(OUT.read_text())
    assert d["provenance"]["new_health_models"] is False
    assert d["provenance"]["governed_counts_read"] is False

    # Gamma: anomaly CI contains the crude seasonal gradient.
    for row in d["gamma_seasonal_containment"]:
        assert row["anomaly_ci_contains_crude_seasonal_slope"] is True

    flu = d["gamma_flu_inside_month_fe"]
    assert flu["flu_variation_share_remaining_after_full_controls"] > 0.40
    chd_flu = next(r for r in flu["rows"] if r["outcome"] == "chd")
    assert math.isclose(chd_flu["rr"], 1.67348469190786, rel_tol=0, abs_tol=1e-12)
    assert chd_flu["p_value"] < 0.001

    # Delta: observed/detectable is z/2.8.
    assert d["delta_observed_power_identity"]["max_abs_gap"] < 1e-4

    # Delta: HF cold window ladder has both excluding and including rungs.
    ladder = d["delta_hf_cold_window_ladder"]
    n_excl = sum(1 for r in ladder if r["excludes_1"])
    n_incl = sum(1 for r in ladder if not r["excludes_1"])
    assert n_excl >= 4
    assert n_incl == 4
    including = {r["scenario"] for r in ladder if not r["excludes_1"]}
    assert including == {
        "trend_ns8",
        "year_fixed_effects",
        "drop_first_12_months",
        "drop_first_24_months",
    }

    # Beta: stipulated dip is only partly spanned by released phase dummies.
    span = d["beta_inversion_genericity"][
        "share_of_stipulated_dip_spanned_by_released_phase_dummies"
    ]
    assert 0.30 < span < 0.45

    # Beta: HF non-cold inversion is not coherent.
    hf = d["beta_inversion_by_outcome"]["by_outcome"]["hf"]
    chd = d["beta_inversion_by_outcome"]["by_outcome"]["chd"]
    assert hf["cv"] > 0.25
    assert chd["cv"] < 0.10

    # Sparsity kill failed: cold-day identifying variance is not a few winters.
    cold = d["delta_identifying_variance_sparsity"]["cold_days"]
    assert cold["year_groups_for_80pct"] >= 8
    assert cold["top_year_group_share"] < 0.20

    print("PASS scripts/test_50_adversarial_audit_checks.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
