# HA secure staging (local only)

Place approved HA / stroke aggregate extracts here for local processing.  
**Never commit real patient-level or restricted extracts.**

This directory is gitignored except for this README.

Expected near-term inputs (post–17 July 2026): **stroke admission aggregates** (monthly ± age/sex if available). The general HA file available to this project does **not** specify reasons for admission.

Field contracts for future aggregates: `schemas/ha_monthly_aggregate.schema.json` and `data_processed/variable_dictionary.csv`.  
Working strategy: `reports/meeting_debrief_2026-07-17.md`.
