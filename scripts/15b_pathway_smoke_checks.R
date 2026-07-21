#!/usr/bin/env Rscript
# 15b_pathway_smoke_checks.R — assert pathway plumbing before real data

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)

required <- c(
  "analysis_plan/pathway_registry.yml",
  "analysis_plan/pathway_catalogue.md",
  "analysis_plan/statistical_analysis_protocol.md",
  "schemas/ha_stroke_aggregate.schema.json",
  "data_processed/exposures_monthly_2013_2023.csv",
  "scripts/run_pathway_pipeline.R",
  "scripts/20_fit_pathway_panel.R",
  "scripts/23_pathway_diagnostics.R",
  "scripts/24_pathway_forest_figure.R"
)
missing <- required[!file.exists(file.path(root, required))]
if (length(missing)) stop("Missing required pathway files:\n", paste(missing, collapse = "\n"))

exp <- utils::read.csv(file.path(root, "data_processed", "exposures_monthly_2013_2023.csv"), stringsAsFactors = FALSE)
stopifnot(nrow(exp) == 132)
need_cols <- c(
  "lag1_mean_tmax", "hw_month_mean_temp_ge_p90", "hw_month_mean_temp_ge_p95",
  "hw_month_mean_temp_ge_p975", "cold_month_mean_temp_le_p05",
  "days_in_2d3n_window", "temp_variability_mean_range"
)
stopifnot(all(need_cols %in% names(exp)))
stopifnot(!anyNA(exp$lag1_mean_tmax))
stopifnot(!anyNA(exp$temp_variability_mean_range))

status_path <- file.path(root, "outputs", "tables", "pathway_panel_status.csv")
if (file.exists(status_path)) {
  st <- utils::read.csv(status_path, stringsAsFactors = FALSE)
  n_ok <- sum(st$status == "ok")
  if (n_ok < 16) stop("Expected >=16 pathways ok in last dry-run; found ", n_ok)
  message("Pathway smoke OK: ", n_ok, " pathways ok in last run")
} else {
  message("No pathway_panel_status.csv yet — run run_pathway_pipeline.R")
}

forest <- file.path(root, "outputs", "figures", "pathway", "pathway_panel_forest.png")
if (!file.exists(forest)) message("Note: forest figure not yet written (expected after full pipeline).")

message("15b pathway smoke checks passed.")
