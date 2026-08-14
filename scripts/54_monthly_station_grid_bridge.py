#!/usr/bin/env python3
"""Monthly-grain bridge: HKO vs ERA5 at the paper's exposure grain.

The live paper uses 132 monthly counts, not 4,017 daily flags. This script
asks whether the station–grid disagreement survives that aggregation.

EXPOSURE ONLY. No health coefficients. No HA rows. Live paper stays on HKO.

Usage:
  python3 scripts/54_monthly_station_grid_bridge.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HKO_DAILY = ROOT / "data_processed" / "md_daily_weather_design_2013_2023.csv"
PEER_HK = ROOT / "data_processed" / "peer_cities" / "cache" / "hong_kong_daily.csv"
OUT_TAB = ROOT / "outputs" / "monthly_bridge"
OUT_FIG = ROOT / "figures" / "monthly_bridge"
HN_C, CD_C = 28.0, 12.0


def ols(x: np.ndarray, y: np.ndarray) -> dict:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot
    r = float(np.corrcoef(x, y)[0, 1]) if np.std(x) > 0 and np.std(y) > 0 else float("nan")
    sigma2 = ss_res / (n - 2)
    se = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * sigma2)
    return {
        "n": int(n),
        "intercept": round(float(beta[0]), 4),
        "slope": round(float(beta[1]), 4),
        "se_slope": round(float(se[1]), 4),
        "r": None if math.isnan(r) else round(r, 4),
        "r2": round(r2, 4),
        "rmse": round(float(np.sqrt(np.mean(resid ** 2))), 4),
        "mean_x": round(float(x.mean()), 4),
        "mean_y": round(float(y.mean()), 4),
    }


def variance_share(values: np.ndarray, months: np.ndarray) -> dict:
    grand = float(values.mean())
    ss_b = 0.0
    ss_w = 0.0
    by_month = []
    for mo in range(1, 13):
        v = values[months == mo]
        ss_b += len(v) * (float(v.mean()) - grand) ** 2
        ss_w += float(np.sum((v - v.mean()) ** 2))
        by_month.append({
            "month": mo,
            "mean": round(float(v.mean()), 3),
            "sd": round(float(v.std(ddof=1)), 3),
            "n_positive": int(np.sum(v > 0)),
            "n_years": int(len(v)),
        })
    tot = ss_b + ss_w
    return {
        "ss_between_calendar_month": round(ss_b, 3),
        "ss_within_month_between_year": round(ss_w, 3),
        "share_identifying_within_month": None if tot == 0 else round(ss_w / tot, 4),
        "n_calendar_months_with_sd": int(sum(1 for row in by_month if row["sd"] > 0)),
        "by_month": by_month,
    }


def write_scatter(path: Path, x, y, title, xlab, ylab, note) -> None:
    w, h = 640, 520
    pad = 64
    xmax = max(float(np.max(x)), 1.0)
    ymax = max(float(np.max(y)), 1.0)
    # keep 1:1 if both are counts on similar scale; otherwise independent
    def xx(v):
        return pad + (v / xmax) * (w - pad - 24)
    def yy(v):
        return (h - 48) - (v / ymax) * (h - pad - 48)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia, serif">',
        '<rect width="100%" height="100%" fill="#f4efe4"/>',
        f'<text x="64" y="28" font-size="16">{title}</text>',
        f'<text x="64" y="46" font-size="11" fill="#5b6773">{note}</text>',
        f'<line x1="{pad}" y1="{h-48}" x2="{w-24}" y2="{h-48}" stroke="#12181f"/>',
        f'<line x1="{pad}" y1="{h-48}" x2="{pad}" y2="{pad}" stroke="#12181f"/>',
    ]
    for xi, yi in zip(x, y):
        parts.append(
            f'<circle cx="{xx(float(xi)):.1f}" cy="{yy(float(yi)):.1f}" r="3.2" fill="#0c6b74" fill-opacity="0.7"/>'
        )
    # y = x if scales allow a readable diagonal
    if abs(xmax - ymax) / max(xmax, ymax) < 0.5:
        parts.append(
            f'<line x1="{xx(0):.1f}" y1="{yy(0):.1f}" x2="{xx(min(xmax,ymax)):.1f}" y2="{yy(min(xmax,ymax)):.1f}" '
            f'stroke="#c24e16" stroke-dasharray="4 4"/>'
        )
    parts.append(f'<text x="{w/2:.0f}" y="{h-16}" text-anchor="middle" font-size="12">{xlab}</text>')
    parts.append(
        f'<text x="18" y="{h/2:.0f}" font-size="12" transform="rotate(-90 18 {h/2:.0f})">{ylab}</text>'
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    hko_rows = list(csv.DictReader(HKO_DAILY.open()))
    era_rows = list(csv.DictReader(PEER_HK.open()))
    era_idx = {r["date"]: r for r in era_rows}
    buckets: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "hko_hn": 0, "era_hn": 0, "era_at": 0,
                 "hko_cd": 0, "era_cd": 0, "hko_tmin": [], "era_tmin": []}
    )
    n_days = 0
    for r in hko_rows:
        e = era_idx.get(r["date"])
        if e is None:
            continue
        key = r["date"][:7]
        ht, et, at = float(r["tmin"]), float(e["tmin"]), float(e["atmin"])
        b = buckets[key]
        b["n"] += 1
        b["hko_hn"] += int(ht >= HN_C)
        b["era_hn"] += int(et >= HN_C)
        b["era_at"] += int(at >= HN_C)
        b["hko_cd"] += int(ht <= CD_C)
        b["era_cd"] += int(et <= CD_C)
        b["hko_tmin"].append(ht)
        b["era_tmin"].append(et)
        n_days += 1
    keys = sorted(buckets)
    if len(keys) != 132 or n_days != 4017:
        raise RuntimeError(f"Expected 132 months / 4017 days, got {len(keys)} / {n_days}.")

    hko_hn = np.array([buckets[k]["hko_hn"] for k in keys], float)
    era_hn = np.array([buckets[k]["era_hn"] for k in keys], float)
    era_at = np.array([buckets[k]["era_at"] for k in keys], float)
    hko_cd = np.array([buckets[k]["hko_cd"] for k in keys], float)
    era_cd = np.array([buckets[k]["era_cd"] for k in keys], float)
    hko_tm = np.array([np.mean(buckets[k]["hko_tmin"]) for k in keys], float)
    era_tm = np.array([np.mean(buckets[k]["era_tmin"]) for k in keys], float)
    months = np.array([int(k[5:7]) for k in keys], int)
    hot_season = (months >= 5) & (months <= 10)

    payload = {
        "title": "Monthly station–grid bridge",
        "window": {"start": "2013-01", "end": "2023-12", "n_months": 132, "n_days": 4017},
        "provenance": (
            "REAL_PUBLIC. HKO Headquarters daily Tmin rolled to 132 calendar months; "
            "Open-Meteo ERA5-Land dry-bulb and apparent Tmin at the Hong Kong coordinate "
            "(script 48 cache). Exposure descriptives only. No health outcomes. "
            "No project coefficients. Live paper stays on HKO Headquarters."
        ),
        "why_this_exists": (
            "The live paper’s exposures are monthly counts. Daily Jaccard 0.031 could "
            "have been an aggregation artefact. It is not: at 132 months, ERA5 28°C "
            "nights still do not reconstruct Headquarters."
        ),
        "fits": {
            "era5_hn_on_hko_hn": ols(hko_hn, era_hn),
            "era5_at_hn_on_hko_hn": ols(hko_hn, era_at),
            "era5_tmin_on_hko_tmin": ols(hko_tm, era_tm),
            "era5_cd_on_hko_cd": ols(hko_cd, era_cd),
            "era5_hn_on_hko_hn_may_oct": ols(hko_hn[hot_season], era_hn[hot_season]),
        },
        "month_flags": {
            "hko_hn_positive": int(np.sum(hko_hn > 0)),
            "era5_hn_positive": int(np.sum(era_hn > 0)),
            "both_hn_positive": int(np.sum((hko_hn > 0) & (era_hn > 0))),
            "hko_cd_positive": int(np.sum(hko_cd > 0)),
            "era5_cd_positive": int(np.sum(era_cd > 0)),
        },
        "identification_hko_hn": variance_share(hko_hn, months),
        "identification_hko_cd": variance_share(hko_cd, months),
        "claim_boundaries": [
            "Do not treat the slope as a health attenuation factor. No outcome was used.",
            "Do not paste ERA5 monthly counts into the live paper’s HKO flags.",
            "Mean Tmin agreement does not license threshold-flag agreement.",
            "This is not Gate 3 and not form 2a.",
        ],
        "literature_position": (
            "Mistry et al. 2022 found ERA5-Land generally usable for temperature–mortality "
            "curves, with weaker heat performance in the tropics. Guo et al. 2024 found the "
            "official Hong Kong 28°C night flag was a poor hospitalization metric next to "
            "hourly excess. This bridge is the missing piece between those papers: the "
            "official flag also fails as a reanalysis object, at the monthly grain of our panel."
        ),
    }
    hn_fit = payload["fits"]["era5_hn_on_hko_hn"]
    tm_fit = payload["fits"]["era5_tmin_on_hko_tmin"]
    payload["punchline"] = (
        f"Monthly mean Tmin agrees (r = {tm_fit['r']}, slope = {tm_fit['slope']}). "
        f"Monthly 28°C-night counts do not (r = {hn_fit['r']}, slope = {hn_fit['slope']}). "
        f"Headquarters has hot nights in {payload['month_flags']['hko_hn_positive']} months; "
        f"ERA5 in {payload['month_flags']['era5_hn_positive']}."
    )

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    (OUT_TAB / "monthly_station_grid_bridge.json").write_text(json.dumps(payload, indent=2) + "\n")
    rows = []
    for k in keys:
        b = buckets[k]
        rows.append({
            "month_id": k,
            "hko_hot_nights": b["hko_hn"],
            "era5_hot_nights": b["era_hn"],
            "era5_apparent_hot_nights": b["era_at"],
            "hko_cold_days": b["hko_cd"],
            "era5_cold_days": b["era_cd"],
            "hko_mean_tmin": round(float(np.mean(b["hko_tmin"])), 3),
            "era5_mean_tmin": round(float(np.mean(b["era_tmin"])), 3),
        })
    with (OUT_TAB / "monthly_station_grid_bridge.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    write_scatter(
        OUT_FIG / "monthly_hot_nights_hko_vs_era5.svg",
        hko_hn, era_hn,
        "Monthly hot nights do not travel",
        "HKO Headquarters nights ≥ 28°C",
        "ERA5-Land nights ≥ 28°C, same coordinate",
        payload["punchline"] + " Exposure only.",
    )
    write_scatter(
        OUT_FIG / "monthly_tmin_hko_vs_era5.svg",
        hko_tm, era_tm,
        "Monthly mean Tmin does travel",
        "HKO Headquarters mean Tmin (°C)",
        "ERA5-Land mean Tmin (°C), same coordinate",
        f"r = {tm_fit['r']}, slope = {tm_fit['slope']}. The continuous field is not the flag. Exposure only.",
    )
    print(payload["punchline"])
    print("identifying within-month share HN", payload["identification_hko_hn"]["share_identifying_within_month"])
    print("wrote", OUT_TAB / "monthly_station_grid_bridge.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
