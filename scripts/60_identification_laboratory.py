#!/usr/bin/env python3
"""Identification laboratory: calibration curve + hot-night year×month map.

Jaccard 0.031 is an integral. This script shows the integrand: P(ERA5 Tmin ≥ 28
| HKO Tmin in bin). It also draws the hot-night analogue of the live paper's
cold-day year×month heatmap (Figure 2), and packs the six live encodings into
one identification-profile table.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.
Daily grain is a companion/supplement diagnostic, not a daily-recovery model.

Usage:
  python3 scripts/60_identification_laboratory.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
PEER_HK = ROOT / "data_processed" / "peer_cities" / "cache" / "hong_kong_daily.csv"
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
SIX = ROOT / "outputs" / "identifying_months" / "hko_six_encodings.json"
IE = ROOT / "outputs" / "identifying_months" / "intensive_extensive.json"
BRIDGE = ROOT / "outputs" / "monthly_bridge" / "monthly_station_grid_bridge.json"
OUT_TAB = ROOT / "outputs" / "identification_lab"
OUT_FIG = ROOT / "figures" / "identification_lab"
OUT_LIVE = ROOT / "figures" / "live_identification"
OUT_DOCS = ROOT / "docs" / "id"
HN_C = 28.0
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
FAMILY = {
    "mean_temp": "continuous temperature",
    "mean_tmax": "continuous temperature",
    "mean_tmin": "continuous temperature",
    "hot_nights": "official heat-count",
    "very_hot_days": "official heat-count",
    "cold_days": "official cold-count",
}


def read_map(path: Path, field: str) -> dict[str, float]:
    out = {}
    with path.open() as f:
        for row in csv.DictReader(f):
            out[row["date"]] = float(row[field])
    return out


def align() -> list[dict]:
    hko_t = read_map(HKO_DAILY, "tmin")
    era_t = read_map(PEER_HK, "tmin")
    at_t = read_map(PEER_HK, "atmin")
    dates = sorted(set(hko_t) & set(era_t) & set(at_t))
    if len(dates) != 4017:
        raise RuntimeError(f"Expected 4017 matched days, got {len(dates)}.")
    rows = []
    for d in dates:
        ht, et, at = hko_t[d], era_t[d], at_t[d]
        rows.append({
            "date": d,
            "year": int(d[:4]),
            "month": int(d[5:7]),
            "hko": ht,
            "era": et,
            "at": at,
            "hko_hn": ht >= HN_C,
            "era_hn": et >= HN_C,
        })
    return rows


def reliability(rows: list[dict], lo: float, hi: float, width: float) -> list[dict]:
    edges = np.round(np.arange(lo, hi + 1e-9, width), 2)
    out = []
    for i in range(len(edges) - 1):
        a, b = float(edges[i]), float(edges[i + 1])
        xs = [r for r in rows if a <= r["hko"] < b]
        n = len(xs)
        n_era = sum(1 for r in xs if r["era_hn"])
        n_at = sum(1 for r in xs if r["at"] >= HN_C)
        out.append({
            "lo": a,
            "hi": b,
            "mid": round((a + b) / 2, 3),
            "n": n,
            "n_era5_ge28": n_era,
            "rate_era5": None if n == 0 else round(n_era / n, 4),
            "n_at_ge28": n_at,
            "rate_at": None if n == 0 else round(n_at / n, 4),
        })
    return out


def spell_membership(rows: list[dict]) -> list[dict]:
    hn_dates = {r["date"] for r in rows if r["hko_hn"]}
    both = [r for r in rows if r["hko_hn"] and r["era_hn"]]
    out = []
    for r in both:
        cur = datetime.strptime(r["date"], "%Y-%m-%d")
        start = cur
        while (start - timedelta(days=1)).strftime("%Y-%m-%d") in hn_dates:
            start -= timedelta(days=1)
        end = cur
        while (end + timedelta(days=1)).strftime("%Y-%m-%d") in hn_dates:
            end += timedelta(days=1)
        length = (end - start).days + 1
        pos = (cur - start).days + 1
        if length == 1:
            place = "isolated"
        elif pos == 1:
            place = "start"
        elif pos == length:
            place = "end"
        else:
            place = "middle"
        out.append({
            "date": r["date"],
            "hko_tmin": round(r["hko"], 1),
            "era5_tmin": round(r["era"], 1),
            "run_length": length,
            "position_in_run": pos,
            "place": place,
        })
    return out


def cell_fill(v: int, vmax: int) -> str:
    if v <= 0:
        return "#e8e2d4"
    t = min(1.0, v / vmax)
    r = int(12 + (194 - 12) * t)
    g = int(107 + (78 - 107) * t)
    b = int(116 + (22 - 116) * t)
    return f"rgb({r},{g},{b})"


def write_heatmap(path: Path, monthly: list[dict], *, chrome: bool) -> int:
    """Paper-grade year × month hot-night counts. Labels live in the margin."""
    by = {(int(r["year"]), int(r["month"])): int(float(r["hot_nights"])) for r in monthly}
    years = list(range(2013, 2024))
    vmax = max(by.values()) if by else 1
    w, h = 920, 520
    left, top, right, bot = 72, 28 if not chrome else 64, 36, 56 if not chrome else 80
    cw = (w - left - right) / 12
    ch = (h - top - bot) / 11
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'preserveAspectRatio="xMidYMid meet" font-family="Georgia, serif" role="img">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
    ]
    if chrome:
        parts.append('<text x="24" y="28" font-size="16">Official hot nights by year and month</text>')
        parts.append(
            '<text x="24" y="46" font-size="11" fill="#5b6773">'
            "HKO Headquarters, 2013–2023. Cell = count of nights Tmin ≥ 28°C. "
            "Exposure only.</text>"
        )
    for i, y in enumerate(years):
        yy = top + i * ch
        parts.append(
            f'<text x="{left - 10}" y="{yy + ch * 0.68:.1f}" text-anchor="end" font-size="11">{y}</text>'
        )
        for m in range(1, 13):
            xx = left + (m - 1) * cw
            v = by.get((y, m), 0)
            fill = cell_fill(v, vmax)
            parts.append(
                f'<rect x="{xx + 2:.1f}" y="{yy + 2:.1f}" width="{cw - 4:.1f}" height="{ch - 4:.1f}" '
                f'rx="3" fill="{fill}"/>'
            )
            if v > 0:
                ink = "#f4efe4" if v >= 12 else "#12181f"
                parts.append(
                    f'<text x="{xx + cw / 2:.1f}" y="{yy + ch * 0.68:.1f}" text-anchor="middle" '
                    f'font-size="10" fill="{ink}">{v}</text>'
                )
    for m in range(1, 13):
        xx = left + (m - 1) * cw + cw / 2
        parts.append(
            f'<text x="{xx:.1f}" y="{h - bot + 16}" text-anchor="middle" font-size="11">{MONTH_NAMES[m - 1]}</text>'
        )
    x0 = left + 5 * cw
    x1 = left + 9 * cw
    bracket_y = h - bot + 28
    parts.append(
        f'<line x1="{x0 + 8:.1f}" y1="{bracket_y}" x2="{x1 - 8:.1f}" y2="{bracket_y}" '
        'stroke="#0c6b74" stroke-width="2"/>'
    )
    parts.append(
        f'<text x="{(x0 + x1) / 2:.1f}" y="{bracket_y + 14}" text-anchor="middle" font-size="11" fill="#0c6b74">'
        "always ≥1 night (11/11 years)</text>"
    )
    if chrome:
        parts.append(
            f'<text x="24" y="{h - 12}" font-size="11" fill="#5b6773">'
            "July 2013 = 1 night; July 2022 = 25. May and October are mixed. "
            "Not a health finding. Live paper stays on Headquarters.</text>"
        )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")
    return vmax


def write_reliability(path: Path, bins05: list[dict], p_ge28: float, p_ge295: float, *, chrome: bool) -> None:
    w, h = 920, 480
    left, top, right, bot = 64, 28 if not chrome else 64, 28, 56 if not chrome else 88
    inner_w = w - left - right
    inner_h = h - top - bot
    tmin, tmax = 24.0, 31.0
    clip_id = "plotChrome" if chrome else "plotWeb"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'preserveAspectRatio="xMidYMid meet" font-family="Georgia, serif" role="img">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
    ]
    if chrome:
        parts.append('<text x="24" y="28" font-size="16">ERA5 agrees only after Headquarters is already hot</text>')
        parts.append(
            '<text x="24" y="46" font-size="11" fill="#5b6773">'
            "P(ERA5 Tmin ≥ 28°C | HKO Tmin in 0.5°C bin). 4,017 matched nights. "
            "Caption sits under the plot, not on it. Exposure only.</text>"
        )
    parts.extend([
        f'<clipPath id="{clip_id}"><rect x="{left}" y="{top}" width="{inner_w}" height="{inner_h}"/></clipPath>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{h - bot}" stroke="#12181f"/>',
        f'<line x1="{left}" y1="{h - bot}" x2="{w - right}" y2="{h - bot}" stroke="#12181f"/>',
    ])

    def x_of(t: float) -> float:
        return left + (t - tmin) / (tmax - tmin) * inner_w

    def y_of(p: float) -> float:
        return h - bot - p * inner_h

    x28 = x_of(28.0)
    parts.append(
        f'<line x1="{x28:.1f}" y1="{top}" x2="{x28:.1f}" y2="{h - bot}" '
        'stroke="#c24e16" stroke-dasharray="4 3"/>'
    )
    parts.append(f'<g clip-path="url(#{clip_id})">')
    pts_era = []
    for row in bins05:
        if row["n"] == 0 or row["rate_era5"] is None:
            continue
        if row["mid"] < tmin or row["mid"] > tmax:
            continue
        x = x_of(row["mid"])
        y = y_of(row["rate_era5"])
        r = 2.4 + min(5.5, math.sqrt(row["n"]) / 3.2)
        pts_era.append(f"{x:.1f},{y:.1f}")
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#0c6b74" '
            'fill-opacity="0.88" stroke="#f4efe4" stroke-width="0.7"/>'
        )
    if len(pts_era) > 1:
        parts.append(
            f'<polyline fill="none" stroke="#0c6b74" stroke-width="1.6" points="{" ".join(pts_era)}"/>'
        )
    parts.append("</g>")
    for tick in (24, 26, 28, 30):
        x = x_of(tick)
        parts.append(f'<line x1="{x:.1f}" y1="{h - bot}" x2="{x:.1f}" y2="{h - bot + 6}" stroke="#12181f"/>')
        label = f"{tick}°C"
        parts.append(f'<text x="{x:.1f}" y="{h - bot + 20}" text-anchor="middle" font-size="11">{label}</text>')
    for p in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = y_of(p)
        parts.append(f'<line x1="{left - 4}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#12181f"/>')
        parts.append(
            f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="#5b6773">{p:.0%}</text>'
        )
    if chrome:
        parts.append(
            f'<text x="24" y="{h - 36}" font-size="11" fill="#5b6773">'
            "Teal = P(ERA5 dry-bulb ≥ 28°C). Marker area scales with bin count. "
            "Axis labels sit in the margin. Apparent temperature is omitted here "
            "because it is already ~1 once Headquarters is ≥ 28°C.</text>"
        )
        parts.append(
            f'<text x="24" y="{h - 18}" font-size="11" fill="#5b6773">'
            f"Among station nights ≥ 29.5°C, ERA5 still agrees only {p_ge295:.0%} of the time "
            f"(unconditional P among official hot nights = {p_ge28:.3f}). "
            "Not a health finding. Not a daily admissions model.</text>"
        )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def identification_profile() -> list[dict]:
    six = json.loads(SIX.read_text())
    ie = json.loads(IE.read_text())
    bridge = json.loads(BRIDGE.read_text())
    by_six = {e["encoding"]: e for e in six["encodings"]}
    by_ie = {e["encoding"]: e for e in ie["encodings"]}
    r_tmin = bridge["fits"]["era5_tmin_on_hko_tmin"]["r"]
    hko_hn_m = bridge["month_flags"]["hko_hn_positive"]
    era_hn_m = bridge["month_flags"]["era5_hn_positive"]
    hko_cd_m = bridge["month_flags"]["hko_cd_positive"]
    era_cd_m = bridge["month_flags"]["era5_cd_positive"]
    instrument = {
        "mean_temp": f"ERA5 monthly mean Tmin r = {r_tmin:.3f}; means travel",
        "mean_tmax": f"ERA5 monthly mean Tmin r = {r_tmin:.3f}; means travel",
        "mean_tmin": f"ERA5 monthly mean Tmin r = {r_tmin:.3f}; means travel",
        "hot_nights": (
            f"Headquarters-only flag; ERA5 28°C months {era_hn_m} vs HKO {hko_hn_m}"
        ),
        "very_hot_days": "Official HKO flag; live paper stays on Headquarters",
        "cold_days": (
            f"ERA5 over-fires cold months ({era_cd_m} vs HKO {hko_cd_m}); opposite night bias"
        ),
    }
    rows = []
    for key in ("mean_temp", "mean_tmax", "mean_tmin", "hot_nights", "very_hot_days", "cold_days"):
        s = by_six[key]
        e = by_ie[key]
        rows.append({
            "encoding": key,
            "label": s["label"],
            "identifying_share": s["share_identifying_within_month"],
            "share_intensive": e["share_intensive_of_identifying"],
            "share_extensive": e["share_extensive_of_identifying"],
            "always_on": e["always_on_abbr"],
            "family": FAMILY[key],
            "instrument": instrument[key],
        })
    return rows


def main() -> int:
    rows = align()
    monthly = list(csv.DictReader(CLIMATE.open()))
    if len(monthly) != 132:
        raise RuntimeError("Expected 132 months.")

    n_hko = sum(1 for r in rows if r["hko_hn"])
    n_era = sum(1 for r in rows if r["era_hn"])
    n_both = sum(1 for r in rows if r["hko_hn"] and r["era_hn"])
    if n_hko != 449 or n_era != 17 or n_both != 14:
        raise RuntimeError(f"Anchor mismatch: HKO {n_hko} ERA5 {n_era} both {n_both}")

    bins02 = reliability(rows, 26.0, 31.2, 0.2)
    bins05 = reliability(rows, 24.0, 32.5, 0.5)
    hn = [r for r in rows if r["hko_hn"]]
    n_ge29 = sum(1 for r in hn if r["hko"] >= 29.0)
    n_ge295 = sum(1 for r in hn if r["hko"] >= 29.5)
    n_era_ge29 = sum(1 for r in hn if r["hko"] >= 29.0 and r["era_hn"])
    n_era_ge295 = sum(1 for r in hn if r["hko"] >= 29.5 and r["era_hn"])
    n_bin28 = sum(1 for r in hn if 28.0 <= r["hko"] < 29.0)
    n_era_bin28 = sum(1 for r in hn if 28.0 <= r["hko"] < 29.0 and r["era_hn"])
    n_jj = sum(1 for r in hn if r["month"] in (6, 7, 8, 9))

    months = defaultdict(lambda: {"hko": 0, "era": 0})
    for r in rows:
        key = f"{r['year']:04d}-{r['month']:02d}"
        if r["hko_hn"]:
            months[key]["hko"] += 1
        if r["era_hn"]:
            months[key]["era"] += 1
    hko_pos = [k for k, v in months.items() if v["hko"] > 0]
    era_inside = [k for k in hko_pos if months[k]["era"] > 0]

    spells = spell_membership(rows)
    both_months = sorted({int(s["date"][5:7]) for s in spells})
    profile = identification_profile()
    year_month = [
        {
            "year": int(r["year"]),
            "month": int(r["month"]),
            "hot_nights": int(float(r["hot_nights"])),
        }
        for r in monthly
    ]
    vmax = max(x["hot_nights"] for x in year_month)

    n_cold_hko_8_12 = sum(1 for r in rows if 8.0 <= r["hko"] < 12.0)
    n_cold_era = sum(1 for r in rows if 8.0 <= r["hko"] < 12.0 and r["era"] <= 12.0)

    payload = {
        "title": "Identification laboratory",
        "window": {"start": "2013-01-01", "end": "2023-12-31", "n_days": 4017, "n_months": 132},
        "provenance": (
            "REAL_PUBLIC. HKO Headquarters daily Tmin; Open-Meteo ERA5-Land "
            "dry-bulb and apparent Tmin at the Hong Kong coordinate. "
            "Exposure descriptives only. No health outcomes. No project coefficients."
        ),
        "anchors": {
            "hko_hn": n_hko,
            "era5_hn": n_era,
            "both": n_both,
            "hko_only": n_hko - n_both,
            "era5_only": n_era - n_both,
            "p_era5_given_hko_hn": round(n_both / n_hko, 4),
        },
        "reliability_0p2": bins02,
        "reliability_0p5": bins05,
        "tail": {
            "n_hko_28_to_29": n_bin28,
            "n_era5_in_28_to_29": n_era_bin28,
            "rate_28_to_29": round(n_era_bin28 / n_bin28, 4),
            "n_hko_ge29": n_ge29,
            "rate_ge29": round(n_era_ge29 / n_ge29, 4),
            "n_hko_ge29_5": n_ge295,
            "rate_ge29_5": round(n_era_ge295 / n_ge295, 4),
        },
        "always_on": {
            "n_hko_hn_jun_sep": n_jj,
            "share_jun_sep": round(n_jj / n_hko, 4),
            "both_nights_calendar_months": both_months,
        },
        "monthly_containment": {
            "n_hko_positive_months": len(hko_pos),
            "n_those_with_any_era5_hn": len(era_inside),
            "n_hko_positive_without_era5": len(hko_pos) - len(era_inside),
        },
        "spells_of_both_nights": spells,
        "identification_profile": profile,
        "year_month_hot_nights": year_month,
        "heatmap_vmax": vmax,
        "cold_analogue": {
            "n_hko_8_to_12": n_cold_hko_8_12,
            "n_era5_le12_in_that_bin": n_cold_era,
            "rate": round(n_cold_era / n_cold_hko_8_12, 4),
            "note": (
                "Opposite bias: when Headquarters is already 8–12°C, ERA5 almost "
                "always also reports ≤12°C. Not a health finding."
            ),
        },
        "hm_cm_footnote": (
            "The unlocked HM/CM catalogue is a separate family (11 live flags, "
            "effective rank 3.92). It is not these six rows, and rank is not a "
            "licence to refit outcomes."
        ),
        "punchline": (
            f"Among {n_bin28} station nights in [28, 29)°C, ERA5 called 28°C "
            f"{n_era_bin28} time(s) (rate {n_era_bin28 / n_bin28:.3f}). "
            f"Among {n_ge295} nights ≥29.5°C the rate is {n_era_ge295 / n_ge295:.2f}. "
            f"{n_jj}/{n_hko} official hot nights fall in June–September. "
            f"{len(hko_pos) - len(era_inside)} of {len(hko_pos)} HKO hot-night months "
            "contain no ERA5 28°C night."
        ),
        "claim_boundaries": [
            "This laboratory does not use hospital counts.",
            "A calibration rate is not a daily admissions coefficient.",
            "Do not paste daily Jaccard or the 14 nights into Hogan’s weather paragraph.",
            "Do not treat 0.045 as a health attenuation factor.",
            "This page is not form 2a and not Gate 3.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "identification_lab.json").write_text(json.dumps(payload, indent=2) + "\n")
    slim = {
        k: payload[k]
        for k in (
            "title", "window", "provenance", "anchors", "reliability_0p5", "tail",
            "always_on", "monthly_containment", "spells_of_both_nights",
            "identification_profile", "year_month_hot_nights", "heatmap_vmax",
            "cold_analogue", "hm_cm_footnote", "punchline", "claim_boundaries",
        )
    }
    (OUT_DOCS / "id_embed.js").write_text(
        "window.ID_LAB = " + json.dumps(slim, separators=(",", ":")) + ";\n"
    )
    with (OUT_TAB / "identification_profile.csv").open("w", newline="") as f:
        wcsv = csv.DictWriter(
            f,
            fieldnames=[
                "encoding", "label", "identifying_share", "share_intensive",
                "share_extensive", "always_on", "family", "instrument",
            ],
        )
        wcsv.writeheader()
        wcsv.writerows(profile)

    write_heatmap(OUT_FIG / "hot_night_year_month.svg", monthly, chrome=True)
    write_heatmap(OUT_FIG / "hot_night_year_month_web.svg", monthly, chrome=False)
    write_heatmap(OUT_LIVE / "figure_D_hot_night_identification.svg", monthly, chrome=True)
    write_reliability(
        OUT_FIG / "era5_reliability_given_hko.svg",
        bins05,
        n_both / n_hko,
        n_era_ge295 / n_ge295,
        chrome=True,
    )
    write_reliability(
        OUT_FIG / "era5_reliability_given_hko_web.svg",
        bins05,
        n_both / n_hko,
        n_era_ge295 / n_ge295,
        chrome=False,
    )
    print(payload["punchline"])
    print("vmax", vmax)
    print("wrote", OUT_TAB / "identification_lab.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
