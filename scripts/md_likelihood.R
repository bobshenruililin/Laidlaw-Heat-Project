# md_likelihood.R
# Clean-room monthly-outcome / daily-exposure (M|D) aggregated Poisson likelihood.
#
# Published equation (Basagaña–Ballester): if latent daily means
#   lambda_d = offset_d * exp(X_d %*% beta),
# and S_m = sum_{d in month m} Y_d is observed, then
#   S_m ~ Poisson(sum_{d in m} lambda_d).
#
# Implemented from the published likelihood identity only. Do not copy or vendor
# any code from xbasagana/aggregated (unlicensed). Do not run directly.

MD_MAX_PARAMETERS <- 20L
MD_HESSIAN_CONDITION_MAX <- 1e8
MD_PROVENANCE_SYNTHETIC <- "SYNTHETIC_CALIBRATION"
MD_PROVENANCE_REAL <- "HA_APPROVED_AGGREGATE"
MD_PROVENANCE_PUBLIC_HKO <- "REAL_PUBLIC_HKO"

# ---------------------------------------------------------------------------
# Numerics
# ---------------------------------------------------------------------------

.md_log_sum_exp <- function(x) {
  x <- as.numeric(x)
  x <- x[is.finite(x)]
  if (!length(x)) return(-Inf)
  m <- max(x)
  if (!is.finite(m)) return(m)
  m + log(sum(exp(x - m)))
}

.md_safe_chol_pd <- function(H) {
  # Returns list(ok, cond, message). Prefer eigenvalues for condition number.
  if (any(!is.finite(H))) {
    return(list(ok = FALSE, cond = Inf, message = "non_finite_hessian"))
  }
  Hsym <- 0.5 * (H + t(H))
  ev <- tryCatch(eigen(Hsym, symmetric = TRUE, only.values = TRUE)$values,
                 error = function(e) NULL)
  if (is.null(ev) || !length(ev) || any(!is.finite(ev))) {
    return(list(ok = FALSE, cond = Inf, message = "eigen_failed"))
  }
  if (any(ev <= 0)) {
    return(list(
      ok = FALSE,
      cond = Inf,
      message = "not_positive_definite"
    ))
  }
  cond <- max(ev) / min(ev)
  list(
    ok = is.finite(cond) && cond < MD_HESSIAN_CONDITION_MAX,
    cond = cond,
    message = if (is.finite(cond) && cond < MD_HESSIAN_CONDITION_MAX) {
      "ok"
    } else {
      "condition_number_exceeded"
    }
  )
}

.md_month_index <- function(month_id) {
  month_id <- as.character(month_id)
  u <- unique(month_id)
  match(month_id, u)
}

# ---------------------------------------------------------------------------
# Constrained lag-kernel helpers
# ---------------------------------------------------------------------------

#' Build a same-day exposure from a daily event indicator.
md_kernel_same_day <- function(event) {
  as.numeric(event)
}

#' Normalized cumulative lag-0..L exposure (equal weights summing to 1).
#' For day d: (1/(L+1)) * sum_{k=0}^L event_{d-k}; missing pre-history treated as 0.
md_kernel_normalized_cumulative <- function(event, max_lag) {
  event <- as.numeric(event)
  event[!is.finite(event)] <- 0
  L <- as.integer(max_lag)
  if (L < 0L) stop("max_lag must be >= 0")
  n <- length(event)
  w <- 1 / (L + 1)
  out <- numeric(n)
  # Running sum via cumsum difference
  cs <- c(0, cumsum(event))
  for (i in seq_len(n)) {
    lo <- max(0L, i - L - 1L)
    out[i] <- w * (cs[i + 1L] - cs[lo + 1L])
  }
  out
}

md_kernel_cumulative_0_5 <- function(event) {
  md_kernel_normalized_cumulative(event, max_lag = 5L)
}

md_kernel_cumulative_0_21 <- function(event) {
  md_kernel_normalized_cumulative(event, max_lag = 21L)
}

