#!/usr/bin/env Rscript
# 36_cvd_final_model_ensemble.R
# Real-only runner: six core exposures × CHD/HF × frozen scenarios + GLARMA + stacked Δ.
# Provenance: HA_APPROVED_AGGREGATE only. result_class = EXPLORATORY_POST_OUTCOME.
# Does not invent coefficients when governed panels are absent.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "final_model_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c(
  "dplyr", "yaml", "MASS", "splines", "sandwich", "lmtest", "glarma"
))

registry <- load_final_model_registry(root = root)
specs <- core_exposure_specs(registry)
scenarios <- scenario_defs(registry)
outcomes <- registry$outcomes %||% c("chd", "hf")

out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

panel_paths <- setNames(
  file.path(root, "data_processed", paste0(outcomes, "_analysis_panel.csv")),
  outcomes
)
missing <- !file.exists(panel_paths)
if (any(missing)) {
  blocker <- missing_governed_panel_blocker(
    outcomes = outcomes,
    root = root,
    script_id = "36_cvd_final_model_ensemble"
  )
  handle_missing_governed_panels(
    blocker,
    file.path(out_dir, "cvd_final_ensemble_blocker.csv")
  )
}

panels <- lapply(outcomes, function(outcome) {
  dat <- utils::read.csv(panel_paths[[outcome]], stringsAsFactors = FALSE)
  prepare_analysis_panel(dat, require_real = TRUE, outcome = outcome)
})
names(panels) <- outcomes

estimate_rows <- list()
status_rows <- list()
glarma_rows <- list()
glarma_diag_rows <- list()

for (outcome in outcomes) {
  dat <- panels[[outcome]]
  for (pid in names(specs)) {
    spec <- specs[[pid]]
    for (sid in names(scenarios)) {
      scenario <- scenarios[[sid]]
      key <- paste(outcome, pid, sid, sep = "::")
      fit <- fit_scenario_nb(
        dat = dat,
        pathway_id = pid,
        exposure_spec = spec,
        scenario = scenario,
        registry = registry,
        offset_policy = "days_only",
        model_id = registry$analysis_of_record$model_id %||% "M01_NB_MONTH_NW6",
        result_class = RESULT_CLASS_EXPLORATORY,
        data_status = REAL_PROVENANCE
      )
      status_rows[[key]] <- fit$status
      if (!is.null(fit$estimates) && nrow(fit$estimates)) {
        est <- fit$estimates
        est$result_class <- RESULT_CLASS_EXPLORATORY
        est$data_status <- REAL_PROVENANCE
        estimate_rows[[key]] <- est
      }
    }

    # GLARMA on baseline design only (R01 controls), days offset.
    base_scenario <- scenarios[["R01_baseline_ns4"]]
    prep <- apply_scenario(dat, base_scenario, pid, spec, registry)
    gkey <- paste(outcome, pid, "GLARMA", sep = "::")
    if (!isTRUE(prep$ok)) {
      status_rows[[gkey]] <- status_row(
        prep$status, prep$message,
        outcome = outcome,
        pathway_id = pid,
        exposure = spec$variable,
        contrast = spec$contrast,
        scenario_id = "R01_baseline_ns4",
        model_id = "M02_M04_GLARMA_SELECT",
        result_class = RESULT_CLASS_EXPLORATORY,
        data_status = REAL_PROVENANCE,
        n_months = nrow(dat)
      )
    } else {
      gfit <- fit_nb_glarma_ensemble(
        prep$data,
        prep$exposure_term,
        prep$controls,
        offset_policy = "days_only",
        metadata = list(
          outcome = outcome,
          pathway_id = pid,
          exposure = spec$variable,
          contrast = spec$contrast,
          scenario_id = "R01_baseline_ns4",
          result_class = RESULT_CLASS_EXPLORATORY,
          data_status = REAL_PROVENANCE
        )
      )
      status_rows[[gkey]] <- gfit$status
      if (!is.null(gfit$diagnostics)) {
        gd <- gfit$diagnostics
        gd$outcome <- outcome
        gd$pathway_id <- pid
        gd$exposure <- spec$variable
        gd$result_class <- RESULT_CLASS_EXPLORATORY
        gd$data_status <- REAL_PROVENANCE
        glarma_diag_rows[[gkey]] <- gd
      }
      if (!is.null(gfit$estimates)) {
        gest <- gfit$estimates
        gest$result_class <- RESULT_CLASS_EXPLORATORY
        gest$data_status <- REAL_PROVENANCE
        glarma_rows[[gkey]] <- gest
      }
    }
  }
}

# Stacked hot-vs-cold cross-outcome contrast
cross <- registry$cross_outcome
stacked <- fit_stacked_heat_cold_contrast(
  panels[["chd"]],
  panels[["hf"]],
  heat_variable = cross$heat_variable %||% "hot_nights",
  cold_variable = cross$cold_variable %||% "cold_days",
  contrast_days = as.numeric(cross$contrast_days %||% 5),
  offset_policy = "days_only",
  result_class = RESULT_CLASS_EXPLORATORY
)
status_rows[["stacked"]] <- stacked$status

est_df <- if (length(estimate_rows)) dplyr::bind_rows(estimate_rows) else {
  data.frame(stringsAsFactors = FALSE)
}
glarma_df <- if (length(glarma_rows)) dplyr::bind_rows(glarma_rows) else {
  data.frame(stringsAsFactors = FALSE)
}
status_df <- dplyr::bind_rows(status_rows)
diag_df <- if (length(glarma_diag_rows)) dplyr::bind_rows(glarma_diag_rows) else {
  data.frame(stringsAsFactors = FALSE)
}
stacked_df <- if (isTRUE(stacked$ok)) stacked$contrast else {
  data.frame(
    model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
    status = stacked$status$status,
    message = stacked$status$message,
    result_class = RESULT_CLASS_EXPLORATORY,
    data_status = REAL_PROVENANCE,
    stringsAsFactors = FALSE
  )
}

# SE ladder table is the long estimate table (model/HC1/NW3/NW6).
write_csv_safe(est_df, file.path(out_dir, "cvd_final_ensemble_estimates.csv"))
write_csv_safe(est_df, file.path(out_dir, "cvd_final_ensemble_se_ladder.csv"))
write_csv_safe(status_df, file.path(out_dir, "cvd_final_ensemble_fit_status.csv"))
write_csv_safe(glarma_df, file.path(out_dir, "cvd_final_ensemble_glarma_estimates.csv"))
write_csv_safe(diag_df, file.path(out_dir, "cvd_final_ensemble_glarma_diagnostics.csv"))
write_csv_safe(stacked_df, file.path(out_dir, "cvd_final_stacked_interaction.csv"))

message(
  "Final model ensemble complete: ",
  nrow(est_df), " NB ladder rows; ",
  nrow(status_df), " status rows; stacked ok=", isTRUE(stacked$ok)
)
