# Monthly station–grid bridge — 14 August 2026

**Mode:** Ship.  
**Provenance:** `REAL_PUBLIC` (HKO Headquarters daily Tmin; ERA5-Land at the Hong Kong coordinate from the script 48 cache).  
**Not:** health findings, a health attenuation factor, Gate 3, or form 2a.

The live paper uses **132 monthly counts**. Daily Jaccard 0.031 could have been an aggregation artefact. It is not.

Rebuild: `python3 scripts/54_monthly_station_grid_bridge.py`.  
Tests: `python3 scripts/test_54_monthly_station_grid_bridge.py`.

## Punchline

Monthly **mean Tmin** agrees (r = **0.986**, slope = **1.032**). Monthly **28°C-night counts** do not (r = **0.475**, slope = **0.045**, SE 0.007). Headquarters has hot nights in **57** months; ERA5 in **9**, all inside those 57.

| Object (132 months) | Slope (ERA5 ~ HKO) | r | Mean HKO | Mean ERA5 |
|---|---:|---:|---:|---:|
| Mean Tmin | 1.032 | 0.986 | 22.10°C | 20.63°C |
| Nights ≥ 28°C | **0.045** | 0.475 | 3.40 | 0.13 |
| Apparent-T nights ≥ 28°C | 1.853 | 0.783 | 3.40 | 11.01 |
| Days ≤ 12°C | 1.537 | 0.881 | 1.10 | 2.24 |
| Nights ≥ 28°C, May–Oct only | 0.050 | 0.422 | 6.80 | 0.26 |

## Identification (HKO hot nights, month-factor design)

Only **29%** of the 132-month sum of squares is between-year within calendar month — the variation that survives month indicators. Six calendar months have any SD (May–October). June–September have hot nights in all 11 years.

This is not a health result. It is why a null-ish CHD hot-night interval is not surprising even before multiplicity: the contrast is identified on a handful of summers.

## Literature position

- Guo et al. 2024: the official 28°C *flag* was a poor hospitalization metric next to hourly excess (already live-paper [17]).
- Mistry et al. 2022 (*Sci Rep*): ERA5-Land is generally usable for temperature–mortality *curves*, with weaker heat performance in the tropics.
- This bridge: the official flag also fails as a **reanalysis object**, at the grain of our panel. Means travel. The threshold does not.

## Claim boundaries

Do not treat 0.045 as the factor by which a health coefficient would shrink. No outcome was used. Do not paste ERA5 monthly counts as HKO flags.
