# Sol main-text and supplement map

**Purpose:** keep the journal article short without hiding the diagnostics that determine identification and uncertainty. This map uses existing `HA_APPROVED_AGGREGATE`, `REAL`, `REAL_PUBLIC_HKO`, and `SYNTHETIC_CALIBRATION` artifacts. It adds no health model and does not freeze Gate 3.

**16 August live-pack numbering (canonical for Hogan paste):** Supplementary **Figure S1** is residual ACF (`figures/live_identification/figure_C_residual_acf.png`). Supplementary **Tables S7** and **S9** are archive influenza and archive pollution. See [`manuscript/live_collaborative/supplement_inventory.md`](../live_collaborative/supplement_inventory.md). This map previously assigned Figure S1 to the core forest; that assignment is withdrawn. The 10 August `chd_hf_supplement.pdf` is not rebuilt.

## Main paper

The main paper should carry the estimand, the complete core family, and the three displays needed to understand identification. It should not carry every diagnostic plot.

### Main figures

| Main display | Exact path | Role | Assembly status in this checkout |
|---|---|---|---|
| **Figure 1: first-event depletion** | `figures/live_identification/figure_B_first_event_depletion.png` | Shows the decline in CHD/HF first-event counts against the rise in the general population aged 35 years or older. It prevents incidence language. | Present in this checkout (PNG and PDF). Source table: `outputs/tables/cvd_descriptive_annual_totals.csv`. |
| **Figure 2: DJF cold-day identification** | `figures/live_identification/figure_A_cold_day_identification.png` | Shows that 141 of 145 official cold days occurred in December–February. It makes clear that the cold-day coefficient is identified by differences between winters. | Present in this checkout (PNG and PDF). Source table: `outputs/live_identification/cold_days_by_month_year.csv`. |
| **Figure 3: trend and first-event-depletion sensitivity** | `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png` | Shows the full core family across trend, window, and COVID-phase specifications. It makes the pre-2020 CHD hot-night interval crossing 1 visible while showing the stronger pre-2020 HF cold-day estimate. | Present in this checkout as PNG, PDF, and SVG. The live paste pack also carries `figures/live_identification/figure_D_trend_depletion_sensitivity.png`. |

Do not substitute the indexed-series, seasonal-profile, or core-forest release figures for these three. Figures 1 and 2 explain the estimand and exposure variation. Figure 3 explains temporal sensitivity.

### Main tables

| Main table | Exact path | Main-text use |
|---|---|---|
| **Table 1: outcome summary** | `outputs/release_chd_hf/tables/table1_outcome_summary.csv` | Keep the two outcome totals, 132 months, monthly means, and exact event construction. |
| **Table 2: complete core panel** | `outputs/release_chd_hf/tables/table2_core_models.csv` | Keep all twelve Newey–West lag-6 count ratios and BH *q*-values. This is the family against which the two exploratory residual signals must be read. |

The main Results should retain four facts even after the diagnostic displays move:

1. all twelve core *q*-values exceed 0.19;
2. CHD hot-night Model and HC1 intervals include 1, while NW3 and NW6 exclude 1 on the unrounded scale;
3. the Newey–West intervals for CHD hot nights are narrower than the model-based interval, so the exclusion of 1 rests on a smaller robust variance estimate; and
4. CHD hot nights are compatible with 1 before 2020, whereas the pre-2020 HF cold-day interval remains above 1.

## Supplement

### S1. Definitions, estimand, governance, and reporting checklist

Keep the existing outcome construction, denominator warning, provenance firewall, scope exclusions, and reproducibility index. Point the checklist to the core panel rather than an undefined “continuity” analysis.

Core files:

- `outputs/release_chd_hf/tables/claim_ledger_v2.csv`
- `outputs/release_chd_hf/tables/analysis_availability.csv`
- `outputs/release_chd_hf/validation_checks.csv`
- `outputs/release_chd_hf/release_manifest.csv`
- `outputs/release_chd_hf/RELEASE_INDEX.md`

### S2. Full core estimates and multiplicity

The twelve core estimates remain in the main paper. The supplement carries their machine-readable identity and the full covariance ladder:

