# final_model_helpers.R
# Reusable monthly model-ensemble helpers for the 10 Aug 2026 final protocol.
# Sourced by scripts 36–37 and by tests/test_final_model_helpers.R.
# Do not run directly. Never writes governed health inputs.

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(x, y) {
    if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
  }
}

if (!exists("validate_required_columns", mode = "function")) {
  validate_required_columns <- function(df, required, context = "input") {
    missing <- setdiff(required, names(df))
    if (length(missing)) {
      stop(context, " missing required columns: ", paste(missing, collapse = ", "))
    }
    invisible(TRUE)
  }
}

REAL_PROVENANCE <- "HA_APPROVED_AGGREGATE"
SYNTHETIC_PROVENANCE <- "SYNTHETIC_CALIBRATION"
RESULT_CLASS_EXPLORATORY <- "EXPLORATORY_POST_OUTCOME"
STUDY_N_MONTHS <- 132L

SE_METHODS_LADDER <- c("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")

CONTROL_TERM_MAP <- list(
  calendar_month_factor = "month_f",
  ns_time_df3 = "splines::ns(time_index, df = 3)",
  ns_time_df4 = "splines::ns(time_index, df = 4)",
  ns_time_df6 = "splines::ns(time_index, df = 6)",
  year_factor = "year_f",
  covid_phase = "covid_phase_f",
  absolute_humidity = "absolute_humidity",
  relative_humidity = "relative_humidity",
  rainfall = "rainfall",
  NO2 = "NO2",
  PM25 = "PM25",
  flu_indicator = "flu_indicator",
  O3 = "O3",
  frozen_exposure = NA_character_
)

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

load_final_model_registry <- function(path = NULL, root = NULL) {
  if (is.null(path)) {
    if (is.null(root)) {
      if (exists("project_root", mode = "function")) {
        root <- project_root()
      } else {
        root <- normalizePath(".", winslash = "/", mustWork = TRUE)
      }
    }
    path <- file.path(root, "analysis_plan", "final_model_registry.yml")
  }
  if (!requireNamespace("yaml", quietly = TRUE)) {
    stop("Package yaml is required to load final_model_registry.yml")
  }
  if (!file.exists(path)) stop("Missing final model registry: ", path)
  yaml::read_yaml(path)
}

core_exposure_specs <- function(registry = NULL) {
  if (is.null(registry)) registry <- load_final_model_registry()
  specs <- registry$core_exposures
  out <- lapply(names(specs), function(id) {
    s <- specs[[id]]
    list(
      pathway_id = id,
      variable = s$variable,
      contrast = as.numeric(s$contrast),
      unit = s$unit,
      pole = s$pole
    )
  })
  names(out) <- names(specs)
  out
}

scenario_defs <- function(registry = NULL) {
  if (is.null(registry)) registry <- load_final_model_registry()
  sc <- registry$robustness_scenarios
  out <- lapply(sc, function(s) s)
  names(out) <- vapply(sc, function(s) s$scenario_id, character(1))
  out
}

control_terms_from_registry <- function(controls, exposure_term = NULL) {
  terms <- character(0)
  for (nm in controls) {
    if (identical(nm, "frozen_exposure")) {
      if (is.null(exposure_term) || !nzchar(exposure_term)) {
        stop("frozen_exposure control requires exposure_term")
      }
      terms <- c(terms, exposure_term)
      next
    }
    mapped <- CONTROL_TERM_MAP[[nm]]
    if (is.null(mapped) || is.na(mapped)) {
      stop("Unknown registry control: ", nm)
    }
    terms <- c(terms, mapped)
  }
  unique(terms)
}

exposure_term_name <- function(variable, contrast = 1) {
  contrast <- as.numeric(contrast)
  if (!is.finite(contrast) || contrast <= 0) {
    stop("contrast must be a positive finite number")
  }
  if (isTRUE(all.equal(contrast, 1))) {
    as.character(variable)
  } else {
    # glm drops spaces inside I(); keep the same convention as scripts 31/32.
    sprintf("I(%s/%s)", variable, format(contrast, scientific = FALSE, trim = TRUE))
  }
}

offset_rhs_for <- function(offset_policy = "days_only") {
  if (identical(offset_policy, "days_only")) return("offset(offset_log_days)")
  if (identical(offset_policy, "population_x_days")) return("offset(offset_log)")
  if (identical(offset_policy, "none")) return(NULL)
  stop("Unknown offset_policy: ", offset_policy)
}

build_count_formula <- function(exposure_term, controls, offset_policy = "days_only",
                                response = "n_events") {
  rhs <- c(exposure_term, controls, offset_rhs_for(offset_policy))
  rhs <- rhs[!is.na(rhs) & nzchar(rhs)]
  stats::as.formula(paste(response, "~", paste(rhs, collapse = " + ")))
}

# ---------------------------------------------------------------------------
# Panel preparation / validation
# ---------------------------------------------------------------------------

.panel_required_columns <- function() {
  c(
    "month_id", "year", "month", "time_index", "n_events", "data_status",
    "days_in_month", "mean_temp", "mean_tmax", "mean_tmin",
    "hot_nights", "cold_days", "very_hot_days"
  )
}

prepare_analysis_panel <- function(dat, require_real = TRUE, outcome = NA_character_) {
  if (!is.data.frame(dat)) stop("dat must be a data.frame")
  validate_required_columns(dat, .panel_required_columns(), "analysis panel")
  out <- dat
  out <- out[order(out$time_index, out$month_id), , drop = FALSE]
  if (!"population" %in% names(out)) out$population <- NA_real_
  if (!"offset_log_days" %in% names(out)) {
    out$offset_log_days <- log(pmax(as.numeric(out$days_in_month), 1))
  }
  if (!"offset_log" %in% names(out)) {
    pop <- as.numeric(out$population)
    if (all(is.na(pop))) {
      # Never silently reinterpret a requested population offset as days-only.
      out$offset_log <- NA_real_
    } else {
      out$offset_log <- log(pmax(pop, 1) * pmax(as.numeric(out$days_in_month), 1))
    }
  }
  out$month_f <- factor(out$month)
  out$year_f <- factor(out$year)
  if ("covid_phase" %in% names(out)) {
    out$covid_phase_f <- factor(out$covid_phase)
  }
  if (!is.na(outcome) && nzchar(outcome)) out$analysis_outcome <- outcome
  validate_analysis_panel(out, require_real = require_real)
  out
}

