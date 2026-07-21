#!/usr/bin/env Rscript
# 19_build_analysis_exposures.R
# Build analysis-ready monthly exposure file for 2013–2023 with:
#   - lag-1 temperature (needs Dec 2012 from dailyExtract_2012.xml)
#   - heatwave-month indicators (percentile + spell collapses)
# Writes: data_processed/exposures_monthly_2013_2023.csv

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "jsonlite", "dplyr", "tidyr", "lubridate"))

extract_dir <- file.path(root, cfg$weather$sources$daily_extract_dir)
thr <- cfg$weather$thresholds

parse_year_extract <- function(path, year) {
  raw <- jsonlite::fromJSON(path, simplifyVector = FALSE)
  rows <- list()
  for (mobj in raw$stn$data) {
    mo <- as.integer(mobj$month)
    for (day_vec in mobj$dayData) {
      day_label <- trimws(as.character(day_vec[[1]]))
      if (!grepl("^[0-9]{1,2}$", day_label)) next
      day <- as.integer(day_label)
      rows[[length(rows) + 1]] <- data.frame(
        date = as.Date(sprintf("%04d-%02d-%02d", year, mo, day)),
        year = year,
        month = mo,
        tmean = parse_hko_number(day_vec[[4]]),
        tmax = parse_hko_number(day_vec[[3]]),
        tmin = parse_hko_number(day_vec[[5]]),
        stringsAsFactors = FALSE
      )
    }
  }
  dplyr::bind_rows(rows)
}

# Monthly climate already built for 2013–2023(+); extend with Dec 2012 only for lags
climate <- utils::read.csv(
  file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
  stringsAsFactors = FALSE
)

path_2012 <- file.path(extract_dir, "dailyExtract_2012.xml")
if (!file.exists(path_2012)) stop("Missing ", path_2012, " required for lag-1 January 2013")

daily_2012 <- parse_year_extract(path_2012, 2012) |>
  dplyr::filter(month == 12)

dec2012 <- daily_2012 |>
  dplyr::summarise(
    month_id = "2012-12",
    year = 2012L,
    month = 12L,
    mean_temp = mean(tmean, na.rm = TRUE),
    mean_tmin = mean(tmin, na.rm = TRUE),
    mean_tmax = mean(tmax, na.rm = TRUE),
    .groups = "drop"
  )

# Lag-1 join
base <- climate |>
  dplyr::arrange(month_id) |>
  dplyr::mutate(time_index = dplyr::row_number())

lag_src <- dplyr::bind_rows(
  dec2012[, c("month_id", "mean_temp", "mean_tmin", "mean_tmax")],
  base[, c("month_id", "mean_temp", "mean_tmin", "mean_tmax")]
) |>
  dplyr::arrange(month_id) |>
  dplyr::mutate(
    lag1_mean_temp = dplyr::lag(mean_temp),
    lag1_mean_tmin = dplyr::lag(mean_tmin),
    lag1_mean_tmax = dplyr::lag(mean_tmax)
  ) |>
  dplyr::select(month_id, lag1_mean_temp, lag1_mean_tmin, lag1_mean_tmax)

# Heatwave-month indicators from within-study monthly distribution + spell proxies
# Multi-percentile grid mirrors Guo/Gasparrini EHP 2017 spirit (monthly collapse).
p90_tmean <- as.numeric(stats::quantile(base$mean_temp, 0.90, na.rm = TRUE))
p95_tmean <- as.numeric(stats::quantile(base$mean_temp, 0.95, na.rm = TRUE))
p975_tmean <- as.numeric(stats::quantile(base$mean_temp, 0.975, na.rm = TRUE))
p05_tmean <- as.numeric(stats::quantile(base$mean_temp, 0.05, na.rm = TRUE))

exposures <- base |>
  dplyr::left_join(lag_src, by = "month_id") |>
  dplyr::mutate(
    hw_month_mean_temp_ge_p90 = as.integer(mean_temp >= p90_tmean),
    hw_month_mean_temp_ge_p95 = as.integer(mean_temp >= p95_tmean),
    hw_month_mean_temp_ge_p975 = as.integer(mean_temp >= p975_tmean),
    cold_month_mean_temp_le_p05 = as.integer(mean_temp <= p05_tmean),
    hw_month_has_vhd_spell_ge3 = as.integer(
      dplyr::coalesce(longest_very_hot_run, 0) >= 3 |
        dplyr::coalesce(days_in_very_hot_spell_ge2, 0) >= 3
    ),
    hw_month_has_hn_spell_ge3 = as.integer(
      dplyr::coalesce(longest_hot_night_run, 0) >= 3 |
        dplyr::coalesce(days_in_hot_night_spell_ge3, 0) >= 3
    ),
    hw_p90_threshold_c = p90_tmean,
    hw_p95_threshold_c = p95_tmean,
    hw_p975_threshold_c = p975_tmean,
    cold_p05_threshold_c = p05_tmean,
    exposure_build_notes = "lag1 from Dec2012+study window; HW-month p90/p95/p975 + spell proxies; TV from daily extracts when available"
  )

