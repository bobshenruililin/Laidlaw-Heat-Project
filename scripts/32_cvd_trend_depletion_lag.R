#!/usr/bin/env Rscript
# 32_cvd_trend_depletion_lag.R
# Trend, first-event depletion, lag, influence and count-time-series sensitivities.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "MASS", "splines", "sandwich", "tscount"))

outcomes <- c("chd", "hf")
specs <- list(
  P01A = list(exposure = "mean_temp", scale = 1),
  P02A = list(exposure = "mean_tmax", scale = 1),
  P02B = list(exposure = "mean_tmin", scale = 1),
  P04A = list(exposure = "hot_nights", scale = 5),
  P04B = list(exposure = "cold_days", scale = 5),
  P04C = list(exposure = "very_hot_days", scale = 5)
)

term_for <- function(exposure, scale) {
  # Coefficient names from glm omit spaces inside I().
  if (scale == 1) exposure else sprintf("I(%s/%s)", exposure, scale)
}

fit_nb_nw <- function(dat, term, controls, offset = "offset(offset_log_days)") {
  rhs <- c(term, controls, offset)
  fml <- stats::as.formula(paste("n_events ~", paste(rhs, collapse = " + ")))
  model <- MASS::glm.nb(fml, data = dat)
  vm <- sandwich::NeweyWest(model, lag = 6, prewhite = FALSE, adjust = TRUE)
  if (!term %in% names(stats::coef(model))) stop("Term not found: ", term)
  b <- unname(stats::coef(model)[term])
  se <- unname(sqrt(diag(vm))[term])
  res <- stats::residuals(model, type = "pearson")
  list(
    model = model,
    row = data.frame(
      term = term,
      estimate = b,
      std_error_nw6 = se,
      p_value_nw6 = 2 * stats::pnorm(abs(b / se), lower.tail = FALSE),
      rr = exp(b),
      rr_low = exp(b - 1.96 * se),
      rr_high = exp(b + 1.96 * se),
      n_months = nrow(dat),
      residual_acf1 = if (length(res) > 1) {
        as.numeric(stats::acf(res, plot = FALSE, lag.max = 1)$acf[2])
      } else {
        NA_real_
      },
      stringsAsFactors = FALSE
    )
  )
}

trend_rows <- list()
lag_rows <- list()
influence_rows <- list()
ts_rows <- list()

