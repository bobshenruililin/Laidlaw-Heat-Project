#!/usr/bin/env Rscript
# 41_fit_md_constrained.R
# Real-only constrained M|D runner.
#
# Default: write missing-governed blocker (panels absent).
# ALLOW_MISSING_GOVERNED=1 exits 0 after blocker.
# Cannot emit a real M|D estimate unless:
#   1) calibration gate summary says PASS, and
#   2) CHD/HF panels exist with exact HA_APPROVED_AGGREGATE provenance.
#
# Even on PASS, result_class is exploratory sensitivity only
# (METHODS_FEASIBILITY until gates pass; never confirmatory).

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
source(file.path("scripts", "md_calibration_helpers.R"))
if (file.exists(file.path("scripts", "final_model_helpers.R"))) {
  source(file.path("scripts", "final_model_helpers.R"))
}
root <- project_root()
setwd(root)
ensure_packages("yaml")

out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cal_dir <- file.path(root, "outputs", "calibration_md")

RESULT_METHODS <- "METHODS_FEASIBILITY"
RESULT_EXPLORATORY <- "EXPLORATORY_POST_OUTCOME_SENSITIVITY"

panel_paths <- c(
  chd = file.path(root, "data_processed", "chd_analysis_panel.csv"),
  hf = file.path(root, "data_processed", "hf_analysis_panel.csv")
)
weather_path <- file.path(root, "data_processed", "md_daily_weather_design_2013_2023.csv")
gate_path <- file.path(cal_dir, "md_calibration_gate_summary.csv")

missing_panels <- !file.exists(panel_paths)
blocker <- data.frame(
  script_id = "41_fit_md_constrained",
  outcome = names(panel_paths),
  panel_path = unname(panel_paths),
  panel_present = !missing_panels,
  weather_design_present = file.exists(weather_path),
  calibration_gate_path = gate_path,
  calibration_gate_present = file.exists(gate_path),
  status = "NOT_RUN_MISSING_GOVERNED_PANEL",
  message = ifelse(
    missing_panels,
    "Governed analysis panel absent; real M|D not run",
    "Panel path present (provenance still required)"
  ),
  result_class = RESULT_METHODS,
  data_status = NA_character_,
  stringsAsFactors = FALSE
)

if (any(missing_panels)) {
  blocker_path <- file.path(out_dir, "md_constrained_blocker.csv")
  write_csv_safe(blocker, blocker_path)
  allow <- identical(Sys.getenv("ALLOW_MISSING_GOVERNED", unset = "0"), "1")
  if (allow) {
    message("ALLOW_MISSING_GOVERNED=1: exiting 0 after blocker ", blocker_path)
    quit(save = "no", status = 0)
  }
  stop(
    "NOT_RUN_MISSING_GOVERNED_PANEL: required governed panels absent. ",
    "Set ALLOW_MISSING_GOVERNED=1 to exit 0 after writing the blocker table."
  )
}

# Panels present: enforce exact real provenance, 132 unique months, calibration PASS.
read_panel <- function(path, outcome) {
  dat <- utils::read.csv(path, stringsAsFactors = FALSE)
  if (!"data_status" %in% names(dat)) {
    stop(outcome, " panel missing data_status column")
  }
  st <- unique(as.character(dat$data_status))
  if (!identical(st, MD_PROVENANCE_REAL) &&
      !identical(st, "HA_APPROVED_AGGREGATE")) {
    stop(
      outcome, " panel provenance is not exact HA_APPROVED_AGGREGATE; got: ",
      paste(st, collapse = ",")
    )
  }
  month_col <- intersect(c("month_id", "ym", "year_month"), names(dat))
  if (!length(month_col)) {
    stop(outcome, " panel missing month_id")
  }
  n_months <- length(unique(as.character(dat[[month_col[[1]]]])))
  if (!identical(as.integer(n_months), 132L)) {
    stop(
      outcome, " panel must have exactly 132 unique months; got ", n_months
    )
  }
  if (!identical(as.integer(nrow(dat)), 132L)) {
    stop(
      outcome, " panel must have exactly 132 rows (one per month); got ", nrow(dat)
    )
  }
  dat
}

