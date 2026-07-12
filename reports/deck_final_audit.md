# Deck final audit — Lab meeting 17 July 2026

**Final deck:** `reports/latex/lab_meeting_2026-07-17_final.tex` → `reports/Lab_Meeting_2026-07-17_final.pdf`  
**Preserved:** original and revised decks (`lab_meeting_2026-07-17.tex` / `_revised.tex` and PDFs)  
**Auditor:** Bob Shen (final pass, with independent numerical / design / narrative review)  
**Date:** 12 July 2026

## Scope

Every numerical or factual statement in the final main deck and appendix is listed below with source and verification status. Design-status statements are included when they claim confirmation status.

## Numerical / factual audit table

| slide | statement | value | source file | source variable or calculation | reproduction command/script | verified status | notes |
|---|---|---|---|---|---|---|---|
| 1 / 2 | Study months N | 132 | `data_processed/climate_monthly_2013_2023.csv` | `len(rows)` | `python3` csv count; first `2013-01`, last `2023-12` | **Verified** | |
| 2 / 3 | Period | Jan 2013–Dec 2023 | same; `config.yml` | `month_id` range | same | **Verified** | No 2024 tick on figure |
| 2 | Station | HKO Headquarters | climate file `station`; `config.yml` | unique `station == HKO` | set of station values | **Verified** | |
| 4 / A5 | Mean temperature mean (SD) | 24.02 (4.70) | climate file | `mean(mean_temp)`, sample SD | independent python: 24.018046 / 4.698265 | **Verified** | 2 dp |
| 4 / A5 | Mean Tmin mean (SD) | 22.10 (4.69) | climate file | `mean(mean_tmin)`, SD | 22.104444 / 4.691418 | **Verified** | |
| 4 / A5 | Mean Tmax mean (SD) | 26.66 (4.82) | climate file | `mean(mean_tmax)`, SD | 26.663841 / 4.819647 | **Verified** | |
| 4 / A5 | Hot nights mean (SD) | 3.40 (5.40) | climate file | `mean(hot_nights)`, SD | 3.401515 / 5.399830 | **Verified** | days/month |
| 4 / A5 | Very hot days mean (SD) | 3.19 (5.18) | climate file | `mean(very_hot_days)`, SD | 3.189394 / 5.177952 | **Verified** | |
| 4 / A5 | Cold days mean (SD) | 1.10 (2.55) | climate file | `mean(cold_days)`, SD | 1.098485 / 2.552831 | **Verified** | |
| 2 / A2 | HKO annual validation | 33/33 MATCH | `outputs/tables/hko_annual_extremes_validation.csv` | 11 years × 3 metrics; all `difference==0` | csv: 33 rows, all MATCH | **Verified** | |
| A2 | Annual totals 2013–2023 | see appendix table | same validation CSV | row-by-row | matched | **Verified** | |
| 6 | Tmax vs lag-1 Tmax | r ≈ 0.82 | climate file | Pearson(`mean_tmax[2:132]`, `mean_tmax[1:131]`) | exact **0.822489** | **Verified** | report ≈ 0.82 |
| 6 | Lag pairs | 131 | climate file | 132 − 1 | 131 | **Verified** | |
| 6 / notes | December 2012 raw weather | available | `data_raw/hko/CLM*_HKO.csv`; `dailyExtract_2012.xml` | 31 daily rows for 2012-12 in each CLM file | `grep '^2012,12,'` → 31 | **Verified** | |
| 6 | Dec 2012 in processed monthly | absent | climate file | first `month_id` | `2013-01` | **Verified** | extension recommended |
| A4 | C&SD population status | real MDT import; monthly interpolated | `population_monthly_age_sex_2013_2023.csv` | `data_status=CSD_IMPORTED`; notes field | 2904/2904 `CSD_IMPORTED` | **Verified** | **Not** labelled “REAL MDT” alone |
| A4 | C&SD source table | 110-01001 | population file | `source_table` | all rows | **Verified** | |
| 2 | ICD-9 confirmed | ICD-9 | `memos/data_request_roro.md`; ledger A03 | Roro 12 Jul 2026 | memo + ledger | **Verified (provenance)** | no HA extract in repo |
| 2 | Ages 65–69 / 70–74 (HA) | available separately | same; ledger A10 | Roro 12 Jul | memo + ledger | **Verified (provenance)** | C&SD bands also present |
| 2 | ED-to-inpatient | not included in extract | same; ledger A08 | Roro 12 Jul | memo + ledger | **Verified (provenance)** | no elective/emergency inference |
| 2 | Patient-level admissions | confirmed | same; ledger A37 | Roro 12 Jul | memo + ledger | **Verified (provenance)** | |
| 2 | Wet-ink / HPC pending | pending | ledger A38 | governance | consistent | **Verified** | |
| 2 | No association estimated yet | true | HA placeholder; no real outcomes | merge script requires HA CSV | **Verified** | |
| A6 | Pollution file | placeholder | `pollution_monthly_2013_2023.csv` | `PLACEHOLDER_NOT_FOR_INFERENCE` | status field | **Verified** | |
| A6 | 2024 weather raw | exists | `dailyExtract_2024.xml`; `climate_monthly_2013_2024.csv` | optional extension | present | **Verified** | not delaying core |
| A1 | ICD-9 code lists | provisional | `memos/data_request_roro.md` | working definitions | memo | **Verified** as provisional | |

