#!/usr/bin/env python3
"""Year-shifted negative control: identifying-share teaching + health hook.

A 12-month shift of an official count flag does *not* collapse identifying
share: that share is a calendar-month property. The useful negative control
is health_t ~ exposure_{t-12}, which needs the gitignored HA analysis panels
(A60). This script always ships the exposure teaching; it calls the R hook
when panels are present and records PARKED_NO_PANEL otherwise.

Usage:
  python3 scripts/63_year_shift_negative_control.py
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib_hko_opendata import parse_hko_opendata  # noqa: E402

CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
TMIN = ROOT / "data_raw" / "hko" / "CLMMINT_HKO.csv"
TMAX = ROOT / "data_raw" / "hko" / "CLMMAXT_HKO.csv"
TMEAN = ROOT / "data_raw" / "hko" / "CLMTEMP_HKO.csv"
OUT_TAB = ROOT / "outputs" / "year_shift"
CHD_PANEL = ROOT / "data_processed" / "chd_analysis_panel.csv"
HF_PANEL = ROOT / "data_processed" / "hf_analysis_panel.csv"
R_HOOK = ROOT / "scripts" / "63_year_shift_health.R"
ENCODINGS = [
    ("mean_temp", "Mean temperature"),
    ("mean_tmax", "Mean Tmax"),
    ("mean_tmin", "Mean Tmin"),
    ("hot_nights", "Hot nights"),
    ("very_hot_days", "Very hot days"),
    ("cold_days", "Cold days"),
]


def identifying_share(values: np.ndarray, months: np.ndarray) -> float | None:
    grand = float(values.mean())
    ss_b = ss_w = 0.0
    for mo in range(1, 13):
        v = values[months == mo]
        ss_b += len(v) * (float(v.mean()) - grand) ** 2
        ss_w += float(np.sum((v - v.mean()) ** 2))
    tot = ss_b + ss_w
    return None if tot == 0 else round(ss_w / tot, 4)


def _monthly_mean(series: dict[str, dict]) -> dict[str, float]:
    acc: dict[str, list[float]] = {}
    for key, rec in series.items():
        if rec["value"] is None or rec["completeness"] != "C":
            continue
        acc.setdefault(key[:7], []).append(float(rec["value"]))
    return {k: sum(v) / len(v) for k, v in acc.items() if v}


def monthly_from_daily() -> dict[str, dict]:
    """Complete-C monthly counts and means including 2012, for a clean 12-month shift."""
    tmin = parse_hko_opendata(TMIN, year_min=2012, year_max=2023)
    tmax = parse_hko_opendata(TMAX, year_min=2012, year_max=2023)
    tmean = parse_hko_opendata(TMEAN, year_min=2012, year_max=2023)
    out: dict[str, dict] = {}
    for key, rec in tmin.items():
        ym = key[:7]
        slot = out.setdefault(
            ym,
            {"hot_nights": 0, "cold_days": 0, "very_hot_days": 0},
        )
        if rec["value"] is None or rec["completeness"] != "C":
            continue
        if rec["value"] >= 28:
            slot["hot_nights"] += 1
        if rec["value"] <= 12:
            slot["cold_days"] += 1
    for key, rec in tmax.items():
        ym = key[:7]
        slot = out.setdefault(
            ym,
            {"hot_nights": 0, "cold_days": 0, "very_hot_days": 0},
        )
        if rec["value"] is None or rec["completeness"] != "C":
            continue
        if rec["value"] >= 33:
            slot["very_hot_days"] += 1
    means_tmin = _monthly_mean(tmin)
    means_tmax = _monthly_mean(tmax)
    means_tmean = _monthly_mean(tmean)
    for ym, slot in out.items():
        slot["mean_tmin"] = means_tmin.get(ym)
        slot["mean_tmax"] = means_tmax.get(ym)
        slot["mean_temp"] = means_tmean.get(ym)
    return out


def main() -> int:
    climate = list(csv.DictReader(CLIMATE.open()))
    if len(climate) != 132:
        raise RuntimeError("Expected 132 months.")
    months = np.array([int(r["month"]) for r in climate], int)
    daily_m = monthly_from_daily()
    # 2013–2023 hot nights from daily C must match the paper file.
    hn_check = [daily_m[r["month_id"]]["hot_nights"] for r in climate]
    file_hn = [int(float(r["hot_nights"])) for r in climate]
    if hn_check != file_hn:
        raise RuntimeError("Daily-C monthly hot nights drifted from climate_monthly.")

    encodings = []
    for col, label in ENCODINGS:
        orig = np.array([float(r[col]) for r in climate], float)
        share_orig = identifying_share(orig, months)
        # Shift by 12 months using 2012–2022 of the same calendar month.
        shifted = []
        for r in climate:
            y, m = int(r["year"]), int(r["month"])
            prev = f"{y - 1:04d}-{m:02d}"
            prev_slot = daily_m.get(prev, {})
            val = prev_slot.get(col)
            shifted.append(float("nan") if val is None else float(val))
        shifted_a = np.array(shifted, float)
        mask = np.isfinite(shifted_a)
        share_shift = identifying_share(shifted_a[mask], months[mask])
        encodings.append({
            "encoding": col,
            "label": label,
            "n_months_original": 132,
            "n_months_shifted": int(mask.sum()),
            "identifying_share_original": share_orig,
            "identifying_share_year_shifted": share_shift,
            "delta": None if share_orig is None or share_shift is None else round(share_shift - share_orig, 4),
        })

    hn = next(e for e in encodings if e["encoding"] == "hot_nights")
    panels_present = CHD_PANEL.exists() and HF_PANEL.exists()
    health = {
        "status": "PANELS_PRESENT" if panels_present else "PARKED_NO_PANEL",
        "reason": (
            "gitignored analysis panels are on disk; R hook will re-fit twelve core contrasts"
            if panels_present
            else (
                "data_processed/*_analysis_panel.csv is gitignored and absent in this workspace "
                "(assumption A60). The useful negative control is health_t ~ exposure_{t-12}. "
                "No HA rows were invented."
            )
        ),
        "r_hook": str(R_HOOK.relative_to(ROOT)),
        "ran": False,
        "returncode": None,
    }
    if R_HOOK.exists():
        proc = subprocess.run(
            ["Rscript", str(R_HOOK)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        health["ran"] = True
        health["returncode"] = proc.returncode
        health["stdout_tail"] = proc.stdout[-2000:]
        health["stderr_tail"] = proc.stderr[-2000:]
        status_file = OUT_TAB / "health_refit_status.json"
        if status_file.exists():
            try:
                health["r_status"] = json.loads(status_file.read_text())
            except json.JSONDecodeError:
                health["r_status"] = None
        if proc.returncode != 0:
            health["status"] = "HOOK_FAILED"

    payload = {
        "title": "Year-shifted negative control",
        "provenance": (
            "REAL_PUBLIC climate. Identifying-share comparison uses HKO Headquarters "
            "monthly encodings; 12-month count shifts use complete open-data days "
            "including 2012. Health re-fit is Gate-3-open and runs only when HA "
            "panels are present. Not a headline. Not a new q."
        ),
        "teaching": (
            "Identifying share after calendar-month indicators is a within-month "
            "between-year property. A whole-year permutation of a seasonal count "
            "flag leaves that share almost unchanged. Collapsing identifying share "
            "is the wrong test of a 12-month shift. The useful test is whether a "
            "displaced exposure still predicts the unshifted monthly counts."
        ),
        "encodings": encodings,
        "hot_nights_anchor": hn,
        "health_refit": health,
        "claim_boundaries": [
            "A pass of the health negative control does not upgrade any q.",
            "Do not chase 1.022.",
            "Do not treat identifying-share invariance as confirmation of a health model.",
            "Gate 3 stays open.",
        ],
    }
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "year_shift_negative_control.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT_TAB / "identifying_share_year_shift.csv").open("w", newline="") as f:
        wcsv = csv.DictWriter(f, fieldnames=list(encodings[0].keys()))
        wcsv.writeheader()
        wcsv.writerows(encodings)
    print(payload["teaching"])
    print(
        "hot nights identifying share",
        hn["identifying_share_original"],
        "→",
        hn["identifying_share_year_shifted"],
        "health",
        health["status"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
