#!/usr/bin/env Rscript
# 02_build_weather_monthly.R
# Build monthly climate extremes from HKO dailyExtract files.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "jsonlite", "dplyr", "tidyr", "lubridate", "digest"))

extract_dir <- file.path(root, cfg$weather$sources$daily_extract_dir)
years <- seq(cfg$study$start_year, cfg$study$optional_extension_year %||% cfg$study$end_year)

# dailyExtract columns (HKO Headquarters):
# 1 day, 2 mean pressure, 3 tmax, 4 tmean, 5 tmin, 6 dew point,
# 7 RH%, 8 cloud%, 9 rainfall mm, 10 sunshine h, 11 wind dir, 12 wind speed
parse_year_extract <- function(path, year) {
  raw <- jsonlite::fromJSON(path, simplifyVector = FALSE)
  months <- raw$stn$data
  rows <- list()
  for (mobj in months) {
    mo <- as.integer(mobj$month)
    for (day_vec in mobj$dayData) {
      day_label <- trimws(as.character(day_vec[[1]]))
      if (!grepl("^[0-9]{1,2}$", day_label)) next
      day <- as.integer(day_label)
      rows[[length(rows) + 1]] <- data.frame(
        date = as.Date(sprintf("%04d-%02d-%02d", year, mo, day)),
        year = year,
        month = mo,
        day = day,
        pressure = parse_hko_number(day_vec[[2]]),
        tmax = parse_hko_number(day_vec[[3]]),
        tmean = parse_hko_number(day_vec[[4]]),
        tmin = parse_hko_number(day_vec[[5]]),
        dew_point = parse_hko_number(day_vec[[6]]),
        relative_humidity = parse_hko_number(day_vec[[7]]),
        cloud = parse_hko_number(day_vec[[8]]),
        rainfall = parse_hko_number(day_vec[[9]]),
        sunshine = parse_hko_number(day_vec[[10]]),
        stringsAsFactors = FALSE
      )
    }
  }
  dplyr::bind_rows(rows)
}

use_cache <- isTRUE(cfg$pipeline$weather_cache %||% TRUE)
if (use_cache && weather_cache_is_valid(root, extract_dir, years)) {
  message("Using cached daily weather parse (SHA match).")
  weather_daily <- load_weather_daily_cache(root)
} else {
  daily_list <- list()
  for (y in years) {
    path <- file.path(extract_dir, sprintf("dailyExtract_%d.xml", y))
    if (!file.exists(path)) {
      warning("Missing daily extract: ", path)
      next
    }
    daily_list[[as.character(y)]] <- parse_year_extract(path, y)
  }
  if (!length(daily_list)) stop("No dailyExtract files found in ", extract_dir)

  weather_daily <- dplyr::bind_rows(daily_list) |>
    dplyr::arrange(date) |>
    dplyr::mutate(
      station = cfg$weather$primary_station,
      hot_night = tmin >= cfg$weather$thresholds$hot_night_tmin_c,
      very_hot_day = tmax >= cfg$weather$thresholds$very_hot_day_tmax_c,
      extremely_hot_day = tmax >= cfg$weather$thresholds$extremely_hot_day_tmax_c,
      cold_day = tmin <= cfg$weather$thresholds$cold_day_tmin_c,
      absolute_humidity = absolute_humidity_gm3(tmean, relative_humidity),
      in_2d3n_window = flag_2d3n_window(very_hot_day, hot_night, window = 5L)
    )

  # Full-series spell IDs for cross-month spell length touching each month
  add_spell_id <- function(flag) {
    flag <- as.logical(flag)
    flag[is.na(flag)] <- FALSE
    ids <- integer(length(flag))
    cur <- 0L
    for (i in seq_along(flag)) {
      if (flag[i]) {
        if (i == 1L || !flag[i - 1L]) cur <- cur + 1L
        ids[i] <- cur
      } else {
        ids[i] <- 0L
      }
    }
    ids
  }

  weather_daily$hot_night_spell_id <- add_spell_id(weather_daily$hot_night)
  weather_daily$very_hot_spell_id <- add_spell_id(weather_daily$very_hot_day)
  weather_daily$cold_spell_id <- add_spell_id(weather_daily$cold_day)

  spell_lengths_hot <- weather_daily |>
    dplyr::filter(hot_night_spell_id > 0) |>
    dplyr::count(hot_night_spell_id, name = "spell_len")

  spell_lengths_vhd <- weather_daily |>
    dplyr::filter(very_hot_spell_id > 0) |>
    dplyr::count(very_hot_spell_id, name = "spell_len")

  spell_lengths_cold <- weather_daily |>
    dplyr::filter(cold_spell_id > 0) |>
    dplyr::count(cold_spell_id, name = "spell_len")

  weather_daily <- weather_daily |>
    dplyr::left_join(spell_lengths_hot, by = "hot_night_spell_id") |>
    dplyr::left_join(spell_lengths_vhd, by = "very_hot_spell_id", suffix = c("_hot", "_vhd")) |>
    dplyr::rename(
      hot_night_spell_len = spell_len_hot,
      very_hot_spell_len = spell_len_vhd
    ) |>
    dplyr::left_join(spell_lengths_cold, by = "cold_spell_id") |>
    dplyr::rename(cold_spell_len = spell_len)

  if (use_cache) save_weather_daily_cache(root, weather_daily, extract_dir, years)
}

