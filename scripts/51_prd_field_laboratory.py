#!/usr/bin/env python3
"""Pearl River Delta space-time field laboratory, 2013–2023.

Eight methods on the same public ERA5-Land Tmin field (90 cells × 4017 days):
EOF/PCA, annual harmonics, Theil–Sen + Mann–Kendall, k-means regimes,
spatial entropy / mutual information, hot-night spells, P(HN|VHD),
Wasserstein-1 distances, and an anomaly-correlation network.

EXPOSURE ONLY. No health coefficients. No HA rows. No district overlay.
Reuses the cache from scripts/50_prd_thermal_mosaic.py. Live paper stays
on HKO Headquarters.

Usage:
  python3 scripts/51_prd_field_laboratory.py
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_TAB = ROOT / "outputs" / "prd_field"
OUT_DOCS = ROOT / "docs" / "field"
K_CLUSTERS = 4
CORR_EDGE = 0.90
N_BOOT = 120
RNG_SEED = 20260814


def load_prd():
    spec = importlib.util.spec_from_file_location(
        "prd50", ROOT / "scripts" / "50_prd_thermal_mosaic.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def theil_sen_slope(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    slopes = []
    n = len(x)
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[j] - x[i]
            if dx != 0.0:
                slopes.append((y[j] - y[i]) / dx)
    if not slopes:
        return float("nan")
    return float(np.median(slopes))


def theil_sen_ci(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, n_boot: int = N_BOOT) -> tuple[float, float, float]:
    slope = theil_sen_slope(x, y)
    n = len(x)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boots[b] = theil_sen_slope(x[idx], y[idx])
    lo, hi = np.percentile(boots, [5.0, 95.0])
    return slope, float(lo), float(hi)


def mann_kendall_s(y: np.ndarray) -> int:
    y = np.asarray(y, float)
    s = 0
    n = len(y)
    for i in range(n):
        for j in range(i + 1, n):
            d = y[j] - y[i]
            if d > 0:
                s += 1
            elif d < 0:
                s -= 1
    return int(s)


def harmonic_amp_phase(y: np.ndarray, t_index: np.ndarray) -> tuple[float, float, float]:
    """Annual cycle: y ~ a0 + a cos(ωt) + b sin(ωt). Peak day of year from phase."""
    y = np.asarray(y, float)
    t_index = np.asarray(t_index, float)
    omega = 2.0 * math.pi / 365.25
    x = np.column_stack([
        np.ones(len(y)),
        np.cos(omega * t_index),
        np.sin(omega * t_index),
    ])
    beta, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    a0, a, b = (float(v) for v in beta)
    amp = math.hypot(a, b)
    phi = math.atan2(b, a)
    t_peak = (phi / omega) % 365.25
    return amp, t_peak, a0


def eof_svd(anom: np.ndarray, lats: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Area-weighted SVD. anom is (time, space). Returns EOFs (k, space), PCs (time, k), var frac, singular values."""
    w = np.sqrt(np.maximum(0.05, np.cos(np.deg2rad(lats))))
    x = anom * w
    x = x - x.mean(axis=0)
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    eofs = vt / w
    pcs = u * s
    var = (s ** 2) / np.sum(s ** 2)
    return eofs, pcs, var, s


