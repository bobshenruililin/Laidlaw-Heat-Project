# Model 2 / Model 3 drop-in

Governed CHD/HF monthly panels are gitignored and are not in this checkout. Do not type coefficients. Do not digitize Figure 1.

## Files to place (local only; never commit)

```
data_processed/chd_analysis_panel.csv
data_processed/hf_analysis_panel.csv
```

Same schema as the 7 August real run (`n_events`, official day counts, `month_id`, `data_status = HA_APPROVED_AGGREGATE`, 132 rows).

## Then run

```bash
Rscript scripts/53_hogan_models_rh_rain.R
Rscript scripts/68_hogan_model3_climatology.R
```

or:

```bash
python3 scripts/62_fit_hogan_model2_model3.py
```

## Outputs (do not overwrite Table 2)

| Script | Writes |
|---|---|
| 53 | `outputs/tables/table2_models_1_12_rh_rain.csv` (Model 2). Leaves `outputs/release_chd_hf/tables/table2_core_models.csv` as Model 1 |
| 68 | `outputs/tables/table_model3_climatology_primary.csv` (four primary warmer/cooler rows) |

Weather already on disk: monthly RH and rainfall in `data_processed/climate_monthly_2013_2023.csv`; climatology day counts in `data_processed/hogan_climatology_day_counts_2013_2023.csv`.