md_apply_kernel <- function(event, kernel = c("same_day", "cumulative_0_5", "cumulative_0_21")) {
  kernel <- match.arg(kernel)
  switch(
    kernel,
    same_day = md_kernel_same_day(event),
    cumulative_0_5 = md_kernel_cumulative_0_5(event),
    cumulative_0_21 = md_kernel_cumulative_0_21(event)
  )
}

md_kernel_weight_sum <- function(kernel = c("same_day", "cumulative_0_5", "cumulative_0_21")) {
  kernel <- match.arg(kernel)
  # Declared equal-weight kernels are normalized to sum 1 by construction.
  1
}

# ---------------------------------------------------------------------------
# Low-dimensional daily design builder
# ---------------------------------------------------------------------------

#' Build a constrained daily design matrix for M|D feasibility fits.
#'
#' Columns: intercept, 2 annual harmonics (doy), ns(time, 3), optional COVID
#' phase indicators (dropping reference), and one frozen exposure column.
#' Total parameters must remain <= MD_MAX_PARAMETERS.
md_build_daily_design <- function(dates,
                                  exposure,
                                  covid_phase = NULL,
                                  include_covid = TRUE,
                                  time_df = 3L,
                                  exposure_name = "exposure") {
  dates <- as.Date(dates)
  n <- length(dates)
  if (length(exposure) != n) stop("exposure length must match dates")
  exposure <- as.numeric(exposure)
  if (any(!is.finite(exposure))) {
    stop("exposure contains non-finite values; impute or drop before design build")
  }

  doy <- as.integer(format(dates, "%j"))
  # Thin source-documented season: two annual Fourier harmonics on day-of-year.
  harm_sin <- sin(2 * pi * doy / 365.25)
  harm_cos <- cos(2 * pi * doy / 365.25)

  time_index <- as.numeric(dates - min(dates)) + 1
  if (!requireNamespace("splines", quietly = TRUE)) {
    stop("Package splines is required for ns(time, df)")
  }
  ns_mat <- splines::ns(time_index, df = as.integer(time_df))
  colnames(ns_mat) <- paste0("ns_time", seq_len(ncol(ns_mat)))

  X <- cbind(
    intercept = 1,
    harm_sin = harm_sin,
    harm_cos = harm_cos,
    ns_mat
  )

  if (isTRUE(include_covid)) {
    if (is.null(covid_phase)) {
      month_id <- format(dates, "%Y-%m")
      # Fallback phases if caller did not supply; mirrors config.yml ranges.
      covid_phase <- rep("pre_covid", n)
      covid_phase[month_id >= "2020-02" & month_id <= "2021-12"] <- "early_covid"
      covid_phase[month_id >= "2022-01" & month_id <= "2022-04"] <- "fifth_wave"
      covid_phase[month_id >= "2022-05" & month_id <= "2022-12"] <- "late_2022"
      covid_phase[month_id >= "2023-01"] <- "post_reopening"
    }
    covid_phase <- as.character(covid_phase)
    # Reference level is always pre_covid (not alphabetical).
    ref <- "pre_covid"
    lev <- unique(covid_phase)
    other <- setdiff(lev, ref)
    # Stable non-alphabetical order for non-reference levels.
    preferred <- c("early_covid", "fifth_wave", "late_2022", "post_reopening")
    other <- c(intersect(preferred, other), setdiff(other, preferred))
    if (length(other)) {
      for (lv in other) {
        X <- cbind(X, as.numeric(covid_phase == lv))
        colnames(X)[ncol(X)] <- paste0("covid_", gsub("[^A-Za-z0-9_]", "_", lv))
      }
    }
  }

  X <- cbind(X, as.numeric(exposure))
  colnames(X)[ncol(X)] <- exposure_name

  p <- ncol(X)
  if (p > MD_MAX_PARAMETERS) {
    stop(
      "Daily design has p=", p,
      " parameters; M|D guard requires p<=", MD_MAX_PARAMETERS
    )
  }
  rank <- qr(X)$rank
  attr(X, "rank") <- rank
  attr(X, "time_index") <- time_index
  attr(X, "covid_phase") <- if (isTRUE(include_covid)) covid_phase else NULL
  X
}

# ---------------------------------------------------------------------------
# Aggregate Poisson log-likelihood, score, Hessian
# ---------------------------------------------------------------------------

