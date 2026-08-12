# Live-manuscript identification figures

**Scope:** diagnostic displays from existing tables only. The script fits no new health model, contains no stroke result, and does not export month-level HA counts.

## Figure A — cold-day identification

- **What it shows:** 141 of 145 cold days occurred in December–February (December 40, January 54, February 47); four occurred in March. With calendar-month indicators, the identifying cold-day variation is between winters across years, not the crude summer–winter contrast.
- **Source:** `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv` (`REAL`, public Hong Kong Observatory Headquarters).
- **Do not claim:** a health effect, a daily lag structure, or that the model compares summer with winter.

## Figure B — first-event depletion and the population contrast

- **What it shows:** CHD annual first-hospitalisation totals changed from 23,830 to 12,323 (-48%), and HF from 4,336 to 2,296 (-47%), while the public population aged 35+ rose by 17%.
- **Sources:** `outputs/tables/cvd_descriptive_annual_totals.csv` and `outputs/release_chd_hf/tables/table1_outcome_summary.csv` (`HA_APPROVED_AGGREGATE`); `data_processed/population_monthly_age_sex_2013_2023.csv` (`REAL`, public C&SD-derived monthly denominators).
- **Do not claim:** incidence, a stable T2D/HTN risk set, or that depletion and pandemic care-seeking uniquely explain the decline. Incidence requires still-at-risk cohort person-time.

## Figure C — residual autocorrelation

- **What it shows:** existing residual ACF(1) is 0.508 for the CHD hot-night contrast and 0.146 for the HF cold-day contrast; CHD has materially stronger serial persistence.
- **Sources:** `outputs/tables/chd_pathway_residual_acf.csv`, `outputs/tables/hf_pathway_residual_acf.csv`, `outputs/release_chd_hf/tables/table2_core_models.csv`, and `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` (existing `HA_APPROVED_AGGREGATE` diagnostics).
- **Do not claim:** that this script fitted a model, that Newey–West uncertainty confirms either thermal association, or that residual ACF establishes causality.

## Files

- `figures/live_identification/figure_A_cold_day_identification.pdf` and `.png`
- `figures/live_identification/figure_B_first_event_depletion.pdf` and `.png`
- `figures/live_identification/figure_C_residual_acf.pdf` and `.png`
- `outputs/live_identification/cold_days_by_month_year.csv`

Figure captions distinguish public environmental/demographic data from approved health aggregates.

## Mapping to the live manuscript (13 August)

| Paper figure | File | Role in Results |
|---|---|---|
| Figure 1 | `figure_B_first_event_depletion.png` | Outcome series: first-event counts vs C&SD 35+ |
| Figure 2 | `figure_A_cold_day_identification.png` | Exposure identification: DJF concentration of official cold days |
| Figure 3 | `figure_C_residual_acf.png` | Why Newey–West is shown for CHD |

Do not paste provisional HM/CM or archive flu/NO₂ coefficients into the paper body.
