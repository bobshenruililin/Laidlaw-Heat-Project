#!/usr/bin/env python3
"""One-page exposure-only composite for a later Bishai science note.

Three panels, one claim: monthly means travel; the official 28°C flag does
not, at either the daily or the monthly grain of the paper.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.
Not form 2a. Not to send until Bob reviews Email B.

Usage:
  python3 scripts/56_email_b_composite.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_CSV = ROOT / "outputs" / "monthly_bridge" / "monthly_station_grid_bridge.csv"
BRIDGE_JSON = ROOT / "outputs" / "monthly_bridge" / "monthly_station_grid_bridge.json"
THRESH_JSON = ROOT / "outputs" / "threshold_demo" / "threshold_does_not_travel.json"
OUT_FIG = ROOT / "figures" / "monthly_bridge"
OUT_TAB = ROOT / "outputs" / "monthly_bridge"


def scatter_group(x, y, x0, y0, pw, ph, xmax, ymax, title, xlab, ylab, note, draw_diag):
    pad_l, pad_b, pad_t, pad_r = 48, 36, 28, 12
    def xx(v):
        return x0 + pad_l + (float(v) / xmax) * (pw - pad_l - pad_r)
    def yy(v):
        return y0 + ph - pad_b - (float(v) / ymax) * (ph - pad_t - pad_b)
    parts = [
        f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none"/>',
        f'<text x="{x0 + pad_l}" y="{y0 + 16}" font-size="13">{title}</text>',
        f'<text x="{x0 + pad_l}" y="{y0 + 30}" font-size="10" fill="#5b6773">{note}</text>',
        f'<line x1="{x0+pad_l}" y1="{y0+ph-pad_b}" x2="{x0+pw-pad_r}" y2="{y0+ph-pad_b}" stroke="#12181f"/>',
        f'<line x1="{x0+pad_l}" y1="{y0+ph-pad_b}" x2="{x0+pad_l}" y2="{y0+pad_t+4}" stroke="#12181f"/>',
    ]
    for xi, yi in zip(x, y):
        parts.append(
            f'<circle cx="{xx(xi):.1f}" cy="{yy(yi):.1f}" r="2.6" fill="#0c6b74" fill-opacity="0.7"/>'
        )
    if draw_diag:
        m = min(xmax, ymax)
        parts.append(
            f'<line x1="{xx(0):.1f}" y1="{yy(0):.1f}" x2="{xx(m):.1f}" y2="{yy(m):.1f}" '
            'stroke="#c24e16" stroke-dasharray="4 4"/>'
        )
    parts.append(
        f'<text x="{x0 + pw/2:.0f}" y="{y0 + ph - 8}" text-anchor="middle" font-size="11">{xlab}</text>'
    )
    cx, cy = x0 + 14, y0 + ph / 2
    parts.append(
        f'<text x="{cx:.0f}" y="{cy:.0f}" font-size="11" transform="rotate(-90 {cx:.0f} {cy:.0f})">{ylab}</text>'
    )
    return parts


def jaccard_panel(thresholds, jaccard, x0, y0, pw, ph, j28, tmax, tcount):
    pad_l, pad_b, pad_t, pad_r = 48, 36, 28, 16
    tmin, tmax_ax = 20.0, 32.0
    def xx(t):
        return x0 + pad_l + ((t - tmin) / (tmax_ax - tmin)) * (pw - pad_l - pad_r)
    def yy(j):
        return y0 + ph - pad_b - float(j) * (ph - pad_t - pad_b)
    pts = []
    for t, j in zip(thresholds, jaccard):
        if j is None:
            continue
        pts.append(f"{xx(t):.1f},{yy(j):.1f}")
    parts = [
        f'<text x="{x0 + pad_l}" y="{y0 + 16}" font-size="13">C. Daily Jaccard collapses at 28°C</text>',
        f'<text x="{x0 + pad_l}" y="{y0 + 30}" font-size="10" fill="#5b6773">'
        f"Same-cut Jaccard {j28:.3f} at 28°C. Max vs fixed HKO 28°C set: {tmax['jaccard']:.3f} at {tmax['threshold_c']}°C. "
        f"Count match {tcount['threshold_c']}°C is not the nights.</text>",
        f'<line x1="{x0+pad_l}" y1="{y0+ph-pad_b}" x2="{x0+pw-pad_r}" y2="{y0+ph-pad_b}" stroke="#12181f"/>',
        f'<line x1="{x0+pad_l}" y1="{y0+ph-pad_b}" x2="{x0+pad_l}" y2="{y0+pad_t+4}" stroke="#12181f"/>',
        f'<polyline fill="none" stroke="#0c6b74" stroke-width="2.2" points="{" ".join(pts)}"/>',
        f'<line x1="{xx(28):.1f}" y1="{y0+pad_t+4}" x2="{xx(28):.1f}" y2="{y0+ph-pad_b}" '
        'stroke="#c24e16" stroke-dasharray="4 4"/>',
        f'<text x="{xx(28)+6:.1f}" y="{y0+pad_t+18}" font-size="11" fill="#c24e16">28°C</text>',
    ]
    for tick, lab in ((20, "20"), (24, "24"), (28, "28"), (32, "32")):
        parts.append(
            f'<text x="{xx(tick):.1f}" y="{y0+ph-10}" text-anchor="middle" font-size="11" fill="#5b6773">{lab}</text>'
        )
    for jv, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1")):
        parts.append(
            f'<text x="{x0+pad_l-8}" y="{yy(jv)+4:.1f}" text-anchor="end" font-size="11" fill="#5b6773">{lab}</text>'
        )
    cx, cy = x0 + 14, y0 + ph / 2
    parts.append(
        f'<text x="{cx:.0f}" y="{cy:.0f}" font-size="11" transform="rotate(-90 {cx:.0f} {cy:.0f})">Jaccard</text>'
    )
    parts.append(
        f'<text x="{x0 + pw/2:.0f}" y="{y0 + ph - 8}" text-anchor="middle" font-size="11">Tmin threshold (°C)</text>'
    )
    return parts


def main() -> int:
    if not BRIDGE_CSV.exists() or not THRESH_JSON.exists():
        raise RuntimeError("Run scripts 53 and 54 first.")
    months = list(csv.DictReader(BRIDGE_CSV.open()))
    bridge = json.loads(BRIDGE_JSON.read_text())
    thresh = json.loads(THRESH_JSON.read_text())
    hko_tm = [float(r["hko_mean_tmin"]) for r in months]
    era_tm = [float(r["era5_mean_tmin"]) for r in months]
    hko_hn = [float(r["hko_hot_nights"]) for r in months]
    era_hn = [float(r["era5_hot_nights"]) for r in months]
    tm = bridge["fits"]["era5_tmin_on_hko_tmin"]
    hn = bridge["fits"]["era5_hn_on_hko_hn"]
    j28 = float(thresh["anchors_at_28"]["jaccard"])
    tmax = thresh["max_jaccard_hko28_vs_era5_t"]
    tcount = thresh["equivalent_thresholds"]["era5_tmin_matching_hko_449"]
    overlap = thresh["overlap_hko_vs_era5_hk"]["jaccard"]
    thresholds = thresh["thresholds_c"]

    w, h = 1100, 770
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="36" y="36" font-size="20">The official flag is the wrong instrument, not only the wrong metric</text>',
        '<text x="36" y="58" font-size="12" fill="#5b6773">'
        "HKO Headquarters vs ERA5-Land at the same Hong Kong coordinate, 2013–2023. "
        "Exposure identification only. No hospital counts. Live paper stays on Headquarters.</text>",
    ]
    parts.extend(
        scatter_group(
            hko_tm, era_tm, 24, 76, 520, 340,
            xmax=max(hko_tm + era_tm), ymax=max(hko_tm + era_tm),
            title="A. Monthly mean Tmin travels",
            xlab="HKO mean Tmin (°C)",
            ylab="ERA5 mean Tmin (°C)",
            note=f"132 months. r = {tm['r']}, slope = {tm['slope']}.",
            draw_diag=True,
        )
    )
    parts.extend(
        scatter_group(
            hko_hn, era_hn, 560, 76, 520, 340,
            xmax=max(max(hko_hn), 1.0), ymax=max(max(era_hn), 1.0) * 1.15,
            title="B. Monthly 28°C-night counts do not",
            xlab="HKO nights ≥ 28°C",
            ylab="ERA5 nights ≥ 28°C",
            note=(
                f"Slope = {hn['slope']} (SE {hn['se_slope']}). "
                f"HKO positive in {bridge['month_flags']['hko_hn_positive']} months; "
                f"ERA5 in {bridge['month_flags']['era5_hn_positive']}."
            ),
            draw_diag=False,
        )
    )
    parts.extend(
        jaccard_panel(thresholds, overlap, 24, 430, 1056, 260, j28, tmax, tcount)
    )
    parts.append(
        '<text x="36" y="716" font-size="11" fill="#5b6773">'
        "Guo et al. 2024: the official 28°C day-flag was a poor hospitalisation metric next to hourly excess. "
        "Mistry et al. 2022: ERA5-Land means usually travel for mortality curves, with weaker heat tails in the tropics.</text>"
    )
    parts.append(
        '<text x="36" y="734" font-size="11" fill="#5b6773">'
        "This page: the flag also fails as a reanalysis object at the grain of the CHD/HF panel. "
        "Do not treat 0.045 as a health attenuation factor.</text>"
    )
    parts.append(
        '<text x="36" y="752" font-size="11" fill="#5b6773">'
        "Not form 2a. Not Gate 3. Not a second health paper. "
        "Rebuild: python3 scripts/56_email_b_composite.py after scripts 53 and 54.</text>"
    )
    parts.append("</svg>")
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    out = OUT_FIG / "email_b_composite.svg"
    out.write_text("\n".join(parts) + "\n")
    meta = {
        "title": "Email B composite — exposure identification",
        "path": str(out.relative_to(ROOT)),
        "provenance": "REAL_PUBLIC. Built from script 54 monthly bridge and script 53 threshold sweep. No health outcomes.",
        "not_to_send_until": "Bob reviews Email B; Email A (form 2a) has already gone; GitHub Pages URL is optional and separate.",
        "punchline": bridge["punchline"],
        "claim_boundaries": bridge["claim_boundaries"],
    }
    (OUT_TAB / "email_b_composite.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
