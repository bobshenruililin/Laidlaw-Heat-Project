# Claim ledger — analysis-window sensitivity live manuscript

Every quantitative statement in
`Heat_CVD_Manuscript_live_update.md` traces to a disclosure-minimised
`HA_APPROVED_AGGREGATE` table, a `REAL` public series, or a cited paper. The
manuscript does not report a post-only Model 1 or an exposure-by-period
interaction.

## Outcome and window

| Claim | Display | Source |
|:--|:--|:--|
| Full window | January 2013–December 2023; 132 months | `table1_outcome_summary.csv` |
| Nested window | January 2013–December 2019; 84 months | `cvd_trend_depletion_sensitivity.csv`, `pre_covid` |
| CHD total / mean | 156,156; 1,183.0 per month | `table1_outcome_summary.csv` |
| HF total / mean | 29,681; 224.9 per month | same |
| CHD annual path | 23,830 (2013); 12,396 (2019); 10,237 (2020); 12,323 (2023) | `cvd_descriptive_annual_totals.csv` |
| HF annual path | 4,336 (2013); 2,344 (2019); 1,964 (2020); 2,296 (2023) | same |
| C&SD population aged 35+ | +17%, 2013–2023 | `mean_population` on annual summary |

## Weather context

| Period | Mean temperature | Hot nights / month | Very hot days / month | Cold days / month | Source |
|:--|--:|--:|--:|--:|:--|
| 2013–2019 | 23.83 °C | 2.74 | 2.55 | 1.12 | HKO monthly panel; cross-check `cvd_descriptive_covid_era_means.csv` |
| 2020–2022 | 24.30 °C | 4.53 | 4.25 | 1.03 | same |
| 2023 | 24.50 °C | 4.67 | 4.50 | 1.17 | same |

Of 145 official cold days, 141 fell in December–February. Twenty-nine of 132
months carried at least one cold day. Source:
`outputs/live_identification/cold_days_by_month_year.csv` (`REAL`).

## Nested-window official-day panel

All estimates below use Newey–West lag-6 intervals. The five-day contrast is a
reporting scale, not consecutive duration.

| Outcome | Exposure | Full window | Nested pre-2020 window |
|:--|:--|--:|--:|
| CHD | Hot nights / 5 | 1.022 (1.002–1.042) | 1.011 (0.991–1.032) |
| CHD | Very hot days / 5 | 0.999 (0.974–1.025) | 0.997 (0.982–1.012) |
| CHD | Cold days / 5 | 0.995 (0.949–1.043) | 1.036 (1.007–1.067) |
| HF | Hot nights / 5 | 1.003 (0.976–1.031) | 0.965 (0.937–0.994) |
| HF | Very hot days / 5 | 0.995 (0.963–1.028) | 0.990 (0.960–1.021) |
| HF | Cold days / 5 | 1.073 (1.006–1.144) | 1.113 (1.053–1.176) |

Source: `outputs/tables/cvd_trend_depletion_sensitivity.csv`. The intervals
for each full/nested pair overlap. No contrast of the coefficients was fitted.
COVID-phase-adjusted rows shown in the body are CHD hot nights 1.013
(0.994–1.033) and HF cold days 1.074 (1.006–1.145), from the same table.

## Complete panel and uncertainty

The full twelve-fit panel is
`outputs/release_chd_hf/tables/table2_core_models.csv`. All twelve
Benjamini–Hochberg *q*-values exceed 0.19; minimum *q* = 0.192.

Main Table 3 draws four rows from
`outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`:

| Contrast | Model | HC1 | NW3 | NW6 |
|:--|--:|--:|--:|--:|
| CHD hot nights / 5 | 1.022 (0.995–1.049) | 1.022 (0.997–1.047) | 1.022 (1.000–1.044) | 1.022 (1.002–1.042) |
| HF mean temperature / °C | 0.974 (0.956–0.993) | 0.974 (0.949–1.000) | 0.974 (0.949–1.001) | 0.974 (0.947–1.002) |
| HF mean minimum temperature / °C | 0.973 (0.956–0.991) | 0.973 (0.950–0.997) | 0.973 (0.948–0.999) | 0.973 (0.947–1.000) |
| HF cold days / 5 | 1.073 (1.023–1.125) | 1.073 (1.011–1.138) | 1.073 (1.007–1.143) | 1.073 (1.006–1.144) |

Pre-2020 mean-temperature rows are CHD 0.980 (0.970–0.990) and HF 0.945
(0.927–0.963). Nine of twelve pre-2020 intervals exclude 1, including all six
continuous-temperature rows. Source:
`outputs/release_chd_hf/supplement/cvd_trend_depletion_sensitivity.csv`.

## Diagnostics

| Claim | Display | Source |
|:--|:--|:--|
| CHD hot-night lag-1 ACF | 0.508 | `chd_pathway_residual_acf.csv`, P04A |
| HF cold-day lag-1 ACF | 0.146 | `hf_pathway_residual_acf.csv`, P04B |
| CHD Model 1 Ljung–Box lag 6 | *p* < 10^−7^ for all six | `chd_pathway_core_diagnostics.csv` |
| HF Model 1 Ljung–Box lag 6 | *p* > 0.3 for all six | `hf_pathway_core_diagnostics.csv` |
| Trend/window/COVID range | CHD hot nights 1.011–1.025; HF cold days 1.043–1.113 | `cvd_trend_depletion_sensitivity.csv` |
| Most influential months | CHD February 2020; HF cold February 2022 | `cvd_influence_sensitivity.csv` |
| Excluding influence month | CHD 1.021 (1.001–1.040); HF 1.088 (1.034–1.144) | same |

## Supplement and provenance

- Supplementary Table S1: complete four-construction ladder.
- Supplementary Table S2 and Figure S6: nested-window panel.
- Supplementary Tables S3–S6: lag, influence, collinearity, and residual
  diagnostics.
- Supplementary Table S7: archive influenza model, 121 months, not core
  adjusted.
- Supplementary Table S8: `SYNTHETIC_CALIBRATION` methods refusal, not a
  health finding.
- Supplementary Table S9: archive pollution models with joint Tmax/Tmin and a
  population × days offset, not core adjusted.
- Supplementary Table S10: public HKO weather summaries by period.

## Cited neighbours

Xin, Wai (two papers), Hung, and Tam are utilisation, mortality, survey, and
delay neighbours. Their counts are not imported into manuscript tables.
Cowling documents influenza suppression. Xie concerns post-acute
cardiovascular harm. Wan concerns vaccination and cardiovascular outcomes
after documented infection. None is a physiological result from this panel.

## Not claimed

No health improvement; protective cold-day effect; tested pre/post difference;
post-only Model 1; cohort incidence; admission-cause effect; daily trigger;
consecutive-duration threshold; antibody mechanism; laboratory result; stroke
coefficient; Gate 3 freeze; or warning-system evaluation.

Machine sibling: `claim_ledger.yml`.
