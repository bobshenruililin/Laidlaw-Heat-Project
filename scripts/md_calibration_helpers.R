# md_calibration_helpers.R
# Synthetic calibration DGP, scenarios, estimator wrappers, and metrics for M|D.
#
# Provenance of every simulated artifact: SYNTHETIC_CALIBRATION.
# Uses committed disclosure summaries only (annual / seasonal / COVID-era means).
# Does NOT reconstruct real monthly outcome counts.
# Do not run directly.

if (!exists("MD_PROVENANCE_SYNTHETIC", inherits = TRUE)) {
  MD_PROVENANCE_SYNTHETIC <- "SYNTHETIC_CALIBRATION"
}
if (!exists("%||%", mode = "function")) {
  `%||%` <- function(x, y) {
    if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
  }
}

MD_MASTER_SEED <- 20260810L

# Effect targets from protocol brief:
# null; RR 1.02 per 5 affected days; RR 1.08 per 5 affected days.
MD_EFFECT_TARGETS <- list(
  null = list(name = "null", rr_per_5 = 1, beta_per_unit = 0),
  small = list(name = "small", rr_per_5 = 1.02, beta_per_unit = log(1.02) / 5),
  moderate = list(name = "moderate", rr_per_5 = 1.08, beta_per_unit = log(1.08) / 5)
)

# ---------------------------------------------------------------------------
# Privacy-safe expected monthly margins from committed disclosure summaries
# ---------------------------------------------------------------------------

md_default_summary_paths <- function(root = NULL) {
  if (is.null(root)) {
    root <- if (exists("project_root", mode = "function")) {
      project_root()
    } else {
      normalizePath(".", winslash = "/", mustWork = TRUE)
    }
  }
  list(
    annual = file.path(root, "outputs", "tables", "cvd_descriptive_annual_totals.csv"),
    seasonal = file.path(root, "outputs", "tables", "cvd_descriptive_seasonality_by_month.csv"),
    covid = file.path(root, "outputs", "tables", "cvd_descriptive_covid_era_means.csv"),
    core_fit = file.path(root, "outputs", "tables", "cvd_core_model_fit.csv")
  )
}

#' Parse disclosure summaries into privacy-safe expected monthly margin components.
#'
#' Derives from disclosed annual totals only (never real monthly cells):
#' - pre-2020 log-linear annual trend (`trend_annual_total`)
#' - constant annual level for depletion-off (`constant_annual_level`)
#' - year-specific COVID factor = observed_annual / trend_annual
#' - calendar-month seasonal shares from disclosed cross-year month means
#'
#' Daily construction applies depletion/COVID toggles in `md_daily_nuisance_mean`.
md_parse_expected_monthly_margins <- function(outcome = c("chd", "hf"),
                                              root = NULL,
                                              paths = NULL) {
  outcome <- match.arg(outcome)
  if (is.null(paths)) paths <- md_default_summary_paths(root)
  for (nm in c("annual", "seasonal")) {
    if (!file.exists(paths[[nm]])) {
      stop("Missing disclosure summary: ", paths[[nm]])
    }
  }
  annual <- utils::read.csv(paths$annual, stringsAsFactors = FALSE)
  seasonal <- utils::read.csv(paths$seasonal, stringsAsFactors = FALSE)

  annual <- annual[annual$outcome == outcome, , drop = FALSE]
  seasonal <- seasonal[seasonal$outcome == outcome, , drop = FALSE]
  if (!nrow(annual) || !nrow(seasonal)) {
    stop("No disclosure rows for outcome=", outcome)
  }

  # Seasonal shares from cross-year mean_events (not actual month values).
  seas <- seasonal$mean_events
  names(seas) <- as.character(as.integer(seasonal$month))
  share <- seas / sum(seas)

  years <- sort(unique(as.integer(annual$year)))
  ann_tot <- setNames(as.numeric(annual$total_events), as.character(annual$year))

  # Pre-2020 log-linear trend on disclosed annual totals.
  pre <- years[years <= 2019]
  if (length(pre) < 2L) stop("Need >=2 pre-2020 annual totals for trend")
  y_pre <- ann_tot[as.character(pre)]
  if (any(!is.finite(y_pre) | y_pre <= 0)) {
    stop("Non-positive pre-2020 annual totals for outcome=", outcome)
  }
  fit_tr <- stats::lm(log(y_pre) ~ pre)
  a <- unname(stats::coef(fit_tr)[1])
  b <- unname(stats::coef(fit_tr)[2])
  trend_annual <- setNames(exp(a + b * years), as.character(years))
  # Constant level when depletion is off: mean of pre-2020 disclosed totals.
  constant_annual <- mean(y_pre)
  # Year-specific COVID / residual factor relative to smooth trend.
  covid_factor <- setNames(ann_tot[as.character(years)] / trend_annual, as.character(years))
  covid_factor[!is.finite(covid_factor)] <- 1

  rows <- list()
  for (yr in years) {
    yk <- as.character(yr)
    for (mo in 1:12) {
      mid <- sprintf("%04d-%02d", yr, mo)
      sh <- as.numeric(share[as.character(mo)])
      rows[[length(rows) + 1L]] <- data.frame(
        outcome = outcome,
        year = yr,
        month = mo,
        month_id = mid,
        seasonal_share = sh,
        annual_total = as.numeric(ann_tot[[yk]]),
        trend_annual_total = as.numeric(trend_annual[[yk]]),
        constant_annual_level = as.numeric(constant_annual),
        covid_year_factor = as.numeric(covid_factor[[yk]]),
        # Scaffold only: trend x season (no COVID baked in). Not a real month cell.
        expected_count_trend = as.numeric(trend_annual[[yk]]) * sh,
        data_status = MD_PROVENANCE_SYNTHETIC,
        margin_source = "disclosure_annual_trend_x_seasonal_share",
        stringsAsFactors = FALSE
      )
    }
  }
  margins <- do.call(rbind, rows)

  margins$days_in_month <- vapply(margins$month_id, function(mid) {
    d0 <- as.Date(paste0(mid, "-01"))
    as.integer(seq(d0, by = "month", length.out = 2L)[2L] - d0)
  }, integer(1))

  rownames(margins) <- NULL
  margins
}

