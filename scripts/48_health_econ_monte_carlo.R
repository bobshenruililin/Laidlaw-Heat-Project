#!/usr/bin/env Rscript
# 48_health_econ_monte_carlo.R
# SYNTHETIC_CALIBRATION for the health-economics identification laboratory.
#
# Uses REAL public HKO monthly/daily temperature as the exposure path.
# Generates SYNTHETIC counts. Does not read HA health files.
# Does not invent findings. Gate 3 is not an input.
#
# Environment:
#   HE_MC_REPS      default 200
#   HE_MC_SEED      default 20260814
#   HE_MC_SCENARIOS all | survivors | smoke | cycle2
#   HE_MC_THETA     MASS NB2 theta (size); default 50  => kappa=0.02
#
# Master seed: 20260814. Every output row carries data_status=SYNTHETIC_CALIBRATION.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("MASS", "splines", "jsonlite"))

N_REPS <- as.integer(Sys.getenv("HE_MC_REPS", unset = "200"))
MASTER_SEED <- as.integer(Sys.getenv("HE_MC_SEED", unset = "20260814"))
SCENARIOS <- Sys.getenv("HE_MC_SCENARIOS", unset = "all")
NB_THETA <- as.numeric(Sys.getenv("HE_MC_THETA", unset = "50"))
if (!is.finite(N_REPS) || N_REPS < 1L) N_REPS <- 200L
if (!is.finite(MASTER_SEED)) MASTER_SEED <- 20260814L
if (!is.finite(NB_THETA) || NB_THETA <= 0) NB_THETA <- 50

out_dir <- file.path(root, "outputs", "health_econ")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

PROVENANCE <- "SYNTHETIC_CALIBRATION"
# Existing exploratory interval widths on the log-RR scale.
# Source: knowledge/2026-08-12_existing_data_insights.md. Gate 3 open. Not a freeze.
CI_HF_COLD_LOG <- log(1.144) - log(1.006)
CI_CHD_HN_LOG <- log(1.042) - log(1.002)
EPS_TRANSPORT <- log(1.05) # SYNTHETIC RTE tolerance
SEW_TOL <- log(1.10)       # SYNTHETIC SEW tolerance

rnb <- function(n, mu, theta = NB_THETA) {
  mu <- pmax(as.numeric(mu), 1e-8)
  stats::rnbinom(n, mu = mu, size = theta)
}

fit_aor <- function(y, x, month, time_index, days, extra = NULL) {
  dat <- data.frame(
    y = as.numeric(y),
    x = as.numeric(x),
    month_f = factor(month, levels = 1:12),
    time_index = as.numeric(time_index),
    days = as.numeric(days)
  )
  if (!is.null(extra)) {
    stopifnot(is.data.frame(extra), nrow(extra) == nrow(dat))
    dat <- cbind(dat, extra)
  }
  keep <- is.finite(dat$y) & is.finite(dat$x) & is.finite(dat$days) & dat$days > 0 &
    dat$y >= 0
  dat <- dat[keep, , drop = FALSE]
  if (nrow(dat) < 80L || length(unique(dat$month_f)) < 8L) {
    return(list(ok = FALSE, est = NA_real_, se = NA_real_, n = nrow(dat)))
  }
  rhs <- "month_f + splines::ns(time_index, df = 4) + x"
  extra_names <- setdiff(names(dat), c("y", "x", "month_f", "time_index", "days"))
  if (length(extra_names)) {
    rhs <- paste(c(rhs, extra_names), collapse = " + ")
  }
  fml <- as.formula(paste("y ~", rhs, "+ offset(log(days))"))
  fit <- tryCatch(
    suppressWarnings(MASS::glm.nb(fml, data = dat)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    fit <- tryCatch(
      suppressWarnings(stats::glm(fml, family = quasipoisson(), data = dat)),
      error = function(e) e
    )
  }
  if (inherits(fit, "error") || is.null(fit) || !inherits(fit, "lm")) {
    return(list(ok = FALSE, est = NA_real_, se = NA_real_, n = nrow(dat)))
  }
  cf <- tryCatch(summary(fit)$coefficients, error = function(e) NULL)
  if (is.null(cf) || !"x" %in% rownames(cf)) {
    return(list(ok = FALSE, est = NA_real_, se = NA_real_, n = nrow(dat)))
  }
  est <- unname(cf["x", "Estimate"])
  se <- unname(cf["x", "Std. Error"])
  list(
    ok = is.finite(est) && is.finite(se) && se > 0,
    est = est,
    se = se,
    n = nrow(dat),
    theta = if (!is.null(fit$theta)) unname(fit$theta) else NA_real_
  )
}

fit_aor_lags <- function(y, x, month, time_index, days) {
  n <- length(y)
  x1 <- c(NA_real_, x[-n])
  x2 <- c(NA_real_, NA_real_, x[-c((n - 1L):n)])
  dat <- data.frame(
    y = as.numeric(y),
    x = as.numeric(x),
    x1 = x1,
    x2 = x2,
    month_f = factor(month, levels = 1:12),
    time_index = as.numeric(time_index),
    days = as.numeric(days)
  )
  dat <- dat[stats::complete.cases(dat), , drop = FALSE]
  if (nrow(dat) < 80L) {
    return(list(ok = FALSE, b0 = NA_real_, b1 = NA_real_, b2 = NA_real_,
                se0 = NA_real_))
  }
  fml <- y ~ month_f + splines::ns(time_index, df = 4) + x + x1 + x2 +
    offset(log(days))
  fit <- tryCatch(
    suppressWarnings(MASS::glm.nb(fml, data = dat)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(ok = FALSE, b0 = NA_real_, b1 = NA_real_, b2 = NA_real_,
                se0 = NA_real_))
  }
  cf <- summary(fit)$coefficients
  need <- c("x", "x1", "x2")
  if (!all(need %in% rownames(cf))) {
    return(list(ok = FALSE, b0 = NA_real_, b1 = NA_real_, b2 = NA_real_,
                se0 = NA_real_))
  }
  list(
    ok = TRUE,
    b0 = unname(cf["x", "Estimate"]),
    b1 = unname(cf["x1", "Estimate"]),
    b2 = unname(cf["x2", "Estimate"]),
    se0 = unname(cf["x", "Std. Error"])
  )
}

fit_regime <- function(y, x, R, month, time_index, days) {
  dat <- data.frame(
    y = as.numeric(y),
    x = as.numeric(x),
    R = as.numeric(R),
    xR = as.numeric(x) * as.numeric(R),
    month_f = factor(month, levels = 1:12),
    time_index = as.numeric(time_index),
    days = as.numeric(days)
  )
  keep <- is.finite(dat$y) & is.finite(dat$x) & dat$days > 0
  dat <- dat[keep, , drop = FALSE]
  if (nrow(dat) < 80L) {
    return(list(ok = FALSE, b0 = NA_real_, dtheta = NA_real_, se_d = NA_real_))
  }
  fml <- y ~ month_f + splines::ns(time_index, df = 4) + x + R + xR +
    offset(log(days))
  fit <- tryCatch(
    suppressWarnings(MASS::glm.nb(fml, data = dat)),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(ok = FALSE, b0 = NA_real_, dtheta = NA_real_, se_d = NA_real_))
  }
  cf <- summary(fit)$coefficients
  if (!all(c("x", "xR") %in% rownames(cf))) {
    return(list(ok = FALSE, b0 = NA_real_, dtheta = NA_real_, se_d = NA_real_))
  }
  list(
    ok = TRUE,
    b0 = unname(cf["x", "Estimate"]),
    dtheta = unname(cf["xR", "Estimate"]),
    se_d = unname(cf["xR", "Std. Error"])
  )
}

