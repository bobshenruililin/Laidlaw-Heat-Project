# Readiness gap analysis — can we run 10+ pathways when HA data arrive?

**Date:** 2026-07-21  
**Verdict before this branch:** **No** — exposures were largely ready, but outcome contracts and modelling still assumed diagnosis-stratified AMI/IS/HS, and there was no executable multi-pathway panel.  
**Verdict after this branch:** **Yes for dry-run** — **15 pathways OK** on SYNTHETIC stroke aggregates with real climate/pollution/flu exposures. **Ready for real aggregates** that match `schemas/ha_stroke_aggregate.schema.json`. Place file → `PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R`.

---

## What was already strong

| Asset | Status |
|---|---|
| HKO monthly climate + extremes + Ren/Wang spell/2D3N metrics | Ready |
| C&SD age–sex denominators | Ready |
| EPD EPIC NO₂/O₃/PM₂.₅/PM₁₀ monthly general means | Ready (merged) |
| Meeting recalibration (stroke aggregates; ~10 methods) | Documented |
| Decision gates / assumption ledger | Present |
| Literature review PDF | Present |

---

## Critical gaps (pre-fix)

1. **Schema mismatch:** `ha_monthly_aggregate.schema.json` required `diagnosis_group ∈ {AMI, IS, HS}` — incompatible with “no admission reasons” + stroke aggregates.
2. **Model mismatch:** `11_fit_main_models_*.R` hard-coded diagnosis strata and only one hot-night/cold-day ladder.
3. **No pathway registry** executable by code — methods lived only in the debrief markdown.
4. **No lag-1 exposure columns** and study climate started at 2013-01 without Dec-2012 join.
5. **No dedicated stroke ingest/QC** for flexible grains (territory-month vs age×sex).
6. **No manuscript panel exporter** labelling every estimate by pathway ID.
7. **Flu / official holidays** still scaffold — pathways that need them must stay optional.
8. **Pollution PR had not landed on main** (fixed by merge into this branch).

---

## Fixes implemented on this branch

| Gap | Fix |
|---|---|
| Schema | `schemas/ha_stroke_aggregate.schema.json` + flexible ingest |
| Pathways | `analysis_plan/pathway_registry.yml` + catalogue (P01–P16) |
| Lag exposures | `scripts/19_build_analysis_exposures.R` (Dec 2012 + lag1 + HW-month indicators) |
| Synthetic stroke | `scripts/07b_simulate_stroke_aggregates.R` |
| QC / merge | `scripts/08c_qc_stroke_aggregates.R`, `scripts/08d_merge_stroke_panel.R` |
| Multi-pathway fit | `scripts/20_fit_pathway_panel.R` — **15 pathways OK** on dry-run |
| Orchestrator | `scripts/run_pathway_pipeline.R` |
| Literature map | `literature/pathway_evidence_memo.md` |
| Flu | CHP Flu Express monthly positivity → P14 |
| Holidays | Deterministic scaffold v2 (`06b_build_hk_holidays.R`) |
| TV pathway | P15 monthly Tmax–Tmin range proxy |
| Pollution | Merged real EPD EPIC series |

---

## Still depends on humans / data arrival

1. Actual stroke aggregate files (grain, subtype, suppression rules).
2. PI governance / IRB determination for use.
3. Optional: official holiday gazette calendar (scaffold is deterministic but not official).
4. Gate 3 headline freeze after first real descriptives.
5. Do **not** claim AMI findings from general HA without reasons.
6. Flu coverage is 121/132 months — document missing months in real write-up.

---

## Scientist operating rule

When files arrive: place under `data_raw/ha_secure_placeholder/` → run `Rscript scripts/run_pathway_pipeline.R` → read `outputs/reports/pathway_panel_summary.md`. Synthetic mode proves the plumbing; real mode refuses SYNTHETIC outcomes.
