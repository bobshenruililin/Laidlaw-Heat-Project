#!/usr/bin/env Rscript
# 04_build_pollution_monthly.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr", "readr"))

epd_dir <- file.path(root, cfg$pollution$raw_dir)
status_file <- file.path(epd_dir, "import_status.txt")
status <- if (file.exists(status_file)) paste(readLines(status_file), collapse = "\n") else ""

placeholder_path <- file.path(epd_dir, "epd_monthly_PLACEHOLDER.csv")
real_csvs <- list.files(epd_dir, pattern = "\\.csv$", full.names = TRUE)
real_csvs <- real_csvs[!grepl("PLACEHOLDER|placeholder", basename(real_csvs))]

normalize_names <- function(nm) {
  nm <- toupper(gsub("[^A-Za-z0-9]+", "", nm))
  nm
}

if (length(real_csvs)) {
  message("Building pollution monthly file from real EPD CSVs (flexible parser).")
  pieces <- lapply(real_csvs, function(f) {
    df <- utils::read.csv(f, stringsAsFactors = FALSE, check.names = FALSE)
    nms <- normalize_names(names(df))
    names(df) <- nms
    df$source_file <- basename(f)
    df
  })
  raw <- dplyr::bind_rows(pieces)

  # Attempt to locate date and pollutant columns
  date_col <- intersect(c("DATE", "DATETIME", "YEARMONTH", "MONTHID", "YEAR"), names(raw))
  # This flexible parser expects either monthly pre-aggregates with NO2/O3/PM25/PM10
  # or daily rows with DATE + pollutant columns. Hogan should finalize station logic.
  if ("YEAR" %in% names(raw) && "MONTH" %in% names(raw)) {
    raw$month_id <- sprintf("%04d-%02d", as.integer(raw$YEAR), as.integer(raw$MONTH))
  } else if ("DATE" %in% names(raw)) {
    raw$DATE <- as.Date(raw$DATE)
    raw$month_id <- format(raw$DATE, "%Y-%m")
  } else if ("MONTHID" %in% names(raw)) {
    raw$month_id <- raw$MONTHID
  } else {
    stop("Could not infer date/month columns from EPD files. Please standardize inputs.")
  }

  # Map common aliases
  rename_map <- c(
    NO2 = "NO2", NOX = "NO2",
    O3 = "O3", OZONE = "O3",
    PM25 = "PM25", FSP = "PM25", PM2POINT5 = "PM25",
    PM10 = "PM10", RSP = "PM10"
  )
  for (src in names(rename_map)) {
    if (src %in% names(raw) && !rename_map[[src]] %in% names(raw)) {
      raw[[rename_map[[src]]]] <- raw[[src]]
    }
  }

  needed <- c("NO2", "O3", "PM25", "PM10")
  missing <- setdiff(needed, names(raw))
  if (length(missing)) {
    stop("Missing pollutant columns after alias mapping: ", paste(missing, collapse = ", "))
  }

  pollution_monthly <- raw |>
    dplyr::group_by(month_id) |>
    dplyr::summarise(
      NO2 = mean(as.numeric(NO2), na.rm = TRUE),
      O3 = mean(as.numeric(O3), na.rm = TRUE),
      PM25 = mean(as.numeric(PM25), na.rm = TRUE),
      PM10 = mean(as.numeric(PM10), na.rm = TRUE),
      n_rows = dplyr::n(),
      data_status = "EPD_IMPORTED_REVIEW_STATION_RULES",
      .groups = "drop"
    )
} else if (file.exists(placeholder_path)) {
  message("Using PLACEHOLDER pollution series for pipeline testing only.")
  pollution_monthly <- utils::read.csv(placeholder_path, stringsAsFactors = FALSE) |>
    dplyr::select(month_id, NO2, O3, PM25, PM10, data_status, station_set, unit, notes)
} else {
  stop("No pollution inputs found. Run 03_download_or_import_pollution.R first.")
}

# Restrict to study window
pollution_monthly <- pollution_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  )

stopifnot(!any(duplicated(pollution_monthly$month_id)))
assert_month_id(pollution_monthly$month_id)
validate_required_columns(
  pollution_monthly,
  c("month_id", "NO2", "O3", "PM25", "PM10"),
  "pollution_monthly"
)
write_csv_safe(pollution_monthly, file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"))

message("Pollution monthly build complete. Rows: ", nrow(pollution_monthly))
if (any(grepl("PLACEHOLDER", pollution_monthly$data_status))) {
  message("WARNING: pollution file contains PLACEHOLDER values — not for substantive inference.")
}
