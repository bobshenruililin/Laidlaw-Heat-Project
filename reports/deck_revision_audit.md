# Deck revision audit — Lab meeting 17 July 2026

**Revised deck:** `reports/latex/lab_meeting_2026-07-17_revised.tex` → `reports/Lab_Meeting_2026-07-17_revised.pdf`  
**Original preserved:** `reports/latex/lab_meeting_2026-07-17.tex` → `reports/Lab_Meeting_2026-07-17.pdf`  
**Auditor:** Bob Shen (revision pass)  
**Date:** 12 July 2026

## Scope

Every numerical statement in the revised main deck and appendix is listed below with source and verification status. Non-numerical design statements are listed only when they claim a confirmation status.

## Numerical statements

| Statement in revised deck | Value shown | Source file(s) | Computation / check | Verified? |
|---|---|---|---|---|
| Study months N | 132 | `data_processed/climate_monthly_2013_2023.csv` | `len(rows) == 132`; month_id `2013-01` … `2023-12` | **Verified** |
| Mean temperature mean | 24.02 °C | same | `mean(mean_temp) = 24.018046` → 24.02 | **Verified** |
| Mean temperature SD | 4.70 | same | sample SD = 4.698265 → 4.70 | **Verified** |
| Mean Tmin mean | 22.10 °C | same | 22.104444 → 22.10 | **Verified** |
| Mean Tmin SD | 4.69 | same | 4.691418 → 4.69 | **Verified** |
| Mean Tmax mean | 26.66 °C | same | 26.663841 → 26.66 | **Verified** |
| Mean Tmax SD | 4.82 | same | 4.819647 → 4.82 | **Verified** |
| Hot nights mean | 3.40 days/month | same | 3.401515 → 3.40 | **Verified** |
| Hot nights SD | 5.40 | same | 5.399830 → 5.40 | **Verified** |
| Cold days mean | 1.10 days/month | same | 1.098485 → 1.10 | **Verified** |
| Cold days SD | 2.55 | same | 2.552831 → 2.55 | **Verified** |
| Very hot days mean | 3.19 days/month | same | 3.189394 → 3.19 | **Verified** |
| Very hot days SD | 5.18 | same | 5.177952 → 5.18 | **Verified** |
| Station | HKO Headquarters | climate file `station` column; `config.yml` `weather.station_label` | unique station = `HKO` | **Verified** |
| HKO annual extremes validation | 33/33 MATCH | `outputs/tables/hko_annual_extremes_validation.csv`; `reports/hko_figure_validation_note.md` | 11 years × 3 metrics; all `difference == 0` | **Verified** |
| Appendix A2 annual totals 2013–2023 | see table | `hko_annual_extremes_validation.csv` | row-by-row match to validation file | **Verified** |
| Tmax vs lag-1 Tmax correlation | r ≈ 0.82 | climate file | Pearson r(current Tmax[2:132], lag Tmax[1:131]) = 0.822489 | **Verified** |
| Lag correlation pairs | 131 pairs | climate file | 132 − 1 = 131 | **Verified** |
| Figure x-axis / series end | Dec 2023 | climate file; revised figure | last month_id `2023-12`; plot xlim ends Dec 2023 | **Verified** |
| December 2012 daily weather available | yes (raw) | `data_raw/hko/daily_extract/dailyExtract_2012.xml`; `CLMTEMP/CLMMINT/CLMMAXT_HKO.csv` | Dec 2012 has 31 daily rows in CLM files; 2012 extract present | **Verified** |
| December 2012 in processed monthly file | no | `climate_monthly_2013_2023.csv` | first month_id = `2013-01` | **Verified** |
| January 2013 lag-1 missing unless extended | yes | processed file start + lag construction | lag-1 for 2013-01 requires 2012-12 monthly row | **Verified** |
| C&SD population months | 2013-01–2023-12 | `data_processed/population_monthly_age_sex_2013_2023.csv` | month range confirmed; `data_status = CSD_IMPORTED` | **Verified** |
| Age bands 65–69 and 70–74 in C&SD panel | present | same population file | both age groups present | **Verified** |
| Meeting length target | ~8–10 min | task brief / speaker notes | non-data planning target | N/A (not empirical) |

## Confirmation-status statements (non-numeric)

| Statement | Source | Verified? |
|---|---|---|
| ICD-9 confirmed | `memos/data_request_roro.md` status block; `analysis_plan/assumption_ledger.md` A03 | **Verified** against project records (Roro, 12 Jul 2026) |
| Patient-level admission information confirmed | same; ledger A37 | **Verified** against project records |
| 65–69 and 70–74 available separately (HA) | same; ledger A10 | **Verified** against project records |
| No ED-to-inpatient episodes included | same; ledger A08 | **Verified** against project records |
| Wet-ink / HPC access pending | same; ledger A38 | **Verified** against project records |
| No real admission analysis yet | README; HA placeholder; no real HA outcomes in repo | **Verified** |
| DAE meaning unknown / not invented | ledger A03; memo status (“definition TBD”) | **Verified** — marked for Roro clarification |
| IRB amendment is PI decision | ledger A39 | **Verified** against project records |
| Bishai requested Tmax/Tmin (+ lag), AMI/stroke, covariates (age, sex, diuretics, beta blockers, metformin, SGLT2is, BMI), Table 1 | memo status; ledger A27, A30 | **Verified** against project records (12 Jul 2026 direction) |
| Provisional ICD-9 code lists | `memos/data_request_roro.md` | **Verified** as provisional working definitions |

## Design corrections relative to original deck

| Issue in original | Correction in revised deck | Status |
|---|---|---|
| Mixed “admission risk” language without denominator fork | Explicit monthly population-rate vs patient-month risk fork | Corrected |
| Called for lag preference as uncertainty (“I am unsure which lag Prof. Bishai prefers”) | Proposed model ladder with request for confirmation | Corrected |
| Table 1 mixed environmental and patient rows under one table without denominator distinction | Split Panel A (N=132 months) vs Panel B (denominator TBD) | Corrected |
| Question list framed like interrogation / “blocked” tone | Collaborative confirmations + assigned actions | Corrected |
| Medications/BMI implied as automatic model confounders | Descriptive inclusion requested; model role conditional on cohort/timing | Corrected |
| Temperature figure used “(C)” and lacked “Environmental exposure data only” | Revised ribbon figure with °C and exposure-only note | Corrected |
| Original deck overwritten risk | New `_revised` tex/PDF; originals retained | Preserved |

## Files created / preserved

| Path | Role |
|---|---|
| `reports/latex/lab_meeting_2026-07-17.tex` | **Original source preserved** |
| `reports/Lab_Meeting_2026-07-17.pdf` | **Original PDF preserved** |
| `reports/latex/lab_meeting_2026-07-17_revised.tex` | Revised source |
| `reports/Lab_Meeting_2026-07-17_revised.pdf` | Revised compiled PDF |
| `figures/lab_meeting/monthly_temp_ribbon_2013_2023.{pdf,png}` | New Slide 3 figure (original Tmax/Tmin figure retained) |
| `figures/lab_meeting/tmax_lag1_example_revised.{pdf,png}` | Revised lag illustration (original retained) |
| `reports/speaker_notes_2026-07-17.md` | Speaker notes |
| `reports/deck_revision_audit.md` | This audit |
| `memos/clarification_email_to_roro.md` | Follow-up email draft |

## Rounding policy

Means and SDs reported to 2 decimal places, matching the original deck’s Table 1 display convention. Correlation reported as `r ≈ 0.82` (exact 0.822489).
