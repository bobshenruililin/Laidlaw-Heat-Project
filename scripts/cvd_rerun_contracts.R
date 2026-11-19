# Contracts for the governed territory-month CHD/HF rerun.
# Every validator is data-in, data-out. Nothing in this file discovers inputs.

assert_cvd_event_calendar <- function(month_id, counts, expected) {
  if (length(month_id) != length(expected) || anyNA(month_id) ||
      anyDuplicated(month_id) || !setequal(month_id, expected)) {
    stop("Expected one territory count for every study month, with no extra months")
  }
  if (!is.numeric(counts) || length(counts) != length(expected) ||
      any(!is.finite(counts)) || any(counts < 0 | counts != floor(counts))) {
    stop("Monthly event counts must be observed non-negative integers")
  }
}

assert_cvd_outcome <- function(dat, outcome) {
  for (field in intersect(c("analysis_outcome", "outcome"), names(dat))) {
    if (anyNA(dat[[field]]) || !all(dat[[field]] == outcome)) {
      stop("Panel outcome disagrees with requested analysis: ", outcome)
    }
  }
}

read_cvd_model_panel <- function(path, outcome) {
  # Reuse the complete calendar, exposure, counts and provenance contract
  # already implemented by the prospective runner. Sourcing it runs no fits.
  source(file.path("scripts", "83_covid_common_basis_interactions.R"), local = TRUE)
  dat <- utils::read.csv(path, stringsAsFactors = FALSE)
  assert_cvd_outcome(dat, outcome)
  dat <- validate_monthly_panel(dat, synthetic = FALSE)
  # Stable keys survive omissions and reordered input.
  rownames(dat) <- dat$month_id
  dat
}

cvd_fitted_rows <- function(model, data) {
  keys <- rownames(stats::model.frame(model))
  indices <- match(keys, rownames(data))
  if (length(indices) != stats::nobs(model) || anyNA(indices) ||
      anyDuplicated(indices)) stop("Cannot map model rows to source rows")
  indices
}

cvd_max_cook_row <- function(model, data) {
  fitted_rows <- cvd_fitted_rows(model, data)
  cooks <- stats::cooks.distance(model)
  valid <- which(is.finite(cooks))
  if (length(cooks) != length(fitted_rows) || !length(valid)) {
    stop("No usable aligned Cook's distances")
  }
  selected <- valid[which.max(cooks[valid])]
  list(index = fitted_rows[selected], distance = unname(cooks[selected]))
}

# For a leave-one-month-out fit, adjacent score rows may be two months apart.
# Use Bartlett weights on calendar distance. The small-sample divisor counts
# fitted observations, so removing a month adds neither an observation nor a score.
cvd_monthly_nw <- function(model, months, lag = 6L) {
  if (length(months) != stats::nobs(model) || any(!is.finite(months)) ||
      any(months != floor(months)) || any(diff(months) <= 0)) {
    stop("HAC requires ordered, distinct calendar indices for all fitted rows")
  }
  if (all(diff(months) == 1L)) {
    return(sandwich::NeweyWest(model, lag = lag, prewhite = FALSE, adjust = TRUE))
  }
  scores <- sandwich::estfun(model)
  distance <- abs(outer(months, months, "-"))
  weights <- pmax(1 - distance / (lag + 1L), 0)
  meat <- crossprod(scores, weights %*% scores) / (nrow(scores) - ncol(scores))
  sandwich::sandwich(model, meat. = meat)
}

cvd_monthly_acf1 <- function(residuals, months) {
  if (length(residuals) != length(months)) stop("Residual/calendar length mismatch")
  centered <- residuals - mean(residuals)
  adjacent <- which(diff(months) == 1L)
  denominator <- sum(centered^2)
  if (!length(adjacent) || !is.finite(denominator) || denominator == 0) return(NA_real_)
  sum(centered[adjacent] * centered[adjacent + 1L]) / denominator
}

cvd_core_bh <- function(baseline) {
  exposures <- c(P01A = "mean_temp", P02A = "mean_tmax", P02B = "mean_tmin",
                 P04A = "hot_nights", P04B = "cold_days", P04C = "very_hot_days")
  expected <- as.vector(outer(c("chd", "hf"), names(exposures), paste, sep = "/"))
  keys <- paste(baseline$outcome, baseline$pathway_id, sep = "/")
  if (length(keys) != 12L || anyDuplicated(keys) || !setequal(keys, expected) ||
      anyNA(baseline$exposure) ||
      !all(baseline$exposure == unname(exposures[as.character(baseline$pathway_id)]))) {
    stop("Incomplete or mismatched twelve-member baseline family. Missing: ",
         paste(setdiff(expected, keys), collapse = ", "))
  }
  p <- baseline$p_value
  if (!is.numeric(p) || length(p) != 12L || any(!is.finite(p) | p < 0 | p > 1)) {
    stop("Every member of the baseline family needs a finite p-value before release")
  }
  stats::p.adjust(p, method = "BH", n = 12L)
}

cvd_ingarch_vcov <- function(model) {
  # tscount would fall back to Poisson information if the NB meat were missing.
  if (is.null(model$info.matrix_corrected)) return(NULL)
  tryCatch(stats::vcov(model), error = function(e) NULL)
}

cvd_converged <- function(model) {
  isTRUE(model$converged) &&
    (!inherits(model, "negbin") ||
       (is.finite(model$theta) && model$theta > 0 && is.null(model$th.warn)))
}

fit_nb_nw <- function(dat, term, controls, offset = "offset(offset_log_days)") {
  rhs <- c(term, controls, offset)
  fml <- stats::as.formula(paste("n_events ~", paste(rhs, collapse = " + ")))
  model <- MASS::glm.nb(fml, data = dat, na.action = stats::na.fail)
  if (!cvd_converged(model)) stop("Negative-binomial fit did not converge")
  calendar <- dat$time_index[cvd_fitted_rows(model, dat)]
  vm <- cvd_monthly_nw(model, calendar, lag = 6L)
  if (!term %in% names(stats::coef(model))) stop("Term not found: ", term)
  b <- unname(stats::coef(model)[term])
  se <- unname(sqrt(diag(vm))[term])
  if (!is.finite(b) || !is.finite(se) || se <= 0) stop("Unusable exposure estimate or interval")
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
      n_fitted = stats::nobs(model),
      residual_acf1 = cvd_monthly_acf1(res, calendar),
      stringsAsFactors = FALSE
    )
  )
}
