# Identifying months — six HKO encodings — 14 August 2026

**Mode:** Ship.  
**Provenance:** `REAL` HKO Headquarters monthly encodings in `data_processed/climate_monthly_2013_2023.csv` (132 months).  
**Not:** health findings, q-values, Gate 3, or form 2a.

Rebuild: `python3 scripts/55_identifying_months_six_encodings.py`.  
Tests: `python3 scripts/test_55_identifying_months.py`.

The twelve-contrast panel puts calendar-month indicators in every model. Remaining identifying variation is between years within calendar month. That is a design fact, not only a multiplicity accident.

## Punchline

| Encoding | Identifying share | Calendar months with SD | Months ever > 0 |
|---|---:|---:|---:|
| Mean temperature | **4.2%** | 12 | 132 |
| Mean Tmax | 5.3% | 12 | 132 |
| Mean Tmin | 4.4% | 12 | 132 |
| Hot nights ≥ 28°C | **28.8%** | 6 (May–Oct) | 57 |
| Very hot days ≥ 33°C | 33.1% | 6 (May–Oct) | 53 |
| Cold days ≤ 12°C | **46.9%** | 4 (Dec–Mar) | 29 |

Mean temperature looks like it has eleven years of data. After month indicators it is identified on a 4% residual. Hot nights look like a summer series; month indicators absorb “summer versus winter,” leaving six calendar months. Cold days are already winter-concentrated, so a larger share survives — on four months, matching the live paper’s 141/145 December–February plus four March days.

## Why this belongs next to the maps

The maps showed that ERA5 cannot reconstruct the official 28°C nights (daily Jaccard 0.031; monthly slope 0.045). This table shows that even the *station* flag is thinly identified. Together they explain a null-ish hot-night interval without promoting any coefficient.

## Claim boundaries

Do not treat an identifying share as a coefficient. Do not treat a low share as proof that a null is true. No hospital counts were used.
