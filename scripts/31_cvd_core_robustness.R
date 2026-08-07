#!/usr/bin/env Rscript
# 31_cvd_core_robustness.R
# Amended single-exposure CHD/HF models with alternative offsets and robust SEs.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "MASS", "splines", "sandwich", "lmtest"))

outcomes <- c("chd", "hf")
core_specs <- list(
  P01A = list(exposure = "mean_temp", scale = 1, label = "Mean temperature (per 1 C)"),
  P02A = list(exposure = "mean_tmax", scale = 1, label = "Mean maximum temperature (per 1 C)"),
  P02B = list(exposure = "mean_tmin", scale = 1, label = "Mean minimum temperature (per 1 C)"),
  P04A = list(exposure = "hot_nights", scale = 5, label = "Hot nights (per 5 days)"),
  P04B = list(exposure = "cold_days", scale = 5, label = "Cold days (per 5 days)"),
  P04C = list(exposure = "very_hot_days", scale = 5, label = "Very hot days (per 5 days)")
)
offsets <- list(
  days_only = "offset(offset_log_days)",
  population_x_days = "offset(offset_log)",
  none = NULL
)
families <- c("negative_binomial", "quasipoisson")
se_methods <- c("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")

fit_count_model <- function(formula, data, family_name) {
  if (identical(family_name, "negative_binomial")) {
    return(MASS::glm.nb(formula, data = data))
  }
  stats::glm(formula, data = data, family = stats::quasipoisson())
}

vcov_for <- function(model, method) {
  if (identical(method, "model")) return(stats::vcov(model))
  if (identical(method, "HC1")) {
    return(sandwich::vcovHC(model, type = "HC1"))
  }
  lag <- if (identical(method, "NeweyWest_lag3")) 3L else 6L
  sandwich::NeweyWest(model, lag = lag, prewhite = FALSE, adjust = TRUE)
}

extract_term <- function(model, term, vcov_mat, metadata) {
  if (!term %in% names(stats::coef(model))) return(NULL)
  b <- unname(stats::coef(model)[term])
  se <- sqrt(diag(vcov_mat))[term]
  if (!is.finite(se)) return(NULL)
  z <- b / se
  dplyr::bind_cols(
    metadata,
    data.frame(
      term = term,
      estimate = b,
      std_error = unname(se),
      statistic = unname(z),
      p_value = 2 * stats::pnorm(abs(z), lower.tail = FALSE),
      rr = exp(b),
      rr_low = exp(b - 1.96 * se),
      rr_high = exp(b + 1.96 * se),
      stringsAsFactors = FALSE
    )
  )
}

build_formula <- function(terms, offset_rhs = NULL, trend_df = 4L) {
  rhs <- c(
    terms,
    "month_f",
    paste0("splines::ns(time_index, df = ", trend_df, ")"),
    offset_rhs
  )
  stats::as.formula(paste("n_events ~", paste(rhs[!is.na(rhs) & nzchar(rhs)], collapse = " + ")))
}

scalar_or_na <- function(x, default = NA_real_) {
  if (is.null(x) || length(x) == 0 || all(is.na(x))) return(default)
  x[[1]]
}

residual_metrics <- function(model) {
  res <- stats::residuals(model, type = "pearson")
  acf1 <- if (length(res) > 1) as.numeric(stats::acf(res, plot = FALSE, lag.max = 1)$acf[2]) else NA_real_
  data.frame(
    aic = scalar_or_na(tryCatch(stats::AIC(model), error = function(e) NA_real_)),
    theta = scalar_or_na(tryCatch(model$theta, error = function(e) NA_real_)),
    dispersion = sum(res^2, na.rm = TRUE) / max(stats::df.residual(model), 1),
    residual_acf1 = acf1,
    ljung_box_p_lag6 = if (length(res) > 6) {
      stats::Box.test(res, lag = 6, type = "Ljung-Box")$p.value
    } else {
      NA_real_
    },
    converged = scalar_or_na(
      tryCatch(model$converged, error = function(e) NA),
      default = NA
    ),
    stringsAsFactors = FALSE
  )
}

estimate_rows <- list()
fit_rows <- list()
joint_rows <- list()
cor_rows <- list()
vif_rows <- list()

