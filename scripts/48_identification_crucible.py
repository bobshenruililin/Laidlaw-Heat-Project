#!/usr/bin/env python3
"""First-principles identification diagnostics for the CHD/HF monthly panel.

Provenance: REAL HKO monthly climate (2013-01..2023-12) plus already-paid
HA_APPROVED_AGGREGATE coefficients from outputs/release_chd_hf/.
No governed outcome counts are read. No new health model is fit.

This script asks a linear-algebra question, not a literature question:
after calendar-month indicators and a 4-df natural spline in time, how much
independent variation remains in each thermal exposure, and what effect
sizes are therefore even in principle detectable at n=132?
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
TABLE2 = ROOT / "outputs" / "release_chd_hf" / "tables" / "table2_core_models.csv"
TABLE4 = ROOT / "outputs" / "release_chd_hf" / "tables" / "table4_uncertainty_ladder.csv"
OUT_DIR = ROOT / "outputs" / "identification_crucible"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def as_float(x: str) -> float:
    return float(x)


def ns_basis(t: np.ndarray, df: int = 4) -> np.ndarray:
    """Natural cubic spline basis with df columns, knots at interior quantiles.

    Truncated-power construction with linear-tail constraints, matching the
    usual ns(time, df) shape enough for an identification R^2, not for
    reproducing MASS::glm.nb coefficients.
    """
    t = np.asarray(t, dtype=float)
    n = t.size
    # df natural-spline columns: intercept is handled separately, so we want
    # df = (degree 1 linear) + (K-2 free knots) with K interior+boundary knots.
    # For df=4: linear term + 3 constrained truncated powers = 4 columns
    # without intercept. Use K = df interior quantile knots plus boundaries.
    qs = np.linspace(0, 1, df + 1)
    knots = np.quantile(t, qs)
    knots = np.unique(knots)
    if knots.size < 3:
        # degenerate: return orthonormal polynomials
        x = (t - t.mean()) / (t.std() or 1.0)
        return np.column_stack([x, x**2, x**3, x**4])[:, :df]

    k0, kL = knots[0], knots[-1]
    interiors = knots[1:-1]
    def tp(x, k):
        return np.maximum(x - float(k), 0.0) ** 3

    if interiors.size == 0:
        x = (t - t.mean()) / (t.std() or 1.0)
        return np.column_stack([x ** i for i in range(1, df + 1)])

    k_penult = interiors[-1] if interiors.size else k0
    # Use all interior knots except last as free; last two boundary knots
    # impose natural constraints.
    free = interiors[:-1] if interiors.size > 1 else interiors
    cols = [(t - t.mean()) / (t.std() or 1.0)]
    denom = kL - k_penult
    if denom == 0:
        denom = 1.0
    for kj in free:
        d_j = tp(t, kj)
        d_k = tp(t, k_penult)
        d_L = tp(t, kL)
        col = d_j - d_k * (kL - kj) / denom - d_L * (k_penult - kj) / denom
        cols.append(col)
    basis = np.column_stack(cols)
    # pad/truncate to df
    if basis.shape[1] < df:
        x = (t - t.mean()) / (t.std() or 1.0)
        extra = []
        p = 2
        while basis.shape[1] + len(extra) < df:
            extra.append(x**p)
            p += 1
        basis = np.column_stack([basis] + extra)
    return basis[:, :df]


def month_dummies(months: np.ndarray) -> np.ndarray:
    """11 dummies, January as reference."""
    cols = []
    for m in range(2, 13):
        cols.append((months == m).astype(float))
    return np.column_stack(cols)


def add_intercept(X: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(X.shape[0]), X])


def ols_fit(X: np.ndarray, y: np.ndarray) -> dict:
    """OLS with intercept already in X. Returns R2, residual SD, rank, coef."""
    n, p = X.shape
    xtx = X.T @ X
    # ridge a tiny bit for numerical rank
    try:
        beta = np.linalg.solve(xtx, X.T @ y)
        rank = int(np.linalg.matrix_rank(xtx, tol=1e-8))
    except np.linalg.LinAlgError:
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rank = int(np.linalg.matrix_rank(X, tol=1e-8))
    fitted = X @ beta
    resid = y - fitted
    sst = np.sum((y - y.mean()) ** 2)
    sse = np.sum(resid**2)
    r2 = 1.0 - sse / sst if sst > 0 else 1.0
    df_res = max(n - rank, 1)
    sigma = math.sqrt(sse / df_res)
    return {
        "n": n,
        "p": p,
        "rank": rank,
        "r2": float(r2),
        "sse": float(sse),
        "sst": float(sst),
        "residual_sd": float(np.std(resid, ddof=1)),
        "residual_sd_mle": float(np.std(resid, ddof=0)),
        "sigma_ols": float(sigma),
        "y_sd": float(np.std(y, ddof=1)),
        "y_mean": float(np.mean(y)),
        "df_residual": int(df_res),
    }


def bh_q(p: list[float]) -> list[float]:
    m = len(p)
    order = np.argsort(p)
    q = [0.0] * m
    prev = 1.0
    for rank_from_end, idx in enumerate(order[::-1]):
        r = m - rank_from_end  # 1-based rank of this p in ascending order
        val = min(prev, p[idx] * m / r)
        q[idx] = val
        prev = val
    return q


def main() -> None:
    rows = read_csv(CLIMATE)
    assert len(rows) == 132, f"expected 132 months, got {len(rows)}"
    month = np.array([int(r["month"]) for r in rows], dtype=int)
    year = np.array([int(r["year"]) for r in rows], dtype=int)
    t_index = np.arange(len(rows), dtype=float)
    exposures = {
        "mean_temp": np.array([as_float(r["mean_temp"]) for r in rows]),
        "mean_tmax": np.array([as_float(r["mean_tmax"]) for r in rows]),
        "mean_tmin": np.array([as_float(r["mean_tmin"]) for r in rows]),
        "hot_nights": np.array([as_float(r["hot_nights"]) for r in rows]),
        "cold_days": np.array([as_float(r["cold_days"]) for r in rows]),
        "very_hot_days": np.array([as_float(r["very_hot_days"]) for r in rows]),
    }

    M = month_dummies(month)
    S = ns_basis(t_index, df=4)
    X_month = add_intercept(M)
    X_full = add_intercept(np.column_stack([M, S]))
    X_trend = add_intercept(S)
    X_null = add_intercept(np.zeros((len(rows), 0))) if False else np.ones((len(rows), 1))

    ident_rows = []
    residual_series = {}
    for name, y in exposures.items():
        r_null = ols_fit(X_null, y)
        r_month = ols_fit(X_month, y)
        r_trend = ols_fit(X_trend, y)
        r_full = ols_fit(X_full, y)
        # remaining variation share
        ident_rows.append(
            {
                "exposure": name,
                "n": 132,
                "y_mean": r_null["y_mean"],
                "y_sd": r_null["y_sd"],
                "r2_month_fe": r_month["r2"],
                "r2_ns4_only": r_trend["r2"],
                "r2_month_plus_ns4": r_full["r2"],
                "residual_sd_after_month": r_month["residual_sd"],
                "residual_sd_after_month_ns4": r_full["residual_sd"],
                "variation_share_remaining_after_full_controls": (
                    1.0 - r_full["r2"]
                ),
                "df_residual_full": r_full["df_residual"],
                "rank_full": r_full["rank"],
                "nonzero_months": int(np.sum(y > 0)),
                "zero_months": int(np.sum(y == 0)),
                "max": float(np.max(y)),
                "min": float(np.min(y)),
                "data_status": "REAL",
            }
        )
        # store residuals after full controls
        beta = np.linalg.lstsq(X_full, y, rcond=None)[0]
        residual_series[name] = y - X_full @ beta

    # Calendar-month support (identification geography)
    support_rows = []
    for m in range(1, 13):
        mask = month == m
        support_rows.append(
            {
                "calendar_month": m,
                "n": int(mask.sum()),
                "cold_days_total": float(exposures["cold_days"][mask].sum()),
                "hot_nights_total": float(exposures["hot_nights"][mask].sum()),
                "very_hot_days_total": float(exposures["very_hot_days"][mask].sum()),
                "cold_days_mean": float(exposures["cold_days"][mask].mean()),
                "hot_nights_mean": float(exposures["hot_nights"][mask].mean()),
                "very_hot_days_mean": float(exposures["very_hot_days"][mask].mean()),
                "cold_days_sd": float(exposures["cold_days"][mask].std(ddof=1)),
                "hot_nights_sd": float(exposures["hot_nights"][mask].std(ddof=1)),
                "july_like_hot_nights_min": float(exposures["hot_nights"][mask].min()),
                "july_like_hot_nights_max": float(exposures["hot_nights"][mask].max()),
                "data_status": "REAL",
            }
        )

    cold_total = exposures["cold_days"].sum()
    hot_total = exposures["hot_nights"].sum()
    vhd_total = exposures["very_hot_days"].sum()
    djf = np.isin(month, [12, 1, 2])
    jja = np.isin(month, [6, 7, 8])
    geography = {
        "cold_days_total": float(cold_total),
        "cold_days_djf_share": float(exposures["cold_days"][djf].sum() / cold_total),
        "cold_days_nonzero_months": int(np.sum(exposures["cold_days"] > 0)),
        "hot_nights_total": float(hot_total),
        "hot_nights_jja_share": float(exposures["hot_nights"][jja].sum() / hot_total),
        "hot_nights_nonzero_months": int(np.sum(exposures["hot_nights"] > 0)),
        "very_hot_days_total": float(vhd_total),
        "very_hot_days_jja_share": float(exposures["very_hot_days"][jja].sum() / vhd_total),
        "july_hot_nights_min": float(exposures["hot_nights"][month == 7].min()),
        "july_hot_nights_max": float(exposures["hot_nights"][month == 7].max()),
        "july_hot_nights_mean": float(exposures["hot_nights"][month == 7].mean()),
        "january_cold_days_min": float(exposures["cold_days"][month == 1].min()),
        "january_cold_days_max": float(exposures["cold_days"][month == 1].max()),
        "january_cold_days_mean": float(exposures["cold_days"][month == 1].mean()),
        "data_status": "REAL",
    }

    # Residual correlation of exposures after month+ns4 (identifying collinearity)
    names = list(exposures)
    R = np.column_stack([residual_series[n] for n in names])
    corr = np.corrcoef(R, rowvar=False)
    corr_rows = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            corr_rows.append(
                {
                    "exposure_1": a,
                    "exposure_2": b,
                    "residual_corr_after_month_ns4": float(corr[i, j]),
                    "data_status": "REAL",
                }
            )

    # Paid-table BH reconstruction and detectability
    t2 = read_csv(TABLE2)
    pvals = [as_float(r["p_value"]) for r in t2]
    q_recomputed = bh_q(pvals)
    m = len(pvals)
    # For q<=0.05, smallest p must satisfy p <= 0.05 * 1 / m if it is rank 1
    p_needed_rank1_q05 = 0.05 * 1 / m
    p_needed_rank2_q05 = 0.05 * 2 / m
    min_p = min(pvals)
    detectability = []
    # Approximate Wald: for a 5-day scaled count exposure, remaining SD after
    # controls is residual_sd/5 in the scaled units of the coefficient.
    # Using reported NW6 SEs from table2 as the actual information, invert
    # detectable |log RR| at 80% power two-sided alpha=0.05 ≈ 2.8 * SE
    for r in t2:
        se_from_ci = (math.log(as_float(r["rr_high"])) - math.log(as_float(r["rr_low"]))) / (
            2 * 1.959964
        )
        log_rr = math.log(as_float(r["rr"]))
        detectability.append(
            {
                "outcome": r["outcome"],
                "pathway_id": r["pathway_id"],
                "exposure": r["exposure"],
                "rr": as_float(r["rr"]),
                "p_value": as_float(r["p_value"]),
                "q_value_release": as_float(r["q_value_core_bh"]),
                "q_value_recomputed": q_recomputed[t2.index(r)],
                "approx_se_from_nw6_ci": se_from_ci,
                "abs_log_rr": abs(log_rr),
                "detectable_abs_log_rr_80pct_alpha05": 2.8 * se_from_ci,
                "detectable_rr_up_80pct": math.exp(2.8 * se_from_ci),
                "detectable_rr_down_80pct": math.exp(-2.8 * se_from_ci),
                "observed_over_detectable": abs(log_rr) / (2.8 * se_from_ci)
                if se_from_ci > 0
                else None,
                "data_status": "HA_APPROVED_AGGREGATE",
            }
        )

    # SE-method discordance: does CI exclude 1?
    t4 = read_csv(TABLE4)
    discordance = []
    grouped: dict[tuple[str, str], list] = {}
    for r in t4:
        key = (r["outcome"], r["pathway_id"])
        grouped.setdefault(key, []).append(r)
    for (outcome, pid), items in grouped.items():
        excludes = {}
        for r in items:
            lo, hi = as_float(r["rr_low"]), as_float(r["rr_high"])
            excludes[r["se_method"]] = not (lo <= 1.0 <= hi)
        discordance.append(
            {
                "outcome": outcome,
                "pathway_id": pid,
                "model_excludes_1": excludes.get("model"),
                "hc1_excludes_1": excludes.get("HC1"),
                "nw3_excludes_1": excludes.get("NeweyWest_lag3"),
                "nw6_excludes_1": excludes.get("NeweyWest_lag6"),
                "n_methods_excluding_1": int(sum(1 for v in excludes.values() if v)),
                "se_concordant_exclude_1": int(sum(1 for v in excludes.values() if v)) == 4,
                "data_status": "HA_APPROVED_AGGREGATE",
            }
        )

    summary = {
        "problem": "What claims are logically licensed by a 132-month first-event count panel after calendar-month FE + ns(time,4)?",
        "n_months": 132,
        "control_rank_full": ident_rows[0]["rank_full"],
        "df_residual_full": ident_rows[0]["df_residual_full"],
        "bh_tests": m,
        "min_p": min_p,
        "p_needed_rank1_for_q05": p_needed_rank1_q05,
        "p_needed_rank2_for_q05": p_needed_rank2_q05,
        "min_p_over_rank1_threshold": min_p / p_needed_rank1_q05,
        "all_q_gt_019": all(as_float(r["q_value_core_bh"]) > 0.19 for r in t2),
        "geography": geography,
        "provenance": {
            "climate": "REAL",
            "coefficients": "HA_APPROVED_AGGREGATE",
            "new_health_models": False,
            "governed_counts_read": False,
        },
    }

    def write_csv(path: Path, rows_out: list[dict]) -> None:
        if not rows_out:
            return
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
            w.writeheader()
            w.writerows(rows_out)

    write_csv(OUT_DIR / "exposure_residual_variation.csv", ident_rows)
    write_csv(OUT_DIR / "calendar_month_support.csv", support_rows)
    write_csv(OUT_DIR / "residual_exposure_correlations.csv", corr_rows)
    write_csv(OUT_DIR / "bh_detectability.csv", detectability)
    write_csv(OUT_DIR / "se_method_discordance.csv", discordance)
    with (OUT_DIR / "identification_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print("\nExposure residual variation:")
    for r in ident_rows:
        print(
            f"  {r['exposure']:16s}  R2(month)={r['r2_month_fe']:.3f}  "
            f"R2(full)={r['r2_month_plus_ns4']:.3f}  "
            f"remain_sd={r['residual_sd_after_month_ns4']:.3f}  "
            f"nonzero={r['nonzero_months']}/132"
        )


if __name__ == "__main__":
    main()
