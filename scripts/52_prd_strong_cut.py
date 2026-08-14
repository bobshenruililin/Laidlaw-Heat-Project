#!/usr/bin/env python3
"""Second-cut diagnostics on the PRD Tmin field.

Year-holdout EOF stability, moving-block bootstrap of EOF1 variance,
Benjamini–Hochberg on 90 Mann–Kendall tests, circular harmonic phase,
compound-extreme odds ratios, and lagged HQ–Guangzhou cross-correlation.

EXPOSURE ONLY. Reuses scripts/51 loaders and the script 50 cache.
Live paper stays on HKO Headquarters.

Usage:
  python3 scripts/52_prd_strong_cut.py
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "prd_field"
RNG_SEED = 20260814
N_BLOCK_BOOT = 80
BLOCK = 10
Q_FDR = 0.10


def load51():
    spec = importlib.util.spec_from_file_location(
        "field51", ROOT / "scripts" / "51_prd_field_laboratory.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def normal_two_sided_p(z: float) -> float:
    """2 * (1 - Phi(|z|)) via erfc. No scipy."""
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def mann_kendall_p(y: np.ndarray) -> tuple[int, float, float]:
    y = np.asarray(y, float)
    n = len(y)
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = y[j] - y[i]
            if d > 0:
                s += 1
            elif d < 0:
                s -= 1
    var = n * (n - 1) * (2 * n + 5) / 18.0
    if var <= 0:
        return int(s), float("nan"), 1.0
    if s > 0:
        z = (s - 1) / math.sqrt(var)
    elif s < 0:
        z = (s + 1) / math.sqrt(var)
    else:
        z = 0.0
    return int(s), float(z), normal_two_sided_p(z)


def benjamini_hochberg(p: np.ndarray, q: float = Q_FDR) -> np.ndarray:
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    ranked = p[order]
    thresh = q * (np.arange(1, m + 1) / m)
    hit = ranked <= thresh
    keep = np.zeros(m, dtype=bool)
    if hit.any():
        k = int(np.max(np.where(hit)[0]))
        keep[order[: k + 1]] = True
    return keep


def circular_stats(doy: np.ndarray, period: float = 365.25) -> dict:
    theta = 2.0 * math.pi * np.asarray(doy, float) / period
    c = float(np.mean(np.cos(theta)))
    s = float(np.mean(np.sin(theta)))
    r = math.hypot(c, s)
    mean_doy = (math.atan2(s, c) % (2 * math.pi)) * period / (2 * math.pi)
    # Mardia circular SD (radians → days)
    sd_days = math.sqrt(max(0.0, -2.0 * math.log(max(r, 1e-12)))) * period / (2 * math.pi)
    return {
        "mean_doy": round(mean_doy, 2),
        "resultant_length": round(r, 4),
        "sd_days": round(sd_days, 2),
        "n": int(len(doy)),
    }


def odds_ratio(hn: np.ndarray, vhd: np.ndarray) -> dict:
    hn = np.asarray(hn, int) == 1
    vhd = np.asarray(vhd, int) == 1
    n11 = int(np.sum(hn & vhd))
    n10 = int(np.sum(hn & ~vhd))
    n01 = int(np.sum(~hn & vhd))
    n00 = int(np.sum(~hn & ~vhd))
    p_hn = float(hn.mean())
    p_vhd = float(vhd.mean())
    p_both = float((hn & vhd).mean())
    lift = p_both / (p_hn * p_vhd) if p_hn * p_vhd > 0 else float("nan")
    if n10 == 0 or n01 == 0:
        or_ = float("inf") if n11 and n00 else float("nan")
    else:
        or_ = (n11 * n00) / (n10 * n01)
    p_vhd_given_hn = n11 / (n11 + n10) if (n11 + n10) else None
    p_hn_given_vhd = n11 / (n11 + n01) if (n11 + n01) else None
    return {
        "n11": n11, "n10": n10, "n01": n01, "n00": n00,
        "p_hn": round(p_hn, 4),
        "p_vhd": round(p_vhd, 4),
        "p_both": round(p_both, 4),
        "p_vhd_given_hn": None if p_vhd_given_hn is None else round(p_vhd_given_hn, 4),
        "p_hn_given_vhd": None if p_hn_given_vhd is None else round(p_hn_given_vhd, 4),
        "lift_vs_independence": None if math.isnan(lift) else round(lift, 3),
        "odds_ratio": None if (isinstance(or_, float) and math.isnan(or_)) else (
            "inf" if or_ == float("inf") else round(float(or_), 3)
        ),
        "or_unstable_small_n11_or_n10": bool(n11 < 20 or n10 < 20 or n01 < 20),
    }


def xcorr_lags(a: np.ndarray, b: np.ndarray, max_lag: int = 3) -> list[dict]:
    a = (a - a.mean()) / (a.std() or 1.0)
    b = (b - b.mean()) / (b.std() or 1.0)
    out = []
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            r = float(np.mean(a[-lag:] * b[:lag]))
        elif lag > 0:
            r = float(np.mean(a[:-lag] * b[lag:]))
        else:
            r = float(np.mean(a * b))
        out.append({"lag_days": lag, "r": round(r, 4)})
    return out


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def eof1_pattern(anom: np.ndarray, lats: np.ndarray, m51, marine: np.ndarray) -> tuple[np.ndarray, float]:
    eofs, pcs, var, _ = m51.eof_svd(anom, lats)
    eof, _ = m51.flip_to_marine_positive(eofs[0], pcs[:, 0], marine)
    return eof, float(var[0])


def residual_network_edges(anom: np.ndarray, lats: np.ndarray, m51, marine: np.ndarray, r0: float = 0.90) -> dict:
    eofs, pcs, _, _ = m51.eof_svd(anom, lats)
    eof1, pc1 = m51.flip_to_marine_positive(eofs[0], pcs[:, 0], marine)
    centered = anom - anom.mean(axis=0)
    resid = centered - np.outer(pc1, eof1)
    corr = np.corrcoef(resid.T)
    np.fill_diagonal(corr, 0.0)
    n_edges = int(np.sum(np.triu(corr > r0, 1)))
    raw = np.corrcoef(centered.T)
    np.fill_diagonal(raw, 0.0)
    n_raw = int(np.sum(np.triu(raw > r0, 1)))
    return {
        "r_threshold": r0,
        "n_edges_raw": n_raw,
        "n_edges_after_removing_eof1": n_edges,
        "note": "If the r>0.90 graph collapses after removing EOF1, it was the common pulse, not a separate network.",
    }


def year_holdout(tmin: np.ndarray, doy: np.ndarray, years: np.ndarray, lats: np.ndarray, m51, marine: np.ndarray) -> dict:
    anom_full = m51.seasonal_anomaly(tmin, doy)
    full, full_v = eof1_pattern(anom_full, lats, m51, marine)
    years_u = np.array(sorted(set(years.tolist())))
    corrs = []
    fracs = []
    for y in years_u:
        mask = years != y
        anom = m51.seasonal_anomaly(tmin[mask], doy[mask])
        eof, v = eof1_pattern(anom, lats, m51, marine)
        if float(np.dot(eof, full)) < 0:
            eof = -eof
        corrs.append(float(np.corrcoef(eof, full)[0, 1]))
        fracs.append(v)
    return {
        "pattern_r_min": round(min(corrs), 4),
        "pattern_r_median": round(float(np.median(corrs)), 4),
        "pattern_r_max": round(max(corrs), 4),
        "var_frac_min": round(min(fracs), 4),
        "var_frac_median": round(float(np.median(fracs)), 4),
        "var_frac_max": round(max(fracs), 4),
        "by_year": [
            {"year": int(y), "pattern_r": round(c, 4), "var_frac": round(v, 4)}
            for y, c, v in zip(years_u, corrs, fracs)
        ],
    }


def block_bootstrap_var1(anom: np.ndarray, lats: np.ndarray, rng: np.random.Generator,
                         n_boot: int = N_BLOCK_BOOT, block: int = BLOCK) -> dict:
    t = anom.shape[0]
    starts = list(range(0, t, block))
    n_blocks = len(starts)
    fracs = []
    for _ in range(n_boot):
        pick = rng.integers(0, n_blocks, size=n_blocks)
        chunks = [anom[starts[i]: starts[i] + block] for i in pick]
        boot = np.vstack(chunks)[:t]
        _, _, var, _ = m51_eof(boot, lats)
        fracs.append(float(var[0]))
    fracs = np.array(fracs)
    return {
        "n_boot": n_boot,
        "block_days": block,
        "var1_mean": round(float(fracs.mean()), 4),
        "var1_p05": round(float(np.percentile(fracs, 5)), 4),
        "var1_p95": round(float(np.percentile(fracs, 95)), 4),
        "var1_min": round(float(fracs.min()), 4),
        "var1_max": round(float(fracs.max()), 4),
    }


def m51_eof(anom, lats):
    # late-bound; set on main
    return _M51.eof_svd(anom, lats)


_M51 = None


def main() -> int:
    global _M51
    m51 = load51()
    _M51 = m51
    prd = m51.load_prd()
    cube = m51.load_cube(prd)
    pts = cube["pts"]
    tmin, tmax, hn, vhd = cube["tmin"], cube["tmax"], cube["hn"], cube["vhd"]
    lats = cube["lats"]
    years = cube["years"]
    rng = np.random.default_rng(RNG_SEED)
    marine = np.array([prd.region_of(p["lat"], p["lon"]) == "marine south" for p in pts])
    gz = np.array([prd.region_of(p["lat"], p["lon"]) == "Guangzhou" for p in pts])
    anom = m51.seasonal_anomaly(tmin, cube["doy"])
    tmax_anom = m51.seasonal_anomaly(tmax, cube["doy"])

    eofs, pcs, var, _ = m51.eof_svd(anom, lats)
    eof1, _ = m51.flip_to_marine_positive(eofs[0], pcs[:, 0], marine)

    net = residual_network_edges(anom, lats, m51, marine)
    hold = year_holdout(tmin, cube["doy"], years, lats, m51, marine)
    boot = block_bootstrap_var1(anom, lats, rng)

    years_u = np.array(sorted(set(years.tolist())))
    yearly = np.stack([tmin[years == y].mean(axis=0) for y in years_u], axis=0)
    pvals = np.empty(yearly.shape[1])
    zs = np.empty(yearly.shape[1])
    for j in range(yearly.shape[1]):
        _, z, p = mann_kendall_p(yearly[:, j])
        pvals[j] = p
        zs[j] = z
    fdr = benjamini_hochberg(pvals, Q_FDR)
    ci_excl = []
    # reuse script 51 cell file if present for CI comparison
    cells_path = OUT / "prd_field.json"
    n_ci = None
    if cells_path.exists():
        payload = json.loads(cells_path.read_text())
        n_ci = payload["model"]["trend"]["n_ci_excludes_zero"]

    # harmonic phases from existing cells or recompute
    doys = []
    marine_doy = []
    inland_doy = []
    t_index = cube["t_index"]
    for j, pt in enumerate(pts):
        _, t_peak, _ = m51.harmonic_amp_phase(tmin[:, j], t_index)
        doys.append(t_peak)
        region = prd.region_of(pt["lat"], pt["lon"])
        if region == "marine south":
            marine_doy.append(t_peak)
        if region == "Guangzhou":
            inland_doy.append(t_peak)
    circ_all = circular_stats(np.array(doys))
    circ_marine = circular_stats(np.array(marine_doy))
    circ_gz = circular_stats(np.array(inland_doy))
    phase_diff = abs(circ_marine["mean_doy"] - circ_gz["mean_doy"])
    phase_diff = min(phase_diff, 365.25 - phase_diff)

    hq_i = m51.nearest_index(lats, cube["lons"], 22.3022, 114.1742, prd)
    gz_i = m51.nearest_index(lats, cube["lons"], 23.1291, 113.2644, prd)
    wag_i = m51.nearest_index(lats, cube["lons"], 22.1820, 114.3033, prd)
    lags = xcorr_lags(anom[:, hq_i], anom[:, gz_i], 3)
    peak_lag = max(lags, key=lambda d: abs(d["r"]))

    def pool(mask):
        return odds_ratio(hn[:, mask].ravel(), vhd[:, mask].ravel())

    compound = {
        "marine_south": pool(marine),
        "guangzhou": pool(gz),
        "hq_cell": odds_ratio(hn[:, hq_i], vhd[:, hq_i]),
        "grid": odds_ratio(hn.ravel(), vhd.ravel()),
    }
    rho_s = {
        "marine_tmin_tmax_anom": round(spearman(anom[:, marine].ravel(), tmax_anom[:, marine].ravel()), 4),
        "guangzhou_tmin_tmax_anom": round(spearman(anom[:, gz].ravel(), tmax_anom[:, gz].ravel()), 4),
        "hq_tmin_tmax_anom": round(spearman(anom[:, hq_i], tmax_anom[:, hq_i]), 4),
    }

    model = {
        "provenance": "REAL_PUBLIC. Same Open-Meteo ERA5-Land 0.2° cache as script 51. Exposure only.",
        "eof_year_holdout": hold,
        "eof_block_bootstrap": boot,
        "full_sample_eof1_var": round(float(var[0]), 4),
        "mann_kendall_fdr": {
            "q": Q_FDR,
            "n_cells": int(len(pvals)),
            "n_raw_p_lt_0_10": int(np.sum(pvals < 0.10)),
            "n_fdr_q_0_10": int(fdr.sum()),
            "min_p": round(float(np.min(pvals)), 4),
            "n_fdr_positive_z": int(np.sum(fdr & (zs > 0))),
            "n_fdr_negative_z": int(np.sum(fdr & (zs < 0))),
            "script51_n_ci_excludes_zero": n_ci,
            "note": (
                "BH on two-sided Mann–Kendall normal p-values, n=11 years. "
                "Ignores spatial dependence, so surviving cells are still an upper bound on detections. "
                "Not a climate-change result."
            ),
        },
        "circular_phase": {
            "all": circ_all,
            "marine_south": circ_marine,
            "guangzhou": circ_gz,
            "marine_minus_guangzhou_days": round(phase_diff, 2),
            "note": "Day of fitted Tmin maximum. The year turns together.",
        },
        "compound_extremes": compound,
        "spearman_tmin_tmax_anomaly": rho_s,
        "hq_guangzhou_xcorr": {
            "lags": lags,
            "peak": peak_lag,
            "note": "De-seasoned Tmin. Positive lag means Guangzhou follows Headquarters.",
        },
        "network_after_eof1": net,
        "claim_boundaries": [
            "Do not paste FDR counts as climate-change detections.",
            "Do not treat lagged r as a hospitalisation lag.",
            "Live paper stays on HKO Headquarters.",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "prd_strong_cut.json"
    path.write_text(json.dumps(model, indent=2) + "\n")
    print("EOF1 full", round(float(var[0]), 4))
    print("holdout r", hold["pattern_r_min"], hold["pattern_r_median"], hold["pattern_r_max"])
    print("holdout var", hold["var_frac_min"], hold["var_frac_median"], hold["var_frac_max"])
    print("block boot var1", boot)
    print("FDR", model["mann_kendall_fdr"]["n_fdr_q_0_10"], "raw p<0.10", model["mann_kendall_fdr"]["n_raw_p_lt_0_10"])
    print("phase", circ_all, "diff", phase_diff)
    print("compound marine", compound["marine_south"]["odds_ratio"], "gz", compound["guangzhou"]["odds_ratio"])
    print("xcorr peak", peak_lag)
    print("network after eof1", net)
    js = "window.PRD_STRONG_CUT = " + json.dumps(model, separators=(",", ":")) + ";\n"
    docs = ROOT / "docs" / "field"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "strong_cut_embed.js").write_text(js)
    print("wrote", path)
    print("wrote", docs / "strong_cut_embed.js")
    return 0


if __name__ == "__main__":
    sys.exit(main())
