# Monthly CHD/HF analysis: current limits and decisions for discussion

**Shen Ruililin (Bob), Laidlaw intern, Bishai Lab**
**For:** Professor David Bishai and Hogan
**Date:** 18 August 2026
**Print:** this note (about three pages) or the one-page card. The public-file audit is a separate log, not this meeting’s reading.

This meeting note concerns Hospital Authority–approved aggregate CHD and HF counts. Stroke, daily outcomes, and cohort person-time are not included. I have not invented those series.

---

## What the delivered panel supports

Zhenyuan Liu (Roro) delivered territory-month counts of first recorded CHD and HF hospitalisation after first diagnosis, among people with type 2 diabetes and/or hypertension, January 2013–December 2023. Admission cause is absent. Stroke was named and not attached.

The delivered panel supports an ecological monthly analysis of those first recorded hospitalisations. The models are separate negative binomial regressions with calendar-month indicators, a 4-df time spline, and a days-in-month offset. The panel does not support cohort incidence, principal-diagnosis claims, daily triggering, or attributable-mortality claims.

All twelve predeclared contrasts had Benjamini–Hochberg *q*-values above 0.19. For CHD hot nights, the analysis-of-record estimate was 1.022 (95% CI 1.002–1.042), compared with 1.011 (0.991–1.032) before 2020. Official cold days in 2013–2023 totalled 145; 141 fell in December–February. CHD first-event counts declined from 23,830 in 2013 to 12,323 in 2023, while the interpolated Census population aged 35 or older rose about 17%. Without still-at-risk person-time, these count ratios cannot be interpreted as incidence.

Hogan’s weather paragraph is already the authority. Official hot-night, very-hot-day, and cold-day flags are aggregated to months. I have not overwritten that paragraph. Jingwen Liu et al. (2020) and Roro’s excess-mortality work answer different questions. I have not transported their relative risks onto this CHD/HF series.

---

## Why further intern modelling does not raise this

Additional modelling cannot resolve the main limitations: monthly outcome timing, incomplete outcome semantics, and absent person-time. Further specifications may test robustness. They cannot create the missing data.

I cannot sign a Hospital Authority Undertaking or act as principal investigator.

---

## Public files I opened

I checked whether a public substitute existed. It does not. The fetch log is `public_data_ceiling_search_2026-08-18.md`.

Public HA open data give financial-year discharges by hospital (809 rows; no month; no ICD). The Department of Health 2023 disease-class file gives one year of episode counts, including day inpatients; circulatory chapter I00–I99 is 162,691 discharges and deaths. DATA.GOV.HK’s catalogue search for inpatient/hospitalisation returned one quarterly throughput table. Public HKO daily mean temperature for 2013 is complete (365 days). Weather is not the missing object.

Guo et al. (2024) analysed daily emergency hospitalisations using HA data under licence; those admissions are not public. A different outcome series would require a collaborator-provided extract or a separate PI-led application (HA Form A or B, or HKU-EHPDCL). I can draft a specification. I cannot submit it.

---

## Questions for this meeting

1. **Hogan.** Should official monthly hot-night, very-hot-day, and cold-day counts remain the exposure family for the current paper? If the Li-HW / HM23 tail month remains in play, which reference period and month-assignment rule should apply? You do not need to send another temperature file.

2. **Professor Bishai.** Should the CHD/HF analysis proceed as an identification-focused paper without a confirmatory primary, once the weather paragraph and health-data methods are confirmed?

3. **Follow-up for Roro, not a same-day extract request.** Ask for the outcome definitions (ICD/ICPC lists; inpatient versus day inpatient or A&E; how first-event month is dated) and a yes/no availability statement for stroke, monthly still-at-risk person-time, and ages 65–69 / 70–74. Scope any new extract separately.

Authorship, ethics paperwork, journal choice, paid HA access, and a new governed project are later. They should not travel in the same round as the three questions above.

---

## What I will keep doing

I will work in the shared manuscript using the agreed outcome and weather definitions. Any new governed file will be checked for structure, documentation, and suppression before analysis.
