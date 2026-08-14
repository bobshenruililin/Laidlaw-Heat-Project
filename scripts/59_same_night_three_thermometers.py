#!/usr/bin/env python3
"""Same-night three thermometers at the official 28°C cut.

The threshold instrument already shows that Jaccard at 28°C is 0.031.
This script names the nights: 435 HKO-only, 14 both, 3 ERA5-only, and
lets the public page step through them without dumping another 4,017-day blob.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.
Not form 2a.

Usage:
  python3 scripts/59_same_night_three_thermometers.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
PEER_HK = ROOT / "data_processed" / "peer_cities" / "cache" / "hong_kong_daily.csv"
OUT_TAB = ROOT / "outputs" / "threshold_demo"
OUT_DOCS = ROOT / "docs" / "demo"
OUT_FIG = ROOT / "figures" / "threshold_demo"
HN_C = 28.0


def read_series(path: Path, field: str) -> dict[str, float]:
    out = {}
    with path.open() as f:
        for row in csv.DictReader(f):
            out[row["date"]] = float(row[field])
    return out


def tag_of(hko_on: bool, era_on: bool) -> str | None:
    if hko_on and era_on:
        return "both"
    if hko_on:
        return "hko"
    if era_on:
        return "era5"
    return None


def write_featured_svg(path: Path, night: dict, n_both: int, n_hko: int, n_era: int) -> None:
    """Three thermometers for one named night. Hogan-spare cream card."""
    w, h = 720, 420
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="24" y="28" font-size="16">The same night, three thermometers</text>',
        f'<text x="24" y="48" font-size="12" fill="#5b6773">{night["date"]} · tag {night["tag"]} · official cut 28°C</text>',
    ]
    scale_lo, scale_hi = 22.0, 36.0
    tubes = [
        ("HKO Headquarters", night["hko_tmin"], "#12181f"),
        ("ERA5 dry-bulb", night["era5_tmin"], "#0c6b74"),
        ("ERA5 apparent", night["atmin"], "#c9a227"),
    ]

    def y_of(t: float) -> float:
        return 360 - (t - scale_lo) / (scale_hi - scale_lo) * 260

    for i, (lab, val, color) in enumerate(tubes):
        x = 90 + i * 200
        parts.append(f'<rect x="{x}" y="80" width="36" height="280" rx="18" fill="#fffdf8" stroke="{color}" stroke-width="2"/>')
        mercury_h = 360 - y_of(val)
        parts.append(
            f'<rect x="{x + 6}" y="{y_of(val):.1f}" width="24" height="{mercury_h - 20:.1f}" '
            f'rx="12" fill="{color}" fill-opacity="0.85"/>'
        )
        parts.append(f'<circle cx="{x + 18}" cy="352" r="22" fill="{color}"/>')
        y28 = y_of(HN_C)
        parts.append(f'<line x1="{x - 12}" x2="{x + 48}" y1="{y28:.1f}" y2="{y28:.1f}" stroke="#c24e16" stroke-dasharray="4 3"/>')
        parts.append(f'<text x="{x + 18}" y="78" text-anchor="middle" font-size="11">{lab}</text>')
        parts.append(
            f'<text x="{x + 18}" y="400" text-anchor="middle" font-size="16" fill="{color}">{val:.1f}°C</text>'
        )
    parts.append(f'<text x="24" y="64" font-size="11" fill="#c24e16">28°C</text>')
    parts.append(
        f'<text x="24" y="414" font-size="11" fill="#5b6773">'
        f"{n_both} nights in both · {n_hko} HKO-only · {n_era} ERA5-only · 4,017 matched days. "
        "Not a health finding. Live paper stays on Headquarters.</text>"
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    hko = read_series(HKO_DAILY, "tmin")
    era = read_series(PEER_HK, "tmin")
    atmin = read_series(PEER_HK, "atmin")
    dates = sorted(set(hko) & set(era) & set(atmin))
    if len(dates) != 4017:
        raise RuntimeError(f"Expected 4017 matched days, got {len(dates)}.")

    nights = []
    for d in dates:
        ht, et, at = hko[d], era[d], atmin[d]
        tag = tag_of(ht >= HN_C, et >= HN_C)
        if tag is None:
            continue
        nights.append({
            "date": d,
            "year": int(d[:4]),
            "month": int(d[5:7]),
            "hko_tmin": round(ht, 1),
            "era5_tmin": round(et, 1),
            "atmin": round(at, 1),
            "gap_hko_minus_era5": round(ht - et, 1),
            "tag": tag,
        })

    by_tag = {"hko": [], "both": [], "era5": []}
    for n in nights:
        by_tag[n["tag"]].append(n)

    hottest_both = max(by_tag["both"], key=lambda n: n["hko_tmin"])
    hottest_miss = max(by_tag["hko"], key=lambda n: (n["hko_tmin"], n["gap_hko_minus_era5"]))
    widest_gap = max(by_tag["hko"], key=lambda n: n["gap_hko_minus_era5"])
    n_hko_ge29_miss = sum(1 for n in by_tag["hko"] if n["hko_tmin"] >= 29.0)

    payload = {
        "title": "Same-night three thermometers",
        "window": {"start": "2013-01-01", "end": "2023-12-31", "n_days": 4017},
        "cut_c": HN_C,
        "provenance": (
            "REAL_PUBLIC. HKO Headquarters daily Tmin from the project weather "
            "design file; Open-Meteo ERA5-Land dry-bulb and apparent Tmin at the "
            "Hong Kong coordinate (script 48 cache). Union of nights ≥ 28°C on "
            "either dry-bulb encoding. Exposure descriptives only. No health "
            "outcomes. No project coefficients."
        ),
        "counts": {
            "hko_only": len(by_tag["hko"]),
            "both": len(by_tag["both"]),
            "era5_only": len(by_tag["era5"]),
            "union": len(nights),
            "hko_total": len(by_tag["hko"]) + len(by_tag["both"]),
            "era5_total": len(by_tag["era5"]) + len(by_tag["both"]),
            "n_hko_ge29_era5_below_28": n_hko_ge29_miss,
        },
        "featured": {
            "hottest_both": hottest_both["date"],
            "hottest_hko_miss": hottest_miss["date"],
            "widest_gap": widest_gap["date"],
            "first_both": by_tag["both"][0]["date"],
            "era5_only": [n["date"] for n in by_tag["era5"]],
        },
        "nights": nights,
        "punchline": (
            f"{len(by_tag['both'])} nights in both, {len(by_tag['hko'])} HKO-only, "
            f"{len(by_tag['era5'])} ERA5-only. Hottest agreement: {hottest_both['date']} "
            f"(HKO {hottest_both['hko_tmin']}°C). Hottest miss: {hottest_miss['date']} "
            f"(HKO {hottest_miss['hko_tmin']}°C, ERA5 {hottest_miss['era5_tmin']}°C). "
            f"{n_hko_ge29_miss} station nights ≥29°C are invisible to ERA5 at 28°C."
        ),
        "claim_boundaries": [
            "Do not rank these nights by harm.",
            "Do not treat the 14 overlapping nights as a reconstructed HKO series.",
            "Apparent temperature is a third encoding, not a correction.",
            "This page is not the Scholars Network essay and not form 2a.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "nights_28.json").write_text(json.dumps(payload, indent=2) + "\n")
    slim = {k: v for k, v in payload.items() if k != "nights"}
    slim["nights"] = nights  # needed by the page; keep one file
    (OUT_DOCS / "nights_28.js").write_text(
        "window.NIGHTS_28 = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    )
    write_featured_svg(
        OUT_FIG / "same_night_three_thermometers.svg",
        hottest_both,
        len(by_tag["both"]),
        len(by_tag["hko"]),
        len(by_tag["era5"]),
    )
    print(payload["punchline"])
    print("wrote", OUT_DOCS / "nights_28.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
