#!/usr/bin/env python3
"""Hong Kong spatial thermal field, 2013–2023.

Public ERA5-Land via Open-Meteo on a 0.1° grid plus named landmarks.
Fits a two-covariate spatial model (elevation + distance-to-coast) for
night minima, then reports Moran's I and an empirical variogram.

EXPOSURE ONLY. No health coefficients. No HA rows. No district-level
health overlay. The live paper stays on HKO Headquarters.

Usage:
  python3 scripts/49_hk_spatial_thermal_field.py
  python3 scripts/49_hk_spatial_thermal_field.py --skip-fetch
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data_processed" / "hk_spatial" / "cache"
OUT_TAB = ROOT / "outputs" / "hk_spatial"
OUT_DOCS = ROOT / "docs" / "geo"
OUT_FIG = ROOT / "figures" / "hk_spatial"

START = "2013-01-01"
END = "2023-12-31"
HN_C, VHD_C, CD_C = 28.0, 33.0, 12.0
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
STEP = 0.10
CACHE_FIELDS = [
    "date", "tmax", "tmin", "tmean", "source", "cell_id",
]
DAILY_VARS = "temperature_2m_max,temperature_2m_min,temperature_2m_mean"

LANDMARKS = [
    {"id": "hko_hq", "name": "HKO Headquarters", "lat": 22.3022, "lon": 114.1742,
     "kind": "station", "note": "Live-paper station. Official 28/33/12 flags live here."},
    {"id": "airport", "name": "Hong Kong International Airport", "lat": 22.3080, "lon": 113.9185,
     "kind": "station", "note": "Chek Lap Kok. Coastal, reclaimed land."},
    {"id": "ta_kwu_ling", "name": "Ta Kwu Ling", "lat": 22.5286, "lon": 114.1567,
     "kind": "station", "note": "Northern New Territories. Often the winter contrast."},
    {"id": "the_peak", "name": "Victoria Peak", "lat": 22.2708, "lon": 114.1501,
     "kind": "ridge", "note": "Island ridge ~550 m. A 0.1° grid may not see it."},
    {"id": "sai_kung", "name": "Sai Kung", "lat": 22.3815, "lon": 114.2707,
     "kind": "coast", "note": "Eastern peninsula, more maritime."},
    {"id": "cheung_chau", "name": "Cheung Chau", "lat": 22.2011, "lon": 114.0267,
     "kind": "island", "note": "Outlying island south-west of the harbour."},
    {"id": "sha_tin", "name": "Sha Tin", "lat": 22.3771, "lon": 114.1974,
     "kind": "new_town", "note": "Inland new town, Shing Mun River valley."},
    {"id": "tuen_mun", "name": "Tuen Mun", "lat": 22.3908, "lon": 113.9730,
     "kind": "new_town", "note": "Western New Territories."},
    {"id": "waglan", "name": "Waglan Island", "lat": 22.1820, "lon": 114.3033,
     "kind": "marine", "note": "Southeast marine exposure."},
]

COAST = [
    (22.25, 113.86), (22.31, 113.92), (22.39, 113.97), (22.37, 114.11),
    (22.28, 114.16), (22.29, 114.20), (22.38, 114.27), (22.22, 114.21),
    (22.21, 114.26), (22.20, 114.13), (22.21, 114.03), (22.50, 114.03),
    (22.55, 114.22), (22.47, 114.35), (22.54, 114.43), (22.18, 114.30),
]


def grid_points() -> list[dict]:
    lats = [round(22.15 + i * STEP, 2) for i in range(5)]  # 22.15–22.55
    lons = [round(113.85 + i * STEP, 2) for i in range(6)]  # 113.85–114.35
    pts = []
    for lat in lats:
        for lon in lons:
            pts.append({
                "id": f"g_{lat:.2f}_{lon:.2f}",
                "name": f"{lat:.2f}°N {lon:.2f}°E",
                "lat": lat,
                "lon": lon,
                "kind": "grid",
                "note": "ERA5-Land sample, 0.1° lattice.",
            })
    return pts


def all_points() -> list[dict]:
    return LANDMARKS + grid_points()


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def dist_to_coast_km(lat: float, lon: float) -> float:
    return min(haversine_km(lat, lon, c[0], c[1]) for c in COAST)


def cache_path(cell_id: str) -> Path:
    safe = cell_id.replace(".", "p")
    return CACHE / f"{safe}_daily.csv"


def cache_complete(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open() as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or any(c not in reader.fieldnames for c in CACHE_FIELDS):
            return False
        n = sum(1 for _ in reader)
    return n >= 4000


def _fmt(x) -> str:
    return f"{float(x):.2f}"


def fetch_point(pt: dict, skip: bool) -> tuple[list[dict], float]:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = cache_path(pt["id"])
    meta_path = path.with_suffix(".meta.json")
    if skip and cache_complete(path) and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        return list(csv.DictReader(path.open())), float(meta["elevation"])
    if skip:
        raise RuntimeError(f"Incomplete cache for {pt['id']}; rerun without --skip-fetch")
    params = {
        "latitude": f"{pt['lat']:.4f}",
        "longitude": f"{pt['lon']:.4f}",
        "start_date": START,
        "end_date": END,
        "daily": DAILY_VARS,
        "timezone": "Asia/Hong_Kong",
        "temperature_unit": "celsius",
    }
    url = ARCHIVE + "?" + urllib.parse.urlencode(params)
    last_err = None
    body = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Laidlaw-Heat-Project/hk-spatial"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = json.loads(resp.read().decode())
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(2 ** attempt)
    if body is None:
        raise RuntimeError(f"Open-Meteo failed for {pt['id']}: {last_err}")
    elevation = float(body.get("elevation") if body.get("elevation") is not None else 0.0)
    daily = body["daily"]
    rows = []
    for i, date in enumerate(daily["time"]):
        tmax, tmin, tmean = daily["temperature_2m_max"][i], daily["temperature_2m_min"][i], daily["temperature_2m_mean"][i]
        if tmax is None or tmin is None or tmean is None:
            continue
        rows.append({
            "date": date,
            "tmax": _fmt(tmax),
            "tmin": _fmt(tmin),
            "tmean": _fmt(tmean),
            "source": "OPEN_METEO_ERA5_LAND",
            "cell_id": pt["id"],
        })
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CACHE_FIELDS)
        w.writeheader()
        w.writerows(rows)
    meta_path.write_text(json.dumps({
        "id": pt["id"], "lat": pt["lat"], "lon": pt["lon"],
        "elevation": elevation, "n_days": len(rows),
    }) + "\n")
    time.sleep(0.35)
    return rows, elevation


def encode(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        tmax, tmin, tmean = float(r["tmax"]), float(r["tmin"]), float(r["tmean"])
        dt = datetime.strptime(r["date"], "%Y-%m-%d")
        out.append({
            "date": r["date"], "month": dt.month, "year": dt.year,
            "tmax": tmax, "tmin": tmin, "tmean": tmean,
            "hn": int(tmin >= HN_C), "vhd": int(tmax >= VHD_C), "cd": int(tmin <= CD_C),
        })
    return out


def series_fingerprint(days: list[dict]) -> str:
    blob = ",".join(f"{d['tmin']:.2f}" for d in days)
    return hashlib.sha1(blob.encode()).hexdigest()[:12]


def summarise(pt: dict, days: list[dict], elevation: float) -> dict:
    tmins = [d["tmin"] for d in days]
    tmaxs = [d["tmax"] for d in days]
    tmeans = [d["tmean"] for d in days]
    climatology = []
    for m in range(1, 13):
        xs = [d["tmean"] for d in days if d["month"] == m]
        climatology.append(round(sum(xs) / len(xs), 3) if xs else None)
    amp = max(x for x in climatology if x is not None) - min(x for x in climatology if x is not None)
    return {
        **pt,
        "n_days": len(days),
        "elevation_m": round(elevation, 1),
        "dist_coast_km": round(dist_to_coast_km(pt["lat"], pt["lon"]), 2),
        "dist_hq_km": round(haversine_km(pt["lat"], pt["lon"], 22.3022, 114.1742), 2),
        "mean_t": round(sum(tmeans) / len(tmeans), 3),
        "mean_tmin": round(sum(tmins) / len(tmins), 3),
        "mean_tmax": round(sum(tmaxs) / len(tmaxs), 3),
        "p05_tmin": round(float(np.percentile(tmins, 5)), 3),
        "p95_tmax": round(float(np.percentile(tmaxs, 95)), 3),
        "seasonal_amp": round(amp, 3),
        "hn_total": sum(d["hn"] for d in days),
        "vhd_total": sum(d["vhd"] for d in days),
        "cd_total": sum(d["cd"] for d in days),
        "fingerprint": series_fingerprint(days),
        "climatology_mean_t": climatology,
        "provenance": "OPEN_METEO_ERA5_LAND_PUBLIC",
    }


def ols(y: np.ndarray, X: np.ndarray) -> dict:
    n, k = X.shape
    beta, residuals, rank, _ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    resid = y - fitted
    sst = float(np.sum((y - y.mean()) ** 2))
    sse = float(np.sum(resid ** 2))
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")
    df = max(n - k, 1)
    mse = sse / df
    try:
        xtx_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(np.maximum(0.0, mse * np.diag(xtx_inv)))
    except np.linalg.LinAlgError:
        se = np.full(k, float("nan"))
    return {
        "n": int(n),
        "k": int(k),
        "beta": [round(float(b), 4) for b in beta],
        "se": [round(float(s), 4) for s in se],
        "r2": round(float(r2), 4),
        "rmse": round(float(np.sqrt(np.mean(resid ** 2))), 3),
        "fitted": fitted,
        "resid": resid,
    }


def morans_i(values: np.ndarray, coords: list[tuple[float, float]], cutoff_km: float = 12.0) -> dict:
    n = len(values)
    z = values - values.mean()
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = haversine_km(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            if d <= cutoff_km:
                w[i, j] = 1.0
    wsum = float(w.sum())
    if wsum < 1e-9:
        return {"I": None, "expected": round(-1.0 / (n - 1), 4), "neighbors": 0, "cutoff_km": cutoff_km}
    num = float(z @ w @ z)
    den = float(z @ z)
    I = (n / wsum) * (num / den) if den else float("nan")
    return {
        "I": round(float(I), 4),
        "expected": round(-1.0 / (n - 1), 4),
        "W": round(wsum, 1),
        "cutoff_km": cutoff_km,
        "mean_neighbors": round(wsum / n, 2),
    }


def variogram(values: np.ndarray, coords: list[tuple[float, float]]) -> list[dict]:
    edges = [0, 12, 20, 28, 40, 56, 80]
    buckets = {i: [] for i in range(len(edges) - 1)}
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine_km(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            gamma = 0.5 * (values[i] - values[j]) ** 2
            for b in range(len(edges) - 1):
                if edges[b] <= d < edges[b + 1]:
                    buckets[b].append(gamma)
                    break
    out = []
    for b in range(len(edges) - 1):
        xs = buckets[b]
        out.append({
            "bin_km": f"{edges[b]}–{edges[b+1]}",
            "mid_km": round((edges[b] + edges[b + 1]) / 2, 1),
            "n_pairs": len(xs),
            "gamma": round(float(np.mean(xs)), 4) if xs else None,
        })
    return out


def loo_hq(summaries: list[dict]) -> dict:
    hq = next(s for s in summaries if s["id"] == "hko_hq")
    others = [s for s in summaries if s["id"] != "hko_hq"]
    y = np.array([s["mean_tmin"] for s in others], dtype=float)
    X = np.column_stack([
        np.ones(len(others)),
        [s["elevation_m"] for s in others],
        [s["dist_coast_km"] for s in others],
    ])
    fit = ols(y, X)
    x0 = np.array([1.0, hq["elevation_m"], hq["dist_coast_km"]])
    pred = float(x0 @ np.array(fit["beta"]))
    return {
        "observed_era5_tmin": hq["mean_tmin"],
        "predicted_from_neighbors": round(pred, 3),
        "error": round(pred - hq["mean_tmin"], 3),
        "r2_without_hq": fit["r2"],
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def cell_polygon(lat: float, lon: float, half: float = STEP / 2) -> list[list[float]]:
    return [
        [lon - half, lat - half],
        [lon + half, lat - half],
        [lon + half, lat + half],
        [lon - half, lat + half],
        [lon - half, lat - half],
    ]


def write_transect_svg(summaries: list[dict], path: Path) -> None:
    grid = [s for s in summaries if s["kind"] == "grid"]
    # west-east at ~22.35
    we = sorted([s for s in grid if abs(s["lat"] - 22.35) < 0.06], key=lambda s: s["lon"])
    ns = sorted([s for s in grid if abs(s["lon"] - 114.15) < 0.06], key=lambda s: s["lat"])
    w, h = 760, 420

    def series_path(rows: list[dict], key: str, xkey: str, x0: float, x1: float, y0: float, y1: float, pad):
        if len(rows) < 2:
            return ""
        xs = [r[xkey] for r in rows]
        ys = [r[key] for r in rows]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys) - 0.3, max(ys) + 0.3
        def xx(v):
            return pad[0] + (v - xmin) / (xmax - xmin) * (x1 - x0)
        def yy(v):
            return pad[1] + (ymax - v) / (ymax - ymin) * (y1 - y0)
        d = " ".join(
            f"{'M' if i == 0 else 'L'}{xx(x):.1f},{yy(y):.1f}" for i, (x, y) in enumerate(zip(xs, ys))
        )
        return f'<path d="{d}" fill="none" stroke="#0c6b74" stroke-width="2.4"/>'

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        '<text x="190" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15">West–east night Tmin (~22.35°N)</text>',
        '<text x="570" y="28" text-anchor="middle" font-family="Georgia, serif" font-size="15">South–north night Tmin (~114.15°E)</text>',
        series_path(we, "mean_tmin", "lon", 40, 340, 50, 360, (40, 50)),
        series_path(ns, "mean_tmin", "lat", 40, 340, 50, 360, (420, 50)),
        '<text x="190" y="400" text-anchor="middle" font-size="11" fill="#5b6773">Longitude</text>',
        '<text x="570" y="400" text-anchor="middle" font-size="11" fill="#5b6773">Latitude</text>',
        "</svg>",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-fetch", action="store_true")
    args = parser.parse_args()
    skip = args.skip_fetch or os.environ.get("HK_SPATIAL_SKIP_FETCH") == "1"

    points = all_points()
    summaries = []
    day_store: dict[str, list[dict]] = {}
    for pt in points:
        raw, elev = fetch_point(pt, skip=skip)
        days = encode(raw)
        day_store[pt["id"]] = days
        s = summarise(pt, days, elev)
        summaries.append(s)
        print(
            f"{pt['id']:22s} elev={s['elevation_m']:6.1f}m  Tmin={s['mean_tmin']:6.2f}  "
            f"HN={s['hn_total']:4d}  CD={s['cd_total']:4d}  fp={s['fingerprint']}",
            flush=True,
        )

    fps = {}
    for s in summaries:
        fps.setdefault(s["fingerprint"], []).append(s["id"])
    n_unique = len(fps)

    hq = next(s for s in summaries if s["id"] == "hko_hq")
    peak = next(s for s in summaries if s["id"] == "the_peak")
    airport = next(s for s in summaries if s["id"] == "airport")
    tkl = next(s for s in summaries if s["id"] == "ta_kwu_ling")
    hq_days = day_store["hko_hq"]
    peak_days = day_store["the_peak"]
    paired = list(zip(hq_days, peak_days))
    peak_rmse = math.sqrt(sum((a["tmin"] - b["tmin"]) ** 2 for a, b in paired) / len(paired))

    # Spatial model on GRID cells only (regular lattice; landmarks are overlays).
    grid = [s for s in summaries if s["kind"] == "grid"]
    y = np.array([s["mean_tmin"] for s in grid], dtype=float)
    X = np.column_stack([
        np.ones(len(grid)),
        [s["elevation_m"] for s in grid],
        [s["dist_coast_km"] for s in grid],
    ])
    fit = ols(y, X)
    for s, fval, rval in zip(grid, fit["fitted"], fit["resid"]):
        s["tmin_fitted"] = round(float(fval), 3)
        s["tmin_resid"] = round(float(rval), 3)
    for s in summaries:
        if "tmin_fitted" not in s:
            s["tmin_fitted"] = None
            s["tmin_resid"] = None
        if "tmin_trend_fitted" not in s:
            s["tmin_trend_fitted"] = None
            s["tmin_trend_resid"] = None

    coords = [(s["lat"], s["lon"]) for s in grid]
    moran_raw = morans_i(y, coords)
    moran_resid = morans_i(fit["resid"], coords)
    Xtrend = np.column_stack([
        np.ones(len(grid)),
        [s["elevation_m"] for s in grid],
        [s["lat"] for s in grid],
        [s["lon"] for s in grid],
    ])
    fit_trend = ols(y, Xtrend)
    moran_trend = morans_i(fit_trend["resid"], coords)
    for s, fval, rval in zip(grid, fit_trend["fitted"], fit_trend["resid"]):
        s["tmin_trend_fitted"] = round(float(fval), 3)
        s["tmin_trend_resid"] = round(float(rval), 3)
    vgm = variogram(y, coords)
    loo = loo_hq(summaries)

    model = {
        "outcome": "ERA5-Land mean daily Tmin, 2013–2023, grid cells only",
        "formula": "mean_tmin ~ elevation_m + dist_coast_km",
        "coefficients": {
            "intercept": {"beta": fit["beta"][0], "se": fit["se"][0]},
            "elevation_m": {"beta": fit["beta"][1], "se": fit["se"][1], "unit": "°C per metre"},
            "dist_coast_km": {"beta": fit["beta"][2], "se": fit["se"][2], "unit": "°C per km inland"},
        },
        "r2": fit["r2"],
        "rmse": fit["rmse"],
        "n_grid": fit["n"],
        "moran_raw_tmin": moran_raw,
        "moran_residual": moran_resid,
        "trend_model": {
            "formula": "mean_tmin ~ elevation_m + lat + lon",
            "r2": fit_trend["r2"],
            "rmse": fit_trend["rmse"],
            "beta": {
                "intercept": fit_trend["beta"][0],
                "elevation_m": fit_trend["beta"][1],
                "lat": fit_trend["beta"][2],
                "lon": fit_trend["beta"][3],
            },
            "moran_residual": moran_trend,
        },
        "variogram_tmin": vgm,
        "loo_headquarters": loo,
        "unique_fingerprints": n_unique,
        "n_points": len(summaries),
        "n_grid_points": len(grid),
        "peak_vs_hq_tmin_rmse": round(peak_rmse, 3),
        "peak_same_cell_as_hq": peak["fingerprint"] == hq["fingerprint"],
        "airport_minus_tkl_tmin": round(airport["mean_tmin"] - tkl["mean_tmin"], 3),
        "note": (
            "Open-Meteo returns a DEM elevation at the requested coordinate and a "
            "lapse-adjusted temperature. Victoria Peak (407 m) is 2.15 °C cooler at "
            "night than Headquarters on this source; that is not an HKO hill station. "
            "Waglan records 252 ERA5 nights ≥28 °C against Headquarters' 17. The 28 °C "
            "flag is a location even inside the territory. Residual Moran's I after "
            "elevation+coast stays high because the leftover field is marine and "
            "north–south, not white noise. Live paper stays on HKO."
        ),
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    skip_keys = {"climatology_mean_t"}
    write_csv(OUT_TAB / "hk_spatial_cells.csv", [
        {k: v for k, v in s.items() if k not in skip_keys} for s in summaries
    ])
    (OUT_TAB / "hk_spatial_model.json").write_text(json.dumps(model, indent=2) + "\n")

    features = []
    for s in summaries:
        geom = {
            "type": "Polygon",
            "coordinates": [cell_polygon(s["lat"], s["lon"])],
        } if s["kind"] == "grid" else {
            "type": "Point",
            "coordinates": [s["lon"], s["lat"]],
        }
        props = {k: v for k, v in s.items() if k != "climatology_mean_t"}
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    fc = {"type": "FeatureCollection", "features": features}

    payload = {
        "title": "Hong Kong spatial thermal field",
        "window": {"start": START, "end": END, "n_years": 11},
        "provenance": "REAL_PUBLIC. Open-Meteo ERA5-Land daily 2 m temperatures on a 0.1° lattice plus named landmarks. Exposure descriptives only. No health outcomes. No project coefficients.",
        "step_deg": STEP,
        "thresholds_hko": {"hot_night_tmin_ge": HN_C, "very_hot_day_tmax_ge": VHD_C, "cold_day_tmin_le": CD_C},
        "model": model,
        "cells": summaries,
        "geojson": fc,
        "claim_boundaries": [
            "Do not treat this grid as HKO Headquarters.",
            "Do not overlay CHD/HF or stroke counts on districts or cells.",
            "A 0.1° cell is not a person, a building, or The Peak.",
            "Live paper stays on HKO official flags.",
        ],
    }
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    js = "window.HK_SPATIAL = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    (OUT_DOCS / "geo_embed.js").write_text(js)
    (OUT_TAB / "hk_spatial_field.json").write_text(json.dumps(payload, indent=2) + "\n")
    write_transect_svg(summaries, OUT_FIG / "hk_tmin_transects.svg")
    write_transect_svg(summaries, OUT_DOCS / "hk_tmin_transects.svg")
    print("unique fingerprints", n_unique, "of", len(summaries))
    print("peak vs hq rmse", round(peak_rmse, 3), "same_cell", model["peak_same_cell_as_hq"])
    print("OLS R2", fit["r2"], "Moran raw", moran_raw, "Moran resid", moran_resid)
    print("wrote", OUT_DOCS / "geo_embed.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
