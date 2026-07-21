# Readiness gap analysis — can we run 10+ pathways when HA data arrive?

**Date:** 2026-07-21 (updated after SAP + P17/P18 + diagnostics pass)  
**Verdict before pathway branch:** **No** — exposures ready-ish, but outcome contracts and modelling assumed AMI/IS/HS diagnosis strata; no executable multi-pathway panel.  
**Verdict now:** **Yes for dry-run and for real aggregates matching the schema.** **17 pathways enabled** (P01–P12, P14–P18); P13 waits on subtype. Place file → `PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R`.

---

## What was already strong

| Asset | Status |
|---|---|
| HKO monthly climate + extremes + Ren/Wang spell/2D3N metrics | Ready |
| C&SD age–sex denominators | Ready |
| EPD EPIC NO₂/O₃/PM₂.₅/PM₁₀ monthly general means | Ready |
| Meeting recalibration (stroke aggregates; ~10 methods) | Documented |
| Decision gates / assumption ledger | Present |
| Literature review PDF | Present |

---

## Critical gaps (pre-fix) → closed

| Gap | Fix |
|---|---|
| Schema mismatch (AMI/IS/HS required) | `schemas/ha_stroke_aggregate.schema.json` |
| Single-model scripts | `scripts/20_fit_pathway_panel.R` + registry |
| No pathway catalogue / SAP | catalogue + `statistical_analysis_protocol.md` |
| No lag-1 / HW-month exposures | `scripts/19_build_analysis_exposures.R` (p90/p95/p975 + daily TV) |
| No stroke ingest/QC | `08c` / `08d` |
| No manuscript exporter / forest / diagnostics | `22` / `23` / `24` |
| Flu / holidays | CHP Flu Express + deterministic holiday scaffold v2 |
| Pollution not on main | Merged into this branch |

---

## Still depends on humans / data arrival

1. Actual stroke aggregate files (grain, subtype, suppression rules).
2. PI governance / IRB determination for use.
3. Optional: official holiday gazette (scaffold is deterministic, not gazette).
4. Gate 3 headline freeze after first real descriptives (**proposal: P02 + P04**).
5. Do **not** claim AMI findings from general HA without reasons.
6. Flu coverage **121/132** months — P14 uses complete-case and documents the gap.
7. Enable P13 only if IS/HS fields exist.

---

## Scientist operating rule

When files arrive: place under `data_raw/ha_secure_placeholder/` → run `PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R` → read QC receipt + pathway summary + forest. Synthetic mode proves plumbing; real mode refuses SYNTHETIC outcomes.

See also: `analysis_plan/scientist_runbook.md`, `analysis_plan/statistical_analysis_protocol.md`.
