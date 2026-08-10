#!/usr/bin/env Rscript
# 40_build_daily_weather_design.R
# Public HKO daily weather design for 2013–2023 (no health inputs).
# Output: data_processed/md_daily_weather_design_2013_2023.csv
# Provenance: REAL_PUBLIC_HKO

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
root <- project_root()
setwd(root)
ensure_packages("yaml")

cfg <- load_config(root)

# Thresholds: HKO absolute extremes from config; heat also cross-checked vs source lock.
thr_hot_night <- cfg$weather$thresholds$hot_night_tmin_c %||% 28
thr_very_hot <- cfg$weather$thresholds$very_hot_day_tmax_c %||% 33
thr_cold <- cfg$weather$thresholds$cold_day_tmin_c %||% 12
src_path <- file.path(root, "analysis_plan", "weather_source_definitions.yml")
if (file.exists(src_path) && requireNamespace("yaml", quietly = TRUE)) {
  defs <- yaml::read_yaml(src_path)$definitions
  if (!is.null(defs$wang_hn5$threshold_c)) thr_hot_night <- defs$wang_hn5$threshold_c
  if (!is.null(defs$wang_vhd5$threshold_c)) thr_very_hot <- defs$wang_vhd5$threshold_c
}
if (!is.finite(thr_cold)) stop("cold_day threshold missing from config.yml")

read_hko_open_daily <- function(path, value_name) {
  if (!file.exists(path)) stop("Missing HKO open-data series: ", path)
  raw <- utils::read.csv(
    path,
    skip = 2,
    stringsAsFactors = FALSE,
    check.names = FALSE,
    fileEncoding = "UTF-8-BOM"
  )
  if (ncol(raw) < 4L) stop("Unexpected HKO open-data layout: ", path)
  out <- data.frame(
    year = suppressWarnings(as.integer(raw[[1]])),
    month = suppressWarnings(as.integer(raw[[2]])),
    day = suppressWarnings(as.integer(raw[[3]])),
    value = parse_hko_number(raw[[4]]),
    stringsAsFactors = FALSE
  )
  out <- out[
    is.finite(out$year) & is.finite(out$month) & is.finite(out$day),
    ,
    drop = FALSE
  ]
  out$date <- as.Date(sprintf("%04d-%02d-%02d", out$year, out$month, out$day))
  names(out)[names(out) == "value"] <- value_name
  out <- out[!is.na(out$date), , drop = FALSE]
  out[, c("date", value_name)]
}

tmax <- read_hko_open_daily(
  file.path(root, "data_raw", "hko", "CLMMAXT_HKO.csv"),
  "tmax"
)
tmin <- read_hko_open_daily(
  file.path(root, "data_raw", "hko", "CLMMINT_HKO.csv"),
  "tmin"
)
tmean <- read_hko_open_daily(
  file.path(root, "data_raw", "hko", "CLMTEMP_HKO.csv"),
  "tmean"
)

daily <- Reduce(
  function(x, y) merge(x, y, by = "date", all = TRUE),
  list(tmax, tmin, tmean)
)
daily <- daily[order(daily$date), , drop = FALSE]
daily <- daily[
  daily$date >= as.Date("2013-01-01") & daily$date <= as.Date("2023-12-31"),
  ,
  drop = FALSE
]

full_grid <- data.frame(
  date = seq(as.Date("2013-01-01"), as.Date("2023-12-31"), by = "day"),
  stringsAsFactors = FALSE
)
daily <- merge(full_grid, daily, by = "date", all.x = TRUE, sort = TRUE)
if (anyDuplicated(daily$date)) stop("Duplicate dates in daily weather design")

n_missing_temp <- sum(
  !is.finite(daily$tmean) | !is.finite(daily$tmax) | !is.finite(daily$tmin)
)
if (n_missing_temp > 0) {
  stop(
    "Missing study-window temperature on ", n_missing_temp,
    " days (2013–2023). Refusing to code missing as non-extreme."
  )
}

# Official HKO absolute thresholds (config + source-locked heat defs).
daily$hot_night <- as.integer(daily$tmin >= thr_hot_night)
daily$very_hot_day <- as.integer(daily$tmax >= thr_very_hot)
daily$cold_day <- as.integer(daily$tmin <= thr_cold)

daily$year <- as.integer(format(daily$date, "%Y"))
daily$month <- as.integer(format(daily$date, "%m"))
daily$day <- as.integer(format(daily$date, "%d"))
daily$month_id <- format(daily$date, "%Y-%m")
daily$doy <- as.integer(format(daily$date, "%j"))
daily$time_index <- as.numeric(daily$date - as.Date("2013-01-01")) + 1

if (!is.null(cfg$covid_phases)) {
  daily$covid_phase <- assign_covid_phase(daily$month_id, cfg$covid_phases)
} else {
  daily$covid_phase <- "pre_covid"
  daily$covid_phase[daily$month_id >= "2020-02" & daily$month_id <= "2021-12"] <- "early_covid"
  daily$covid_phase[daily$month_id >= "2022-01" & daily$month_id <= "2022-04"] <- "fifth_wave"
  daily$covid_phase[daily$month_id >= "2022-05" & daily$month_id <= "2022-12"] <- "late_2022"
  daily$covid_phase[daily$month_id >= "2023-01"] <- "post_reopening"
}

# Constrained kernel exposures for allowed M|D exposure models
daily$hot_night_same_day <- md_kernel_same_day(daily$hot_night)
daily$cold_day_same_day <- md_kernel_same_day(daily$cold_day)
daily$hot_night_lag_0_5 <- md_kernel_cumulative_0_5(daily$hot_night)
daily$cold_day_lag_0_21 <- md_kernel_cumulative_0_21(daily$cold_day)

daily$data_status <- MD_PROVENANCE_PUBLIC_HKO
daily$threshold_hot_night_c <- thr_hot_night
daily$threshold_very_hot_day_c <- thr_very_hot
daily$threshold_cold_day_c <- thr_cold
daily$notes <- "Public HKO open-data design only; no health outcomes joined."

out_path <- file.path(root, "data_processed", "md_daily_weather_design_2013_2023.csv")
write_csv_safe(daily, out_path)

meta <- data.frame(
  artifact = "md_daily_weather_design_2013_2023.csv",
  n_days = nrow(daily),
  start_date = as.character(min(daily$date)),
  end_date = as.character(max(daily$date)),
  n_missing_temp = n_missing_temp,
  cold_threshold_c = thr_cold,
  data_status = MD_PROVENANCE_PUBLIC_HKO,
  stringsAsFactors = FALSE
)
write_csv_safe(
  meta,
  file.path(root, "data_processed", "md_daily_weather_design_2013_2023_meta.csv")
)

message(
  "Daily weather design complete: ", nrow(daily), " days; provenance=",
  MD_PROVENANCE_PUBLIC_HKO, "; cold_threshold_c=", thr_cold
)
