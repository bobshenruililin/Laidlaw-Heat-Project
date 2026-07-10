#!/usr/bin/env Rscript
# run_pipeline.R — execute scripts 00–13 in order

scripts <- sprintf("scripts/%02d_%s.R", 0:13, c(
  "setup",
  "download_or_import_weather",
  "build_weather_monthly",
  "download_or_import_pollution",
  "build_pollution_monthly",
  "build_population_denominators",
  "build_confounders",
  "simulate_ha_outcomes",
  "merge_analysis_panel",
  "descriptive_tables",
  "descriptive_figures",
  "fit_main_models_synthetic",
  "model_diagnostics",
  "make_report_outputs"
))

# Actual filenames differ slightly — use explicit list
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
  "scripts/13_make_report_outputs.R"
)

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)

for (s in scripts) {
  message("\n========== RUNNING ", s, " ==========\n")
  rc <- system2("Rscript", s)
  if (rc != 0) stop("Pipeline failed at ", s, " (exit ", rc, ")")
}

message("\nPipeline completed successfully.")