- `outputs/release_chd_hf/tables/table2_core_models.csv`
- `outputs/release_chd_hf/tables/claim_ledger_v2.csv`
- **Supplementary Table S1:** `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`
- **Supplementary Figure S2:** `outputs/release_chd_hf/figures/figure5_se_method_ladder.png`
- available vector source in this checkout: `outputs/release_chd_hf/figures/figure5_se_method_ladder.svg`

Do not describe the ladder as a search for the interval that excludes 1.

### S3. Identification, residual dependence, and collinearity

Demote the current ACF display and core forest:

- **Supplementary Figure S1:** `figures/live_identification/figure_C_residual_acf.png` (live-body citation)
- supporting ACF/PACF plots:
  - `outputs/release_chd_hf/supplement/chd_core_residual_acf_pacf.png`
  - `outputs/release_chd_hf/supplement/hf_core_residual_acf_pacf.png`
- residual tables:
  - `outputs/release_chd_hf/supplement/chd_pathway_residual_acf.csv`
  - `outputs/release_chd_hf/supplement/hf_pathway_residual_acf.csv`
  - `outputs/release_chd_hf/supplement/chd_pathway_core_diagnostics.csv`
  - `outputs/release_chd_hf/supplement/hf_pathway_core_diagnostics.csv`
- **Supplementary Figure S3, complete core forest:** `outputs/release_chd_hf/figures/figure3_core_forest.png`
- available vector source in this checkout: `outputs/release_chd_hf/figures/figure3_core_forest.svg`
- collinearity files:
  - `outputs/release_chd_hf/supplement/cvd_single_vs_joint_estimates.csv`
  - `outputs/release_chd_hf/supplement/cvd_exposure_vif.csv`
  - `outputs/release_chd_hf/supplement/cvd_exposure_correlations.csv`
  - **Supplementary Figure S4:** `outputs/release_chd_hf/supplement/figureS1_exposure_correlation.png` (source filename retained; live-pack display number is S4, not S1)

The live-identification ACF PNG is present at `figures/live_identification/figure_C_residual_acf.png`. Live-pack numbering: [`manuscript/live_collaborative/supplement_inventory.md`](../live_collaborative/supplement_inventory.md).

### Caption for the demoted ACF figure

> **Supplementary Figure S1. Residual autocorrelation in two displayed exploratory core models.** Bars show the Pearson residual autocorrelation function for the separate-exposure negative-binomial CHD hot-night and HF cold-day models. Dashed lines mark ±1.96/√132. Lag-1 residual autocorrelation was 0.508 for CHD hot nights and 0.146 for HF cold days. These diagnostics motivate reporting more than one covariance estimator; they do not establish that a particular estimator is correct, protect either contrast from multiplicity, or identify a causal thermal effect. Provenance: `HA_APPROVED_AGGREGATE` residuals from existing fitted core models.

### S4. Full twelve-contrast robustness

Figure 3 in the main paper gives the visual summary. The complete numerical inventory belongs in the supplement:

- **Supplementary Table S2:** `outputs/release_chd_hf/tables/table3_robustness_summary.csv`
- full trend/depletion rows: `outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv`
- lag sensitivities: `outputs/release_chd_hf/supplement/cvd_lag_sensitivity.csv`
- influence sensitivities: `outputs/release_chd_hf/supplement/cvd_influence_sensitivity.csv`
- offset/family/SE combinations: `outputs/release_chd_hf/supplement/cvd_core_robust_estimates.csv`
- unoffset dependence diagnostic: `outputs/release_chd_hf/supplement/cvd_count_timeseries_sensitivity.csv`

The main text should quote the pre-2020 intervals for both displayed exploratory contrasts:

- CHD hot nights: 1.011 (0.991–1.032);
- HF cold days: 1.113 (1.053–1.176).

It should also quote the CHD COVID-phase-adjusted interval, 1.013 (0.994–1.033), because that is the second specification in which the hot-night interval includes 1. These values are already in the claim ledger and existing sensitivity table.

### S5. Weather source lock and provisional HM/CM material

Put the complete source audit in the supplement:

