#!/usr/bin/env python3
"""Build the live-track supplementary information from existing archive tables.

No new health model. Does not rebuild manuscript/chd_hf_supplement.pdf.
Does not freeze Gate 3. Numerals are transcribed from named CSVs.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript/live_collaborative/supplement_live_track.md"


def rows(rel: str) -> list[dict]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rrci(r: dict, decimals: int = 3) -> str:
    rr = round(float(r["rr"]), decimals)
    lo = round(float(r["rr_low"]), decimals)
    hi = round(float(r["rr_high"]), decimals)
    return f"{rr:.{decimals}f} ({lo:.{decimals}f}–{hi:.{decimals}f})"


def fmt_p(x: str) -> str:
    v = float(x)
    if v < 1e-7:
        return "<10⁻⁷"
    if v < 0.001:
        return f"{v:.2e}"
    return f"{v:.3f}"


EXPOSURE_ORDER = [
    "mean_temp",
    "mean_tmax",
    "mean_tmin",
    "hot_nights",
    "cold_days",
    "very_hot_days",
]
EXPOSURE_LABEL = {
    "mean_temp": "Mean temperature / 1 °C",
    "mean_tmax": "Mean maximum temperature / 1 °C",
    "mean_tmin": "Mean minimum temperature / 1 °C",
    "hot_nights": "Hot nights / 5 days",
    "cold_days": "Cold days / 5 days",
    "very_hot_days": "Very hot days / 5 days",
}
OUTCOME_LABEL = {"chd": "CHD", "hf": "HF"}
CORE_PATHWAYS = {"P01A", "P02A", "P02B", "P04A", "P04B", "P04C"}
SE_ORDER = ["model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6"]
SE_LABEL = {
    "model": "Model",
    "HC1": "HC1",
    "NeweyWest_lag3": "NW3",
    "NeweyWest_lag6": "NW6",
}


def md_table(headers: list[str], body: list[list[str]]) -> str:
    align = []
    for h in headers:
        align.append("--:" if any(ch.isdigit() for ch in "".join(r[headers.index(h)] for r in body if r)) else ":--")
    # Simpler: numeric-looking columns right-aligned if header suggests it
    lines = ["| " + " | ".join(headers) + " |"]
    aligns = []
    for h in headers:
        aligns.append("--:" if h not in ("Outcome", "Exposure", "Exposure contrast", "Stage", "Term") else ":--")
    lines.append("|" + "|".join(aligns) + "|")
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def table_s1() -> str:
    data = rows("outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv")
    keyed: dict[tuple[str, str], dict[str, str]] = {}
    for r in data:
        keyed.setdefault((r["outcome"], r["exposure"]), {})[r["se_method"]] = r["count_ratio_95CI"].replace("-", "–")
    body = []
    for out in ("chd", "hf"):
        for exp in EXPOSURE_ORDER:
            cells = keyed[(out, exp)]
            body.append(
                [
                    OUTCOME_LABEL[out],
                    EXPOSURE_LABEL[exp],
                    cells["model"],
                    cells["HC1"],
                    cells["NeweyWest_lag3"],
                    cells["NeweyWest_lag6"],
                ]
            )
    return md_table(
        ["Outcome", "Exposure contrast", "Model", "HC1", "NW3", "NW6"],
        body,
    )


def table_s2() -> str:
    data = [
        r
        for r in rows("outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv")
        if r["scenario"] == "pre_covid"
    ]
    data.sort(key=lambda r: (0 if r["outcome"] == "chd" else 1, EXPOSURE_ORDER.index(r["exposure"])))
    body = []
    for r in data:
        lo, hi = float(r["rr_low"]), float(r["rr_high"])
        excl = "excludes 1" if (lo > 1 or hi < 1) else "includes 1"
        body.append(
            [
                OUTCOME_LABEL[r["outcome"]],
                EXPOSURE_LABEL[r["exposure"]],
                rrci(r),
                excl,
            ]
        )
    return md_table(
        ["Outcome", "Exposure contrast", "Count ratio (NW6 95% CI)", "Interval"],
        body,
    )


def table_s3() -> str:
    data = rows("outputs/release_chd_hf/supplement/cvd_lag_sensitivity.csv")
    keyed: dict[tuple[str, str], dict[str, dict]] = {}
    for r in data:
        keyed.setdefault((r["outcome"], r["exposure"]), {})[r["lag_months"]] = r
    body = []
    for out in ("chd", "hf"):
        for exp in EXPOSURE_ORDER:
            cells = keyed[(out, exp)]
            body.append(
                [
                    OUTCOME_LABEL[out],
                    EXPOSURE_LABEL[exp],
                    rrci(cells["0"]),
                    rrci(cells["1"]),
                    rrci(cells["2"]),
                ]
            )
    return md_table(
        ["Outcome", "Exposure contrast", "Lag 0", "Lag 1 month", "Lag 2 months"],
        body,
    )


def table_s4() -> str:
    data = rows("outputs/release_chd_hf/supplement/cvd_influence_sensitivity.csv")
    data.sort(key=lambda r: (0 if r["outcome"] == "chd" else 1, EXPOSURE_ORDER.index(r["exposure"])))
    body = []
    for r in data:
        body.append(
            [
                OUTCOME_LABEL[r["outcome"]],
                EXPOSURE_LABEL[r["exposure"]],
                rrci(r),
                r["excluded_month"],
            ]
        )
    return md_table(
        ["Outcome", "Exposure contrast", "Count ratio after excluding max-Cook month", "Excluded month"],
        body,
    )


def table_s5() -> str:
    vif = rows("outputs/release_chd_hf/supplement/cvd_exposure_vif.csv")
    # VIF is identical across outcomes; show once per exposure group.
    seen = []
    body = []
    for r in vif:
        key = (r["exposure_group"], r["exposure"])
        if key in seen:
            continue
        seen.append(key)
        body.append(
            [
                r["exposure_group"],
                r["exposure"],
                f"{round(float(r['vif_after_month_and_trend']), 2):.2f}",
            ]
        )
    vif_md = md_table(["Joint group", "Exposure", "VIF after month and trend"], body)

    joint = [
        r
        for r in rows("outputs/release_chd_hf/supplement/cvd_single_vs_joint_estimates.csv")
        if r["se_method"] == "NeweyWest_lag6" and r["model_structure"] == "joint_exploratory"
    ]
    jbody = []
    for r in joint:
        label = r["exposure"]
        if "hot_nights" in r["term"]:
            label = "Hot nights / 5 days"
        elif "cold_days" in r["term"]:
            label = "Cold days / 5 days"
        elif "very_hot_days" in r["term"]:
            label = "Very hot days / 5 days"
        elif r["exposure"] == "mean_tmax":
            label = "Mean maximum temperature / 1 °C"
        elif r["exposure"] == "mean_tmin":
            label = "Mean minimum temperature / 1 °C"
        jbody.append([OUTCOME_LABEL[r["outcome"]], label, rrci(r)])
    joint_md = md_table(["Outcome", "Exposure in joint model", "Joint NW6 count ratio (95% CI)"], jbody)
    return vif_md + "\n\nJoint Newey–West lag-6 estimates (diagnostics, not preferred):\n\n" + joint_md


def table_s6() -> str:
    chd = [
        r
        for r in rows("outputs/release_chd_hf/supplement/chd_pathway_core_diagnostics.csv")
        if r["pathway_id"] in CORE_PATHWAYS and r["offset_policy"] == "days_only"
    ]
    hf = [
        r
        for r in rows("outputs/release_chd_hf/supplement/hf_pathway_core_diagnostics.csv")
        if r["pathway_id"] in CORE_PATHWAYS and r["offset_policy"] == "days_only"
    ]
    path_exp = {
        "P01A": "Mean temperature",
        "P02A": "Mean maximum temperature",
        "P02B": "Mean minimum temperature",
        "P04A": "Hot nights",
        "P04B": "Cold days",
        "P04C": "Very hot days",
    }
    body = []
    for r in chd + hf:
        body.append(
            [
                OUTCOME_LABEL[r["outcome"]],
                path_exp[r["pathway_id"]],
                f"{float(r['residual_acf1']):.3f}",
                fmt_p(r["ljung_box_p_lag6"]),
                fmt_p(r["ljung_box_p_lag12"]),
            ]
        )
    return md_table(
        ["Outcome", "Core exposure", "Pearson ACF lag 1", "Ljung–Box p, lag 6", "Ljung–Box p, lag 12"],
        body,
    )


def table_s8() -> str:
    data = rows(
        "outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_gate_summary.csv"
    )
    body = []
    for r in data:
        body.append(
            [
                r["gate_id"],
                r["detail"].split(";")[0],
                "passed" if r["passed"].upper() == "TRUE" else "failed",
            ]
        )
    return md_table(["Gate", "Observed (methods validation)", "Result"], body)


def table_s7() -> str:
    data = [
        r
        for r in rows("outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv")
        if r["pathway_id"] == "P14" and r["term"] == "flu_indicator"
    ]
    body = []
    for r in data:
        body.append(
            [
                OUTCOME_LABEL[r["outcome"]],
                "Influenza indicator",
                rrci(r),
                r["n_months"],
            ]
        )
    return md_table(["Outcome", "Term", "Count ratio (95% CI)", "Months"], body)


def table_s9() -> str:
    data = [
        r
        for r in rows("outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv")
        if r["pathway_id"] == "P11"
    ]

    def stage_block(outcome: str) -> str:
        stages = ["none", "NO2", "PM25", "O3", "multi"]
        stage_label = {
            "none": "none",
            "NO2": "NO₂",
            "PM25": "PM2.5",
            "O3": "O₃",
            "multi": "multi",
        }
        body = []
        for st in stages:
            subset = [r for r in data if r["outcome"] == outcome and r["pollution_stage"] == st]
            tmax = next(r for r in subset if r["term"] == "mean_tmax")
            tmin = next(r for r in subset if r["term"] == "mean_tmin")
            pols = [r for r in subset if r["term"] in ("NO2", "PM25", "O3")]
            if not pols:
                pol_s = "—"
            else:
                bits = []
                for r in pols:
                    name = {"NO2": "NO₂", "PM25": "PM2.5", "O3": "O₃"}[r["term"]]
                    bits.append(f"{name} {rrci(r)}")
                pol_s = "; ".join(bits)
            body.append([stage_label[st], rrci(tmax), rrci(tmin), pol_s])
        return md_table(["Stage", "Mean Tmax", "Mean Tmin", "Pollutant term"], body)

    return (
        "*CHD*\n\n"
        + stage_block("chd")
        + "\n\n*HF*\n\n"
        + stage_block("hf")
    )


def table_s10() -> str:
    data = [
        r
        for r in rows("outputs/tables/cvd_descriptive_covid_era_means.csv")
        if r["outcome"] == "chd"
    ]
    order = [
        ("pre_covid_2013_2019", "2013–2019"),
        ("covid_2020_2022", "2020–2022"),
        ("post_reopening_2023", "2023"),
    ]
    keyed = {r["period"]: r for r in data}
    body = []
    for period, label in order:
        r = keyed[period]
        body.append(
            [
                label,
                r["n_months"],
                f"{float(r['mean_temp']):.2f}",
                f"{float(r['mean_hot_nights']):.2f}",
                f"{float(r['mean_very_hot_days']):.2f}",
                f"{float(r['mean_cold_days']):.2f}",
            ]
        )
    return md_table(
        [
            "Period",
            "Months",
            "Mean temperature, °C",
            "Hot nights / month",
            "Very hot days / month",
            "Cold days / month",
        ],
        body,
    )


def main() -> int:
    text = f"""# Live-track supplementary information