validate_analysis_panel <- function(dat, require_real = TRUE) {
  if (nrow(dat) != STUDY_N_MONTHS) {
    stop(
      "Panel must contain exactly ", STUDY_N_MONTHS, " rows; found ", nrow(dat)
    )
  }
  statuses <- unique(as.character(dat$data_status))
  if (isTRUE(require_real)) {
    if (!identical(statuses, REAL_PROVENANCE)) {
      stop(
        "require_real=TRUE needs uniform ", REAL_PROVENANCE,
        "; found: ", paste(statuses, collapse = ",")
      )
    }
  } else {
    if (REAL_PROVENANCE %in% statuses && SYNTHETIC_PROVENANCE %in% statuses) {
      stop("Mixed real and synthetic provenance in one panel is forbidden")
    }
    if (!all(statuses %in% c(REAL_PROVENANCE, SYNTHETIC_PROVENANCE, "SYNTHETIC"))) {
      stop("Unexpected data_status values: ", paste(statuses, collapse = ","))
    }
  }
  if (anyDuplicated(dat$month_id)) stop("Duplicate month_id in panel")
  invisible(TRUE)
}

panel_provenance_label <- function(dat) {
  statuses <- unique(as.character(dat$data_status))
  if (identical(statuses, REAL_PROVENANCE)) return(REAL_PROVENANCE)
  if (all(statuses %in% c(SYNTHETIC_PROVENANCE, "SYNTHETIC"))) {
    return(SYNTHETIC_PROVENANCE)
  }
  paste(statuses, collapse = ",")
}

# ---------------------------------------------------------------------------
# SE ladder / extraction
# ---------------------------------------------------------------------------

vcov_for_method <- function(model, method) {
  if (identical(method, "model")) return(stats::vcov(model))
  if (!requireNamespace("sandwich", quietly = TRUE)) {
    stop("Package sandwich is required for robust variance ", method)
  }
  if (identical(method, "HC1")) {
    return(sandwich::vcovHC(model, type = "HC1"))
  }
  if (identical(method, "NeweyWest_lag3")) {
    return(sandwich::NeweyWest(model, lag = 3L, prewhite = FALSE, adjust = TRUE))
  }
  if (identical(method, "NeweyWest_lag6")) {
    return(sandwich::NeweyWest(model, lag = 6L, prewhite = FALSE, adjust = TRUE))
  }
  stop("Unknown SE method: ", method)
}

extract_coef_row <- function(model, term, vcov_mat, metadata = NULL) {
  cf <- stats::coef(model)
  if (!term %in% names(cf)) {
    return(NULL)
  }
  b <- unname(cf[[term]])
  se_vec <- sqrt(diag(vcov_mat))
  if (!term %in% names(se_vec)) return(NULL)
  se <- unname(se_vec[[term]])
  if (!is.finite(se) || se < 0) return(NULL)
  z <- b / se
  row <- data.frame(
    term = term,
    estimate = b,
    std_error = se,
    statistic = z,
    p_value = 2 * stats::pnorm(abs(z), lower.tail = FALSE),
    rr = exp(b),
    rr_low = exp(b - 1.96 * se),
    rr_high = exp(b + 1.96 * se),
    stringsAsFactors = FALSE
  )
  if (!is.null(metadata)) row <- cbind(metadata, row)
  row
}

empty_fit_status <- function(...) {
  dots <- list(...)
  base <- data.frame(
    status = NA_character_,
    message = NA_character_,
    converged = NA,
    aic = NA_real_,
    theta = NA_real_,
    residual_acf1 = NA_real_,
    n_months = NA_integer_,
    stringsAsFactors = FALSE
  )
  if (length(dots)) {
    meta <- as.data.frame(dots, stringsAsFactors = FALSE)
    cbind(meta, base)
  } else {
    base
  }
}

status_row <- function(status, message = "", converged = NA, aic = NA_real_,
                       theta = NA_real_, residual_acf1 = NA_real_,
                       n_months = NA_integer_, ...) {
  meta <- list(...)
  row <- data.frame(
    status = as.character(status),
    message = as.character(message),
    converged = converged,
    aic = aic,
    theta = theta,
    residual_acf1 = residual_acf1,
    n_months = as.integer(n_months),
    stringsAsFactors = FALSE
  )
  if (length(meta)) {
    meta_df <- as.data.frame(meta, stringsAsFactors = FALSE)
    cbind(meta_df, row)
  } else {
    row
  }
}

residual_acf1 <- function(model) {
  res <- tryCatch(
    stats::residuals(model, type = "pearson"),
    error = function(e) NA_real_
  )
  if (length(res) < 2L || all(is.na(res))) return(NA_real_)
  as.numeric(stats::acf(res, plot = FALSE, lag.max = 1)$acf[2])
}

# ---------------------------------------------------------------------------
# Scenario transforms R01–R16
# ---------------------------------------------------------------------------

.season_months_for_pole <- function(pole, scenario) {
  restr <- scenario$restriction
  if (is.null(restr) || is.character(restr)) return(NULL)
  heat_m <- as.integer(restr$heat)
  cold_m <- as.integer(restr$cold)
  if (identical(pole, "cold")) return(cold_m)
  # heat and continuous temperature exposures use the warm-season window
  heat_m
}