- `outputs/release_chd_hf/supplement/methods_feasibility/weather_definition_source_lock.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/weather_definition_source_validation.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/weather_event_morphology_audit.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/weather_spillover_exposure_build.md`
- `outputs/release_chd_hf/supplement/methods_feasibility/figure_spillover_event_counts.png`
- `outputs/release_chd_hf/supplement/hm_cm_selected_months_audit.csv`
- **Supplementary Figure S5:** `outputs/release_chd_hf/supplement/figureS2_provisional_hm_cm_calendar.png` (source filename retained; published display number changes)
- `outputs/release_chd_hf/supplement/chd_hm_cm_panel_estimates.csv`
- `outputs/release_chd_hf/supplement/hf_hm_cm_panel_estimates.csv`

Label HM/CM estimates provisional and ineligible for a primary claim until the weather co-investigator locks the reference rules. Source reproduction checks do not close that human decision.

### S6. M\|D methods-feasibility gates

Quarantine all synthetic calibration material in the methods supplement:

- `outputs/release_chd_hf/supplement/methods_feasibility/md_pilot_f1_0_failure_note.md`
- `outputs/release_chd_hf/supplement/methods_feasibility/md_pilot_f1_0_gate_summary.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_f1_2_decision_report.md`
- `outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_gate_summary.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/md_calibration_summary.csv`
- `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_type1_by_outcome_kernel.png`
- `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_coverage_by_outcome_kernel.png`
- `outputs/release_chd_hf/supplement/methods_feasibility/figure_calibration_gate_passfail.png`

Every caption must state `SYNTHETIC_CALIBRATION` and “methods validation, not a CHD/HF health finding.” The main paper needs only the refusal and the failed gate classes. It does not need the full gate table.

### S7. Influenza coverage and pollution completeness

These are data-availability diagnostics, not adjusted core results.

**Influenza**

- release evidence: `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv` (P14 rows record `n_months = 121`);
- public exposure dictionary: `outputs/share_for_roro/README.md`;
- monthly public exposure layer: `outputs/share_for_roro/analysis_exposures_monthly_2013_2023.csv`.

Report **121/132 months**, identify the early-2013 gap, and state that missing months were never zero-filled. Do not promote the archive flu coefficient into the main Results.

**Pollution**

- monthly completeness fields: `data_processed/pollution_monthly_2013_2023.csv`;
- panel inventory: `outputs/tables/data_inventory_counts.csv`;
- annual context only: `outputs/tables/pollution_annual_means_general_2013_2023.csv`;
- release archive models: `outputs/release_chd_hf/supplement/combined_pathway_panel_estimates.csv` (P11 rows).

The current release has no standalone, disclosure-minimised pollution-completeness table. Before submission, create a supplement table from the existing public pollution layer that reports, by pollutant, the monthly completeness rule and the number of non-missing eligible months. This is a public-data summary, not a new health model. Do not infer source completeness merely from the P11 model rows having 132 months.

### S8. Scope and provenance firewall

Retain explicit exclusions:

- no stroke result;
- no principal-diagnosis or AMI result;
- no cohort incidence;
- no real daily M\|D coefficient;
- no confounding-adjusted version of the separate core panel;
- no health-economic result; and
- no Gate 3 freeze asserted in the supplement.

## Exact “continuity” replacements in `manuscript/chd_hf_supplement.md`

Line numbers refer to the pre-edit file audited on 15 August 2026. These replacements were applied in this branch.

| Source line | Replace | With |
|---:|---|---|
| 24 | `Complete 12-contrast continuity table` | `Complete 12-contrast core table` |
| 59 | `Thermal exposures used in the continuity panel` | `Thermal exposures used in the core panel` |
| 82 | `Twelve continuity NW6 contrasts` | `Twelve core NW6 contrasts` |
| 89 | `Continuity forest` | `Core forest` |
| 102 | `Separate continuity IDs ... manuscript continuity panel` | `Separate core IDs ... manuscript core panel` |
| 104 | `separate continuity models` | `separate core models` |
| 209 | `continuity-panel exposure` and `continuity slice` | `core-panel exposure` and `core slice` |
| 242 | `days-offset continuity estimates` | `days-offset core estimates` |
| 246 | `Continuity residual ACF` and `continuity exposures` | `Core residual ACF` and `core exposures` |
| 382 | `Confounding-adjusted continuity estimates` | `Confounding-adjusted core estimates` |