**Authority:** live collaborative manuscript `Heat_CVD_Manuscript_live_update.md`.  
**Not** the 10 August `manuscript/chd_hf_supplement.pdf` (do not rebuild).  
**Not** Hogan’s shared Word/Google file (Bob pastes; agents do not).

This file is the journal-takeable supplement for the analysis-window sensitivity manuscript. Every numeral is transcribed from an existing `HA_APPROVED_AGGREGATE`, `REAL`, or `SYNTHETIC_CALIBRATION` table. No new health model was fitted. The twelve thermal fits are **Model 1**. Archive influenza and pollution models are **not** adjusted versions of Model 1. No confirmatory primary is declared.

Numbering matches the live body: Supplementary Figure S1 is residual ACF; Supplementary Tables S7 and S9 are archive influenza and archive pollution. The release heatmap filename `figureS1_exposure_correlation.png` is Supplementary Figure **S4** here.

## Supplementary Figure S1. Residual autocorrelation in two displayed exploratory core models

![Supplementary Figure S1](../../figures/live_identification/figure_C_residual_acf.png)

Bars show the Pearson residual autocorrelation function for the separate-exposure negative-binomial CHD hot-night and HF cold-day models. Dashed lines mark ±1.96/√132. Lag-1 residual autocorrelation was 0.508 for CHD hot nights and 0.146 for HF cold days. These diagnostics motivate reporting more than one covariance estimator; they do not establish that a particular estimator is correct, protect either contrast from multiplicity, or identify a causal thermal effect. Source: residuals from the governed aggregate core models.

