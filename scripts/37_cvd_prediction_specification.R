#!/usr/bin/env Rscript
# 37_cvd_prediction_specification.R
# Real-only prediction (LOYO + rolling origin), specification curve, and
# serial-null max-statistic runner. Frozen pairs: CHD/P04A, HF/P04B.
# SPEC_BOOT_REPS defaults to 200 (lower in tests).

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "final_model_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "yaml", "MASS", "splines", "sandwich", "lmtest"))

registry <- load_final_model_registry(root = root)
specs <- core_exposure_specs(registry)
scenarios <- scenario_defs(registry)
outcomes <- registry$outcomes %||% c("chd", "hf")

boot_reps <- suppressWarnings(as.integer(Sys.getenv("SPEC_BOOT_REPS", unset = "200")))
if (!is.finite(boot_reps) || boot_reps < 1L) boot_reps <- 200L

out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

panel_paths <- setNames(
  file.path(root, "data_processed", paste0(outcomes, "_analysis_panel.csv")),
  outcomes
)
if (any(!file.exists(panel_paths))) {
  blocker <- missing_governed_panel_blocker(
    outcomes = outcomes,
    root = root,
    script_id = "37_cvd_prediction_specification"
  )
  handle_missing_governed_panels(
    blocker,
    file.path(out_dir, "cvd_prediction_spec_blocker.csv")
  )
}

panels <- lapply(outcomes, function(outcome) {
  dat <- utils::read.csv(panel_paths[[outcome]], stringsAsFactors = FALSE)
  prepare_analysis_panel(dat, require_real = TRUE, outcome = outcome)
})
names(panels) <- outcomes

# ---- Frozen prediction pairs -------------------------------------------------
pred_pairs <- registry$prediction$frozen_pairs
pred_controls <- control_terms_from_registry(
  registry$prediction$models$baseline %||% c("calendar_month_factor", "ns_time_df4")
)

pred_scores <- list()
pred_status <- list()
for (outcome in names(pred_pairs)) {
  pid <- pred_pairs[[outcome]]
  if (!outcome %in% names(panels)) next
  if (!pid %in% names(specs)) {
    pred_status[[paste(outcome, "missing_spec", sep = "::")]] <- status_row(
      "FAILED", paste0("Frozen pathway ", pid, " not in registry"),
      outcome = outcome, pathway_id = pid
    )
    next
  }
  spec <- specs[[pid]]
  dat <- panels[[outcome]]
  term <- exposure_term_name(spec$variable, spec$contrast)
  meta <- list(
    outcome = outcome,
    pathway_id = pid,
    exposure = spec$variable,
    contrast = spec$contrast,
    model_id = "PRED_BASELINE_VS_EXPOSURE",
    result_class = RESULT_CLASS_EXPLORATORY,
    data_status = REAL_PROVENANCE
  )
  loyo <- score_loyo_nb(dat, term, pred_controls, "days_only", metadata = meta)
  roll <- score_rolling_origin_nb(
    dat, term, pred_controls, "days_only",
    horizon = 12L, min_train = 60L, metadata = meta
  )
  if (!is.null(loyo$scores)) pred_scores[[paste(outcome, "loyo", sep = "::")]] <- loyo$scores
  if (!is.null(roll$scores)) pred_scores[[paste(outcome, "roll", sep = "::")]] <- roll$scores
  pred_status[[paste(outcome, "loyo", sep = "::")]] <- {
    st <- loyo$status
    st$outcome <- outcome
    st$pathway_id <- pid
    st$result_class <- RESULT_CLASS_EXPLORATORY
    st$data_status <- REAL_PROVENANCE
    st
  }
  pred_status[[paste(outcome, "roll", sep = "::")]] <- {
    st <- roll$status
    st$outcome <- outcome
    st$pathway_id <- pid
    st$result_class <- RESULT_CLASS_EXPLORATORY
    st$data_status <- REAL_PROVENANCE
    st
  }
}

# ---- Specification curve (registry axes) ------------------------------------
spec_curve_cfg <- registry$specification_curve
curve_scenarios <- spec_curve_cfg$scenarios
curve_exposures <- spec_curve_cfg$exposures
curve_outcomes <- spec_curve_cfg$outcomes
curve_offsets <- spec_curve_cfg$offsets %||% c("days_only")

spec_estimates <- list()
spec_status <- list()

