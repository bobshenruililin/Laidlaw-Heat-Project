# First-Stage Exploratory Report

**Project:** Thermal extremes, aging, pollution, and cardiovascular hospital burden in Hong Kong, 2013–2023  
**Date:** 2026-07-10  
**Audience:** Professor Bishai, Bob, Hogan, Roro  

> **Hospital Authority outcome data were not available for this first-stage report; all outcome-modeling demonstrations use synthetic data only.**

---

## Executive Summary

This first-stage report converts a broad climate-health idea into an auditable analysis plan and executable public-data pipeline. We successfully built monthly HKO thermal-extreme exposures for January 2013–December 2023 (with optional 2024), including hot nights, very hot days, extremely hot days, cold days, and spell-length metrics. Annual hot-night and very-hot-day counts rose markedly in 2019–2023 relative to 2013–2018, while cold days remained variable. Pollution and official C&SD denominators still require manual deposits from Hogan and Bob; placeholders/scaffolds are clearly labeled. A synthetic Negative Binomial workflow confirms offsets, strata, interactions, diagnostics, and table/figure generation. No substantive hospital-association claims are made.

**Recommended framing:** reassessment of cold and heat burden under contemporary warming, aging, and pollution change — not “prove heat replaced cold.”

---

## 1. Project Background

### 1.1 Original motivation

The project began as a retrospective ecological time-series of temperature and cardiovascular admissions in Hong Kong using monthly Hospital Authority data (2013–2023), stratified by age, sex, and diagnosis.

### 1.2 Historical Hong Kong evidence

Older daily studies by Goggins and colleagues found strong cold-related associations for AMI, increased ischemic stroke risk at cooler temperatures (especially older adults), seasonality in hemorrhagic stroke, little or no significant heat effect in earlier periods, and important NO2 associations in AMI work. Related subtropical winter-excess literature supports continued attention to cold-related cardiovascular burden. See `memos/literature_baseline.md`.

### 1.3 Why 2013–2023 is scientifically useful

The decade spans warming and more frequent hot nights/very hot days; growth in older age groups (especially 65–69 and 70–74); changing pollution after the Clean Air Plan (NO2/PM declines; O3 concern); and COVID-era utilization disruption. It therefore supports a contemporary reassessment of the weather–CVD hospitalization profile.

### 1.4 Why monthly data are acceptable but limited

Monthly studies can be publishable for broad seasonal and multi-day burden questions, but aggregation blunts acute short-lag heat effects. Therefore this project:

- does not rely only on monthly mean temperature;
- derives monthly counts of extreme days/nights from daily data;
- includes spell-length metrics;
- interprets null heat findings cautiously.

---

## 2. Refined Research Questions

### Primary

1. Are monthly counts of hot nights, very hot days, extremely hot days, and cold days associated with CVD admission rates among Hong Kong residents aged 35+ (2013–2023)?
2. Do associations differ for AMI, ischemic stroke, and hemorrhagic stroke?
3. Are associations stronger in older groups (65–69, 70–74, 75–84, 85+)?
4. Does the recent period show weaker, similar, or stronger cold-related burden relative to historical Hong Kong findings (**qualitative unless methods are harmonized**)?
5. Are heat metrics — especially hot nights — more informative than monthly mean temperature?

### Secondary

1. How have thermal extremes changed from 2013–2023?
2. How have population denominators shifted by age, especially older adults?
3. How have NO2, O3, PM2.5, and PM10 changed?
4. Are heat effects confounded or modified by pollution, especially ozone?
5. How much did COVID disrupt admissions in 2020–2022?
6. Would adding 2024 materially improve exposure contrast?

---

## 3. Data Inventory

### 3.1 Hospital Authority data status

**Not available.** Secure placeholder directory: `data_raw/ha_secure_placeholder/`. Request memo: `memos/data_request_roro.md`.

### 3.2 Weather data

| Item | Status |
|---|---|
| HKO dailyExtract 2012–2024 | Downloaded |
| Open-data Tmean/Tmax/Tmin | Downloaded |
| Monthly extremes 2013–2023 | **Built** (`data_processed/climate_monthly_2013_2023.csv`) |
| Optional 2024 monthly file | Built (`climate_monthly_2013_2024.csv`) |

### 3.3 Pollution data

