#!/usr/bin/env Rscript
# 08b_merge_real_ha_panel.R
# Merge approved HA aggregate extract with environmental / population panels.
# Refuses to proceed without a non-synthetic HA file.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

ha_dir <- file.path(root, "data_raw", "ha_secure_placeholder")
candidates <- list.files(
  ha_dir,
  pattern = "ha_monthly.*\\.(csv|CSV)$",
  full.names = TRUE
)
candidates <- candidates[!grepl("SYNTHETIC|PLACEHOLDER|mock", basename(candidates), ignore.case = TRUE)]

if (!length(candidates)) {
  stop(
    "Real pipeline requires an approved HA aggregate CSV in ", ha_dir, "\n",
    "Expected name pattern: ha_monthly_cvd_admissions_2013_2023.csv\n",
    "Schema: schemas/ha_monthly_aggregate.schema.json\n",
    "Until Roro delivers the extract, use: Rscript scripts/run_pipeline_dev.R"
  )
}

ha_path <- candidates[1]
message("Using HA extract: ", ha_path)
outcomes <- utils::read.csv(ha_path, stringsAsFactors = FALSE)
validate_required_columns(
  outcomes,
  c("month_id", "age_group", "sex", "diagnosis_group", "n_events"),
  "HA extract"
)
assert_month_id(outcomes$month_id)

if (!"data_status" %in% names(outcomes)) {
  outcomes$data_status <- "HA_APPROVED_AGGREGATE"
}
stop_if_synthetic(outcomes)

# Suppression: never treat suppressed cells as zero
if ("suppression_flag" %in% names(outcomes)) {
  outcomes$n_events[outcomes$suppression_flag %in% c(TRUE, "TRUE", "true", 1, "1")] <- NA_integer_
}

climate <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                           stringsAsFactors = FALSE)
pollution <- utils::read.csv(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"),
                             stringsAsFactors = FALSE)
pop <- utils::read.csv(file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"),
                       stringsAsFactors = FALSE)
conf <- utils::read.csv(file.path(root, "data_processed", "confounders_monthly_2013_2023.csv"),
                        stringsAsFactors = FALSE)
months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

if (any(grepl("SYNTHETIC", pop$data_status %||% ""))) {
  stop("Real pipeline refuses SYNTHETIC_DENOMINATOR population. Import C&SD first.")
}
if (any(grepl("PLACEHOLDER", pollution$data_status %||% ""))) {
  warning("Pollution series still PLACEHOLDER — staged pollution models not inferential.")
}

clim_cols <- intersect(c(
  "month_id", "mean_temp", "mean_tmin", "mean_tmax",
  "hot_nights", "very_hot_days", "extremely_hot_days", "cold_days",
  "longest_hot_night_run", "longest_very_hot_run", "longest_cold_run",
  "relative_humidity", "absolute_humidity", "rainfall", "dew_point",
  "max_hot_night_spell_touching", "max_very_hot_spell_touching", "max_cold_spell_touching",
  "days_in_hot_night_spell_ge3", "days_in_hot_night_spell_ge5",
  "days_in_very_hot_spell_ge2", "days_in_very_hot_spell_ge5",
  "days_in_2d3n_window", "month_has_2d3n_window"
), names(climate))

if ("data_status" %in% names(pollution)) {
  names(pollution)[names(pollution) == "data_status"] <- "pollution_data_status"
}
pol_cols <- intersect(
  c("month_id", "NO2", "O3", "PM25", "PM10", "pollution_data_status"),
  names(pollution)
)
conf_cols <- intersect(
  c("month_id", "covid_phase", "chinese_new_year_month", "public_holiday_days",
    "flu_indicator", "typhoon_signal_days"),
  names(conf)
)
pop_cols <- intersect(
  c("month_id", "age_group", "sex", "population", "data_status"),
  names(pop)
)
if ("data_status" %in% pop_cols) {
  names(pop)[names(pop) == "data_status"] <- "population_data_status"
  pop_cols <- intersect(
    c("month_id", "age_group", "sex", "population", "population_data_status"),
    names(pop)
  )
}

panel <- outcomes |>
  dplyr::left_join(pop[, pop_cols, drop = FALSE], by = c("month_id", "age_group", "sex")) |>
  dplyr::left_join(climate[, clim_cols, drop = FALSE], by = "month_id") |>
  dplyr::left_join(pollution[, pol_cols, drop = FALSE], by = "month_id") |>
  dplyr::left_join(conf[, conf_cols, drop = FALSE], by = "month_id") |>
  dplyr::left_join(months, by = "month_id") |>
  dplyr::mutate(
    offset_log = log(population * days_in_month),
    stratum_id = interaction(age_group, sex, diagnosis_group, drop = TRUE),
    age_group = factor(age_group, levels = cfg$population$preferred_age_groups),
    sex = factor(sex, levels = cfg$sexes),
    diagnosis_group = factor(diagnosis_group, levels = cfg$diagnosis_groups),
    covid_phase = factor(covid_phase, levels = names(cfg$covid_phases))
  )

stopifnot(!any(duplicated(panel[, c("month_id", "age_group", "sex", "diagnosis_group")])))
stop_if_synthetic(panel)

out_path <- file.path(root, "data_processed", "ha_analysis_panel.csv")
write_csv_safe(panel, out_path)
message("Merged REAL analysis panel: ", nrow(panel), " rows -> ", out_path)
