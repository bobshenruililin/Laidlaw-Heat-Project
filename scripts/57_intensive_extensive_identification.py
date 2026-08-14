#!/usr/bin/env python3
"""Intensive vs extensive identification for the six live-paper encodings.

Script 55 asked how much of each 132-month series survives calendar-month
indicators. This script asks what that residual *is*: whether a usually-hot
month had any events (extensive), or how many events it had (intensive).

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.

Usage:
  python3 scripts/57_intensive_extensive_identification.py
"""
from __future__ import annotations

import csv
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
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def month_span(months: list[int]) -> str:
    if not months:
        return "none"
    if months == [1, 2, 3, 12]:
        return "Dec–Mar"
    consecutive = months == list(range(months[0], months[-1] + 1))
    if consecutive and len(months) > 1:
        return f"{MONTH_NAMES[months[0] - 1]}–{MONTH_NAMES[months[-1] - 1]}"
    return ", ".join(MONTH_NAMES[m - 1] for m in months)


def classify_count_month(n_positive: int, n_years: int) -> str:
    if n_positive == 0:
        return "never"
    if n_positive == n_years:
        return "always"
    return "mixed"


def decompose_month(values: np.ndarray) -> dict:
    """Split one calendar month's sum of squares into extensive vs intensive.

    Extensive: between the zero years and the positive years.
    Intensive: within the positive years. Zero years contribute nothing
    within-group. For a continuous series with no zeros, extensive is 0.
    """
    y = np.asarray(values, float)
    n = int(len(y))
    mu = float(y.mean())
    ss_total = float(np.sum((y - mu) ** 2))
    pos = y > 0
    n_pos = int(np.sum(pos))
    n_zero = n - n_pos
    if n_pos:
        mu_pos = float(y[pos].mean())
        ss_intensive = float(np.sum((y[pos] - mu_pos) ** 2))
        min_pos = float(y[pos].min())
        max_pos = float(y[pos].max())
    else:
        mu_pos = 0.0
        ss_intensive = 0.0
        min_pos = None
        max_pos = None
    if n_zero == 0 or n_pos == 0:
        ss_extensive = 0.0
    else:
        ss_extensive = float(n_zero * (0.0 - mu) ** 2 + n_pos * (mu_pos - mu) ** 2)
    return {
        "n_years": n,
        "n_positive_years": n_pos,
        "n_zero_years": n_zero,
        "mean": round(mu, 4),
        "sd": None if n < 2 else round(float(y.std(ddof=1)), 4),
        "min": round(float(y.min()), 4),
        "max": round(float(y.max()), 4),
        "mean_when_positive": None if n_pos == 0 else round(mu_pos, 4),
        "min_when_positive": None if min_pos is None else round(min_pos, 4),
        "max_when_positive": None if max_pos is None else round(max_pos, 4),
        "ss_within_month": round(ss_total, 4),
        "ss_extensive": round(ss_extensive, 4),
        "ss_intensive": round(ss_intensive, 4),
        "class": classify_count_month(n_pos, n),
    }


def analyse_encoding(values: np.ndarray, months: np.ndarray, kind: str) -> dict:
    by_month = []
    ss_w = ss_ext = ss_int = 0.0
    always, mixed, never = [], [], []
    for mo in range(1, 13):
        row = decompose_month(values[months == mo])
        row["month"] = mo
        row["month_abbr"] = MONTH_NAMES[mo - 1]
        if kind == "continuous":
            row["class"] = "intensity_only"
        by_month.append(row)
        ss_w += row["ss_within_month"]
        ss_ext += row["ss_extensive"]
        ss_int += row["ss_intensive"]
        if kind == "count":
            if row["class"] == "always":
                always.append(mo)
            elif row["class"] == "mixed":
                mixed.append(mo)
            else:
                never.append(mo)

    identifying = ss_w
    out = {
        "kind": kind,
        "ss_identifying": round(ss_w, 4),
        "ss_extensive": round(ss_ext, 4),
        "ss_intensive": round(ss_int, 4),
        "share_extensive_of_identifying": None if identifying == 0 else round(ss_ext / identifying, 4),
        "share_intensive_of_identifying": None if identifying == 0 else round(ss_int / identifying, 4),
        "always_on_months": always,
        "mixed_months": mixed,
        "never_months": never,
        "always_on_abbr": month_span(always) if kind == "count" else "all 12 (continuous)",
        "mixed_abbr": month_span(mixed) if kind == "count" else "none",
        "n_months_positive": int(np.sum(values > 0)),
        "by_month": by_month,
    }
    if kind == "count" and identifying > 0:
        july = next(r for r in by_month if r["month"] == 7)
        out["july_share_of_identifying"] = round(july["ss_within_month"] / identifying, 4)
    return out