load_monthly <- function() {
  path <- file.path(root, "data_processed", "exposures_monthly_2013_2023.csv")
  if (!file.exists(path)) stop("Missing monthly exposures: ", path)
  d <- utils::read.csv(path, stringsAsFactors = FALSE)
  d$month_date <- as.Date(d$month_date)
  d$month <- as.integer(d$month)
  d$year <- as.integer(d$year)
  d$time_index <- as.numeric(d$time_index)
  d$days <- as.numeric(d$expected_days)
  d$mean_temp <- as.numeric(d$mean_temp)
  d$hot_nights <- as.numeric(d$hot_nights)
  d$cold_days <- as.numeric(d$cold_days)
  d$hn5 <- d$hot_nights / 5
  d$cd5 <- d$cold_days / 5
  d$covid_R <- as.integer(d$month_date >= as.Date("2020-03-01") &
                            d$month_date <= as.Date("2022-12-01"))
  d$is_202002 <- as.integer(d$month_id == "2020-02")
  d$is_202202 <- as.integer(d$month_id == "2022-02")
  d
}

load_daily <- function() {
  path <- file.path(root, "data_processed", "md_daily_weather_design_2013_2023.csv")
  if (!file.exists(path)) stop("Missing daily HKO design: ", path)
  d <- utils::read.csv(path, stringsAsFactors = FALSE)
  d$date <- as.Date(d$date)
  d$tmean <- as.numeric(d$tmean)
  d$cold_day <- as.integer(d$cold_day)
  d$hot_night <- as.integer(d$hot_night)
  d$month_id <- as.character(d$month_id)
  d
}

macro_shock <- function(n, is_202002, is_202202, seed, xi = log(1.20)) {
  set.seed(seed)
  e <- numeric(n)
  nu <- stats::rnorm(n, 0, 0.25)
  for (t in seq_len(n)) {
    prev <- if (t == 1L) 0 else e[t - 1L]
    e[t] <- 0.4 * prev + nu[t]
  }
  xi * is_202002 + xi * is_202202 + e
}

mnar_keep <- function(y, x, frac_drop = 0.10, seed) {
  set.seed(seed)
  z <- as.numeric(scale(log1p(y))) + as.numeric(scale(abs(x)))
  # Calibrate intercept so mean keep ≈ 1 - frac_drop
  a0 <- stats::uniroot(
    function(a) mean(stats::plogis(a - 0.8 * z)) - (1 - frac_drop),
    interval = c(-8, 8)
  )$root
  stats::rbinom(length(y), 1, stats::plogis(a0 - 0.8 * z)) == 1
}

apply_keep <- function(y, keep) {
  y2 <- y
  y2[!keep] <- NA_real_
  y2
}

empty_row <- function(scenario, hypothesis, rep_id, extras = list()) {
  base <- list(
    scenario = scenario,
    hypothesis = hypothesis,
    rep = as.integer(rep_id),
    ok = FALSE,
    est = NA_real_,
    se = NA_real_,
    reject05 = NA,
    covers_true = NA,
    true_theta = NA_real_,
    stat_name = NA_character_,
    stat_value = NA_real_,
    data_status = PROVENANCE
  )
  modifyList(base, extras)
}