def flip_to_marine_positive(eof: np.ndarray, pc: np.ndarray, marine_mask: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if marine_mask.any() and float(eof[marine_mask].mean()) < 0:
        return -eof, -pc
    return eof, pc


def north_separated(s: np.ndarray, n_eff: float, k: int = 0) -> bool:
    lam = s ** 2
    if k + 1 >= len(lam) or n_eff <= 2:
        return False
    delta = float(lam[k] * math.sqrt(2.0 / n_eff))
    return abs(float(lam[k] - lam[k + 1])) > delta


def kmeans(x: np.ndarray, k: int, rng: np.random.Generator, n_init: int = 8, max_iter: int = 80) -> tuple[np.ndarray, np.ndarray, float]:
    x = np.asarray(x, float)
    n, p = x.shape
    best = None
    for _ in range(n_init):
        centers = np.empty((k, p))
        centers[0] = x[int(rng.integers(n))]
        d2 = np.sum((x - centers[0]) ** 2, axis=1)
        for c in range(1, k):
            total = float(d2.sum())
            if total <= 0:
                centers[c] = x[int(rng.integers(n))]
            else:
                centers[c] = x[int(rng.choice(n, p=d2 / total))]
            d2 = np.minimum(d2, np.sum((x - centers[c]) ** 2, axis=1))
        labels = np.zeros(n, dtype=int)
        for _it in range(max_iter):
            dist = np.linalg.norm(x[:, None, :] - centers[None, :, :], axis=2)
            new_labels = dist.argmin(axis=1)
            new_centers = centers.copy()
            for c in range(k):
                mask = new_labels == c
                if mask.any():
                    new_centers[c] = x[mask].mean(axis=0)
                else:
                    new_centers[c] = x[int(np.argmax(dist.min(axis=1)))]
            if np.array_equal(new_labels, labels) and np.allclose(new_centers, centers):
                break
            labels, centers = new_labels, new_centers
        inertia = float(np.sum((x - centers[labels]) ** 2))
        if best is None or inertia < best[0]:
            best = (inertia, labels.copy(), centers.copy())
    return best[1], best[2], best[0]


def name_clusters(labels: np.ndarray, hn: np.ndarray, elev: np.ndarray, k: int = K_CLUSTERS) -> dict[int, str]:
    stats = []
    for c in range(k):
        m = labels == c
        if not m.any():
            stats.append((c, -1.0, -1.0, 0))
            continue
        stats.append((c, float(hn[m].mean()), float(elev[m].mean()), int(m.sum())))
    by_hn = sorted(stats, key=lambda z: -z[1])
    names: dict[int, str] = {}
    if by_hn:
        names[by_hn[0][0]] = "marine"
    if len(by_hn) > 1:
        names[by_hn[1][0]] = "estuary"
    rest = sorted(by_hn[2:], key=lambda z: -z[2])
    if rest:
        names[rest[0][0]] = "highland"
    if len(rest) > 1:
        names[rest[1][0]] = "inland"
    for c, _, _, _ in stats:
        names.setdefault(c, f"cluster {c}")
    return names


def binary_mi(x: np.ndarray, y: np.ndarray) -> float:
    """Mutual information of two binary series, bits."""
    x = np.asarray(x, int)
    y = np.asarray(y, int)
    n = len(x)
    if n == 0:
        return 0.0
    mi = 0.0
    for a in (0, 1):
        px = float(np.mean(x == a))
        for b in (0, 1):
            py = float(np.mean(y == b))
            pxy = float(np.mean((x == a) & (y == b)))
            if pxy > 0.0 and px > 0.0 and py > 0.0:
                mi += pxy * math.log(pxy / (px * py), 2)
    return float(mi)


def shannon_evenness(weights: np.ndarray) -> dict:
    w = np.asarray(weights, float)
    w = np.clip(w, 0, None)
    total = float(w.sum())
    n = len(w)
    if total <= 0 or n < 2:
        return {"H": 0.0, "H_max": math.log(max(n, 2), 2), "evenness": 0.0}
    p = w / total
    p = p[p > 0]
    h = float(-np.sum(p * np.log2(p)))
    h_max = math.log(n, 2)
    return {"H": round(h, 4), "H_max": round(h_max, 4), "evenness": round(h / h_max, 4)}


def spell_stats(flag: np.ndarray) -> dict:
    runs = []
    cur = 0
    for v in np.asarray(flag, int):
        if v:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    if not runs:
        return {"n_spells": 0, "mean": 0.0, "max": 0}
    return {"n_spells": len(runs), "mean": float(np.mean(runs)), "max": int(max(runs))}


def wasserstein1(a: np.ndarray, b: np.ndarray) -> float:
    a = np.sort(np.asarray(a, float))
    b = np.sort(np.asarray(b, float))
    n = min(len(a), len(b))
    if n == 0:
        return float("nan")
    if len(a) != len(b):
        qa = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(a)), a)
        qb = np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(b)), b)
        return float(np.mean(np.abs(qa - qb)))
    return float(np.mean(np.abs(a - b)))