#' Prepare month groups for M|D evaluation.
md_prepare_groups <- function(month_id, offset = NULL, n_days = NULL) {
  month_id <- as.character(month_id)
  if (is.null(n_days)) n_days <- length(month_id)
  if (is.null(offset)) offset <- rep(1, n_days)
  offset <- as.numeric(offset)
  if (length(offset) != n_days) stop("offset length must match daily rows")
  if (any(!is.finite(offset) | offset <= 0)) {
    stop("daily offset must be positive and finite")
  }
  g <- split(seq_len(n_days), month_id)
  list(
    month_id = names(g),
    indices = g,
    offset = offset,
    n_days = n_days,
    n_months = length(g)
  )
}

# Clamp linear predictors to avoid exp() overflow during optimizer excursions.
MD_ETA_CLAMP <- 50

.md_clamp_eta <- function(eta, lo = -MD_ETA_CLAMP, hi = MD_ETA_CLAMP) {
  pmin(pmax(as.numeric(eta), lo), hi)
}

#' Daily linear predictors and month means (log-sum-exp stable).
#'
#' Non-finite eta before/after clamping, or non-finite/non-positive month means,
#' raise an explicit error instead of silently dropping months.
md_month_means <- function(beta, X, groups) {
  beta <- as.numeric(beta)
  if (any(!is.finite(beta))) stop("non_finite_beta")
  eta_raw <- as.numeric(X %*% beta)
  if (any(!is.finite(eta_raw))) stop("non_finite_linear_predictor")
  eta <- .md_clamp_eta(eta_raw)
  log_off <- log(groups$offset)
  if (any(!is.finite(log_off))) stop("non_finite_log_offset")
  log_lam <- eta + log_off
  lambda <- exp(log_lam)
  if (any(!is.finite(lambda)) || any(lambda < 0)) stop("non_finite_daily_lambda")
  log_mu <- vapply(groups$indices, function(idx) {
    .md_log_sum_exp(log_lam[idx])
  }, numeric(1))
  mu <- exp(log_mu)
  if (any(!is.finite(mu)) || any(mu <= 0)) stop("non_finite_month_mean")
  list(
    eta = eta,
    eta_raw = eta_raw,
    lambda = lambda,
    log_mu = log_mu,
    mu = mu,
    log_off = log_off
  )
}

#' Aggregate Poisson log-likelihood (up to constant -sum log(S_m!)).
#'
#' Uses stable log-sum-exp for log(mu_m) when evaluating S_m * log(mu_m).
md_loglik <- function(beta, S, X, groups, include_factorial = FALSE) {
  beta <- as.numeric(beta)
  S <- as.numeric(S)
  if (length(S) != groups$n_months) {
    stop("S length must equal number of months")
  }
  mm <- md_month_means(beta, X, groups)
  ll <- 0
  for (m in seq_len(groups$n_months)) {
    sm <- S[m]
    log_mu <- mm$log_mu[m]
    mu <- mm$mu[m]
    if (!is.finite(log_mu) || !is.finite(mu) || mu <= 0) {
      stop("non_finite_month_mean in loglik")
    }
    ll <- ll + sm * log_mu - mu
    if (isTRUE(include_factorial) && sm > 0 && is.finite(sm)) {
      ll <- ll - lgamma(sm + 1)
    }
  }
  if (!is.finite(ll)) stop("non_finite_loglik")
  ll
}

#' Analytic score (gradient) of the aggregate Poisson log-likelihood.
md_score <- function(beta, S, X, groups) {
  mm <- md_month_means(beta, X, groups)
  p <- ncol(X)
  score <- numeric(p)
  for (m in seq_len(groups$n_months)) {
    idx <- groups$indices[[m]]
    mu <- mm$mu[m]
    if (!is.finite(mu) || mu <= 0) stop("non_finite_month_mean in score")
    # Softmax weights pi_d = lambda_d / mu for stable dmu/mu.
    pi <- mm$lambda[idx] / mu
    if (any(!is.finite(pi))) stop("non_finite_softmax_weights in score")
    # score contrib = (S - mu) * X^T pi
    Xm <- X[idx, , drop = FALSE]
    score <- score + (S[m] - mu) * as.numeric(crossprod(Xm, pi))
  }
  if (any(!is.finite(score))) stop("non_finite_score")
  score
}

