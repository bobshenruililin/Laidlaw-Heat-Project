# Hogan card — the threshold does not travel

**Date:** 14 August 2026.  
**Audience:** Hogan (weather lock). Exposure only. No coefficients.

The live paper should keep **HKO Headquarters**. Official flags are station objects at 28°C. What changes, if the same step is asked of ERA5-Land, is not a footnote. It is the encoding.

On 4,017 matched days (2013–2023):

| Encoding at 28°C | Nights |
|---|---:|
| HKO Headquarters | **449** |
| ERA5-Land dry-bulb, same coordinate | **17** |
| ERA5-Land apparent temperature | **1,453** |
| Jaccard (station ∩ grid) / union | **0.031** |

Jaccard is a function of the threshold, not a single calibration statistic.

| Threshold | Jaccard |
|---|---:|
| 24°C | 0.83 |
| 26°C | 0.49 |
| 28°C | 0.031 |
| 30°C | 0 |

To recover a *count* near 449 on ERA5 dry-bulb you must lower the night to **26.4°C** (448 nights). Those are not the same 449 nights. Intersection at 28°C is 14 days (PPV 0.82, sensitivity 0.031).

The best monotone match to the **fixed** station 28°C set is ERA5 ≥ **26.3°C**: Jaccard **0.47**, not 1. Mean-bias correction recovers 378 nights and Jaccard 0.43. Frequency can be matched. The nights cannot.

On the 0.2° Pearl River Delta lattice the remaining 28°C nights are marine (cell-night share **0.78**). Waglan’s cell records 423; Guangzhou’s records 23. At 24°C every cell lights and marine share falls to 0.27.

Use HKO for the paper. Use ERA5 only for same-source geography. Do not paste mosaic or apparent-temperature counts as Headquarters flags.

Instrument: `docs/demo/index.html`. Static figure: `figures/threshold_demo/exceedance_and_agreement.svg`.
