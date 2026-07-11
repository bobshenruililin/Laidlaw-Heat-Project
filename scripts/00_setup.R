#!/usr/bin/env Rscript
# 00_setup.R — create folders, install packages, record session info

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)

dirs <- c(
  "analysis_plan",
  "data_raw/hko/daily_extract",
  "data_raw/epd",
  "data_raw/csd_population",
  "data_raw/chp_flu",
  "data_raw/ha_secure_placeholder",
  "data_processed",
  "data_processed/.cache",
  "figures",
  "outputs/tables",
  "outputs/figures/exploratory",
  "outputs/figures/synthetic_diagnostic_plots",
  "outputs/figures/ha_diagnostic_plots",
  "outputs/model_objects",
  "outputs/table_shells",
  "literature",
  "memos",
  "reports/latex",
  "manuscript",
  "schemas"
)
for (d in dirs) dir.create(file.path(root, d), recursive = TRUE, showWarnings = FALSE)

pkgs <- c(
  "yaml", "jsonlite", "dplyr", "tidyr", "readr", "lubridate",
  "ggplot2", "MASS", "splines", "sandwich", "lmtest", "digest"
)
ensure_packages(pkgs)

set.seed(cfg$project$seed %||% 20250308)

session_path <- file.path(root, "outputs", "session_info_setup.txt")
writeLines(c(
  paste("timestamp:", as.character(Sys.time())),
  paste("project_root:", root),
  capture.output(sessionInfo())
), session_path)

message("Setup complete. Session info: ", session_path)