apply_scenario <- function(dat, scenario, pathway_id, exposure_spec,
                           registry = NULL) {
  if (is.null(registry)) registry <- load_final_model_registry()
  scenario_id <- scenario$scenario_id
  variable <- exposure_spec$variable
  contrast <- exposure_spec$contrast
  pole <- exposure_spec$pole

  applies_to <- scenario$applies_to
  if (!is.null(applies_to) && length(applies_to) && !pathway_id %in% applies_to) {
    return(list(
      ok = FALSE,
      skip = TRUE,
      status = "SKIPPED",
      message = paste0(
        scenario_id, " applies only to ", paste(applies_to, collapse = ","),
        "; skipped for ", pathway_id
      ),
      data = NULL,
      exposure_term = NA_character_,
      controls = character(0)
    ))
  }

  d <- dat
  exposure_col <- variable
  controls <- control_terms_from_registry(scenario$controls)

  transform <- scenario$transform %||% NULL
  if (!is.null(transform) && identical(transform, "calendar_month_anomaly")) {
    cal_mean <- stats::ave(d[[variable]], d$month, FUN = function(x) mean(x, na.rm = TRUE))
    anom_name <- paste0(variable, "_month_anomaly")
    d[[anom_name]] <- d[[variable]] - cal_mean
    exposure_col <- anom_name
  }
  if (!is.null(transform) && identical(transform, "lead_1")) {
    lead_name <- paste0(variable, "_lead1")
    d[[lead_name]] <- dplyr::lead(d[[variable]], 1L)
    d <- d[!is.na(d[[lead_name]]), , drop = FALSE]
    exposure_col <- lead_name
  }
  if (!is.null(transform) && identical(transform, "lead_2")) {
    lead_name <- paste0(variable, "_lead2")
    d[[lead_name]] <- dplyr::lead(d[[variable]], 2L)
    d <- d[!is.na(d[[lead_name]]), , drop = FALSE]
    exposure_col <- lead_name
  }

  restr <- scenario$restriction
  if (!is.null(restr)) {
    if (is.character(restr) && identical(restr, "year < 2020")) {
      d <- d[d$year < 2020, , drop = FALSE]
    } else if (is.list(restr)) {
      months_keep <- .season_months_for_pole(pole, scenario)
      d <- d[d$month %in% months_keep, , drop = FALSE]
      # season restriction drops calendar-month FE when not in controls
    }
  }

  if (identical(scenario_id, "R12_influenza_cold")) {
    if (!"flu_indicator" %in% names(d)) {
      return(list(
        ok = FALSE, skip = FALSE, status = "FAILED",
        message = "flu_indicator column missing",
        data = NULL, exposure_term = NA_character_, controls = controls
      ))
    }
    d <- d[stats::complete.cases(d[, c(exposure_col, "flu_indicator"), drop = FALSE]), , drop = FALSE]
  }

  if (identical(scenario_id, "R14_exclude_max_cooks")) {
    base_term <- exposure_term_name(variable, contrast)
    base_controls <- control_terms_from_registry(c("calendar_month_factor", "ns_time_df4"))
    base_fit <- tryCatch(
      {
        fml <- build_count_formula(base_term, base_controls, "days_only")
        MASS::glm.nb(fml, data = dat)
      },
      error = function(e) e
    )
    if (inherits(base_fit, "error")) {
      return(list(
        ok = FALSE, skip = FALSE, status = "FAILED",
        message = paste0("R14 baseline Cook fit failed: ", conditionMessage(base_fit)),
        data = NULL, exposure_term = NA_character_, controls = controls
      ))
    }
    cooks <- stats::cooks.distance(base_fit)
    if (!length(cooks) || all(is.na(cooks))) {
      return(list(
        ok = FALSE, skip = FALSE, status = "FAILED",
        message = "R14 could not compute Cook's distance",
        data = NULL, exposure_term = NA_character_, controls = controls
      ))
    }
    drop_idx <- which.max(cooks)
    d <- dat[-drop_idx, , drop = FALSE]
    exposure_col <- variable
  }

  # Covariate completeness for staged confounders
  ctrl_vars <- character(0)
  if ("covid_phase_f" %in% controls) ctrl_vars <- c(ctrl_vars, "covid_phase_f")
  if ("absolute_humidity" %in% controls) ctrl_vars <- c(ctrl_vars, "absolute_humidity")
  if ("NO2" %in% controls) ctrl_vars <- c(ctrl_vars, "NO2")
  if ("PM25" %in% controls) ctrl_vars <- c(ctrl_vars, "PM25")
  if ("O3" %in% controls) ctrl_vars <- c(ctrl_vars, "O3")
  if ("flu_indicator" %in% controls) ctrl_vars <- c(ctrl_vars, "flu_indicator")
  if (length(ctrl_vars)) {
    miss_cols <- setdiff(ctrl_vars, names(d))
    if (length(miss_cols)) {
      return(list(
        ok = FALSE, skip = FALSE, status = "FAILED",
        message = paste0("Missing covariate columns: ", paste(miss_cols, collapse = ",")),
        data = NULL, exposure_term = NA_character_, controls = controls
      ))
    }
    keep <- stats::complete.cases(d[, c(exposure_col, ctrl_vars), drop = FALSE])
    d <- d[keep, , drop = FALSE]
  }

  if (nrow(d) < 24L) {
    return(list(
      ok = FALSE, skip = FALSE, status = "FAILED",
      message = paste0("Insufficient rows after scenario filters: n=", nrow(d)),
      data = NULL, exposure_term = NA_character_, controls = controls
    ))
  }

  # refresh factors on filtered data
  d$month_f <- factor(d$month)
  d$year_f <- factor(d$year)
  if ("covid_phase" %in% names(d)) d$covid_phase_f <- factor(d$covid_phase)

  list(
    ok = TRUE,
    skip = FALSE,
    status = "OK",
    message = "",
    data = d,
    exposure_term = exposure_term_name(exposure_col, contrast),
    exposure_col = exposure_col,
    controls = controls
  )
}

# ---------------------------------------------------------------------------
# NB fit with SE ladder
# ---------------------------------------------------------------------------

fit_nb_se_ladder <- function(dat, exposure_term, controls,
                             offset_policy = "days_only",
                             se_methods = SE_METHODS_LADDER,
                             metadata = NULL) {
  fml <- build_count_formula(exposure_term, controls, offset_policy)
  model <- tryCatch(
    MASS::glm.nb(fml, data = dat),
    error = function(e) e
  )
  if (inherits(model, "error")) {
    st <- status_row(
      "FAILED", conditionMessage(model),
      n_months = nrow(dat)
    )
    if (!is.null(metadata)) st <- cbind(as.data.frame(metadata, stringsAsFactors = FALSE), st)
    return(list(ok = FALSE, model = NULL, estimates = NULL, status = st))
  }

  acf1 <- residual_acf1(model)
  aic <- tryCatch(stats::AIC(model), error = function(e) NA_real_)
  theta <- tryCatch(unname(model$theta), error = function(e) NA_real_)
  conv <- tryCatch(isTRUE(model$converged), error = function(e) NA)

  est_rows <- list()
  se_messages <- character(0)
  for (method in se_methods) {
    vm <- tryCatch(vcov_for_method(model, method), error = function(e) e)
    if (inherits(vm, "error")) {
      se_messages <- c(se_messages, paste0(method, ": ", conditionMessage(vm)))
      next
    }
    meta <- metadata
    if (!is.null(meta)) {
      meta <- as.data.frame(meta, stringsAsFactors = FALSE)
      meta$se_method <- method
      meta$offset_policy <- offset_policy
      meta$family <- "negative_binomial"
    } else {
      meta <- data.frame(
        se_method = method,
        offset_policy = offset_policy,
        family = "negative_binomial",
        stringsAsFactors = FALSE
      )
    }
    row <- extract_coef_row(model, exposure_term, vm, meta)
    if (is.null(row)) {
      se_messages <- c(se_messages, paste0(method, ": term not found (", exposure_term, ")"))
    } else {
      est_rows[[method]] <- row
    }
  }

  msg <- if (length(est_rows)) {
    if (length(se_messages)) paste(se_messages, collapse = " | ") else ""
  } else {
    paste0("No SE ladder rows extracted. ", paste(se_messages, collapse = " | "))
  }
  st <- status_row(
    if (length(est_rows)) "OK" else "FAILED",
    msg,
    converged = conv,
    aic = aic,
    theta = theta,
    residual_acf1 = acf1,
    n_months = nrow(dat)
  )
  if (!is.null(metadata)) {
    st <- cbind(as.data.frame(metadata, stringsAsFactors = FALSE), st)
  }

  list(
    ok = length(est_rows) > 0,
    model = model,
    estimates = if (length(est_rows)) dplyr::bind_rows(est_rows) else NULL,
    status = st
  )
}

