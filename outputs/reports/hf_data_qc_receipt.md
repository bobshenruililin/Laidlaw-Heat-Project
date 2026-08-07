# HF aggregate QC receipt

- **Outcome:** `hf`
- **File:** `/workspace/data_raw/ha_secure_placeholder/ha_hf_monthly_2013_2023.csv`
- **Rows:** 132
- **Grain:** territory
- **data_status:** HA_APPROVED_AGGREGATE
- **Cohort:** T2D_and_or_HTN_2013_2023
- **Event definition:** first_hospitalization_after_first_cvd_diagnosis_record
- **Type labels:** hf_all
- **Months:** 132 (2013-01 → 2023-12)
- **Missing study months:** 0
- **Total events:** 29681
- **Mean events / month:** 224.86
- **Annual totals 2013 → 2023:** 4336 → 2296
- **Suppressed rows:** 0
- **Normalized path:** `/workspace/data_processed/hf_aggregates_normalized.csv`
- **Checked at:** 2026-08-07 09:00:09.589776

## Denominator caveat

Events are restricted to patients with T2D and/or HTN (2013–2023) using first hospitalisation after first CVD diagnosis.
C&SD general-population offsets are ecological person-time, **not** cohort at-risk person-time.

**Provenance:** HA_APPROVED_AGGREGATE (monthly). Do not commit microdata.

## Annual event totals

| Year | Events |
|---|---|
| 2013 | 4336 |
| 2014 | 3675 |
| 2015 | 2934 |
| 2016 | 2734 |
| 2017 | 2620 |
| 2018 | 2527 |
| 2019 | 2344 |
| 2020 | 1964 |
| 2021 | 2275 |
| 2022 | 1976 |
| 2023 | 2296 |