## Supplementary Table S1. Complete Model 1 uncertainty ladder

Count ratios use the days-in-month offset. Intervals are model-based, HC1, Newey–West lag 3, and Newey–West lag 6. No interval was selected because it excluded 1. Display strings are those in `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`.

{table_s1()}

## Supplementary Figure S2. Standard-error method ladder for two displayed exploratory contrasts

![Supplementary Figure S2](../../outputs/release_chd_hf/figures/figure5_se_method_ladder.png)

The figure displays the same four constructions as Table 3 of the main paper. Concordance across constructions is not multiplicity protection. Source: `outputs/release_chd_hf/figures/figure5_se_method_ladder.png`.

## Supplementary Table S2. Model 1 contrasts in the pre-2020 window (Newey–West lag-6)

January 2013–December 2019; 84 months. Nine of twelve intervals exclude 1. All six continuous temperature contrasts are inverse. No multiplicity control was computed within this window, and no pre-2020 estimate is promoted beyond a sensitivity. Source: `pre_covid` rows of `outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv`. Main-text Figure 3 shows the six official-count fits. Continuous-temperature fits for the same nine specifications are Supplementary Figure S6.

{table_s2()}

## Supplementary Figure S6. Continuous-temperature Model 1 estimates across the same checks

![Supplementary Figure S6](../../figures/live_identification/figure_E_continuous_temperature_sensitivity.png)

