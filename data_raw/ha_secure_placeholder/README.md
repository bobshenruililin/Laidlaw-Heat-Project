# HA secure staging (local only)

Place approved **stroke admission aggregates** here for analysis.  
**Never commit real patient-level or restricted extracts.**

This directory is gitignored except for this README.

## Expected near-term file

Example name: `ha_stroke_aggregates_2013_2023.csv`

Minimum columns (see `schemas/ha_stroke_aggregate.schema.json`):

| Column | Required | Notes |
|---|---|---|
| `month_id` | yes | `YYYY-MM` |
| `n_events` | yes | admission counts |
| `age_group` | optional | if absent/all → territory-month models |
| `sex` | optional | Female/Male |
| `stroke_type` | optional | `stroke_all` default; IS/HS enable pathway P13 |
| `data_status` | recommended | `HA_APPROVED_AGGREGATE` |
| `suppression_flag` | if used | never treat suppressed as zero |

## Run after drop-in

```bash
PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R
```

Strategy docs: `reports/meeting_debrief_2026-07-17.md`, `analysis_plan/pathway_catalogue.md`.