monthly <- load_monthly()
daily <- load_daily()
n <- nrow(monthly)
stopifnot(n == 132L)

season_log <- as.numeric(log(pmax(
  tapply(rep(1, n), monthly$month, function(z) 1)[as.character(monthly$month)],
  1
)))
# Crude seasonal shape for synthetic means: winter higher.
season_hf <- 0.18 * cos(2 * pi * (monthly$month - 1) / 12)

g_daily <- function(tmean, a, bc, bh, mmt = 26) {
  exp(a + bc * pmax(mmt - tmean, 0)^2 + bh * pmax(tmean - mmt, 0)^2)
}

calibrate_a <- function(target_month_mean, bc, bh, mmt = 26) {
  # Choose intercept so mean of monthly sums ≈ target.
  stats::optimize(function(a) {
    gy <- g_daily(daily$tmean, a, bc, bh, mmt)
    mu_m <- tapply(gy, daily$month_id, sum)
    (mean(mu_m) - target_month_mean)^2
  }, interval = c(-8, 8))$minimum
}

run_reps <- function(n_reps, fun) {
  rows <- vector("list", n_reps)
  for (r in seq_len(n_reps)) {
    rows[[r]] <- fun(r)
  }
  rows
}

results <- list()
push_rows <- function(xs) {
  results <<- c(results, xs)
}

want <- function(tag) {
  SCENARIOS == "all" ||
    (SCENARIOS == "survivors" && tag %in% c("HE-07", "HE-08", "HE-10", "HE-C2-10")) ||
    (SCENARIOS == "cycle2" && tag %in% c("HE-C2-10", "HE-C2-02", "HE-08")) ||
    (SCENARIOS == "smoke" && tag %in% c("HE-01", "HE-10"))
}

# ---- HE-01 size under depletion ------------------------------------------------
if (want("HE-01")) {
  message("HE-01 size under depletion")
  rhos <- c(0.6, 0.8, 1.0)
  for (rho in rhos) {
    for (kink in c(FALSE, TRUE)) {
      if (rho != 0.6 && kink) next
      scen <- sprintf("HE01_size_rho%02d%s", as.integer(rho * 10),
                      if (kink) "_kink2020" else "")
      rows <- run_reps(N_REPS, function(r) {
        set.seed(MASTER_SEED + 1000L + r + as.integer(rho * 100) + 17L * kink)
        x <- monthly$cd5
        S <- numeric(n + 1L)
        S[1] <- 220 * 80
        h0 <- 220 / mean(S[1] * monthly$days)
        y <- numeric(n)
        freeze <- kink & monthly$year == 2020
        for (t in seq_len(n)) {
          h <- h0 * exp(season_hf[t])
          p <- 1 - exp(-monthly$days[t] * h)
          p <- min(max(p, 1e-8), 0.5)
          y[t] <- stats::rbinom(1, size = max(as.integer(round(S[t])), 1L), prob = p)
          inflow_mean <- rho * S[t] * p
          if (freeze[t]) inflow_mean <- 0
          I <- stats::rpois(1, inflow_mean)
          S[t + 1L] <- max(S[t] - y[t] + I, 1)
        }
        fit <- fit_aor(y, x, monthly$month, monthly$time_index, monthly$days)
        extras <- list(
          true_theta = 0,
          reject05 = if (fit$ok) as.integer(abs(fit$est / fit$se) > 1.96) else NA,
          covers_true = if (fit$ok) as.integer(abs(fit$est) <= 1.96 * fit$se) else NA,
          stat_name = "size_reject",
          stat_value = if (fit$ok) as.numeric(abs(fit$est / fit$se) > 1.96) else NA_real_,
          rho = rho,
          kink2020 = as.integer(kink)
        )
        modifyList(empty_row(scen, "HE-01", r, list(
          ok = fit$ok, est = fit$est, se = fit$se
        )), extras)
      })
      push_rows(rows)
    }
  }
}

# ---- HE-03 daily censoring attenuation -----------------------------------------
if (want("HE-03")) {
  message("HE-03 daily capacity attenuation")
  # Use HF-like daily mean ~ 220/30.4
  daily_base <- 220 / mean(monthly$days)
  theta_true <- log(1.07)
  for (u in c(0.85, 0.95, 0.99)) {
    scen <- sprintf("HE03_u%03d", as.integer(u * 100))
    K <- ceiling(daily_base / u)
    rows <- run_reps(N_REPS, function(r) {
      set.seed(MASTER_SEED + 2000L + r + as.integer(u * 1000))
      # Daily log mean responds to cold_day
      lam <- daily_base * exp(theta_true * daily$cold_day +
                                0.18 * cos(2 * pi * (daily$month - 1) / 12))
      D <- stats::rpois(nrow(daily), lam)
      Q <- pmin(D, K)
      y_c <- as.numeric(tapply(Q, daily$month_id, sum)[monthly$month_id])
      y_u <- as.numeric(tapply(D, daily$month_id, sum)[monthly$month_id])
      fit_c <- fit_aor(y_c, monthly$cd5, monthly$month, monthly$time_index, monthly$days)
      fit_u <- fit_aor(y_u, monthly$cd5, monthly$month, monthly$time_index, monthly$days)
      att <- if (fit_c$ok && fit_u$ok && abs(fit_u$est) > 1e-8) {
        1 - fit_c$est / fit_u$est
      } else {
        NA_real_
      }
      modifyList(empty_row(scen, "HE-03", r, list(
        ok = isTRUE(fit_c$ok),
        est = fit_c$est,
        se = fit_c$se,
        true_theta = theta_true,
        reject05 = if (fit_c$ok) as.integer(abs(fit_c$est / fit_c$se) > 1.96) else NA,
        covers_true = if (fit_c$ok) {
          as.integer(abs(fit_c$est - theta_true) <= 1.96 * fit_c$se)
        } else {
          NA
        },
        stat_name = "relative_attenuation",
        stat_value = att,
        utilisation = u,
        K = K,
        est_uncensored = if (fit_u$ok) fit_u$est else NA_real_
      )), list())
    })
    push_rows(rows)
  }
}