def write_figure(path: Path, encodings: list[dict]) -> None:
    hn = next(e for e in encodings if e["encoding"] == "hot_nights")
    cd = next(e for e in encodings if e["encoding"] == "cold_days")
    w, h = 880, 620
    left, right, top = 64, 36, 72
    panel_h = 220
    gap = 56
    inner_w = w - left - right
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="17">What the identifying residual is</text>',
        '<text x="24" y="48" font-size="11" fill="#5b6773">'
        "Within-calendar-month sum of squares, 132 months, HKO Headquarters. "
        "Teal = how many events. Amber = whether the month had any. Exposure only.</text>",
    ]

    def panel(enc: dict, y0: float, title: str, ymax: float) -> None:
        parts.append(f'<text x="{left}" y="{y0 - 10}" font-size="13">{title}</text>')
        bw = inner_w / 12.0
        for i, row in enumerate(enc["by_month"]):
            x = left + i * bw
            tot = row["ss_within_month"]
            if tot <= 0:
                parts.append(
                    f'<rect x="{x + 8:.1f}" y="{y0 + panel_h - 8:.1f}" width="{bw - 16:.1f}" '
                    f'height="4" fill="#d7d1c4"/>'
                )
            else:
                h_tot = tot / ymax * (panel_h - 16)
                h_ext = row["ss_extensive"] / ymax * (panel_h - 16)
                h_int = row["ss_intensive"] / ymax * (panel_h - 16)
                y_int = y0 + panel_h - h_int
                y_ext = y_int - h_ext
                parts.append(
                    f'<rect x="{x + 8:.1f}" y="{y_int:.1f}" width="{bw - 16:.1f}" '
                    f'height="{h_int:.1f}" fill="#0c6b74" fill-opacity="0.88"/>'
                )
                if h_ext > 0.4:
                    parts.append(
                        f'<rect x="{x + 8:.1f}" y="{y_ext:.1f}" width="{bw - 16:.1f}" '
                        f'height="{h_ext:.1f}" fill="#c9a227" fill-opacity="0.92"/>'
                    )
            cls = row["class"]
            mark = {"always": "11/11", "mixed": f"{row['n_positive_years']}/11",
                    "never": "0/11", "intensity_only": ""}[cls]
            parts.append(
                f'<text x="{x + bw/2:.1f}" y="{y0 + panel_h + 16:.1f}" text-anchor="middle" '
                f'font-size="11">{row["month_abbr"]}</text>'
            )
            parts.append(
                f'<text x="{x + bw/2:.1f}" y="{y0 + panel_h + 30:.1f}" text-anchor="middle" '
                f'font-size="9" fill="#5b6773">{mark}</text>'
            )
        parts.append(
            f'<line x1="{left}" y1="{y0 + panel_h}" x2="{w - right}" y2="{y0 + panel_h}" stroke="#12181f"/>'
        )

    panel(hn, top + 18, "A. Official hot nights ≥ 28°C", 520)
    panel(cd, top + 18 + panel_h + gap, "B. Official cold days ≤ 12°C", 200)
    parts.append(
        f'<rect x="{left}" y="{h - 52}" width="14" height="10" fill="#0c6b74"/>'
        f'<text x="{left + 20}" y="{h - 43}" font-size="11">intensive (count when the month already has events)</text>'
    )
    parts.append(
        f'<rect x="{left + 340}" y="{h - 52}" width="14" height="10" fill="#c9a227"/>'
        f'<text x="{left + 360}" y="{h - 43}" font-size="11">extensive (years with zero events)</text>'
    )
    parts.append(
        '<text x="24" y="608" font-size="11" fill="#5b6773">'
        "June–September always had ≥1 hot night (11/11 years). July 2013 had 1 night; July 2022 had 25. "
        "No winter month always had a cold day. Not a health finding.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    rows_in = list(csv.DictReader(CLIMATE.open()))
    if len(rows_in) != 132:
        raise RuntimeError(f"Expected 132 months, got {len(rows_in)}.")
    months = np.array([int(r["month"]) for r in rows_in], int)
    years = np.array([int(r["year"]) for r in rows_in], int)
    if sorted(set(years.tolist())) != list(range(2013, 2024)):
        raise RuntimeError("Expected years 2013–2023.")

    encodings = []
    for col, label, kind in ENCODINGS:
        values = np.array([float(r[col]) for r in rows_in], float)
        block = analyse_encoding(values, months, kind)
        block["encoding"] = col
        block["label"] = label
        encodings.append(block)

    hn = next(e for e in encodings if e["encoding"] == "hot_nights")
    vhd = next(e for e in encodings if e["encoding"] == "very_hot_days")
    cd = next(e for e in encodings if e["encoding"] == "cold_days")
    jul = next(r for r in hn["by_month"] if r["month"] == 7)
    jun = next(r for r in hn["by_month"] if r["month"] == 6)

    payload = {
        "title": "Intensive versus extensive identification",
        "window": {"start": "2013-01", "end": "2023-12", "n_months": 132, "n_years": 11},
        "source": "data_processed/climate_monthly_2013_2023.csv (HKO Headquarters)",
        "provenance": (
            "REAL HKO monthly encodings used in the live twelve-contrast panel. "
            "Extensive SS is the between-group sum of squares of zero versus "
            "positive years inside a calendar month. Intensive SS is the "
            "within-positive-years sum of squares. Exposure descriptives only. "
            "No health outcomes. No project coefficients."
        ),
        "why_this_exists": (
            "Script 55 showed that month indicators leave 29% of hot-night SS "
            "and 4% of mean-temperature SS. This script shows that the hot-night "
            "residual is almost entirely how many nights an already-hot month "
            "contained: June–September recorded at least one official hot night "
            "in every year of the window."
        ),
        "encodings": encodings,
        "punchline": (
            f"Hot nights: {hn['share_intensive_of_identifying']:.1%} of identifying SS is intensive; "
            f"June–September always on ({hn['always_on_abbr']}); mixed only {hn['mixed_abbr']}. "
            f"July alone is {hn['july_share_of_identifying']:.0%} of that residual "
            f"({int(jul['min'])} night in 2013 vs {int(jul['max'])} in 2022). "
            f"Every June had at least {int(jun['min_when_positive'])} nights. "
            f"Cold days: {cd['share_extensive_of_identifying']:.1%} extensive; no always-on winter month. "
            f"Very hot days always on {vhd['always_on_abbr']}."
        ),
        "claim_boundaries": [
            "This table does not use hospital counts.",
            "An intensive share is not a coefficient and not a q-value.",
            "Do not treat thin extensive variation as proof that a null is true.",
            "Do not paste these shares into Hogan’s weather paragraph.",
            "This is not Gate 3 and not form 2a.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "intensive_extensive.json").write_text(json.dumps(payload, indent=2) + "\n")
    slim_rows = []
    for e in encodings:
        slim_rows.append({
            "encoding": e["encoding"],
            "label": e["label"],
            "kind": e["kind"],
            "share_intensive_of_identifying": e["share_intensive_of_identifying"],
            "share_extensive_of_identifying": e["share_extensive_of_identifying"],
            "always_on_months": ",".join(str(m) for m in e["always_on_months"]),
            "mixed_months": ",".join(str(m) for m in e["mixed_months"]),
            "n_months_positive": e["n_months_positive"],
        })
    with (OUT_TAB / "intensive_extensive.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(slim_rows[0].keys()))
        w.writeheader()
        w.writerows(slim_rows)

    write_figure(OUT_FIG / "intensive_extensive.svg", encodings)
    print(payload["punchline"])
    print("wrote", OUT_TAB / "intensive_extensive.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
