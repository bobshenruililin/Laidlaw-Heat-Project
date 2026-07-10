# Email to Professor Bishai

**From:** Bob Shen  
**To:** Professor David Bishai  
**Cc:** Hogan; Roro (optional, once timing is agreed)  
**Subject:** First-stage progress update — thermal extremes & CVD admissions pipeline (HA outcomes still pending)  
**Date:** 10 July 2026  

---

Dear Professor Bishai,

Thank you for the opportunity to develop this Laidlaw climate-health project. I have completed a first-stage analysis pipeline and exploratory preparation. The purpose of this stage was to build a reproducible workflow, process public environmental data, and test the planned statistical structure **before** we access Hospital Authority (HA) outcome data.

## What I completed

- Processed real Hong Kong Observatory (HKO) daily climate extracts into monthly thermal-extreme variables for January 2013–December 2023 (with a 2024 extract also prepared), using official definitions for hot nights, very hot days, extremely hot days, and cold days.
- Built a synthetic HA-like outcome panel and ran Negative Binomial / Poisson model templates with age, sex, diagnosis strata, seasonality, time trend, COVID phases, and population × days-in-month offsets.
- Prepared import structures for C&SD age-sex population denominators and EPD pollution files (current files are clearly labeled synthetic/placeholder until real deposits arrive).
- Drafted an assumption ledger, literature baseline, Methods outline, and data-request memos for Roro (HA) and Hogan (climate/pollution).
- Organized the repository so that real, placeholder, and synthetic datasets are distinguishable, and the pipeline can be re-run end to end.

Draft PR: https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/1

## Preliminary observations

**Verified public-data (HKO) descriptive findings only:**

- Annual hot nights rose from an average of about **31/year in 2013–2018** to about **53/year in 2019–2023**; very hot days rose from about **30** to about **48**.
- Cold days remained variable (range **1–21** per year) rather than showing a simple monotonic decline.
- Hot nights and very hot days are highly correlated in the monthly series (**r ≈ 0.88**), which supports keeping them in separate primary/alternative models rather than entering both together by default.

**Synthetic-data pipeline validation (not cardiovascular findings):**

The synthetic models run, converge, detect overdispersion (Poisson is inadequate in the synthetic example), and recover a planted cold > heat signal. These are workflow findings rather than substantive cardiovascular findings because HA outcome data are not yet available.

## What is still needed

Before any real outcome analysis, we still need:

1. An approved HA aggregate extract (coding system; principal diagnosis; episode/transfer rules; age bands including 65–69 and 70–74; ED vs inpatient separation; suppression rules).
2. Real C&SD age-sex population denominators.
3. Real EPD general-station pollution files (NO₂, O₃, PM2.5, PM10).
4. Team decisions on study window (2013–2023 vs optional 2024), HKO/EPD station choices, COVID phases, and whether influenza belongs in the primary or sensitivity model.

## Data-sharing note

Public HKO/EPD/C&SD files, code, synthetic datasets, and drafts can normally be shared through ordinary institutional channels, subject to HKU rules. **I will not email any HA extracts, patient-level data, or unvetted secure-server outputs until Roro confirms the permitted transfer route, output-vetting process, and small-cell rules.**

## Proposed meeting

Could we schedule a **30–45 minute** meeting with you, Hogan, Roro, and me? Suggested agenda:

1. Approve primary question and study period  
2. Finalize HA outcome definition  
3. Finalize environmental and denominator files  
4. Agree secure transfer/access  
5. Freeze the pre-analysis plan  
6. Assign next actions  

## Suggested attachments (3)

1. First-Stage Progress Report (`reports/professor_progress_report.md`)  
2. One-Page Decisions and Data Needs (`reports/decision_and_data_needs_one_page.md`)  
3. Draft Introduction and Methods (`manuscript/introduction_draft.md` + `manuscript/methods_draft_revised.md`)  

The full repository/PR and technical appendix can be linked separately rather than attached as many files.

## Closing recommendation

The environmental and coding infrastructure is substantially prepared, but the cardiovascular models have so far been tested only on synthetic outcomes. The next scientific milestone is to finalize outcome definitions and securely obtain the real HA data, C&SD denominators, and EPD pollution files. I would value your guidance on which decisions you want locked before we proceed.

Best regards,  
Bob Shen