for (outcome in outcomes) {
  panel_path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  if (!file.exists(panel_path)) stop("Missing real panel: ", panel_path)
  dat <- utils::read.csv(panel_path, stringsAsFactors = FALSE) |>
    dplyr::arrange(time_index) |>
    dplyr::mutate(month_f = factor(month))
  statuses <- unique(as.character(dat$data_status))
  if (!identical(statuses, "HA_APPROVED_AGGREGATE") || nrow(dat) != 132L) {
    stop("Core robustness requires a 132-month HA_APPROVED_AGGREGATE panel for ", outcome)
  }

  for (pid in names(core_specs)) {
    spec <- core_specs[[pid]]
    # Coefficient names from glm omit spaces inside I().
    term <- if (spec$scale == 1) {
      spec$exposure
    } else {
      sprintf("I(%s/%s)", spec$exposure, spec$scale)
    }

    for (offset_name in names(offsets)) {
      for (family_name in families) {
        fml <- build_formula(term, offsets[[offset_name]])
        model <- tryCatch(
          fit_count_model(fml, dat, family_name),
          error = function(e) {
            warning(outcome, " ", pid, " ", offset_name, " ", family_name, ": ", conditionMessage(e))
            NULL
          }
        )
        if (is.null(model)) next

        fit_meta <- data.frame(
          outcome = outcome,
          pathway_id = pid,
          exposure = spec$exposure,
          exposure_label = spec$label,
          scale = spec$scale,
          model_structure = "single_exposure",
          family = family_name,
          offset_policy = offset_name,
          n_months = nrow(dat),
          data_status = "HA_APPROVED_AGGREGATE",
          stringsAsFactors = FALSE
        )
        fit_rows[[paste(outcome, pid, offset_name, family_name, sep = "_")]] <-
          dplyr::bind_cols(fit_meta, residual_metrics(model))

        for (se_method in se_methods) {
          vm <- tryCatch(vcov_for(model, se_method), error = function(e) NULL)
          if (is.null(vm)) next
          meta <- fit_meta
          meta$se_method <- se_method
          row <- extract_term(model, term, vm, meta)
          if (!is.null(row)) {
            estimate_rows[[paste(outcome, pid, offset_name, family_name, se_method, sep = "_")]] <- row
          }
        }
      }
    }
  }

  # Original joint structures, retained for collinearity comparison only.
  joint_specs <- list(
    P02 = c("mean_tmax", "mean_tmin"),
    P04 = c("I(hot_nights/5)", "I(cold_days/5)", "I(very_hot_days/5)")
  )
  for (pid in names(joint_specs)) {
    fml <- build_formula(joint_specs[[pid]], offsets$days_only)
    model <- MASS::glm.nb(fml, data = dat)
    for (se_method in c("HC1", "NeweyWest_lag6")) {
      vm <- vcov_for(model, se_method)
      for (term in joint_specs[[pid]]) {
        meta <- data.frame(
          outcome = outcome,
          pathway_id = pid,
          exposure = term,
          exposure_label = term,
          scale = if (grepl("/5", term, fixed = TRUE)) 5 else 1,
          model_structure = "joint_exploratory",
          family = "negative_binomial",
          offset_policy = "days_only",
          n_months = nrow(dat),
          data_status = "HA_APPROVED_AGGREGATE",
          se_method = se_method,
          stringsAsFactors = FALSE
        )
        row <- extract_term(model, term, vm, meta)
        if (!is.null(row)) {
          joint_rows[[paste(outcome, pid, term, se_method, sep = "_")]] <- row
        }
      }
    }
  }

  # Raw and season/trend-residualised exposure correlation matrices.
  exposure_names <- vapply(core_specs, `[[`, character(1), "exposure")
  raw_cor <- stats::cor(dat[, exposure_names], use = "pairwise.complete.obs")
  residualised <- lapply(exposure_names, function(exposure) {
    stats::residuals(stats::lm(
      stats::as.formula(
        paste0(exposure, " ~ month_f + splines::ns(time_index, df = 4)")
      ),
      data = dat
    ))
  })
  names(residualised) <- exposure_names
  resid_cor <- stats::cor(as.data.frame(residualised), use = "pairwise.complete.obs")

  matrix_to_long <- function(mat, type) {
    grid <- expand.grid(
      exposure_1 = rownames(mat),
      exposure_2 = colnames(mat),
      stringsAsFactors = FALSE
    )
    grid$correlation <- as.vector(mat)
    grid$correlation_type <- type
    grid$outcome <- outcome
    grid
  }
  cor_rows[[paste0(outcome, "_raw")]] <- matrix_to_long(raw_cor, "raw")
  cor_rows[[paste0(outcome, "_residualised")]] <- matrix_to_long(resid_cor, "month_and_trend_residualised")

  for (group_name in c("P02_joint", "P04_joint")) {
    vars <- if (identical(group_name, "P02_joint")) {
      c("mean_tmax", "mean_tmin")
    } else {
      c("hot_nights", "cold_days", "very_hot_days")
    }
    r <- resid_cor[vars, vars, drop = FALSE]
    vifs <- tryCatch(diag(solve(r)), error = function(e) rep(NA_real_, length(vars)))
    vif_rows[[paste(outcome, group_name, sep = "_")]] <- data.frame(
      outcome = outcome,
      exposure_group = group_name,
      exposure = vars,
      vif_after_month_and_trend = as.numeric(vifs),
      stringsAsFactors = FALSE
    )
  }
}

est_df <- dplyr::bind_rows(estimate_rows)
joint_df <- dplyr::bind_rows(joint_rows)
fit_df <- dplyr::bind_rows(fit_rows)
cor_df <- dplyr::bind_rows(cor_rows)
vif_df <- dplyr::bind_rows(vif_rows)

main_idx <- est_df$family == "negative_binomial" &
  est_df$offset_policy == "days_only" &
  est_df$se_method == "NeweyWest_lag6"
est_df$q_value_core_bh <- NA_real_
est_df$q_value_core_bh[main_idx] <- stats::p.adjust(est_df$p_value[main_idx], method = "BH")
est_df$manuscript_role <- ifelse(main_idx, "amended_core_candidate", "sensitivity")
joint_df$manuscript_role <- "joint_collinearity_sensitivity"

out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
write_csv_safe(est_df, file.path(out_dir, "cvd_core_robust_estimates.csv"))
write_csv_safe(joint_df, file.path(out_dir, "cvd_single_vs_joint_estimates.csv"))
write_csv_safe(fit_df, file.path(out_dir, "cvd_core_model_fit.csv"))
write_csv_safe(cor_df, file.path(out_dir, "cvd_exposure_correlations.csv"))
write_csv_safe(vif_df, file.path(out_dir, "cvd_exposure_vif.csv"))

message(
  "Core robustness complete: ", nrow(est_df), " single-exposure estimates; ",
  nrow(joint_df), " joint comparisons"
)
