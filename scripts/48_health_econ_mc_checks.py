#!/usr/bin/env python3
"""Regression checks on SYNTHETIC_CALIBRATION outputs. Not health findings."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "health_econ"


def main() -> int:
    errors = []
    summ = pd.read_csv(OUT / "cycle1_mc_summary.csv")
    gates = json.loads((OUT / "cycle1_mc_gates.json").read_text())
    varsigma = json.loads((OUT / "varsigma_hko.json").read_text())
    if gates.get("provenance") != "SYNTHETIC_CALIBRATION":
        errors.append("gates provenance")
    if gates.get("monetisation_permitted") is not False:
        errors.append("monetisation must be false")
    if gates.get("gate3_input") is not False:
        errors.append("must not be a Gate 3 input")
    if len(summ) < 40:
        errors.append(f"expected >=40 scenarios, got {len(summ)}")
    if float(summ["frac_ok"].min()) < 0.99:
        errors.append("fit failures")
    size = float(gates.get("HE01_size") or 0)
    if not (0.02 <= size <= 0.10):
        errors.append(f"HE-01 size off-nominal: {size}")
    if varsigma.get("data_status") != "REAL_PUBLIC_HKO":
        errors.append("varsigma provenance")
    if not (varsigma.get("varsigma", 0) < 0):
        errors.append("expected negative subtropical variance gradient")
    if "HKD" in json.dumps(gates) or "$" in json.dumps(gates):
        errors.append("currency slipped into gates")
    if errors:
        print("FAIL", errors)
        return 1
    print("PASS", len(summ), "scenarios; HE01_size", size, "varsigma", round(varsigma["varsigma"], 4))
    return 0


if __name__ == "__main__":
    sys.exit(main())
