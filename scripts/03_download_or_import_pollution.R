#!/usr/bin/env Rscript
# 03_download_or_import_pollution.R
# Prefer automated EPIC monthly download (script 18). Falls back to documenting
# the manual portal workflow if Python download has not been run yet.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "readr"))

epd_dir <- file.path(root, cfg$pollution$raw_dir)
dir.create(epd_dir, recursive = TRUE, showWarnings = FALSE)

general_csvs <- list.files(epd_dir, pattern = "^epd_general_monthly_.*\\.csv$", full.names = TRUE)
roadside_csvs <- list.files(epd_dir, pattern = "^epd_roadside_monthly_.*\\.csv$", full.names = TRUE)

if (!length(general_csvs)) {
  py <- file.path(root, "scripts", "18_download_epd_epic_monthly.py")
  message("No EPIC general monthly CSVs found. Attempting: python3 ", py)
  status <- system2("python3", args = c(py, "--include-roadside"), stdout = TRUE, stderr = TRUE)
  writeLines(status)
  general_csvs <- list.files(epd_dir, pattern = "^epd_general_monthly_.*\\.csv$", full.names = TRUE)
  roadside_csvs <- list.files(epd_dir, pattern = "^epd_roadside_monthly_.*\\.csv$", full.names = TRUE)
}

if (length(general_csvs)) {
  message("Found EPD EPIC general monthly files:")
  print(basename(general_csvs))
  if (length(roadside_csvs)) {
    message("Roadside files (sensitivity only):")
    print(basename(roadside_csvs))
  }
  # Remove obsolete placeholder if real files exist
  ph <- file.path(epd_dir, "epd_monthly_PLACEHOLDER.csv")
  if (file.exists(ph)) {
    file.remove(ph)
    message("Removed obsolete placeholder: ", basename(ph))
  }
  writeLines(
    c(
      "status: REAL_FILES_PRESENT",
      paste("n_general_files:", length(general_csvs)),
      paste("n_roadside_files:", length(roadside_csvs)),
      paste("general_files:", paste(basename(general_csvs), collapse = "; ")),
      paste("checked_at:", as.character(Sys.time()))
    ),
    file.path(epd_dir, "import_status.txt")
  )
} else {
  message("WARNING: Still no EPIC CSVs. Writing PLACEHOLDER for pipeline testing only.")
  message("THIS IS NOT ANALYTIC-GRADE POLLUTION DATA.")
  set.seed(cfg$project$seed)
  months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)
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

message("Pollution import step complete. See ", file.path(epd_dir, "README_manual_download.md"))
