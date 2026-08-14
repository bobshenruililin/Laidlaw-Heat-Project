# Hong Kong spatial thermal field — 14 August 2026

**Mode:** Explore + Ship.  
**Provenance:** `REAL_PUBLIC` (Open-Meteo ERA5-Land daily 2 m temperatures, 2013–2023, 0.1° lattice plus named landmarks).  
**Not:** health findings, district CHD/HF maps, stroke, Gate 3, or a live-manuscript paste.

Interactive map: [`docs/geo/index.html`](../docs/geo/index.html).  
Rebuild: `python3 scripts/49_hk_spatial_thermal_field.py` (or `--skip-fetch`).  
Tests: `python3 scripts/test_49_hk_spatial_thermal_field.py`.

## What this is

The peer-city atlas showed that a 28°C night is a **station object**. This lattice shows that it is also a **location object** inside Hong Kong.

Thirty ERA5-Land cells and nine landmarks. Same 4,017 days. Same 28/33/12 °C cuts as the peer atlas.

## Punchline numbers

| Place | ERA5 hot nights | ERA5 cold days | Mean Tmin |
|---|---:|---:|---:|
| Headquarters cell | 17 | 296 | 20.66 °C |
| Waglan Island | 252 | 151 | 22.05 °C |
| Tuen Mun | 123 | 324 | 20.99 °C |
| Ta Kwu Ling | 15 | 399 | 20.38 °C |
| Victoria Peak (DEM-lapse) | 0 | 562 | 18.51 °C |

Unique daily fingerprints: **37 of 39** points. Two neighbouring sea cells share a series (native grain). The Peak is *not* the same fingerprint as Headquarters (night RMSE 2.15 °C). Open-Meteo is applying an elevation correction; that is not an HKO hill station.

## Spatial model

On 30 lattice cells:

- `mean_tmin ~ elevation + dist_coast`: R² **0.546**, elevation **−0.0062 °C/m**, coast ≈ 0.
- Residual Moran’s I **0.67** (raw I was 0.18): elevation soaks up a few ridge cells; the leftover marine/north–south field is more clustered, not white.
- `mean_tmin ~ elevation + lat + lon`: R² **0.882**, latitude **−3.66 °C per degree north**, residual I **0.34**.
- Leave-one-out Headquarters ERA5 Tmin: predicted 20.94 vs observed 20.66 (error 0.28 °C). The remaining gap to the *station* is the 1.47 °C bias from the peer atlas.

## Laidlaw deliverable path

- Public companion in `docs/` (hub + geo + peers + LSN).
- GitHub Pages workflow: `.github/workflows/github-pages.yml`. The `github.io` URL still 404s until Bob enables Pages.
- Website blog draft: [`reports/blog/a_city_is_not_a_point.md`](../reports/blog/a_city_is_not_a_point.md). Bob’s voice/privacy pass before posting.
- LSN addendum with preview links: [`reports/lsn/research_project_summary.md`](../reports/lsn/research_project_summary.md).

## What this does not license

- Overlaying CHD/HF or stroke counts on cells or the 18 districts.
- Quoting lattice flags as HKO yearbook numbers.
- Treating the Peak series as a weather station.
- Moving the live paper off Headquarters.
