#!/usr/bin/env python3
"""The threshold does not travel.

Sweep Tmin thresholds across HKO Headquarters, ERA5-Land at the same
coordinate (dry-bulb and apparent), and the 90-cell Pearl River Delta
lattice. Jaccard(station, grid) and the geography of exceedances are
functions of the threshold.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on
HKO Headquarters. Reuses the script 48 Hong Kong cache and the script
50 PRD cache.

Usage:
  python3 scripts/53_threshold_does_not_travel.py
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
PEER_HK = ROOT / "data_processed" / "peer_cities" / "cache" / "hong_kong_daily.csv"
OUT_TAB = ROOT / "outputs" / "threshold_demo"
OUT_DOCS = ROOT / "docs" / "demo"
OUT_FIG = ROOT / "figures" / "threshold_demo"
HN_C = 28.0
THRESH = np.round(np.arange(20.0, 32.01, 0.5), 2)
FINE = np.round(np.arange(20.0, 32.01, 0.1), 2)


def load51():
    spec = importlib.util.spec_from_file_location(
        "field51", ROOT / "scripts" / "51_prd_field_laboratory.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_csv_series(path: Path, field: str) -> tuple[list[str], np.ndarray]:
    dates, vals = [], []
    with path.open() as f:
        for row in csv.DictReader(f):
            dates.append(row["date"])
            vals.append(float(row[field]))
    return dates, np.asarray(vals, dtype=float)


def align(dates_a, vals_a, dates_b, vals_b) -> tuple[list[str], np.ndarray, np.ndarray]:
    idx_b = {d: i for i, d in enumerate(dates_b)}
    dates, a, b = [], [], []
    for i, d in enumerate(dates_a):
        j = idx_b.get(d)
        if j is None:
            continue
        dates.append(d)
        a.append(vals_a[i])
        b.append(vals_b[j])
    return dates, np.asarray(a, float), np.asarray(b, float)


def counts_vs_threshold(x: np.ndarray, thresholds: np.ndarray) -> list[int]:
    return [int(np.sum(x >= t)) for t in thresholds]


def binary_overlap(gold: np.ndarray, pred: np.ndarray) -> dict:
    gold = np.asarray(gold, bool)
    pred = np.asarray(pred, bool)
    tp = int(np.sum(gold & pred))
    fp = int(np.sum(~gold & pred))
    fn = int(np.sum(gold & ~pred))
    union = tp + fp + fn
    n_gold = int(np.sum(gold))
    n_pred = int(np.sum(pred))
    return {
        "intersection": tp,
        "gold_only": fn,
        "pred_only": fp,
        "union": union,
        "n_gold": n_gold,
        "n_pred": n_pred,
        "jaccard": None if union == 0 else round(tp / union, 4),
        "sensitivity": None if n_gold == 0 else round(tp / n_gold, 4),
        "ppv": None if n_pred == 0 else round(tp / n_pred, 4),
    }


def overlap_vs_threshold(gold: np.ndarray, x: np.ndarray, thresholds: np.ndarray) -> dict:
    rows = [binary_overlap(gold, x >= t) for t in thresholds]
    return {k: [r[k] for r in rows] for k in rows[0]}


def max_overlap(gold: np.ndarray, x: np.ndarray, thresholds: np.ndarray) -> dict:
    rows = []
    for t in thresholds:
        r = binary_overlap(gold, x >= t)
        if r["jaccard"] is None:
            continue
        rows.append((r["jaccard"], float(t), r))
    if not rows:
        return {"threshold_c": None, "jaccard": None}
    _j, t, r = max(rows, key=lambda z: z[0])
    return {
        "threshold_c": t,
        "jaccard": r["jaccard"],
        "sensitivity": r["sensitivity"],
        "ppv": r["ppv"],
        "intersection": r["intersection"],
        "n_pred": r["n_pred"],
        "n_gold": r["n_gold"],
        "note": (
            "Station gold set is HKO Tmin ≥ 28°C, held fixed. Grid set is "
            "ERA5 Tmin ≥ t. A low maximum means no monotone threshold shift "
            "recovers the station nights."
        ),
    }


def jaccard_vs_threshold(a: np.ndarray, b: np.ndarray, thresholds: np.ndarray) -> dict:
    n_int, n_union, jac, a_only, b_only = [], [], [], [], []
    for t in thresholds:
        aa = a >= t
        bb = b >= t
        inter = int(np.sum(aa & bb))
        union = int(np.sum(aa | bb))
        n_int.append(inter)
        n_union.append(union)
        a_only.append(int(np.sum(aa & ~bb)))
        b_only.append(int(np.sum(~aa & bb)))
        jac.append(None if union == 0 else round(inter / union, 4))
    return {
        "intersection": n_int,
        "union": n_union,
        "hko_only": a_only,
        "era5_only": b_only,
        "jaccard": jac,
    }


def closest_threshold(counts: list[int], thresholds: np.ndarray, target: int) -> dict:
    arr = np.asarray(counts, dtype=float)
    i = int(np.argmin(np.abs(arr - target)))
    return {
        "threshold_c": float(thresholds[i]),
        "count": int(counts[i]),
        "target": int(target),
        "abs_err": int(abs(int(counts[i]) - target)),
    }


def write_static_figure(payload: dict) -> None:
    """Two-panel SVG Hogan can keep. No matplotlib."""
    t = payload["thresholds_c"]
    s = payload["series"]
    ov = payload["overlap_hko28_vs_era5_t"]
    w, h = 920, 640
    pad = 56
    left, right = pad, w - 24
    mid = 300
    bottom = h - 48

    def x_of(i: int) -> float:
        return left + i * (right - left) / (len(t) - 1)

    def y_count(v: float, ymax: float) -> float:
        return pad + (1 - v / ymax) * (mid - 20 - pad)

    def y_jac(v: float) -> float:
        top = mid + 36
        return top + (1 - v) * (bottom - top)

    ymax = max(s["hko_tmin"] + s["era5_hk_atmin"])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        '<text x="56" y="34" font-size="18">The threshold does not travel</text>',
        '<text x="56" y="54" font-size="11" fill="#5b6773">HKO Headquarters vs ERA5-Land at the same coordinate, 4,017 days, 2013–2023. Exposure only.</text>',
    ]

    def polyline(vals, color, ymax_local, yfun):
        pts = " ".join(f"{x_of(i):.1f},{yfun(v, ymax_local):.1f}" if yfun is y_count else f"{x_of(i):.1f},{yfun(v):.1f}" for i, v in enumerate(vals))
        return f'<polyline fill="none" stroke="{color}" stroke-width="2.2" points="{pts}"/>'

    # counts panel
    parts.append(polyline(s["hko_tmin"], "#12181f", ymax, y_count))
    parts.append(polyline(s["era5_hk_tmin"], "#0c6b74", ymax, y_count))
    parts.append(polyline(s["era5_hk_atmin"], "#c9a227", ymax, y_count))
    i28 = t.index(28.0)
    parts.append(f'<line x1="{x_of(i28):.1f}" x2="{x_of(i28):.1f}" y1="{pad}" y2="{mid-20}" stroke="#c24e16" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{x_of(i28)+8:.1f}" y="{pad+18}" font-size="11" fill="#c24e16">28°C</text>')
    parts.append('<text x="700" y="70" font-size="11" fill="#12181f">HKO</text>')
    parts.append('<text x="740" y="70" font-size="11" fill="#0c6b74">ERA5 dry-bulb</text>')
    parts.append('<text x="840" y="70" font-size="11" fill="#c9a227">apparent</text>')
    parts.append('<text x="20" y="180" font-size="11" fill="#5b6773" transform="rotate(-90 20 180)">nights ≥ t</text>')

    # agreement panel
    jac_same = [0 if v is None else v for v in payload["overlap_hko_vs_era5_hk"]["jaccard"]]
    jac_fixed = [0 if v is None else v for v in ov["jaccard"]]
    se = [0 if v is None else v for v in ov["sensitivity"]]
    ppv = [0 if v is None else v for v in ov["ppv"]]
    parts.append(polyline(jac_same, "#12181f", 1.0, lambda v, _=None: y_jac(v)))
    parts.append(polyline(jac_fixed, "#0c6b74", 1.0, lambda v, _=None: y_jac(v)))
    parts.append(polyline(se, "#c24e16", 1.0, lambda v, _=None: y_jac(v)))
    parts.append(polyline(ppv, "#c9a227", 1.0, lambda v, _=None: y_jac(v)))
    parts.append(f'<line x1="{x_of(i28):.1f}" x2="{x_of(i28):.1f}" y1="{mid+36}" y2="{bottom}" stroke="#c24e16" stroke-dasharray="4 4"/>')
    mx = payload["max_jaccard_hko28_vs_era5_t"]
    parts.append(f'<text x="56" y="{mid+28}" font-size="12">Jaccard(HKO≥t, ERA5≥t) · Jaccard(HKO≥28, ERA5≥t) · sensitivity · PPV</text>')
    parts.append(
        f'<text x="56" y="{h-18}" font-size="11" fill="#5b6773">'
        f'Max Jaccard against the fixed 28°C station set is {mx["jaccard"]} at {mx["threshold_c"]}°C. '
        f'Bias-corrected ERA5 Jaccard is {payload["bias_adjusted_hko28"]["jaccard"]}. '
        f'Not health findings. Live paper stays on HKO.</text>'
    )
    for tv in (20, 24, 28, 32):
        if tv in t:
            i = t.index(tv)
            parts.append(f'<text x="{x_of(i):.1f}" y="{h-32}" text-anchor="middle" font-size="11" fill="#5b6773">{tv}</text>')
    parts.append("</svg>")
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    (OUT_FIG / "exceedance_and_agreement.svg").write_text("\n".join(parts) + "\n")


def tenths(x: np.ndarray) -> list[int]:
    return [int(round(float(v) * 10.0)) for v in x]


def main() -> int:
    field = load51()
    prd = field.load_prd()
    cube = field.load_cube(prd)

    hko_dates, hko_tmin = read_csv_series(HKO_DAILY, "tmin")
    era_dates, era_tmin = read_csv_series(PEER_HK, "tmin")
    _, era_atmin = read_csv_series(PEER_HK, "atmin")
    dates, hko, era = align(hko_dates, hko_tmin, era_dates, era_tmin)
    dates2, era2, atmin = align(era_dates, era_tmin, era_dates, era_atmin)
    if dates != dates2 or not np.allclose(era, era2):
        raise RuntimeError("Hong Kong series failed to align.")
    if len(dates) != 4017:
        raise RuntimeError(f"Expected 4017 matched days, got {len(dates)}.")

    pts = cube["pts"]
    tmin = cube["tmin"]
    if tmin.shape[0] != 4017:
        raise RuntimeError("PRD cube day count does not match the HKO window.")
    lats, lons, elevs = cube["lats"], cube["lons"], cube["elevs"]
    hq_i = field.nearest_index(lats, lons, 22.3022, 114.1742, prd)
    wag_i = field.nearest_index(lats, lons, 22.1820, 114.3033, prd)
    gz_i = field.nearest_index(lats, lons, 23.1291, 113.2644, prd)
    marine = np.array([prd.region_of(p["lat"], p["lon"]) == "marine south" for p in pts])
    gz_box = np.array([prd.region_of(p["lat"], p["lon"]) == "Guangzhou" for p in pts])

    hko_n = counts_vs_threshold(hko, THRESH)
    era_n = counts_vs_threshold(era, THRESH)
    at_n = counts_vs_threshold(atmin, THRESH)
    wag_n = counts_vs_threshold(tmin[:, wag_i], THRESH)
    gz_n = counts_vs_threshold(tmin[:, gz_i], THRESH)
    hq_cell_n = counts_vs_threshold(tmin[:, hq_i], THRESH)
    overlap = jaccard_vs_threshold(hko, era, THRESH)
    gold28 = hko >= HN_C
    overlap_fixed = overlap_vs_threshold(gold28, era, THRESH)
    overlap_fixed_fine = overlap_vs_threshold(gold28, era, FINE)
    max_jac = max_overlap(gold28, era, FINE)
    bias = float(np.mean(era - hko))
    recovered = (era - bias) >= HN_C
    bias_adj_set = binary_overlap(gold28, recovered)
    bias_adj_n = int(np.sum(recovered))

    cell_counts = np.stack([(tmin >= t).sum(axis=0) for t in THRESH], axis=1).astype(int)
    marine_nights = cell_counts[:, :][marine].sum(axis=0)
    all_nights = cell_counts.sum(axis=0)
    marine_share = [
        None if int(all_nights[k]) == 0 else round(float(marine_nights[k] / all_nights[k]), 4)
        for k in range(len(THRESH))
    ]
    marine_mean = [round(float(cell_counts[marine, k].mean()), 1) for k in range(len(THRESH))]
    gz_mean = [round(float(cell_counts[gz_box, k].mean()), 1) for k in range(len(THRESH))]
    n_cells_lit = [int(np.sum(cell_counts[:, k] > 0)) for k in range(len(THRESH))]

    i28 = int(np.where(np.isclose(THRESH, HN_C))[0][0])
    hko_fine = counts_vs_threshold(hko, FINE)
    era_fine = counts_vs_threshold(era, FINE)
    at_fine = counts_vs_threshold(atmin, FINE)
    match_hko449 = closest_threshold(era_fine, FINE, 449)
    match_era17 = closest_threshold(hko_fine, FINE, 17)

    years = [int(d[:4]) for d in dates]
    months = [int(d[5:7]) for d in dates]

    cells = []
    for j, pt in enumerate(pts):
        cells.append({
            "id": pt["id"],
            "lat": pt["lat"],
            "lon": pt["lon"],
            "elev_m": round(float(elevs[j]), 1),
            "region": prd.region_of(pt["lat"], pt["lon"]),
            "counts": [int(v) for v in cell_counts[j]],
        })

    payload = {
        "title": "The threshold does not travel",
        "window": {"start": "2013-01-01", "end": "2023-12-31", "n_days": 4017, "n_years": 11},
        "provenance": (
            "REAL_PUBLIC. HKO Headquarters daily Tmin from the project weather "
            "design file; Open-Meteo ERA5-Land dry-bulb and apparent Tmin at the "
            "Hong Kong coordinate (script 48 cache); ERA5-Land 0.2° Pearl River "
            "Delta lattice (script 50 cache). Exposure descriptives only. No "
            "health outcomes. No project coefficients."
        ),
        "thresholds_c": [float(t) for t in THRESH],
        "fine_thresholds_c": [float(t) for t in FINE],
        "official_hot_night_c": HN_C,
        "series": {
            "hko_tmin": hko_n,
            "era5_hk_tmin": era_n,
            "era5_hk_atmin": at_n,
            "era5_hq_cell_tmin": hq_cell_n,
            "era5_waglan_tmin": wag_n,
            "era5_guangzhou_tmin": gz_n,
            "era5_marine_mean": marine_mean,
            "era5_guangzhou_box_mean": gz_mean,
            "n_cells_lit": n_cells_lit,
            "marine_share_cellnights": marine_share,
        },
        "overlap_hko_vs_era5_hk": overlap,
        "overlap_hko28_vs_era5_t": overlap_fixed,
        "max_jaccard_hko28_vs_era5_t": max_jac,
        "bias_adjusted_hko28": {
            **bias_adj_set,
            "bias_openmeteo_minus_hko_tmin": round(bias, 3),
            "note": (
                "ERA5 Tmin shifted by the mean bias, then cut at 28°C. "
                "Count recovery is not set recovery."
            ),
        },
        "anchors_at_28": {
            "hko_tmin": hko_n[i28],
            "era5_hk_tmin": era_n[i28],
            "era5_hk_atmin": at_n[i28],
            "era5_hq_cell_tmin": hq_cell_n[i28],
            "era5_waglan_tmin": wag_n[i28],
            "era5_guangzhou_tmin": gz_n[i28],
            "jaccard": overlap["jaccard"][i28],
            "intersection": overlap["intersection"][i28],
            "hko_only": overlap["hko_only"][i28],
            "era5_only": overlap["era5_only"][i28],
            "marine_share_cellnights": marine_share[i28],
            "n_cells_lit": n_cells_lit[i28],
            "bias_openmeteo_minus_hko_tmin": round(bias, 3),
            "bias_adjusted_era5_hn": bias_adj_n,
            "sensitivity_era5_vs_hko28": overlap_fixed["sensitivity"][i28],
            "ppv_era5_vs_hko28": overlap_fixed["ppv"][i28],
        },
        "equivalent_thresholds": {
            "era5_tmin_matching_hko_449": match_hko449,
            "hko_tmin_matching_era5_17": match_era17,
            "note": (
                "Closest 0.1°C step on 4,017 matched days. Matching a count is "
                "not matching the nights. Jaccard remains the overlap object."
            ),
        },
        "daily": {
            "year": years,
            "month": months,
            "hko_tmin_tenths": tenths(hko),
            "era5_hk_tmin_tenths": tenths(era),
            "era5_hk_atmin_tenths": tenths(atmin),
        },
        "grid": {
            "step_deg": prd.STEP,
            "n_cells": len(pts),
            "hq_cell": pts[hq_i]["id"],
            "waglan_cell": pts[wag_i]["id"],
            "guangzhou_cell": pts[gz_i]["id"],
            "n_marine_south": int(marine.sum()),
            "n_guangzhou_box": int(gz_box.sum()),
            "cells": cells,
        },
        "claim_boundaries": [
            "Do not paste ERA5 night counts into the live paper’s HKO flags.",
            "Do not treat apparent temperature as a reconstruction of Headquarters.",
            "Do not overlay CHD/HF or stroke counts on cells.",
            "Do not transport Hong Kong hospitalisation ratios up the Pearl.",
            "A Jaccard of 1 at a high threshold can mean both encodings are silent.",
            "This page is not the Scholars Network essay and not form 2a.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    slim = {k: v for k, v in payload.items() if k != "daily"}
    (OUT_TAB / "threshold_does_not_travel.json").write_text(json.dumps(payload, indent=2) + "\n")
    (OUT_TAB / "threshold_does_not_travel_slim.json").write_text(json.dumps(slim, indent=2) + "\n")
    (OUT_DOCS / "demo_embed.js").write_text(
        "window.THRESHOLD_DEMO = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    )
    a28 = payload["anchors_at_28"]
    print("n_days", len(dates))
    print("at 28C HKO", a28["hko_tmin"], "ERA5", a28["era5_hk_tmin"], "AT", a28["era5_hk_atmin"])
    print("jaccard", a28["jaccard"], "bias", a28["bias_openmeteo_minus_hko_tmin"])
    print("era5 matching 449", match_hko449)
    print("hko matching 17", match_era17)
    print("max Jaccard HKO28 vs ERA5(t)", max_jac)
    print("bias-adjusted set", bias_adj_set["jaccard"], "inter", bias_adj_set["intersection"])
    write_static_figure(payload)
    print("wrote", OUT_DOCS / "demo_embed.js")
    print("wrote", OUT_FIG / "exceedance_and_agreement.svg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