fit_spec_universe <- function(panel_list) {
  est <- list()
  st <- list()
  for (outcome in curve_outcomes) {
    dat <- panel_list[[outcome]]
    for (pid in curve_exposures) {
      spec <- specs[[pid]]
      for (sid in curve_scenarios) {
        scenario <- scenarios[[sid]]
        for (off in curve_offsets) {
          key <- paste(outcome, pid, sid, off, sep = "::")
          fit <- fit_scenario_nb(
            dat = dat,
            pathway_id = pid,
            exposure_spec = spec,
            scenario = scenario,
            registry = registry,
            offset_policy = off,
            model_id = "SPEC_CURVE_NB",
            result_class = RESULT_CLASS_EXPLORATORY,
            data_status = REAL_PROVENANCE
          )
          st[[key]] <- fit$status
          if (!is.null(fit$estimates)) {
            # Continuity SE for the curve: NeweyWest_lag6 when present, else model.
            keep <- fit$estimates
            if ("NeweyWest_lag6" %in% keep$se_method) {
              keep <- keep[keep$se_method == "NeweyWest_lag6", , drop = FALSE]
            } else if ("model" %in% keep$se_method) {
              keep <- keep[keep$se_method == "model", , drop = FALSE]
            }
            est[[key]] <- keep
          }
        }
      }
    }
  }
  list(
    estimates = if (length(est)) dplyr::bind_rows(est) else NULL,
    status = dplyr::bind_rows(st)
  )
}

observed_curve <- fit_spec_universe(panels)
if (!is.null(observed_curve$estimates)) {
  spec_estimates[["observed"]] <- observed_curve$estimates
}
spec_status[["observed"]] <- observed_curve$status

# Summaries: median, IQR, sign stability (no nominal significance counts).
summarise_spec_curve <- function(est) {
  if (is.null(est) || !nrow(est)) {
    return(data.frame(stringsAsFactors = FALSE))
  }
  est |>
    dplyr::group_by(outcome, pathway_id, exposure) |>
    dplyr::summarise(
      n_specs = dplyr::n(),
      median_estimate = stats::median(estimate, na.rm = TRUE),
      iqr_estimate = stats::IQR(estimate, na.rm = TRUE),
      median_rr = stats::median(rr, na.rm = TRUE),
      sign_stability = mean(sign(estimate) == sign(stats::median(estimate, na.rm = TRUE)), na.rm = TRUE),
      max_abs_statistic = max(abs(statistic), na.rm = TRUE),
      .groups = "drop"
    ) |>
    as.data.frame(stringsAsFactors = FALSE)
}

spec_summary <- summarise_spec_curve(observed_curve$estimates)
if (nrow(spec_summary)) {
  spec_summary$result_class <- RESULT_CLASS_EXPLORATORY
  spec_summary$data_status <- REAL_PROVENANCE
}

observed_max_stat <- max_abs_stat_from_estimates(observed_curve$estimates)

# ---- Serial-null max-stat calibration ---------------------------------------
# Circular-block Pearson-residual null under each outcome's baseline
# season/trend mean. This preserves short-range dependence before refitting
# the registry specification axes and taking max |z|.
null_max <- rep(NA_real_, boot_reps)
null_status <- vector("list", boot_reps)

# Pre-fit baseline mu/theta per outcome
base_mu <- lapply(panels, function(d) {
  fit_baseline_nb_mu_theta(
    d,
    control_terms_from_registry(c("calendar_month_factor", "ns_time_df4")),
    "days_only"
  )
})