fit_scenario_nb <- function(dat, pathway_id, exposure_spec, scenario,
                            registry = NULL,
                            offset_policy = "days_only",
                            model_id = "M01_NB_MONTH_NW6",
                            result_class = RESULT_CLASS_EXPLORATORY,
                            data_status = NULL) {
  if (is.null(registry)) registry <- load_final_model_registry()
  if (is.null(data_status)) data_status <- panel_provenance_label(dat)

  meta_base <- list(
    outcome = dat$analysis_outcome[[1]] %||% NA_character_,
    pathway_id = pathway_id,
    exposure = exposure_spec$variable,
    contrast = exposure_spec$contrast,
    scenario_id = scenario$scenario_id,
    model_id = model_id,
    result_class = result_class,
    data_status = data_status
  )

  prep <- apply_scenario(dat, scenario, pathway_id, exposure_spec, registry)
  if (!isTRUE(prep$ok)) {
    st <- status_row(
      prep$status, prep$message,
      n_months = if (!is.null(prep$data)) nrow(prep$data) else NA_integer_,
      outcome = meta_base$outcome,
      pathway_id = pathway_id,
      exposure = exposure_spec$variable,
      contrast = exposure_spec$contrast,
      scenario_id = scenario$scenario_id,
      model_id = model_id,
      result_class = result_class,
      data_status = data_status
    )
    return(list(ok = FALSE, estimates = NULL, status = st, model = NULL))
  }

  fit_nb_se_ladder(
    prep$data,
    prep$exposure_term,
    prep$controls,
    offset_policy = offset_policy,
    metadata = meta_base
  )
}

# ---------------------------------------------------------------------------
# GLARMA (negative binomial) with frozen AR/MA candidates
# ---------------------------------------------------------------------------

.glarma_design_matrix <- function(dat, exposure_term, controls) {
  # Build a numeric model matrix with intercept; glarma takes y and X separately.
  rhs <- c(exposure_term, controls)
  fml <- stats::as.formula(paste("~", paste(rhs, collapse = " + ")))
  X <- stats::model.matrix(fml, data = dat)
  list(X = X, terms = colnames(X))
}

.pit_uniformity_score <- function(y, mu, theta) {
  # Deterministic mid-PIT uniformity: mean absolute deviation of sorted PIT
  # from a Uniform grid. Lower is better. Avoids stochastic model selection.
  if (length(y) < 5L || !is.finite(theta) || theta <= 0) return(Inf)
  F_ym1 <- stats::pnbinom(pmax(y - 1L, 0L), mu = mu, size = theta)
  F_y <- stats::pnbinom(y, mu = mu, size = theta)
  pit <- (F_ym1 + F_y) / 2
  pit <- pmin(pmax(pit, 0), 1)
  grid <- stats::ppoints(length(pit))
  mean(abs(sort(pit) - grid))
}