for (outcome in outcomes) {
  panel_path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  dat <- utils::read.csv(panel_path, stringsAsFactors = FALSE) |>
    dplyr::arrange(time_index) |>
    dplyr::mutate(
      month_f = factor(month),
      year_f = factor(year),
      covid_phase_f = factor(covid_phase)
    )
  if (!identical(unique(as.character(dat$data_status)), "HA_APPROVED_AGGREGATE") ||
      nrow(dat) != 132L) {
    stop("Trend/depletion sensitivity requires real 132-month panel for ", outcome)
  }

  for (pid in names(specs)) {
    spec <- specs[[pid]]
    term <- term_for(spec$exposure, spec$scale)

    scenarios <- list(
      baseline_ns4 = list(
        data = dat,
        controls = c("month_f", "splines::ns(time_index, df = 4)")
      ),
      trend_ns3 = list(
        data = dat,
        controls = c("month_f", "splines::ns(time_index, df = 3)")
      ),
      trend_ns6 = list(
        data = dat,
        controls = c("month_f", "splines::ns(time_index, df = 6)")
      ),
      trend_ns8 = list(
        data = dat,
        controls = c("month_f", "splines::ns(time_index, df = 8)")
      ),
      year_fixed_effects = list(
        data = dat,
        controls = c("month_f", "year_f")
      ),
      drop_first_12_months = list(
        data = dplyr::filter(dat, time_index > 12),
        controls = c("month_f", "splines::ns(time_index, df = 4)")
      ),
      drop_first_24_months = list(
        data = dplyr::filter(dat, time_index > 24),
        controls = c("month_f", "splines::ns(time_index, df = 4)")
      ),
      pre_covid = list(
        data = dplyr::filter(dat, year < 2020),
        controls = c("month_f", "splines::ns(time_index, df = 4)")
      ),
      covid_phase_adjusted = list(
        data = dat,
        controls = c("month_f", "splines::ns(time_index, df = 4)", "covid_phase_f")
      )
    )

    baseline_fit <- NULL
    for (scenario_name in names(scenarios)) {
      item <- scenarios[[scenario_name]]
      result <- tryCatch(
        fit_nb_nw(item$data, term, item$controls),
        error = function(e) NULL
      )
      if (is.null(result)) next
      if (identical(scenario_name, "baseline_ns4")) baseline_fit <- result$model
      row <- result$row
      row$outcome <- outcome
      row$pathway_id <- pid
      row$exposure <- spec$exposure
      row$scale <- spec$scale
      row$scenario <- scenario_name
      row$data_status <- "HA_APPROVED_AGGREGATE"
      trend_rows[[paste(outcome, pid, scenario_name, sep = "_")]] <- row
    }

    if (!is.null(baseline_fit)) {
      cooks <- stats::cooks.distance(baseline_fit)
      max_idx <- which.max(cooks)
      reduced <- dat[-max_idx, , drop = FALSE]
      influence_fit <- fit_nb_nw(
        reduced,
        term,
        c("month_f", "splines::ns(time_index, df = 4)")
      )
      row <- influence_fit$row
      row$outcome <- outcome
      row$pathway_id <- pid
      row$exposure <- spec$exposure
      row$scale <- spec$scale
      row$scenario <- "exclude_max_cooks_month"
      row$excluded_month <- dat$month_id[max_idx]
      row$max_cooks_distance <- max(cooks)
      row$data_status <- "HA_APPROVED_AGGREGATE"
      influence_rows[[paste(outcome, pid, sep = "_")]] <- row
    }

    # Separate lag-0/1/2 models. Each lag is an alternative monthly estimand.
    for (lag_n in 0:2) {
      lag_var <- paste0(spec$exposure, "_analysis_lag", lag_n)
      dat[[lag_var]] <- dplyr::lag(dat[[spec$exposure]], lag_n)
      lag_dat <- dplyr::filter(dat, !is.na(.data[[lag_var]]))
      lag_term <- term_for(lag_var, spec$scale)
      result <- tryCatch(
        fit_nb_nw(
          lag_dat,
          lag_term,
          c("month_f", "splines::ns(time_index, df = 4)")
        ),
        error = function(e) NULL
      )
      if (is.null(result)) next
      row <- result$row
      row$outcome <- outcome
      row$pathway_id <- pid
      row$exposure <- spec$exposure
      row$scale <- spec$scale
      row$lag_months <- lag_n
      row$data_status <- "HA_APPROVED_AGGREGATE"
      lag_rows[[paste(outcome, pid, lag_n, sep = "_")]] <- row
    }

    # Negative-binomial INGARCH(1,1) sensitivity for residual dependence.
    # tsglm has no fixed offset argument; this is an unoffset count-series sensitivity.
    xreg <- stats::model.matrix(
      stats::as.formula(
        paste0(
          "~ 0 + I(", spec$exposure, " / ", spec$scale,
          ") + month_f + splines::ns(time_index, df = 4)"
        )
      ),
      data = dat
    )
    exposure_col <- colnames(xreg)[1]
    tsfit <- tryCatch(
      tscount::tsglm(
        ts = dat$n_events,
        model = list(
          past_obs = 1,
          past_mean = 1,
          external = rep(TRUE, ncol(xreg))
        ),
        xreg = xreg,
        link = "log",
        distr = "nbinom",
        init.method = "marginal"
      ),
      error = function(e) NULL
    )
    if (!is.null(tsfit) && exposure_col %in% names(stats::coef(tsfit))) {
      b <- unname(stats::coef(tsfit)[exposure_col])
      covariance <- tryCatch(solve(tsfit$info.matrix_corrected), error = function(e) NULL)
      se <- if (is.null(covariance)) NA_real_ else {
        sqrt(diag(covariance))[exposure_col]
      }
      res <- stats::residuals(tsfit)
      ts_rows[[paste(outcome, pid, sep = "_")]] <- data.frame(
        outcome = outcome,
        pathway_id = pid,
        exposure = spec$exposure,
        scale = spec$scale,
        model = "negative_binomial_INGARCH_1_1",
        offset_policy = "none_count_series_sensitivity",
        term = exposure_col,
        estimate = b,
        std_error = unname(se),
        rr = exp(b),
        rr_low = if (is.finite(se)) exp(b - 1.96 * se) else NA_real_,
        rr_high = if (is.finite(se)) exp(b + 1.96 * se) else NA_real_,
        residual_acf1 = if (length(res) > 1) {
          as.numeric(stats::acf(res, plot = FALSE, lag.max = 1)$acf[2])
        } else {
          NA_real_
        },
        n_months = nrow(dat),
        data_status = "HA_APPROVED_AGGREGATE",
        stringsAsFactors = FALSE
      )
    }
  }
}

trend_df <- dplyr::bind_rows(trend_rows)
lag_df <- dplyr::bind_rows(lag_rows)
influence_df <- dplyr::bind_rows(influence_rows)
ts_df <- dplyr::bind_rows(ts_rows)

out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
write_csv_safe(trend_df, file.path(out_dir, "cvd_trend_depletion_sensitivity.csv"))
write_csv_safe(lag_df, file.path(out_dir, "cvd_lag_sensitivity.csv"))
write_csv_safe(influence_df, file.path(out_dir, "cvd_influence_sensitivity.csv"))
write_csv_safe(ts_df, file.path(out_dir, "cvd_count_timeseries_sensitivity.csv"))

message(
  "Trend/depletion/lag sensitivity complete: ",
  nrow(trend_df), " trend rows; ",
  nrow(lag_df), " lag rows; ",
  nrow(ts_df), " INGARCH rows"
)
