# Pearl River Delta field laboratory — 14 August 2026

**Mode:** Explore + Ship.  
**Provenance:** `REAL_PUBLIC` (Open-Meteo ERA5-Land daily 2 m temperatures, 2013–2023, the same 90-cell 0.2° cache as script 50).  
**Not:** health findings, prefecture maps, stroke, Gate 3, a climate-change detection, or a live-manuscript paste.

Interactive map: [`docs/field/index.html`](../docs/field/index.html).  
Rebuild: `python3 scripts/51_prd_field_laboratory.py`.  
Tests: `python3 scripts/test_51_prd_field_laboratory.py`.

## Why this exists

Bob asked to use methods an agent can run more densely than a human PhD usually will — many disciplines, one labelled field, no fake discoveries. Climate dynamics, geophysics, robust climatology, unsupervised learning, information theory, extremes, optimal transport, and network science all see the same 4,017 × 90 Tmin matrix. Panel reporting, not eight press releases.

## Punchline numbers

| Object | Result | How to read it |
|---|---|---|
| EOF1 of *de-seasoned* daily Tmin | **92.1%** of variance; all loadings positive | A basin-wide pulse. Neighbouring cells share the weather. |
| EOF1 vs latitude / vs hot-night counts | r = **+0.78** / **−0.93** | Inland cells have the larger anomaly; the sea has the 28°C nights. Those are different maps. |
| First three EOFs | **96.2%** cumulative | EOF2 is a small residual (3.0%). North’s rule separates 1 from 2 (Bartlett n_eff ≈ 425). |
| Annual harmonic | Peak day **198–207** (mid-July) everywhere; marine amp **6.1°C**, highland **7.3°C** | The year turns together. The sea damps the swing. |
| k-means (k=4) | marine 17 cells, HN mean **444**; highland 10 cells, HN **0**, elev **295 m**; estuary 32; inland 31 | Labels are interpretive, not municipalities. |
| Spatial evenness of hot-night occupancy | **0.735** (1 = spread evenly) | 28°C nights are concentrated, not a delta-wide event. |
| Theil–Sen on 11 yearly means | median **+0.29°C/decade**; **23/90** CIs exclude 0; **0/90** survive BH at 10% | A window slope, not a detection. Do not paste into the live paper. |
| Anomaly-correlation network (r > 0.90) | **2,428** edges; mean degree **54** | The de-seasoned field is coherent. That is EOF1 again. |
| P(HN \| VHD) | marine **0.43**; Guangzhou box **0.03** | A very hot day is often a hot night on the water, rarely inland. |
| HQ–Waglan / HQ–Guangzhou anomaly r | **0.93** / **0.89** | Same pulse, slightly weaker up-river. |

## What this does not license

- EOF loadings as hospitalisation factors.
- k-means names as neighbourhoods or catchments.
- Theil–Sen as a climate-change result for Hogan’s weather Methods.
- Transporting Hong Kong CHD/HF ratios.
- Overlaying health counts on cells.

The live paper stays on **HKO Headquarters**. This page is a public companion.

## Relation to the mosaic (script 50)

Script 50 mapped where the 28°C threshold occurred in this ERA5-Land sample: mainly marine cells, with little inland occurrence. It also fitted OLS/SLX/SAR. Script 51 asks what *kind of object* the field is once you look at every day. The mosaic is a spatial model of climatology. The laboratory is a space-time decomposition of the same cache.
