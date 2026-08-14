# The threshold does not travel — 14 August 2026

**Mode:** Ship.  
**Provenance:** `REAL_PUBLIC` (HKO Headquarters daily Tmin; Open-Meteo ERA5-Land dry-bulb and apparent Tmin at the Hong Kong coordinate from the script 48 cache; ERA5-Land 0.2° PRD lattice from the script 50 cache).  
**Not:** health findings, CHD/HF coefficients, stroke, Gate 3, a live-manuscript paste of mosaic flags as HKO, or a substitute for the 31 August Network essay.

Instrument: [`docs/demo/index.html`](../docs/demo/index.html).  
Rebuild: `python3 scripts/53_threshold_does_not_travel.py`.  
Tests: `python3 scripts/test_53_threshold_does_not_travel.py`.

## Why this exists

The peer atlas, Hong Kong lattice, PRD mosaic, and field laboratory were four rooms around one fact: a 28°C night is an encoding and a location. This page is the instrument, not a fifth dashboard. Move the threshold. Watch three objects and a field change together.

## Anchors at the official 28°C night (4,017 matched days, 2013–2023)

| Object | Nights ≥ 28°C |
|---|---:|
| HKO Headquarters dry-bulb | **449** |
| ERA5-Land dry-bulb at the HK coordinate | **17** |
| ERA5-Land apparent temperature at the same coordinate | **1,453** |
| Jaccard (HKO ∩ ERA5 dry-bulb) / union | **0.031** |
| Intersection / HKO-only / ERA5-only | 14 / 435 / 3 |
| ERA5 Waglan cell | 423 |
| ERA5 Guangzhou cell | 23 |
| Marine-south share of all cell-nights | **0.778** |
| Cells lit at least once | 65 / 90 |
| ERA5 − HKO Tmin bias | **−1.473°C** |

Matching a *count* is not matching the *nights*. Closest 0.1°C steps:

- ERA5 dry-bulb needs **26.4°C** to reach 448 nights (target 449, abs err 1).
- HKO dry-bulb needs **29.5°C** to reach 16 nights (target ERA5’s 17, abs err 1).

The station’s **fixed** 28°C set against ERA5 ≥ *t*:

| Recalibration | Jaccard | Sensitivity | PPV | Intersection |
|---|---:|---:|---:|---:|
| Official 28°C on both | 0.031 | 0.031 | 0.824 | 14 |
| ERA5 mean-bias shift then 28°C | 0.433 | 0.557 | 0.661 | 250 |
| **Max Jaccard** (ERA5 ≥ **26.3°C**) | **0.471** | 0.668 | 0.615 | 300 |

No monotone threshold shift recovers the station nights. The 14 ERA5 28°C nights are almost all inside the station set (PPV 0.82) and almost none of it (14/449).

## Jaccard is a function of the threshold

| Tmin threshold | Jaccard | HKO | ERA5 HK | Cells lit | Marine share of cell-nights |
|---|---:|---:|---:|---:|---:|
| 24.0°C | 0.834 | 1,824 | 1,560 | 90 / 90 | 0.274 |
| 26.0°C | 0.488 | 1,234 | 648 | 88 / 90 | 0.446 |
| 26.5°C | 0.361 | 1,054 | 416 | 88 / 90 | 0.528 |
| 28.0°C | 0.031 | 449 | 17 | 65 / 90 | 0.778 |
| 30.0°C | 0.000 | 1 | 0 | 14 / 90 | 0.909 |

At a mild threshold the station and the grid mostly agree, and the whole delta lights. At the official hot-night step they almost never fire together, and the remaining nights sit on the water. A Jaccard of 1 at a still-higher threshold can mean both encodings are silent; the instrument reports that as missing, not as agreement.

## Claim boundaries

- Do not paste ERA5 night counts into the live paper’s HKO flags.
- Do not treat apparent temperature as a reconstruction of Headquarters.
- Do not overlay CHD/HF or stroke on cells.
- Do not transport Hong Kong hospitalisation ratios.
- This URL is not form 2a and not the Scholars Network University-room post.

Assumption **A68**. Hogan card: [`reports/hogan_threshold_does_not_travel_2026-08-14.md`](../reports/hogan_threshold_does_not_travel_2026-08-14.md).
