#!/usr/bin/env python3
"""Minimum detectable count ratio from the existing covariance ladder.

This is intern-owned identification work on delivered SEs. It is not a new
model, not a primary, and not a substitute for person-time or a stroke file.

Wald 80% power, two-sided 5%: MDE on the log-ratio scale is (1.96+0.84)*SE,
with SE recovered from the reported 95% interval.

Run from the repository root:

    python3 scripts/53_mde_from_uncertainty_ladder.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "release_chd_hf" / "tables" / "table4_uncertainty_ladder.csv"
OUT = ROOT / "outputs" / "auto_research" / "mde_from_uncertainty_ladder.csv"
NOTE = ROOT / "analysis_plan" / "auto_research" / "mde_from_ladder_2026-08-18.md"

Z_A = 1.959963984540054
Z_B = 0.841621233572914  # 80% power
K = Z_A + Z_B


def main() -> None:
    rows = list(csv.DictReader(SRC.open()))
    out_rows = []
    for r in rows:
        lo = float(r["rr_low"])
        hi = float(r["rr_high"])
        if lo <= 0 or hi <= 0:
            continue
        se_log = (math.log(hi) - math.log(lo)) / (2.0 * Z_A)
        mde = math.exp(K * se_log)
        rr = float(r["rr"])
        excludes = (lo > 1.0) or (hi < 1.0)
        out_rows.append(
            {
                "outcome": r["outcome"],
                "exposure_label": r["exposure_label"],
                "se_method_label": r["se_method_label"],
                "rr": f"{rr:.6f}",
                "rr_low": f"{lo:.6f}",
                "rr_high": f"{hi:.6f}",
                "se_log": f"{se_log:.6f}",
                "mde_rr_80pct": f"{mde:.4f}",
                "mde_pct_80pct": f"{100*(mde-1):.2f}",
                "observed_excludes_1": str(excludes).lower(),
                "data_status": r["data_status"],
                "result_class": "DERIVED_FROM_LADDER_SE — not a new model; not a primary",
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    # Core NW6 lines for the note
    nw6 = [x for x in out_rows if x["se_method_label"] == "NW6"]
    lines = [
        "# Minimum detectable count ratio from the existing ladder — 18 August 2026",
        "",
        "**Provenance:** derived from `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` (`HA_APPROVED_AGGREGATE`). Not a new fit. Not a primary.",
        "**Rule:** Wald MDE at 80% power, two-sided 5%, SE from the reported 95% interval. Count-scale MDE is exp((1.96+0.84)×SE_log).",
        "",
        "This table says what the 132-month design could have detected under each reported standard error, and did not protect at *q* < 0.05. It does not create person-time, stroke, or admission cause.",
        "",
        "## Newey–West lag-6 (analysis-of-record display)",
        "",
        "| Outcome | Contrast | Observed RR | MDE (80%) | Observed excludes 1 |",
        "|---|---|---:|---:|---|",
    ]
    for x in nw6:
        lines.append(
            f"| {x['outcome']} | {x['exposure_label']} | {float(x['rr']):.3f} "
            f"({float(x['rr_low']):.3f}–{float(x['rr_high']):.3f}) | "
            f"{x['mde_rr_80pct']} ({x['mde_pct_80pct']}%) | {x['observed_excludes_1']} |"
        )
    lines.extend(
        [
            "",
            f"Machine table: `{OUT.relative_to(ROOT)}`.",
            "",
            "Permutation and future-month negative-control checks are not in this file.",
            "",
        ]
    )
    NOTE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(out_rows)} rows)")
    print(f"Wrote {NOTE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
