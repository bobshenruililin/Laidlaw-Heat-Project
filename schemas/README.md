# Input schemas

Machine-readable contracts for collaborator files. R validators in `scripts/utils.R`
(`validate_required_columns`, `assert_month_id`) enforce the required fields at
import time. JSON Schema files document the full intended shape for Hogan/Roro.

| File | Owner | Used by |
|---|---|---|
| `ha_monthly_aggregate.schema.json` | Roro | Future `08b_merge_real_ha_panel.R` |
| `epd_monthly.schema.json` | Hogan / Bob | `04_build_pollution_monthly.R` |
| `csd_population_annual.schema.json` | Bob (public MDT) | `05_build_population_denominators.R` |