# ---- HE-05 harvesting power ----------------------------------------------------
if (want("HE-05")) {
  message("HE-05 harvesting phi power")
  theta0 <- log(1.07)
  for (phi in c(0, 0.3, 0.6)) {
    scen <- sprintf("HE05_phi%02d", as.integer(phi * 10))
    b0 <- theta0
    b1 <- -0.60 * phi * theta0
    b2 <- -0.40 * phi * theta0
    x <- monthly$cd5
    x1 <- c(mean(x), x[-n])
    x2 <- c(mean(x), mean(x), x[-c((n - 1L):n)])[seq_len(n)]
    rows <- run_reps(N_REPS, function(r) {
      set.seed(MASTER_SEED + 3000L + r + as.integer(phi * 100))
      mu <- 220 * exp(season_hf + b0 * x + b1 * x1 + b2 * x2)
      y <- rnb(n, mu)
      fit <- fit_aor_lags(y, x, monthly$month, monthly$time_index, monthly$days)
      bsum <- if (fit$ok) fit$b0 + fit$b1 + fit$b2 else NA_real_
      # Implied phi from sum = (1-phi) b0  =>  phi = 1 - sum/b0
      phi_hat <- if (fit$ok && abs(fit$b0) > 1e-8) 1 - bsum / fit$b0 else NA_real_
      # Wald on H0: b1=b2=0 is not quite H0: phi=0; use sign of lag sum vs 0
      # when true phi>0, power = reject phi=0 via bsum < b0 (one-sided)
      reject_phi0 <- if (fit$ok) as.integer((fit$b1 + fit$b2) < -1.64 * abs(fit$se0) * 0.5) else NA
      modifyList(empty_row(scen, "HE-05", r, list(
        ok = isTRUE(fit$ok),
        est = if (fit$ok) bsum else NA_real_,
        se = fit$se0,
        true_theta = (1 - phi) * theta0,
        reject05 = reject_phi0,
        covers_true = if (fit$ok) {
          as.integer(abs(bsum - (1 - phi) * theta0) <= 1.96 * abs(fit$se0))
        } else {
          NA
        },
        stat_name = "phi_hat",
        stat_value = phi_hat,
        phi_true = phi,
        b0 = if (fit$ok) fit$b0 else NA_real_,
        b1 = if (fit$ok) fit$b1 else NA_real_,
        b2 = if (fit$ok) fit$b2 else NA_real_
      )), list())
    })
    push_rows(rows)
  }
}

# ---- HE-07 SEW -----------------------------------------------------------------
if (want("HE-07")) {
  message("HE-07 selection envelope")
  # True morbidity elasticity alpha_T = log(1.07) on cold days /5
  alpha_T <- log(1.07)
  omega0 <- 0.20
  z0 <- stats::qnorm(1 - omega0)
  phi_z <- stats::dnorm(z0)
  c_grid <- c(0, 0.15, 0.30, 0.45) # SYNTHETIC threshold movement
  x <- monthly$cd5
  x_s <- as.numeric(scale(x))
  rows <- list()
  idx <- 0L
  for (cT in c_grid) {
    for (stress in c("base", "macro", "mnar")) {
      for (r in seq_len(N_REPS)) {
        idx <- idx + 1L
        set.seed(MASTER_SEED + 4000L + idx)
        # epsilon_Y = alpha_T + mills * (bT - cT); we set bT=0, vary cT
        mills <- phi_z / omega0
        vis_term <- mills * (0 - cT) * 0.25 * x_s
        mu_m <- (220 / omega0) * exp(season_hf + alpha_T * x)
        M <- rnb(n, mu_m)
        z <- z0 + cT * x_s
        omega <- pmin(pmax(1 - stats::pnorm(z), 0.02), 0.95)
        y <- stats::rbinom(n, size = pmax(M, 0), prob = omega)
        if (stress == "macro") {
          U <- macro_shock(n, monthly$is_202002, monthly$is_202202,
                           MASTER_SEED + 4100L + r)
          y <- rnb(n, pmax(y, 1) * exp(U))
        }
        keep <- rep(TRUE, n)
        if (stress == "mnar") {
          keep <- mnar_keep(y, x, 0.10, MASTER_SEED + 4200L + r)
          y <- apply_keep(y, keep)
        }
        fit <- fit_aor(y, x, monthly$month, monthly$time_index, monthly$days)
        eps_y <- if (fit$ok) fit$est else NA_real_
        gap <- if (is.finite(eps_y)) alpha_T - eps_y else NA_real_
        rows[[idx]] <- modifyList(empty_row(
          sprintf("HE07_cT%02d_%s", as.integer(cT * 100), stress),
          "HE-07", r,
          list(
            ok = isTRUE(fit$ok),
            est = eps_y,
            se = fit$se,
            true_theta = alpha_T,
            reject05 = if (fit$ok) as.integer(abs(fit$est / fit$se) > 1.96) else NA,
            covers_true = if (fit$ok) {
              as.integer(abs(fit$est - alpha_T) <= 1.96 * fit$se)
            } else {
              NA
            },
            stat_name = "epsM_minus_epsY",
            stat_value = gap,
            cT = cT,
            stress = stress
          )
        ), list())
      }
    }
  }
  push_rows(rows)
}

