#!/usr/bin/env Rscript
# 13_make_report_outputs.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

# Table shells
shell_dir <- file.path(root, "outputs", "table_shells")
dir.create(shell_dir, recursive = TRUE, showWarnings = FALSE)

shells <- list(
  table01_data_sources = data.frame(
    domain = c("Weather", "Pollution", "Population", "Outcomes", "Confounders"),
    source = c("HKO dailyExtract / open data", "EPD EPIC", "C&SD 110-01002", "Hospital Authority", "CHP/COVID/holidays"),
    status = c("Built", "Manual/placeholder", "Manual/synthetic scaffold", "Not available — synthetic only", "Partial"),
    key_variables = c(
      "hot_nights, very_hot_days, cold_days, temps, RH, rainfall",
      "NO2, O3, PM25, PM10",
      "age-sex population",
      "n_events by age/sex/dx",
      "covid_phase, holidays, flu"
    ),
    stringsAsFactors = FALSE
  ),
  table02_descriptive_by_period = data.frame(
    period = c("pre_covid", "covid_2020_2022", "post_reopening_2023"),
    mean_temp = NA, hot_nights = NA, cold_days = NA, NO2 = NA, O3 = NA,
    notes = "Fill from descriptive_weather_by_period.csv / pollution tables",
    stringsAsFactors = FALSE
  ),
  table03_weather_trends = data.frame(
    year = 2013:2023,
    hot_nights = NA, very_hot_days = NA, extremely_hot_days = NA, cold_days = NA, mean_temp = NA,
    stringsAsFactors = FALSE
  ),
  table04_pollution_trends = data.frame(
    year = 2013:2023, NO2 = NA, O3 = NA, PM25 = NA, PM10 = NA,
    notes = "Requires real EPD series",
    stringsAsFactors = FALSE
  ),
  table05_population_by_age = data.frame(
    age_group = cfg$population$preferred_age_groups,
    pop_2013 = NA, pop_2023 = NA, abs_change = NA, pct_change = NA,
    stringsAsFactors = FALSE
  ),
  table06_main_nb_results = data.frame(
    exposure = c("Hot nights (per 5)", "Cold days (per 5)", "Very hot days (per 5)", "Mean Tmin (per 1C)"),
    rr = NA, rr_low = NA, rr_high = NA, p_value = NA,
    notes = "Real HA results TBD; synthetic demo in synthetic_model_results.csv",
    stringsAsFactors = FALSE
  ),
  table07_age_stratified_rr = data.frame(
    age_group = cfg$population$preferred_age_groups,
    rr_hot_nights = NA, rr_cold_days = NA,
    stringsAsFactors = FALSE
  ),
  table08_diagnosis_specific = data.frame(
    diagnosis_group = cfg$diagnosis_groups,
    rr_hot_nights = NA, rr_cold_days = NA,
    stringsAsFactors = FALSE
  ),
  table09_sensitivity_analyses = data.frame(
    analysis = c(
      "Poisson vs NB", "Exclude 2020-2022", "Pre-COVID only", "Lag-1 month",
      "Alternative heat metrics", "With/without pollutants", "Multi-pollutant",
      "Age grouping alternatives", "ED vs inpatient", "Optional 2024 extension"
    ),
    result_summary = NA,
    stringsAsFactors = FALSE
  )
)

for (nm in names(shells)) {
  write_csv_safe(shells[[nm]], file.path(shell_dir, paste0(nm, ".csv")))
}

# Populate weather trend shell from real climate annual table if present
ann_path <- file.path(root, "outputs", "tables", "weather_annual_extremes_2013_2023.csv")
if (file.exists(ann_path)) {
  ann <- utils::read.csv(ann_path, stringsAsFactors = FALSE)
  write_csv_safe(ann, file.path(shell_dir, "table03_weather_trends_FILLED.csv"))
}

# Session info
writeLines(capture.output(sessionInfo()), file.path(root, "outputs", "session_info_final.txt"))

# Short pipeline status note for the report appendix
status <- c(
  paste("pipeline_completed_at:", as.character(Sys.time())),
  paste("climate_monthly:", file.exists(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"))),
  paste("pollution_monthly:", file.exists(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"))),
  paste("population_monthly:", file.exists(file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"))),
  paste("synthetic_panel:", file.exists(file.path(root, "data_processed", "synthetic_analysis_panel.csv"))),
  paste("synthetic_model_results:", file.exists(file.path(root, "outputs", "tables", "synthetic_model_results.csv"))),
  "ha_data: NOT_AVAILABLE"
)
writeLines(status, file.path(root, "outputs", "pipeline_status.txt"))
message("Report outputs / table shells written.")