fit_glarma_negbin_candidate <- function(dat, exposure_term, controls,
                                        offset_policy = "days_only",
                                        phi_lags = NULL,
                                        theta_lags = NULL,
                                        model_id = NA_character_) {
  if (!requireNamespace("glarma", quietly = TRUE)) {
    return(list(
      ok = FALSE,
      model = NULL,
      estimate = NULL,
      diagnostics = data.frame(
        model_id = model_id,
        status = "FAILED",
        message = "Package glarma is not available",
        aic = NA_real_,
        pit_uniformity = NA_real_,
        residual_acf1_absolute = NA_real_,
        stringsAsFactors = FALSE
      )
    ))
  }

  off <- NULL
  if (identical(offset_policy, "days_only")) {
    off <- dat$offset_log_days
  } else if (identical(offset_policy, "population_x_days")) {
    off <- dat$offset_log
  } else if (!identical(offset_policy, "none")) {
    stop("Unknown offset_policy for glarma: ", offset_policy)
  }

  mm <- tryCatch(
    .glarma_design_matrix(dat, exposure_term, controls),
    error = function(e) e
  )
  if (inherits(mm, "error")) {
    return(list(
      ok = FALSE, model = NULL, estimate = NULL,
      diagnostics = data.frame(
        model_id = model_id, status = "FAILED",
        message = conditionMessage(mm),
        aic = NA_real_, pit_uniformity = NA_real_,
        residual_acf1_absolute = NA_real_,
        stringsAsFactors = FALSE
      )
    ))
  }

  y <- as.numeric(dat$n_events)
  args <- list(
    y = y,
    X = mm$X,
    type = "NegBin",
    method = "FS",
    residuals = "Pearson"
  )
  if (!is.null(off)) args$offset <- off
  if (!is.null(phi_lags) && length(phi_lags)) args$phiLags <- as.integer(phi_lags)
  if (!is.null(theta_lags) && length(theta_lags)) args$thetaLags <- as.integer(theta_lags)

  fit <- tryCatch(
    do.call(glarma::glarma, args),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    # Fallback: some glarma builds want type = "NegBin" with alpha start via glm.nb
    nb0 <- tryCatch({
      fml <- build_count_formula(exposure_term, controls, offset_policy)
      MASS::glm.nb(fml, data = dat)
    }, error = function(e2) e2)
    if (!inherits(nb0, "error")) {
      args$alpha <- unname(nb0$theta)
      fit <- tryCatch(do.call(glarma::glarma, args), error = function(e) e)
    }
  }
  if (inherits(fit, "error")) {
    return(list(
      ok = FALSE, model = NULL, estimate = NULL,
      diagnostics = data.frame(
        model_id = model_id, status = "FAILED",
        message = conditionMessage(fit),
        aic = NA_real_, pit_uniformity = NA_real_,
        residual_acf1_absolute = NA_real_,
        stringsAsFactors = FALSE
      )
    ))
  }

  coef_parts <- tryCatch(stats::coef(fit), error = function(e) NULL)
  beta <- if (!is.null(coef_parts) && !is.null(coef_parts$beta)) {
    coef_parts$beta
  } else {
    # Package fallback: first ncol(X) entries of delta are regression terms.
    raw_delta <- tryCatch(as.numeric(fit$delta), error = function(e) numeric())
    if (length(raw_delta) >= ncol(mm$X)) {
      setNames(raw_delta[seq_len(ncol(mm$X))], colnames(mm$X))
    } else {
      numeric()
    }
  }

  term <- exposure_term
  # model.matrix may alter I() names slightly; match flexibly
  if (!term %in% names(beta)) {
    hit <- grep(gsub("([()])", "\\\\\\1", term), names(beta))
    if (length(hit) == 1L) term <- names(beta)[hit]
  }

  aic <- tryCatch(as.numeric(fit$aic)[1], error = function(e) NA_real_)
  if (!length(aic) || !is.finite(aic)) aic <- NA_real_
  mu <- tryCatch(as.numeric(fitted(fit)), error = function(e) rep(NA_real_, length(y)))
  theta <- tryCatch(
    as.numeric(coef_parts$NB[["alpha"]]),
    error = function(e) NA_real_
  )
  if (!is.finite(theta)) {
    theta <- tryCatch(unname(MASS::glm.nb(
      build_count_formula(exposure_term, controls, offset_policy), data = dat
    )$theta), error = function(e) NA_real_)
  }
  pit <- .pit_uniformity_score(y, mu, theta)
  res <- tryCatch(as.numeric(residuals(fit)), error = function(e) NA_real_)
  acf1_abs <- if (length(res) > 1L && all(is.finite(res))) {
    abs(as.numeric(stats::acf(res, plot = FALSE, lag.max = 1)$acf[2]))
  } else {
    Inf
  }

  est <- NULL
  if (term %in% names(beta) && is.finite(beta[[term]])) {
    # Prefer model-based SE from glarma summary when available; never select by p.
    se <- tryCatch({
      s <- summary(fit)
      cm <- s$coefficients1
      if (is.null(cm) || !term %in% rownames(cm)) {
        NA_real_
      } else {
        se_col <- intersect(colnames(cm), c("Std. Error", "Std.Error", "SE", "se"))
        if (!length(se_col)) NA_real_ else unname(cm[term, se_col[[1]]])
      }
    }, error = function(e) NA_real_)
    b <- unname(beta[[term]])
    est <- data.frame(
      term = term,
      estimate = b,
      std_error = se,
      statistic = if (is.finite(se) && se > 0) b / se else NA_real_,
      p_value = if (is.finite(se) && se > 0) {
        2 * stats::pnorm(abs(b / se), lower.tail = FALSE)
      } else {
        NA_real_
      },
      rr = exp(b),
      rr_low = if (is.finite(se)) exp(b - 1.96 * se) else NA_real_,
      rr_high = if (is.finite(se)) exp(b + 1.96 * se) else NA_real_,
      stringsAsFactors = FALSE
    )
  }

  list(
    ok = !is.null(est),
    model = fit,
    estimate = est,
    diagnostics = data.frame(
      model_id = model_id,
      status = if (!is.null(est)) "OK" else "FAILED",
      message = if (!is.null(est)) "" else paste0("Exposure term not in glarma coefs: ", exposure_term),
      aic = aic,
      pit_uniformity = pit,
      residual_acf1_absolute = acf1_abs,
      stringsAsFactors = FALSE
    )
  )
}

select_glarma_by_diagnostics <- function(candidate_results) {
  # Rank by AIC, then PIT uniformity, then |ACF1|. Never by exposure p-value.
  ok <- vapply(candidate_results, function(x) isTRUE(x$ok), logical(1))
  if (!any(ok)) {
    return(list(
      selected = NULL,
      diagnostics = dplyr::bind_rows(lapply(candidate_results, `[[`, "diagnostics")),
      status = "FAILED",
      message = "No GLARMA candidate converged"
    ))
  }
  diags <- dplyr::bind_rows(lapply(candidate_results, `[[`, "diagnostics"))
  diags$rank_aic <- rank(diags$aic, ties.method = "min", na.last = TRUE)
  diags$rank_pit <- rank(diags$pit_uniformity, ties.method = "min", na.last = TRUE)
  diags$rank_acf <- rank(diags$residual_acf1_absolute, ties.method = "min", na.last = TRUE)
  diags$rank_sum <- diags$rank_aic + diags$rank_pit + diags$rank_acf
  # only OK rows compete
  diags$rank_sum[diags$status != "OK"] <- Inf
  pick <- which.min(diags$rank_sum)
  list(
    selected = candidate_results[[pick]],
    diagnostics = diags,
    status = "OK",
    message = paste0("Selected ", diags$model_id[[pick]], " by AIC/PIT/ACF ranks")
  )
}

fit_nb_glarma_ensemble <- function(dat, exposure_term, controls,
                                   offset_policy = "days_only",
                                   metadata = NULL) {
  candidates <- list(
    M02_GLARMA_AR1 = list(phi = 1L, theta = NULL),
    M03_GLARMA_MA1 = list(phi = NULL, theta = 1L),
    M04_GLARMA_ARMA11 = list(phi = 1L, theta = 1L)
  )
  fits <- lapply(names(candidates), function(mid) {
    cfg <- candidates[[mid]]
    fit_glarma_negbin_candidate(
      dat, exposure_term, controls, offset_policy,
      phi_lags = cfg$phi, theta_lags = cfg$theta, model_id = mid
    )
  })
  names(fits) <- names(candidates)
  sel <- select_glarma_by_diagnostics(fits)

  est <- NULL
  if (!is.null(sel$selected) && !is.null(sel$selected$estimate)) {
    est <- sel$selected$estimate
    if (!is.null(metadata)) {
      meta <- as.data.frame(metadata, stringsAsFactors = FALSE)
      meta$model_id <- sel$selected$diagnostics$model_id[[1]]
      meta$family <- "negative_binomial_glarma"
      meta$offset_policy <- offset_policy
      meta$se_method <- "glarma_model"
      est <- cbind(meta, est)
    }
  }

  st_meta <- if (is.null(metadata)) list() else as.list(metadata)
  st <- do.call(status_row, c(
    list(
      status = sel$status,
      message = sel$message,
      aic = if (!is.null(sel$selected)) sel$selected$diagnostics$aic[[1]] else NA_real_,
      residual_acf1 = if (!is.null(sel$selected)) {
        sel$selected$diagnostics$residual_acf1_absolute[[1]]
      } else {
        NA_real_
      },
      n_months = nrow(dat)
    ),
    st_meta
  ))

  list(
    ok = identical(sel$status, "OK"),
    estimates = est,
    status = st,
    diagnostics = sel$diagnostics,
    selected_model = if (!is.null(sel$selected)) sel$selected$model else NULL
  )
}

