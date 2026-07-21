#!/usr/bin/env Rscript
# 04_build_pollution_monthly.R
# Build territory-wide monthly pollution panel from EPD EPIC CSVs.
# Primary: unweighted mean across general stations with ≥75% station completeness.
# Roadside files (if present) are archived but not mixed into the primary series.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr", "readr", "stringr"))

epd_dir <- file.path(root, cfg$pollution$raw_dir)
completeness_thr <- cfg$pollution$completeness_threshold %||% 0.75

pollutant_alias <- c(
  "FINE SUSPENDED PARTICULATES" = "PM25",
  "FSP" = "PM25",
  "PM2.5" = "PM25",
  "PM25" = "PM25",
  "RESPIRABLE SUSPENDED PARTICULATES" = "PM10",
  "RSP" = "PM10",
  "PM10" = "PM10",
  "NITROGEN DIOXIDE" = "NO2",
  "NO2" = "NO2",
  "OZONE" = "O3",
  "O3" = "O3",
  "SULPHUR DIOXIDE" = "SO2",
  "SO2" = "SO2"
)

is_epic_wide <- function(path) {
  hdr <- tryCatch(readLines(path, n = 20, warn = FALSE), error = function(e) character())
  any(grepl("YEAR\\s*,\\s*POLLUTANT\\s*,\\s*STATION", hdr, ignore.case = TRUE))
}

read_epic_wide <- function(path) {
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  # Skip remarks; find header
  hdr_i <- which(grepl("^YEAR\\s*,\\s*POLLUTANT\\s*,\\s*STATION", lines, ignore.case = TRUE))[1]
  if (is.na(hdr_i)) stop("No YEAR,POLLUTANT,STATION header in ", basename(path))
  df <- utils::read.csv(
    text = paste(lines[hdr_i:length(lines)], collapse = "\n"),
    stringsAsFactors = FALSE,
    check.names = FALSE,
    na.strings = c("", "NA", "N.A.", "N.A", "n.a.", "-")
  )
  names(df) <- trimws(names(df))
  month_cols <- grep("^Month\\s*\\d+", names(df), ignore.case = TRUE, value = TRUE)
  if (!length(month_cols)) stop("No Month columns in ", basename(path))
  # Force month columns to character so pivot_longer can combine N.A. with numbers
  df[month_cols] <- lapply(df[month_cols], function(x) trimws(as.character(x)))

  long <- tidyr::pivot_longer(
    df,
    cols = dplyr::all_of(month_cols),
    names_to = "month_label",
    values_to = "value_raw"
  ) |>
    dplyr::mutate(
      month = as.integer(stringr::str_extract(month_label, "\\d+")),
      year = as.integer(YEAR),
      pollutant_raw = toupper(trimws(POLLUTANT)),
      pollutant = unname(pollutant_alias[pollutant_raw]),
      station = trimws(STATION),
      value_raw = ifelse(value_raw %in% c("", "NA", "N.A.", "N.A", "n.a.", "-", "NaN"), NA_character_, value_raw),
      value = suppressWarnings(as.numeric(gsub(",", "", value_raw))),
      month_id = sprintf("%04d-%02d", year, month),
      source_file = basename(path)
    ) |>
    dplyr::filter(!is.na(pollutant), !is.na(month), month >= 1, month <= 12)

  long
}

normalize_names <- function(nm) {
  toupper(gsub("[^A-Za-z0-9]+", "", nm))
}

general_csvs <- list.files(epd_dir, pattern = "^epd_general_monthly_.*\\.csv$", full.names = TRUE)
legacy_csvs <- list.files(epd_dir, pattern = "\\.csv$", full.names = TRUE)
legacy_csvs <- legacy_csvs[
  !grepl("PLACEHOLDER|placeholder|roadside", basename(legacy_csvs), ignore.case = TRUE) &
    !basename(legacy_csvs) %in% basename(general_csvs)
]

