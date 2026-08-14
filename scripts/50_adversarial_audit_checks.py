#!/usr/bin/env python3
"""Adversarial-audit arithmetic for the four identification-crucible theses.

Provenance: REAL HKO monthly climate (2013-01..2023-12) plus already-paid
HA_APPROVED_AGGREGATE coefficients and descriptives that are already in
outputs/tables/ and outputs/*_crucible/. No governed monthly count is read, no
health model is fit, and no new health coefficient is produced. Every quantity
here is either a projection of the REAL climate design matrix or an arithmetic
identity applied to numbers the project has already paid for.

Five checks, one per attack that needed a number rather than a reading:

1. GAMMA / seasonal containment. Does the month-FE per-degree interval exclude
   the crude between-season gradient implied by the paid seasonality table?
2. GAMMA / flu counterexample. The P14 flu coefficient is fitted under the same
   month-FE + ns(time,4) control space, so it measures whether that space can
   still detect a winter-concentrated exposure.
3. DELTA / observed-power identity. observed/detectable in bh_detectability.csv
   is z/2.8, a monotone restatement of the p-value.
4. DELTA / cold-day sparsity. Where does residual cold-day identifying variance
   actually sit, by winter?
5. BETA / inversion genericity. The implied "latent dip amplitude" is
   proportional to Cov(xtilde, utilde) / Cov(xtilde, vtilde) for the true shape u
   and the stipulated shape v, so cross-exposure coherence tests only whether two
   pandemic-era time shapes load proportionally on residual weather. Recomputed
   for a family of alternative shapes.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CLIMATE = ROOT / "data_processed" / "climate_monthly_2013_2023.csv"
TABLES = ROOT / "outputs" / "tables"
IDENT = ROOT / "outputs" / "identification_crucible"
DEPL = ROOT / "outputs" / "depletion_crucible"
OUT_DIR = ROOT / "outputs" / "adversarial_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXPOSURES = (
    "mean_temp",
    "mean_tmax",
    "mean_tmin",
    "hot_nights",
    "cold_days",
    "very_hot_days",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _load_crucible_helpers():
    """Reuse script 49's spline and projection helpers so the control space is
    identical to the one both crucible memos already argued from."""
    spec = importlib.util.spec_from_file_location(
        "_depl", ROOT / "scripts" / "49_depletion_crucible.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def norm_ppf(p: float) -> float:
    """Acklam-style inverse normal, sufficient for reporting two decimals."""
    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1
    )


def main() -> None:
    helpers = _load_crucible_helpers()
    rows = read_csv(CLIMATE)
    assert len(rows) == 132, f"expected 132 months, got {len(rows)}"
    month = np.array([int(r["month"]) for r in rows], dtype=int)
    year = np.array([int(r["year"]) for r in rows], dtype=int)
    t_index = np.arange(len(rows), dtype=float)
    exposures = {k: np.array([float(r[k]) for r in rows]) for k in EXPOSURES}

    C = np.column_stack(
        [
            np.ones(len(rows)),
            helpers.month_dummies(month),
            helpers.ns_basis(t_index, df=4),
        ]
    )
    resid = {k: helpers.resid_and_r2(C, v)[0] for k, v in exposures.items()}

    out: dict[str, object] = {
        "problem": "Does each crucible thesis survive a concrete counterexample?",
        "provenance": {
            "climate": "REAL",
            "coefficients": "HA_APPROVED_AGGREGATE",
            "new_health_models": False,
            "governed_counts_read": False,
        },
    }

    # ---------------------------------------------------------------- 1
    # GAMMA: does the anomaly interval exclude the crude seasonal gradient?
    season = read_csv(TABLES / "cvd_descriptive_seasonality_by_month.csv")
    scen = read_csv(TABLES / "cvd_trend_depletion_sensitivity.csv")
    baseline = {
        (r["outcome"], r["pathway_id"]): r
        for r in scen
        if r["scenario"] == "baseline_ns4"
    }
    containment = []
    for outcome in ("chd", "hf"):
        cells = {int(r["month"]): r for r in season if r["outcome"] == outcome}
        jan, sep = cells[1], cells[9]
        d_log = math.log(float(jan["mean_events"]) / float(sep["mean_events"]))
        d_temp = float(sep["mean_temp"]) - float(jan["mean_temp"])
        crude_slope = -d_log / d_temp  # log count change per +1 degree C
        row = baseline[(outcome, "P01A")]
        est = float(row["estimate"])
        se = float(row["std_error_nw6"])
        lo, hi = est - 1.96 * se, est + 1.96 * se
        containment.append(
            {
                "outcome": outcome,
                "jan_mean_events": float(jan["mean_events"]),
                "sep_mean_events": float(sep["mean_events"]),
                "jan_minus_sep_temp_c": -d_temp,
                "crude_between_season_slope_per_c": crude_slope,
                "anomaly_slope_per_c": est,
                "anomaly_ci_low": lo,
                "anomaly_ci_high": hi,
                "anomaly_ci_contains_crude_seasonal_slope": bool(lo <= crude_slope <= hi),
                "provenance": "HA_APPROVED_AGGREGATE descriptives x paid NW6 coefficient",
            }
        )
    out["gamma_seasonal_containment"] = containment

    # ---------------------------------------------------------------- 2
    # GAMMA: flu is fitted inside the same month-FE control space.
    panel = read_csv(TABLES / "combined_pathway_panel_estimates.csv")
    flu = [
        {
            "outcome": r["outcome"],
            "term": r["term"],
            "rr": float(r["rr"]),
            "rr_low": float(r["rr_low"]),
            "rr_high": float(r["rr_high"]),
            "p_value": float(r["p_value"]),
            "n_months": int(r["n_months"]),
            "offset_policy": r["offset_policy"],
            "pathway_role": r["pathway_role"],
            "provenance": r["data_status"],
        }
        for r in panel
        if r["pathway_id"] == "P14" and r["term"] == "flu_indicator"
    ]
    # How much of the flu series survives the same control space? If a lot, the
    # month dummies are removing the fixed calendar pattern of whatever is fed
    # to them, not refusing to estimate winter-linked exposures.
    conf = read_csv(ROOT / "data_processed" / "confounders_monthly_2013_2023.csv")
    flu_raw = np.array(
        [float(r["flu_indicator"]) if r["flu_indicator"] != "" else np.nan for r in conf]
    )
    obs = ~np.isnan(flu_raw)
    C_obs = np.column_stack(
        [
            np.ones(int(obs.sum())),
            helpers.month_dummies(month[obs]),
            helpers.ns_basis(t_index[obs], df=4),
        ]
    )
    flu_res, flu_r2 = helpers.resid_and_r2(C_obs, flu_raw[obs])
    out["gamma_flu_inside_month_fe"] = {
        "controls": "month_f + splines::ns(time_index, df = 4) (scripts/20_fit_pathway_panel.R core controls)",
        "flu_months_observed": int(obs.sum()),
        "flu_r2_month_plus_ns4": flu_r2,
        "flu_variation_share_remaining_after_full_controls": 1.0 - flu_r2,
        "mean_temp_variation_share_remaining_after_full_controls": 1.0
        - helpers.resid_and_r2(C, exposures["mean_temp"])[1],
        "rows": flu,
    }

    # ---------------------------------------------------------------- 3
    # DELTA: observed/detectable is z/2.8.
    det = read_csv(IDENT / "bh_detectability.csv")
    identity = []
    for r in det:
        p = float(r["p_value"])
        z = norm_ppf(1.0 - p / 2.0)
        reported = float(r["observed_over_detectable"])
        identity.append(
            {
                "outcome": r["outcome"],
                "pathway_id": r["pathway_id"],
                "p_value": p,
                "z_from_p": z,
                "z_over_2p8": z / 2.8,
                "reported_observed_over_detectable": reported,
                "abs_gap": abs(z / 2.8 - reported),
            }
        )
    out["delta_observed_power_identity"] = {
        "claim": "observed/detectable = |beta|/(2.8*SE) = z/2.8, a monotone function of p alone",
        "max_abs_gap": max(r["abs_gap"] for r in identity),
        "rows": identity,
    }

    # ---------------------------------------------------------------- 4
    # DELTA: where does residual cold-day identifying variance live?
    sparsity = {}
    for name in ("cold_days", "hot_nights"):
        x = resid[name]
        ss = x**2
        total = float(ss.sum())
        # Winter label: Dec of year y groups with Jan/Feb of y+1.
        wyear = np.where(month == 12, year + 1, year)
        shares = {}
        for wy in sorted(set(wyear.tolist())):
            shares[int(wy)] = float(ss[wyear == wy].sum() / total)
        ordered = sorted(shares.values(), reverse=True)
        cum, n80 = 0.0, 0
        for s in ordered:
            cum += s
            n80 += 1
            if cum >= 0.80:
                break
        top_months = np.sort(ss)[::-1] / total
        sparsity[name] = {
            "nonzero_months": int((exposures[name] > 0).sum()),
            "share_by_year_group": shares,
            "top_year_group_share": ordered[0],
            "year_groups_for_80pct": n80,
            "top1_month_share": float(top_months[0]),
            "top5_month_share": float(top_months[:5].sum()),
            "top10_month_share": float(top_months[:10].sum()),
            "provenance": "REAL",
        }
    out["delta_identifying_variance_sparsity"] = sparsity

    # HF cold-day window ladder, with the interval at each rung.
    ladder = [
        {
            "scenario": r["scenario"],
            "n_months": int(r["n_months"]),
            "rr": float(r["rr"]),
            "rr_low": float(r["rr_low"]),
            "rr_high": float(r["rr_high"]),
            "p_value_nw6": float(r["p_value_nw6"]),
            "excludes_1": float(r["rr_low"]) > 1.0,
            "provenance": r["data_status"],
        }
        for r in scen
        if r["outcome"] == "hf" and r["pathway_id"] == "P04B"
    ]
    out["delta_hf_cold_window_ladder"] = ladder

    # ---------------------------------------------------------------- 5
    # BETA: is the inverted "common amplitude" generic?
    #
    # amplitude_x proportional to Cov(xtilde, utilde) / Cov(xtilde, vtilde) for
    # true pandemic-era shape u and stipulated shape v. If arbitrary u also give
    # a tight cross-exposure cluster, coherence has no discriminating power.
    v = np.zeros(len(rows))
    v[(t_index >= 85) & (t_index <= 88)] = -0.10  # 2020-02..2020-05
    v[(t_index >= 109) & (t_index <= 112)] = -0.10  # 2022-02..2022-05
    v_res = helpers.resid_and_r2(C, v)[0]

    def block(lo: int, hi: int) -> np.ndarray:
        u = np.zeros(len(rows))
        u[(t_index >= lo) & (t_index <= hi)] = -1.0
        return u

    ramp = np.zeros(len(rows))
    mask = t_index >= 85
    ramp[mask] = -np.linspace(0.0, 1.0, int(mask.sum()))

    alternatives = {
        "beta_stipulated_dip_2020_2022_feb_may": v,
        "released_covid_phase_early_covid_2020_02_2021_12": block(85, 107),
        "released_covid_phase_fifth_wave_2022_01_2022_04": block(84 + 24, 84 + 27),
        "released_covid_phase_late_2022": block(112, 119),
        "released_covid_phase_post_reopening_2023": block(120, 131),
        "single_block_2020_02_to_2023_12": block(85, 131),
        "ramp_from_2020_02": ramp,
    }
    # The five contrasts Beta reports as coherent: all but cold days.
    coherent_set = [e for e in EXPOSURES if e != "cold_days"]
    genericity = []
    for label, u in alternatives.items():
        u_res = helpers.resid_and_r2(C, u)[0]
        ratios = {}
        for e in EXPOSURES:
            num = float(np.dot(resid[e], u_res))
            den = float(np.dot(resid[e], v_res))
            ratios[e] = num / den if den != 0 else float("nan")
        vals = np.array([ratios[e] for e in coherent_set])
        genericity.append(
            {
                "assumed_true_shape": label,
                "ratio_by_exposure": ratios,
                "non_cold_mean": float(np.mean(vals)),
                "non_cold_sd": float(np.std(vals, ddof=1)),
                "non_cold_cv": float(np.std(vals, ddof=1) / abs(np.mean(vals))),
                "cold_days_ratio_sign_flips_vs_non_cold": bool(
                    np.sign(ratios["cold_days"]) != np.sign(np.mean(vals))
                ),
                "provenance": "REAL climate projection",
            }
        )
    out["beta_inversion_genericity"] = {
        "claim": (
            "The recovered amplitude is proportional to "
            "Cov(xtilde,utilde)/Cov(xtilde,vtilde); cross-exposure coherence is a "
            "property of the two time shapes, not evidence for an omitted risk set."
        ),
        "stipulated_shape_v": "0.10 log-unit dip, 2020-02..2020-05 and 2022-02..2022-05",
        "released_operator": (
            "covid_phase_f, a 5-level factor (4 dummies) spanning 2020-02..2023-12, "
            "config.yml covid_phases"
        ),
        "share_of_stipulated_dip_spanned_by_released_phase_dummies": None,
        "rows": genericity,
    }

    # How much of Beta's stipulated dip does the released operator even span?
    phase_design = np.column_stack(
        [
            block(85, 107),
            block(108, 111),
            block(112, 119),
            block(120, 131),
        ]
    )
    phase_res = np.column_stack(
        [helpers.resid_and_r2(C, phase_design[:, j])[0] for j in range(4)]
    )
    fit = phase_res @ np.linalg.lstsq(phase_res, v_res, rcond=None)[0]
    r2_span = 1.0 - float(np.sum((v_res - fit) ** 2) / np.sum(v_res**2))
    out["beta_inversion_genericity"][
        "share_of_stipulated_dip_spanned_by_released_phase_dummies"
    ] = r2_span

    # BETA: the same inversion, read for both outcomes rather than CHD only.
    inv = read_csv(DEPL / "covid_kink_amplitude_inversion.csv")
    per_outcome = {}
    for outcome in ("chd", "hf"):
        vals = [
            float(r["implied_dip_log_amplitude"])
            for r in inv
            if r["outcome"] == outcome and r["exposure"] != "cold_days"
        ]
        arr = np.array(vals)
        per_outcome[outcome] = {
            "non_cold_amplitudes": vals,
            "mean": float(arr.mean()),
            "sd": float(arr.std(ddof=1)),
            "cv": float(arr.std(ddof=1) / abs(arr.mean())),
            "cold_days_amplitude": next(
                float(r["implied_dip_log_amplitude"])
                for r in inv
                if r["outcome"] == outcome and r["exposure"] == "cold_days"
            ),
        }
    out["beta_inversion_by_outcome"] = {
        "note": (
            "Beta reports the CHD five only. The same table's HF five span a "
            "factor of 2.3 and centre on a different amplitude."
        ),
        "by_outcome": per_outcome,
        "hf_over_chd_mean_ratio": per_outcome["hf"]["mean"] / per_outcome["chd"]["mean"],
        "provenance": "HA_APPROVED_AGGREGATE x ILLUSTRATIVE_ALGEBRA",
    }

    path = OUT_DIR / "adversarial_audit_checks.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {path}")
    print(json.dumps(out["gamma_seasonal_containment"], indent=2))
    print(
        "max |z/2.8 - reported observed/detectable| =",
        out["delta_observed_power_identity"]["max_abs_gap"],
    )
    for r in out["beta_inversion_genericity"]["rows"]:
        print(
            f"  {r['assumed_true_shape']:<52s} non-cold CV = {r['non_cold_cv']:.3f}"
        )
    print(
        "dip spanned by released phase dummies R2 =",
        round(r2_span, 4),
    )
    print(json.dumps(out["beta_inversion_by_outcome"]["by_outcome"], indent=2))
    print(
        "cold-day identifying variance: top winter share =",
        round(sparsity["cold_days"]["top_year_group_share"], 3),
        "| winters for 80% =",
        sparsity["cold_days"]["year_groups_for_80pct"],
    )


if __name__ == "__main__":
    main()
