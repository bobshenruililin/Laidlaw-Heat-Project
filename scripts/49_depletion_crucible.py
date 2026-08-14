#!/usr/bin/env python3
"""Depletion diagnostics for the CHD/HF monthly first-event panel.

Provenance: REAL HKO monthly climate (2013-01..2023-12), HA_APPROVED_AGGREGATE
annual first-event totals from outputs/tables/cvd_descriptive_annual_totals.csv,
and already-paid HA_APPROVED_AGGREGATE scenario coefficients from
outputs/tables/cvd_trend_depletion_sensitivity.csv. No governed monthly counts
are read. No health model is fit. No new health coefficient is produced.

The question is not "is there an association". It is: what does an absorbing
first-event risk set do to a log-link count model that offsets days-in-month
instead of still-at-risk person-time?

Three quantities are computed, all from the design matrix:

1. Count-weighted information share. Fisher information for the exposure slope
   in a log-link count model is sum_t Q_t * xtilde_t^2 with Q_t increasing in the
   fitted mean, and the fitted mean is proportional to the risk set. Using the
   approved annual totals as a risk-set-scale proxy, this measures whether an
   exposure's identifying variance sits in fat-risk-set months or depleted ones.

2. Additive omitted-log-risk-set bias. Under the accounting identity
   log E[Y_t] = log R_t + log alpha_t + log D_t + controls + beta * x_t, omitting
   log R_t biases beta-hat by Cov(xtilde, gtilde)/Var(xtilde). The depletion path
   is ILLUSTRATIVE_ALGEBRA: a family of monotone shapes normalised to the
   constant-hazard reading of the observed halving. Level cancels; only shape
   enters.

3. Interaction absorption. ns(time,4) spans functions of t. It does not span
   functions of t interacted with x_t. This is measured by projecting the
   product of a depletion path and an exposure onto the control space.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
ANNUAL = ROOT / "outputs" / "tables" / "cvd_descriptive_annual_totals.csv"
SCENARIOS = ROOT / "outputs" / "tables" / "cvd_trend_depletion_sensitivity.csv"
OUT_DIR = ROOT / "outputs" / "depletion_crucible"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXPOSURES = (
    "mean_temp",
    "mean_tmax",
    "mean_tmin",
    "hot_nights",
    "cold_days",
    "very_hot_days",
)
# Reporting scale of the paid model: continuous temperature per 1 degree,
# extreme-day counts per 5 days.
SCALE = {
    "mean_temp": 1.0,
    "mean_tmax": 1.0,
    "mean_tmin": 1.0,
    "hot_nights": 5.0,
    "cold_days": 5.0,
    "very_hot_days": 5.0,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def ns_basis(t: np.ndarray, df: int = 4) -> np.ndarray:
    """Same truncated-power natural-spline construction as script 48.

    Shape-faithful for an identification R^2; not a MASS::ns clone.
    """
    t = np.asarray(t, dtype=float)
    qs = np.linspace(0, 1, df + 1)
    knots = np.unique(np.quantile(t, qs))
    if knots.size < 3:
        x = (t - t.mean()) / (t.std() or 1.0)
        return np.column_stack([x**i for i in range(1, df + 1)])[:, :df]
    k0, kL = knots[0], knots[-1]
    interiors = knots[1:-1]

    def tp(x, k):
        return np.maximum(x - float(k), 0.0) ** 3

    if interiors.size == 0:
        x = (t - t.mean()) / (t.std() or 1.0)
        return np.column_stack([x**i for i in range(1, df + 1)])[:, :df]
    k_penult = interiors[-1]
    free = interiors[:-1] if interiors.size > 1 else interiors
    cols = [(t - t.mean()) / (t.std() or 1.0)]
    denom = (kL - k_penult) or 1.0
    for kj in free:
        col = (
            tp(t, kj)
            - tp(t, k_penult) * (kL - kj) / denom
            - tp(t, kL) * (k_penult - kj) / denom
        )
        cols.append(col)
    basis = np.column_stack(cols)
    if basis.shape[1] < df:
        x = (t - t.mean()) / (t.std() or 1.0)
        extra, p = [], 2
        while basis.shape[1] + len(extra) < df:
            extra.append(x**p)
            p += 1
        basis = np.column_stack([basis] + extra)
    return basis[:, :df]


def month_dummies(months: np.ndarray) -> np.ndarray:
    return np.column_stack([(months == m).astype(float) for m in range(2, 13)])


def resid_and_r2(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    sst = float(np.sum((y - y.mean()) ** 2))
    sse = float(np.sum(resid**2))
    r2 = 1.0 - sse / sst if sst > 0 else 1.0
    return resid, r2


def wresid(X: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Weighted-projection residual, the object the score equation uses."""
    sw = np.sqrt(w)
    beta = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0]
    return y - X @ beta