def harmonic_month_curve(amp: float, t_peak: float, a0: float) -> list[float]:
    omega = 2.0 * math.pi / 365.25
    mids = [15, 46, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350]
    phi = t_peak * omega
    return [round(a0 + amp * math.cos(omega * d - phi), 3) for d in mids]


def cond_prob(event: np.ndarray, given: np.ndarray) -> float | None:
    g = np.asarray(given, int) == 1
    if int(g.sum()) == 0:
        return None
    return float(np.mean(np.asarray(event, int)[g] == 1))


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    if a.std() < 1e-12 or b.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def zscore_cols(x: np.ndarray) -> np.ndarray:
    mu = x.mean(axis=0)
    sd = x.std(axis=0)
    sd[sd < 1e-12] = 1.0
    return (x - mu) / sd


def seasonal_anomaly(tmin: np.ndarray, doy: np.ndarray) -> np.ndarray:
    tmin = np.asarray(tmin, float)
    doy = np.asarray(doy, int)
    t, n = tmin.shape
    clim = np.zeros((366, n))
    count = np.zeros((366, n))
    for i in range(t):
        d = doy[i] - 1
        clim[d] += tmin[i]
        count[d] += 1
    with np.errstate(invalid="ignore", divide="ignore"):
        clim = np.divide(clim, count, out=np.zeros_like(clim), where=count > 0)
    for d in range(366):
        missing = count[d] == 0
        if missing.any():
            prev = clim[(d - 1) % 366]
            clim[d, missing] = prev[missing]
    anom = np.empty_like(tmin)
    for i in range(t):
        anom[i] = tmin[i] - clim[doy[i] - 1]
    return anom


def load_cube(prd) -> dict:
    pts = prd.grid_points()
    encoded = []
    elevs = []
    for pt in pts:
        path = prd.cache_path(pt["id"])
        meta_path = path.with_suffix(".meta.json")
        if not prd.cache_complete(path) or not meta_path.exists():
            raise RuntimeError(
                f"Incomplete cache for {pt['id']}. Run scripts/50_prd_thermal_mosaic.py first."
            )
        rows = list(csv.DictReader(path.open()))
        encoded.append(prd.encode(rows))
        elevs.append(float(json.loads(meta_path.read_text())["elevation"]))
    dates0 = [d["date"] for d in encoded[0]]
    for days in encoded[1:]:
        if [d["date"] for d in days] != dates0:
            raise RuntimeError("Grid cell date axes do not align.")
    tmin = np.array([[d["tmin"] for d in days] for days in encoded], dtype=float).T
    tmax = np.array([[d["tmax"] for d in days] for days in encoded], dtype=float).T
    hn = np.array([[d["hn"] for d in days] for days in encoded], dtype=int).T
    vhd = np.array([[d["vhd"] for d in days] for days in encoded], dtype=int).T
    years = np.array([d["year"] for d in encoded[0]], dtype=int)
    months = np.array([d["month"] for d in encoded[0]], dtype=int)
    doy = np.array(
        [datetime.strptime(d, "%Y-%m-%d").timetuple().tm_yday for d in dates0],
        dtype=int,
    )
    t_index = np.arange(len(dates0), dtype=float)
    lats = np.array([p["lat"] for p in pts], dtype=float)
    lons = np.array([p["lon"] for p in pts], dtype=float)
    return {
        "pts": pts,
        "dates": dates0,
        "tmin": tmin,
        "tmax": tmax,
        "hn": hn,
        "vhd": vhd,
        "years": years,
        "months": months,
        "doy": doy,
        "t_index": t_index,
        "lats": lats,
        "lons": lons,
        "elevs": np.array(elevs, dtype=float),
    }


