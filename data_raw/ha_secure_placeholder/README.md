# Hospital Authority secure data placeholder

Place de-identified aggregate HA extracts here only inside an approved secure environment.

**Do not commit real HA data to git.**

Expected filename example:

```text
ha_monthly_cvd_admissions_2013_2023.csv
```

Required minimum columns are documented in `memos/data_request_roro.md` and `data_processed/variable_dictionary.csv`.

Until a real extract arrives, the pipeline uses:

```text
data_processed/synthetic_ha_outcomes.csv
data_processed/synthetic_analysis_panel.csv
```

with `data_status = "SYNTHETIC"`.
