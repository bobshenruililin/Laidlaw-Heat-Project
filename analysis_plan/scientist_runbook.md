# Scientist runbook — from HA file to pathway panel

## Before real data

```bash
Rscript scripts/run_pathway_pipeline.R
Rscript scripts/15b_pathway_smoke_checks.R
```

Expect **≥14 pathways OK**, all estimates labelled `SYNTHETIC`.

## When stroke aggregates arrive

1. Confirm PI/governance path for use.
2. Place CSV in `data_raw/ha_secure_placeholder/` (never commit microdata).
3. Match columns to `schemas/ha_stroke_aggregate.schema.json` (minimum: `month_id`, `n_events`).
4. Run:

```bash
PATHWAY_MODE=real Rscript scripts/run_pathway_pipeline.R
```

5. Read:
   - `outputs/reports/stroke_data_qc_receipt.md`
   - `outputs/reports/pathway_panel_summary.md`
   - `outputs/tables/pathway_panel_estimates.csv`

6. Gate 3: freeze headline pair (proposal **P02 + P04**) before manuscript claims.
7. If subtype exists, enable `P13` in `analysis_plan/pathway_registry.yml` and re-run fit.

## Pathway families (short)

| IDs | Family |
|---|---|
| P01–P03 | Continuous temperature / lag |
| P04–P07 | Extremes, spells, 2D3N, heatwave-month |
| P08 | Cold-primary |
| P09–P10 | Age / COVID–holiday sensitivities |
| P11–P12 | Pollution-staged / absolute humidity |
| P13 | Subtype (optional) |
| P14–P16 | Flu, temperature variability, pre-COVID |

## Honesty rules

- Monthly burden ≠ daily DLNM ≠ excess deaths.
- No AMI claims without admission reasons.
- Panel reporting, not ten independent discoveries.