def nearest_index(lats: np.ndarray, lons: np.ndarray, lat: float, lon: float, prd) -> int:
    d = [prd.haversine_km(lat, lon, a, b) for a, b in zip(lats, lons)]
    return int(np.argmin(d))


def write_csv(path: Path, rows: list[dict], skip: set[str] | None = None) -> None:
    skip = skip or set()
    if not rows:
        return
    keys = [k for k in rows[0].keys() if k not in skip]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in keys})


def main() -> int:
    prd = load_prd()
    cube = load_cube(prd)
    pts = cube["pts"]
    tmin = cube["tmin"]
    hn = cube["hn"]
    vhd = cube["vhd"]
    lats, lons, elevs = cube["lats"], cube["lons"], cube["elevs"]
    n_t, n_s = tmin.shape
    rng = np.random.default_rng(RNG_SEED)

    anom = seasonal_anomaly(tmin, cube["doy"])
    eofs, pcs, var, svals = eof_svd(anom, lats)
    marine = np.array([prd.region_of(p["lat"], p["lon"]) == "marine south" for p in pts])
    for k in range(min(3, eofs.shape[0])):
        eofs[k], pcs[:, k] = flip_to_marine_positive(eofs[k], pcs[:, k], marine)

    r_lag1 = pearson(pcs[1:, 0], pcs[:-1, 0])
    n_eff = n_t * (1.0 - r_lag1) / (1.0 + r_lag1) if abs(r_lag1) < 0.999 else 2.0
    n_eff = max(n_eff, 2.0)

    hq_i = nearest_index(lats, lons, 22.3022, 114.1742, prd)
    wag_i = nearest_index(lats, lons, 22.1820, 114.3033, prd)
    gz_i = nearest_index(lats, lons, 23.1291, 113.2644, prd)

    years_u = np.array(sorted(set(cube["years"].tolist())))
    yearly = np.stack([tmin[cube["years"] == y].mean(axis=0) for y in years_u], axis=0)

    corr = np.corrcoef(anom.T)
    np.fill_diagonal(corr, 0.0)
    edges = int(np.sum(np.triu(corr > CORR_EDGE, 1)))
    degree = (corr > CORR_EDGE).sum(axis=1)

    hn_tot = hn.sum(axis=0).astype(float)
    entropy = shannon_evenness(hn_tot)
    hq_hn = hn[:, hq_i]

    monthly_pc = []
    cal_pc1 = np.zeros(12)
    cal_n = np.zeros(12)
    for year in years_u:
        for month in range(1, 13):
            mask = (cube["years"] == year) & (cube["months"] == month)
            if not mask.any():
                continue
            pc1_m = float(pcs[mask, 0].mean())
            pc2_m = float(pcs[mask, 1].mean())
            monthly_pc.append({
                "year": int(year), "month": int(month),
                "pc1": round(pc1_m, 4), "pc2": round(pc2_m, 4),
            })
            cal_pc1[month - 1] += pc1_m
            cal_n[month - 1] += 1
    cal_pc1 = np.divide(cal_pc1, cal_n, out=np.zeros(12), where=cal_n > 0)

    cells = []
    feature_rows = []
    for j, pt in enumerate(pts):
        amp, t_peak, a0 = harmonic_amp_phase(tmin[:, j], cube["t_index"])
        slope, lo, hi = theil_sen_ci(years_u.astype(float), yearly[:, j], rng)
        mk = mann_kendall_s(yearly[:, j])
        spells = spell_stats(hn[:, j])
        p_hn_vhd = cond_prob(hn[:, j], vhd[:, j])
        p_vhd_hn = cond_prob(vhd[:, j], hn[:, j])
        mi = binary_mi(hq_hn, hn[:, j])
        w1 = wasserstein1(tmin[:, hq_i], tmin[:, j])
        dist_coast = prd.dist_to_coast_km(pt["lat"], pt["lon"])
        dist_hq = prd.haversine_km(pt["lat"], pt["lon"], 22.3022, 114.1742)
        rec_month = [round(float(cal_pc1[m] * eofs[0, j]), 4) for m in range(12)]
        harm_month = harmonic_month_curve(amp, t_peak, a0)
        row = {
            **pt,
            "kind": "grid",
            "region": prd.region_of(pt["lat"], pt["lon"]),
            "n_days": n_t,
            "elevation_m": round(float(elevs[j]), 1),
            "dist_coast_km": round(dist_coast, 2),
            "dist_hq_km": round(dist_hq, 2),
            "mean_tmin": round(float(tmin[:, j].mean()), 3),
            "hn_total": int(hn_tot[j]),
            "vhd_total": int(vhd[:, j].sum()),
            "eof1": round(float(eofs[0, j]), 4),
            "eof2": round(float(eofs[1, j]), 4),
            "eof3": round(float(eofs[2, j]), 4),
            "pc1_recon_by_month": rec_month,
            "harmonic_by_month": harm_month,
            "harmonic_amp": round(amp, 3),
            "harmonic_doy_max": round(t_peak, 1),
            "harmonic_mean": round(a0, 3),
            "theil_sen_c_per_decade": round(slope * 10.0, 4),
            "theil_sen_p05": round(lo * 10.0, 4),
            "theil_sen_p95": round(hi * 10.0, 4),
            "mann_kendall_s": mk,
            "mi_hq_bits": round(mi, 4),
            "spell_n": spells["n_spells"],
            "spell_mean": round(spells["mean"], 3),
            "spell_max": spells["max"],
            "p_hn_given_vhd": None if p_hn_vhd is None else round(p_hn_vhd, 4),
            "p_vhd_given_hn": None if p_vhd_hn is None else round(p_vhd_hn, 4),
            "wasserstein_hq": round(w1, 3),
            "corr_degree_r90": int(degree[j]),
            "provenance": "OPEN_METEO_ERA5_LAND_PUBLIC",
        }
        cells.append(row)
        feature_rows.append([
            row["mean_tmin"], row["hn_total"], amp, dist_coast, elevs[j],
        ])

    feats = zscore_cols(np.array(feature_rows, float))
    labels, centers, inertia = kmeans(feats, K_CLUSTERS, rng)
    names = name_clusters(
        labels,
        np.array([c["hn_total"] for c in cells], float),
        elevs,
    )
    for j, row in enumerate(cells):
        row["cluster"] = int(labels[j])
        row["cluster_name"] = names[int(labels[j])]

    cluster_summary = []
    for c in range(K_CLUSTERS):
        m = labels == c
        cluster_summary.append({
            "id": c,
            "name": names[c],
            "n": int(m.sum()),
            "mean_tmin": round(float(np.mean([cells[i]["mean_tmin"] for i in range(n_s) if m[i]])), 3),
            "hn_mean": round(float(np.mean([cells[i]["hn_total"] for i in range(n_s) if m[i]])), 1),
            "elev_mean": round(float(elevs[m].mean()), 1),
        })

    eof1_lat = pearson(eofs[0], lats)
    eof1_coast = pearson(eofs[0], np.array([c["dist_coast_km"] for c in cells], float))
    eof1_hn = pearson(eofs[0], hn_tot)

    xcorr0 = pearson(anom[:, hq_i], anom[:, wag_i])
    xcorr_gz = pearson(anom[:, hq_i], anom[:, gz_i])

    mi_map = np.array([c["mi_hq_bits"] for c in cells], float)
    spell_means = np.array([c["spell_mean"] for c in cells], float)

    methods = [
        {
            "id": "eof",
            "field": "climate dynamics",
            "name": "EOF / PCA of seasonally anomalized daily Tmin",
            "note": "Area-weighted SVD after subtracting each cell’s day-of-year climatology. Not a health factor.",
        },
        {
            "id": "harmonic",
            "field": "geophysics / tides of the year",
            "name": "Annual harmonic amplitude and phase",
            "note": "One annual Fourier pair per cell. Phase is the day of year of the fitted Tmin maximum.",
        },
        {
            "id": "theil_sen",
            "field": "robust climatology",
            "name": "Theil–Sen trend of yearly mean Tmin, with Mann–Kendall S",
            "note": "Eleven years only. A slope is a description of this window, not a detection of climate change for the paper.",
        },
        {
            "id": "kmeans",
            "field": "unsupervised learning",
            "name": "k-means on standardised climatology (k=4)",
            "note": "Features: mean Tmin, hot-night count, harmonic amplitude, distance to coast, elevation. Labels are interpretive.",
        },
        {
            "id": "entropy",
            "field": "information theory",
            "name": "Spatial entropy of hot-night occupancy; MI with the Headquarters cell",
            "note": "Evenness near 1 would mean 28°C nights are spread across the delta. They are not.",
        },
        {
            "id": "spells",
            "field": "extremes",
            "name": "Hot-night spell persistence and P(HN | VHD)",
            "note": "Runs of Tmin ≥ 28°C. Joint occurrence with Tmax ≥ 33°C on the same calendar day.",
        },
        {
            "id": "wasserstein",
            "field": "optimal transport",
            "name": "Wasserstein-1 distance of daily Tmin from the Headquarters cell",
            "note": "A distributional distance, not kilometres and not a hospital catchment.",
        },
        {
            "id": "network",
            "field": "network science",
            "name": f"Anomaly-correlation graph, edge if r > {CORR_EDGE}",
            "note": "Cells whose de-seasoned nights move together. Not a patient-sharing network.",
        },
    ]

    model = {
        "n_cells": n_s,
        "n_days": n_t,
        "eof": {
            "variance_frac": [round(float(v), 4) for v in var[:8]],
            "cumulative_3": round(float(var[:3].sum()), 4),
            "pc1_lag1": round(float(r_lag1), 4),
            "n_eff_bartlett": round(float(n_eff), 1),
            "north_separated_1_2": bool(north_separated(svals, n_eff, 0)),
            "eof1_lat_corr": round(float(eof1_lat), 4),
            "eof1_coast_corr": round(float(eof1_coast), 4),
            "eof1_hn_corr": round(float(eof1_hn), 4),
            "calendar_month_pc1": [round(float(v), 4) for v in cal_pc1],
            "hq_cell": pts[hq_i]["id"],
            "waglan_cell": pts[wag_i]["id"],
            "guangzhou_cell": pts[gz_i]["id"],
            "hq_waglan_anom_r": round(float(xcorr0), 4),
            "hq_guangzhou_anom_r": round(float(xcorr_gz), 4),
            "note": (
                "EOF1 is flipped so marine-south mean loading is non-negative. "
                "A mode is a pattern on this grid, not a finding about hospitalisation."
            ),
        },
        "clusters": {
            "k": K_CLUSTERS,
            "inertia": round(float(inertia), 3),
            "summary": cluster_summary,
        },
        "entropy": {
            **entropy,
            "mean_mi_hq_bits": round(float(mi_map.mean()), 4),
            "max_mi_hq_bits": round(float(mi_map.max()), 4),
        },
        "spells": {
            "mean_run_length": round(float(spell_means.mean()), 3),
            "max_run_length_cell": int(max(c["spell_max"] for c in cells)),
        },
        "network": {
            "r_threshold": CORR_EDGE,
            "n_edges": edges,
            "mean_degree": round(float(degree.mean()), 2),
            "max_degree": int(degree.max()),
        },
        "trend": {
            "median_theil_sen_c_per_decade": round(
                float(np.median([c["theil_sen_c_per_decade"] for c in cells])), 4
            ),
            "n_ci_excludes_zero": int(sum(
                1 for c in cells
                if c["theil_sen_p05"] > 0 or c["theil_sen_p95"] < 0
            )),
            "n_ci_positive": int(sum(1 for c in cells if c["theil_sen_p05"] > 0)),
            "n_ci_negative": int(sum(1 for c in cells if c["theil_sen_p95"] < 0)),
            "note": "Eleven annual means. A slope whose bootstrap interval covers zero is not a detection. Do not paste as a climate-change result.",
        },
        "monthly_pc": monthly_pc,
        "note": (
            "A 0.2° cell is not a city, a weather station, or a hospital catchment. "
            "Do not transport Hong Kong CHD/HF ratios. Live paper stays on HKO Headquarters."
        ),
    }

    features = []
    for row in cells:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [prd.cell_polygon(row["lat"], row["lon"])],
            },
            "properties": {k: v for k, v in row.items() if k != "pc1_recon_by_month"},
        })
    # Keep reconstruction on properties for the month slider.
    for feat, row in zip(features, cells):
        feat["properties"]["pc1_recon_by_month"] = row["pc1_recon_by_month"]

    city_marks = []
    for city in prd.CITIES:
        j = nearest_index(lats, lons, city["lat"], city["lon"], prd)
        src = cells[j]
        city_marks.append({
            **city,
            "nearest_cell": src["id"],
            "eof1": src["eof1"],
            "cluster_name": src["cluster_name"],
            "harmonic_amp": src["harmonic_amp"],
            "theil_sen_c_per_decade": src["theil_sen_c_per_decade"],
            "hn_total": src["hn_total"],
            "mean_tmin": src["mean_tmin"],
            "mi_hq_bits": src["mi_hq_bits"],
        })

    payload = {
        "title": "A field has modes",
        "window": {"start": prd.START, "end": prd.END, "n_years": 11, "n_days": n_t},
        "provenance": (
            "REAL_PUBLIC. Open-Meteo ERA5-Land daily 2 m temperatures on the 0.2° "
            "Pearl River Delta lattice (script 50 cache). Exposure descriptives only. "
            "No health outcomes. No project coefficients."
        ),
        "step_deg": prd.STEP,
        "months": prd.MONTHS,
        "methods": methods,
        "model": model,
        "cells": cells,
        "cities": city_marks,
        "geojson": {"type": "FeatureCollection", "features": features},
        "claim_boundaries": [
            "Do not treat EOF loadings as hospitalisation factors.",
            "Do not treat k-means labels as neighbourhoods or catchments.",
            "Do not paste Theil–Sen slopes as a climate-change finding in the live paper.",
            "Do not overlay CHD/HF or stroke counts on cells.",
            "Do not transport Hong Kong hospitalisation ratios to Shenzhen or Guangzhou.",
            "Live paper stays on HKO official flags.",
        ],
    }

    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    skip = {"pc1_recon_by_month", "harmonic_by_month"}
    write_csv(OUT_TAB / "prd_field_cells.csv", cells, skip)
    (OUT_TAB / "prd_field_model.json").write_text(json.dumps(model, indent=2) + "\n")
    (OUT_TAB / "prd_field.json").write_text(json.dumps(payload, indent=2) + "\n")
    js = "window.PRD_FIELD = " + json.dumps(payload, separators=(",", ":")) + ";\n"
    (OUT_DOCS / "field_embed.js").write_text(js)

    print("EOF var", [round(float(v), 4) for v in var[:5]], "cum3", round(float(var[:3].sum()), 4))
    print("EOF1 corr lat", round(float(eof1_lat), 4), "coast", round(float(eof1_coast), 4), "HN", round(float(eof1_hn), 4))
    print("North 1 vs 2", north_separated(svals, n_eff, 0), "n_eff", round(n_eff, 1), "lag1", round(float(r_lag1), 4))
    print("clusters", cluster_summary)
    print("entropy evenness", entropy["evenness"], "mean MI", round(float(mi_map.mean()), 4))
    print("network edges", edges, "mean degree", round(float(degree.mean()), 2))
    print("median Theil-Sen °C/decade", model["trend"]["median_theil_sen_c_per_decade"])
    print("wrote", OUT_DOCS / "field_embed.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