EPIC portal confirmed; real station files not yet deposited. Current file is a **PLACEHOLDER** for pipeline testing (`pollution_monthly_2013_2023.csv` with `data_status` flag). Instructions: `data_raw/epd/README_manual_download.md`. Memo: `memos/environmental_data_request_hogan.md`.

### 3.4 Population data

C&SD Table 110-01002 preferred; interactive API `param` required. Current denominators are a **SYNTHETIC_DENOMINATOR** scaffold for workflow testing. Import instructions: `data_raw/csd_population/README_manual_download.md`.

### 3.5 Influenza / COVID / holidays

COVID phases implemented in `config.yml` and `confounders_monthly_2013_2023.csv`. Holiday calendar is provisional scaffold. Flu indicator not yet loaded (CHP import path prepared).

---

## 4. Exposure Construction Plan

### 4.1 HKO definitions

As above (hot night ≥28°C Tmin; VHD ≥33°C Tmax; extremely hot ≥35°C Tmax; cold ≤12°C Tmin).

### 4.2 Hot nights and heat spells

Primary heat metric: monthly hot-night count. Also constructed:

- longest within-month hot-night run;
- max full hot-night spell touching the month (cross-boundary aware);
- days in spells of ≥3 hot nights;
- analogous very-hot-day spell metrics.

### 4.3 Cold days

Co-primary thermal exposure. Cold days concentrate in winter months; month fixed effects remain appropriate.

### 4.4 Humidity and wet heat

Daily RH and dew point available from dailyExtract; monthly means constructed. Wet-bulb / heat index deferred to Hogan if temporally aligned inputs are confirmed.

### Observed descriptive pattern (real weather)

Hot nights and very hot days were substantially higher in 2019–2023 than 2013–2018. Extremely hot days were rare until recent years (notably 15 in 2022). Cold days fluctuated (range 1–21). Figures: `outputs/figures/fig01_annual_thermal_extremes.png`, `fig02_monthly_temp_hot_nights.png`.

**Collinearity note:** hot nights, very hot days, and mean temperature are correlated (`outputs/tables/weather_exposure_correlations.csv`). Primary models should not include all heat metrics simultaneously.

---

## 5. Population Aging and Denominator Plan

Preferred age groups include separated **65–69** and **70–74**. Offset:

```text
log(age-sex population × days in month)
```

Monthly populations via linear interpolation between mid-year estimates (calendar-year assignment as sensitivity). Align population universe with HA residency definitions; consider FDH-excluded table as sensitivity.

**Current status:** synthetic scaffold only — do not interpret aging percentages as official until C&SD file is imported.

---

## 6. Pollution Plan

### 6.1–6.3 NO2, O3, PM2.5, PM10

Primary: general stations; roadside sensitivity only. Station-month valid if ≥75% expected observations. Prefer unweighted mean of valid general stations + balanced-panel sensitivity. Seek monthly mean O3 and peak-oriented MDA8-style metric.

### 6.4 Staged adjustment strategy

1. No pollutant (total thermal association)  
2. NO2 only  
3. PM2.5 only  
4. O3 only  
5. O3 × hot nights  
6. Multi-pollutant sensitivity  

Treat O3 cautiously as potential confounder, modifier, or pathway variable.

---

## 7. Outcome Definition Plan

### 7.1–7.3 Diagnosis groups

Provisional ICD-9-CM / ICD-10 definitions in assumption ledger and Roro memo. Confirm coding system before final algorithms. Sensitivity around `436` / `I64` and hemorrhagic `432.x`.

### 7.4 ED/inpatient distinction

Primary: inpatient (prefer emergency/unplanned). ED separate unless mutually exclusive ED-only records exist.

### 7.5 Episode definition

Combine transfers where feasible; retain true readmissions. Month = admission/presentation month.

---

## 8. Statistical Analysis Plan

### 8.1 Descriptive analysis

Weather (done), pollution (pending real data), population (pending real data), admissions (pending HA).

### 8.2 Main model

Negative Binomial default:

```r
n_events ~ I(hot_nights/5) + I(cold_days/5) + age_group + sex + diagnosis_group +
  factor(month) + ns(time_index, df=4) + covid_phase + offset(offset_log)
```

Report RR per 5 hot nights / 5 cold days / 5 VHD / 1°C mean Tmin.

### 8.3 Interactions

