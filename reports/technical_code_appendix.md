# Technical Code Appendix

**Audience:** Bob, Hogan, Roro, technical reviewers  
**Date:** 10 July 2026  
**Not for the main email body**

---

## 1. Script-by-script description

| Script | Purpose | Input | Output | Data type | Verified? | Notes |
|---|---|---|---|---|---|---|
| `00_setup.R` | Create folders; install/load packages; record session | `config.yml` | `outputs/session_info_setup.txt` | N/A | Yes | Uses user R library path |
| `01_download_or_import_weather.R` | Download HKO dailyExtract + open-data temp CSVs | HKO URLs | `data_raw/hko/...`; source manifest | Real public | Yes | Skips existing files; does not overwrite |
| `02_build_weather_monthly.R` | Build daily/monthly extremes and spells | dailyExtract XML/JSON | `climate_daily_hko.csv`; `climate_monthly_2013_2023.csv`; annual table | Real | Yes | Official HKO thresholds |
| `03_download_or_import_pollution.R` | Document EPIC download; import CSVs or write placeholder | Manual EPIC CSVs or none | `data_raw/epd/...` | Placeholder if no CSV | Yes | Currently placeholder |
| `04_build_pollution_monthly.R` | Aggregate pollution to monthly file | EPD raw/placeholder | `pollution_monthly_2013_2023.csv` | Placeholder | Yes | Flexible parser for future real files |
| `05_build_population_denominators.R` | Import C&SD or build synthetic denominators | C&SD CSV or none | `population_monthly_age_sex_2013_2023.csv` | Synthetic now | Yes | Replace before rate inference |
| `06_build_confounders.R` | COVID phases, holiday scaffold, flu slot | `config.yml`; optional CHP CSV | `confounders_monthly_2013_2023.csv` | Mixed/provisional | Yes | Holiday calendar provisional |
| `07_simulate_ha_outcomes.R` | Create synthetic HA-like counts | Climate + pop + confounders | `synthetic_ha_outcomes.csv` | Synthetic | Yes | Planted cold > heat signal |
| `08_merge_analysis_panel.R` | Merge analysis panel; QC; dictionary | Outcomes + exposures | `synthetic_analysis_panel.csv`; variable dictionary | Synthetic outcomes + real climate + placeholder pollution + synthetic pop | Yes | Enforces SYNTHETIC label |
| `09_descriptive_tables.R` | Descriptive tables | Processed files | `outputs/tables/*` | Mixed; synthetic tables labeled | Yes | |
| `10_descriptive_figures.R` | Figures | Processed files | `outputs/figures/*` | Fig1–2 real weather; Fig3–4 placeholder/synthetic | Yes | Captions note data type |
| `11_fit_main_models_synthetic.R` | Fit NB/Poisson templates | Synthetic panel | `synthetic_model_results.csv`; model RDS | Synthetic | Yes | Stops if not SYNTHETIC |
| `12_model_diagnostics.R` | Residuals, ACF/PACF | Synthetic models | diagnostic plots + summary | Synthetic | Yes | |
| `13_make_report_outputs.R` | Table shells; pipeline status | Prior outputs | `outputs/table_shells/`; status | N/A | Yes | |
| `run_pipeline.R` | Run 00–13 in order | All | All | Mixed | Yes | Stops on first failure |
| `utils.R` | Shared helpers | — | — | N/A | Yes | Config, month grid, spell run, labels |

## 2. Dependency map

```text
01 weather download → 02 weather monthly ─┐
03 pollution import → 04 pollution monthly ─┼→ 08 merge ← 07 synthetic outcomes
05 population ─────────────────────────────┤         ↑
06 confounders ────────────────────────────┘         │
                                                     │
05 + 02 + 06 ──────────────────────────────────────→ 07
08 → 09 tables / 10 figures / 11 models → 12 diagnostics → 13 report outputs
```

## 3. Dataset labels (authoritative)

| File | Label | May support substantive CVD claims? |
|---|---|---|
| `climate_monthly_2013_2023.csv` | Real HKO-derived | Descriptive climate claims only |
| `climate_monthly_2013_2024.csv` | Real HKO-derived | Descriptive; optional extension |
| `pollution_monthly_2013_2023.csv` | `PLACEHOLDER_NOT_FOR_INFERENCE` | No |
| `population_monthly_age_sex_2013_2023.csv` | `SYNTHETIC_DENOMINATOR` | No |
| `synthetic_analysis_panel.csv` | `SYNTHETIC` | No |
| `outputs/tables/synthetic_model_results.csv` | `SYNTHETIC` | No |

## 4. Model formulas (as coded for synthetic testing)

