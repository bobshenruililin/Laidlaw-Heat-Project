# Source-locked weather morphology build

- Provenance: `REAL_PUBLIC_HKO`.
- Result class: `EXPOSURE_AUDIT`.
- Health outcomes were not read.
- Li monthly upper-tail classification remains Hogan-unlocked.
- Primary-source reproduction checks: 5 / 5 passed.

## Definitions

| ID | Implementation | Status |
|---|---|---|
| wang_vhd5 | Tmax >= 33 C; >= 5 consecutive VHDs | PRIMARY_SOURCE_LOCKED |
| wang_hn5 | Tmin >= 28 C; >= 5 consecutive HNs | PRIMARY_SOURCE_LOCKED |
| wang_2d3n | NDNDN: VHD[i:i+1] and HN[i:i+2]; overlapping/touching windows merged; post-event days 1-5 | PRIMARY_SOURCE_LOCKED_DAILY_DATE_ALIGNMENT_DOCUMENTED |
| li_hw | May-Sep Tmax > calendar-day p90; 15-day moving window; 1980-2023 reference; >=3 days; merge event interval <=2 days (<=1 intervening non-hot day) | PRIMARY_SOURCE_LOCKED_HOGAN_MONTHLY_TAIL_NOT_LOCKED |

## Study-window event counts

- li_hw: 38
- wang_2d3n: 33
- wang_hn5: 27
- wang_vhd5: 25

Calendar-spillover phases are assigned by affected date. A late-month 2D3N event therefore contributes post-event days to the following month.
