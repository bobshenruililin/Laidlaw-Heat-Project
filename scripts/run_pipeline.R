#!/usr/bin/env Rscript
# run_pipeline.R — execute scripts 00–14 in order

scripts <- c(
  "scripts/00_setup.R",
  "scripts/01_download_or_import_weather.R",
  "scripts/02_build_weather_monthly.R",
  "scripts/03_download_or_import_pollution.R",
  "scripts/04_build_pollution_monthly.R",
  "scripts/05_build_population_denominators.R",
  "scripts/06_build_confounders.R",
  "scripts/07_simulate_ha_outcomes.R",
  "scripts/08_merge_analysis_panel.R",
  "scripts/09_descriptive_tables.R",
  "scripts/10_descriptive_figures.R",
  "scripts/11_fit_main_models_synthetic.R",
  "scripts/12_model_diagnostics.R",
  "scripts/13_make_report_outputs.R",
  "scripts/14_hko_annual_extremes_figure.R"
)

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)

for (s in scripts) {
  message("\n========== RUNNING ", s, " ==========\n")
  rc <- system2("Rscript", s)
  if (rc != 0) stop("Pipeline failed at ", s, " (exit ", rc, ")")
}

message("\nPipeline completed successfully.")
