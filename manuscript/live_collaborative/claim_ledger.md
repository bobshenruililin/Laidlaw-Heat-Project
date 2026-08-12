# Claim ledger — live collaborative manuscript (12 August 2026)

Every quantitative sentence in `Heat_CVD_Manuscript_live_update.md` traces to a disclosure-minimised `HA_APPROVED_AGGREGATE` or `REAL` public table. No new models were fitted for this draft.

| Claim | Display | Source |
|---|---|---|
| CHD events / mean | 156,156; 1,183.0 / month | `outputs/release_chd_hf/tables/table1_outcome_summary.csv` |
| HF events / mean | 29,681; 224.9 / month | same |
| CHD annual 2013 → 2023 | 23,830 → 12,323 | `outputs/tables/cvd_descriptive_annual_totals.csv` |
| HF annual 2013 → 2023 | 4,336 → 2,296 | same |
| 2020 trough | CHD 10,237; HF 1,964 | same |
| Seasonal means | CHD Jan 1,386 / Sep 1,097; HF Jan 287 / Sep 196 | `outputs/tables/cvd_descriptive_seasonality_by_month.csv` (rounded) |
| Hot nights / VHD / cold days | 10/17/14 (2013); 61/54/13 (2021); 56/54/14 (2023); cold days 1 in 2019 | `outputs/tables/hko_annual_extremes_2013_2023.csv` |
| EPD general-station means | NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 | `outputs/tables/pollution_annual_means_general_2013_2023.csv` |
| Table 2 twelve contrasts | as displayed | `outputs/release_chd_hf/tables/table2_core_models.csv` |
| HF Tmin NW6 upper bound includes 1 | 1.00004966 | table2 `rr_high` |
| Table 3 ladder | as displayed; NW3 CHD hot nights 1.000253–1.043860 | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` |
| All core *q* > 0.19 | min *q* = 0.192 | table2 `q_value_core_bh` |
| Joint CHD hot nights | 1.045 (1.015–1.075) | `cvd_single_vs_joint_estimates.csv` NW6 |
| Joint HF cold days | 1.073 | same |
| VIF Tmax/Tmin | 4.66 | `cvd_exposure_vif.csv` (4.658) |
| VIF hot nights / VHD | ~1.96 | same (1.958) |
| CHD ACF1 | 0.51–0.53 | `chd_pathway_residual_acf.csv` lag 1, P01A–P04C |
| HF ACF1 | 0.13–0.18 | `hf_pathway_residual_acf.csv` |
| Ljung–Box lag 6 | CHD *p* < 10⁻⁸; HF *p* > 0.3 | `*_pathway_core_diagnostics.csv` |
| Trend range CHD hot nights | 1.011–1.025 | `table3_robustness_summary.csv` |
| Trend range HF cold days | 1.043–1.113 | same |
| HF cold pre-2020 | 1.113 (1.053–1.176) | `cvd_trend_depletion_sensitivity.csv` `pre_covid` |
| CHD hot nights lag 1 | 1.010 (0.979–1.042) | `cvd_lag_sensitivity.csv` |
| HF cold lag 1 / lag 2 | 1.073 (1.014–1.135); 1.053 (0.985–1.127) | same |
| Influence months | CHD 2020-02; HF cold 2022-02 | `cvd_influence_sensitivity.csv` |
| After max Cook | CHD 1.021 (1.001–1.040); HF 1.088 (1.034–1.144) | same |
| M\|D gates | Type I 0.048–0.150; coverage 0.840; rel. bias 32.8; false-sign 0.808 | `md_calibration_gate_summary.csv` |
| Flu coverage | 121/132 | CHP layer; P14 n_months |
| Archive flu CHD | 1.673 (1.249–2.243) on 121 months | `combined_pathway_panel_estimates.csv` P14; **not** continuity-adjusted |
| Software | R 4.3.3; MASS 7.3-60.0.1; sandwich 3.1.3 | session on 12 Aug 2026 |

**Not claimed.** Stroke coefficients; AMI / principal-diagnosis effects; cohort incidence; daily DLNM lags; Hogan-locked HM/CM confirmatory estimates; Gate 3 freeze; CNS-journal suitability.
