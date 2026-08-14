#!/usr/bin/env python3
"""Identifying-month table for the six live-paper HKO encodings.

With calendar-month indicators, each contrast is identified between years
within month. This script prints that fact for mean temperature, mean Tmax,
mean Tmin, hot nights, very hot days, and cold days — exposure only.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.

Usage:
  python3 scripts/55_identifying_months_six_encodings.py
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
OUT_TAB = ROOT / "outputs" / "identifying_months"
OUT_FIG = ROOT / "figures" / "identifying_months"

ENCODINGS = [
    ("mean_temp", "Mean temperature", "continuous"),
    ("mean_tmax", "Mean Tmax", "continuous"),
    ("mean_tmin", "Mean Tmin", "continuous"),
    ("hot_nights", "Hot nights ≥ 28°C", "count"),
    ("very_hot_days", "Very hot days ≥ 33°C", "count"),
    ("cold_days", "Cold days ≤ 12°C", "count"),
]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def month_span(months: list[int]) -> str:
    if not months:
        return "none"
    names = [MONTH_NAMES[m - 1] for m in months]
    if months == [1, 2, 3, 12]:
        return "Dec–Mar"
    consecutive = months == list(range(months[0], months[-1] + 1))
    if consecutive and len(months) > 1:
        return f"{names[0]}–{names[-1]}"
    return ", ".join(names)


def load54():
    spec = importlib.util.spec_from_file_location(
        "bridge54", ROOT / "scripts" / "54_monthly_station_grid_bridge.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_bars(path: Path, rows: list[dict]) -> None:
    w, h = 720, 420
    left, right, top, bot = 280, 48, 72, 56
    inner_w = w - left - right
    inner_h = h - top - bot
    n = len(rows)
    gap = 10
    bh = (inner_h - gap * (n - 1)) / n
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="16">What survives month indicators</text>',
        '<text x="24" y="48" font-size="11" fill="#5b6773">'
        "Share of 132-month sum of squares that is between-year within calendar month. "
        "Exposure only. Not a health finding.</text>",
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{h-bot}" stroke="#12181f"/>',
        f'<line x1="{left}" y1="{h-bot}" x2="{w-right}" y2="{h-bot}" stroke="#12181f"/>',
    ]
    for i, row in enumerate(rows):
        y = top + i * (bh + gap)
        share = float(row["share_identifying_within_month"])
        bar_w = share * inner_w / 0.55
        fill = "#0c6b74" if row["kind"] == "count" else "#5b6773"
        parts.append(
            f'<text x="{left-12}" y="{y + bh*0.62:.1f}" text-anchor="end" font-size="12">{row["label"]}</text>'
        )
        parts.append(
            f'<rect x="{left}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" fill="{fill}" fill-opacity="0.85"/>'
        )
        parts.append(
            f'<text x="{left + bar_w + 8:.1f}" y="{y + bh*0.62:.1f}" font-size="11" fill="#12181f">'
            f'{share:.0%} · {row["n_calendar_months_with_sd"]} months</text>'
        )
    for tick, lab in ((0.0, "0"), (0.25, "25%"), (0.50, "50%")):
        x = left + tick * inner_w / 0.55
        parts.append(f'<line x1="{x:.1f}" y1="{h-bot}" x2="{x:.1f}" y2="{h-bot+6}" stroke="#12181f"/>')
        parts.append(
            f'<text x="{x:.1f}" y="{h-24}" text-anchor="middle" font-size="11" fill="#5b6773">{lab}</text>'
        )
    parts.append(
        '<text x="24" y="404" font-size="11" fill="#5b6773">'
        "Grey = monthly means (season already explains most of the series). "
        "Teal = official count flags. Live paper stays on Headquarters.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    bridge = load54()
    rows_in = list(csv.DictReader(CLIMATE.open()))
    if len(rows_in) != 132:
        raise RuntimeError(f"Expected 132 months, got {len(rows_in)}.")
    months = np.array([int(r["month"]) for r in rows_in], int)
    encodings = []
    for col, label, kind in ENCODINGS:
        values = np.array([float(r[col]) for r in rows_in], float)
        ident = bridge.variance_share(values, months)
        sd_months = [row["month"] for row in ident["by_month"] if row["sd"] > 0]
        pos_cal = [row["month"] for row in ident["by_month"] if row["n_positive"] > 0]
        encodings.append({
            "encoding": col,
            "label": label,
            "kind": kind,
            "share_identifying_within_month": ident["share_identifying_within_month"],
            "n_calendar_months_with_sd": ident["n_calendar_months_with_sd"],
            "months_with_sd": sd_months,
            "months_with_sd_abbr": month_span(sd_months) if kind == "count" else "all 12",
            "n_months_positive": int(np.sum(values > 0)),
            "calendar_months_ever_positive": pos_cal,
            "mean": round(float(values.mean()), 4),
            "ss_between_calendar_month": ident["ss_between_calendar_month"],
            "ss_within_month_between_year": ident["ss_within_month_between_year"],
            "by_month": ident["by_month"],
        })

    payload = {
        "title": "Identifying months for six HKO encodings",
        "window": {"start": "2013-01", "end": "2023-12", "n_months": 132},
        "source": "data_processed/climate_monthly_2013_2023.csv (HKO Headquarters)",
        "provenance": (
            "REAL HKO monthly encodings used in the live twelve-contrast panel. "
            "Identifying share is the within-calendar-month, between-year fraction of "
            "the 132-month sum of squares. Exposure descriptives only. No health outcomes. "
            "No project coefficients."
        ),
        "why_this_exists": (
            "All core q-values exceed 0.19. Part of that is multiplicity. Part is design: "
            "month indicators absorb the seasonal cycle, so mean temperature is identified "
            "on a 4% residual, hot nights on six calendar months, and cold days on four."
        ),
        "encodings": encodings,
        "claim_boundaries": [
            "This table does not use hospital counts.",
            "An identifying share is not a coefficient and not a q-value.",
            "Do not treat a low identifying share as proof that a null is true.",
            "This is not Gate 3 and not form 2a.",
        ],
    }
    hn = next(e for e in encodings if e["encoding"] == "hot_nights")
    tm = next(e for e in encodings if e["encoding"] == "mean_temp")
    cd = next(e for e in encodings if e["encoding"] == "cold_days")
    payload["punchline"] = (
        f"Mean temperature: {tm['share_identifying_within_month']:.1%} identifying "
        f"({tm['n_calendar_months_with_sd']} months). "
        f"Hot nights: {hn['share_identifying_within_month']:.1%} identifying "
        f"({hn['n_calendar_months_with_sd']} months, {hn['months_with_sd_abbr']}). "
        f"Cold days: {cd['share_identifying_within_month']:.1%} identifying "
        f"({cd['n_calendar_months_with_sd']} months, {cd['months_with_sd_abbr']})."
    )

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "hko_six_encodings.json").write_text(json.dumps(payload, indent=2) + "\n")
    slim_rows = []
    for e in encodings:
        slim_rows.append({
            "encoding": e["encoding"],
            "label": e["label"],
            "kind": e["kind"],
            "share_identifying_within_month": e["share_identifying_within_month"],
            "n_calendar_months_with_sd": e["n_calendar_months_with_sd"],
            "months_with_sd": ",".join(str(m) for m in e["months_with_sd"]),
            "n_months_positive": e["n_months_positive"],
            "mean": e["mean"],
        })
    with (OUT_TAB / "hko_six_encodings.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(slim_rows[0].keys()))
        w.writeheader()
        w.writerows(slim_rows)

    write_bars(OUT_FIG / "hko_six_encodings.svg", encodings)
    print(payload["punchline"])
    print("wrote", OUT_TAB / "hko_six_encodings.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
