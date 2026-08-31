#!/usr/bin/env python3
"""Fit Hogan Model 2 (rainfall + RH) and Model 3 (climatology-relative days).

Requires the gitignored governed CHD/HF monthly panels. This workspace does not
contain them. On a machine that holds:

  data_processed/chd_analysis_panel.csv
  data_processed/hf_analysis_panel.csv

run:

  Rscript scripts/53_hogan_models_rh_rain.R
  Rscript scripts/68_hogan_model3_climatology.R

Does not invent coefficients. Does not write health microdata. Does not
reconstruct monthly counts from Figure 1 or annual totals.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHD = ROOT / "data_processed" / "chd_analysis_panel.csv"
HF = ROOT / "data_processed" / "hf_analysis_panel.csv"
CLIM = ROOT / "data_processed" / "hogan_climatology_day_counts_2013_2023.csv"


def main() -> int:
    missing = [p for p in (CHD, HF) if not p.exists()]
    if missing:
        print(
            "Governed analysis panels are not in this workspace:\n  "
            + "\n  ".join(str(p) for p in missing)
            + "\nModel 2 and Model 3 are specified in Methods. "
            "Do not invent count ratios. Do not digitize Figure 1. "
            "Place the gitignored panels, then run:\n"
            "  Rscript scripts/53_hogan_models_rh_rain.R\n"
            "  Rscript scripts/68_hogan_model3_climatology.R",
            file=sys.stderr,
        )
        if not CLIM.exists():
            print(f"Missing climatology file {CLIM}", file=sys.stderr)
            return 2
        return 1
    for script in (
        ROOT / "scripts" / "53_hogan_models_rh_rain.R",
        ROOT / "scripts" / "68_hogan_model3_climatology.R",
    ):
        proc = subprocess.run(["Rscript", str(script)], cwd=str(ROOT))
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