## Wording corrections relative to revised deck

| Issue in revised deck | Final correction | Status |
|---|---|---|
| Opening used forbidden title / room / duration / attendees | Mission Frame 1 title + status strip only | Corrected |
| Extra “Purpose” frame | Removed; seven main frames | Corrected |
| “REAL MDT” on pipeline slide | “C&SD MDT mid-year; monthly interpolated” | Corrected |
| Flowchart ended at locked “Negative Binomial” | “monthly admission-rate model” / “count models after definitions locked” | Corrected |
| Four confirmation headings + action matrix | Three headings + next deliverable | Corrected |
| Defensive “not a gap in Roro’s reply” | Removed | Corrected |
| ED wording risked elective inference | Neutral: episodes not included; admission-route fields still open | Corrected |
| `\scriptsize` substantive table text | Panel A at `\footnotesize` | Corrected |

## Dataset status summary (shown materials)

| Dataset | Status | How shown |
|---|---|---|
| HKO monthly exposures 2013–2023 | **Real** | Main Frames 2–4, 6; Appendix A2 |
| HKO Dec 2012 daily | **Real raw; not yet in processed monthly** | Frame 6 recommendation |
| C&SD denominators | **Real MDT import; monthly interpolated** | Appendix A4 (precise label) |
| HA admissions | **Pending HPC** | Frames 2, 5, 7 |
| Pollution monthly | **Placeholder** | Appendix A6 |
| Synthetic HA / synthetic models | **Workflow only** | Not shown as findings |

## Independent review passes

| Pass | Role | Key outcome |
|---|---|---|
| A | Numerical / provenance | All Panel A stats, r, 33/33, Dec 2012, C&SD status reproduced; flagged “REAL MDT” |
| B | Statistical design | Admissions-rate default sound; meds/BMI descriptive-first; Gate stop conditions |
| C | Narrative / presentation | Seven-frame map; cut Purpose slide; status strip; three ask headings |
| D | LaTeX / visual QA | Compile ×2; rasterize all 14 slides; figure title overlaps fixed via `_final` figures |

## Visual QA (Subagent D + main-agent re-check)

| Check | Result |
|---|---|
| Compile ×2 | Success; 14 pages |
| Missing figures | None |
| Main-frame count | Exactly 7 before appendix divider |
| Overfull boxes | 0.6 pt residual on title status strip (invisible) |
| Figure title collisions | Fixed in `*_final` figures (PR #11 figures preserved) |
| °C symbols | Correct on Frames 3, 4, 6; added to A5 |
| Font floor | Substantive text ≥ `\footnotesize`; `\scriptsize` for source/caption only |
| C&SD label | “MDT mid-year; monthly interpolated” (not “REAL MDT”) |
| Raster inspection | Slides 1–14 inspected; meeting-ready after figure fix |

## Rounding policy

Means and SDs to 2 decimal places. Correlation reported as `r ≈ 0.82` (exact 0.822489).

## Files created (this final pass)

| Path | Role |
|---|---|
| `reports/latex/lab_meeting_2026-07-17_final.tex` | Final source |
| `reports/Lab_Meeting_2026-07-17_final.pdf` | Final PDF |
| `reports/speaker_notes_2026-07-17_final.md` | Speaker notes |
| `reports/deck_final_audit.md` | This audit |
| `reports/post_meeting_next_steps.md` | Post-meeting action template |
| `analysis_plan/decision_gates.md` | Gates 1–5 |
| `memos/clarification_email_to_roro_final.md` | Concise follow-up email |
| `figures/lab_meeting/monthly_temp_ribbon_2013_2023_final.{pdf,png}` | Final ribbon figure (no title collision) |
| `figures/lab_meeting/tmax_lag1_example_final.{pdf,png}` | Final lag figure (no title collision) |

**Preserved unchanged:** original and revised `.tex`/`.pdf`, prior speaker notes, prior revision audit, prior clarification email, and PR #11 figure files (`monthly_temp_ribbon_2013_2023.*`, `tmax_lag1_example_revised.*`).