# ---- HE-08 RTE -----------------------------------------------------------------
if (want("HE-08")) {
  message("HE-08 regime transportability")
  theta0 <- log(1.07)
  deltas <- c(0, log(1.03), -log(1.03))
  x <- monthly$cd5
  R <- monthly$covid_R
  for (dth in deltas) {
    for (stress in c("base", "macro", "mnar")) {
      scen <- sprintf("HE08_d%+03d_%s", as.integer(round(dth * 100)), stress)
      rows <- run_reps(N_REPS, function(r) {
        set.seed(MASTER_SEED + 5000L + r + as.integer(dth * 1000) +
                   nchar(stress))
        theta_t <- theta0 + dth * R
        mu <- 220 * exp(season_hf + theta_t * x - 0.15 * R)
        y <- rnb(n, mu)
        if (stress == "macro") {
          U <- macro_shock(n, monthly$is_202002, monthly$is_202202,
                           MASTER_SEED + 5100L + r)
          y <- rnb(n, mu * exp(U))
        }
        if (stress == "mnar") {
          keep <- mnar_keep(y, x, 0.10, MASTER_SEED + 5200L + r)
          y <- apply_keep(y, keep)
        }
        pooled <- fit_aor(y, x, monthly$month, monthly$time_index, monthly$days)
        reg <- fit_regime(y, x, R, monthly$month, monthly$time_index, monthly$days)
        rte <- if (reg$ok) abs(reg$dtheta) else NA_real_
        modifyList(empty_row(scen, "HE-08", r, list(
          ok = isTRUE(pooled$ok),
          est = pooled$est,
          se = pooled$se,
          true_theta = theta0,
          reject05 = if (reg$ok) as.integer(abs(reg$dtheta / reg$se_d) > 1.96) else NA,
          covers_true = if (pooled$ok) {
            as.integer(abs(pooled$est - theta0) <= 1.96 * pooled$se)
          } else {
            NA
          },
          stat_name = "RTE",
          stat_value = rte,
          delta_true = dth,
          stress = stress,
          b0 = if (reg$ok) reg$b0 else NA_real_,
          dtheta = if (reg$ok) reg$dtheta else NA_real_,
          se_d = if (reg$ok) reg$se_d else NA_real_
        )), list())
      })
      push_rows(rows)
    }
  }
}

# ---- HE-10 ADR on real daily HKO ----------------------------------------------
if (want("HE-10")) {
  message("HE-10 aggregation distortion")
  theta_cold <- log(1.07)
  bc <- theta_cold / 25
  bh <- theta_cold / 100
  a_hat <- calibrate_a(220, bc, bh)
  gy <- g_daily(daily$tmean, a_hat, bc, bh)
  mu_month <- as.numeric(tapply(gy, daily$month_id, sum)[monthly$month_id])
  g_bar <- g_daily(monthly$mean_temp, a_hat, bc, bh)
  mu_rep <- monthly$days * g_bar
  target_agg <- fit_aor(mu_month, monthly$mean_temp, monthly$month,
                        monthly$time_index, monthly$days)
  target_rep <- fit_aor(mu_rep, monthly$mean_temp, monthly$month,
                        monthly$time_index, monthly$days)
  beta_target <- target_agg$est
  beta_rep <- target_rep$est
  message(sprintf("HE-10 noiseless beta_agg=%.4f beta_rep=%.4f ok_agg=%s",
                  beta_target, beta_rep, target_agg$ok))

  for (stress in c("base", "macro", "mnar", "select")) {
    scen <- sprintf("HE10_mean_%s", stress)
    rows <- run_reps(N_REPS, function(r) {
      set.seed(MASTER_SEED + 6000L + r + nchar(stress))
      y_day <- stats::rpois(nrow(daily), gy)
      if (stress == "select") {
        keep_p <- stats::pnorm(-0.4 * scale(daily$tmean))
        y_day <- stats::rbinom(nrow(daily), y_day, pmin(pmax(keep_p, 0.2), 0.95))
      }
      y <- as.numeric(tapply(y_day, daily$month_id, sum)[monthly$month_id])
      if (stress == "macro") {
        U <- macro_shock(n, monthly$is_202002, monthly$is_202202,
                         MASTER_SEED + 6100L + r)
        y <- rnb(n, pmax(y, 1) * exp(U))
      }
      if (stress == "mnar") {
        keep <- mnar_keep(y, monthly$mean_temp, 0.10, MASTER_SEED + 6200L + r)
        y <- apply_keep(y, keep)
      }
      fit <- fit_aor(y, monthly$mean_temp, monthly$month, monthly$time_index,
                     monthly$days)
      adr <- if (fit$ok && is.finite(beta_target)) {
        abs(fit$est - beta_target) / (0.5 * CI_HF_COLD_LOG)
      } else {
        NA_real_
      }
      modifyList(empty_row(scen, "HE-10", r, list(
        ok = isTRUE(fit$ok),
        est = fit$est,
        se = fit$se,
        true_theta = beta_target,
        reject05 = if (fit$ok) as.integer(abs(fit$est / fit$se) > 1.96) else NA,
        covers_true = if (fit$ok && is.finite(beta_target)) {
          as.integer(abs(fit$est - beta_target) <= 1.96 * fit$se)
        } else {
          NA
        },
        stat_name = "ADR",
        stat_value = adr,
        stress = stress,
        beta_rep = beta_rep,
        beta_target = beta_target
      )), list())
    })
    push_rows(rows)
  }

  # Extreme-count family: generate from daily g, regress monthly on cold_days/5
  for (stress in c("base", "mnar")) {
    scen <- sprintf("HE10_cold_%s", stress)
    rows <- run_reps(N_REPS, function(r) {
      set.seed(MASTER_SEED + 6300L + r + nchar(stress))
      y_day <- stats::rpois(nrow(daily), gy)
      y <- as.numeric(tapply(y_day, daily$month_id, sum)[monthly$month_id])
      if (stress == "mnar") {
        keep <- mnar_keep(y, monthly$cd5, 0.10, MASTER_SEED + 6400L + r)
        y <- apply_keep(y, keep)
      }
      fit <- fit_aor(y, monthly$cd5, monthly$month, monthly$time_index, monthly$days)
      tgt <- fit_aor(mu_month, monthly$cd5, monthly$month, monthly$time_index,
                     monthly$days)$est
      adr <- if (fit$ok && is.finite(tgt)) {
        abs(fit$est - tgt) / (0.5 * CI_HF_COLD_LOG)
      } else {
        NA_real_
      }
      modifyList(empty_row(scen, "HE-10", r, list(
        ok = isTRUE(fit$ok),
        est = fit$est,
        se = fit$se,
        true_theta = tgt,
        covers_true = if (fit$ok && is.finite(tgt)) {
          as.integer(abs(fit$est - tgt) <= 1.96 * fit$se)
        } else {
          NA
        },
        stat_name = "ADR",
        stat_value = adr,
        stress = stress,
        exposure_family = "cold_days_per5"
      )), list())
    })
    push_rows(rows)
  }
}