#' Analytic Hessian of the aggregate Poisson log-likelihood.
md_hessian <- function(beta, S, X, groups) {
  mm <- md_month_means(beta, X, groups)
  p <- ncol(X)
  H <- matrix(0, p, p)
  for (m in seq_len(groups$n_months)) {
    idx <- groups$indices[[m]]
    mu <- mm$mu[m]
    if (!is.finite(mu) || mu <= 0) stop("non_finite_month_mean in hessian")
    lam <- mm$lambda[idx]
    pi <- lam / mu
    if (any(!is.finite(pi))) stop("non_finite_softmax_weights in hessian")
    Xm <- X[idx, , drop = FALSE]
    # d log_mu / d beta = X^T pi; d2 uses weighted cov of rows
    # Original: H = - (S/mu^2) dmu dmu^T + (S/mu - 1) d2mu
    # with dmu = mu * (X^T pi), d2mu = X^T diag(lam) X
    # => H = -S (X^T pi)(X^T pi)^T + (S - mu) (X^T diag(pi) X)
    #         wait: (S/mu - 1) * X^T diag(lam) X = (S - mu)/mu * X^T diag(lam) X
    #              = (S - mu) * X^T diag(pi) X
    xtpi <- as.numeric(crossprod(Xm, pi))
    xt_diag_pi_x <- crossprod(Xm, pi * Xm)
    H <- H - S[m] * tcrossprod(xtpi) + (S[m] - mu) * xt_diag_pi_x
  }
  H <- 0.5 * (H + t(H))
  if (any(!is.finite(H))) stop("non_finite_hessian")
  H
}

# Negative log-likelihood / score for optimizers — propagate non-finite as Inf/NA
.md_nll <- function(beta, S, X, groups) {
  out <- tryCatch(
    -md_loglik(beta, S, X, groups, include_factorial = FALSE),
    error = function(e) Inf
  )
  if (!is.finite(out)) Inf else out
}
.md_nll_grad <- function(beta, S, X, groups) {
  tryCatch(
    -md_score(beta, S, X, groups),
    error = function(e) rep(NA_real_, length(beta))
  )
}

#' Whether a fitted M|D object may emit a real estimate under registry gates.
md_real_fit_admissible <- function(fit, hessian_condition_max = MD_HESSIAN_CONDITION_MAX) {
  isTRUE(fit$converged) &&
    isTRUE(fit$hessian_pd) &&
    is.finite(fit$hessian_condition) &&
    fit$hessian_condition < hessian_condition_max
}

# ---------------------------------------------------------------------------
# Fitting
# ---------------------------------------------------------------------------

.md_rank_guard <- function(X) {
  p <- ncol(X)
  if (p > MD_MAX_PARAMETERS) {
    return(list(
      ok = FALSE,
      rank = NA_integer_,
      p = p,
      message = sprintf("p=%d exceeds max_parameters=%d", p, MD_MAX_PARAMETERS)
    ))
  }
  r <- qr(X)$rank
  if (r < p) {
    return(list(
      ok = FALSE,
      rank = r,
      p = p,
      message = sprintf("rank-deficient design: rank=%d < p=%d", r, p)
    ))
  }
  list(ok = TRUE, rank = r, p = p, message = "ok")
}

.md_fit_status_row <- function(status, message, ...) {
  dots <- list(...)
  base <- data.frame(
    status = status,
    message = message,
    stringsAsFactors = FALSE
  )
  if (length(dots)) {
    extra <- as.data.frame(dots, stringsAsFactors = FALSE)
    cbind(base, extra)
  } else {
    base
  }
}

