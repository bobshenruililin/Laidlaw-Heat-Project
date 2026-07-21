# Scientist runbook — from HA file to pathway panel

## Before real data

```bash
Rscript scripts/run_pathway_pipeline.R
```

Expect **≥16 pathways OK** (P13 disabled), all estimates labelled `SYNTHETIC`, plus:

- `outputs/figures/pathway/pathway_panel_forest.png`
- `outputs/tables/manuscript_pathway_panel_table.csv`
- `outputs/tables/pathway_headline_diagnostics.csv`

## When stroke aggregates arrive

1. Confirm PI/governance path for use.
2. Place CSV in `data_raw/ha_secure_placeholder/` (never commit microdata).
3. Match columns to `schemas/ha_stroke_aggregate.schema.json` (minimum: `month_id`, `n_events`).
4. Run:

```bash
PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R
```

5. Read:
   - `outputs/reports/stroke_data_qc_receipt.md` (Gate 2)
   - `outputs/reports/pathway_panel_summary.md`
   - `outputs/tables/pathway_panel_estimates.csv`
   - Forest + diagnostics under `outputs/`

6. Gate 3: freeze headline pair (proposal **P02 + P04**) in the assumption ledger before manuscript claims.
7. If subtype exists, set `P13.enabled: true` in `pathway_registry.yml` and re-run fit.

## Pathway families (short)

| IDs | Family |
|---|---|
| P01–P03 | Continuous temperature / lag |
| P04–P07 | Extremes, spells, 2D3N, multi-def heatwave-month |
| P08, P18 | Cold-primary / cold-month |
| P09, P17 | Age / sex structure |
| P10–P12 | COVID–holiday / pollution / humidity |
| P13 | Subtype (optional) |
| P14–P16 | Flu, TV, pre-COVID |

## Honesty rules

- Monthly burden ≠ daily DLNM ≠ excess deaths.
- No AMI claims without admission reasons.
- Panel reporting, not ten independent discoveries.
- Follow `analysis_plan/statistical_analysis_protocol.md`.
