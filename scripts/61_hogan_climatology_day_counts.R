#!/usr/bin/env Rscript
# Monthly counts of days warmer/cooler than the historical same-calendar-day mean.
# Hogan (24 Aug 2026): do not threshold a temperature-variability index.
# Climatology is leave-one-year-out mean of that month-day in 2012–2023 HKO Headquarters series.
# Does not join health outcomes.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "jsonlite", "dplyr", "lubridate"))

extract_dir <- file.path(root, cfg$weather$sources$daily_extract_dir)

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

years <- 2012:2023
daily_list <- list()
for (y in years) {
  path <- file.path(extract_dir, sprintf("dailyExtract_%d.xml", y))
  if (!file.exists(path)) {
    warning("Missing daily extract: ", path)
    next
  }
  daily_list[[as.character(y)]] <- parse_year_extract(path, y)
}
if (!length(daily_list)) stop("No dailyExtract files found")

daily <- dplyr::bind_rows(daily_list) |>
  dplyr::arrange(date) |>
  dplyr::mutate(md = sprintf("%02d-%02d", month, day))

# Leave-one-year-out climatology for each calendar day.
clim <- daily |>
  dplyr::select(year, md, tmean, tmax, tmin) |>
  dplyr::inner_join(
    daily |> dplyr::select(year_ref = year, md, tmean_y = tmean, tmax_y = tmax, tmin_y = tmin),
    by = "md",
    relationship = "many-to-many"
  ) |>
  dplyr::filter(year_ref != year) |>
  dplyr::group_by(year, md) |>
  dplyr::summarise(
    clim_tmean = mean(tmean_y, na.rm = TRUE),
    clim_tmax = mean(tmax_y, na.rm = TRUE),
    clim_tmin = mean(tmin_y, na.rm = TRUE),
    n_clim_years = dplyr::n(),
    .groups = "drop"
  )

daily2 <- daily |>
  dplyr::left_join(clim, by = c("year", "md")) |>
  dplyr::mutate(
    warmer_tmean = as.integer(!is.na(tmean) & !is.na(clim_tmean) & tmean > clim_tmean),
    cooler_tmean = as.integer(!is.na(tmean) & !is.na(clim_tmean) & tmean < clim_tmean),
    warmer_tmax = as.integer(!is.na(tmax) & !is.na(clim_tmax) & tmax > clim_tmax),
    cooler_tmin = as.integer(!is.na(tmin) & !is.na(clim_tmin) & tmin < clim_tmin)
  )

study <- daily2 |>
  dplyr::filter(year >= 2013, year <= 2023)

monthly <- study |>
  dplyr::mutate(month_id = format(date, "%Y-%m")) |>
  dplyr::group_by(month_id, year, month) |>
  dplyr::summarise(
    n_days = dplyr::n(),
    days_warmer_than_climatology = sum(warmer_tmean, na.rm = TRUE),
    days_cooler_than_climatology = sum(cooler_tmean, na.rm = TRUE),
    days_tmax_above_climatology = sum(warmer_tmax, na.rm = TRUE),
    days_tmin_below_climatology = sum(cooler_tmin, na.rm = TRUE),
    mean_relative_humidity = mean(relative_humidity, na.rm = TRUE),
    total_rainfall_mm = sum(rainfall, na.rm = TRUE),
    .groups = "drop"
  ) |>
  dplyr::mutate(
    climatology_rule = "leave_one_year_out_same_calendar_day_2012_2023",
    data_status = "REAL_PUBLIC_HKO"
  )

stopifnot(nrow(monthly) == 132L)
stopifnot(all(monthly$days_warmer_than_climatology + monthly$days_cooler_than_climatology <= monthly$n_days))

by_calendar_month <- monthly |>
  dplyr::group_by(month) |>
  dplyr::summarise(
    mean_warmer = mean(days_warmer_than_climatology),
    mean_cooler = mean(days_cooler_than_climatology),
    mean_rainfall_mm = mean(total_rainfall_mm),
    mean_rh = mean(mean_relative_humidity),
    .groups = "drop"
  )

dir.create(file.path(root, "outputs", "tables"), showWarnings = FALSE, recursive = TRUE)
utils::write.csv(
  monthly,
  file.path(root, "data_processed", "hogan_climatology_day_counts_2013_2023.csv"),
  row.names = FALSE
)
utils::write.csv(
  by_calendar_month,
  file.path(root, "outputs", "tables", "hogan_climatology_day_counts_by_calendar_month.csv"),
  row.names = FALSE
)

message(
  "Wrote 132 months. Mean warmer days/month: ",
  round(mean(monthly$days_warmer_than_climatology), 1),
  "; cooler: ",
  round(mean(monthly$days_cooler_than_climatology), 1)
)
print(by_calendar_month)
