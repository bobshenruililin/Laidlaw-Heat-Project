# CHD aggregate QC receipt

- **Outcome:** `chd`
- **File:** `/workspace/data_raw/ha_secure_placeholder/ha_chd_monthly_2013_2023.csv`
- **Rows:** 132
- **Grain:** territory
- **data_status:** HA_APPROVED_AGGREGATE
- **Cohort:** T2D_and_or_HTN_2013_2023
- **Event definition:** first_hospitalization_after_first_cvd_diagnosis_record
- **Type labels:** chd_all
- **Months:** 132 (2013-01 → 2023-12)
- **Missing study months:** 0
- **Total events:** 156156
- **Mean events / month:** 1183
- **Annual totals 2013 → 2023:** 23830 → 12323
- **Suppressed rows:** 0
- **Normalized path:** `/workspace/data_processed/chd_aggregates_normalized.csv`
- **Checked at:** 2026-08-07 09:00:05.988071

## Denominator caveat

Events are restricted to patients with T2D and/or HTN (2013–2023) using first hospitalisation after first CVD diagnosis.
C&SD general-population offsets are ecological person-time, **not** cohort at-risk person-time.

**Provenance:** HA_APPROVED_AGGREGATE (monthly). Do not commit microdata.

## Annual event totals

| Year | Events |
|---|---|
| 2013 | 23830 |
| 2014 | 17760 |
| 2015 | 15411 |
| 2016 | 14510 |
| 2017 | 13962 |
| 2018 | 12616 |
| 2019 | 12396 |
| 2020 | 10237 |
| 2021 | 12035 |
| 2022 | 11076 |
| 2023 | 12323 |