# ---------------------------------------------------------------------------
# Stacked CHD/HF hot-vs-cold interaction (quasi-Poisson, month-clustered)
# ---------------------------------------------------------------------------

fit_stacked_heat_cold_contrast <- function(chd_dat, hf_dat,
                                           heat_variable = "hot_nights",
                                           cold_variable = "cold_days",
                                           contrast_days = 5,
                                           offset_policy = "days_only",
                                           result_class = RESULT_CLASS_EXPLORATORY) {
  chd <- chd_dat
  hf <- hf_dat
  chd$outcome_f <- factor("chd", levels = c("chd", "hf"))
  hf$outcome_f <- factor("hf", levels = c("chd", "hf"))
  common <- intersect(names(chd), names(hf))
  stacked <- rbind(chd[common], hf[common])
  stacked <- stacked[order(stacked$month_id, stacked$outcome_f), , drop = FALSE]
  stacked$month_f <- factor(stacked$month)
  stacked$heat_x <- as.numeric(stacked[[heat_variable]]) / contrast_days
  stacked$cold_x <- as.numeric(stacked[[cold_variable]]) / contrast_days

  off <- offset_rhs_for(offset_policy)
  # Outcome-specific seasonality and trend; outcome-specific heat/cold slopes.
  rhs <- c(
    "0 + outcome_f:heat_x",
    "outcome_f:cold_x",
    "outcome_f:month_f",
    "outcome_f:splines::ns(time_index, df = 4)",
    off
  )
  fml <- stats::as.formula(paste("n_events ~", paste(rhs[!is.na(rhs)], collapse = " + ")))

  model <- tryCatch(
    stats::glm(fml, data = stacked, family = stats::quasipoisson()),
    error = function(e) e
  )
  if (inherits(model, "error")) {
    return(list(
      ok = FALSE,
      model = NULL,
      contrast = NULL,
      status = status_row(
        "FAILED", conditionMessage(model),
        model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
        result_class = result_class,
        data_status = panel_provenance_label(stacked),
        n_months = length(unique(stacked$month_id))
      )
    ))
  }

  cf <- stats::coef(model)
  # Expected names like outcome_fchd:heat_x
  nm_h_chd <- "outcome_fchd:heat_x"
  nm_c_chd <- "outcome_fchd:cold_x"
  nm_h_hf <- "outcome_fhf:heat_x"
  nm_c_hf <- "outcome_fhf:cold_x"
  need <- c(nm_h_chd, nm_c_chd, nm_h_hf, nm_c_hf)
  if (!all(need %in% names(cf))) {
    # Alternative naming from some R versions
    alt <- names(cf)
    find_one <- function(outcome, var) {
      hits <- alt[grepl(paste0(outcome, ".*", var), alt) | grepl(paste0(var, ".*", outcome), alt)]
      if (length(hits) == 1L) hits[[1]] else NA_character_
    }
    resolved <- c(
      find_one("chd", "heat_x"),
      find_one("chd", "cold_x"),
      find_one("hf", "heat_x"),
      find_one("hf", "cold_x")
    )
    if (anyNA(resolved) || anyDuplicated(resolved)) {
      missing <- need[!need %in% names(cf)]
      return(list(
        ok = FALSE, model = model, contrast = NULL,
        status = status_row(
          "FAILED",
          paste0("Missing stacked terms: ", paste(missing, collapse = ", "),
                 "; available: ", paste(names(cf), collapse = ", ")),
          model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
          result_class = result_class,
          data_status = panel_provenance_label(stacked),
          n_months = length(unique(stacked$month_id))
        )
      ))
    }
    nm_h_chd <- resolved[[1]]
    nm_c_chd <- resolved[[2]]
    nm_h_hf <- resolved[[3]]
    nm_c_hf <- resolved[[4]]
  }

  # Delta = (H_CHD - C_CHD) - (H_HF - C_HF)
  L <- setNames(rep(0, length(cf)), names(cf))
  L[[nm_h_chd]] <- 1
  L[[nm_c_chd]] <- -1
  L[[nm_h_hf]] <- -1
  L[[nm_c_hf]] <- 1
  delta <- sum(L * cf)

  vm <- tryCatch({
    if (!requireNamespace("sandwich", quietly = TRUE)) {
      stop("sandwich required for month-clustered covariance")
    }
    sandwich::vcovCL(model, cluster = stacked$month_id, type = "HC1")
  }, error = function(e) e)
  if (inherits(vm, "error")) {
    return(list(
      ok = FALSE, model = model, contrast = NULL,
      status = status_row(
        "FAILED", paste0("Clustered vcov failed: ", conditionMessage(vm)),
        model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
        result_class = result_class,
        data_status = panel_provenance_label(stacked),
        n_months = length(unique(stacked$month_id))
      )
    ))
  }

  se <- as.numeric(sqrt(as.numeric(t(L) %*% vm %*% L)))
  z <- delta / se
  contrast <- data.frame(
    model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
    contrast_id = "delta_heat_minus_cold_chd_vs_hf",
    estimate = delta,
    std_error = se,
    statistic = z,
    p_value = 2 * stats::pnorm(abs(z), lower.tail = FALSE),
    heat_chd = unname(cf[[nm_h_chd]]),
    cold_chd = unname(cf[[nm_c_chd]]),
    heat_hf = unname(cf[[nm_h_hf]]),
    cold_hf = unname(cf[[nm_c_hf]]),
    heat_variable = heat_variable,
    cold_variable = cold_variable,
    contrast_days = contrast_days,
    offset_policy = offset_policy,
    inference = "month_clustered_HC1",
    result_class = result_class,
    data_status = panel_provenance_label(stacked),
    n_months = length(unique(stacked$month_id)),
    stringsAsFactors = FALSE
  )

  list(
    ok = TRUE,
    model = model,
    contrast = contrast,
    status = status_row(
      "OK", "",
      converged = isTRUE(model$converged),
      model_id = "M06_STACKED_HEAT_COLD_INTERACTION",
      result_class = result_class,
      data_status = panel_provenance_label(stacked),
      n_months = length(unique(stacked$month_id))
    )
  )
}

# ---------------------------------------------------------------------------
# Predictive scoring (LOYO + rolling origin)
# ---------------------------------------------------------------------------

