# Thermal Extremes, Aging, Pollution, and Cardiovascular Admissions in Hong Kong (2013–2023)

Reproducible first-stage research pipeline for an ecological time-series study of officially defined thermal extremes (especially **hot nights** and **cold days**) and cardiovascular hospital admissions among Hong Kong residents aged 35+, with attention to population aging, air pollution, and COVID-period disruption.

> **Framing:** In Hong Kong from 2013–2023, how do officially defined thermal extremes — especially hot nights and cold days — relate to cardiovascular hospital admissions in an aging population, and do these contemporary patterns differ from the historically cold-dominant risk profile reported in earlier Hong Kong studies?

## Status (first-stage)

| Component | Status |
|---|---|
| Public HKO weather pipeline | Executable; daily extracts downloaded |
| Population denominators | Scripted; C&SD API requires interactive `param` — see import notes |
| Pollution | Import scripts + placeholder/manual EPIC workflow |
| HA clinical outcomes | **Not available** — synthetic panel only |
| First-stage exploratory report | `reports/first_stage_exploratory_report.md` |

**Hospital Authority outcome data were not available for this first-stage report; all outcome-modeling demonstrations use synthetic data only.**

## Project structure

```text
.
├── README.md
├── config.yml
├── analysis_plan/
├── data_raw/
│   ├── hko/
│   ├── epd/
│   ├── csd_population/
│   ├── chp_flu/
│   └── ha_secure_placeholder/
├── data_processed/
├── scripts/
├── outputs/
│   ├── tables/
│   ├── figures/
│   ├── model_objects/
│   ├── table_shells/
│   └── figure_shells/
├── memos/
├── reports/
└── manuscript/
```

## Quick start

```bash
# From repository root
Rscript scripts/00_setup.R
Rscript scripts/01_download_or_import_weather.R
Rscript scripts/02_build_weather_monthly.R
Rscript scripts/03_download_or_import_pollution.R
Rscript scripts/04_build_pollution_monthly.R
Rscript scripts/05_build_population_denominators.R
Rscript scripts/06_build_confounders.R
Rscript scripts/07_simulate_ha_outcomes.R
Rscript scripts/08_merge_analysis_panel.R
Rscript scripts/09_descriptive_tables.R
Rscript scripts/10_descriptive_figures.R
Rscript scripts/11_fit_main_models_synthetic.R
Rscript scripts/12_model_diagnostics.R
Rscript scripts/13_make_report_outputs.R
```

Or run the driver:

```bash
Rscript scripts/run_pipeline.R
```

## Key exposure definitions (HKO)

| Metric | Definition |
|---|---|
| Hot night | Daily minimum temperature ≥ 28°C |
| Very hot day | Daily maximum temperature ≥ 33°C |
| Extremely hot day | Daily maximum temperature ≥ 35°C |
| Cold day | Daily minimum temperature ≤ 12°C |

Primary heat metric: **monthly number of hot nights**.

## Team roles

- **Professor Bishai / Dr. Bishai** — senior investigator
- **Bob** — student/scholar analyst (R pipeline)
- **Hogan** — climate and pollution variables
- **Roro** — Hospital Authority / clinical data access

## Important documents

- `reports/initial_exploration_note.md` — Phase-1 source exploration
- `reports/first_stage_exploratory_report.md` — first-stage exploratory report
- `analysis_plan/assumption_ledger.md` — assumptions and confirmation checklist
- `memos/data_request_roro.md` — HA data request
- `memos/environmental_data_request_hogan.md` — climate/pollution request
- `memos/literature_baseline.md` — literature baseline
- `manuscript/methods_draft.md` — draft Methods section

## Standards

1. Do not fabricate HA data; label all synthetic outputs `data_status = "SYNTHETIC"`.
2. Do not overclaim causality; this is an ecological time-series design.
3. Preserve raw files; never overwrite `data_raw/`.
4. Keep assumptions explicit in the assumption ledger.
5. Prefer staged pollution models; treat ozone cautiously as a potential pathway variable.
