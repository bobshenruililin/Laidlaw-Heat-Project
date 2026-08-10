# Cold-day identification audit (public HKO only)

**Date:** 10 August 2026  
**Provenance:** `REAL_PUBLIC_HKO`  
**Scope:** Exposure-support diagnostics for official cold days (daily minimum ≤12 °C aggregated to months). No health outcomes, no governed HA rows, no new health coefficients.

**Source:** `data_processed/exposures_monthly_2013_2023.csv` (132 months, Jan 2013–Dec 2023).  
**Machine tables:** `outputs/tables/cold_day_identification_audit.csv`, `outputs/tables/cold_day_identification_windows.csv`.

## Why this audit exists

A reviewer asked whether the HF × cold-days association is identified only from winter months and whether calendar-month indicators leave usable within-month variation. That question can be answered from public weather without reopening Gate 3 or inventing outcome rows.

## Calendar support

| Calendar month | Months in series | Months with any cold day | Mean cold days | Within-month variance |
|---:|---:|---:|---:|---:|
| Jan | 11 | 9 | 4.91 | 13.69 |
| Feb | 11 | 8 | 4.27 | 17.22 |
| Mar | 11 | 2 | 0.36 | 0.85 |
| Apr–Nov | 11 each | 0 | 0 | 0 |
| Dec | 11 | 10 | 3.64 | 8.25 |

In this Headquarters series, cold days occur almost entirely in December–February, with sparse March support and **zero** April–November cold days across 2013–2023. A “Nov–Apr” window therefore adds November and April months that contribute no cold-day contrast.

## Residual variation after season and trend

A full-series linear projection of monthly cold-day counts on
`factor(month) + ns(time, 4)` yields:

- R² ≈ 0.541
- design condition number ≈ 13.9
- maximum leverage ≈ 0.19

Residual variance remains material, especially inside December–February. The
table fits the projection once to all 132 months and then calculates the sample
variance of those residuals within each listed window:

| Window | n months | Months with any cold | Within-window variance | Full-series projection residual variance within window |
|---|---:|---:|---:|---:|
| All 132 | 132 | 29 | 6.52 | 2.99 |
| Nov–Apr | 66 | 29 | 10.68 | 5.96 |
| Dec–Feb | 33 | 27 | 12.52 | 11.84 |

Refitting `cold_days ~ factor(month) + ns(time, 4)` separately within each
window gives residual sample variances of 2.99, 5.90, and 11.42 for all months,
November–April, and December–February, respectively. Both calculations support
the same conclusion; the displayed machine-table values are the full-series
projection subsets.

Interpretation: calendar-month indicators absorb the average winter elevation, but **between-year differences within the same winter month remain**. That is the exposure variation that can identify a cold-day coefficient under month fixed effects. Restricting to December–February concentrates that residual variation; it also reduces n from 132 to 33.

## Does a winter-only health model improve identification?

**Not automatically.** On exposure grounds alone:

1. A winter-only negative-binomial model would use fewer months and therefore less precision unless residual confounding falls sharply.
2. November–April is a weak “winter” definition here because November and April contribute no cold days.
3. December–February is the scientifically honest restricted window for this station and threshold.
4. Any winter-only health coefficient remains **blocked in this checkout** until the governed CHD/HF analysis panel is restored and verified. This audit does not fit or invent those coefficients.

## Accepted vs rejected recommendation

| Memo recommendation | Decision |
|---|---|
| Discuss that cold days concentrate in winter and identification uses within-month, between-year variation | **Accept** — supported by this table |
| Fit a winter-only health model immediately | **Defer** — requires governed panel; Dec–Feb preferred over Nov–Apr |
| Treat winter restriction as a cure for multiplicity or confirmatory status | **Reject** — Gate 3 remains open |

## CHD hot-night NW3 check (release table)

From `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`:

| Method | Exact interval | 3-d.p. display |
|---|---|---|
| NW3 | 1.021824 (1.000253–1.043860) | 1.022 (1.000–1.044) |
| NW6 | 1.021824 (1.001854–1.042193) | 1.022 (1.002–1.042) |

NW3 **excludes 1 on the unrounded scale** and **touches 1.000 when rounded to three decimals**. Honest prose must say so.

## Limits

- Public weather only; no HA outcomes.
- Headquarters station proxy.
- Linear residualisation is a diagnostic for exposure support, not a health model.
- Gate 3 remains open.
