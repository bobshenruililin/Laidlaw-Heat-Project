#!/usr/bin/env Rscript
# 35_build_spillover_exposures.R
# Source-locked daily heat-event morphology and calendar-spillover audit.
#
# Health outcomes are never read. Outputs are public-weather exposure files.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "exposure_morphology.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "tidyr", "yaml"))
source_registry <- yaml::read_yaml(
  file.path(root, "analysis_plan", "weather_source_definitions.yml")
)
defs <- source_registry$definitions

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
    completeness = if (ncol(raw) >= 5L) as.character(raw[[5]]) else NA_character_,
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
  function(x, y) merge(x, y, by = "date", all = TRUE, suffixes = c("", "_source")),
  list(tmax, tmin, tmean)
)
daily <- daily[order(daily$date), , drop = FALSE]
daily <- daily[daily$date >= as.Date("1980-01-01") &
                 daily$date <= as.Date("2024-12-31"), , drop = FALSE]

# The open-data files can have distinct source completeness columns. They are
# retained in raw HKO files; only temperatures enter this public exposure audit.
daily <- daily[, c("date", "tmax", "tmin", "tmean")]
daily <- daily[!is.na(daily$date), , drop = FALSE]
if (anyDuplicated(daily$date)) stop("Duplicate dates after HKO open-data merge")
full_grid <- data.frame(
  date = seq(min(daily$date, na.rm = TRUE), max(daily$date, na.rm = TRUE), by = "day"),
  stringsAsFactors = FALSE
)
daily <- merge(full_grid, daily, by = "date", all.x = TRUE, sort = TRUE)
as_daily_dates(daily$date)

daily$hot_night <- is.finite(daily$tmin) &
  daily$tmin >= defs$wang_hn5$threshold_c
daily$very_hot_day <- is.finite(daily$tmax) &
  daily$tmax >= defs$wang_vhd5$threshold_c
daily$cold_day <- is.finite(daily$tmin) & daily$tmin <= 12

vhd5 <- detect_wang_spells(
  daily$date,
  daily$very_hot_day,
  min_length = defs$wang_vhd5$minimum_consecutive_days
)
hn5 <- detect_wang_spells(
  daily$date,
  daily$hot_night,
  min_length = defs$wang_hn5$minimum_consecutive_days
)
compound <- detect_wang_2d3n(daily$date, daily$very_hot_day, daily$hot_night)
li_hw <- detect_li_heatwaves(
  daily$date,
  daily$tmax,
  reference_start = as.Date(defs$li_hw$reference_start),
  reference_end = as.Date(defs$li_hw$reference_end),
  warm_months = unlist(defs$li_hw$warm_months),
  probability = defs$li_hw$percentile,
  half_window = defs$li_hw$calendar_window_half_width_days,
  min_length = defs$li_hw$minimum_consecutive_days,
  merge_gap_days = defs$li_hw$merge_if_gap_days_lte
)

monthly <- Reduce(
  function(x, y) merge(x, y, by = "month_id", all = TRUE, sort = TRUE),
  list(
    summarise_event_months(daily$date, vhd5$events, vhd5$daily, "wang_vhd5"),
    summarise_event_months(daily$date, hn5$events, hn5$daily, "wang_hn5"),
    summarise_event_months(daily$date, compound$events, compound$daily, "wang_2d3n"),
    summarise_event_months(daily$date, li_hw$events, li_hw$daily, "li_hw")
  )
)
monthly <- monthly[
  monthly$month_id >= "2013-01" & monthly$month_id <= "2023-12",
  ,
  drop = FALSE
]
monthly$data_status <- "REAL_PUBLIC_HKO"
monthly$result_class <- "EXPOSURE_AUDIT"
stopifnot(nrow(monthly) == 132L)