# ---- HE-C2-10 signed CATD: truncation composed with aggregation ----------------
if (want("HE-C2-10")) {
  message("HE-C2-10 signed CATD composition")
  theta_cold <- log(1.07)
  bc <- theta_cold / 25
  bh <- theta_cold / 100
  a_hat <- calibrate_a(220, bc, bh)
  gy <- g_daily(daily$tmean, a_hat, bc, bh)
  mu_month <- as.numeric(tapply(gy, daily$month_id, sum)[monthly$month_id])
  beta_target <- fit_aor(mu_month, monthly$mean_temp, monthly$month,
                         monthly$time_index, monthly$days)$est
  daily_base <- mean(gy)
  for (u in c(0.85, 0.95, 1.05)) {
    for (seasonal_k in c(FALSE, TRUE)) {
      scen <- sprintf("HEC210_u%03d_%s", as.integer(u * 100),
                      if (seasonal_k) "Kseason" else "Kflat")
      K_flat <- daily_base / u
      rows <- run_reps(N_REPS, function(r) {
        set.seed(MASTER_SEED + 7000L + r + as.integer(u * 100) + 11L * seasonal_k)
        K <- if (seasonal_k) {
          K_flat * exp(0.12 * cos(2 * pi * (daily$month - 1) / 12))
        } else {
          rep(K_flat, nrow(daily))
        }
        D <- stats::rpois(nrow(daily), gy)
        Q <- pmin(D, K)
        y <- as.numeric(tapply(Q, daily$month_id, sum)[monthly$month_id])
        fit <- fit_aor(y, monthly$mean_temp, monthly$month, monthly$time_index,
                       monthly$days)
        catd <- if (fit$ok && is.finite(beta_target)) {
          (fit$est - beta_target) / (0.5 * CI_HF_COLD_LOG)
        } else {
          NA_real_
        }
        modifyList(empty_row(scen, "HE-C2-10", r, list(
          ok = isTRUE(fit$ok),
          est = fit$est,
          se = fit$se,
          true_theta = beta_target,
          covers_true = if (fit$ok && is.finite(beta_target)) {
            as.integer(abs(fit$est - beta_target) <= 1.96 * fit$se)
          } else {
            NA
          },
          stat_name = "CATD",
          stat_value = catd,
          utilisation = u,
          K_seasonal = as.integer(seasonal_k)
        )), list())
      })
      push_rows(rows)
    }
  }
}

