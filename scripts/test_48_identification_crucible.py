#!/usr/bin/env python3
"""Invariant checks for scripts/48_identification_crucible.py.

No governed HA counts. Re-runs the diagnostic and asserts linear-algebra
facts that the crucible proof depends on.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "identification_crucible"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "48_identification_crucible.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads((OUT / "identification_summary.json").read_text())
    ident = {r["exposure"]: r for r in _read(OUT / "exposure_residual_variation.csv")}
    det = _read(OUT / "bh_detectability.csv")
    disc = _read(OUT / "se_method_discordance.csv")

    assert summary["n_months"] == 132
    assert summary["bh_tests"] == 12
    assert summary["all_q_gt_019"] is True
    assert summary["min_p"] > 0.03
    assert summary["p_needed_rank1_for_q05"] == 0.05 / 12
    assert summary["min_p_over_rank1_threshold"] > 7.0
    assert 0.96 < summary["geography"]["cold_days_djf_share"] < 1.0
    assert summary["geography"]["cold_days_total"] == 145.0
    assert summary["geography"]["july_hot_nights_min"] == 1.0
    assert summary["geography"]["july_hot_nights_max"] == 25.0
    assert summary["provenance"]["new_health_models"] is False
    assert summary["provenance"]["governed_counts_read"] is False

    # Continuous temperature is almost a calendar-month function.
    assert 0.94 < float(ident["mean_temp"]["r2_month_fe"]) < 0.97
    assert float(ident["mean_temp"]["variation_share_remaining_after_full_controls"]) < 0.05
    # Extreme-day counts retain substantial within-month-of-year variation.
    assert float(ident["hot_nights"]["r2_month_fe"]) < 0.80
    assert float(ident["cold_days"]["r2_month_fe"]) < 0.60
    assert float(ident["cold_days"]["variation_share_remaining_after_full_controls"]) > 0.40
    assert int(ident["cold_days"]["nonzero_months"]) == 29
    assert int(ident["hot_nights"]["nonzero_months"]) == 57

    # BH recomputation matches the release q-values.
    for row in det:
        assert math.isclose(
            float(row["q_value_release"]),
            float(row["q_value_recomputed"]),
            rel_tol=0,
            abs_tol=1e-12,
        )

    hf_cold = next(r for r in disc if r["outcome"] == "hf" and r["pathway_id"] == "P04B")
    chd_hn = next(r for r in disc if r["outcome"] == "chd" and r["pathway_id"] == "P04A")
    assert hf_cold["se_concordant_exclude_1"] == "True"
    assert chd_hn["n_methods_excluding_1"] == "2"
    assert chd_hn["se_concordant_exclude_1"] == "False"

    print("PASS scripts/test_48_identification_crucible.py")
    print(proc.stdout.split("Exposure residual variation:")[0].strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