def spearman(a: list[float], b: list[float]) -> float:
    def rank(v):
        order = np.argsort(np.asarray(v, dtype=float))
        r = np.empty(len(v), dtype=float)
        r[order] = np.arange(1, len(v) + 1, dtype=float)
        return r

    ra, rb = rank(a), rank(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def depletion_paths(
    t_index: np.ndarray, monthly_events: np.ndarray, total_log_decline: float
) -> dict[str, np.ndarray]:
    """Monotone log-risk-set shapes, each normalised to the same total decline.

    ILLUSTRATIVE_ALGEBRA. These are not estimates of the T2D/HTN risk set. No
    cohort size, HA row count, or inflow rate is asserted. Only the shape of
    log R_t enters the bias algebra; any multiplicative level cancels in the
    residual projection, so the normalising constant is a scale device.
    """
    n = t_index.size
    u = t_index / (n - 1)
    paths: dict[str, np.ndarray] = {}

    # (a) linear in calendar time
    paths["linear"] = -total_log_decline * u

    # (b) geometric decay, front-loaded like a first-event pool
    k = 3.0
    shape = (1.0 - np.exp(-k * u)) / (1.0 - math.exp(-k))
    paths["front_loaded"] = -total_log_decline * shape

    # (c) closed-pool accounting: R_t = R_0 - cumulative events, with R_0 fixed
    #     only so that the total log decline matches the same normalisation.
    cum = np.cumsum(monthly_events)
    cum_shift = np.concatenate([[0.0], cum[:-1]])
    target = math.exp(-total_log_decline)
    r0 = cum_shift[-1] / (1.0 - target) if target < 1 else cum_shift[-1] * 2.0
    paths["closed_pool"] = np.log(np.maximum(r0 - cum_shift, 1.0)) - math.log(r0)

    # (d) smooth depletion plus non-smooth care-seeking dips in 2020 and 2022
    covid_1 = (t_index >= 85) & (t_index <= 88)  # 2020-02..2020-05
    covid_5 = (t_index >= 109) & (t_index <= 112)  # 2022-02..2022-05
    dip = np.zeros(n)
    dip[covid_1] = -0.12
    dip[covid_5] = -0.18
    paths["front_loaded_plus_covid_kink"] = paths["front_loaded"] + dip

    # (e) unit-amplitude kink alone. Bias is linear in amplitude, so the row for
    #     this path is the transfer coefficient per 0.10 log-unit of dip.
    unit = np.zeros(n)
    unit[covid_1] = -0.10
    unit[covid_5] = -0.10
    paths["covid_kink_0p10_only"] = unit

    return paths


def main() -> None:
    rows = read_csv(CLIMATE)
    assert len(rows) == 132, f"expected 132 months, got {len(rows)}"
    month = np.array([int(r["month"]) for r in rows], dtype=int)
    year = np.array([int(r["year"]) for r in rows], dtype=int)
    t_index = np.arange(len(rows), dtype=float)
    days = np.array([float(r["expected_days"]) for r in rows])
    exposures = {k: np.array([float(r[k]) for r in rows]) for k in EXPOSURES}

    M = month_dummies(month)
    S = ns_basis(t_index, df=4)
    C = np.column_stack([np.ones(len(rows)), M, S])

    # Approved annual totals -> a monthly risk-set-scale proxy. Deliberately
    # seasonality-free: calendar-month effects are already in the control space,
    # so only the secular level is used as the weight.
    annual = read_csv(ANNUAL)
    totals: dict[str, dict[int, float]] = {"chd": {}, "hf": {}}
    for r in annual:
        totals[r["outcome"]][int(r["year"])] = float(r["total_events"])
    mu_proxy = {
        o: np.array([totals[o][int(y)] / 12.0 for y in year]) for o in ("chd", "hf")
    }

    # ------------------------------------------------------------------ 1
    # Count-weighted information share: where does identifying variance live,
    # and how much Fisher weight sits there?
    weight_rows = []
    early = year <= 2018
    pre_covid = year <= 2019
    for name, x in exposures.items():
        x_un, _ = resid_and_r2(C, x)
        var_un = float(np.sum(x_un**2))
        share_early_var = float(np.sum(x_un[early] ** 2) / var_un)
        share_early_raw = float(x[early].sum() / x.sum()) if x.sum() > 0 else float("nan")
        for outcome, mu in mu_proxy.items():
            x_w = wresid(C, x, mu)
            info_w = float(np.sum(mu * x_w**2))
            info_flat = float(np.mean(mu) * np.sum(x_un**2))
            share_early_info = float(
                np.sum(mu[early] * x_w[early] ** 2) / info_w
            )
            weight_rows.append(
                {
                    "outcome": outcome,
                    "exposure": name,
                    "raw_share_2013_2018": share_early_raw,
                    "residual_var_share_2013_2018": share_early_var,
                    "count_weighted_info_share_2013_2018": share_early_info,
                    "count_weight_ratio_vs_flat": info_w / info_flat,
                    "mu_proxy_ratio_first_to_last_year": float(
                        totals[outcome][2013] / totals[outcome][2023]
                    ),
                    "residual_var_share_pre_covid": float(
                        np.sum(x_un[pre_covid] ** 2) / var_un
                    ),
                    "provenance": "REAL climate x HA_APPROVED_AGGREGATE annual totals",
                }
            )

    # ------------------------------------------------------------------ 2
    # Additive omitted-log-risk-set bias.
    total_log_decline = -math.log(
        (totals["chd"][2023] + totals["hf"][2023])
        / (totals["chd"][2013] + totals["hf"][2013])
    )
    monthly_events = np.array(
        [(totals["chd"][int(y)] + totals["hf"][int(y)]) / 12.0 for y in year]
    )
    paths = depletion_paths(t_index, monthly_events, total_log_decline)

    bias_rows = []
    path_rows = []
    for pname, g in paths.items():
        g_res, g_r2 = resid_and_r2(C, g)
        _, g_r2_month = resid_and_r2(np.column_stack([np.ones(len(rows)), M]), g)
        path_rows.append(
            {
                "path": pname,
                "total_log_decline_normalisation": total_log_decline,
                "r2_absorbed_by_month_fe": g_r2_month,
                "r2_absorbed_by_month_plus_ns4": g_r2,
                "share_surviving_controls": 1.0 - g_r2,
                "residual_sd_after_controls": float(np.std(g_res, ddof=1)),
                "provenance": "ILLUSTRATIVE_ALGEBRA",
            }
        )
        for name, x in exposures.items():
            x_res, _ = resid_and_r2(C, x)
            b = float(np.sum(x_res * g_res) / np.sum(x_res**2))
            step = SCALE[name]
            bias_rows.append(
                {
                    "path": pname,
                    "exposure": name,
                    "reporting_step": step,
                    "bias_per_unit_exposure": b,
                    "bias_per_reporting_step": b * step,
                    "rr_multiplier_per_reporting_step": math.exp(b * step),
                    "residual_corr_exposure_vs_path": float(
                        np.corrcoef(x_res, g_res)[0, 1]
                    ),
                    "provenance": "REAL climate x ILLUSTRATIVE_ALGEBRA path",
                }
            )

    # ------------------------------------------------------------------ 3
    # Interaction absorption: can the control space represent path x exposure?
    inter_rows = []
    for pname, g in paths.items():
        g_res, _ = resid_and_r2(C, g)
        for name, x in exposures.items():
            prod = g * x
            _, r2_prod = resid_and_r2(C, prod)
            # also the centred version, which is what a varying slope contributes
            x_res, _ = resid_and_r2(C, x)
            prod_c = g_res * x_res
            _, r2_prod_c = resid_and_r2(C, prod_c)
            inter_rows.append(
                {
                    "path": pname,
                    "exposure": name,
                    "r2_of_path_times_exposure_on_controls": r2_prod,
                    "share_of_interaction_surviving_controls": 1.0 - r2_prod,
                    "r2_of_residualised_product_on_controls": r2_prod_c,
                    "share_of_residualised_product_surviving": 1.0 - r2_prod_c,
                    "provenance": "REAL climate x ILLUSTRATIVE_ALGEBRA path",
                }
            )

    # ------------------------------------------------------------------ 4
    # Risk-set fatness ladder over already-paid scenario coefficients.
    scen = read_csv(SCENARIOS)
    windows = {
        "baseline_ns4": (2013, 2023),
        "drop_first_12_months": (2014, 2023),
        "drop_first_24_months": (2015, 2023),
        "pre_covid": (2013, 2019),
    }
    ladder_rows = []
    for r in scen:
        w = windows.get(r["scenario"])
        if w is None:
            continue
        y0, y1 = w
        yrs = [y for y in range(y0, y1 + 1)]
        n_months = 12 * len(yrs)
        mean_monthly = sum(totals[r["outcome"]][y] for y in yrs) / n_months
        ladder_rows.append(
            {
                "outcome": r["outcome"],
                "pathway_id": r["pathway_id"],
                "exposure": r["exposure"],
                "scenario": r["scenario"],
                "window": f"{y0}-{y1}",
                "n_months": int(r["n_months"]),
                "mean_monthly_events_in_window": mean_monthly,
                "rr": float(r["rr"]),
                "rr_low": float(r["rr_low"]),
                "rr_high": float(r["rr_high"]),
                "log_rr": math.log(float(r["rr"])),
                "p_value_nw6": float(r["p_value_nw6"]),
                "provenance": "HA_APPROVED_AGGREGATE",
            }
        )

    # All twelve core contrasts, not a chosen subset.
    ladder_stats = []
    seen = []
    for r in ladder_rows:
        key = (r["outcome"], r["pathway_id"])
        if key not in seen:
            seen.append(key)
    for outcome, pid in seen:
        sub = [r for r in ladder_rows if r["outcome"] == outcome and r["pathway_id"] == pid]
        if len(sub) < 3:
            continue
        fat = [r["mean_monthly_events_in_window"] for r in sub]
        lrr = [r["log_rr"] for r in sub]
        alrr = [abs(v) for v in lrr]
        ladder_stats.append(
            {
                "outcome": outcome,
                "pathway_id": pid,
                "exposure": sub[0]["exposure"],
                "n_windows": len(sub),
                "spearman_fatness_vs_log_rr": spearman(fat, lrr),
                "spearman_fatness_vs_abs_log_rr": spearman(fat, alrr),
                "min_rr": min(r["rr"] for r in sub),
                "max_rr": max(r["rr"] for r in sub),
                "rr_range_width": max(r["rr"] for r in sub) - min(r["rr"] for r in sub),
                "provenance": "HA_APPROVED_AGGREGATE",
            }
        )

    # ------------------------------------------------------------------ 5
    # Invert the paid covid_phase_adjusted scenario through the transfer
    # coefficient. This asks what non-smooth care-seeking amplitude would
    # reproduce an already-paid coefficient change. It produces an amplitude,
    # never a corrected health coefficient.
    unit_bias = {
        r["exposure"]: r["bias_per_reporting_step"]
        for r in bias_rows
        if r["path"] == "covid_kink_0p10_only"
    }
    by_key: dict[tuple[str, str, str], dict[str, dict]] = {}
    for r in scen:
        by_key.setdefault((r["outcome"], r["pathway_id"], r["exposure"]), {})[
            r["scenario"]
        ] = r
    inversion_rows = []
    for (outcome, pid, expo), got in sorted(by_key.items()):
        base = got.get("baseline_ns4")
        adj = got.get("covid_phase_adjusted")
        if base is None or adj is None:
            continue
        d_log = math.log(float(adj["rr"])) - math.log(float(base["rr"]))
        transfer = unit_bias[expo]
        implied = -0.10 * d_log / transfer if transfer != 0 else float("nan")
        inversion_rows.append(
            {
                "outcome": outcome,
                "pathway_id": pid,
                "exposure": expo,
                "rr_baseline_ns4": float(base["rr"]),
                "rr_covid_phase_adjusted": float(adj["rr"]),
                "delta_log_rr_adjusted_minus_baseline": d_log,
                "transfer_per_0p10_log_dip": transfer,
                "implied_dip_log_amplitude": implied,
                "implied_dip_percent_count_shortfall": 100.0
                * (1.0 - math.exp(-abs(implied)))
                if implied == implied
                else float("nan"),
                "provenance": "HA_APPROVED_AGGREGATE x ILLUSTRATIVE_ALGEBRA",
            }
        )

    # Annual collinearity of exposure trend with the depleting count trend.
    annual_rows = []
    yrs = sorted(set(int(y) for y in year))
    for name, x in exposures.items():
        xa = np.array([x[year == y].sum() for y in yrs])
        for outcome in ("chd", "hf"):
            ya = np.array([totals[outcome][y] for y in yrs])
            annual_rows.append(
                {
                    "exposure": name,
                    "outcome": outcome,
                    "pearson_annual_exposure_vs_events": float(
                        np.corrcoef(xa, ya)[0, 1]
                    ),
                    "pearson_annual_exposure_vs_log_events": float(
                        np.corrcoef(xa, np.log(ya))[0, 1]
                    ),
                    "provenance": "REAL climate x HA_APPROVED_AGGREGATE annual totals",
                }
            )

    hf_cold = next(
        r for r in ladder_stats if r["outcome"] == "hf" and r["pathway_id"] == "P04B"
    )
    chd_hot = next(
        r for r in ladder_stats if r["outcome"] == "chd" and r["pathway_id"] == "P04A"
    )
    hot_ann = next(
        r
        for r in annual_rows
        if r["exposure"] == "hot_nights" and r["outcome"] == "chd"
    )
    cold_ann = next(
        r for r in annual_rows if r["exposure"] == "cold_days" and r["outcome"] == "chd"
    )
    cold_w = next(
        r
        for r in weight_rows
        if r["exposure"] == "cold_days" and r["outcome"] == "hf"
    )
    hot_w = next(
        r
        for r in weight_rows
        if r["exposure"] == "hot_nights" and r["outcome"] == "chd"
    )

    summary = {
        "problem": (
            "What does an absorbing first-event risk set do to a log-link "
            "monthly count model that offsets days-in-month instead of "
            "still-at-risk person-time?"
        ),
        "n_months": 132,
        "total_log_decline_normalisation": total_log_decline,
        "implied_event_halving_ratio": float(
            (totals["chd"][2013] + totals["hf"][2013])
            / (totals["chd"][2023] + totals["hf"][2023])
        ),
        "information_asymmetry": {
            "cold_days_hf_count_weighted_info_share_2013_2018": cold_w[
                "count_weighted_info_share_2013_2018"
            ],
            "hot_nights_chd_count_weighted_info_share_2013_2018": hot_w[
                "count_weighted_info_share_2013_2018"
            ],
            "cold_days_residual_var_share_2013_2018": cold_w[
                "residual_var_share_2013_2018"
            ],
            "hot_nights_residual_var_share_2013_2018": hot_w[
                "residual_var_share_2013_2018"
            ],
        },
        "annual_trend_collinearity": {
            "hot_nights_vs_chd_events": hot_ann["pearson_annual_exposure_vs_events"],
            "hot_nights_vs_log_chd_events": hot_ann[
                "pearson_annual_exposure_vs_log_events"
            ],
            "cold_days_vs_chd_events": cold_ann["pearson_annual_exposure_vs_events"],
        },
        "riskset_fatness_ladder": {
            "n_core_contrasts": len(ladder_stats),
            "n_with_abs_log_rr_rank_corr_eq_1": sum(
                1
                for r in ladder_stats
                if abs(r["spearman_fatness_vs_abs_log_rr"] - 1.0) < 1e-9
            ),
            "n_with_abs_log_rr_rank_corr_ge_0p8": sum(
                1
                for r in ladder_stats
                if r["spearman_fatness_vs_abs_log_rr"] >= 0.8 - 1e-9
            ),
            "n_with_abs_log_rr_rank_corr_le_0": sum(
                1 for r in ladder_stats if r["spearman_fatness_vs_abs_log_rr"] <= 0.0
            ),
            "mean_abs_log_rr_rank_corr": float(
                np.mean([r["spearman_fatness_vs_abs_log_rr"] for r in ladder_stats])
            ),
            "note": (
                "The twelve contrasts share one climate series and are not "
                "independent; the mean is a description, not a test."
            ),
            "hf_cold_days_spearman": hf_cold["spearman_fatness_vs_log_rr"],
            "hf_cold_days_rr_range": [hf_cold["min_rr"], hf_cold["max_rr"]],
            "chd_hot_nights_spearman": chd_hot["spearman_fatness_vs_log_rr"],
            "chd_hot_nights_rr_range": [chd_hot["min_rr"], chd_hot["max_rr"]],
        },
        "covid_kink_inversion": {
            "chd_hot_nights_implied_dip_log_amplitude": next(
                r["implied_dip_log_amplitude"]
                for r in inversion_rows
                if r["outcome"] == "chd" and r["pathway_id"] == "P04A"
            ),
            "hf_cold_days_implied_dip_log_amplitude": next(
                r["implied_dip_log_amplitude"]
                for r in inversion_rows
                if r["outcome"] == "hf" and r["pathway_id"] == "P04B"
            ),
            "transfer_per_0p10_log_dip_hot_nights": unit_bias["hot_nights"],
            "transfer_per_0p10_log_dip_cold_days": unit_bias["cold_days"],
            "chd_non_cold_amplitudes": [
                r["implied_dip_log_amplitude"]
                for r in inversion_rows
                if r["outcome"] == "chd" and r["pathway_id"] != "P04B"
            ],
            "chd_non_cold_amplitude_mean": float(
                np.mean(
                    [
                        r["implied_dip_log_amplitude"]
                        for r in inversion_rows
                        if r["outcome"] == "chd" and r["pathway_id"] != "P04B"
                    ]
                )
            ),
            "chd_non_cold_amplitude_sd": float(
                np.std(
                    [
                        r["implied_dip_log_amplitude"]
                        for r in inversion_rows
                        if r["outcome"] == "chd" and r["pathway_id"] != "P04B"
                    ],
                    ddof=1,
                )
            ),
            "transfer_coefficient_spread_ratio": float(
                max(abs(v) for v in unit_bias.values())
                / min(abs(v) for v in unit_bias.values())
            ),
        },
        "interaction_never_absorbed": {
            "min_share_surviving_controls": min(
                r["share_of_interaction_surviving_controls"] for r in inter_rows
            ),
            "cold_days_front_loaded": next(
                r["share_of_interaction_surviving_controls"]
                for r in inter_rows
                if r["exposure"] == "cold_days" and r["path"] == "front_loaded"
            ),
        },
        "provenance": {
            "climate": "REAL",
            "annual_totals": "HA_APPROVED_AGGREGATE",
            "scenario_coefficients": "HA_APPROVED_AGGREGATE",
            "depletion_paths": "ILLUSTRATIVE_ALGEBRA",
            "new_health_models": False,
            "governed_monthly_counts_read": False,
            "cohort_risk_set_available": False,
        },
    }

    def write_csv(path: Path, rows_out: list[dict]) -> None:
        if not rows_out:
            return
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
            w.writeheader()
            w.writerows(rows_out)

    write_csv(OUT_DIR / "count_weighted_information.csv", weight_rows)
    write_csv(OUT_DIR / "depletion_path_absorption.csv", path_rows)
    write_csv(OUT_DIR / "omitted_logr_bias.csv", bias_rows)
    write_csv(OUT_DIR / "interaction_absorption.csv", inter_rows)
    write_csv(OUT_DIR / "riskset_fatness_ladder.csv", ladder_rows)
    write_csv(OUT_DIR / "riskset_fatness_ladder_stats.csv", ladder_stats)
    write_csv(OUT_DIR / "annual_trend_collinearity.csv", annual_rows)
    write_csv(OUT_DIR / "covid_kink_amplitude_inversion.csv", inversion_rows)
    with (OUT_DIR / "depletion_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print("\nDepletion-path absorption by month FE + ns(time,4):")
    for r in path_rows:
        print(
            f"  {r['path']:32s} R2={r['r2_absorbed_by_month_plus_ns4']:.4f}  "
            f"surviving={r['share_surviving_controls']:.4f}  "
            f"resid_sd={r['residual_sd_after_controls']:.4f}"
        )
    print("\nRisk-set fatness ladder (paid scenario coefficients):")
    for r in sorted(
        ladder_rows, key=lambda r: (r["outcome"], r["pathway_id"], -r["mean_monthly_events_in_window"])
    ):
        if (r["outcome"], r["pathway_id"]) in (("hf", "P04B"), ("chd", "P04A")):
            print(
                f"  {r['outcome']}/{r['exposure']:12s} {r['scenario']:22s} "
                f"mean_monthly={r['mean_monthly_events_in_window']:8.1f}  "
                f"RR={r['rr']:.4f} ({r['rr_low']:.3f}-{r['rr_high']:.3f})"
            )


if __name__ == "__main__":
    main()