set.seed(20260810)
for (j in seq_len(boot_reps)) {
  panel_j <- list()
  for (outcome in outcomes) {
    d <- panels[[outcome]]
    d$n_events <- as.numeric(
      simulate_block_residual_null(
        d$n_events,
        base_mu[[outcome]]$mu,
        base_mu[[outcome]]$theta,
        n_reps = 1L,
        block_length = 6L,
        seed = 20260810L + j * 100L + match(outcome, outcomes)
      )[, 1]
    )
    d$data_status <- SYNTHETIC_PROVENANCE
    panel_j[[outcome]] <- d
  }

  # Null curve uses days_only and the registry scenario list (same family).
  est_j <- list()
  failed <- FALSE
  fail_msg <- ""
  for (outcome in curve_outcomes) {
    dat <- panel_j[[outcome]]
    for (pid in curve_exposures) {
      spec <- specs[[pid]]
      for (sid in curve_scenarios) {
        scenario <- scenarios[[sid]]
        for (off in curve_offsets) {
          fit <- fit_scenario_nb(
            dat = dat,
            pathway_id = pid,
            exposure_spec = spec,
            scenario = scenario,
            registry = registry,
            offset_policy = off,
            model_id = "SPEC_CURVE_NULL",
            result_class = "NULL_CALIBRATION",
            data_status = SYNTHETIC_PROVENANCE
          )
          if (!is.null(fit$estimates)) {
            keep <- fit$estimates
            if ("NeweyWest_lag6" %in% keep$se_method) {
              keep <- keep[keep$se_method == "NeweyWest_lag6", , drop = FALSE]
            } else if ("model" %in% keep$se_method) {
              keep <- keep[keep$se_method == "model", , drop = FALSE]
            }
            est_j[[paste(outcome, pid, sid, off, sep = "::")]] <- keep
          } else if (!identical(fit$status$status, "SKIPPED")) {
            fail_msg <- paste(fail_msg, fit$status$message, sep = " | ")
          }
        }
      }
    }
  }
  est_df_j <- if (length(est_j)) dplyr::bind_rows(est_j) else NULL
  null_max[[j]] <- max_abs_stat_from_estimates(est_df_j)
  null_status[[j]] <- status_row(
    if (is.finite(null_max[[j]])) "OK" else "FAILED",
    if (is.finite(null_max[[j]])) "" else paste0("Non-finite max stat", fail_msg),
    rep = j,
    result_class = "NULL_CALIBRATION",
    data_status = SYNTHETIC_PROVENANCE
  )
}

null_ok <- null_max[is.finite(null_max)]
simultaneous_p <- if (length(null_ok) && is.finite(observed_max_stat)) {
  mean(null_ok >= observed_max_stat)
} else {
  NA_real_
}
q975 <- if (length(null_ok)) as.numeric(stats::quantile(null_ok, 0.975, names = FALSE)) else NA_real_

null_summary <- data.frame(
  observed_max_abs_statistic = observed_max_stat,
  null_reps_requested = boot_reps,
  null_reps_ok = length(null_ok),
  null_max_mean = if (length(null_ok)) mean(null_ok) else NA_real_,
  null_max_q975 = q975,
  simultaneous_p_ge_observed = simultaneous_p,
  method = "circular_block_residual_null_length6",
  result_class = "NULL_CALIBRATION",
  data_status = SYNTHETIC_PROVENANCE,
  source_data_status = REAL_PROVENANCE,
  stringsAsFactors = FALSE
)

# ---- Write artifacts ---------------------------------------------------------
pred_score_df <- if (length(pred_scores)) dplyr::bind_rows(pred_scores) else {
  data.frame(stringsAsFactors = FALSE)
}
pred_status_df <- if (length(pred_status)) dplyr::bind_rows(pred_status) else {
  data.frame(stringsAsFactors = FALSE)
}
spec_est_df <- if (!is.null(observed_curve$estimates)) observed_curve$estimates else {
  data.frame(stringsAsFactors = FALSE)
}
spec_status_df <- observed_curve$status
null_status_df <- dplyr::bind_rows(null_status)
null_draws_df <- data.frame(
  rep = seq_len(boot_reps),
  max_abs_statistic = null_max,
  result_class = "NULL_CALIBRATION",
  data_status = SYNTHETIC_PROVENANCE,
  stringsAsFactors = FALSE
)

write_csv_safe(pred_score_df, file.path(out_dir, "cvd_prediction_scores.csv"))
write_csv_safe(pred_status_df, file.path(out_dir, "cvd_prediction_fit_status.csv"))
write_csv_safe(spec_est_df, file.path(out_dir, "cvd_specification_curve_estimates.csv"))
write_csv_safe(spec_status_df, file.path(out_dir, "cvd_specification_curve_fit_status.csv"))
write_csv_safe(spec_summary, file.path(out_dir, "cvd_specification_curve_summary.csv"))
write_csv_safe(null_summary, file.path(out_dir, "cvd_specification_null_maxstat_summary.csv"))
write_csv_safe(null_draws_df, file.path(out_dir, "cvd_specification_null_maxstat_draws.csv"))
write_csv_safe(null_status_df, file.path(out_dir, "cvd_specification_null_fit_status.csv"))

message(
  "Prediction/specification complete: pred rows=", nrow(pred_score_df),
  "; spec rows=", nrow(spec_est_df),
  "; null reps=", boot_reps,
  "; observed max|z|=", observed_max_stat
)
