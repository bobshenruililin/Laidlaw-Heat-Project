# Pearl River Delta thermal mosaic — 14 August 2026

**Mode:** Explore + Ship.  
**Provenance:** `REAL_PUBLIC` (Open-Meteo ERA5-Land daily 2 m temperatures, 2013–2023, 0.2° lattice plus named city coordinates).  
**Not:** health findings, prefecture CHD/HF maps, stroke, Gate 3, a CMA yearbook, or a live-manuscript paste.

Interactive map: [`docs/prd/index.html`](../docs/prd/index.html).  
Rebuild: `python3 scripts/50_prd_thermal_mosaic.py` (or `--skip-fetch`).  
Tests: `python3 scripts/test_50_prd_thermal_mosaic.py`.

## What this is

The peer-city atlas treated Shenzhen and Guangzhou as points. The Hong Kong lattice showed that a 28°C night is a location *inside* the territory. This mosaic asks the next spatial question: once you leave the harbour, does that night travel up the Pearl?

Ninety ERA5-Land cells from 21.9–23.5°N and 112.9–114.7°E, plus ten city coordinates. Same 4,017 days. Same 28/33/12 °C cuts. Same source as the peer atlas. Not HKO, not CMA.

## Punchline numbers

Mean ERA5 nights with `Tmin ≥ 28°C`, 2013–2023, by lattice region (not official normals):

| Region | Cells | Mean Tmin | Mean hot nights | Mean cold days |
|---|---:|---:|---:|---:|
| marine south | 20 | 22.07 °C | **353.2** | 166 |
| Hong Kong box | 6 | 20.40 °C | 29.7 | 369 |
| Zhuhai–Macau | 10 | 20.13 °C | 43.5 | 459 |
| Guangzhou box | 12 | 19.33 °C | 12.1 | 630 |
| Shenzhen box | 3 | 19.72 °C | 5.3 | 508 |
| Dongguan | 6 | 19.31 °C | 3.5 | 582 |
| Huizhou | 12 | 18.62 °C | 0.2 | 718 |

City coordinates on the same source: Macau **143** hot nights, Zhuhai 84, Hong Kong 17, Guangzhou 11, Shenzhen 10, Huizhou **0**.

Waglan → Guangzhou transect (nearest mosaic cell):

| Stop | Cell Tmin | Cell hot nights | km from HQ |
|---|---:|---:|---:|
| Waglan Island | 22.75 °C | **423** | 19 |
| HKO Headquarters | 21.16 °C | 68 | 0 |
| Shenzhen | 20.15 °C | 10 | 29 |
| Dongguan | 19.58 °C | 11 | 91 |
| Guangzhou | 19.72 °C | 23 | 131 |

The 28°C night on this grid is a **marine object**. Inland Guangdong barely sees it. Exporting Headquarters’ official flag up the river is a larger spatial act than exporting it across Victoria Harbour.

Unique daily fingerprints: **99 of 100** points.

## Spatial models (90 lattice cells)

Neighbour graph: binary distance weights, 35 km cutoff (mean 6.8 neighbours).

- OLS `Tmin ~ elevation + lat + lon`: R² **0.890**, elevation **−0.0074 °C/m**, latitude **−2.18 °C per degree north**, longitude **+0.46 °C per degree east**. Residual Moran’s I **0.567** (raw I **0.676**).
- SLX `Tmin ~ X + WX`: R² **0.906**, residual I **0.520**. Neighbours’ elevation and latitude still shift a cell.
- SAR-2SLS `Tmin ~ X + W Tmin`: ρ **0.45** (SE 0.12), R² **0.906**, residual I **0.522**. Two-stage least squares with WX as instruments for Wy. The R² is a fit diagnostic, not a likelihood.
- Getis-Ord Gi* on annual hot-night counts: **17 hotspot** cells (|z| > 1.96), **0 coldspot** cells. The hotspots sit on the water.
- Thermal-versus-geographic distance (z-scored Tmin, hot nights, cold days, seasonal amplitude vs km from Headquarters): Pearson **r = 0.53**. Climate only half-follows the map; marine and ridge cells are the remainder.

## Laidlaw deliverable path

These maps are **programme public surfaces**, not journal results.

| Surface | What this mosaic does | What it must not do |
|---|---|---|
| Laidlaw website blog | Draft [`the_river_has_a_temperature.md`](../reports/blog/the_river_has_a_temperature.md) | Post without Bob’s voice/privacy pass |
| LSN | Link after privacy pass | Quote mosaic flags as HKO or paste coefficients |
| GitHub Pages (`docs/`) | Public companion once Settings → Pages is on | Pretend the `github.io` URL already works (it 404s until enabled) |
| Stage 3 report / A0 poster | Nothing. Those PDFs stay frozen | Rebuild or insert lattice numbers |
| Hogan live manuscript | Hogan card only | Overwrite weather Methods or move the paper off Headquarters |

## What this does not license

- Overlaying CHD/HF or stroke counts on cells, districts, or prefectures.
- Transporting Hong Kong hospitalisation ratios to Shenzhen or Guangzhou.
- Quoting mosaic hot nights as HKO or CMA flags.
- Treating Open-Meteo DEM-lapse series as hill stations.
- Moving the live paper off Headquarters.