# Attach pollution if real
pol_path <- file.path(root, "data_processed", "pollution_monthly_2013_2023.csv")
if (file.exists(pol_path)) {
  pol <- utils::read.csv(pol_path, stringsAsFactors = FALSE)
  keep <- intersect(c("month_id", "NO2", "O3", "PM25", "PM10", "data_status"), names(pol))
  exposures <- exposures |>
    dplyr::left_join(pol[, keep], by = "month_id", suffix = c("", "_pol"))
  if ("data_status_pol" %in% names(exposures)) {
    exposures$pollution_data_status <- exposures$data_status_pol
    exposures$data_status_pol <- NULL
  } else if ("data_status" %in% names(pol)) {
    exposures$pollution_data_status <- pol$data_status[match(exposures$month_id, pol$month_id)]
  }
}

# Confounders
conf_path <- file.path(root, "data_processed", "confounders_monthly_2013_2023.csv")
if (file.exists(conf_path)) {
  conf <- utils::read.csv(conf_path, stringsAsFactors = FALSE)
  conf_keep <- intersect(
    c("month_id", "covid_phase", "chinese_new_year_month", "public_holiday_days",
      "flu_indicator", "flu_data_status", "absolute_humidity"),
    names(conf)
  )
  # absolute humidity lives on climate; ensure present
  exposures <- exposures |>
    dplyr::left_join(conf[, conf_keep], by = "month_id", suffix = c("", "_conf"))
}

# Temperature variability: prefer mean daily diurnal range from HKO daily extracts
tv_built <- FALSE
daily_csv <- file.path(root, "data_processed", "climate_daily_hko.csv")
if (file.exists(daily_csv)) {
  daily <- utils::read.csv(daily_csv, stringsAsFactors = FALSE)
  if (all(c("date", "tmax", "tmin") %in% names(daily))) {
    daily$month_id <- format(as.Date(daily$date), "%Y-%m")
    tv <- daily |>
      dplyr::mutate(diurnal_range = tmax - tmin) |>
      dplyr::group_by(month_id) |>
      dplyr::summarise(
        temp_variability_mean_range = mean(diurnal_range, na.rm = TRUE),
        temp_variability_sd_tmean = stats::sd(tmean, na.rm = TRUE),
        .groups = "drop"
      )
    exposures <- exposures |> dplyr::left_join(tv, by = "month_id")
    tv_built <- TRUE
  }
}
if (!tv_built) {
  # Build from dailyExtract_YYYY.xml for study years
  years <- seq(cfg$study$start_year, cfg$study$end_year)
  daily_rows <- list()
  for (yy in years) {
    pth <- file.path(extract_dir, sprintf("dailyExtract_%04d.xml", yy))
    if (!file.exists(pth)) next
    daily_rows[[as.character(yy)]] <- parse_year_extract(pth, yy)
  }
  if (length(daily_rows)) {
    daily_all <- dplyr::bind_rows(daily_rows) |>
      dplyr::mutate(month_id = format(date, "%Y-%m"), diurnal_range = tmax - tmin)
    tv <- daily_all |>
      dplyr::group_by(month_id) |>
      dplyr::summarise(
        temp_variability_mean_range = mean(diurnal_range, na.rm = TRUE),
        temp_variability_sd_tmean = stats::sd(tmean, na.rm = TRUE),
        .groups = "drop"
      )
    exposures <- exposures |> dplyr::left_join(tv, by = "month_id")
    tv_built <- TRUE
  }
}
if (!tv_built) {
  # Coarser fallback: monthly mean Tmax − mean Tmin
  exposures <- exposures |>
    dplyr::mutate(
      temp_variability_mean_range = mean_tmax - mean_tmin,
      temp_variability_sd_tmean = NA_real_
    )
}

stopifnot(nrow(exposures) == 132)
stopifnot(!anyNA(exposures$lag1_mean_tmax))
write_csv_safe(exposures, file.path(root, "data_processed", "exposures_monthly_2013_2023.csv"))

message(
  "Exposures ready. lag1 Jan2013 Tmax=", round(exposures$lag1_mean_tmax[1], 2),
  " | HW p95 Tmean=", round(p95_tmean, 2),
  " | HW months=", sum(exposures$hw_month_mean_temp_ge_p95),
  " | flu nonmiss=", sum(!is.na(exposures$flu_indicator))
)
