#!/usr/bin/env Rscript
# run_cvd_full_analysis.R
# Playbook 02→03 orchestrator for multi-outcome HA first-hospitalisation aggregates.
#
# Usage:
#   PATHWAY_MODE=real Rscript scripts/run_cvd_full_analysis.R
#   OUTCOMES=chd,hf PATHWAY_MODE=real Rscript scripts/run_cvd_full_analysis.R

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
setwd(root)
mode <- Sys.getenv("PATHWAY_MODE", unset = "real")
outcomes <- strsplit(Sys.getenv("OUTCOMES", unset = "chd,hf"), ",", fixed = TRUE)[[1]]
outcomes <- trimws(tolower(outcomes))
if (!identical(mode, "real")) {
  stop("run_cvd_full_analysis.R is real-only. Set PATHWAY_MODE=real.")
}
if (!length(outcomes) || any(!outcomes %in% c("chd", "hf"))) {
  stop("OUTCOMES must be a comma-separated subset of chd,hf")
}

run_one <- function(script, env = character()) {
  message("\n========== RUNNING ", script, " ==========\n")
  rc <- system2("Rscript", script, env = unique(c(paste0("PATHWAY_MODE=", mode), env)))
  if (rc != 0) stop("Failed at ", script, " (exit ", rc, ")")
}

message("===== CVD FULL ANALYSIS mode=", mode, " outcomes=", paste(outcomes, collapse = ","), " =====")

# Shared exposure stack
for (s in c(
  "scripts/00_setup.R",
  "scripts/06_build_confounders.R",
  "scripts/06b_build_hk_holidays.R",
  "scripts/19_build_analysis_exposures.R",
  "scripts/19b_build_hm_cm_exposures.R"
)) {
  run_one(s)
}

for (outcome in outcomes) {
  message("\n##### OUTCOME=", outcome, " #####\n")
  env <- c(paste0("OUTCOME=", outcome), paste0("PATHWAY_MODE=", mode))
  run_one("scripts/08c_qc_cvd_aggregates.R", env)
  # Refuse synthetic in real mode
  if (identical(mode, "real")) {
    norm <- file.path(root, "data_processed", paste0(outcome, "_aggregates_normalized.csv"))
    st <- unique(utils::read.csv(norm, stringsAsFactors = FALSE)$data_status)
    if (any(grepl("SYNTHETIC", st))) stop("Real mode refused SYNTHETIC for ", outcome)
  }
  run_one("scripts/08d_merge_cvd_panel.R", env)
  run_one("scripts/20_fit_pathway_panel.R", env)
  run_one("scripts/20b_fit_hm_cm_panel.R", env)
  run_one("scripts/22_make_pathway_manuscript_tables.R", env)
  run_one("scripts/23_pathway_diagnostics.R", env)
  run_one("scripts/24_pathway_forest_figure.R", env)
}

# Combined cross-outcome table (needed before script 30)
tabs <- lapply(outcomes, function(o) {
  f <- file.path(root, "outputs", "tables", paste0(o, "_pathway_panel_estimates.csv"))
  if (!file.exists(f)) return(NULL)
  d <- utils::read.csv(f, stringsAsFactors = FALSE)
  if (!"outcome" %in% names(d)) d$outcome <- o
  d
})
comb <- do.call(rbind, tabs[!vapply(tabs, is.null, logical(1))])
if (!is.null(comb) && nrow(comb)) {
  utils::write.csv(comb, file.path(root, "outputs", "tables", "combined_pathway_panel_estimates.csv"), row.names = FALSE)
}

# Post-panel PhD-grade extensions (do not re-fit full pathway panel)
for (s in c(
  "scripts/27_cvd_descriptives_real.R",
  "scripts/28_cvd_sensitivity_offsets.R",
  "scripts/29_cvd_period_split.R",
  "scripts/30_cvd_cross_outcome_forest.R",
  "scripts/31_cvd_core_robustness.R",
  "scripts/32_cvd_trend_depletion_lag.R",
  "scripts/33_cvd_publication_artifacts.R",
  "scripts/34_cvd_real_release_checks.R"
)) {
  run_one(s)
}

message("\nCVD full analysis completed for: ", paste(outcomes, collapse = ", "))
message("See outputs/reports/*_pathway_panel_summary.md and outputs/tables/")
