#!/usr/bin/env Rscript
# 23_pathway_diagnostics.R
# Residual / fit diagnostics for headline pathways (and any ok pathways).
# Writes tables + a short markdown note. Does not invent scientific findings.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines"))

panel_path <- file.path(root, "data_processed", "stroke_analysis_panel.csv")
est_path <- file.path(root, "outputs", "tables", "pathway_panel_estimates.csv")
fit_path <- file.path(root, "outputs", "tables", "pathway_panel_fit_stats.csv")
reg <- yaml::read_yaml(file.path(root, "analysis_plan", "pathway_registry.yml"))

if (!file.exists(panel_path) || !file.exists(fit_path)) {
  stop("Run pathway fit first (panel + fit stats missing).")
}

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
fit <- utils::read.csv(fit_path, stringsAsFactors = FALSE)
is_synthetic <- any(grepl("SYNTHETIC", panel$data_status %||% ""))

panel <- panel |>
  dplyr::mutate(
    month_f = factor(month),
    age_group = factor(age_group),
    sex = factor(sex)
  )

has_age_sex <- !all(panel$age_group %in% c("all", "", NA)) &&
  !all(panel$sex %in% c("all", "", NA))

headline <- unlist(reg$headline_proposal %||% c("P02", "P04"))
targets <- unique(c(headline, fit$pathway_id[fit$pathway_id %in% headline]))

diag_rows <- list()
for (pid in targets) {
  spec <- reg$pathways[[pid]]
  if (is.null(spec) || !isTRUE(spec$enabled)) next
  exposures <- spec$exposures
  if (!all(exposures %in% names(panel))) next

  rhs <- c(
    exposures,
    "month_f",
    paste0("splines::ns(time_index, df = ", 4, ")")
  )
  if (has_age_sex) rhs <- c(rhs, "age_group", "sex")
  if (!is.null(spec$scale) && !is.na(spec$scale)) {
    rhs <- setdiff(rhs, exposures)
    rhs <- c(sprintf("I(%s / %s)", exposures, spec$scale), rhs)
  }
  fml <- as.formula(paste("n_events ~", paste(rhs, collapse = " + "), "+ offset(offset_log)"))
  model <- tryCatch(
    MASS::glm.nb(fml, data = panel),
    error = function(e) stats::glm(fml, data = panel, family = stats::quasipoisson())
  )
  res <- residuals(model, type = "pearson")
  diag_rows[[pid]] <- data.frame(
    pathway_id = pid,
    n = length(res),
    pearson_mean = mean(res, na.rm = TRUE),
    pearson_sd = stats::sd(res, na.rm = TRUE),
    pearson_abs_gt2 = sum(abs(res) > 2, na.rm = TRUE),
    pearson_abs_gt3 = sum(abs(res) > 3, na.rm = TRUE),
    aic = tryCatch(AIC(model), error = function(e) NA_real_),
    theta = tryCatch(model$theta, error = function(e) NA_real_),
    converged = tryCatch(model$converged, error = function(e) NA),
    synthetic = is_synthetic,
    stringsAsFactors = FALSE
  )
}

diag_df <- dplyr::bind_rows(diag_rows)
out_tab <- file.path(root, "outputs", "tables")
dir.create(out_tab, recursive = TRUE, showWarnings = FALSE)
write_csv_safe(diag_df, file.path(out_tab, "pathway_headline_diagnostics.csv"))

# Fit-stat overview for all pathways
fit_note <- fit |>
  dplyr::group_by(pathway_id) |>
  dplyr::summarise(
    stages = dplyr::n(),
    aic_min = min(aic, na.rm = TRUE),
    any_nonconverged = any(!converged %in% TRUE),
    .groups = "drop"
  )

write_csv_safe(fit_note, file.path(out_tab, "pathway_fit_overview.csv"))

rep <- file.path(root, "outputs", "reports", "pathway_diagnostics_note.md")
lines <- c(
  "# Pathway diagnostics note",
  "",
  paste0("- Written: ", as.character(Sys.time())),
  paste0("- Synthetic: ", is_synthetic),
  paste0("- Headline pathways diagnosed: ", paste(targets, collapse = ", ")),
  "",
  "See `outputs/tables/pathway_headline_diagnostics.csv` and `pathway_fit_overview.csv`.",
  "",
  if (is_synthetic) {
    "**SYNTHETIC — diagnostics validate plumbing, not model adequacy for inference.**"
  } else {
    "Review Pearson residual extremes and non-convergence before Gate 3 claims."
  }
)
writeLines(lines, rep)
message("Diagnostics written for ", nrow(diag_df), " headline pathway(s).")
