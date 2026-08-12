# Claim ledger — live collaborative manuscript (13 August 2026)

Every quantitative sentence in `Heat_CVD_Manuscript_live_update.md` traces to a disclosure-minimised `HA_APPROVED_AGGREGATE` or `REAL` public table, or to a cited paper. No new health models were fitted for this draft. Identification figures reuse existing tables.

| Claim | Display | Source |
|---|---|---|
| CHD events / mean | 156,156; 1,183.0 / month | `outputs/release_chd_hf/tables/table1_outcome_summary.csv` |
| HF events / mean | 29,681; 224.9 / month | same |
| CHD annual 2013 → 2023 | 23,830 → 12,323 | `outputs/tables/cvd_descriptive_annual_totals.csv` |
| HF annual 2013 → 2023 | 4,336 → 2,296 | same |
| 2020 trough | CHD 10,237; HF 1,964 | same |
| C&SD 35+ rise 2013→2023 | 17% (5,188,660 / 4,430,186) | same `mean_population` on CHD rows |
| Seasonal means | CHD Jan 1,386 / Sep 1,097; HF Jan 287 / Sep 196 | `outputs/tables/cvd_descriptive_seasonality_by_month.csv` (rounded) |
| 2013 hot nights vs 1981–2010 normal | 10; about seven days below normal | REAL HKO Year’s Weather 2013 |
| Cold days in DJF | 141 of 145 (Dec 40, Jan 54, Feb 47; Mar 4) | `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv` |
| EPD general-station means | NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 | `outputs/tables/pollution_annual_means_general_2013_2023.csv` |
| Table 2 twelve contrasts | as displayed | `outputs/release_chd_hf/tables/table2_core_models.csv` |
| HF Tmin NW6 upper bound includes 1 | 1.00004966 | table2 `rr_high` |
| Table 3 ladder | as displayed; NW3 CHD hot nights 1.000253–1.043860 | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` |
| All core *q* > 0.19 | min *q* = 0.192 | table2 `q_value_core_bh` |
| Joint CHD hot nights | 1.045 (1.015–1.075) | `cvd_single_vs_joint_estimates.csv` NW6 |
| Joint HF cold days | 1.073 | same |
| VIF Tmax/Tmin | 4.66 | `cvd_exposure_vif.csv` (4.658) |
| VIF hot nights / VHD | ~1.96 | same (1.958) |
| CHD ACF1 | 0.51–0.53 panel; 0.508 for hot nights | `chd_pathway_residual_acf.csv` lag 1, P01A–P04C / P04A |
| HF ACF1 | 0.13–0.18 panel; 0.146 for cold days | `hf_pathway_residual_acf.csv` |
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
| Goggins 2013 AMI | 3.7% per 1 °C below ~24 °C, lags 0–13; no significant heat in three cities | Goggins et al. *Int J Cardiol* 2013;168:243–249 [1] |
| Goggins and Chan 2017 HF | cumulative RR 2.63 (2.43–2.84) for 11 °C vs 25 °C, lags to 23 days; daily public-hospital HF admissions 2002–2011 | Goggins and Chan *Int J Cardiol* 2017;228:537–542 [21] |
| Guo 2024 official HNday28 | no overall association lag 0–4 after mean-temperature adjustment | Guo et al. *Lancet Reg Health West Pac* 2024;51:101168 [17] |
| Guo 2024 extreme HNe | +3.1% (1.5–4.8%) NCNE hospitalisation, 99th pct 28.9 °C·h vs 0 | same [17] |
| Liu 2026 excess deaths | 1,455–3,238 across four heatwave definitions | Liu et al. medRxiv 2026 [13]; complementary mortality, not our ratios |
| Figure 1 | depletion vs 35+ population | `figures/live_identification/figure_B_first_event_depletion.png` from annual totals |
| Figure 2 | cold-day year×month heatmap | `figures/live_identification/figure_A_cold_day_identification.png` from temperature panel |
| Figure 3 | residual ACF | `figures/live_identification/figure_C_residual_acf.png` from pathway ACF tables |

**Not claimed in the paper body.** Stroke coefficients; AMI / principal-diagnosis effects; cohort incidence; daily DLNM lags; Hogan-locked HM/CM confirmatory estimates (`CM08` 1.173, `CM03` 1.122, `HM23` null, `CM05` zero months — Explore only); Gate 3 freeze; CNS-journal suitability; sleep or blood-pressure mediation; numerical equality of 2.63 with 1.073 or of 3.1% with 1.022; 2019 as a health experiment.