.nb_log_score <- function(y, mu, theta) {
  if (!is.finite(theta) || theta <= 0) return(rep(NA_real_, length(y)))
  stats::dnbinom(y, mu = pmax(mu, 1e-12), size = theta, log = TRUE)
}

.nb_unit_deviance <- function(y, mu, theta) {
  # Standard NB deviance contribution; saturated uses y for mu when y>0.
  mu <- pmax(mu, 1e-12)
  if (!is.finite(theta) || theta <= 0) return(rep(NA_real_, length(y)))
  term <- function(yy, mm) {
    ifelse(
      yy == 0,
      2 * theta * log((theta + mm) / theta),
      2 * (yy * log(pmax(yy, 1e-12) / mm) - (yy + theta) * log((yy + theta) / (mm + theta)))
    )
  }
  term(y, mu)
}

.predict_nb_mu <- function(model, newdata) {
  as.numeric(stats::predict(model, newdata = newdata, type = "response"))
}

.fit_nb_simple <- function(dat, exposure_term = NULL, controls,
                           offset_policy = "days_only") {
  if (is.null(exposure_term)) {
    rhs <- c(controls, offset_rhs_for(offset_policy))
    fml <- stats::as.formula(paste("n_events ~", paste(rhs[!is.na(rhs)], collapse = " + ")))
  } else {
    fml <- build_count_formula(exposure_term, controls, offset_policy)
  }
  MASS::glm.nb(fml, data = dat)
}

score_prediction_pair <- function(train, test, exposure_term, controls,
                                  offset_policy = "days_only") {
  base_fit <- tryCatch(
    .fit_nb_simple(train, NULL, controls, offset_policy),
    error = function(e) e
  )
  exp_fit <- tryCatch(
    .fit_nb_simple(train, exposure_term, controls, offset_policy),
    error = function(e) e
  )
  if (inherits(base_fit, "error") || inherits(exp_fit, "error")) {
    msg <- paste(
      if (inherits(base_fit, "error")) paste0("baseline: ", conditionMessage(base_fit)) else NULL,
      if (inherits(exp_fit, "error")) paste0("exposure: ", conditionMessage(exp_fit)) else NULL,
      sep = " | "
    )
    return(list(
      ok = FALSE,
      message = msg,
      scores = NULL
    ))
  }
  y <- as.numeric(test$n_events)
  mu0 <- .predict_nb_mu(base_fit, test)
  mu1 <- .predict_nb_mu(exp_fit, test)
  th0 <- unname(base_fit$theta)
  th1 <- unname(exp_fit$theta)
  ls0 <- .nb_log_score(y, mu0, th0)
  ls1 <- .nb_log_score(y, mu1, th1)
  scores <- data.frame(
    n_test = length(y),
    log_score_baseline = mean(ls0),
    log_score_exposure = mean(ls1),
    log_score_diff = mean(ls1) - mean(ls0),
    deviance_baseline = mean(.nb_unit_deviance(y, mu0, th0)),
    deviance_exposure = mean(.nb_unit_deviance(y, mu1, th1)),
    mae_baseline = mean(abs(y - mu0)),
    mae_exposure = mean(abs(y - mu1)),
    stringsAsFactors = FALSE
  )
  list(ok = TRUE, message = "", scores = scores)
}

score_loyo_nb <- function(dat, exposure_term, controls = c("month_f", "splines::ns(time_index, df = 4)"),
                          offset_policy = "days_only", metadata = NULL) {
  years <- sort(unique(as.integer(dat$year)))
  rows <- list()
  status_rows <- list()
  for (yr in years) {
    train <- dat[dat$year != yr, , drop = FALSE]
    test <- dat[dat$year == yr, , drop = FALSE]
    train$month_f <- factor(train$month, levels = levels(factor(dat$month)))
    test$month_f <- factor(test$month, levels = levels(factor(dat$month)))
    res <- score_prediction_pair(train, test, exposure_term, controls, offset_policy)
    if (!isTRUE(res$ok)) {
      status_rows[[as.character(yr)]] <- status_row(
        "FAILED", res$message,
        scheme = "leave_one_year_out", held_out_year = yr,
        n_months = nrow(train)
      )
      next
    }
    sc <- res$scores
    sc$scheme <- "leave_one_year_out"
    sc$held_out_year <- yr
    sc$train_months <- nrow(train)
    if (!is.null(metadata)) sc <- cbind(as.data.frame(metadata, stringsAsFactors = FALSE), sc)
    rows[[as.character(yr)]] <- sc
    status_rows[[as.character(yr)]] <- status_row(
      "OK", "",
      scheme = "leave_one_year_out", held_out_year = yr,
      n_months = nrow(train)
    )
  }
  list(
    scores = if (length(rows)) dplyr::bind_rows(rows) else NULL,
    status = dplyr::bind_rows(status_rows)
  )
}

score_rolling_origin_nb <- function(dat, exposure_term,
                                    controls = c("month_f", "splines::ns(time_index, df = 4)"),
                                    offset_policy = "days_only",
                                    horizon = 12L,
                                    min_train = 60L,
                                    metadata = NULL) {
  d <- dat[order(dat$time_index), , drop = FALSE]
  n <- nrow(d)
  rows <- list()
  status_rows <- list()
  starts <- seq.int(min_train, n - horizon)
  if (!length(starts)) {
    return(list(
      scores = NULL,
      status = status_row(
        "FAILED",
        paste0("Insufficient length for rolling origin (n=", n, ", horizon=", horizon, ")"),
        scheme = "rolling_origin_12_month",
        n_months = n
      )
    ))
  }
  for (tr_end in starts) {
    train <- d[seq_len(tr_end), , drop = FALSE]
    test <- d[seq.int(tr_end + 1L, tr_end + horizon), , drop = FALSE]
    train$month_f <- factor(train$month, levels = levels(factor(d$month)))
    test$month_f <- factor(test$month, levels = levels(factor(d$month)))
    res <- score_prediction_pair(train, test, exposure_term, controls, offset_policy)
    key <- as.character(tr_end)
    if (!isTRUE(res$ok)) {
      status_rows[[key]] <- status_row(
        "FAILED", res$message,
        scheme = "rolling_origin_12_month",
        train_end_index = tr_end,
        n_months = nrow(train)
      )
      next
    }
    sc <- res$scores
    sc$scheme <- "rolling_origin_12_month"
    sc$train_end_index <- tr_end
    sc$train_months <- nrow(train)
    if (!is.null(metadata)) sc <- cbind(as.data.frame(metadata, stringsAsFactors = FALSE), sc)
    rows[[key]] <- sc
    status_rows[[key]] <- status_row(
      "OK", "",
      scheme = "rolling_origin_12_month",
      train_end_index = tr_end,
      n_months = nrow(train)
    )
  }
  list(
    scores = if (length(rows)) dplyr::bind_rows(rows) else NULL,
    status = dplyr::bind_rows(status_rows)
  )
}

