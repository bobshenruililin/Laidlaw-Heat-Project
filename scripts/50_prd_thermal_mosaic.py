#!/usr/bin/env python3
"""Pearl River Delta thermal mosaic, 2013–2023.

Public ERA5-Land via Open-Meteo on a 0.2° lattice covering Hong Kong,
Shenzhen, Guangzhou, and the estuary. Fits nested spatial models
(OLS, SLX, SAR-2SLS), Getis-Ord Gi*, an empirical variogram, and a
thermal-versus-geographic distance check.

EXPOSURE ONLY. No health coefficients. No HA rows. No district or
prefecture health overlay. City markers are coordinates on this grid,
not HKO / CMA yearbook stations. The live paper stays on HKO Headquarters.

Usage:
  python3 scripts/50_prd_thermal_mosaic.py
  python3 scripts/50_prd_thermal_mosaic.py --skip-fetch
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data_processed" / "prd_spatial" / "cache"
OUT_TAB = ROOT / "outputs" / "prd_spatial"
OUT_DOCS = ROOT / "docs" / "prd"
OUT_FIG = ROOT / "figures" / "prd_spatial"

START = "2013-01-01"
END = "2023-12-31"
HN_C, VHD_C, CD_C = 28.0, 33.0, 12.0
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
STEP = 0.20
W_CUTOFF_KM = 35.0
CACHE_FIELDS = ["date", "tmax", "tmin", "tmean", "source", "cell_id"]
DAILY_VARS = "temperature_2m_max,temperature_2m_min,temperature_2m_mean"
MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

# South China Sea + Lingdingyang + Hong Kong waters. Not the river through
# Guangzhou, so inland basin cells stay inland.
COAST = [
    (21.90, 112.95), (21.95, 113.15), (22.05, 113.35),
    (22.12, 113.50), (22.20, 113.58), (22.32, 113.62),
    (22.45, 113.68), (22.55, 113.72),
    (22.20, 113.85), (22.28, 113.95), (22.30, 114.12),
    (22.18, 114.18), (22.17, 114.30), (22.28, 114.38),
    (22.42, 114.42), (22.55, 114.50), (22.65, 114.62),
    (22.75, 114.70),
]

CITIES = [
    {"id": "hong_kong", "name": "Hong Kong", "lat": 22.3022, "lon": 114.1742,
     "kind": "city", "note": "Live-paper station coordinate. Official flags live here, not on this grid."},
    {"id": "shenzhen", "name": "Shenzhen", "lat": 22.5431, "lon": 114.0579,
     "kind": "city", "note": "Northern neighbour. Same ERA5 source as the mosaic, not a CMA station."},
    {"id": "guangzhou", "name": "Guangzhou", "lat": 23.1291, "lon": 113.2644,
     "kind": "city", "note": "Inland basin of the Pearl. Cooler nights on this grid than the estuary."},
    {"id": "dongguan", "name": "Dongguan", "lat": 23.0205, "lon": 113.7518,
     "kind": "city", "note": "Corridor between Shenzhen and Guangzhou."},
    {"id": "zhuhai", "name": "Zhuhai", "lat": 22.2710, "lon": 113.5767,
     "kind": "city", "note": "West shore of Lingdingyang."},
    {"id": "macau", "name": "Macau", "lat": 22.1987, "lon": 113.5439,
     "kind": "city", "note": "Estuary city, marine nights."},
    {"id": "foshan", "name": "Foshan", "lat": 23.0215, "lon": 113.1216,
     "kind": "city", "note": "West of Guangzhou."},
    {"id": "zhongshan", "name": "Zhongshan", "lat": 22.5170, "lon": 113.3925,
     "kind": "city", "note": "Western PRD, between Zhuhai and Foshan."},
    {"id": "huizhou", "name": "Huizhou", "lat": 23.1115, "lon": 114.4158,
     "kind": "city", "note": "Eastern PRD."},
    {"id": "jiangmen", "name": "Jiangmen", "lat": 22.5787, "lon": 113.0815,
     "kind": "city", "note": "Western corridor."},
]

TRANSECT = [
    {"name": "Waglan Island", "lat": 22.1820, "lon": 114.3033},
    {"name": "HKO Headquarters", "lat": 22.3022, "lon": 114.1742},
    {"name": "Shenzhen", "lat": 22.5431, "lon": 114.0579},
    {"name": "Dongguan", "lat": 23.0205, "lon": 113.7518},
    {"name": "Guangzhou", "lat": 23.1291, "lon": 113.2644},
]


def grid_points() -> list[dict]:
    lats = [round(21.9 + i * STEP, 1) for i in range(9)]  # 21.9–23.5
    lons = [round(112.9 + i * STEP, 1) for i in range(10)]  # 112.9–114.7
    pts = []
    for lat in lats:
        for lon in lons:
            pts.append({
                "id": f"p_{lat:.1f}_{lon:.1f}",
                "name": f"{lat:.1f}°N {lon:.1f}°E",
                "lat": lat,
                "lon": lon,
                "kind": "grid",
                "note": "ERA5-Land sample, 0.2° Pearl River Delta lattice.",
            })
    return pts


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def dist_to_coast_km(lat: float, lon: float) -> float:
    return min(haversine_km(lat, lon, c[0], c[1]) for c in COAST)


def region_of(lat: float, lon: float) -> str:
    # Open water south of the estuary, not a municipal box.
    if lat <= 22.15:
        return "marine south"
    if 22.15 < lat <= 22.52 and 113.82 <= lon <= 114.44:
        return "Hong Kong"
    if 22.52 < lat <= 22.85 and 113.78 <= lon <= 114.40:
        return "Shenzhen"
    if 22.90 <= lat <= 23.50 and 113.05 <= lon <= 113.58:
        return "Guangzhou"
    if 22.85 <= lat <= 23.20 and 113.58 < lon <= 114.15:
        return "Dongguan"
    if lat <= 22.50 and lon <= 113.82:
        return "Zhuhai–Macau"
    if lat >= 22.90 and lon >= 114.15:
        return "Huizhou"
    return "wider PRD"


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
    for attempt in range(6):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Laidlaw-Heat-Project/prd-spatial"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = json.loads(resp.read().decode())
            break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(min(32, 2 ** attempt))
    if body is None:
        raise RuntimeError(f"Open-Meteo failed for {pt['id']}: {last_err}")
    elevation = float(body.get("elevation") if body.get("elevation") is not None else 0.0)
    daily = body["daily"]
    rows = []
    for i, date in enumerate(daily["time"]):
        tmax = daily["temperature_2m_max"][i]
        tmin = daily["temperature_2m_min"][i]
        tmean = daily["temperature_2m_mean"][i]
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
    time.sleep(0.12)
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
    hn_by_month, cd_by_month, vhd_by_month = [], [], []
    for m in range(1, 13):
        xs = [d for d in days if d["month"] == m]
        climatology.append(round(sum(d["tmean"] for d in xs) / len(xs), 3) if xs else None)
        hn_by_month.append(sum(d["hn"] for d in xs))
        cd_by_month.append(sum(d["cd"] for d in xs))
        vhd_by_month.append(sum(d["vhd"] for d in xs))
    amp = max(x for x in climatology if x is not None) - min(x for x in climatology if x is not None)
    jja_hn = hn_by_month[5] + hn_by_month[6] + hn_by_month[7]
    return {
        **pt,
        "n_days": len(days),
        "elevation_m": round(elevation, 1),
        "dist_coast_km": round(dist_to_coast_km(pt["lat"], pt["lon"]), 2),
        "dist_hq_km": round(haversine_km(pt["lat"], pt["lon"], 22.3022, 114.1742), 2),
        "region": region_of(pt["lat"], pt["lon"]),
        "mean_t": round(sum(tmeans) / len(tmeans), 3),
        "mean_tmin": round(sum(tmins) / len(tmins), 3),
        "mean_tmax": round(sum(tmaxs) / len(tmaxs), 3),
        "p05_tmin": round(float(np.percentile(tmins, 5)), 3),
        "p95_tmax": round(float(np.percentile(tmaxs, 95)), 3),
        "seasonal_amp": round(amp, 3),
        "hn_total": sum(d["hn"] for d in days),
        "vhd_total": sum(d["vhd"] for d in days),
        "cd_total": sum(d["cd"] for d in days),
        "jja_hn": jja_hn,
        "hn_by_month": hn_by_month,
        "cd_by_month": cd_by_month,
        "vhd_by_month": vhd_by_month,
        "climatology_mean_t": climatology,
        "fingerprint": series_fingerprint(days),
        "provenance": "OPEN_METEO_ERA5_LAND_PUBLIC",
    }


def ols(y: np.ndarray, X: np.ndarray) -> dict:
    n, k = X.shape
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
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
    aic = n * math.log(max(sse / n, 1e-12)) + 2 * k
    return {
        "n": int(n),
        "k": int(k),
        "beta": [round(float(b), 4) for b in beta],
        "se": [round(float(s), 4) for s in se],
        "r2": round(float(r2), 4),
        "rmse": round(float(np.sqrt(np.mean(resid ** 2))), 3),
        "aic": round(float(aic), 2),
        "fitted": fitted,
        "resid": resid,
    }


def distance_weights(coords: list[tuple[float, float]], cutoff_km: float, include_self: bool = False) -> np.ndarray:
    n = len(coords)
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                if include_self:
                    w[i, j] = 1.0
                continue
            d = haversine_km(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            if d <= cutoff_km:
                w[i, j] = 1.0
    return w


def row_standardize(w: np.ndarray) -> np.ndarray:
    rs = w.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1.0
    return w / rs


def morans_i(values: np.ndarray, w: np.ndarray) -> dict:
    n = len(values)
    z = values - values.mean()
    wsum = float(w.sum())
    if wsum < 1e-9:
        return {"I": None, "expected": round(-1.0 / (n - 1), 4), "W": 0, "cutoff_km": W_CUTOFF_KM}
    num = float(z @ w @ z)
    den = float(z @ z)
    I = (n / wsum) * (num / den) if den else float("nan")
    return {
        "I": round(float(I), 4),
        "expected": round(-1.0 / (n - 1), 4),
        "W": round(wsum, 1),
        "cutoff_km": W_CUTOFF_KM,
        "mean_neighbors": round(wsum / n, 2),
    }


def moran_scatter(values: np.ndarray, ws: np.ndarray) -> list[list[float]]:
    z = (values - values.mean()) / (values.std() if values.std() else 1.0)
    wz = ws @ z
    return [[round(float(a), 4), round(float(b), 4)] for a, b in zip(z, wz)]


def variogram(values: np.ndarray, coords: list[tuple[float, float]]) -> list[dict]:
    edges = [0, 25, 40, 60, 85, 120, 170]
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
            "bin_km": f"{edges[b]}–{edges[b + 1]}",
            "mid_km": round((edges[b] + edges[b + 1]) / 2, 1),
            "n_pairs": len(xs),
            "gamma": round(float(np.mean(xs)), 4) if xs else None,
        })
    return out


def getis_ord_gistar(values: np.ndarray, coords: list[tuple[float, float]], cutoff_km: float) -> np.ndarray:
    n = len(values)
    x = values.astype(float)
    xbar = float(x.mean())
    s = float(x.std(ddof=1))
    z = np.zeros(n)
    for i in range(n):
        w = np.array([
            1.0 if (i == j or haversine_km(coords[i][0], coords[i][1], coords[j][0], coords[j][1]) <= cutoff_km) else 0.0
            for j in range(n)
        ])
        wsum = float(w.sum())
        w2 = float((w ** 2).sum())
        num = float(w @ x) - xbar * wsum
        den = s * math.sqrt(max((n * w2 - wsum ** 2) / (n - 1), 0.0))
        z[i] = num / den if den > 1e-12 else 0.0
    return z


def spatial_lag_2sls(y: np.ndarray, X: np.ndarray, ws: np.ndarray) -> dict:
    wy = ws @ y
    wx = ws @ X[:, 1:]
    z = np.column_stack([X, wx])
    fs = ols(wy, z)
    wy_hat = fs["fitted"]
    x2 = np.column_stack([X, wy_hat])
    ss = ols(y, x2)
    return {
        "rho": ss["beta"][-1],
        "rho_se": ss["se"][-1],
        "beta": ss["beta"][:-1],
        "se": ss["se"][:-1],
        "r2": ss["r2"],
        "rmse": ss["rmse"],
        "aic": ss["aic"],
        "resid": ss["resid"],
        "wy": [round(float(v), 4) for v in wy],
        "note": "Anselin 2SLS: WX instruments Wy. R² is a fit diagnostic, not a likelihood.",
    }


def pearson(x: np.ndarray, y: np.ndarray) -> float:
    if x.std() < 1e-12 or y.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def nearest_grid(lat: float, lon: float, grid: list[dict]) -> dict:
    return min(grid, key=lambda s: haversine_km(lat, lon, s["lat"], s["lon"]))


def write_csv(path: Path, rows: list[dict], skip: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in r.items() if k not in skip} for r in rows]
    if not slim:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(slim[0].keys()))
        w.writeheader()
        w.writerows(slim)


def cell_polygon(lat: float, lon: float, half: float = STEP / 2) -> list[list[float]]:
    return [
        [lon - half, lat - half],
        [lon + half, lat - half],
        [lon + half, lat + half],
        [lon - half, lat + half],
        [lon - half, lat - half],
    ]


def write_transect_svg(rows: list[dict], path: Path) -> None:
    if len(rows) < 2:
        return
    w, h = 760, 280
    xs = list(range(len(rows)))
    ys = [r["mean_tmin"] for r in rows]
    hns = [r["hn_total"] for r in rows]
    ymin, ymax = min(ys) - 0.4, max(ys) + 0.4
    hmax = max(hns) if max(hns) else 1

    def xx(i):
        return 70 + i / (len(rows) - 1) * 640

    def yy(v):
        return 40 + (ymax - v) / (ymax - ymin) * 180

    path_d = " ".join(f"{'M' if i == 0 else 'L'}{xx(i):.1f},{yy(v):.1f}" for i, v in enumerate(ys))
    labels = []
    for i, r in enumerate(rows):
        labels.append(
            f'<text x="{xx(i):.1f}" y="250" text-anchor="middle" font-size="11" fill="#5b6773">{r["name"]}</text>'
        )
        labels.append(
            f'<circle cx="{xx(i):.1f}" cy="{yy(r["mean_tmin"]):.1f}" r="{4 + 10 * r["hn_total"] / hmax:.1f}" fill="#c24e16" fill-opacity=".85"/>'
        )
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#fffdf8"/>',
        '<text x="380" y="22" text-anchor="middle" font-family="Georgia, serif" font-size="15">Waglan → Guangzhou night Tmin (circle = ERA5 hot nights)</text>',
        f'<path d="{path_d}" fill="none" stroke="#0c6b74" stroke-width="2.4"/>',
        *labels,
        "</svg>",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(svg) + "\n")


def collect_point(pt: dict, skip: bool) -> dict:
    raw, elev = fetch_point(pt, skip=skip)
    days = encode(raw)
    s = summarise(pt, days, elev)
    print(
        f"{pt['id']:22s} {s['region']:14s} elev={s['elevation_m']:6.1f}m  "
        f"Tmin={s['mean_tmin']:6.2f}  HN={s['hn_total']:4d}  CD={s['cd_total']:4d}",
        flush=True,
    )
    return s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-fetch", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    skip = args.skip_fetch or os.environ.get("PRD_SPATIAL_SKIP_FETCH") == "1"

    points = grid_points() + CITIES
    summaries: list[dict] = []
    if skip:
        for pt in points:
            summaries.append(collect_point(pt, skip=True))
    else:
        workers = max(1, min(args.workers, 6))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = {pool.submit(collect_point, pt, False): pt["id"] for pt in points}
            by_id = {}
            for fut in as_completed(futs):
                pid = futs[fut]
                try:
                    by_id[pid] = fut.result()
                except Exception as exc:
                    raise RuntimeError(f"fetch failed for {pid}: {exc}") from exc
        summaries = [by_id[pt["id"]] for pt in points]

    fps: dict[str, list[str]] = {}
    for s in summaries:
        fps.setdefault(s["fingerprint"], []).append(s["id"])

    grid = [s for s in summaries if s["kind"] == "grid"]
    cities = [s for s in summaries if s["kind"] == "city"]
    y = np.array([s["mean_tmin"] for s in grid], dtype=float)
    hn = np.array([s["hn_total"] for s in grid], dtype=float)
    coords = [(s["lat"], s["lon"]) for s in grid]
    X = np.column_stack([
        np.ones(len(grid)),
        [s["elevation_m"] for s in grid],
        [s["lat"] for s in grid],
        [s["lon"] for s in grid],
    ])
    w = distance_weights(coords, W_CUTOFF_KM, include_self=False)
    ws = row_standardize(w)

    fit_ols = ols(y, X)
    wx = ws @ X[:, 1:]
    Xslx = np.column_stack([X, wx])
    fit_slx = ols(y, Xslx)
    sar = spatial_lag_2sls(y, X, ws)

    moran_raw = morans_i(y, w)
    moran_ols = morans_i(fit_ols["resid"], w)
    moran_slx = morans_i(fit_slx["resid"], w)
    moran_sar = morans_i(sar["resid"], w)
    moran_hn = morans_i(hn, w)
    scatter = moran_scatter(y, ws)
    vgm = variogram(y, coords)
    gi = getis_ord_gistar(hn, coords, W_CUTOFF_KM)

    for s, fval, rval, slx_r, sar_r, gi_z, wy in zip(
        grid, fit_ols["fitted"], fit_ols["resid"], fit_slx["resid"], sar["resid"], gi, sar["wy"]
    ):
        s["tmin_fitted"] = round(float(fval), 3)
        s["tmin_resid"] = round(float(rval), 3)
        s["tmin_slx_resid"] = round(float(slx_r), 3)
        s["tmin_sar_resid"] = round(float(sar_r), 3)
        s["hn_gi_z"] = round(float(gi_z), 3)
        s["wy_tmin"] = wy
        if gi_z > 1.96:
            s["hn_cluster"] = "hotspot"
        elif gi_z < -1.96:
            s["hn_cluster"] = "coldspot"
        else:
            s["hn_cluster"] = "none"

    hq_cell = nearest_grid(22.3022, 114.1742, grid)
    feats = np.column_stack([
        [s["mean_tmin"] for s in grid],
        [s["hn_total"] for s in grid],
        [s["cd_total"] for s in grid],
        [s["seasonal_amp"] for s in grid],
    ]).astype(float)
    feats = (feats - feats.mean(0)) / np.where(feats.std(0) < 1e-9, 1.0, feats.std(0))
    hq_vec = feats[grid.index(hq_cell)]
    thermal = np.linalg.norm(feats - hq_vec, axis=1)
    geo = np.array([s["dist_hq_km"] for s in grid], dtype=float)
    r_td = pearson(thermal, geo)
    for s, td in zip(grid, thermal):
        s["thermal_distance"] = round(float(td), 3)

    for s in summaries:
        for key in (
            "tmin_fitted", "tmin_resid", "tmin_slx_resid", "tmin_sar_resid",
            "hn_gi_z", "hn_cluster", "wy_tmin", "thermal_distance",
        ):
            s.setdefault(key, None)

    regional = {}
    for name in ("marine south", "Hong Kong", "Shenzhen", "Guangzhou", "Dongguan", "Zhuhai–Macau", "Huizhou", "wider PRD"):
        xs = [s for s in grid if s["region"] == name]
        if not xs:
            continue
        regional[name] = {
            "n": len(xs),
            "mean_tmin": round(sum(s["mean_tmin"] for s in xs) / len(xs), 3),
            "hn_mean": round(sum(s["hn_total"] for s in xs) / len(xs), 1),
            "cd_mean": round(sum(s["cd_total"] for s in xs) / len(xs), 1),
            "jja_hn_mean": round(sum(s["jja_hn"] for s in xs) / len(xs), 1),
        }

    transect_rows = []
    for stop in TRANSECT:
        cell = nearest_grid(stop["lat"], stop["lon"], grid)
        transect_rows.append({
            "name": stop["name"],
            "lat": stop["lat"],
            "lon": stop["lon"],
            "cell_id": cell["id"],
            "mean_tmin": cell["mean_tmin"],
            "hn_total": cell["hn_total"],
            "cd_total": cell["cd_total"],
            "dist_hq_km": round(haversine_km(stop["lat"], stop["lon"], 22.3022, 114.1742), 2),
            "region": cell["region"],
        })

    n_hotspot = sum(1 for s in grid if s["hn_cluster"] == "hotspot")
    n_coldspot = sum(1 for s in grid if s["hn_cluster"] == "coldspot")
    hk_hn = regional.get("Hong Kong", {}).get("hn_mean")
    gz_hn = regional.get("Guangzhou", {}).get("hn_mean")
    sz_hn = regional.get("Shenzhen", {}).get("hn_mean")

    model = {
        "outcome": "ERA5-Land mean daily Tmin, 2013–2023, 0.2° PRD lattice",
        "weights": {"type": "binary distance", "cutoff_km": W_CUTOFF_KM, "row_standardized_for_lag": True},
        "ols": {
            "formula": "mean_tmin ~ elevation_m + lat + lon",
            "r2": fit_ols["r2"],
            "rmse": fit_ols["rmse"],
            "aic": fit_ols["aic"],
            "beta": {
                "intercept": {"beta": fit_ols["beta"][0], "se": fit_ols["se"][0]},
                "elevation_m": {"beta": fit_ols["beta"][1], "se": fit_ols["se"][1], "unit": "°C per metre"},
                "lat": {"beta": fit_ols["beta"][2], "se": fit_ols["se"][2], "unit": "°C per degree north"},
                "lon": {"beta": fit_ols["beta"][3], "se": fit_ols["se"][3], "unit": "°C per degree east"},
            },
            "moran_residual": moran_ols,
        },
        "slx": {
            "formula": "mean_tmin ~ X + WX  (X = elevation, lat, lon)",
            "r2": fit_slx["r2"],
            "rmse": fit_slx["rmse"],
            "aic": fit_slx["aic"],
            "beta": {
                "intercept": fit_slx["beta"][0],
                "elevation_m": fit_slx["beta"][1],
                "lat": fit_slx["beta"][2],
                "lon": fit_slx["beta"][3],
                "W_elevation_m": fit_slx["beta"][4],
                "W_lat": fit_slx["beta"][5],
                "W_lon": fit_slx["beta"][6],
            },
            "se": fit_slx["se"],
            "moran_residual": moran_slx,
            "note": "Spatial lag of X. Neighbours' elevation and latitude can shift a cell without lagging the outcome.",
        },
        "sar_2sls": {
            "formula": "mean_tmin ~ elevation_m + lat + lon + W mean_tmin",
            "rho": sar["rho"],
            "rho_se": sar["rho_se"],
            "r2": sar["r2"],
            "rmse": sar["rmse"],
            "aic": sar["aic"],
            "beta": {
                "intercept": sar["beta"][0],
                "elevation_m": sar["beta"][1],
                "lat": sar["beta"][2],
                "lon": sar["beta"][3],
            },
            "moran_residual": moran_sar,
            "note": sar["note"],
        },
        "moran_raw_tmin": moran_raw,
        "moran_hn": moran_hn,
        "moran_scatter_tmin": scatter,
        "variogram_tmin": vgm,
        "getis_ord_hn": {
            "cutoff_km": W_CUTOFF_KM,
            "n_hotspot_z_gt_1_96": n_hotspot,
            "n_coldspot_z_lt_m1_96": n_coldspot,
            "note": "Gi* z-score on annual ERA5 hot-night counts, binary weights including self.",
        },
        "thermal_vs_geographic": {
            "features": ["mean_tmin", "hn_total", "cd_total", "seasonal_amp"],
            "pearson_r": round(r_td, 4),
            "hq_anchor_cell": hq_cell["id"],
            "note": "Euclidean distance in z-scored climate space versus km from Headquarters. High r means climate follows the map; low r means local marine/ridge effects dominate.",
        },
        "regional_means": regional,
        "transect": transect_rows,
        "unique_fingerprints": len(fps),
        "n_points": len(summaries),
        "n_grid": len(grid),
        "n_cities": len(cities),
        "hong_kong_vs_guangzhou_hn_mean": None if hk_hn is None or gz_hn is None else round(hk_hn - gz_hn, 1),
        "shenzhen_hn_mean": sz_hn,
        "note": (
            "A 0.2° cell is not a city, a weather station, or a hospital catchment. "
            "Open-Meteo applies DEM elevation. Do not transport Hong Kong CHD/HF ratios "
            "across this mosaic. Live paper stays on HKO Headquarters."
        ),
    }

    skip_keys = {"climatology_mean_t", "hn_by_month", "cd_by_month", "vhd_by_month"}
    write_csv(OUT_TAB / "prd_spatial_cells.csv", summaries, skip_keys)
    (OUT_TAB / "prd_spatial_model.json").write_text(json.dumps(model, indent=2) + "\n")

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
        "title": "Pearl River Delta thermal mosaic",
        "window": {"start": START, "end": END, "n_years": 11},
        "provenance": "REAL_PUBLIC. Open-Meteo ERA5-Land daily 2 m temperatures on a 0.2° lattice plus named city coordinates. Exposure descriptives only. No health outcomes. No project coefficients.",
        "step_deg": STEP,
        "months": MONTHS,
        "thresholds_hko": {"hot_night_tmin_ge": HN_C, "very_hot_day_tmax_ge": VHD_C, "cold_day_tmin_le": CD_C},
        "model": model,
        "cells": summaries,
        "geojson": fc,
        "claim_boundaries": [
            "Do not treat this mosaic as HKO Headquarters or as CMA city stations.",
            "Do not overlay CHD/HF or stroke counts on cells, districts, or prefectures.",
            "A 0.2° cell is not a person, a building, or a city.",
            "Do not transport Hong Kong hospitalisation ratios to Shenzhen or Guangzhou.",
            "Live paper stays on HKO official flags.",
        ],
    }
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    js = "window.PRD_SPATIAL = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    (OUT_DOCS / "prd_embed.js").write_text(js)
    (OUT_TAB / "prd_spatial_field.json").write_text(json.dumps(payload, indent=2) + "\n")
    write_transect_svg(transect_rows, OUT_FIG / "prd_waglan_guangzhou_transect.svg")
    write_transect_svg(transect_rows, OUT_DOCS / "prd_waglan_guangzhou_transect.svg")

    print("unique fingerprints", len(fps), "of", len(summaries))
    print("OLS R2", fit_ols["r2"], "SLX R2", fit_slx["r2"], "SAR rho", sar["rho"], "SAR R2", sar["r2"])
    print("Moran raw", moran_raw["I"], "OLS resid", moran_ols["I"], "SAR resid", moran_sar["I"])
    print("Gi* hotspots", n_hotspot, "coldspots", n_coldspot)
    print("thermal vs geo r", round(r_td, 4))
    print("regional HN", {k: v["hn_mean"] for k, v in regional.items()})
    print("wrote", OUT_DOCS / "prd_embed.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