# ---- HE-C2-02 dispersion profile (queue vs demand) -----------------------------
if (want("HE-C2-02")) {
  message("HE-C2-02 second-moment detection")
  daily_base <- 220 / mean(monthly$days)
  theta_true <- log(1.07)
  lam <- daily_base * exp(theta_true * daily$cold_day +
                            0.18 * cos(2 * pi * (daily$month - 1) / 12))
  for (family in c("demand", "queue")) {
    u <- 0.85
    K <- daily_base / u
    scen <- sprintf("HEC202_%s", family)
    rows <- run_reps(N_REPS, function(r) {
      set.seed(MASTER_SEED + 8000L + r + nchar(family))
      D <- stats::rpois(nrow(daily), lam)
      A <- if (family == "queue") pmin(D, K) else D
      y <- as.numeric(tapply(A, daily$month_id, sum)[monthly$month_id])
      fit <- fit_aor(y, monthly$cd5, monthly$month, monthly$time_index, monthly$days)
      # Dispersion profile: slope of squared Pearson resid on fitted mean.
      # Reconstruct fitted means from a Poisson GLM for residuals.
      dat <- data.frame(
        y = y,
        x = monthly$cd5,
        month_f = factor(monthly$month, levels = 1:12),
        time_index = monthly$time_index,
        days = monthly$days
      )
      g <- tryCatch(
        suppressWarnings(stats::glm(
          y ~ month_f + splines::ns(time_index, df = 4) + x + offset(log(days)),
          family = quasipoisson(), data = dat
        )),
        error = function(e) NULL
      )
      slope <- NA_real_
      if (!is.null(g)) {
        mu <- stats::fitted(g)
        pr <- (dat$y - mu)^2 / pmax(mu, 1e-6)
        slope <- tryCatch(unname(stats::coef(stats::lm(pr ~ mu))[["mu"]]),
                          error = function(e) NA_real_)
      }
      modifyList(empty_row(scen, "HE-C2-02", r, list(
        ok = isTRUE(fit$ok),
        est = fit$est,
        se = fit$se,
        true_theta = theta_true,
        stat_name = "dispersion_slope",
        stat_value = slope,
        family = family
      )), list())
    })
    push_rows(rows)
  }
}

# ---- bind, summarise, write ----------------------------------------------------
raw <- do.call(rbind, lapply(results, function(z) {
  # Harmonise columns
  as.data.frame(z, stringsAsFactors = FALSE)
}))

# Some rows have extra columns; rbind of data.frames with different cols is messy.
# Rebuild with union of names.
all_names <- unique(unlist(lapply(results, names)))
raw <- do.call(rbind, lapply(results, function(z) {
  miss <- setdiff(all_names, names(z))
  if (length(miss)) z[miss] <- NA
  as.data.frame(z[all_names], stringsAsFactors = FALSE)
}))
rownames(raw) <- NULL
raw$data_status <- PROVENANCE
raw$master_seed <- MASTER_SEED
raw$n_reps_requested <- N_REPS
raw$run_scenarios <- SCENARIOS

raw_path <- file.path(out_dir, "cycle1_mc_raw.csv")
utils::write.csv(raw, raw_path, row.names = FALSE)

summarise_one <- function(d) {
  ok <- d[isTRUE(d$ok) | d$ok %in% c(TRUE, 1, "TRUE"), , drop = FALSE]
  n_ok <- nrow(ok)
  qs <- function(v) {
    v <- as.numeric(v)
    v <- v[is.finite(v)]
    if (!length(v)) return(c(NA, NA, NA, NA, NA))
    c(stats::quantile(v, 0.05, names = FALSE),
      stats::quantile(v, 0.25, names = FALSE),
      stats::median(v),
      stats::quantile(v, 0.75, names = FALSE),
      stats::quantile(v, 0.95, names = FALSE))
  }
  qe <- qs(ok$est)
  qs_stat <- qs(ok$stat_value)
  data.frame(
    scenario = d$scenario[1],
    hypothesis = d$hypothesis[1],
    n_reps = nrow(d),
    n_ok = n_ok,
    frac_ok = n_ok / nrow(d),
    mean_est = mean(ok$est, na.rm = TRUE),
    mean_se = mean(ok$se, na.rm = TRUE),
    est_p05 = qe[1],
    est_p50 = qe[3],
    est_p95 = qe[5],
    mean_stat = mean(ok$stat_value, na.rm = TRUE),
    stat_p05 = qs_stat[1],
    stat_p50 = qs_stat[3],
    stat_p95 = qs_stat[5],
    empirical_size_or_power = mean(as.numeric(ok$reject05), na.rm = TRUE),
    coverage = mean(as.numeric(ok$covers_true), na.rm = TRUE),
    stat_name = unique(na.omit(as.character(d$stat_name)))[1],
    data_status = PROVENANCE,
    stringsAsFactors = FALSE
  )
}

summ <- do.call(rbind, lapply(split(raw, raw$scenario), summarise_one))
rownames(summ) <- NULL
summ_path <- file.path(out_dir, "cycle1_mc_summary.csv")
utils::write.csv(summ, summ_path, row.names = FALSE)

