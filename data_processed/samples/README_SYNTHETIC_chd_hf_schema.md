# SYNTHETIC CHD/HF schema (Playbook 08 / DUA mocking)

**Provenance:** `SYNTHETIC`. Eight mock months. Column names match `scripts/final_model_helpers.R` `.panel_required_columns` plus Hogan Model 2 covariates.

Do **not** treat `n_events` as Hospital Authority counts. Real panels are gitignored and must not be reconstructed from Figure 1.

| Column | Type | Role |
|---|---|---|
| `month_id` | YYYY-MM | Time key |
| `year`, `month`, `time_index` | integer | Trend / factors |
| `n_events` | integer | Mock counts |
| `data_status` | string | Always `SYNTHETIC` in this file |
| `days_in_month` | integer | Offset |
| `mean_temp`, `mean_tmax`, `mean_tmin` | °C | Continuous exposures |
| `hot_nights`, `cold_days`, `very_hot_days` | integer | Official-day counts |
| `relative_humidity`, `rainfall` | numeric | Model 2 (specified, not fitted on real data here) |
