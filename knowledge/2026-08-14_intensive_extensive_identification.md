# Intensive vs extensive identification — 14 August 2026

**Mode:** Ship.  
**Provenance:** `REAL` HKO Headquarters monthly encodings, 132 months (`data_processed/climate_monthly_2013_2023.csv`).  
**Not:** health findings, q-values, Gate 3, or form 2a.

Rebuild: `python3 scripts/57_intensive_extensive_identification.py`.  
Tests: `python3 scripts/test_57_intensive_extensive.py`.

Script 55 asked how much of each series survives calendar-month indicators. This script asks what that residual *is*.

## Punchline

| Encoding | Identifying residual | Of which intensive | Always-on months | Mixed months |
|---|---:|---:|---|---|
| Mean temperature | 4.2% (script 55) | **100%** | n/a (continuous) | none |
| Hot nights ≥ 28°C | 28.8% | **95.4%** | Jun–Sep (11/11 years) | May, Oct |
| Very hot days ≥ 33°C | 33.1% | 85.4% | Jun–Aug | May, Sep, Oct |
| Cold days ≤ 12°C | 46.9% | 61.2% | **none** | Dec–Mar |

June–September always had at least one official hot night. Every June had at least **six**. July 2013 had **1**; July 2022 had **25**; July is **44%** of hot-night identifying sum of squares. The extensive margin of “was this a hot-night month?” is almost entirely May and October.

No winter month always had a cold day. 2019 is almost a null winter (December 0, January 1, February 0, March 0). That is why cold days keep more identifying share *and* more extensive variation: “whether this January was cold” still moves.

## Why this belongs next to q > 0.19

Month indicators absorb summer versus winter. For hot nights they also absorb “June–September happen.” What remains is mostly July intensity. A twelve-contrast panel can be correctly specified and still have little leftover contrast. Multiplicity is not the only reason every core *q* exceeds 0.19.

## Claim boundaries

Do not treat an intensive share as a coefficient. Do not treat thin extensive variation as proof that a null is true. No hospital counts were used. Do not paste this into Hogan’s weather paragraph.

Figure: `figures/identifying_months/intensive_extensive.svg`.
