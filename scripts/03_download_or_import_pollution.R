#!/usr/bin/env Rscript
# 03_download_or_import_pollution.R
# EPD EPIC portal is interactive. This script:
# 1) documents the manual download workflow;
# 2) imports any CSVs placed in data_raw/epd/;
# 3) if none are present, builds a clearly labeled PLACEHOLDER trend file
#    from published annual descriptive patterns for pipeline testing only.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "readr"))

epd_dir <- file.path(root, cfg$pollution$raw_dir)
dir.create(epd_dir, recursive = TRUE, showWarnings = FALSE)

readme <- file.path(epd_dir, "README_manual_download.md")
writeLines(c(
  "# EPD pollution raw data — manual download instructions",
  "",
  "Primary portal: https://cd.epic.epd.gov.hk/EPICDI/air/",
  "",
  "## Recommended download steps",
  "",
  "1. Open EPIC Air Quality Data Download / Display.",
  "2. Select pollutants: NO2, O3, RSP/PM10, FSP/PM2.5 (SO2 optional).",
  "3. Select **general** stations for the primary extract; download roadside separately.",
  "4. Prefer daily or hourly validated data; monthly aggregates are acceptable if completeness metadata are available.",
  "5. Because monthly requests are limited (e.g. 120 months), download in chunks covering 2013–2023 (and optional 2024).",
  "6. Save files into this folder as CSV, e.g.:",
  "   - `epd_general_daily_2013_2017.csv`",
  "   - `epd_general_daily_2018_2022.csv`",
  "   - `epd_general_daily_2023_2024.csv`",
  "   - `epd_roadside_daily_*.csv`",
  "7. Keep a station metadata file if possible (`stations_metadata.csv`).",
  "",
  "## Completeness rule",
  "",
  "Station-month valid if ≥75% of expected observations are present.",
  "",
  "## Units",
  "",
  "Document units as provided by EPD (typically µg/m³ for these pollutants in recent reports).",
  "",
  "Do not overwrite raw files after download; append new versions with dates if revised."
), readme)

csv_files <- list.files(epd_dir, pattern = "\\.csv$", full.names = TRUE)
csv_files <- csv_files[!grepl("placeholder|README", basename(csv_files), ignore.case = TRUE)]

if (length(csv_files)) {
  message("Found EPD CSV files:")
  print(basename(csv_files))
  # Lightweight validation only; detailed cleaning in 04_
  for (f in csv_files) {
    message("Preview ", basename(f))
    print(utils::read.csv(f, nrows = 3, stringsAsFactors = FALSE))
  }
  writeLines(
    c(
      "status: REAL_FILES_PRESENT",
      paste("n_files:", length(csv_files)),
      paste("files:", paste(basename(csv_files), collapse = "; ")),
      paste("checked_at:", as.character(Sys.time()))
    ),
    file.path(epd_dir, "import_status.txt")
  )
} else {
  message("No EPD CSV files found. Writing PLACEHOLDER annual-inspired monthly series for pipeline testing.")
  message("THIS IS NOT ANALYTIC-GRADE POLLUTION DATA.")

  # Approximate territory-wide annual levels informed by published EPD trend direction
  # (declining NO2/PM; rising/high O3). Values are synthetic placeholders for code tests.
  set.seed(cfg$project$seed)
  months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)
  # Simple seasonal + trend placeholders
  t <- months$time_index
  placeholder <- months |>
    dplyr::mutate(
      NO2 = pmax(20, 55 - 0.12 * t + 8 * sin(2 * pi * (month - 1) / 12) + rnorm(dplyr::n(), 0, 2)),
      O3 = pmax(15, 35 + 0.08 * t + 12 * sin(2 * pi * (month - 7) / 12) + rnorm(dplyr::n(), 0, 2.5)),
      PM25 = pmax(8, 30 - 0.10 * t + 6 * sin(2 * pi * (month - 1) / 12) + rnorm(dplyr::n(), 0, 1.5)),
      PM10 = pmax(12, 45 - 0.12 * t + 8 * sin(2 * pi * (month - 1) / 12) + rnorm(dplyr::n(), 0, 2)),
      data_status = "PLACEHOLDER_NOT_FOR_INFERENCE",
      station_set = "placeholder_general",
      unit = "ug_m3_placeholder",
      notes = "Replace with EPIC downloads before substantive pollution analysis"
    )
  out <- file.path(epd_dir, "epd_monthly_PLACEHOLDER.csv")
  write_csv_safe(placeholder, out)
  writeLines(
    c(
      "status: PLACEHOLDER_ONLY",
      "warning: No real EPD files found. Pollution values are synthetic placeholders.",
      paste("written:", out),
      paste("checked_at:", as.character(Sys.time()))
    ),
    file.path(epd_dir, "import_status.txt")
  )
}

message("Pollution import step complete. See ", readme)