# ---------------------------------------------------------------------------
# Serial-null / dependence-preserving max-stat helpers
# ---------------------------------------------------------------------------

fit_baseline_nb_mu_theta <- function(dat, controls = c("month_f", "splines::ns(time_index, df = 4)"),
                                    offset_policy = "days_only") {
  model <- .fit_nb_simple(dat, NULL, controls, offset_policy)
  list(
    model = model,
    mu = as.numeric(stats::fitted(model)),
    theta = unname(model$theta)
  )
}

simulate_serial_null_counts <- function(mu, theta, n_reps = 200L, seed = 1L) {
  # Parametric NB draws under the fitted baseline mean (exposure null).
  if (!is.finite(theta) || theta <= 0) stop("theta must be positive finite")
  n <- length(mu)
  out <- matrix(NA_integer_, nrow = n, ncol = as.integer(n_reps))
  set.seed(seed)
  for (j in seq_len(n_reps)) {
    out[, j] <- stats::rnbinom(n, mu = pmax(mu, 1e-12), size = theta)
  }
  out
}

stationary_block_indices <- function(n, block_length = 6L, seed = 1L) {
  # Circular fixed-length block bootstrap index generator.
  if (block_length < 1L || block_length > n) stop("Invalid block_length")
  set.seed(seed)
  n_blocks <- ceiling(n / block_length)
  starts <- sample.int(n, size = n_blocks, replace = TRUE)
  idx <- unlist(lapply(starts, function(s) {
    ((s - 1L + seq_len(block_length) - 1L) %% n) + 1L
  }), use.names = FALSE)
  idx[seq_len(n)]
}

simulate_block_residual_null <- function(y, mu, theta, n_reps = 200L,
                                         block_length = 6L, seed = 1L) {
  # Dependence-preserving null: bootstrap Pearson residuals in circular blocks,
  # then reconstruct counts around baseline mu (clipped at 0).
  pearson <- (y - mu) / sqrt(pmax(mu + mu^2 / theta, 1e-8))
  n <- length(y)
  out <- matrix(NA_real_, nrow = n, ncol = as.integer(n_reps))
  for (j in seq_len(n_reps)) {
    idx <- stationary_block_indices(n, block_length, seed = seed + j)
    y_star <- mu + pearson[idx] * sqrt(pmax(mu + mu^2 / theta, 1e-8))
    out[, j] <- pmax(round(y_star), 0)
  }
  out
}

max_abs_stat_from_estimates <- function(estimate_df, stat_col = "statistic") {
  if (is.null(estimate_df) || !nrow(estimate_df)) return(NA_real_)
  max(abs(as.numeric(estimate_df[[stat_col]])), na.rm = TRUE)
}

run_serial_null_max_stat <- function(dat, fit_one_rep,
                                     n_reps = 200L,
                                     method = c("parametric_nb", "block_residual"),
                                     block_length = 6L,
                                     seed = 1L,
                                     baseline_controls = c("month_f", "splines::ns(time_index, df = 4)"),
                                     offset_policy = "days_only") {
  method <- match.arg(method)
  base <- fit_baseline_nb_mu_theta(dat, baseline_controls, offset_policy)
  y <- as.numeric(dat$n_events)
  if (identical(method, "parametric_nb")) {
    sims <- simulate_serial_null_counts(base$mu, base$theta, n_reps = n_reps, seed = seed)
  } else {
    sims <- simulate_block_residual_null(
      y, base$mu, base$theta, n_reps = n_reps,
      block_length = block_length, seed = seed
    )
  }

  max_stats <- rep(NA_real_, n_reps)
  status <- vector("list", n_reps)
  for (j in seq_len(n_reps)) {
    d_j <- dat
    d_j$n_events <- as.numeric(sims[, j])
    rep_res <- tryCatch(fit_one_rep(d_j), error = function(e) e)
    if (inherits(rep_res, "error")) {
      status[[j]] <- status_row("FAILED", conditionMessage(rep_res), rep = j)
      next
    }
    max_stats[[j]] <- max_abs_stat_from_estimates(rep_res$estimates)
    status[[j]] <- status_row(
      if (is.finite(max_stats[[j]])) "OK" else "FAILED",
      if (is.finite(max_stats[[j]])) "" else "Non-finite max statistic",
      rep = j
    )
  }
  list(
    max_stats = max_stats,
    status = dplyr::bind_rows(status),
    method = method,
    n_reps = n_reps
  )
}

# ---------------------------------------------------------------------------
# Missing-panel blocker artifact
# ---------------------------------------------------------------------------

missing_governed_panel_blocker <- function(outcomes = c("chd", "hf"),
                                           root = NULL,
                                           script_id = NA_character_) {
  if (is.null(root)) {
    root <- if (exists("project_root", mode = "function")) project_root() else getwd()
  }
  paths <- file.path(root, "data_processed", paste0(outcomes, "_analysis_panel.csv"))
  present <- file.exists(paths)
  data.frame(
    script_id = script_id,
    outcome = outcomes,
    panel_path = paths,
    panel_present = present,
    status = "NOT_RUN_MISSING_GOVERNED_PANEL",
    message = ifelse(
      present,
      "Panel present",
      "Governed analysis panel absent in this checkout; real ensemble not run"
    ),
    result_class = RESULT_CLASS_EXPLORATORY,
    data_status = NA_character_,
    stringsAsFactors = FALSE
  )
}

handle_missing_governed_panels <- function(blocker_df, out_path,
                                           allow_env = "ALLOW_MISSING_GOVERNED") {
  dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(blocker_df, out_path, row.names = FALSE, na = "")
  message("Wrote missing-panel blocker: ", out_path)
  allow <- identical(Sys.getenv(allow_env, unset = "0"), "1")
  if (allow) {
    message(
      "ALLOW_MISSING_GOVERNED=1: exiting 0 after blocker artifact (",
      out_path, ")"
    )
    quit(save = "no", status = 0)
  }
  stop(
    "NOT_RUN_MISSING_GOVERNED_PANEL: required governed panels absent. ",
    "Set ALLOW_MISSING_GOVERNED=1 to exit 0 after writing the blocker table."
  )
}
