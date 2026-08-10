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

#' Simplified spillover-burden monthly model: month-sum kernel exposure.
#'
#' Predictor is the month sum of the daily kernel exposure (not the daily mean).
#' That coefficient is a different estimand from monthly_nb (mean exposure) and
#' from M|D daily beta; do not compare coefficients as identical.
md_fit_spillover_burden <- function(sim) {
  target_map <- paste0(
    "spillover_burden_coef_on_month_SUM_kernel_exposure_",
    "NOT_identical_to_md_daily_beta_or_monthly_nb_mean; different estimand"
  )
  um <- names(sim$S)
  xsum <- vapply(um, function(m) sum(sim$exposure[sim$month_id == m]), numeric(1))
  days <- vapply(um, function(m) sum(sim$month_id == m), numeric(1))
  y <- as.numeric(sim$S[um])
  time_index <- seq_along(um)
  month_f <- factor(as.integer(substr(um, 6, 7)))
  # Distinct from monthly_nb: month-sum exposure, not mean (xsum/days).
  dat <- data.frame(
    y = y,
    x = xsum,
    time_index = time_index,
    month_f = month_f,
    days = days
  )
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
# Metrics (F1.2: admissible M|D, comparable targets, worst-cell gates)
# ---------------------------------------------------------------------------

MD_COMPARABLE_ESTIMATORS <- c("oracle_daily", "md")

#' Row-wise M|D admissibility from raw metric columns (vectorized).
md_raw_rows_admissible <- function(converged,
                                   hessian_pd,
                                   hessian_condition,
                                   hessian_condition_max = MD_HESSIAN_CONDITION_MAX) {
  conv <- as.logical(converged)
  pd <- as.logical(hessian_pd)
  cond <- as.numeric(hessian_condition)
  conv[is.na(conv)] <- FALSE
  pd[is.na(pd)] <- FALSE
  conv & pd & is.finite(cond) & (cond < hessian_condition_max)
}

#' Whether an estimator's coefficient is comparable to the DGP daily beta.
md_estimator_target_comparable <- function(estimator) {
  as.character(estimator) %in% MD_COMPARABLE_ESTIMATORS
}

#' Explicit stress cells for coverage gate (F1.2).
#' AR-on core cells plus edge IDs involving depletion/covid/stress.
#' Does not treat all core cells as stress merely because depletion/COVID are on.
md_stress_metric_rows <- function(metric_rows) {
  if (!nrow(metric_rows)) return(metric_rows[FALSE, , drop = FALSE])
  ar_core <- !is.na(metric_rows$cell_class) &
    metric_rows$cell_class == "core" &
    !is.na(metric_rows$serial_dependence) &
    metric_rows$serial_dependence == "outcome_matched"
  edge_stress <- grepl(
    "EDGE_depletion|EDGE_covid|EDGE_stress",
    as.character(metric_rows$scenario_id %||% ""),
    ignore.case = TRUE
  )
  metric_rows[ar_core | edge_stress, , drop = FALSE]
}

.md_failing_ids <- function(ids, max_n = 12L) {
  ids <- unique(as.character(ids))
  ids <- ids[nzchar(ids) & !is.na(ids)]
  if (!length(ids)) return("none")
  if (length(ids) > max_n) {
    paste0(paste(ids[seq_len(max_n)], collapse = ","), ",...(+", length(ids) - max_n, ")")
  } else {
    paste(ids, collapse = ",")
  }
}

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
                                       loglik_sat = NULL,
                                       estimator = NULL,
                                       target_comparable = NULL,
                                       hessian_condition_max = MD_HESSIAN_CONDITION_MAX) {
  if (is.null(target_comparable)) {
    target_comparable <- md_estimator_target_comparable(estimator %||% "")
  }
  target_comparable <- isTRUE(target_comparable)

  conv_flag <- as.logical(converged)
  conv_flag[is.na(conv_flag)] <- FALSE
  est <- as.numeric(estimates)
  s <- as.numeric(se)
  lo <- as.numeric(conf_low)
  hi <- as.numeric(conf_high)
  n <- length(est)

  # M|D: admissible only if md_real_fit_admissible criteria hold.
  if (identical(as.character(estimator), "md")) {
    if (is.null(hessian_pd) || is.null(hessian_condition)) {
      admissible <- rep(FALSE, n)
    } else {
      admissible <- md_raw_rows_admissible(
        conv_flag, hessian_pd, hessian_condition, hessian_condition_max
      )
    }
    use <- admissible
    divergent_rate <- mean(!admissible, na.rm = TRUE)
    conv_rate <- mean(admissible, na.rm = TRUE)
    n_converged <- sum(admissible, na.rm = TRUE)
  } else {
    use <- conv_flag
    if (!is.null(hessian_pd)) {
      divergent_rate <- mean(
        !conv_flag | !as.logical(hessian_pd),
        na.rm = TRUE
      )
    } else {
      divergent_rate <- mean(!conv_flag, na.rm = TRUE)
    }
    conv_rate <- mean(conv_flag, na.rm = TRUE)
    n_converged <- sum(conv_flag, na.rm = TRUE)
  }

  se_mean <- mean(s[use], na.rm = TRUE)
  sd_est <- stats::sd(est[use], na.rm = TRUE)
  se_sd_ratio <- if (is.finite(sd_est) && sd_est > 0) se_mean / sd_est else NA_real_
  pred_log_score <- if (!is.null(loglik)) {
    mean(as.numeric(loglik)[use], na.rm = TRUE)
  } else NA_real_

  pd_rate <- if (!is.null(hessian_pd)) {
    mean(as.logical(hessian_pd)[use], na.rm = TRUE)
  } else NA_real_
  cond_med <- if (!is.null(hessian_condition)) {
    stats::median(as.numeric(hessian_condition)[use], na.rm = TRUE)
  } else NA_real_

  if (isTRUE(target_comparable)) {
    bias <- mean(est[use] - beta_true, na.rm = TRUE)
    rmse <- sqrt(mean((est[use] - beta_true)^2, na.rm = TRUE))
    cover <- mean(lo[use] <= beta_true & hi[use] >= beta_true, na.rm = TRUE)
    reject <- (lo > 0) | (hi < 0)
    type1 <- if (identical(effect_name, "null") || isTRUE(all.equal(beta_true, 0))) {
      mean(reject[use], na.rm = TRUE)
    } else {
      NA_real_
    }
    false_sign <- if (!identical(effect_name, "null") && beta_true != 0) {
      mean(sign(est[use]) != sign(beta_true) & is.finite(est[use]), na.rm = TRUE)
    } else {
      NA_real_
    }
    rel_bias <- if (is.finite(beta_true) && abs(beta_true) > 1e-12) {
      abs(bias / beta_true)
    } else {
      NA_real_
    }
  } else {
    bias <- NA_real_
    rmse <- NA_real_
    cover <- NA_real_
    type1 <- NA_real_
    false_sign <- NA_real_
    rel_bias <- NA_real_
  }

  data.frame(
    n_reps = n,
    n_converged = n_converged,
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
    target_comparable = target_comparable,
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
}

#' Summarise one scenario's raw replicate rows into per-estimator metrics.
md_summarise_scenario_raw <- function(raw_sc,
                                      hessian_condition_max = MD_HESSIAN_CONDITION_MAX) {
  if (!nrow(raw_sc)) return(NULL)
  ests <- unique(as.character(raw_sc$estimator))
  out <- lapply(ests, function(est) {
    sub <- raw_sc[as.character(raw_sc$estimator) == est, , drop = FALSE]
    comparable <- md_estimator_target_comparable(est)
    met <- md_metrics_from_replicates(
      estimates = sub$estimate,
      se = sub$se,
      conf_low = sub$conf_low,
      conf_high = sub$conf_high,
      beta_true = sub$beta_true[[1]],
      effect_name = sub$effect[[1]],
      converged = sub$converged,
      hessian_pd = sub$hessian_pd,
      hessian_condition = sub$hessian_condition,
      loglik = sub$loglik,
      estimator = est,
      target_comparable = comparable,
      hessian_condition_max = hessian_condition_max
    )
    cbind(
      scenario_id = sub$scenario_id[[1]],
      cell_class = sub$cell_class[[1]],
      scale = sub$scale[[1]],
      outcome = sub$outcome[[1]],
      effect = sub$effect[[1]],
      kernel = sub$kernel[[1]],
      serial_dependence = sub$serial_dependence[[1]],
      depletion = sub$depletion[[1]],
      covid_shock = sub$covid_shock[[1]],
      overdispersion = sub$overdispersion[[1]],
      estimator = est,
      target_mapping = sub$target_mapping[[1]],
      met,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, out)
}

#' Summarise all scenarios in a raw metrics table.
md_summarise_raw_metrics <- function(raw_all,
                                     hessian_condition_max = MD_HESSIAN_CONDITION_MAX) {
  if (!nrow(raw_all)) return(raw_all)
  parts <- lapply(split(raw_all, raw_all$scenario_id), function(raw_sc) {
    md_summarise_scenario_raw(raw_sc, hessian_condition_max = hessian_condition_max)
  })
  out <- do.call(rbind, parts)
  rownames(out) <- NULL
  out$data_status <- MD_PROVENANCE_SYNTHETIC
  out
}

#' Evaluate admission gates with worst-cell / all-cell rules (F1.2).
#'
#' Averages are not used for pass/fail. Failing scenario IDs are reported in
#' detail. Decision remains FAIL unless every criterion passes.
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

  md <- metric_rows[as.character(metric_rows$estimator) == "md", , drop = FALSE]
  if (!nrow(md)) {
    return(data.frame(
      gate_id = "all",
      value = NA_real_,
      threshold = NA_real_,
      passed = FALSE,
      detail = "no md metric rows",
      failing_scenario_ids = NA_character_,
      all_passed = FALSE,
      admission_decision = "FAIL_METHODS_FEASIBILITY_ONLY",
      data_status = MD_PROVENANCE_SYNTHETIC,
      stringsAsFactors = FALSE
    ))
  }

  core <- md[is.na(md$cell_class) | md$cell_class == "core", , drop = FALSE]
  if (!nrow(core)) core <- md

  # 1) Minimum convergence across core cells
  conv_min <- min(core$convergence_rate, na.rm = TRUE)
  conv_fail <- core$scenario_id[
    !is.finite(core$convergence_rate) |
      core$convergence_rate < g$convergence_min
  ]

  # 2) Every null core cell Type I in [type1_min, type1_max]
  null_rows <- core[core$effect_name == "null" | core$effect == "null", , drop = FALSE]
  type1_min_obs <- if (nrow(null_rows)) min(null_rows$type1, na.rm = TRUE) else NA_real_
  type1_max_obs <- if (nrow(null_rows)) max(null_rows$type1, na.rm = TRUE) else NA_real_
  type1_fail <- if (nrow(null_rows)) {
    null_rows$scenario_id[
      !is.finite(null_rows$type1) |
        null_rows$type1 < g$type1_min |
        null_rows$type1 > g$type1_max
    ]
  } else {
    character(0)
  }
  type1_pass <- length(type1_fail) == 0L && nrow(null_rows) > 0L &&
    is.finite(type1_min_obs) && is.finite(type1_max_obs)

  # 3) Minimum core coverage
  cover_min <- min(core$coverage, na.rm = TRUE)
  cover_fail <- core$scenario_id[
    !is.finite(core$coverage) |
      core$coverage < g$coverage_min
  ]

  # 4) Maximum non-null relative bias
  nonnull <- core[!(core$effect_name == "null" | core$effect == "null"), , drop = FALSE]
  relb_max <- if (nrow(nonnull)) max(nonnull$relative_bias_abs, na.rm = TRUE) else NA_real_
  relb_fail <- if (nrow(nonnull)) {
    nonnull$scenario_id[
      !is.finite(nonnull$relative_bias_abs) |
        nonnull$relative_bias_abs > g$relative_bias_max
    ]
  } else character(0)

  # 5) Maximum moderate false-sign
  mod <- core[core$effect_name == "moderate" | core$effect == "moderate", , drop = FALSE]
  fsign_max <- if (nrow(mod)) max(mod$false_sign, na.rm = TRUE) else NA_real_
  fsign_fail <- if (nrow(mod)) {
    mod$scenario_id[
      !is.finite(mod$false_sign) | mod$false_sign > g$false_sign_max
    ]
  } else character(0)

  # 6) Maximum core median Hessian condition
  cond_max <- max(core$hessian_condition_median, na.rm = TRUE)
  cond_fail <- core$scenario_id[
    !is.finite(core$hessian_condition_median) |
      core$hessian_condition_median >= g$hessian_condition_max
  ]

  # 7) Maximum core divergence
  div_max <- max(core$divergent_or_boundary_rate, na.rm = TRUE)
  div_fail <- core$scenario_id[
    !is.finite(core$divergent_or_boundary_rate) |
      core$divergent_or_boundary_rate >= g$divergent_fit_max
  ]

  # 8) Minimum coverage among explicit stress cells
  stress <- md_stress_metric_rows(md)
  stress_cover_min <- if (nrow(stress)) min(stress$coverage, na.rm = TRUE) else NA_real_
  stress_fail <- if (nrow(stress)) {
    stress$scenario_id[
      !is.finite(stress$coverage) | stress$coverage < g$stress_coverage_min
    ]
  } else character(0)

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
    value = c(
      conv_min, type1_max_obs, cover_min, relb_max, fsign_max,
      cond_max, div_max, stress_cover_min
    ),
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
      is.finite(conv_min) && conv_min >= g$convergence_min &&
        length(conv_fail) == 0L,
      type1_pass,
      is.finite(cover_min) && cover_min >= g$coverage_min &&
        length(cover_fail) == 0L,
      is.finite(relb_max) && relb_max <= g$relative_bias_max &&
        length(relb_fail) == 0L,
      is.finite(fsign_max) && fsign_max <= g$false_sign_max &&
        length(fsign_fail) == 0L,
      is.finite(cond_max) && cond_max < g$hessian_condition_max &&
        length(cond_fail) == 0L,
      is.finite(div_max) && div_max < g$divergent_fit_max &&
        length(div_fail) == 0L,
      is.finite(stress_cover_min) &&
        stress_cover_min >= g$stress_coverage_min &&
        length(stress_fail) == 0L
    ),
    detail = c(
      sprintf(
        "min_core_convergence=%.4f (need >=%.2f); failing=%s",
        conv_min, g$convergence_min, .md_failing_ids(conv_fail)
      ),
      sprintf(
        "null_type1 min=%.4f max=%.4f (need [%.2f, %.2f]); failing=%s",
        type1_min_obs, type1_max_obs, g$type1_min, g$type1_max,
        .md_failing_ids(type1_fail)
      ),
      sprintf(
        "min_core_coverage=%.4f (need >=%.2f); failing=%s",
        cover_min, g$coverage_min, .md_failing_ids(cover_fail)
      ),
      sprintf(
        "max_nonnull_abs_rel_bias=%.4f (need <=%.2f); failing=%s",
        relb_max, g$relative_bias_max, .md_failing_ids(relb_fail)
      ),
      sprintf(
        "max_moderate_false_sign=%.4f (need <=%.2f); failing=%s",
        fsign_max, g$false_sign_max, .md_failing_ids(fsign_fail)
      ),
      sprintf(
        "max_core_hessian_cond_median=%.3g (need <%.3g); failing=%s",
        cond_max, g$hessian_condition_max, .md_failing_ids(cond_fail)
      ),
      sprintf(
        "max_core_divergent_rate=%.4f (need <%.2f); failing=%s",
        div_max, g$divergent_fit_max, .md_failing_ids(div_fail)
      ),
      sprintf(
        "min_stress_coverage=%.4f (need >=%.2f; stress=AR-on core + EDGE_depletion/covid/stress); failing=%s",
        stress_cover_min, g$stress_coverage_min, .md_failing_ids(stress_fail)
      )
    ),
    failing_scenario_ids = c(
      .md_failing_ids(conv_fail),
      .md_failing_ids(type1_fail),
      .md_failing_ids(cover_fail),
      .md_failing_ids(relb_fail),
      .md_failing_ids(fsign_fail),
      .md_failing_ids(cond_fail),
      .md_failing_ids(div_fail),
      .md_failing_ids(stress_fail)
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
  # Extra diagnostic columns for reports (not used for gaming)
  checks$type1_min_obs <- type1_min_obs
  checks$type1_max_obs <- type1_max_obs
  checks
}

#' Build a concise F1.1 raw / F1.2 decision report from summary + gates.
md_format_f12_decision_report <- function(summary_df,
                                          gates_df,
                                          raw_note = "F1.1 500-rep raw metrics (untouched)") {
  md <- summary_df[as.character(summary_df$estimator) == "md", , drop = FALSE]
  core <- md[md$cell_class == "core", , drop = FALSE]
  null_rows <- core[core$effect == "null" | core$effect_name == "null", , drop = FALSE]
  decision <- unique(as.character(gates_df$admission_decision))
  lines <- c(
    "# M|D calibration F1.2 decision report",
    "",
    paste0("- Raw source: ", raw_note),
    paste0("- Protocol amendment: F1.2 (worst-cell gates; admissible M|D; comparator noncomparability)"),
    paste0("- Admission decision: ", paste(decision, collapse = ", ")),
    paste0("- All gates passed: ", all(gates_df$passed)),
    paste0("- Provenance: ", MD_PROVENANCE_SYNTHETIC),
    "",
    "## Gate table",
    "",
    paste0(
      "| ", paste(c("gate_id", "passed", "value", "detail"), collapse = " | "), " |"
    ),
    paste0("| ", paste(rep("---", 4), collapse = " | "), " |")
  )
  for (i in seq_len(nrow(gates_df))) {
    lines <- c(lines, sprintf(
      "| %s | %s | %s | %s |",
      gates_df$gate_id[[i]],
      gates_df$passed[[i]],
      format(gates_df$value[[i]], digits = 4),
      gsub("\\|", "/", gates_df$detail[[i]])
    ))
  }
  lines <- c(lines, "", "## Per-cell null Type I and coverage (M|D core)", "")
  if (nrow(null_rows)) {
    lines <- c(
      lines,
      "| scenario_id | outcome | kernel | AR | type1 | coverage |",
      "| --- | --- | --- | --- | --- | --- |"
    )
    for (i in seq_len(nrow(null_rows))) {
      lines <- c(lines, sprintf(
        "| %s | %s | %s | %s | %.4f | %.4f |",
        null_rows$scenario_id[[i]],
        null_rows$outcome[[i]],
        null_rows$kernel[[i]],
        null_rows$serial_dependence[[i]],
        null_rows$type1[[i]],
        null_rows$coverage[[i]]
      ))
    }
    lines <- c(
      lines,
      "",
      sprintf(
        "Null Type I range: CHD/HF pooled min=%.4f max=%.4f",
        min(null_rows$type1, na.rm = TRUE),
        max(null_rows$type1, na.rm = TRUE)
      ),
      sprintf(
        "Null coverage range: min=%.4f max=%.4f",
        min(null_rows$coverage, na.rm = TRUE),
        max(null_rows$coverage, na.rm = TRUE)
      )
    )
  } else {
    lines <- c(lines, "_No null core M|D rows in summary._")
  }
  nonnull <- core[!(core$effect == "null" | core$effect_name == "null"), , drop = FALSE]
  mod <- core[core$effect == "moderate" | core$effect_name == "moderate", , drop = FALSE]
  lines <- c(
    lines,
    "",
    "## Binding non-null diagnostics (core M|D)",
    "",
    sprintf(
      "- Max abs relative bias (non-null): %.4f",
      if (nrow(nonnull)) max(nonnull$relative_bias_abs, na.rm = TRUE) else NA_real_
    ),
    sprintf(
      "- Max false-sign (moderate): %.4f",
      if (nrow(mod)) max(mod$false_sign, na.rm = TRUE) else NA_real_
    ),
    "",
    "Final decision must remain methods-feasibility only unless every F1.2 gate passes.",
    ""
  )
  lines
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