Same nine trend, window, and COVID-period specifications as main-text Figure 3. Each estimate is per 1 °C. Pre-2020 inverse associations for mean, maximum, and minimum temperature are in this panel. Rows labelled 3, 6, or 8 df change the time-trend spline, not heatwave length. Source: `outputs/tables/cvd_trend_depletion_sensitivity.csv` (`HA_APPROVED_AGGREGATE`). No new health model.

## Supplementary Figure S3. Complete twelve-contrast core forest (Newey–West lag-6)

![Supplementary Figure S3](../../outputs/release_chd_hf/figures/figure3_core_forest.png)

Main-text Table 2 remains the reporting table. Source: `outputs/release_chd_hf/figures/figure3_core_forest.png`.

## Supplementary Figure S4. Pairwise exposure correlations

![Supplementary Figure S4](../../outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png)

Source filename `figureS1_exposure_correlation.png` is retained; the live-pack display number is S4, not S1.

## Supplementary Table S3. Lag-0, lag-1, and lag-2 month exposures (Newey–West lag-6)

Lag-one month is a labelled sensitivity, not a daily lag curve. Source: `outputs/release_chd_hf/supplement/cvd_lag_sensitivity.csv`.

{table_s3()}

## Supplementary Table S4. Exclusion of the month with largest Cook’s distance (Newey–West lag-6)