#' Spread margin components to a daily nuisance mean on HKO dates.
#'
#' depletion=TRUE  -> use trend_annual_total (smooth decline)
#' depletion=FALSE -> use constant_annual_level (flat year level)
#' covid_on=TRUE   -> multiply by year-specific covid_year_factor
#' covid_on=FALSE  -> no COVID residual factor
#'
#' Does not use or reconstruct real monthly outcome counts.
md_daily_nuisance_mean <- function(margins, dates, depletion = FALSE,
                                   covid_on = FALSE) {
  dates <- as.Date(dates)
  month_id <- format(dates, "%Y-%m")
  required <- c(
    "month_id", "seasonal_share", "days_in_month",
    "trend_annual_total", "constant_annual_level", "covid_year_factor"
  )
  missing <- setdiff(required, names(margins))
  if (length(missing)) {
    stop("margins missing columns: ", paste(missing, collapse = ", "))
  }

  ann_level <- if (isTRUE(depletion)) {
    setNames(margins$trend_annual_total, margins$month_id)
  } else {
    setNames(margins$constant_annual_level, margins$month_id)
  }
  covid_f <- setNames(margins$covid_year_factor, margins$month_id)
  share <- setNames(margins$seasonal_share, margins$month_id)
  days <- setNames(margins$days_in_month, margins$month_id)

  year_level <- as.numeric(ann_level[month_id])
  if (isTRUE(covid_on)) {
    year_level <- year_level * as.numeric(covid_f[month_id])
  }
  mu_month <- year_level * as.numeric(share[month_id])
  base <- mu_month / pmax(as.numeric(days[month_id]), 1)
  base <- as.numeric(base)
  if (any(!is.finite(base))) {
    stop("non_finite daily nuisance mean from margin components")
  }

  data.frame(
    date = dates,
    month_id = month_id,
    mu_nuisance = base,
    depletion = isTRUE(depletion),
    covid_on = isTRUE(covid_on),
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
}

# ---------------------------------------------------------------------------
# Coherent daily DGP
# ---------------------------------------------------------------------------

.md_ar1_centered <- function(n, rho, sd = 0.05, innov_scale = NULL) {
  if (!is.finite(rho) || abs(rho) < 1e-12) return(rep(0, n))
  if (is.null(innov_scale)) {
    innov_scale <- sd * sqrt(max(1 - rho^2, 1e-8))
  }
  e <- numeric(n)
  e[1] <- stats::rnorm(1, 0, sd)
  if (n > 1L) {
    for (i in 2:n) {
      e[i] <- rho * e[i - 1L] + stats::rnorm(1, 0, innov_scale)
    }
  }
  e - mean(e)
}

#' Simulate latent daily counts and monthly aggregates under fixed HKO weather.
#'
#' @param weather_daily data.frame with date and exposure columns
#' @param margins privacy-safe expected monthly margins
#' @param exposure_col name of daily exposure column (already kernel-applied or raw event)
#' @param kernel kernel name if exposure_col is a raw event indicator
#' @param effect_name null/small/moderate
#' @param overdispersion_phi NB/gamma frailty variance on monthly multiplier
#'   (phi=0 => pure Poisson aggregation)
#' @param ar1_rho centered monthly AR(1) on log frailty; 0 disables
#' @param depletion logical secular depletion tilt
#' @param covid_on logical COVID phase switches
#' @param seed integer
md_simulate_dgp <- function(weather_daily,
                            margins,
                            exposure_col = "hot_night",
                            kernel = c("same_day", "cumulative_0_5", "cumulative_0_21"),
                            effect_name = c("null", "small", "moderate"),
                            overdispersion_phi = 0.02,
                            ar1_rho = 0,
                            depletion = TRUE,
                            covid_on = TRUE,
                            seed = 1L,
                            outcome = "chd") {
  kernel <- match.arg(kernel)
  effect_name <- match.arg(effect_name)
  set.seed(as.integer(seed))

  w <- weather_daily[order(as.Date(weather_daily$date)), , drop = FALSE]
  dates <- as.Date(w$date)
  if (!exposure_col %in% names(w)) {
    stop("weather_daily missing exposure_col=", exposure_col)
  }
  event <- as.numeric(w[[exposure_col]])
  event[!is.finite(event)] <- 0
  x_exp <- md_apply_kernel(event, kernel)

  eff <- MD_EFFECT_TARGETS[[effect_name]]
  beta_true <- eff$beta_per_unit

  nuis <- md_daily_nuisance_mean(
    margins = margins,
    dates = dates,
    depletion = depletion,
    covid_on = covid_on
  )
  mu0 <- nuis$mu_nuisance
  # Apply thermal effect on daily intensity
  mu_d <- mu0 * exp(beta_true * x_exp)

  month_id <- nuis$month_id
  um <- unique(month_id)
  M <- length(um)

  # Month-level gamma frailty => NB-like monthly overdispersion when aggregated.
  if (is.finite(overdispersion_phi) && overdispersion_phi > 0) {
    # Gamma mean 1, variance phi
    shape <- 1 / overdispersion_phi
    frailty <- stats::rgamma(M, shape = shape, rate = shape)
  } else {
    frailty <- rep(1, M)
  }
  names(frailty) <- um

  # Centered monthly AR(1) log factor
  ar_factor <- exp(.md_ar1_centered(M, rho = ar1_rho, sd = 0.04))
  names(ar_factor) <- um
  # Renormalize to mean 1 to avoid shifting total burden
  ar_factor <- ar_factor / mean(ar_factor)

  month_mult <- frailty * ar_factor
  mu_d <- mu_d * month_mult[month_id]

  # Latent daily counts
  y_d <- stats::rpois(length(mu_d), lambda = pmax(mu_d, 0))
  S <- vapply(um, function(m) sum(y_d[month_id == m]), numeric(1))
  names(S) <- um

  list(
    dates = dates,
    month_id = month_id,
    exposure_event = event,
    exposure = x_exp,
    mu_nuisance = mu0,
    mu_daily = as.numeric(mu_d),
    y_daily = y_d,
    S = S,
    beta_true = beta_true,
    rr_per_5_true = eff$rr_per_5,
    effect_name = effect_name,
    kernel = kernel,
    exposure_col = exposure_col,
    overdispersion_phi = overdispersion_phi,
    ar1_rho = ar1_rho,
    depletion = depletion,
    covid_on = covid_on,
    outcome = outcome,
    frailty = frailty,
    ar_factor = ar_factor,
    data_status = MD_PROVENANCE_SYNTHETIC,
    target_mapping = list(
      md_parameter = "beta_per_unit_exposure",
      declared_scalar = "beta_per_unit",
      rr_per_5 = eff$rr_per_5,
      note = paste0(
        "M|D estimates beta on daily kernel exposure; ",
        "declared scalar target is beta = log(RR_per_5)/5. ",
        "Monthly NB / spillover estimators target a monthly burden coefficient ",
        "and are reported with explicit target_mapping, not as identical betas."
      )
    )
  )
}

# ---------------------------------------------------------------------------
# Scenario builder
# ---------------------------------------------------------------------------

#' Build sparse balanced core (36) plus one-factor edge cells.
#'
#' Core: 2 scales × 3 effects × 3 kernels × AR off/on,
#' with depletion=ON and covid=ON fixed.
md_build_scenarios <- function(include_edge = TRUE) {
  scales <- c("chd_like", "hf_like")
  effects <- c("null", "small", "moderate")
  kernels <- c("same_day", "cumulative_0_5", "cumulative_0_21")
  ar_opts <- c("none", "outcome_matched")

  rows <- list()
  sid <- 0L
  for (sc in scales) {
    for (ef in effects) {
      for (kn in kernels) {
        for (ar in ar_opts) {
          sid <- sid + 1L
          rows[[length(rows) + 1L]] <- data.frame(
            scenario_id = sprintf("CORE_%02d", sid),
            cell_class = "core",
            scale = sc,
            outcome = if (sc == "chd_like") "chd" else "hf",
            effect = ef,
            kernel = kn,
            serial_dependence = ar,
            depletion = "outcome_matched",
            covid_shock = "observed_pattern",
            overdispersion = "outcome_matched",
            # Outcome-specific exposure family for all kernels.
            exposure_col = if (identical(sc, "chd_like")) "hot_night" else "cold_day",
            stringsAsFactors = FALSE
          )
        }
      }
    }
  }
  core <- do.call(rbind, rows)
  stopifnot(nrow(core) == 36L)

  edge <- NULL
  if (isTRUE(include_edge)) {
    # Baseline for one-factor edges: CHD, null, same_day, AR none, depletion on, covid on
    base <- list(
      scale = "chd_like", outcome = "chd", effect = "null",
      kernel = "same_day", serial_dependence = "none",
      depletion = "outcome_matched", covid_shock = "observed_pattern",
      overdispersion = "outcome_matched", exposure_col = "hot_night"
    )
    edges <- list(
      list(depletion = "none", tag = "EDGE_depletion_off"),
      list(covid_shock = "none", tag = "EDGE_covid_off"),
      list(overdispersion = "none", tag = "EDGE_od_off"),
      list(overdispersion = "high", tag = "EDGE_od_high"),
      list(effect = "moderate", serial_dependence = "outcome_matched",
           depletion = "outcome_matched", covid_shock = "observed_pattern",
           tag = "EDGE_stress_AR_dep_covid_mod"),
      list(effect = "small", kernel = "cumulative_0_21", tag = "EDGE_small_lag21")
    )
    erows <- lapply(seq_along(edges), function(i) {
      e <- edges[[i]]
      b <- base
      for (nm in setdiff(names(e), "tag")) b[[nm]] <- e[[nm]]
      data.frame(
        scenario_id = e$tag,
        cell_class = "edge",
        scale = b$scale,
        outcome = b$outcome,
        effect = b$effect,
        kernel = b$kernel,
        serial_dependence = b$serial_dependence,
        depletion = b$depletion,
        covid_shock = b$covid_shock,
        overdispersion = b$overdispersion,
        exposure_col = b$exposure_col,
        stringsAsFactors = FALSE
      )
    })
    edge <- do.call(rbind, erows)
  }

  out <- if (is.null(edge)) core else rbind(core, edge)
  out$data_status <- MD_PROVENANCE_SYNTHETIC
  rownames(out) <- NULL
  out
}

md_scenario_params <- function(scenario_row, core_fit_path = NULL) {
  # Map scenario factors to numeric DGP knobs.
  outcome <- scenario_row$outcome
  # Default overdispersion from NB theta in disclosure fit if available.
  phi <- 0.02
  ar_rho <- 0
  if (identical(as.character(scenario_row$overdispersion), "none")) {
    phi <- 0
  } else if (identical(as.character(scenario_row$overdispersion), "high")) {
    phi <- 0.08
  } else {
    # outcome_matched: frailty variance ≈ 1/theta from NB disclosure fit.
    if (!is.null(core_fit_path) && file.exists(core_fit_path)) {
      cf <- utils::read.csv(core_fit_path, stringsAsFactors = FALSE)
      cf <- cf[cf$outcome == outcome &
                 cf$family == "negative_binomial" &
                 cf$offset_policy == "days_only", , drop = FALSE]
      if (nrow(cf) && any(is.finite(cf$theta))) {
        th <- stats::median(cf$theta, na.rm = TRUE)
        if (is.finite(th) && th > 0) phi <- 1 / th
      }
    }
  }

  if (identical(as.character(scenario_row$serial_dependence), "outcome_matched")) {
    # Match committed residual ACF1 diagnostics (~0.53 CHD, ~0.15 HF).
    ar_rho <- if (identical(outcome, "chd")) 0.50 else 0.15
  }

  list(
    overdispersion_phi = phi,
    ar1_rho = ar_rho,
    depletion = !identical(as.character(scenario_row$depletion), "none"),
    covid_on = !identical(as.character(scenario_row$covid_shock), "none")
  )
}

#' Checkpoint path unique by scenario, run mode, and repetition count.
md_checkpoint_path <- function(
    ckpt_dir,
    scenario_id,
    run_mode,
    n_reps,
    design_version = NULL) {
  version_tag <- if (is.null(design_version) || !nzchar(design_version)) {
    ""
  } else {
    paste0("__design-", gsub("[^A-Za-z0-9_.-]", "_", design_version))
  }
  file.path(
    ckpt_dir,
    sprintf(
      "%s%s__mode-%s__reps-%d.csv",
      scenario_id,
      version_tag,
      run_mode,
      as.integer(n_reps)
    )
  )
}

# ---------------------------------------------------------------------------
# Estimator wrappers (preserve explicit failures)
# ---------------------------------------------------------------------------

.md_estimator_fail <- function(estimator, message, target_mapping = NA_character_) {
  list(
    ok = FALSE,
    estimator = estimator,
    message = message,
    estimate = NA_real_,
    se = NA_real_,
    conf_low = NA_real_,
    conf_high = NA_real_,
    converged = FALSE,
    hessian_pd = NA,
    hessian_condition = NA_real_,
    dispersion = NA_real_,
    loglik = NA_real_,
    target_mapping = target_mapping,
    data_status = MD_PROVENANCE_SYNTHETIC
  )
}

#' Capture and muffle warnings from an expression; return value + warning texts.
#'
#' Errors are returned as the value (inherits "error") rather than thrown, so
#' callers can attach captured warnings to an explicit failure message.
.md_with_captured_warnings <- function(expr) {
  warns <- character(0)
  val <- withCallingHandlers(
    tryCatch(force(expr), error = function(e) e),
    warning = function(w) {
      warns <<- c(warns, conditionMessage(w))
      tryInvokeRestart("muffleWarning")
    }
  )
  list(value = val, warnings = unique(as.character(warns)))
}

#' Classify fit warnings that must fail the estimator (not silently accepted).
.md_serious_fit_warning <- function(msgs) {
  if (!length(msgs)) return(FALSE)
  pat <- paste(
    "theta\\.ml",
    "iteration limit",
    "alternation limit",
    "did not converge",
    "failed to converge",
    "algorithm did not converge",
    "non[- ]?convergence",
    "fitted probabilities numerically 0 or 1",
    sep = "|"
  )
  any(grepl(pat, msgs, ignore.case = TRUE, perl = TRUE))
}

.md_message_with_warnings <- function(base, warns) {
  base <- as.character(base %||% "ok")
  if (!length(warns)) return(base)
  paste0(base, " | warnings: ", paste(warns, collapse = " || "))
}

#' Oracle daily Poisson / quasi-Poisson (simulation only; uses latent y_daily).
md_fit_oracle_daily <- function(sim, include_covid = TRUE, quasi = TRUE) {
  target_map <- "oracle_daily_beta_per_unit_exposure_identical_to_DGP"
  if (is.null(sim$y_daily)) {
    return(.md_estimator_fail("oracle_daily", "missing latent y_daily", target_map))
  }
  X <- tryCatch(
    md_build_daily_design(
      dates = sim$dates,
      exposure = sim$exposure,
      include_covid = include_covid,
      exposure_name = "exposure"
    ),
    error = function(e) e
  )
  if (inherits(X, "error")) {
    return(.md_estimator_fail("oracle_daily", conditionMessage(X), target_map))
  }
  off <- rep(1, length(sim$y_daily))
  dat <- data.frame(y = sim$y_daily, X, check.names = FALSE)
  form <- stats::as.formula(paste("y ~ 0 +", paste(colnames(X), collapse = " + ")))
  captured <- .md_with_captured_warnings(
    stats::glm(
      form,
      family = if (quasi) stats::quasipoisson() else stats::poisson(),
      data = dat,
      offset = log(off)
    )
  )
  fit <- captured$value
  warns <- captured$warnings
  if (inherits(fit, "error")) {
    return(.md_estimator_fail(
      "oracle_daily",
      .md_message_with_warnings(conditionMessage(fit), warns),
      target_map
    ))
  }
  if (.md_serious_fit_warning(warns) || !isTRUE(fit$converged)) {
    return(.md_estimator_fail(
      "oracle_daily",
      .md_message_with_warnings(
        if (!isTRUE(fit$converged)) "glm_not_converged" else "serious_fit_warning",
        warns
      ),
      target_map
    ))
  }
  cf <- summary(fit)$coefficients
  if (!"exposure" %in% rownames(cf)) {
    return(.md_estimator_fail(
      "oracle_daily",
      .md_message_with_warnings("exposure coef missing", warns),
      target_map
    ))
  }
  est <- cf["exposure", "Estimate"]
  se <- cf["exposure", "Std. Error"]
  list(
    ok = TRUE,
    estimator = "oracle_daily",
    message = .md_message_with_warnings("ok", warns),
    estimate = unname(est),
    se = unname(se),
    conf_low = unname(est - 1.96 * se),
    conf_high = unname(est + 1.96 * se),
    converged = TRUE,
    hessian_pd = TRUE,
    hessian_condition = NA_real_,
    dispersion = if (quasi) summary(fit)$dispersion else 1,
    loglik = tryCatch(as.numeric(stats::logLik(fit)), error = function(e) NA_real_),
    target_mapping = target_map,
    data_status = MD_PROVENANCE_SYNTHETIC
  )
}

#' Constrained M|D aggregate likelihood estimator.
md_fit_md_estimator <- function(sim, include_covid = TRUE, quasi = TRUE) {
  target_map <- "md_beta_per_unit_exposure_identical_to_DGP_declared_scalar"
  X <- tryCatch(
    md_build_daily_design(
      dates = sim$dates,
      exposure = sim$exposure,
      include_covid = include_covid,
      exposure_name = "exposure"
    ),
    error = function(e) e
  )
  if (inherits(X, "error")) {
    return(.md_estimator_fail("md", conditionMessage(X), target_map))
  }
  fit <- tryCatch(
    md_fit(
      S = sim$S,
      X = X,
      month_id = sim$month_id,
      offset = rep(1, length(sim$dates)),
      quasi = quasi
    ),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(.md_estimator_fail("md", conditionMessage(fit), target_map))
  }
  if (!isTRUE(fit$converged)) {
    out <- .md_estimator_fail("md", fit$message %||% fit$status, target_map)
    out$hessian_pd <- fit$hessian_pd
    out$hessian_condition <- fit$hessian_condition
    out$converged <- FALSE
    return(out)
  }
  ci <- md_exposure_ci(fit, exposure_name = "exposure", use_quasi = quasi, contrast = 1)
  list(
    ok = TRUE,
    estimator = "md",
    message = fit$message,
    estimate = ci$estimate[[1]],
    se = ci$se[[1]],
    conf_low = ci$conf_low[[1]],
    conf_high = ci$conf_high[[1]],
    converged = TRUE,
    hessian_pd = isTRUE(fit$hessian_pd),
    hessian_condition = fit$hessian_condition,
    dispersion = fit$dispersion,
    loglik = fit$loglik,
    target_mapping = target_map,
    data_status = MD_PROVENANCE_SYNTHETIC,
    fit = fit
  )
}

#' Monthly negative-binomial on month-summed exposure burden.
md_fit_monthly_nb <- function(sim) {
  target_map <- paste0(
    "monthly_nb_coef_on_mean_daily_exposure_NOT_identical_to_md_beta; ",
    "compare via declared rr_per_5 mapping only with caution"
  )
  um <- names(sim$S)
  xbar <- vapply(um, function(m) mean(sim$exposure[sim$month_id == m]), numeric(1))
  days <- vapply(um, function(m) sum(sim$month_id == m), numeric(1))
  y <- as.numeric(sim$S[um])
  time_index <- seq_along(um)
  month_f <- factor(as.integer(substr(um, 6, 7)))
  dat <- data.frame(
    y = y,
    x = xbar,
    time_index = time_index,
    month_f = month_f,
    days = days
  )
  if (!requireNamespace("MASS", quietly = TRUE)) {
    return(.md_estimator_fail("monthly_nb", "MASS not available", target_map))
  }
  if (!requireNamespace("splines", quietly = TRUE)) {
    return(.md_estimator_fail("monthly_nb", "splines not available", target_map))
  }
  captured <- .md_with_captured_warnings(
    MASS::glm.nb(
      y ~ month_f + splines::ns(time_index, df = 4) + x + offset(log(days)),
      data = dat
    )
  )
  fit <- captured$value
  warns <- captured$warnings
  if (inherits(fit, "error")) {
    return(.md_estimator_fail(
      "monthly_nb",
      .md_message_with_warnings(conditionMessage(fit), warns),
      target_map
    ))
  }
  if (.md_serious_fit_warning(warns)) {
    return(.md_estimator_fail(
      "monthly_nb",
      .md_message_with_warnings("serious_nb_fit_warning", warns),
      target_map
    ))
  }
  cf <- summary(fit)$coefficients
  if (!"x" %in% rownames(cf)) {
    return(.md_estimator_fail(
      "monthly_nb",
      .md_message_with_warnings("exposure coef missing", warns),
      target_map
    ))
  }
  est <- cf["x", "Estimate"]
  se <- cf["x", "Std. Error"]
  list(
    ok = TRUE,
    estimator = "monthly_nb",
    message = .md_message_with_warnings("ok", warns),
    estimate = unname(est),
    se = unname(se),
    conf_low = unname(est - 1.96 * se),
    conf_high = unname(est + 1.96 * se),
    converged = TRUE,
    hessian_pd = TRUE,
    hessian_condition = NA_real_,
    dispersion = NA_real_,
    loglik = tryCatch(as.numeric(stats::logLik(fit)), error = function(e) NA_real_),
    target_mapping = target_map,
    data_status = MD_PROVENANCE_SYNTHETIC
  )
}

#' Negative-binomial GLARMA AR1 + offset if glarma is available.
md_fit_glarma_ar1 <- function(sim) {
  target_map <- paste0(
    "glarma_ar1_coef_on_mean_daily_exposure_NOT_identical_to_md_beta"
  )
  if (!requireNamespace("glarma", quietly = TRUE)) {
    return(.md_estimator_fail("glarma_ar1", "glarma package not available", target_map))
  }
  if (!requireNamespace("MASS", quietly = TRUE) ||
      !requireNamespace("splines", quietly = TRUE)) {
    return(.md_estimator_fail("glarma_ar1", "MASS/splines required", target_map))
  }
  um <- names(sim$S)
  xbar <- vapply(um, function(m) mean(sim$exposure[sim$month_id == m]), numeric(1))
  days <- vapply(um, function(m) sum(sim$month_id == m), numeric(1))
  y <- as.numeric(sim$S[um])
  time_index <- seq_along(um)
  month_f <- factor(as.integer(substr(um, 6, 7)))
  # Design without intercept (glarma style often includes)
  Xmm <- stats::model.matrix(
    ~ month_f + splines::ns(time_index, df = 4) + xbar
  )
  seed_cap <- .md_with_captured_warnings(
    MASS::glm.nb(
      y ~ month_f + splines::ns(time_index, df = 4) + xbar + offset(log(days))
    )
  )
  fit0 <- seed_cap$value
  warns <- seed_cap$warnings
  if (inherits(fit0, "error")) {
    return(.md_estimator_fail(
      "glarma_ar1",
      .md_message_with_warnings(paste("nb seed failed:", conditionMessage(fit0)), warns),
      target_map
    ))
  }
  if (.md_serious_fit_warning(warns)) {
    return(.md_estimator_fail(
      "glarma_ar1",
      .md_message_with_warnings("serious_nb_seed_warning", warns),
      target_map
    ))
  }
  alpha <- unname(fit0$theta)
  final_cap <- .md_with_captured_warnings(
    glarma::glarma(
      y = y,
      X = Xmm,
      offset = log(days),
      type = "NegBin",
      alpha = alpha,
      phiLags = 1L,
      method = "FS"
    )
  )
  fit <- final_cap$value
  warns <- c(warns, final_cap$warnings)
  if (inherits(fit, "error")) {
    return(.md_estimator_fail(
      "glarma_ar1",
      .md_message_with_warnings(conditionMessage(fit), warns),
      target_map
    ))
  }
  if (.md_serious_fit_warning(final_cap$warnings)) {
    return(.md_estimator_fail(
      "glarma_ar1",
      .md_message_with_warnings("serious_glarma_fit_warning", warns),
      target_map
    ))
  }
  cf <- tryCatch(summary(fit)$coefficients1, error = function(e) NULL)
  if (is.null(cf)) cf <- tryCatch(summary(fit)$coefficients, error = function(e) NULL)
  rn <- rownames(cf)
  hit <- grep("xbar", rn)[1]
  if (!length(hit) || is.na(hit)) {
    return(.md_estimator_fail(
      "glarma_ar1",
      .md_message_with_warnings("exposure coef missing in glarma", warns),
      target_map
    ))
  }
  est <- cf[hit, 1]
  se <- cf[hit, 2]
  list(
    ok = TRUE,
    estimator = "glarma_ar1",
    message = .md_message_with_warnings("ok", warns),
    estimate = unname(est),
    se = unname(se),
    conf_low = unname(est - 1.96 * se),
    conf_high = unname(est + 1.96 * se),
    converged = TRUE,
    hessian_pd = TRUE,
    hessian_condition = NA_real_,
    dispersion = NA_real_,
    loglik = tryCatch(as.numeric(fit$logLik), error = function(e) NA_real_),
    target_mapping = target_map,
    data_status = MD_PROVENANCE_SYNTHETIC
  )
}

#' Simplified spillover-burden monthly model: month sum of kernel exposure.
md_fit_spillover_burden <- function(sim) {
  target_map <- paste0(
    "spillover_burden_coef_on_month_sum_exposure_NOT_identical_to_md_beta; ",
    "scalar comparable only after /days_in_month scaling"
  )
  um <- names(sim$S)
  xsum <- vapply(um, function(m) sum(sim$exposure[sim$month_id == m]), numeric(1))
  days <- vapply(um, function(m) sum(sim$month_id == m), numeric(1))
  y <- as.numeric(sim$S[um])
  time_index <- seq_along(um)
  month_f <- factor(as.integer(substr(um, 6, 7)))
  dat <- data.frame(y = y, x = xsum / days, time_index = time_index,
                    month_f = month_f, days = days)
  if (!requireNamespace("MASS", quietly = TRUE)) {
    return(.md_estimator_fail("spillover_burden", "MASS not available", target_map))
  }
  captured <- .md_with_captured_warnings(
    MASS::glm.nb(
      y ~ month_f + splines::ns(time_index, df = 4) + x + offset(log(days)),
      data = dat
    )
  )
  fit <- captured$value
  warns <- captured$warnings
  if (inherits(fit, "error")) {
    return(.md_estimator_fail(
      "spillover_burden",
      .md_message_with_warnings(conditionMessage(fit), warns),
      target_map
    ))
  }
  if (.md_serious_fit_warning(warns)) {
    return(.md_estimator_fail(
      "spillover_burden",
      .md_message_with_warnings("serious_nb_fit_warning", warns),
      target_map
    ))
  }
  cf <- summary(fit)$coefficients
  if (!"x" %in% rownames(cf)) {
    return(.md_estimator_fail(
      "spillover_burden",
      .md_message_with_warnings("coef missing", warns),
      target_map
    ))
  }
  est <- cf["x", "Estimate"]
  se <- cf["x", "Std. Error"]
  list(
    ok = TRUE,
    estimator = "spillover_burden",
    message = .md_message_with_warnings("ok", warns),
    estimate = unname(est),
    se = unname(se),
    conf_low = unname(est - 1.96 * se),
    conf_high = unname(est + 1.96 * se),
    converged = TRUE,
    hessian_pd = TRUE,
    hessian_condition = NA_real_,
    dispersion = NA_real_,
    loglik = tryCatch(as.numeric(stats::logLik(fit)), error = function(e) NA_real_),
    target_mapping = target_map,
    data_status = MD_PROVENANCE_SYNTHETIC
  )
}

md_run_estimators <- function(sim, estimators = c(
  "oracle_daily", "md", "monthly_nb", "glarma_ar1", "spillover_burden"
)) {
  out <- list()
  for (est in estimators) {
    res <- tryCatch(
      {
        switch(
          est,
          oracle_daily = md_fit_oracle_daily(sim),
          md = md_fit_md_estimator(sim),
          monthly_nb = md_fit_monthly_nb(sim),
          glarma_ar1 = md_fit_glarma_ar1(sim),
          spillover_burden = md_fit_spillover_burden(sim),
          .md_estimator_fail(est, "unknown estimator")
        )
      },
      error = function(e) .md_estimator_fail(est, conditionMessage(e))
    )
    # Strip heavy fit object before binding
    res$fit <- NULL
    out[[est]] <- res
  }
  out
}

# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

md_metrics_from_replicates <- function(estimates,
                                       se,
                                       conf_low,
                                       conf_high,
                                       beta_true,
                                       effect_name,
                                       converged,
                                       hessian_pd = NULL,
                                       hessian_condition = NULL,
                                       loglik = NULL,
                                       loglik_sat = NULL) {
  ok <- isTRUE(converged) | converged %in% TRUE
  # Allow vectorized
  conv <- as.logical(converged)
  est <- as.numeric(estimates)
  s <- as.numeric(se)
  lo <- as.numeric(conf_low)
  hi <- as.numeric(conf_high)
  n <- length(est)
  conv[is.na(conv)] <- FALSE

  bias <- mean(est[conv] - beta_true, na.rm = TRUE)
  rmse <- sqrt(mean((est[conv] - beta_true)^2, na.rm = TRUE))
  cover <- mean(lo[conv] <= beta_true & hi[conv] >= beta_true, na.rm = TRUE)
  # Type I: reject H0 at 5% when true null
  reject <- (lo > 0) | (hi < 0)
  type1 <- if (identical(effect_name, "null") || isTRUE(all.equal(beta_true, 0))) {
    mean(reject[conv], na.rm = TRUE)
  } else {
    NA_real_
  }
  # False sign for non-null: estimate opposite sign of truth among converged
  false_sign <- if (!identical(effect_name, "null") && beta_true != 0) {
    mean(sign(est[conv]) != sign(beta_true) & is.finite(est[conv]), na.rm = TRUE)
  } else {
    NA_real_
  }
  conv_rate <- mean(conv, na.rm = TRUE)
  se_mean <- mean(s[conv], na.rm = TRUE)
  sd_est <- stats::sd(est[conv], na.rm = TRUE)
  se_sd_ratio <- if (is.finite(sd_est) && sd_est > 0) se_mean / sd_est else NA_real_

  rel_bias <- if (is.finite(beta_true) && abs(beta_true) > 1e-12) {
    abs(bias / beta_true)
  } else {
    NA_real_
  }

  pd_rate <- if (!is.null(hessian_pd)) {
    mean(as.logical(hessian_pd)[conv], na.rm = TRUE)
  } else NA_real_
  cond_med <- if (!is.null(hessian_condition)) {
    stats::median(as.numeric(hessian_condition)[conv], na.rm = TRUE)
  } else NA_real_
  divergent_rate <- mean(!conv | (!is.null(hessian_pd) & !as.logical(hessian_pd)),
                         na.rm = TRUE)

  # Predictive log score where feasible: mean held-in loglik (higher better)
  pred_log_score <- if (!is.null(loglik)) {
    mean(as.numeric(loglik)[conv], na.rm = TRUE)
  } else NA_real_

  data.frame(
    n_reps = n,
    n_converged = sum(conv, na.rm = TRUE),
    convergence_rate = conv_rate,
    bias = bias,
    relative_bias_abs = rel_bias,
    rmse = rmse,
    coverage = cover,
    type1 = type1,
    false_sign = false_sign,
    se_mean = se_mean,
    sd_est = sd_est,
    se_sd_ratio = se_sd_ratio,
    hessian_pd_rate = pd_rate,
    hessian_condition_median = cond_med,
    divergent_or_boundary_rate = divergent_rate,
    predictive_log_score = pred_log_score,
    beta_true = beta_true,
    effect_name = effect_name,
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
}

#' Evaluate admission gates exactly from registry thresholds (no gaming).
md_evaluate_gates <- function(metric_rows, registry = NULL, root = NULL) {
  if (is.null(registry)) {
    if (exists("load_final_model_registry", mode = "function")) {
      registry <- load_final_model_registry(root = root)
    } else if (!is.null(root) && requireNamespace("yaml", quietly = TRUE)) {
      registry <- yaml::read_yaml(
        file.path(root, "analysis_plan", "final_model_registry.yml")
      )
    } else {
      stop("registry required for gate evaluation")
    }
  }
  g <- registry$md_feasibility$admission_gates
  g <- lapply(g, function(x) as.numeric(x))
  # Restrict to M|D estimator rows
  md <- metric_rows[metric_rows$estimator == "md", , drop = FALSE]
  if (!nrow(md)) {
    return(data.frame(
      gate_id = "all",
      passed = FALSE,
      detail = "no md metric rows",
      data_status = MD_PROVENANCE_SYNTHETIC,
      stringsAsFactors = FALSE
    ))
  }

  # Aggregate across core cells for primary gates; stress cells checked separately.
  core <- md[is.na(md$cell_class) | md$cell_class == "core", , drop = FALSE]
  if (!nrow(core)) core <- md

  conv <- mean(core$convergence_rate, na.rm = TRUE)
  # Type I from null effect cells only
  null_rows <- core[core$effect_name == "null" | core$effect == "null", , drop = FALSE]
  type1 <- if (nrow(null_rows)) mean(null_rows$type1, na.rm = TRUE) else NA_real_
  cover <- mean(core$coverage, na.rm = TRUE)
  # Relative bias on non-null
  nonnull <- core[!(core$effect_name == "null" | core$effect == "null"), , drop = FALSE]
  relb <- if (nrow(nonnull)) mean(nonnull$relative_bias_abs, na.rm = TRUE) else NA_real_
  # False sign on moderate
  mod <- core[core$effect_name == "moderate" | core$effect == "moderate", , drop = FALSE]
  fsign <- if (nrow(mod)) mean(mod$false_sign, na.rm = TRUE) else NA_real_
  cond_ok <- mean(core$hessian_condition_median < g$hessian_condition_max, na.rm = TRUE)
  # Require median condition among cells to pass; also track PD
  cond_med <- stats::median(core$hessian_condition_median, na.rm = TRUE)
  div <- mean(core$divergent_or_boundary_rate, na.rm = TRUE)

  # Stress scenarios: AR / depletion / COVID edge or core with those on
  stress <- md
  if ("serial_dependence" %in% names(md)) {
    stress <- md[
      md$serial_dependence == "outcome_matched" |
        md$depletion == "outcome_matched" |
        md$covid_shock == "observed_pattern" |
        grepl("EDGE_stress|EDGE_depletion|EDGE_covid", md$scenario_id %||% ""),
      ,
      drop = FALSE
    ]
  }
  stress_cover <- if (nrow(stress)) mean(stress$coverage, na.rm = TRUE) else NA_real_

  checks <- data.frame(
    gate_id = c(
      "convergence_min",
      "type1_range",
      "coverage_min",
      "relative_bias_max",
      "false_sign_max",
      "hessian_condition_max",
      "divergent_fit_max",
      "stress_coverage_min"
    ),
    value = c(conv, type1, cover, relb, fsign, cond_med, div, stress_cover),
    threshold = c(
      g$convergence_min,
      NA_real_,
      g$coverage_min,
      g$relative_bias_max,
      g$false_sign_max,
      g$hessian_condition_max,
      g$divergent_fit_max,
      g$stress_coverage_min
    ),
    passed = c(
      is.finite(conv) && conv >= g$convergence_min,
      is.finite(type1) && type1 >= g$type1_min && type1 <= g$type1_max,
      is.finite(cover) && cover >= g$coverage_min,
      is.finite(relb) && relb <= g$relative_bias_max,
      is.finite(fsign) && fsign <= g$false_sign_max,
      is.finite(cond_med) && cond_med < g$hessian_condition_max,
      is.finite(div) && div < g$divergent_fit_max,
      is.finite(stress_cover) && stress_cover >= g$stress_coverage_min
    ),
    detail = c(
      sprintf("convergence_rate=%.4f (min %.2f)", conv, g$convergence_min),
      sprintf("type1=%.4f (allowed [%.2f, %.2f])", type1, g$type1_min, g$type1_max),
      sprintf("coverage=%.4f (min %.2f)", cover, g$coverage_min),
      sprintf("abs_rel_bias=%.4f (max %.2f)", relb, g$relative_bias_max),
      sprintf("false_sign=%.4f (max %.2f)", fsign, g$false_sign_max),
      sprintf("hessian_cond_median=%.3g (max %.3g)", cond_med, g$hessian_condition_max),
      sprintf("divergent_rate=%.4f (max %.2f)", div, g$divergent_fit_max),
      sprintf("stress_coverage=%.4f (min %.2f)", stress_cover, g$stress_coverage_min)
    ),
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
  checks$all_passed <- all(checks$passed)
  checks$admission_decision <- if (all(checks$passed)) {
    "PASS_EXPLORATORY_REAL_SENSITIVITY_ONLY"
  } else {
    "FAIL_METHODS_FEASIBILITY_ONLY"
  }
  checks
}

md_estimator_result_to_row <- function(res, scenario_row, rep_id, beta_true) {
  data.frame(
    scenario_id = scenario_row$scenario_id,
    cell_class = scenario_row$cell_class,
    scale = scenario_row$scale,
    outcome = scenario_row$outcome,
    effect = scenario_row$effect,
    effect_name = scenario_row$effect,
    kernel = scenario_row$kernel,
    serial_dependence = scenario_row$serial_dependence,
    depletion = scenario_row$depletion,
    covid_shock = scenario_row$covid_shock,
    overdispersion = scenario_row$overdispersion,
    exposure_col = scenario_row$exposure_col,
    rep_id = as.integer(rep_id),
    estimator = res$estimator %||% NA_character_,
    ok = isTRUE(res$ok),
    message = res$message %||% NA_character_,
    estimate = res$estimate %||% NA_real_,
    se = res$se %||% NA_real_,
    conf_low = res$conf_low %||% NA_real_,
    conf_high = res$conf_high %||% NA_real_,
    converged = isTRUE(res$converged),
    hessian_pd = res$hessian_pd %||% NA,
    hessian_condition = res$hessian_condition %||% NA_real_,
    dispersion = res$dispersion %||% NA_real_,
    loglik = res$loglik %||% NA_real_,
    beta_true = beta_true,
    target_mapping = res$target_mapping %||% NA_character_,
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
}