#' Fit constrained M|D aggregate Poisson model.
#'
#' @param S length-M monthly counts (aligned to unique month order in month_id)
#' @param X n x p daily design (including intercept)
#' @param month_id length-n month identifiers
#' @param offset length-n positive daily offsets (default 1)
#' @param method "BFGS" then Newton fallback on failure
#' @param quasi if TRUE, inflate covariance by Pearson quasi-Poisson dispersion
md_fit <- function(S,
                   X,
                   month_id,
                   offset = NULL,
                   start = NULL,
                   method = c("BFGS", "Newton"),
                   quasi = TRUE,
                   control = list(maxit = 200),
                   tol = 1e-8) {
  method <- match.arg(method)
  X <- as.matrix(X)
  storage.mode(X) <- "double"
  p <- ncol(X)
  groups <- md_prepare_groups(month_id, offset = offset, n_days = nrow(X))
  S <- as.numeric(S)
  if (is.null(names(S)) && length(S) == groups$n_months) {
    names(S) <- groups$month_id
  }
  # Align S to group month order
  if (!is.null(names(S))) {
    S <- as.numeric(S[groups$month_id])
  }
  if (length(S) != groups$n_months || any(!is.finite(S)) || any(S < 0)) {
    return(list(
      converged = FALSE,
      status = "invalid_response",
      message = "S must be non-negative finite and length n_months",
      beta = rep(NA_real_, p),
      vcov = matrix(NA_real_, p, p),
      vcov_quasi = matrix(NA_real_, p, p),
      dispersion = NA_real_,
      hessian = matrix(NA_real_, p, p),
      hessian_pd = FALSE,
      hessian_condition = Inf,
      loglik = NA_real_,
      rank = NA_integer_,
      p = p,
      n_months = groups$n_months,
      n_days = groups$n_days,
      method_used = NA_character_,
      status_row = .md_fit_status_row(
        "invalid_response", "S must be non-negative finite and length n_months",
        p = p, n_months = groups$n_months, converged = FALSE
      )
    ))
  }

  rg <- .md_rank_guard(X)
  if (!isTRUE(rg$ok)) {
    return(list(
      converged = FALSE,
      status = "rank_or_p_guard",
      message = rg$message,
      beta = rep(NA_real_, p),
      vcov = matrix(NA_real_, p, p),
      vcov_quasi = matrix(NA_real_, p, p),
      dispersion = NA_real_,
      hessian = matrix(NA_real_, p, p),
      hessian_pd = FALSE,
      hessian_condition = Inf,
      loglik = NA_real_,
      rank = rg$rank,
      p = p,
      n_months = groups$n_months,
      n_days = groups$n_days,
      method_used = NA_character_,
      status_row = .md_fit_status_row(
        "rank_or_p_guard", rg$message,
        p = p, rank = rg$rank, n_months = groups$n_months, converged = FALSE
      )
    ))
  }

  if (is.null(start)) {
    # Intercept = log(mean daily rate); other coefs 0.
    start <- rep(0, p)
    mean_daily <- sum(S) / groups$n_days
    if (is.finite(mean_daily) && mean_daily > 0) {
      start[1] <- log(mean_daily)
    }
  }
  start <- as.numeric(start)
  if (length(start) != p || any(!is.finite(start))) {
    start <- rep(0, p)
  }

  fit_bfgs <- tryCatch(
    stats::optim(
      par = start,
      fn = .md_nll,
      gr = .md_nll_grad,
      S = S,
      X = X,
      groups = groups,
      method = "BFGS",
      control = control
    ),
    error = function(e) e
  )

  method_used <- "BFGS"
  beta <- NULL
  optim_ok <- FALSE
  optim_msg <- ""

  if (!inherits(fit_bfgs, "error") &&
      is.list(fit_bfgs) &&
      isTRUE(fit_bfgs$convergence == 0) &&
      all(is.finite(fit_bfgs$par))) {
    beta <- as.numeric(fit_bfgs$par)
    optim_ok <- TRUE
  } else {
    optim_msg <- if (inherits(fit_bfgs, "error")) {
      conditionMessage(fit_bfgs)
    } else if (is.list(fit_bfgs)) {
      paste0("BFGS convergence=", fit_bfgs$convergence, " ", fit_bfgs$message %||% "")
    } else {
      "BFGS failed"
    }
  }

  # Newton fallback (Fisher-scoring style with analytic Hessian)
  if (!optim_ok || identical(method, "Newton")) {
    method_used <- if (optim_ok) "BFGS" else "Newton"
    beta_n <- if (!is.null(beta)) beta else start
    newton_ok <- FALSE
    for (iter in seq_len(control$maxit %||% 200L)) {
      g <- md_score(beta_n, S, X, groups)
      H <- md_hessian(beta_n, S, X, groups)
      # Solve H delta = -g for maximizer => (-H) delta = g
      negH <- -H
      pd <- .md_safe_chol_pd(negH)
      if (!isTRUE(pd$ok)) {
        # ridge
        negH <- negH + diag(1e-6, p)
      }
      delta <- tryCatch(
        solve(negH, g),
        error = function(e) rep(NA_real_, p)
      )
      if (any(!is.finite(delta))) break
      # Backtracking
      step <- 1
      nll0 <- .md_nll(beta_n, S, X, groups)
      improved <- FALSE
      for (bt in 1:20) {
        trial <- beta_n + step * delta
        nll1 <- tryCatch(.md_nll(trial, S, X, groups), error = function(e) Inf)
        if (is.finite(nll1) && nll1 < nll0) {
          beta_n <- trial
          improved <- TRUE
          break
        }
        step <- step / 2
      }
      if (!improved) break
      if (sqrt(sum(delta * delta)) < tol) {
        newton_ok <- TRUE
        break
      }
    }
    if (newton_ok || (optim_ok && identical(method, "BFGS"))) {
      if (!optim_ok) {
        beta <- beta_n
        optim_ok <- newton_ok
        method_used <- "Newton"
      }
    } else if (!optim_ok && newton_ok) {
      beta <- beta_n
      optim_ok <- TRUE
      method_used <- "Newton"
    } else if (!optim_ok) {
      # try Newton from start even if BFGS partially ran
      if (all(is.finite(beta_n))) {
        beta <- beta_n
        optim_ok <- isTRUE(newton_ok)
        method_used <- "Newton"
      }
    }
  }

  if (!optim_ok || is.null(beta) || any(!is.finite(beta))) {
    return(list(
      converged = FALSE,
      status = "optim_failed",
      message = paste("optimizer failed:", optim_msg),
      beta = rep(NA_real_, p),
      vcov = matrix(NA_real_, p, p),
      vcov_quasi = matrix(NA_real_, p, p),
      dispersion = NA_real_,
      hessian = matrix(NA_real_, p, p),
      hessian_pd = FALSE,
      hessian_condition = Inf,
      loglik = NA_real_,
      rank = rg$rank,
      p = p,
      n_months = groups$n_months,
      n_days = groups$n_days,
      method_used = method_used,
      status_row = .md_fit_status_row(
        "optim_failed", paste("optimizer failed:", optim_msg),
        p = p, rank = rg$rank, n_months = groups$n_months,
        method_used = method_used, converged = FALSE
      )
    ))
  }

  names(beta) <- colnames(X)
  H <- md_hessian(beta, S, X, groups)
  # Observed information = -Hessian for maximization objective
  info <- -H
  pd <- .md_safe_chol_pd(info)
  vcov <- matrix(NA_real_, p, p)
  if (isTRUE(pd$ok) || (is.finite(pd$cond) && all(eigen(0.5 * (info + t(info)),
                                                       symmetric = TRUE,
                                                       only.values = TRUE)$values > 0))) {
    vcov <- tryCatch(solve(info), error = function(e) matrix(NA_real_, p, p))
  }
  dimnames(vcov) <- list(colnames(X), colnames(X))

  # Quasi-Poisson dispersion from monthly Pearson residuals
  mm <- md_month_means(beta, X, groups)
  pearson <- (S - mm$mu) / sqrt(pmax(mm$mu, 1e-12))
  df_resid <- max(groups$n_months - p, 1L)
  dispersion <- sum(pearson^2, na.rm = TRUE) / df_resid
  if (!is.finite(dispersion) || dispersion <= 0) dispersion <- 1
  vcov_quasi <- vcov * dispersion
  dimnames(vcov_quasi) <- dimnames(vcov)

  ll <- md_loglik(beta, S, X, groups, include_factorial = TRUE)
  status <- if (isTRUE(pd$ok)) "ok" else "hessian_issue"
  msg <- if (isTRUE(pd$ok)) {
    "converged"
  } else {
    paste0("converged_with_hessian:", pd$message)
  }

  list(
    converged = TRUE,
    status = status,
    message = msg,
    beta = beta,
    vcov = vcov,
    vcov_quasi = if (isTRUE(quasi)) vcov_quasi else vcov,
    dispersion = dispersion,
    hessian = H,
    information = info,
    hessian_pd = isTRUE(pd$ok),
    hessian_condition = pd$cond,
    loglik = ll,
    mu = mm$mu,
    groups = groups,
    rank = rg$rank,
    p = p,
    n_months = groups$n_months,
    n_days = groups$n_days,
    method_used = method_used,
    X = X,
    S = S,
    status_row = .md_fit_status_row(
      status, msg,
      p = p, rank = rg$rank, n_months = groups$n_months,
      method_used = method_used, converged = TRUE,
      hessian_pd = isTRUE(pd$ok),
      hessian_condition = pd$cond,
      dispersion = dispersion
    )
  )
}

