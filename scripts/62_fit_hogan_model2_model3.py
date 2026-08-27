#!/usr/bin/env python3
"""Fit Hogan Model 2 (rainfall + RH) and Model 3 (climatology-relative days).

Requires the gitignored governed CHD/HF monthly panels. This workspace does not
contain them. Run on the analysis machine that holds:

  data_processed/chd_analysis_panel.csv
  data_processed/hf_analysis_panel.csv

Does not invent coefficients. Does not write health microdata.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIM = ROOT / "data_processed" / "hogan_climatology_day_counts_2013_2023.csv"
CHD = ROOT / "data_processed" / "chd_analysis_panel.csv"
HF = ROOT / "data_processed" / "hf_analysis_panel.csv"


def main() -> int:
    missing = [p for p in (CHD, HF) if not p.exists()]
    if missing:
        print(
            "Governed analysis panels are not in this workspace:\n  "
            + "\n  ".join(str(p) for p in missing)
            + "\nModel 2 and Model 3 are specified in Methods. "
            "Do not invent count ratios. Copy "
            f"{CLIM.name} onto the analysis machine and refit there.",
            file=sys.stderr,
        )
        if not CLIM.exists():
            print(f"Missing climatology file {CLIM}", file=sys.stderr)
            return 2
        return 1
    print("Panels present. Wire this script to scripts/31_cvd_core_robustness.R on the analysis machine.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
