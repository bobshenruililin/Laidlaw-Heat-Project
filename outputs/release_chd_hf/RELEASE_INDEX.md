# CHD/HF release index (augmented)

Disclosure-minimised release package. Analysis of record remains the amended
monthly negative-binomial panel with Newey-West lag-6 intervals.

## Preserved (script 33)

| Artifact | Role |
|---|---|
| `tables/table1_outcome_summary.csv` | Outcome summary |
| `tables/table2_core_models.csv` | Twelve core contrasts |
| `tables/table3_robustness_summary.csv` | Robustness ranges |
| `tables/claim_ledger.csv` | Claim ledger v1 |
| `figures/figure1_indexed_outcome_series.*` | Indexed series |
| `figures/figure2_seasonal_pattern.*` | Seasonality |
| `figures/figure3_core_forest.*` | Core forest |
| `figures/figure4_trend_depletion_sensitivity.*` | Trend/depletion |

## Added (script 38)

| Artifact | Role | Provenance |
|---|---|---|
| `tables/table4_uncertainty_ladder.csv` | SE ladder (12×4) | HA_APPROVED_AGGREGATE |
| `tables/analysis_availability.csv` | Ensemble/prediction/M|D status | blockers or HA |
| `tables/claim_ledger_v2.csv` | Tiered claim ledger | HA_APPROVED_AGGREGATE |
| `figures/figure5_se_method_ladder.*` | SE ladder forest | HA_APPROVED_AGGREGATE |
| `supplement/methods_feasibility/` | Weather + calibration quarantine | mixed; see manifest |

## Methods-feasibility quarantine

`supplement/methods_feasibility/` is the only release location
allowed to carry `SYNTHETIC_CALIBRATION`. Those materials validate methods;
they are not CHD/HF effect evidence.

SYNTHETIC CALIBRATION - METHOD VALIDATION, NOT HEALTH FINDINGS.
