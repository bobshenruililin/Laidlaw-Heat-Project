# Supplement — CHD/HF monthly thermal associations, Hong Kong, 2013–2023

Companion to [`chd_hf_thermal_associations_2013_2023.md`](chd_hf_thermal_associations_2013_2023.md).
All numerical claims below are drawn from `outputs/release_chd_hf/` or the cited sensitivity tables. Provenance is `HA_APPROVED_AGGREGATE`.

## S1. Complete pathway panel

Territory-month negative-binomial (or quasi-Poisson fallback) fits for enabled pathway IDs are archived in:

- `outputs/tables/chd_pathway_panel_estimates.csv`
- `outputs/tables/hf_pathway_panel_estimates.csv`
- `outputs/tables/combined_pathway_panel_estimates.csv`
- forests in `outputs/release_chd_hf/supplement/*_pathway_panel_forest.png`

Joint P02, P04, and nested P07 remain exploratory. Separate amended IDs P01A, P02A/B, P04A–C, and P07A–D are the structures used for manuscript inference candidates.

## S2. Joint versus separate exposure models

File: `outputs/release_chd_hf/supplement/cvd_single_vs_joint_estimates.csv`

After month and trend residualisation, VIF for mean maximum and minimum temperature was 4.66. VIF for hot nights and very hot days was approximately 1.96 (`cvd_exposure_vif.csv`). The CHD hot-night coefficient was larger in the joint extreme-day model than in the separate P04A model under the same days-only offset and Newey–West lag-6 intervals.

## S3. Offset, SE method, and family ladder

File: `outputs/release_chd_hf/supplement/cvd_core_robust_estimates.csv`

For each amended core exposure, estimates are available for:

- offsets: days only, population × days, none;
- families: negative binomial, quasi-Poisson;
- SE methods: model-based, HC1, Newey–West lag 3, Newey–West lag 6.

Manuscript Table 2 freezes the days-only, negative-binomial, Newey–West lag-6 slice.

## S4. Trend, depletion, lag, influence, and INGARCH

Files:

- `cvd_trend_depletion_sensitivity.csv`
- `cvd_lag_sensitivity.csv`
- `cvd_influence_sensitivity.csv`
- `cvd_count_timeseries_sensitivity.csv`
- Figure 4 and residual ACF/PACF plots in the release supplement folder

## S5. Provisional hot-month and cold-month calendar

Provisional HM/CM flags remain unlocked. The calendar figure is supplementary only (`figureS2_provisional_hm_cm_calendar.*`). Estimates from `*_hm_cm_panel_estimates.csv` are not eligible for primary claims until weather reference rules are locked.

## S6. Diagnostics and release validation

- Real-panel diagnostics: `*_pathway_core_diagnostics.csv` (n = 132; `synthetic = FALSE`).
- Release validation: `outputs/reports/cvd_real_release_validation.md` (9/9 checks passed on the package used for this draft).
- Claim ledger: `outputs/release_chd_hf/tables/claim_ledger.csv`.

## S7. What this supplement does not contain

- Source monthly HA count files
- Merged health–environment panels with event counts
- Synthetic coefficients
- Stroke results
- Locked hot-month / cold-month primary estimates
