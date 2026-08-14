# Hogan card — Headquarters is a location

**Date:** 14 August 2026.  
**Audience:** Hogan (weather lock). Exposure only. No coefficients.

The live paper should keep **HKO Headquarters**. Official flags are station objects.

A 0.1° ERA5-Land lattice over the territory (2013–2023) is a second object. On that source:

| Place | ERA5 hot nights (`Tmin ≥ 28`) | ERA5 cold days (`Tmin ≤ 12`) | Mean night Tmin |
|---|---:|---:|---:|
| HKO Headquarters cell | 17 | 296 | 20.66 °C |
| Waglan Island | **252** | 151 | 22.05 °C |
| Tuen Mun | 123 | 324 | 20.99 °C |
| Airport | 72 | 260 | 21.21 °C |
| Ta Kwu Ling | 15 | **399** | 20.38 °C |
| Victoria Peak (DEM-lapse, not a station) | 0 | 562 | 18.51 °C |

OLS on 30 lattice cells: `Tmin ~ elevation + coast` has R² **0.55**; elevation ≈ **−0.62 °C / 100 m**; coast is indistinguishable from zero. Adding lat+lon lifts R² to **0.88** (nights cool toward the north). Residual Moran’s I remains positive. The leftover is still a field.

Open-Meteo’s Peak series is a lapse-adjusted coordinate, not an HKO hill station. Do not treat it as independent observational evidence.

**Ask in the lock conversation**

1. Headquarters remains the encoding for Hong Kong.
2. A later multi-station composite (A15) would be a different paper, not a silent swap.
3. Exporting 28/33/12 across the harbour is already a spatial act; exporting them to Singapore or Phoenix is a larger one.

Map: `docs/geo/index.html`. Peer atlas: `docs/peers/index.html`.
