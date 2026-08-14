# Parked-object close-out — 14 August 2026

**Mode:** Ship. Internship analysis on public HKO / WorldPop / ERA5 caches already in the repo. Weather guidance remains Hogan’s; HA aggregates remain Roro’s; multi-method direction remains Bishai’s. No new health headline. Gate 3 stays open. Form 2a is still not this URL.

## What closed

| Parked object | Verdict | Evidence |
|---|---|---|
| Cold-side reliability companion | **Shipped** | When HKO is 8–12°C, ERA5 is ≤12°C on **127/128** nights. `docs/id/` second panel; not a third essay. Script 60. |
| ggplot Figure D | **Shipped** | Script 47 now draws the hot-night year×month map with the same monthly file and vmax 25 as Figure A. Python SVG remains the web analogue. |
| Public HKO station replicates | **Shipped** | Open-data CLMMINT/CLMMAXT for Headquarters, King’s Park, Waglan. Complete-C hot nights: HKO **449**, KP **160**, WGL **107**. KP Jaccard vs HKO **0.47** (every complete KP hot night is also an HKO hot night). WGL Jaccard **0.21**. Not ERA5. Not a substitute encoding. Script 61. |
| WorldPop-weighted ERA5 nights | **Shipped** | WorldPop 2020 1 km ASCII × 30 ERA5 0.1° cells. Southern cells (≤22.25°N) hold **66%** of unweighted 28°C cell-nights and a much smaller population-weighted share. Exposure only. Script 62. |
| Year-shifted negative control | **Teaching shipped; health re-fit parked** | Identifying share of hot nights is **0.288** before and almost unchanged after a 12-month shift — a calendar-month property, not a collapsed flag. The useful test is `health_t ~ exposure_{t-12}`. Gitignored analysis panels are absent (A60), so the R hook writes `PARKED_NO_PANEL` and invents no HA rows. Script 63. Gate 3 open. |
| Hogan W03 lock card | **Card shipped; lock not made** | Checkbox sheet for reference period, percentile/ties, gaps, missingness, month assignment. Registry remains `null`. Playbook 01 not executed. `reports/hogan_w03_lock_card_2026-08-14.md`. |

## Still human

- Hogan ticks W03. Agents do not.
- Bishai’s 2a endorsement. Still Email A, still not today.
- Roro’s stroke file. Still missing.
- Health year-shift re-fit. Needs the local HA panels; do not reconstruct monthly counts from annual totals.

## Misconduct list (unchanged)

Fitting more catalogue IDs because rank is 3.92; inverting P(HKO\|ERA5); using reliability as a measurement-error correction; treating 0.045 as attenuation; overlaying hospital counts; rebuilding frozen Stage 3 PDFs.
