# Input schemas

Machine-readable contracts for collaborator files. Validators in `scripts/utils.R`.

| File | Owner | Used by |
|---|---|---|
| `ha_stroke_aggregate.schema.json` | Roro / Bob | `08c_qc_stroke_aggregates.R`, pathway pipeline (**primary**) |
| `ha_monthly_aggregate.schema.json` | Legacy | Older AMI/IS/HS stratified design — demoted after 17 Jul meeting |
| `epd_monthly.schema.json` | Bob | `04_build_pollution_monthly.R` |
| `csd_population_annual.schema.json` | Bob | `05_build_population_denominators.R` |