# Gates
he01 <- raw[raw$hypothesis == "HE-01" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
he03 <- raw[raw$hypothesis == "HE-03" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
he05 <- raw[raw$hypothesis == "HE-05" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
he07 <- raw[raw$hypothesis == "HE-07" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
he08 <- raw[raw$hypothesis == "HE-08" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
he10 <- raw[raw$hypothesis == "HE-10" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
c210 <- raw[raw$hypothesis == "HE-C2-10" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
c202 <- raw[raw$hypothesis == "HE-C2-02" & raw$ok %in% c(TRUE, 1, "TRUE"), ]

sew <- if (nrow(he07)) {
  v <- as.numeric(he07$stat_value)
  v <- v[is.finite(v)]
  if (length(v)) stats::quantile(v, 0.975, names = FALSE) -
    stats::quantile(v, 0.025, names = FALSE) else NA_real_
} else {
  NA_real_
}
ss <- if (nrow(he07)) {
  # SS = Pr(eps_M > 0); true alpha_T > 0 by construction. Sign of eps_Y.
  mean(he07$est > 0, na.rm = TRUE)
} else {
  NA_real_
}

adr95 <- if (nrow(he10)) {
  stats::quantile(as.numeric(he10$stat_value), 0.95, na.rm = TRUE, names = FALSE)
} else {
  NA_real_
}

gates <- list(
  provenance = PROVENANCE,
  master_seed = MASTER_SEED,
  n_reps = N_REPS,
  scenarios = SCENARIOS,
  monetisation_permitted = FALSE,
  gate3_input = FALSE,
  existing_interval_widths_log = list(
    hf_cold_days = CI_HF_COLD_LOG,
    chd_hot_nights = CI_CHD_HN_LOG,
    source = "EXISTING_EXPLORATORY_INTERVAL"
  ),
  HE01_size = if (nrow(he01)) mean(as.numeric(he01$reject05), na.rm = TRUE) else NA,
  HE01_size_gate = if (nrow(he01)) {
    sz <- mean(as.numeric(he01$reject05), na.rm = TRUE)
    if (is.finite(sz) && sz <= 0.10) "size_nominal_costing_caveat_only" else "size_inflated_identification_leak"
  } else {
    "not_run"
  },
  HE03_median_attenuation = if (nrow(he03)) {
    stats::median(as.numeric(he03$stat_value), na.rm = TRUE)
  } else {
    NA
  },
  HE05_power_phi06 = if (any(raw$scenario == "HE05_phi06", na.rm = TRUE)) {
    d <- raw[raw$scenario == "HE05_phi06" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
    mean(as.numeric(d$reject05), na.rm = TRUE)
  } else {
    NA
  },
  HE07_SEW = sew,
  HE07_SS = ss,
  HE07_gate = if (is.finite(sew) && is.finite(ss)) {
    if (ss >= 0.95 && sew <= SEW_TOL) "lower_bound_passes_synthetic_grid" else "lower_bound_fails"
  } else {
    "not_run"
  },
  HE08_RTE_p95_when_delta0 = if (any(grepl("HE08_d\\+000_base", raw$scenario), na.rm = TRUE)) {
    d <- raw[raw$scenario == "HE08_d+000_base" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
    stats::quantile(as.numeric(d$stat_value), 0.95, na.rm = TRUE, names = FALSE)
  } else {
    NA
  },
  HE08_power_when_delta_log103 = if (any(grepl("HE08_d\\+003_base", raw$scenario), na.rm = TRUE)) {
    d <- raw[raw$scenario == "HE08_d+003_base" & raw$ok %in% c(TRUE, 1, "TRUE"), ]
    mean(as.numeric(d$reject05), na.rm = TRUE)
  } else {
    NA
  },
  HE10_ADR_p95 = unname(adr95),
  HE10_gate = if (is.finite(adr95)) {
    if (adr95 < 1) "cosmetic_under_imposed_g" else "projection_validity_fails"
  } else {
    "not_run"
  },
  HEC210_CATD_p05 = if (nrow(c210)) {
    stats::quantile(as.numeric(c210$stat_value), 0.05, na.rm = TRUE, names = FALSE)
  } else {
    NA
  },
  HEC210_CATD_p95 = if (nrow(c210)) {
    stats::quantile(as.numeric(c210$stat_value), 0.95, na.rm = TRUE, names = FALSE)
  } else {
    NA
  },
  HEC210_sign_flip = if (nrow(c210)) {
    q05 <- stats::quantile(as.numeric(c210$stat_value), 0.05, na.rm = TRUE, names = FALSE)
    q95 <- stats::quantile(as.numeric(c210$stat_value), 0.95, na.rm = TRUE, names = FALSE)
    is.finite(q05) && is.finite(q95) && (q05 * q95 < 0)
  } else {
    NA
  },
  HEC202_demand_slope = if (nrow(c202)) {
    d <- c202[c202$family == "demand", ]
    mean(as.numeric(d$stat_value), na.rm = TRUE)
  } else {
    NA
  },
  HEC202_queue_slope = if (nrow(c202)) {
    d <- c202[c202$family == "queue", ]
    mean(as.numeric(d$stat_value), na.rm = TRUE)
  } else {
    NA
  },
  notes = c(
    "All count series are SYNTHETIC. Exposure path is REAL_PUBLIC_HKO.",
    "No HA microdata were read. No stroke file. No currency.",
    "A passing size test does not revive a KILL on an unobserved stock level.",
    "ADR/CATD are conditional on an imposed daily g; they do not recover a daily coefficient."
  )
)

jsonlite::write_json(gates, file.path(out_dir, "cycle1_mc_gates.json"),
                     auto_unbox = TRUE, pretty = TRUE)

status <- data.frame(
  timestamp = as.character(Sys.time()),
  status = "ok",
  n_rows = nrow(raw),
  n_scenarios = length(unique(raw$scenario)),
  n_reps = N_REPS,
  scenarios = SCENARIOS,
  master_seed = MASTER_SEED,
  data_status = PROVENANCE,
  stringsAsFactors = FALSE
)
utils::write.csv(status, file.path(out_dir, "cycle1_mc_status.csv"), row.names = FALSE)

message("Wrote ", raw_path)
message("Wrote ", summ_path)
message("Scenarios: ", paste(unique(raw$scenario), collapse = ", "))