completeness_thr <- cfg$weather$completeness_threshold %||% 0.90

climate_monthly <- weather_daily |>
  dplyr::mutate(
    month_date = as.Date(format(date, "%Y-%m-01")),
    month_id = format(date, "%Y-%m")
  ) |>
  dplyr::group_by(month_id, month_date, year = as.integer(format(month_date, "%Y")),
                  month = as.integer(format(month_date, "%m"))) |>
  dplyr::summarise(
    expected_days = as.integer(lubridate::days_in_month(dplyr::first(month_date))),
    observed_days = dplyr::n(),
    observed_tmin = sum(!is.na(tmin)),
    observed_tmax = sum(!is.na(tmax)),
    tmin_completeness = observed_tmin / expected_days,
    tmax_completeness = observed_tmax / expected_days,
    mean_temp = mean(tmean, na.rm = TRUE),
    mean_tmin = mean(tmin, na.rm = TRUE),
    mean_tmax = mean(tmax, na.rm = TRUE),
    relative_humidity = mean(relative_humidity, na.rm = TRUE),
    absolute_humidity = mean(absolute_humidity, na.rm = TRUE),
    rainfall = sum(rainfall, na.rm = TRUE),
    dew_point = mean(dew_point, na.rm = TRUE),
    hot_nights = ifelse(tmin_completeness >= completeness_thr, sum(hot_night, na.rm = TRUE), NA_integer_),
    cold_days = ifelse(tmin_completeness >= completeness_thr, sum(cold_day, na.rm = TRUE), NA_integer_),
    very_hot_days = ifelse(tmax_completeness >= completeness_thr, sum(very_hot_day, na.rm = TRUE), NA_integer_),
    extremely_hot_days = ifelse(tmax_completeness >= completeness_thr, sum(extremely_hot_day, na.rm = TRUE), NA_integer_),
    longest_hot_night_run = longest_true_run(hot_night),
    longest_very_hot_run = longest_true_run(very_hot_day),
    longest_cold_run = longest_true_run(cold_day),
    max_hot_night_spell_touching = ifelse(any(!is.na(hot_night_spell_len)), max(hot_night_spell_len, na.rm = TRUE), 0L),
    max_very_hot_spell_touching = ifelse(any(!is.na(very_hot_spell_len)), max(very_hot_spell_len, na.rm = TRUE), 0L),
    max_cold_spell_touching = ifelse(any(!is.na(cold_spell_len)), max(cold_spell_len, na.rm = TRUE), 0L),
    days_in_hot_night_spell_ge3 = sum(hot_night_spell_len >= 3, na.rm = TRUE),
    days_in_hot_night_spell_ge5 = sum(hot_night_spell_len >= 5, na.rm = TRUE),
    days_in_very_hot_spell_ge2 = sum(very_hot_spell_len >= 2, na.rm = TRUE),
    days_in_very_hot_spell_ge5 = sum(very_hot_spell_len >= 5, na.rm = TRUE),
    days_in_2d3n_window = sum(in_2d3n_window, na.rm = TRUE),
    month_has_2d3n_window = as.integer(any(in_2d3n_window, na.rm = TRUE)),
    station = cfg$weather$primary_station,
    .groups = "drop"
  ) |>
  dplyr::mutate(
    dplyr::across(
      c(hot_nights, cold_days, very_hot_days, extremely_hot_days,
        longest_hot_night_run, longest_very_hot_run, longest_cold_run,
        max_hot_night_spell_touching, max_very_hot_spell_touching, max_cold_spell_touching,
        days_in_hot_night_spell_ge3, days_in_hot_night_spell_ge5,
        days_in_very_hot_spell_ge2, days_in_very_hot_spell_ge5,
        days_in_2d3n_window, month_has_2d3n_window),
      as.integer
    )
  )

# Quality checks
stopifnot(!any(duplicated(climate_monthly$month_id)))
bad_hot <- which(!is.na(climate_monthly$hot_nights) &
                   (climate_monthly$hot_nights < 0 |
                      climate_monthly$hot_nights > climate_monthly$expected_days))
if (length(bad_hot)) stop("hot_nights out of bounds")

core <- climate_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  )

write_csv_safe(weather_daily, file.path(root, "data_processed", "climate_daily_hko.csv"))
write_csv_safe(core, file.path(root, "data_processed", "climate_monthly_2013_2023.csv"))

ext <- climate_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-12", cfg$study$optional_extension_year %||% cfg$study$end_year)
  )
write_csv_safe(ext, file.path(root, "data_processed", "climate_monthly_2013_2024.csv"))

# Annual summary for report
annual <- core |>
  dplyr::group_by(year) |>
  dplyr::summarise(
    hot_nights = sum(hot_nights, na.rm = TRUE),
    very_hot_days = sum(very_hot_days, na.rm = TRUE),
    extremely_hot_days = sum(extremely_hot_days, na.rm = TRUE),
    cold_days = sum(cold_days, na.rm = TRUE),
    mean_temp = mean(mean_temp, na.rm = TRUE),
    .groups = "drop"
  )
write_csv_safe(annual, file.path(root, "outputs", "tables", "weather_annual_extremes_2013_2023.csv"))

message("Weather monthly build complete. Core months: ", nrow(core))