panels <- lapply(names(panel_paths), function(o) read_panel(panel_paths[[o]], o))
names(panels) <- names(panel_paths)

if (!file.exists(gate_path)) {
  status <- data.frame(
    script_id = "41_fit_md_constrained",
    status = "BLOCKED_CALIBRATION_GATE_ABSENT",
    message = "Calibration gate summary missing; real M|D estimate suppressed",
    result_class = RESULT_METHODS,
    data_status = MD_PROVENANCE_REAL,
    stringsAsFactors = FALSE
  )
  write_csv_safe(status, file.path(out_dir, "md_constrained_fit_status.csv"))
  quit(save = "no", status = 0)
}

gates <- utils::read.csv(gate_path, stringsAsFactors = FALSE)
if (!"data_status" %in% names(gates) ||
    any(gates$data_status != MD_PROVENANCE_SYNTHETIC)) {
  stop("Calibration gate summary must be labelled SYNTHETIC_CALIBRATION")
}
decision <- unique(as.character(gates$admission_decision))
passed <- length(decision) == 1L &&
  grepl("^PASS", decision[[1]]) &&
  ("all_passed" %in% names(gates)) &&
  isTRUE(all(as.logical(gates$all_passed)))

if (!passed) {
  status <- data.frame(
    script_id = "41_fit_md_constrained",
    status = "BLOCKED_CALIBRATION_GATE_FAIL",
    message = paste0(
      "Calibration gates did not PASS; methods-feasibility failure only. ",
      "admission_decision=", paste(decision, collapse = ",")
    ),
    result_class = RESULT_METHODS,
    data_status = MD_PROVENANCE_REAL,
    stringsAsFactors = FALSE
  )
  write_csv_safe(status, file.path(out_dir, "md_constrained_fit_status.csv"))
  write_csv_safe(
    gates,
    file.path(out_dir, "md_constrained_gate_echo.csv")
  )
  message("Calibration FAIL documented; no real M|D coefficients emitted.")
  quit(save = "no", status = 0)
}

if (!file.exists(weather_path)) {
  stop("Missing daily weather design; run scripts/40_build_daily_weather_design.R first")
}
weather <- utils::read.csv(weather_path, stringsAsFactors = FALSE)
if (!all(weather$data_status == MD_PROVENANCE_PUBLIC_HKO)) {
  stop("Weather design provenance must be REAL_PUBLIC_HKO")
}
weather$date <- as.Date(weather$date)

# Allowed constrained exposure models from registry
registry <- if (exists("load_final_model_registry", mode = "function")) {
  load_final_model_registry(root = root)
} else if (requireNamespace("yaml", quietly = TRUE)) {
  yaml::read_yaml(file.path(root, "analysis_plan", "final_model_registry.yml"))
} else {
  stop("yaml required")
}
allowed <- unlist(registry$md_feasibility$allowed_exposure_models)
hess_max <- registry$md_feasibility$admission_gates$hessian_condition_max %||%
  MD_HESSIAN_CONDITION_MAX

exposure_map <- list(
  daily_hot_night_same_day = list(col = "hot_night_same_day", outcome = "chd"),
  daily_cold_day_same_day = list(col = "cold_day_same_day", outcome = "hf"),
  constrained_hot_night_lag_0_5 = list(col = "hot_night_lag_0_5", outcome = "chd"),
  constrained_cold_day_lag_0_21 = list(col = "cold_day_lag_0_21", outcome = "hf")
)

estimate_rows <- list()
status_rows <- list()

