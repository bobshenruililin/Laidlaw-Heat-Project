#!/usr/bin/env Rscript
# 08_merge_analysis_panel.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

outcomes <- utils::read.csv(file.path(root, "data_processed", "synthetic_ha_outcomes.csv"),
                            stringsAsFactors = FALSE)
climate <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                           stringsAsFactors = FALSE)
pollution <- utils::read.csv(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"),
                             stringsAsFactors = FALSE)
conf <- utils::read.csv(file.path(root, "data_processed", "confounders_monthly_2013_2023.csv"),
                        stringsAsFactors = FALSE)
months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

# Keep outcome data_status; track other statuses separately
clim_cols <- c(
  "month_id", "mean_temp", "mean_tmin", "mean_tmax",
  "hot_nights", "very_hot_days", "extremely_hot_days", "cold_days",
  "longest_hot_night_run", "longest_very_hot_run",
  "relative_humidity", "rainfall", "dew_point",
  "max_hot_night_spell_touching", "max_very_hot_spell_touching"
)
clim_cols <- intersect(clim_cols, names(climate))

if ("data_status" %in% names(pollution)) {
  names(pollution)[names(pollution) == "data_status"] <- "pollution_data_status"
}
pol_cols <- intersect(
  c("month_id", "NO2", "O3", "PM25", "PM10", "pollution_data_status"),
  names(pollution)
)

conf_cols <- c("month_id", "covid_phase", "chinese_new_year_month", "public_holiday_days",
               "flu_indicator", "typhoon_signal_days")
conf_cols <- intersect(conf_cols, names(conf))

panel <- outcomes |>
  dplyr::select(-dplyr::any_of(c(
    "mean_temp", "mean_tmin", "mean_tmax", "hot_nights", "very_hot_days",
    "extremely_hot_days", "cold_days", "relative_humidity", "rainfall"
  ))) |>
  dplyr::left_join(climate[, clim_cols, drop = FALSE], by = "month_id") |>
  dplyr::left_join(pollution[, pol_cols, drop = FALSE], by = "month_id") |>
  dplyr::left_join(conf[, conf_cols, drop = FALSE], by = "month_id")

# Ensure time_index / days_in_month
panel <- panel |>
  dplyr::select(-dplyr::any_of(c("time_index", "days_in_month", "year", "month", "month_date"))) |>
  dplyr::left_join(months, by = "month_id")

panel <- panel |>
  dplyr::mutate(
    offset_log = log(population * days_in_month),
    stratum_id = interaction(age_group, sex, diagnosis_group, drop = TRUE),
    age_group = factor(age_group, levels = cfg$population$preferred_age_groups),
    sex = factor(sex, levels = cfg$sexes),
    diagnosis_group = factor(diagnosis_group, levels = cfg$diagnosis_groups),
    covid_phase = factor(covid_phase, levels = names(cfg$covid_phases))
  )

# Quality checks
stopifnot(!any(duplicated(panel[, c("month_id", "age_group", "sex", "diagnosis_group")])))
expected_months <- months$month_id
stopifnot(all(expected_months %in% unique(panel$month_id)))
stopifnot(!any(is.na(panel$population)))
stopifnot(all(panel$days_in_month %in% c(28L, 29L, 30L, 31L)))
stopifnot(all(is.na(panel$hot_nights) | (panel$hot_nights >= 0 & panel$hot_nights <= panel$days_in_month)))
stopifnot(all(is.na(panel$cold_days) | (panel$cold_days >= 0 & panel$cold_days <= panel$days_in_month)))
stop_if_not_synthetic(panel)

write_csv_safe(panel, file.path(root, "data_processed", "synthetic_analysis_panel.csv"))

# Variable dictionary
dict <- data.frame(
  variable = c(
    "month_id", "n_events", "population", "days_in_month", "offset_log",
    "hot_nights", "very_hot_days", "extremely_hot_days", "cold_days",
    "mean_temp", "mean_tmin", "mean_tmax", "relative_humidity", "rainfall",
    "NO2", "O3", "PM25", "PM10", "covid_phase", "data_status"
  ),
  description = c(
    "YYYY-MM month identifier",
    "Monthly event count (SYNTHETIC in this file)",
    "Age-sex population denominator",
    "Number of days in calendar month",
    "log(population * days_in_month)",
    "Count of days with Tmin >= 28C",
    "Count of days with Tmax >= 33C",
    "Count of days with Tmax >= 35C",
    "Count of days with Tmin <= 12C",
    "Monthly mean of daily mean temperature",
    "Monthly mean of daily minimum temperature",
    "Monthly mean of daily maximum temperature",
    "Monthly mean relative humidity (%)",
    "Monthly total rainfall (mm)",
    "Nitrogen dioxide (µg/m3 or placeholder)",
    "Ozone (µg/m3 or placeholder)",
    "PM2.5 (µg/m3 or placeholder)",
    "PM10 (µg/m3 or placeholder)",
    "COVID period phase",
    "Must equal SYNTHETIC for this development panel"
  ),
  stringsAsFactors = FALSE
)
write_csv_safe(dict, file.path(root, "data_processed", "variable_dictionary.csv"))

message("Merged synthetic analysis panel: ", nrow(panel), " rows")
