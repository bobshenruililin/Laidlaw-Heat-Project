# Grok second cut of the PRD field — 14 August 2026

**Model:** parent, Cursor Grok 4.6 (this session).  
**Mode:** Explore.  
**Provenance:** `REAL_PUBLIC`, script 50 cache, `scripts/52_prd_strong_cut.py`.  
**Not:** health findings, climate-change detections, or a live-manuscript paste.

This is the “yourself” arm of [`2026-08-14_strong_model_experiment.md`](2026-08-14_strong_model_experiment.md). Luna and Sol were launched in parallel.

## What was fragile in script 51

| Script 51 claim | After the harder cut | Keep? |
|---|---|---|
| EOF1 = 92.1%, all loadings positive | Year-holdout pattern r ≥ **0.999**; variance **0.918–0.923**. 10-day block bootstrap 5–95% **0.915–0.926** | **Robust.** The pulse is the field. |
| r(EOF1, HN) = −0.93 | Not re-tested; follows from climatology vs anomaly | Keep as a reading, not a new test |
| Harmonic peak day 198–207 | Circular mean day **201.4**; SD **2.5** days; marine vs Guangzhou **4.4** days | **Robust.** The year turns together. |
| 23/90 Theil–Sen CIs exclude 0 | Raw MK p < 0.10: **24** cells. BH at 10%: **0** cells. Minimum p = **0.013** (BH hurdle 0.0011). n=11 | **Fragile.** Drop as a headline. Eleven years cannot support a spatial trend map. |
| Network r > 0.90, mean degree 54 | Same object as EOF1 | Dead end as a separate finding |
| P(HN \| VHD) marine 0.43 vs GZ 0.03 | Still true, and incomplete | Keep, but add the reverse conditional |

## New sentence

On the water, a 28°C night is a common climatology and is usually **not** a 33°C day (P(VHD \| HN) ≈ **0.008**). In the Guangzhou box, a 28°C night is rare and is almost always a 33°C day (P(VHD \| HN) ≈ **0.97**, 140/145 nights). The huge Guangzhou odds ratio is a rarity artefact. HQ vs Guangzhou de-seasoned Tmin peaks at **lag 0** (r = 0.89); nobody leads by a day.

Hogan one-liner: a 28°C night on this grid is a **marine mean**, not a synoptic pulse and not an inland compound extreme.

## Dead ends

- Lagged teleconnection as a story (peak is lag 0).
- Quoting Guangzhou OR = 349 without n10 = 5.
- Treating 23/90 CIs as detections.
- Recomputing EOF without holding out the climatology (the year-holdout here rebuilds the seasonal cycle each fold; it did not matter).
