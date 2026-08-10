#!/usr/bin/env Rscript
# 23_pathway_diagnostics.R
# Real outcome-specific residual, autocorrelation and influence diagnostics.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines", "ggplot2"))

outcome <- tolower(Sys.getenv("OUTCOME", unset = "stroke"))
mode <- tolower(Sys.getenv("PATHWAY_MODE", unset = "dev"))
panel_path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
fit_path <- file.path(root, "outputs", "tables", paste0(outcome, "_pathway_panel_fit_stats.csv"))
reg <- yaml::read_yaml(file.path(root, "analysis_plan", "pathway_registry.yml"))

if (!file.exists(panel_path) || !file.exists(fit_path)) {
  stop("Run the ", outcome, " pathway fit first (panel + fit stats required).")
}

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
fit <- utils::read.csv(fit_path, stringsAsFactors = FALSE)
validate_required_columns(
  panel,
  c("month_id", "n_events", "data_status", "time_index", "month"),
  paste(outcome, "analysis panel")
)

statuses <- unique(as.character(panel$data_status))
is_synthetic <- any(grepl("SYNTHETIC", statuses, ignore.case = TRUE))
if (identical(mode, "real")) {
  if (is_synthetic || !identical(statuses, "HA_APPROVED_AGGREGATE")) {
    stop(
      "Real diagnostics require data_status=HA_APPROVED_AGGREGATE only; found: ",
      paste(statuses, collapse = ", ")
    )
  }
  if (nrow(panel) != 132L) {
    stop("Real territory-month diagnostics expected 132 rows; found ", nrow(panel))
  }
}

panel <- panel |>
  dplyr::arrange(time_index) |>
  dplyr::mutate(
    month_f = factor(month),
    age_group = factor(age_group),
    sex = factor(sex)
  )

has_age_sex <- !all(panel$age_group %in% c("all", "", NA)) &&
  !all(panel$sex %in% c("all", "", NA))

offset_term <- function(spec, dat) {
  policy <- spec$offset %||% "population_x_days"
  if (identical(policy, "days_only")) {
    if (!"offset_log_days" %in% names(dat)) stop("offset_log_days missing")
    return("offset(offset_log_days)")
  }
  if (!"offset_log" %in% names(dat)) stop("offset_log missing")
  "offset(offset_log)"
}

core_targets <- c("P01A", "P02A", "P02B", "P04A", "P04B", "P04C")
legacy_targets <- unlist(reg$headline_proposal %||% c("P02", "P04"))
targets <- unique(c(core_targets[core_targets %in% names(reg$pathways)], legacy_targets))

diag_rows <- list()
acf_rows <- list()
influence_rows <- list()

for (pid in targets) {
  spec <- reg$pathways[[pid]]
  if (is.null(spec) || !isTRUE(spec$enabled)) next
  exposures <- unlist(spec$exposures)
  if (!all(exposures %in% names(panel))) next

  terms <- exposures
  if (!is.null(spec$scale) && !is.na(spec$scale)) {
    terms <- sprintf("I(%s / %s)", exposures, spec$scale)
  }
  rhs <- c(
    terms,
    "month_f",
    paste0("splines::ns(time_index, df = ", cfg$modeling$time_trend_df %||% 4, ")")
  )
  if (has_age_sex) rhs <- c(rhs, "age_group", "sex")
  fml <- stats::as.formula(
    paste("n_events ~", paste(rhs, collapse = " + "), "+", offset_term(spec, panel))
  )

  fit_family <- "negative_binomial"
  model <- tryCatch(
    MASS::glm.nb(fml, data = panel),
    error = function(e) {
      fit_family <<- "quasipoisson_fallback"
      stats::glm(fml, data = panel, family = stats::quasipoisson())
    }
  )

  res <- stats::residuals(model, type = "pearson")
  keep <- is.finite(res)
  res <- res[keep]
  month_ids <- panel$month_id[keep]
  n <- length(res)
  rdf <- max(stats::df.residual(model), 1)
  dispersion <- sum(res^2, na.rm = TRUE) / rdf
  cooks <- tryCatch(stats::cooks.distance(model), error = function(e) rep(NA_real_, nrow(panel)))
  cooks <- cooks[keep]
  max_cook_idx <- if (all(is.na(cooks))) NA_integer_ else which.max(cooks)

  acf_obj <- stats::acf(res, plot = FALSE, lag.max = min(12, n - 1), na.action = na.pass)
  pacf_obj <- stats::pacf(res, plot = FALSE, lag.max = min(12, n - 1), na.action = na.pass)
  acf_values <- as.numeric(acf_obj$acf)[-1]
  pacf_values <- as.numeric(pacf_obj$acf)
  lags <- seq_along(acf_values)

  diag_rows[[pid]] <- data.frame(
    outcome = outcome,
    pathway_id = pid,
    n = n,
    data_status = paste(statuses, collapse = ";"),
    family = fit_family,
    offset_policy = spec$offset %||% "population_x_days",
    pearson_mean = mean(res, na.rm = TRUE),
    pearson_sd = stats::sd(res, na.rm = TRUE),
    pearson_dispersion = dispersion,
    pearson_abs_gt2 = sum(abs(res) > 2, na.rm = TRUE),
    pearson_abs_gt3 = sum(abs(res) > 3, na.rm = TRUE),
    residual_acf1 = if (length(acf_values)) acf_values[1] else NA_real_,
    ljung_box_p_lag6 = if (n > 6) stats::Box.test(res, lag = 6, type = "Ljung-Box", fitdf = 0)$p.value else NA_real_,
    ljung_box_p_lag12 = if (n > 12) stats::Box.test(res, lag = 12, type = "Ljung-Box", fitdf = 0)$p.value else NA_real_,
    max_cooks_distance = if (all(is.na(cooks))) NA_real_ else max(cooks, na.rm = TRUE),
    max_cook_month = if (is.na(max_cook_idx)) NA_character_ else month_ids[max_cook_idx],
    aic = tryCatch(stats::AIC(model), error = function(e) NA_real_),
    theta = tryCatch(model$theta, error = function(e) NA_real_),
    converged = tryCatch(model$converged, error = function(e) NA),
    synthetic = is_synthetic,
    stringsAsFactors = FALSE
  )

  acf_rows[[pid]] <- data.frame(
    outcome = outcome,
    pathway_id = pid,
    lag = lags,
    acf = acf_values,
    pacf = pacf_values[seq_along(lags)],
    stringsAsFactors = FALSE
  )

  influence_rows[[pid]] <- data.frame(
    outcome = outcome,
    pathway_id = pid,
    month_id = month_ids,
    pearson_residual = res,
    cooks_distance = cooks,
    stringsAsFactors = FALSE
  ) |>
    dplyr::arrange(dplyr::desc(cooks_distance)) |>
    dplyr::slice_head(n = 10)
}

