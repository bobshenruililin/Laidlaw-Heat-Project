# Identification remainder — salvaged from the monthly-panel crucible

**Date:** 15 August 2026  
**Ledger:** `A79` (was a colliding `A63` on `cursor/identification-crucible-1fd0`)  
**Mode:** Decide. Not a Gate 3 freeze. No new health model.

The crucible PR remains open as Explore. These two objects are the durable residue if that draft later closes.

## 1. Licensed paragraph

Across twelve core contrasts fitted separately by outcome and exposure, the estimand is a within-calendar-month, year-to-year weather-anomaly count ratio for first recorded hospitalisation after first diagnosis, conditional on a four-degree-of-freedom secular trend and a days-in-month offset, with the still-at-risk cohort denominator absent. No contrast clears Benjamini–Hochberg control: rank one would require *p* ≤ 0.004167 and the smallest observed *p* is 0.031. At the frozen baseline one contrast, heart failure and cold days per five days at 1.073, excludes 1 under all four displayed uncertainty methods; under four of nine paid trend and window scenarios it does not. The panel licenses no confirmatory primary, no daily, individual, cause-specific or cross-outcome claim, and no statement that thermal association is absent.

That is a reporting rule, not a finding. Option A as already written — no confirmatory primary; report the twelve contrasts with *q* and the SE ladder — is compatible with this paragraph. Narrating *q* > 0.19 as “no association” is not.

## 2. BH arithmetic (checked 15 August against release)

Twelve Newey–West lag-6 core rows in `outputs/release_chd_hf/supplement/cvd_core_robust_estimates.csv`. Rank 1 at *q* < 0.05 requires *p* ≤ 0.05/12 = 0.004167. Smallest *p* = 0.03096 (HF, cold days per five days), displayed 0.031. About 7.4 times the rank-1 threshold. Minimum *q* = 0.192.

## 3. Operator split (do not overwrite)

| ID | Residualisation | Object |
|---|---|---|
| A70 | Calendar-month indicators only | Identifying share of SS (mean T 4%; hot nights 29%; cold days 47%) |
| A79 | Calendar-month indicators **and** `ns(time,4)` | What the paid health panel can license |

Also in the Gate 3 packet (`reports/gate3_decision_packet_2026-08-07.md`) and the live Discussion (BH threshold sentence).
