#!/usr/bin/env Rscript
# run_pipeline_real.R — real-data track (requires approved HA aggregate)
#
# Skips synthetic outcome simulation and synthetic model fits.
# Fails clearly until Roro's approved extract is present.

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)
Sys.setenv(HK_THERMAL_PIPELINE_MODE = "real")

scripts <- c(
  "scripts/00_setup.R",
  "scripts/01_download_or_import_weather.R",
  "scripts/02_build_weather_monthly.R",
  "scripts/03_download_or_import_pollution.R",
  "scripts/04_build_pollution_monthly.R",
  "scripts/05_build_population_denominators.R",
  "scripts/06_build_confounders.R",
  "scripts/08b_merge_real_ha_panel.R",
  "scripts/09_descriptive_tables.R",
  "scripts/10_descriptive_figures.R",
  "scripts/11_fit_main_models_real.R",
  "scripts/12_model_diagnostics_real.R",
  "scripts/13_make_report_outputs.R",
  "scripts/14_hko_annual_extremes_figure.R",
  "scripts/15_smoke_checks.R"
)

for (s in scripts) {
  message("\n========== RUNNING ", s, " ==========\n")
  rc <- system2("Rscript", s)
  if (rc != 0) stop("Real pipeline failed at ", s, " (exit ", rc, ")")
}

message("\nReal pipeline completed successfully.")