event_rows <- function(events, definition_id, source_doi) {
  if (!nrow(events)) {
    return(data.frame(
      definition_id = character(),
      source_doi = character(),
      event_id = integer(),
      start_date = as.Date(character()),
      end_date = as.Date(character()),
      event_days = integer(),
      component_windows = integer(),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    definition_id = definition_id,
    source_doi = source_doi,
    event_id = events$event_id,
    start_date = events$start_date,
    end_date = events$end_date,
    event_days = events$event_days,
    component_windows = events$component_windows %||% 1L,
    stringsAsFactors = FALSE
  )
}

events <- dplyr::bind_rows(
  event_rows(vhd5$events, "wang_vhd5", "10.1016/j.scitotenv.2019.07.039"),
  event_rows(hn5$events, "wang_hn5", "10.1016/j.scitotenv.2019.07.039"),
  event_rows(compound$events, "wang_2d3n", "10.1016/j.scitotenv.2019.07.039"),
  event_rows(li_hw$events, "li_hw", "10.1016/j.atmosres.2024.107845")
)
events <- events[
  events$end_date >= as.Date("2013-01-01") &
    events$start_date <= as.Date("2023-12-31"),
  ,
  drop = FALSE
]
events$data_status <- "REAL_PUBLIC_HKO"
events$result_class <- "EXPOSURE_AUDIT"

source_lock <- data.frame(
  definition_id = c("wang_vhd5", "wang_hn5", "wang_2d3n", "li_hw"),
  source_doi = c(
    defs$wang_vhd5$source_doi,
    defs$wang_hn5$source_doi,
    defs$wang_2d3n$source_doi,
    defs$li_hw$source_doi
  ),
  implementation = c(
    paste0(
      "Tmax >= ", defs$wang_vhd5$threshold_c, " C; >= ",
      defs$wang_vhd5$minimum_consecutive_days, " consecutive VHDs"
    ),
    paste0(
      "Tmin >= ", defs$wang_hn5$threshold_c, " C; >= ",
      defs$wang_hn5$minimum_consecutive_days, " consecutive HNs"
    ),
    "NDNDN: VHD[i:i+1] and HN[i:i+2]; overlapping/touching windows merged; post-event days 1-5",
    "May-Sep Tmax > calendar-day p90; 15-day moving window; 1980-2023 reference; >=3 days; merge gaps <=2 days"
  ),
  lock_status = c(
    defs$wang_vhd5$source_status,
    defs$wang_hn5$source_status,
    defs$wang_2d3n$source_status,
    paste0(defs$li_hw$source_status, "_HOGAN_MONTHLY_TAIL_NOT_LOCKED")
  ),
  data_status = "REAL_PUBLIC_HKO",
  stringsAsFactors = FALSE
)

write_csv_safe(
  monthly,
  file.path(root, "data_processed", "exposures_spillover_monthly_2013_2023.csv")
)
write_csv_safe(
  events,
  file.path(root, "outputs", "tables", "weather_event_morphology_audit.csv")
)
write_csv_safe(
  source_lock,
  file.path(root, "outputs", "tables", "weather_definition_source_lock.csv")
)

report_path <- file.path(root, "outputs", "reports", "weather_spillover_exposure_build.md")
writeLines(
  c(
    "# Source-locked weather morphology build",
    "",
    "- Provenance: `REAL_PUBLIC_HKO`.",
    "- Result class: `EXPOSURE_AUDIT`.",
    "- Health outcomes were not read.",
    "- Li monthly upper-tail classification remains Hogan-unlocked.",
    "",
    "## Definitions",
    "",
    "| ID | Implementation | Status |",
    "|---|---|---|",
    paste0(
      "| ", source_lock$definition_id, " | ",
      source_lock$implementation, " | ",
      source_lock$lock_status, " |"
    ),
    "",
    "## Study-window event counts",
    "",
    paste0(
      "- ", names(table(events$definition_id)), ": ",
      as.integer(table(events$definition_id))
    ),
    "",
    "Calendar-spillover phases are assigned by affected date. A late-month 2D3N event therefore contributes post-event days to the following month."
  ),
  report_path
)
message("Spillover exposure build complete: ", nrow(monthly), " months")