Fit separately: heat/cold × age; heat/cold × diagnosis; O3 × hot nights.

### 8.4 Sensitivity analyses

Poisson/quasi-Poisson; exclude 2020–2022; pre-COVID; lag-1; alternative metrics; seasonality alternatives; pollutant staging; age/diagnosis alternatives; ED vs inpatient; optional 2024.

### 8.5 Autocorrelation and overdispersion

Pipeline includes Pearson dispersion, NB theta, ACF/PACF of monthly mean residuals, Durbin–Watson-style summary, and clustered SE scaffold. On real HA data, persist with GEE/GLARMA if needed.

**Design reminder:** 132 monthly weather observations; expanding strata does not create independent exposure months.

---

## 9. Synthetic Pipeline Demonstration

**SYNTHETIC ONLY — not substantive findings.**

Executable pipeline (`scripts/00_setup.R` … `13_make_report_outputs.R`) produced:

| Output | Path |
|---|---|
| Analysis panel | `data_processed/synthetic_analysis_panel.csv` (8,712 rows) |
| Model results | `outputs/tables/synthetic_model_results.csv` |
| Diagnostics | `outputs/figures/synthetic_diagnostic_plots/` |
| Model objects | `outputs/model_objects/synthetic_models.rds` |

The synthetic DGP intentionally embeds a stronger cold than heat signal to test recovery of expected directions under the planned model. **Do not cite these coefficients as epidemiologic results.**

Workflow checks passed: unique month-age-sex-diagnosis keys; full 2013–2023 month coverage; population non-missing; extreme counts within 0–days_in_month; SYNTHETIC label enforced before modeling.

---

## 10. Risks and Mitigation

### 10.1 Monthly aggregation

May attenuate short-lag heat effects → use extreme-day/spell metrics; interpret null heat cautiously; consider future daily analysis if data allow.

### 10.2 Small-cell suppression

Never code suppressed as zero; request coarser strata if needed.

### 10.3 COVID disruption

Phase indicators + exclude 2020–2022 + request all-cause utilization series.

### 10.4 Pollution collinearity / pathway issues

Staged models; separate total vs adjusted thermal associations.

### 10.5 Ecological inference limits

Population-level associations only; no individual causal claims.

### Additional top risks

- Only 132 exposure months  
- Outcome-definition uncertainty (coding, transfers, elective vs emergency, ED overlap)  
- Single-station weather representativeness  
- Historical coefficient comparison invalid without harmonization  

---

## 11. Immediate Next Steps

1. **Roro:** fulfill / negotiate HA extract per `memos/data_request_roro.md`.  
2. **Hogan:** deposit EPD general-station files; review weather station/spell choices.  
3. **Bob:** download C&SD age-sex population CSV; re-run scripts 05+.  
4. **Team:** confirm assumption ledger checklist (period, 2024, coding, age bands, stations, COVID, flu).  
5. After real denominators + pollution: refresh descriptive report sections.  
6. After HA data: swap synthetic outcomes for real extract inside secure environment; re-run models.  
7. Keep 2024 optional; do not delay core 2013–2023 analysis.

---

## Appendix A: Assumption Ledger

See `analysis_plan/assumption_ledger.md`.

## Appendix B: Data Request to Roro

See `memos/data_request_roro.md`.

## Appendix C: Environmental Request to Hogan

See `memos/environmental_data_request_hogan.md`.

## Appendix D: Variable Dictionary

See `data_processed/variable_dictionary.csv`.

## Appendix E: Key file map

```text
reports/initial_exploration_note.md
reports/first_stage_exploratory_report.md
analysis_plan/assumption_ledger.md
memos/{data_request_roro,environmental_data_request_hogan,literature_baseline}.md
manuscript/methods_draft.md
data_processed/climate_monthly_2013_2023.csv          # REAL HKO-derived
data_processed/pollution_monthly_2013_2023.csv        # PLACEHOLDER until EPIC import
data_processed/population_monthly_age_sex_2013_2023.csv  # SYNTHETIC until C&SD import
data_processed/synthetic_analysis_panel.csv           # SYNTHETIC outcomes
scripts/00_setup.R … 13_make_report_outputs.R
outputs/tables/weather_annual_extremes_2013_2023.csv
outputs/figures/fig01_annual_thermal_extremes.png
```