{table_s4()}

Source: `outputs/release_chd_hf/supplement/cvd_influence_sensitivity.csv`.

## Supplementary Table S5. Collinearity diagnostics after month and trend residualisation

Variance inflation factors are identical for the CHD and HF design matrices. Joint coefficients are diagnostics and not preferred estimates. Source: `outputs/release_chd_hf/supplement/cvd_exposure_vif.csv` and `cvd_single_vs_joint_estimates.csv`.

{table_s5()}

## Supplementary Table S6. Residual diagnostics for the twelve Model 1 fits

{table_s6()}

Source: `outputs/release_chd_hf/supplement/chd_pathway_core_diagnostics.csv` and `hf_pathway_core_diagnostics.csv` (days-in-month offset core pathways).

## Supplementary Table S7. Archive influenza co-exposure (pathway P14; 121 months)

Missing influenza months were not zero-filled. This model uses a general-population × days offset and is not an adjusted version of Model 1.

{table_s7()}

Source: `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv`, P14 `flu_indicator` rows.

## Supplementary Table S8. Daily-recovery calibration gates (methods validation, not a health finding)

Source: synthetic calibration (`SYNTHETIC_CALIBRATION`); methods validation, not a CHD/HF health finding. No real daily coefficient is admitted. This table does not establish a general failure of recovering daily effects from aggregated outcomes.

{table_s8()}

Source: `outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_gate_summary.csv`.

## Supplementary Table S9. Archive pollution-staged models (pathway P11; joint mean Tmax and Tmin)

Count ratios are for a 1 °C temperature contrast or a 1 µg m^−3^ pollutant contrast. Stages: none, NO₂, PM2.5, ozone, and all three (`multi`). Offset is general-population × days. On a monthly grain these models cannot separate ozone confounding from mediation. No staged estimate was used to revise Table 2.

{table_s9()}

Nitrogen dioxide retains a positive coefficient in the CHD and HF archive fits. That is a co-predictor fact, not a thermal finding. Source: `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv`, P11 rows.

## Supplementary Table S10. Weather summaries by analysis period

These are exposure summaries, not health effects. Pre-2020 is January 2013–December 2019. The pandemic-era row is January 2020–December 2022. The 2023 row is shown separately because reopening is not the same object as the earlier pandemic period.

{table_s10()}

Source: HKO Headquarters monthly series in `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv` (`REAL`). The same summaries are cross-checked in `outputs/tables/cvd_descriptive_covid_era_means.csv`. Later years were hotter; official cold-day frequency was similar rather than absent.

## Supplementary Note S1. Thermal and mechanistic context

Earlier Hong Kong studies used daily, cause-coded or unplanned admissions. Goggins et al. reported a cold association for acute myocardial infarction [1]. Goggins and Chan reported a cumulative heart-failure admission contrast for 11 °C versus 25 °C over daily lags [21]. Guo et al. distinguished the official hot-night flag from hourly nighttime excess heat [17]. None of those estimands transfers to monthly counts of first hospitalisation after a first diagnosis.

Hong Kong mortality studies are complementary rather than interchangeable. Liu et al. reported temperature-attributable mortality fractions [12]. Liu et al. later modelled heatwave-associated excess deaths [13]. Neither quantity can be rescaled into the count ratios in the main manuscript.

Sleep, nighttime core temperature, heart-rate variability, cold afterload, and heat-health action plans were reviewed in the thermal manuscript [23–33]. Those sources remain hypotheses or policy context. The monthly series measures none of those mechanisms and does not evaluate Hong Kong’s warnings. The HKO yearbooks for 2013, 2017, 2021, and 2024 remain in the reference block [2–5]; the 2024 yearbook is outside the analysis window and is not used in an estimate.

## Scope of this supplement

This supplement does not contain stroke results, principal-diagnosis or AMI claims from this extract, cohort incidence, a real daily-recovery coefficient, a confounding-adjusted version of Model 1, or a health-economic result. Provisional hot-month and cold-month estimates are ineligible as a primary claim.
"""
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