for (model_key in allowed) {
  spec <- exposure_map[[model_key]]
  if (is.null(spec)) {
    status_rows[[model_key]] <- data.frame(
      model_key = model_key,
      status = "skipped_unknown_model",
      message = "No exposure map for allowed model key",
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      stringsAsFactors = FALSE
    )
    next
  }
  outcome <- spec$outcome
  dat <- panels[[outcome]]
  # Monthly counts: prefer count / events / y columns
  count_col <- intersect(
    c("events", "count", "y", "n_events", paste0(outcome, "_events")),
    names(dat)
  )
  month_col <- intersect(c("month_id", "ym", "year_month"), names(dat))
  if (!length(count_col) || !length(month_col)) {
    status_rows[[model_key]] <- data.frame(
      model_key = model_key,
      outcome = outcome,
      status = "failed_panel_schema",
      message = "Panel lacks month_id/events columns",
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      stringsAsFactors = FALSE
    )
    next
  }
  S <- setNames(as.numeric(dat[[count_col[[1]]]]), as.character(dat[[month_col[[1]]]]))
  if (!spec$col %in% names(weather)) {
    status_rows[[model_key]] <- data.frame(
      model_key = model_key,
      outcome = outcome,
      status = "failed_missing_exposure",
      message = paste("Weather design missing", spec$col),
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      stringsAsFactors = FALSE
    )
    next
  }

  X <- tryCatch(
    md_build_daily_design(
      dates = weather$date,
      exposure = weather[[spec$col]],
      covid_phase = weather$covid_phase,
      include_covid = TRUE,
      exposure_name = "exposure"
    ),
    error = function(e) e
  )
  if (inherits(X, "error")) {
    status_rows[[model_key]] <- data.frame(
      model_key = model_key,
      outcome = outcome,
      status = "failed_design",
      message = conditionMessage(X),
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      stringsAsFactors = FALSE
    )
    next
  }

  fit <- tryCatch(
    md_fit(S = S, X = X, month_id = weather$month_id, offset = rep(1, nrow(weather))),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    status_rows[[model_key]] <- data.frame(
      model_key = model_key,
      outcome = outcome,
      status = "failed_fit_error",
      message = conditionMessage(fit),
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      stringsAsFactors = FALSE
    )
    next
  }

  admissible <- md_real_fit_admissible(fit, hessian_condition_max = hess_max)
  status_rows[[model_key]] <- data.frame(
    model_key = model_key,
    outcome = outcome,
    status = if (admissible) fit$status else "rejected_hessian_or_convergence_gate",
    message = if (admissible) {
      fit$message
    } else {
      paste0(
        "Fit not admitted for estimate emission: converged=",
        isTRUE(fit$converged),
        "; hessian_pd=", isTRUE(fit$hessian_pd),
        "; hessian_condition=", fit$hessian_condition %||% NA_real_,
        " (max ", hess_max, "). Underlying: ", fit$message %||% fit$status
      )
    },
    converged = isTRUE(fit$converged),
    hessian_pd = isTRUE(fit$hessian_pd),
    hessian_condition = fit$hessian_condition %||% NA_real_,
    admissible_for_estimate = admissible,
    p = fit$p %||% NA_integer_,
    method_used = fit$method_used %||% NA_character_,
    result_class = RESULT_EXPLORATORY,
    data_status = MD_PROVENANCE_REAL,
    stringsAsFactors = FALSE
  )

  if (isTRUE(admissible)) {
    ci <- md_exposure_ci(fit, "exposure", use_quasi = TRUE, contrast = 1)
    estimate_rows[[model_key]] <- data.frame(
      model_id = registry$md_feasibility$method_id %||% "M07_MONTHLY_OUTCOME_DAILY_EXPOSURE",
      model_key = model_key,
      outcome = outcome,
      exposure = spec$col,
      estimate = ci$estimate,
      se = ci$se,
      conf_low = ci$conf_low,
      conf_high = ci$conf_high,
      rr = ci$rr,
      rr_low = ci$rr_low,
      rr_high = ci$rr_high,
      dispersion = fit$dispersion,
      hessian_condition = fit$hessian_condition,
      result_class = RESULT_EXPLORATORY,
      data_status = MD_PROVENANCE_REAL,
      claim_tier = "exploratory",
      stringsAsFactors = FALSE
    )
  }
}

status_df <- do.call(rbind, status_rows)
write_csv_safe(status_df, file.path(out_dir, "md_constrained_fit_status.csv"))
if (length(estimate_rows)) {
  est_df <- do.call(rbind, estimate_rows)
  write_csv_safe(est_df, file.path(out_dir, "md_constrained_estimates.csv"))
} else {
  message("No admissible real M|D estimates to write.")
}

message("41_fit_md_constrained complete. result_class=", RESULT_EXPLORATORY)