if (length(general_csvs)) {
  message("Building pollution monthly from EPIC general-station CSVs (", length(general_csvs), ").")
  long <- dplyr::bind_rows(lapply(general_csvs, read_epic_wide))

  # Station-month values (one row per station × pollutant × month)
  station_month <- long |>
    dplyr::group_by(month_id, pollutant, station) |>
    dplyr::summarise(value = mean(value, na.rm = TRUE), .groups = "drop") |>
    dplyr::mutate(
      value = ifelse(is.nan(value), NA_real_, value),
      year = as.integer(substr(month_id, 1, 4))
    )

  # Active network for completeness: stations with ≥1 non-missing value in that year
  active <- station_month |>
    dplyr::filter(!is.na(value)) |>
    dplyr::distinct(year, pollutant, station) |>
    dplyr::count(year, pollutant, name = "n_stations_active")

  monthly_pol <- station_month |>
    dplyr::group_by(month_id, year, pollutant) |>
    dplyr::summarise(
      mean_value = mean(value, na.rm = TRUE),
      n_stations_nonmiss = sum(!is.na(value)),
      .groups = "drop"
    ) |>
    dplyr::mutate(mean_value = ifelse(is.nan(mean_value), NA_real_, mean_value)) |>
    dplyr::left_join(active, by = c("year", "pollutant")) |>
    dplyr::mutate(
      n_stations_active = dplyr::coalesce(n_stations_active, 0L),
      completeness = ifelse(n_stations_active > 0, n_stations_nonmiss / n_stations_active, NA_real_),
      # Drop month only if too few active stations report (relative to that year's network)
      mean_value = ifelse(!is.na(completeness) & completeness >= completeness_thr, mean_value, NA_real_)
    )

  wide <- monthly_pol |>
    dplyr::select(month_id, pollutant, mean_value) |>
    tidyr::pivot_wider(names_from = pollutant, values_from = mean_value)

  needed <- c("NO2", "O3", "PM25", "PM10")
  for (p in needed) if (!p %in% names(wide)) wide[[p]] <- NA_real_
  wide <- wide |> dplyr::select(month_id, dplyr::all_of(needed))

  comp_wide <- monthly_pol |>
    dplyr::select(month_id, pollutant, completeness) |>
    tidyr::pivot_wider(names_from = pollutant, values_from = completeness, names_prefix = "completeness_")

  pollution_monthly <- wide |>
    dplyr::left_join(comp_wide, by = "month_id") |>
    dplyr::mutate(
      data_status = "EPD_GENERAL_STATIONS",
      station_set = "general_unweighted_mean",
      unit = "ug_m3",
      notes = "Official EPD EPIC monthly averages; unweighted mean of general stations; month set to NA if station completeness < threshold"
    )

} else if (length(legacy_csvs) && all(vapply(legacy_csvs, is_epic_wide, logical(1)))) {
  stop("Found CSVs but none matching epd_general_monthly_*.csv naming. Rename or re-run download script.")
} else if (file.exists(file.path(epd_dir, "epd_monthly_PLACEHOLDER.csv"))) {
  message("Using PLACEHOLDER pollution series for pipeline testing only.")
  pollution_monthly <- utils::read.csv(
    file.path(epd_dir, "epd_monthly_PLACEHOLDER.csv"),
    stringsAsFactors = FALSE
  ) |>
    dplyr::select(dplyr::any_of(c(
      "month_id", "NO2", "O3", "PM25", "PM10", "data_status", "station_set", "unit", "notes"
    )))
} else {
  stop("No pollution inputs found. Run scripts/18_download_epd_epic_monthly.py then this script.")
}

# Restrict to study window
pollution_monthly <- pollution_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  ) |>
  dplyr::arrange(month_id)

stopifnot(!any(duplicated(pollution_monthly$month_id)))
assert_month_id(pollution_monthly$month_id)
validate_required_columns(
  pollution_monthly,
  c("month_id", "NO2", "O3", "PM25", "PM10"),
  "pollution_monthly"
)

out_path <- file.path(root, "data_processed", "pollution_monthly_2013_2023.csv")
write_csv_safe(pollution_monthly, out_path)

# Update import status
status_lines <- c(
  paste0(
    "status: ",
    if (any(grepl("PLACEHOLDER", pollution_monthly$data_status %||% ""))) {
      "PLACEHOLDER_ONLY"
    } else {
      "EPD_EPIC_GENERAL_IMPORTED"
    }
  ),
  paste("n_months:", nrow(pollution_monthly)),
  paste("n_general_files:", length(general_csvs)),
  paste("completeness_threshold:", completeness_thr),
  paste("written:", out_path),
  paste("checked_at:", as.character(Sys.time()))
)
writeLines(status_lines, file.path(epd_dir, "import_status.txt"))

message("Pollution monthly build complete. Rows: ", nrow(pollution_monthly))
if (any(grepl("PLACEHOLDER", pollution_monthly$data_status %||% ""))) {
  message("WARNING: pollution file contains PLACEHOLDER values — not for substantive inference.")
} else {
  message(
    "Means — NO2: ", round(mean(pollution_monthly$NO2, na.rm = TRUE), 1),
    " O3: ", round(mean(pollution_monthly$O3, na.rm = TRUE), 1),
    " PM25: ", round(mean(pollution_monthly$PM25, na.rm = TRUE), 1),
    " PM10: ", round(mean(pollution_monthly$PM10, na.rm = TRUE), 1)
  )
}