Primary NB:

```r
n_events ~ I(hot_nights/5) + I(cold_days/5) + age_group + sex + diagnosis_group +
  factor(month) + ns(time_index, df = 4) + covid_phase + offset(offset_log)
```

Alternative heat: replace hot nights with very hot days.  
Continuous: `mean_tmin` instead of extreme counts.  
Interactions: hot/cold × age; hot/cold × diagnosis; O3 × hot nights (staged).

Preferred offset:

```text
offset_log = log(population × days_in_month)
```

## 5. Diagnostics recorded (synthetic run)

| Check | Result (synthetic) | Interpretation |
|---|---|---|
| Poisson Pearson dispersion | ≈ 57.1 | Overdispersion; NB preferred in this example |
| NB theta | ≈ 12.2 | Converged |
| NB converged | TRUE | OK for workflow |
| Durbin–Watson on monthly mean residuals | ≈ 2.35 | Check ACF/PACF on real data |
| Duplicate panel keys | 0 | Pass |
| Month coverage | 132 / 132 | Pass |

## 6. Warnings / limitations known in code

- C&SD API requires interactive encrypted `param`; manual CSV import is the practical path.
- EPD EPIC is interactive; no automated bulk download in current scripts.
- Holiday calendar is a provisional scaffold, not an official holiday file.
- Flu indicator is NA until CHP file is supplied.
- Pollution parser is flexible but station-completeness rules still need Hogan’s finalized station file.
- Two-way clustered SE via `sandwich::vcovCL` is attempted; fallback to HC1 if clustering fails.
- Synthetic DGP intentionally embeds effects; recovery is not scientific confirmation.
- Effective exposure sample size remains 132 months even when the panel has thousands of rows.

## 7. How to replace synthetic data with HA data

1. Place approved aggregate HA extract in the secure environment (not ordinary email unless Roro confirms).
2. Confirm columns against `memos/data_request_roro.md` and `variable_dictionary.csv`.
3. Write an import script analogous to `07_`, but reading real HA data and setting `data_status = "HA_AGGREGATE"`.
4. Bypass or gate `stop_if_not_synthetic()` for real-data modeling scripts (create parallel `11_fit_main_models_ha.R`).
5. Replace synthetic population and pollution files first so rates and staged pollutant models are meaningful.
6. Re-run QC: uniqueness, month coverage, suppression handling (never code suppressed as zero).
7. Freeze pre-analysis plan before inspecting outcome–exposure associations.

## 8. Secure-server readiness checklist

- [ ] Roro confirms whether code may be transferred into the HA/secure environment  
- [ ] List of available R packages on secure server obtained  
- [ ] Aggregate-only extract specification approved  
- [ ] Small-cell suppression and complementary suppression rules documented  
- [ ] Output-vetting process documented  
- [ ] Approved channel for any export of tables/figures confirmed  
- [ ] No patient-level or re-identifying fields requested  
- [ ] Local repo remains free of real HA extracts  

## 9. Pipeline re-run instructions

```bash
export R_LIBS_USER="$HOME/R/library"
cd /path/to/Laidlaw-Heat-Project
Rscript scripts/run_pipeline.R
```

After depositing real C&SD/EPD files into `data_raw/`, re-run from the relevant script number rather than relying on placeholders.

## 10. Repository audit table (verification used for this package)

| Item | Claimed status | Verified status | Evidence/file | Issue or action |
|---|---|---|---|---|
| Full scaffold | Built | Present | README + folders | OK |
| Scripts 00–13 | Built | 16 R files including utils/runner | `scripts/` | OK |
| HKO 2013–2023 monthly | Real processed | 132 months; completeness 1.0 | `climate_monthly_2013_2023.csv` | Confirm station choice |
| HKO annual extremes | Match official summaries | Counts verified in annual table | `weather_annual_extremes_2013_2023.csv` | OK for descriptive use |
| 2024 extract | Available | 12 months; 50/52/2/11 extremes | `climate_monthly_2013_2024.csv` | Optional |
| Pollution | Placeholder | Label verified | `pollution_monthly_*.csv` | Hogan deposit needed |
| Population | Synthetic | Label verified | `population_monthly_*.csv` | Bob C&SD download needed |
| HA outcomes | Synthetic | Label verified | `synthetic_analysis_panel.csv` | Blocked on Roro |
| Synthetic models | Workflow only | Labeled; NB converged | `synthetic_model_results.csv` | Do not cite as findings |
| PR #1 | Draft exists | Confirmed via `gh pr view` | GitHub PR #1 | Link in email |
| Confidential HA in git | None | Placeholder README only | `ha_secure_placeholder/` | Keep clean |
