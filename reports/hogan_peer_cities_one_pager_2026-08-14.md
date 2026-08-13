# Hogan card — exporting HKO flags is a climate act

**Date:** 14 August 2026.  
**Audience:** Hogan (weather lock). Exposure only. No coefficients.

Hong Kong’s official flags (`Tmin ≥ 28` hot night, `Tmax ≥ 33` very hot day, `Tmin ≤ 12` cold day) are **station-threshold objects**. They do not travel onto ERA5-Land for free.

## What broke in the calibration (Hong Kong coordinate, 4,017 days)

| Encoding | Hot nights | Very hot days | Cold days |
|---|---:|---:|---:|
| HKO Headquarters | 449 | 421 | 145 |
| ERA5 dry-bulb | 17 | 19 | 296 |
| ERA5 + 1.47 °C offset | 378 | 106 | 186 |
| ERA5 apparent temperature | 1,453 | 1,368 | 589 |

Hot-night Jaccard, dry-bulb vs station: **0.031**. ERA5 nights are **1.47 °C colder** than HKO (Tmin RMSE 1.97 °C). Apparent temperature is not a repair: in humid Hong Kong it overshoots the station.

**Live paper stays on HKO.** Guo’s official-flag vs hourly-intensity distinction is the same family of problem.

## Who is actually a climate cousin (same ERA5 source)

Nearest in mean T + seasonal amplitude + ERA5 flag rates: **Taipei (0.18), Shenzhen (0.20), Guangzhou (0.47)**.  
Singapore’s seasonal amplitude is 1.5 °C (Hong Kong 12.1 °C) and records **zero** 12 °C days on this grid. Phoenix records 1,733 ERA5 days with `Tmax ≥ 33` against Hong Kong’s 19. Both are contrasts, not replicates.

Brisbane’s local winter is **JJA**. Transporting DJF language with the flags would be a hemisphere error.

## Ask in the lock conversation

1. Official monthly hot-night counts remain the encoding for Hong Kong (HKO), not a reanalysis recount and not an apparent-temperature recount.
2. Any later multi-city extension needs **local percentiles or a locally bias-corrected night minimum**, not raw 28/33/12 on ERA5.
3. “Hong Kong is becoming more like Singapore” is a climate claim that this grid does not support for winter.
4. Phoenix / desert heat-health language does not travel to humid-subtropical Hong Kong.

Atlas: `docs/peers/index.html`. Memo: `knowledge/2026-08-14_peer_cities_thermal_atlas.md`. Figures: `figures/peer_cities/`.
