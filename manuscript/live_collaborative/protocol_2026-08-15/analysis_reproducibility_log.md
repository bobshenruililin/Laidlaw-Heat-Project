# Analysis / reproducibility log — 15 August 2026

**Label for this session:** no new health model. Reproduction from **already-written** release tables and public climate files.

## Environment

- Analysis panels: **absent**. `data_processed/*_analysis_panel.csv` not on disk (`PARKED_NO_PANEL` / A60).
- Consequence: cannot re-run `scripts/run_cvd_full_analysis.R` against monthly counts. Do not reconstruct monthly CHD/HF from annual totals.
- Software claimed in the live Methods (R 4.3.3; MASS 7.3-60.0.1; sandwich 3.1.3) is the 12 August session record. This session did not re-execute those models.

## Checks run this session

| Check | Command / method | Result |
|---|---|---|
| Table 2 vs live markdown | Python compare of `table2_core_models.csv` display, rounded *p*, rounded *q* | 12/12 match |
| Table 3 vs `table4_uncertainty_ladder.csv` | Manual/CSV | CHD HN and HF CD four constructions match |
| Robustness ranges | `table3_robustness_summary.csv` | CHD HN 1.011–1.025; HF CD 1.043–1.113 |
| Hot nights July 2013 / 2022 | `hot_nights_by_month_year.csv` | 1 and 25; Jun–Sep every month ≥1 in 2013–2023 |
| Cold-day month split | `temperature_monthly_panel_2013_2023.csv` | 145 total; 141 DJF; 4 March |
| HKO yearbook lock | `hko_annual_extremes_validation.csv` | 33/33 MATCH |
| Pollution rounding | `pollution_annual_means_general_2013_2023.csv` | 1 d.p. display matches |
| ERA5 bridge | `monthly_station_grid_bridge.json` | r 0.9861; slopes 1.0324 and 0.0453 (SE 0.0074); 57 vs 9 |
| Flu archive | `combined_pathway_panel_estimates.csv` P14 | 1.673 (1.249–2.243), n=121, offset `population_x_days` |
| Medication | grep + variable dictionary | **absent** |
| `scripts/check_opus_register_pass.py` | existing checker on superseded `opus_hogan_register_pass.md` | Headline estimates ok; FAIL on token `9,10` (citation cluster parsed as a number). Not a live-file defect. |

## Analysis labels (protocol §6)

| Object | Label |
|---|---|
| Twelve-contrast NB panel, days offset, NW6 reporting | originally specified after outcomes were available → **exploratory** (stated in Methods) |
| Model/HC1/NW3/NW6 ladder | originally specified robustness display |
| Pollution/flu archive models | exploratory; **not** adjusted core |
| Daily-recovery simulation | prespecified extension; **failed**; no real daily coefficient |
| Identification figures 1–4 | originally specified descriptives from existing tables; no new health model |
| 15 Aug manuscript wording (ozone, competing interest, flu offset, working title) | necessary correction of prose / declaration honesty |

## Discrepancy log

None between live Table 2/3 and release CSVs.

One honesty gap closed this session: Discussion previously quoted archive influenza 1.673 without stating that P14 used `population_x_days`, not the core days-in-month offset.
