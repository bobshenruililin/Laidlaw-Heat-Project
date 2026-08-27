#!/usr/bin/env Rscript
# 52_hogan_abnormal_day_counts.R
# Hogan 24 Aug 2026 alternative to Jingjing TV-day counts:
# for each day of the year, take the historical mean of daily mean/max/min
# temperature; then count days in each calendar month that sit above or below
# that day-of-year average.
#
# Climatology: leave-one-year-out means of the same month-day across HKO
# dailyExtract years 2012–2023 (2024 held out of the study window).
# Ties with the climatology count as neither above nor below.
# REAL weather only. No health coefficients.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "jsonlite", "dplyr", "lubridate"))

extract_dir <- file.path(root, cfg$weather$sources$daily_extract_dir)
years_clim <- 2012:2023
years_study <- cfg$study$start_year:cfg$study$end_year

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
        tmax = parse_hko_number(day_vec[[3]]),
        tmean = parse_hko_number(day_vec[[4]]),
        tmin = parse_hko_number(day_vec[[5]]),
        relative_humidity = parse_hko_number(day_vec[[7]]),
        rainfall = parse_hko_number(day_vec[[9]]),
        stringsAsFactors = FALSE
      )
    }
  }
  dplyr::bind_rows(rows)
}

daily_list <- list()
for (y in years_clim) {
  path <- file.path(extract_dir, sprintf("dailyExtract_%d.xml", y))
  if (!file.exists(path)) {
    warning("Missing daily extract: ", path)
    next
  }
  daily_list[[as.character(y)]] <- parse_year_extract(path, y)
}
if (!length(daily_list)) stop("No dailyExtract files for climatology years")

weather_daily <- dplyr::bind_rows(daily_list) |>
  dplyr::arrange(date) |>
  dplyr::mutate(
    month_day = sprintf("%02d-%02d", month, day),
    month_id = format(date, "%Y-%m")
  )

# Leave-one-year-out climatology for each year in the study window.
study_daily <- weather_daily |>
  dplyr::filter(year %in% years_study)

clim_for_year <- function(y) {
  weather_daily |>
    dplyr::filter(year != y) |>
    dplyr::group_by(month_day) |>
    dplyr::summarise(
      clim_tmean = mean(tmean, na.rm = TRUE),
      clim_tmax = mean(tmax, na.rm = TRUE),
      clim_tmin = mean(tmin, na.rm = TRUE),
      n_clim_years = dplyr::n(),
      .groups = "drop"
    ) |>
    dplyr::mutate(year = y)
}

clim <- dplyr::bind_rows(lapply(years_study, clim_for_year))

tagged <- study_daily |>
  dplyr::left_join(clim, by = c("year", "month_day")) |>
  dplyr::mutate(
    tmean_above = as.integer(!is.na(tmean) & !is.na(clim_tmean) & tmean > clim_tmean),
    tmean_below = as.integer(!is.na(tmean) & !is.na(clim_tmean) & tmean < clim_tmean),
    tmax_above = as.integer(!is.na(tmax) & !is.na(clim_tmax) & tmax > clim_tmax),
    tmax_below = as.integer(!is.na(tmax) & !is.na(clim_tmax) & tmax < clim_tmax),
    tmin_above = as.integer(!is.na(tmin) & !is.na(clim_tmin) & tmin > clim_tmin),
    tmin_below = as.integer(!is.na(tmin) & !is.na(clim_tmin) & tmin < clim_tmin)
  )

monthly <- tagged |>
  dplyr::group_by(month_id, year, month) |>
  dplyr::summarise(
    n_days = dplyr::n(),
    n_days_tmean_above_doy = sum(tmean_above, na.rm = TRUE),
    n_days_tmean_below_doy = sum(tmean_below, na.rm = TRUE),
    n_days_tmax_above_doy = sum(tmax_above, na.rm = TRUE),
    n_days_tmax_below_doy = sum(tmax_below, na.rm = TRUE),
    n_days_tmin_above_doy = sum(tmin_above, na.rm = TRUE),
    n_days_tmin_below_doy = sum(tmin_below, na.rm = TRUE),
    mean_relative_humidity = mean(relative_humidity, na.rm = TRUE),
    total_rainfall_mm = sum(rainfall, na.rm = TRUE),
    .groups = "drop"
  ) |>
  dplyr::arrange(month_id)

stopifnot(nrow(monthly) == 132L)
stopifnot(all(monthly$n_days_tmean_above_doy + monthly$n_days_tmean_below_doy <= monthly$n_days))

out_processed <- file.path(root, "data_processed", "hogan_abnormal_day_counts_2013_2023.csv")
out_tables <- file.path(root, "outputs", "tables", "hogan_abnormal_day_counts_2013_2023.csv")
dir.create(dirname(out_tables), recursive = TRUE, showWarnings = FALSE)
utils::write.csv(monthly, out_processed, row.names = FALSE)
utils::write.csv(monthly, out_tables, row.names = FALSE)

meta <- data.frame(
  n_months = nrow(monthly),
  climatology_years = "2012-2023 leave-one-year-out",
  study_window = "2013-01 to 2023-12",
  mean_tmean_above = mean(monthly$n_days_tmean_above_doy),
  mean_tmean_below = mean(monthly$n_days_tmean_below_doy),
  jan_mean_tmean_below = mean(monthly$n_days_tmean_below_doy[monthly$month == 1L]),
  jul_mean_tmean_below = mean(monthly$n_days_tmean_below_doy[monthly$month == 7L]),
  provenance = "REAL_HKO_DAILY",
  stringsAsFactors = FALSE
)
utils::write.csv(
  meta,
  file.path(root, "outputs", "tables", "hogan_abnormal_day_counts_meta.csv"),
  row.names = FALSE
)

message("Wrote ", out_processed)
message(
  "Jan mean days tmean below DOY: ", round(meta$jan_mean_tmean_below, 1),
  "; Jul: ", round(meta$jul_mean_tmean_below, 1)
)
