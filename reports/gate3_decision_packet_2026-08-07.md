# Gate 3 decision packet — CHD / HF thermal panel (team freeze pending)

**Date:** 7 August 2026  
**Playbook:** 03  
**Status:** Packet ready — **Gate 3 not closed by agent alone**

## What was run (complete panel)

For each of CHD and HF (`OUTCOME=chd|hf`, `PATHWAY_MODE=real`):

- Pathway registry P01–P18 (17 enabled): 15 OK; P09/P17 skipped (no age×sex); P13 disabled.
- Provisional HM/CM starter flags from `hot_cold_month_registry.yml` via `19b`/`20b` (study-window reference; **not** Hogan-locked).
- Descriptives, offset sensitivity, pre-COVID P02 split, cross-outcome forest.

Orchestrator: `scripts/run_cvd_full_analysis.R`.

## Candidate headline set (proposal only)

| Role | Proposal | Rationale |
|---|---|---|
| Co-primary continuous | P02 (`mean_tmax`, `mean_tmin`) | Pre-registered headline proposal; interpretable |
| Co-primary extremes | P04 (hot nights, very hot days, cold days per 5 days) | Official extreme-day family |
| Cold sensitivity | P08 / P18 | Cold-side symmetry |
| Heat-month sensitivity | Provisional HM19 / HM08 | Night and mean tails; HM23 provisional only |
| Cold-month sensitivity | Provisional CM03 / CM08 | Mean and tmin tails |
| Adjustment ladder | P10, P11, P12, P14 | COVID/holidays, pollution stages, humidity, flu |
| Period | Full 132 mo + P16 pre-COVID | First-event secular decline |

**Do not freeze** from this packet without Hogan / Roro / Bishai / Bob.

## Panel reading (not a primary claim)

All RR from negative-binomial / quasi-Poisson models with month factors and a 4-df time spline; HC1 SEs; ecological C&SD 35+ offset.

### CHD (first hospitalisation after first CHD diagnosis; T2D/HTN cohort)

| Spec | Contrast | RR (95% CI) |
|---|---|---|
| P04 | Hot nights / 5 days | 1.044 (1.012–1.077) |
| P04 | Very hot days / 5 days | 0.971 (0.943–0.999) |
| P04 | Cold days / 5 days | 0.994 (0.955–1.035) |
| P02 | mean_tmax / °C | 0.990 (0.960–1.021) |
| P02 | mean_tmin / °C | 1.003 (0.970–1.038) |
| P05 | Hot-night spell days (≥5) | 1.005 (1.001–1.009) |
| P07 | Heat month mean_temp ≥ p95 | 1.126 (1.054–1.203) |
| P07 | Heat month mean_temp ≥ p97.5 | 0.832 (0.774–0.896) |

Discordance between P07 p95 and p97.5 warns against selecting a single heat-month percentile after seeing results.

### HF (first hospitalisation after first HF diagnosis; T2D/HTN cohort)

| Spec | Contrast | RR (95% CI) |
|---|---|---|
| P04 | Cold days / 5 days | 1.073 (1.011–1.138) |
| P04 | Hot nights / 5 days | 1.012 (0.973–1.052) |
| P02 | mean_tmin / °C | 0.958 (0.919–0.998) |
| P02 | mean_tmax / °C | 1.016 (0.975–1.059) |
| P08 | cold_days (per day) | 1.020 (1.003–1.038) |
| P16 | mean_tmin (pre-COVID) | 0.923 (0.882–0.967) |
| CM03 (provisional) | Cold month mean_temp ≤ p10 | 1.122 (1.023–1.230) |
| CM08 (provisional) | Cold month mean_tmin ≤ p05 | 1.173 (1.049–1.312) |

Qualitative pattern: **CHD more heat-night associated; HF more cold associated** in this panel. That pattern is a panel observation under an open Gate 3, not a frozen finding.

## Required human decisions before headline freeze

1. Confirm inpatient-only ICD inclusion lists for CHD and HF with Roro.
2. Decide whether C&SD ecological rates remain acceptable or whether cohort denominators can be supplied.
3. Hogan: freeze reference period / HM23 operators (Playbook 01).
4. Stroke file arrival and whether stroke remains co-primary.
5. Whether CHD, HF, or a composite is the Laidlaw Stage 3 primary outcome given the stroke delay.
6. How to treat discordant P07 percentile indicators (pre-specify which heat-month definition is confirmatory).

## Outputs index

- Estimates: `outputs/tables/{chd,hf}_pathway_panel_estimates.csv`, `*_hm_cm_panel_estimates.csv`, `combined_pathway_panel_estimates.csv`
- Forests: `outputs/figures/pathway/{chd,hf}_pathway_panel_forest.png`, `cvd_cross_outcome_forest_*.png`
- Sensitivities: `cvd_offset_sensitivity.csv`, `cvd_period_split_P02.csv`
- Receipt: `reports/data_receipt_2026-08-07.md`
