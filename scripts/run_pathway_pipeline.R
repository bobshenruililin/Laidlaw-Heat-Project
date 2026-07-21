#!/usr/bin/env Rscript
# run_pathway_pipeline.R
# End-to-end multi-pathway pipeline for stroke aggregates.
#
# Modes:
#   PATHWAY_MODE=dev   (default) — build exposures, simulate stroke, QC, merge, fit panel
#   PATHWAY_MODE=real  — require non-synthetic stroke file in data_raw/ha_secure_placeholder/

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)
mode <- Sys.getenv("PATHWAY_MODE", unset = "dev")

scripts_common <- c(
  "scripts/00_setup.R",
  "scripts/19_build_analysis_exposures.R"
)

if (identical(mode, "dev")) {
  scripts <- c(
    scripts_common,
    "scripts/07b_simulate_stroke_aggregates.R",
    "scripts/08c_qc_stroke_aggregates.R",
    "scripts/08d_merge_stroke_panel.R",
    "scripts/20_fit_pathway_panel.R"
  )
} else if (identical(mode, "real")) {
  scripts <- c(
    scripts_common,
    "scripts/08c_qc_stroke_aggregates.R",
    "scripts/08d_merge_stroke_panel.R"
  )
} else {
  stop("Unknown PATHWAY_MODE=", mode, " (use dev or real)")
}

message("===== PATHWAY PIPELINE mode=", mode, " =====")
for (s in scripts) {
  message("\n========== RUNNING ", s, " ==========\n")
  rc <- system2("Rscript", s)
  if (rc != 0) stop("Pathway pipeline failed at ", s, " (exit ", rc, ")")
}

# Real mode: refuse SYNTHETIC before fitting
if (identical(mode, "real")) {
  receipt <- file.path(root, "outputs", "reports", "stroke_data_qc_receipt.md")
  norm <- file.path(root, "data_processed", "stroke_aggregates_normalized.csv")
  syn <- FALSE
  if (file.exists(receipt)) {
    txt <- paste(readLines(receipt, warn = FALSE), collapse = "\n")
    if (grepl("SYNTHETIC", txt)) syn <- TRUE
  }
  if (file.exists(norm)) {
    st <- unique(utils::read.csv(norm, stringsAsFactors = FALSE)$data_status)
    if (any(grepl("SYNTHETIC", st))) syn <- TRUE
  }
  if (syn) {
    stop("PATHWAY_MODE=real but stroke file is SYNTHETIC. Place approved aggregates first.")
  }
  message("\n========== RUNNING scripts/20_fit_pathway_panel.R ==========\n")
  rc <- system2("Rscript", "scripts/20_fit_pathway_panel.R")
  if (rc != 0) stop("Pathway pipeline failed at fit (exit ", rc, ")")
}

message("\nPathway pipeline completed. See outputs/reports/pathway_panel_summary.md")