# ---------------------------------------------------------------------------
# Coefficient / CI / prediction extractors
# ---------------------------------------------------------------------------

md_coef <- function(fit, use_quasi = TRUE) {
  if (is.null(fit$beta) || all(is.na(fit$beta))) {
    return(data.frame(
      term = character(0),
      estimate = numeric(0),
      se = numeric(0),
      conf_low = numeric(0),
      conf_high = numeric(0),
      stringsAsFactors = FALSE
    ))
  }
  V <- if (isTRUE(use_quasi)) fit$vcov_quasi else fit$vcov
  se <- sqrt(pmax(diag(V), 0))
  data.frame(
    term = names(fit$beta) %||% paste0("b", seq_along(fit$beta)),
    estimate = as.numeric(fit$beta),
    se = as.numeric(se),
    conf_low = as.numeric(fit$beta - 1.96 * se),
    conf_high = as.numeric(fit$beta + 1.96 * se),
    stringsAsFactors = FALSE
  )
}

md_exposure_ci <- function(fit,
                          exposure_name = "exposure",
                          use_quasi = TRUE,
                          contrast = 1) {
  cf <- md_coef(fit, use_quasi = use_quasi)
  row <- cf[cf$term == exposure_name, , drop = FALSE]
  if (!nrow(row)) {
    return(data.frame(
      term = exposure_name,
      estimate = NA_real_,
      se = NA_real_,
      conf_low = NA_real_,
      conf_high = NA_real_,
      rr = NA_real_,
      rr_low = NA_real_,
      rr_high = NA_real_,
      contrast = contrast,
      stringsAsFactors = FALSE
    ))
  }
  est <- row$estimate[[1]] * contrast
  se <- row$se[[1]] * abs(contrast)
  data.frame(
    term = exposure_name,
    estimate = est,
    se = se,
    conf_low = est - 1.96 * se,
    conf_high = est + 1.96 * se,
    rr = exp(est),
    rr_low = exp(est - 1.96 * se),
    rr_high = exp(est + 1.96 * se),
    contrast = contrast,
    stringsAsFactors = FALSE
  )
}

#' Predict month means or daily intensities from a fitted M|D object.
md_predict <- function(fit, newdata_X = NULL, type = c("month", "day")) {
  type <- match.arg(type)
  if (is.null(fit$beta) || any(!is.finite(fit$beta))) {
    return(rep(NA_real_, if (type == "month") fit$n_months %||% 0L else fit$n_days %||% 0L))
  }
  X <- if (is.null(newdata_X)) fit$X else as.matrix(newdata_X)
  if (type == "day") {
    return(as.numeric(exp(X %*% fit$beta) * fit$groups$offset))
  }
  mm <- md_month_means(fit$beta, X, fit$groups)
  mm$mu
}

# Fallback %||% if utils not sourced
if (!exists("%||%", mode = "function")) {
  `%||%` <- function(x, y) {
    if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
  }
}