diag_df <- dplyr::bind_rows(diag_rows)
acf_df <- dplyr::bind_rows(acf_rows)
influence_df <- dplyr::bind_rows(influence_rows)
if (!nrow(diag_df)) stop("No diagnostic models were fit for ", outcome)
if (identical(mode, "real") && (any(diag_df$synthetic) || any(diag_df$n > 132))) {
  stop("Fatal real-release diagnostic contamination for ", outcome)
}

out_tab <- file.path(root, "outputs", "tables")
out_fig <- file.path(root, "outputs", "figures", "diagnostics")
out_rep <- file.path(root, "outputs", "reports")
dir.create(out_tab, recursive = TRUE, showWarnings = FALSE)
dir.create(out_fig, recursive = TRUE, showWarnings = FALSE)
dir.create(out_rep, recursive = TRUE, showWarnings = FALSE)

write_csv_safe(diag_df, file.path(out_tab, paste0(outcome, "_pathway_core_diagnostics.csv")))
write_csv_safe(acf_df, file.path(out_tab, paste0(outcome, "_pathway_residual_acf.csv")))
write_csv_safe(influence_df, file.path(out_tab, paste0(outcome, "_pathway_influence_top10.csv")))

fit_note <- fit |>
  dplyr::group_by(pathway_id) |>
  dplyr::summarise(
    stages = dplyr::n(),
    aic_min = if (all(is.na(aic))) NA_real_ else min(aic, na.rm = TRUE),
    any_nonconverged = any(!converged %in% TRUE),
    .groups = "drop"
  )
write_csv_safe(fit_note, file.path(out_tab, paste0(outcome, "_pathway_fit_overview.csv")))

acf_long <- dplyr::bind_rows(
  acf_df |> dplyr::transmute(pathway_id, lag, measure = "ACF", value = acf),
  acf_df |> dplyr::transmute(pathway_id, lag, measure = "PACF", value = pacf)
)
p <- ggplot2::ggplot(acf_long, ggplot2::aes(lag, value)) +
  ggplot2::geom_hline(yintercept = 0, colour = "grey55") +
  ggplot2::geom_col(width = 0.72, fill = "#386c78") +
  ggplot2::facet_grid(pathway_id ~ measure) +
  ggplot2::scale_x_continuous(breaks = seq(1, 12, 2)) +
  ggplot2::labs(
    title = paste(toupper(outcome), "real-panel residual autocorrelation"),
    subtitle = "Pearson residuals; outcome-specific HA_APPROVED_AGGREGATE panel",
    x = "Lag (months)",
    y = "Correlation"
  ) +
  ggplot2::theme_minimal(base_size = 10)
ggplot2::ggsave(
  file.path(out_fig, paste0(outcome, "_core_residual_acf_pacf.png")),
  p,
  width = 9,
  height = max(6, 1.25 * length(unique(acf_long$pathway_id))),
  dpi = 300
)

rep <- file.path(out_rep, paste0(outcome, "_pathway_diagnostics_note.md"))
writeLines(
  c(
    paste0("# Real pathway diagnostics — ", toupper(outcome)),
    "",
    paste0("- Written: ", as.character(Sys.time())),
    paste0("- Panel: `", panel_path, "`"),
    paste0("- Rows: ", nrow(panel)),
    paste0("- data_status: ", paste(statuses, collapse = ";")),
    paste0("- Models diagnosed: ", paste(diag_df$pathway_id, collapse = ", ")),
    "",
    "Review residual autocorrelation, Ljung–Box tests, dispersion and influential months before manuscript claims.",
    "",
    paste0("Tables: `outputs/tables/", outcome, "_pathway_core_diagnostics.csv`, `",
           outcome, "_pathway_residual_acf.csv`, and `", outcome, "_pathway_influence_top10.csv`.")
  ),
  rep
)
message("Real diagnostics written for ", outcome, ": ", nrow(diag_df), " models; n=", nrow(panel))
