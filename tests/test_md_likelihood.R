#!/usr/bin/env Rscript
# tests/test_md_likelihood.R
# Unit tests for clean-room M|D likelihood and calibration helpers.
# In-memory SYNTHETIC_CALIBRATION only. Does not write release outputs.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
source(file.path("scripts", "md_calibration_helpers.R"))

expect_true <- function(x, label) {
  if (!isTRUE(x)) stop("FAILED: ", label, " [got: ", paste(x, collapse = ","), "]")
}

expect_equal <- function(x, y, label, tolerance = 1e-8) {
  if (!isTRUE(all.equal(x, y, tolerance = tolerance, check.attributes = FALSE))) {
    stop(
      "FAILED: ", label,
      "\nexpected: ", paste(utils::head(y, 20), collapse = ","),
      "\nactual: ", paste(utils::head(x, 20), collapse = ",")
    )
  }
}

expect_false <- function(x, label) expect_true(!isTRUE(x), label)

release_dir <- file.path(project_root(), "outputs", "release_chd_hf")
release_before <- if (dir.exists(release_dir)) {
  list.files(release_dir, recursive = TRUE, full.names = TRUE)
} else {
  character(0)
}

# ---------------------------------------------------------------------------
# No agr_* vendored implementation
# ---------------------------------------------------------------------------
agr <- list.files(
  project_root(),
  pattern = "(^|/)agr_.*\\.(R|r|c|cpp|h)$",
  recursive = TRUE,
  full.names = TRUE
)
expect_equal(length(agr), 0L, "no agr_* source files")

# ---------------------------------------------------------------------------
# Manual likelihood identity
# ---------------------------------------------------------------------------
dates <- c(
  seq(as.Date("2015-01-01"), as.Date("2015-01-31"), by = "day"),
  seq(as.Date("2015-02-01"), as.Date("2015-02-28"), by = "day")
)
month_id <- format(dates, "%Y-%m")
X <- cbind(intercept = 1)
beta <- log(3)
groups <- md_prepare_groups(month_id, rep(1, length(dates)))
S <- c(`2015-01` = 93, `2015-02` = 84)  # 31*3, 28*3
ll <- md_loglik(beta, S, X, groups, include_factorial = TRUE)
ll_manual <- stats::dpois(93, 93, log = TRUE) + stats::dpois(84, 84, log = TRUE)
expect_equal(ll, ll_manual, "Poisson aggregate likelihood identity", tolerance = 1e-8)

# Offsets: double offset => double mean
groups2 <- md_prepare_groups(month_id, rep(2, length(dates)))
S2 <- c(`2015-01` = 186, `2015-02` = 168)
ll2 <- md_loglik(beta, S2, X, groups2, include_factorial = TRUE)
ll2_manual <- stats::dpois(186, 186, log = TRUE) + stats::dpois(168, 168, log = TRUE)
expect_equal(ll2, ll2_manual, "likelihood with known daily offset", tolerance = 1e-8)

# ---------------------------------------------------------------------------
# Analytic gradient vs finite differences
# ---------------------------------------------------------------------------
set.seed(11)
n <- 90L
d <- seq(as.Date("2016-01-01"), by = "day", length.out = n)
mid <- format(d, "%Y-%m")
Xg <- cbind(1, rnorm(n), rnorm(n))
colnames(Xg) <- c("intercept", "x1", "x2")
b <- c(0.5, -0.2, 0.15)
g <- md_prepare_groups(mid, rep(1, n))
lam <- exp(as.numeric(Xg %*% b))
S_g <- vapply(g$indices, function(idx) sum(stats::rpois(length(idx), lam[idx])), numeric(1))
names(S_g) <- g$month_id
analytic <- md_score(b, S_g, Xg, g)
eps <- 1e-6
fd <- sapply(seq_along(b), function(j) {
  bp <- bm <- b
  bp[j] <- bp[j] + eps
  bm[j] <- bm[j] - eps
  (md_loglik(bp, S_g, Xg, g) - md_loglik(bm, S_g, Xg, g)) / (2 * eps)
})
expect_equal(analytic, fd, "score vs finite differences", tolerance = 1e-4)

# ---------------------------------------------------------------------------
# Hessian symmetry + FD check on diagonal
# ---------------------------------------------------------------------------
H <- md_hessian(b, S_g, Xg, g)
expect_equal(H, t(H), "Hessian symmetry", tolerance = 1e-10)
# Mixed partial FD for H[1,2]
eps2 <- 1e-4
b_pp <- b; b_pm <- b; b_mp <- b; b_mm <- b
b_pp[1] <- b_pp[1] + eps2; b_pp[2] <- b_pp[2] + eps2
b_pm[1] <- b_pm[1] + eps2; b_pm[2] <- b_pm[2] - eps2
b_mp[1] <- b_mp[1] - eps2; b_mp[2] <- b_mp[2] + eps2
b_mm[1] <- b_mm[1] - eps2; b_mm[2] <- b_mm[2] - eps2
h12_fd <- (
  md_loglik(b_pp, S_g, Xg, g) - md_loglik(b_pm, S_g, Xg, g) -
    md_loglik(b_mp, S_g, Xg, g) + md_loglik(b_mm, S_g, Xg, g)
) / (4 * eps2 * eps2)
expect_equal(H[1, 2], h12_fd, "Hessian FD mixed partial", tolerance = 5e-3)

# ---------------------------------------------------------------------------
# Known-beta recovery with high counts
# ---------------------------------------------------------------------------
set.seed(99)
n_h <- 365L * 2L
dh <- seq(as.Date("2014-01-01"), by = "day", length.out = n_h)
midh <- format(dh, "%Y-%m")
xh <- stats::rbinom(n_h, 1, 0.15)
Xh <- cbind(intercept = 1, exposure = xh)
bt <- c(log(40), log(1.05))
lam_h <- exp(as.numeric(Xh %*% bt))
gh <- md_prepare_groups(midh, rep(1, n_h))
# Near-deterministic high counts (expected values)
Sh <- vapply(gh$indices, function(idx) sum(lam_h[idx]), numeric(1))
names(Sh) <- gh$month_id
fit <- md_fit(Sh, Xh, midh)
expect_true(isTRUE(fit$converged), "high-count recovery converged")
expect_equal(unname(fit$beta["exposure"]), bt[2], "exposure beta recovery", tolerance = 1e-2)
expect_true(isTRUE(fit$hessian_pd), "information positive definite")

# ---------------------------------------------------------------------------
# Unequal month lengths
# ---------------------------------------------------------------------------
mu <- md_month_means(bt, Xh, gh)$mu
# With constant exposure mean, longer months have larger mu
days <- vapply(gh$indices, length, integer(1))
# Correlation between days and mu should be strongly positive after removing exposure variation
expect_true(cor(days, mu) > 0.5, "month means track unequal lengths")

# ---------------------------------------------------------------------------
# p and rank guards
# ---------------------------------------------------------------------------
big <- matrix(stats::rnorm(n_h * 21), n_h, 21)
fit_big <- md_fit(Sh, big, midh)
expect_false(isTRUE(fit_big$converged), "p>20 rejected")
expect_equal(fit_big$status, "rank_or_p_guard", "p guard status")

dup <- cbind(intercept = 1, exposure = xh, exposure2 = xh)
fit_dup <- md_fit(Sh, dup, midh)
expect_false(isTRUE(fit_dup$converged), "rank-deficient rejected")
expect_equal(fit_dup$status, "rank_or_p_guard", "rank guard status")

# ---------------------------------------------------------------------------
# Constrained kernel sums
# ---------------------------------------------------------------------------
expect_equal(md_kernel_weight_sum("same_day"), 1, "same_day weights")
expect_equal(md_kernel_weight_sum("cumulative_0_5"), 1, "cum05 weights")
expect_equal(md_kernel_weight_sum("cumulative_0_21"), 1, "cum021 weights")
ev <- c(rep(0, 5), 1, rep(0, 25))
k <- md_kernel_cumulative_0_5(ev)
expect_equal(sum(k), 1, "mass preserved under equal-weight kernel", tolerance = 1e-12)
k21 <- md_kernel_cumulative_0_21(ev)
expect_equal(sum(k21), 1, "mass preserved lag0-21", tolerance = 1e-12)

# ---------------------------------------------------------------------------
# Design builder
# ---------------------------------------------------------------------------
Xd <- md_build_daily_design(dh, xh, include_covid = TRUE)
expect_true(ncol(Xd) <= MD_MAX_PARAMETERS, "design p<=20")
expect_true("exposure" %in% colnames(Xd), "exposure column present")
expect_true("harm_sin" %in% colnames(Xd) && "harm_cos" %in% colnames(Xd), "harmonics present")

# ---------------------------------------------------------------------------
# DGP provenance + margins parser smoke (disclosure summaries only)
# ---------------------------------------------------------------------------
paths <- md_default_summary_paths(project_root())
if (file.exists(paths$annual) && file.exists(paths$seasonal)) {
  margins <- md_parse_expected_monthly_margins("chd", root = project_root())
  expect_equal(nrow(margins), 132L, "132 synthetic expected months")
  expect_true(
    all(margins$data_status == MD_PROVENANCE_SYNTHETIC),
    "margins labelled SYNTHETIC_CALIBRATION"
  )
  expect_false(
    any(margins$data_status == "HA_APPROVED_AGGREGATE"),
    "margins not labelled as real HA"
  )
  expect_true(
    all(c(
      "trend_annual_total", "constant_annual_level", "covid_year_factor",
      "seasonal_share"
    ) %in% names(margins)),
    "margin components for depletion/COVID toggles present"
  )
  # Toggles must change the nuisance profile (not no-ops).
  dgrid <- seq(as.Date("2013-01-01"), as.Date("2023-12-31"), by = "day")
  n0 <- md_daily_nuisance_mean(margins, dgrid, depletion = FALSE, covid_on = FALSE)
  n_dep <- md_daily_nuisance_mean(margins, dgrid, depletion = TRUE, covid_on = FALSE)
  n_cov <- md_daily_nuisance_mean(margins, dgrid, depletion = FALSE, covid_on = TRUE)
  n_both <- md_daily_nuisance_mean(margins, dgrid, depletion = TRUE, covid_on = TRUE)
  expect_true(
    !isTRUE(all.equal(n0$mu_nuisance, n_dep$mu_nuisance)),
    "depletion toggle changes annual profile"
  )
  expect_true(
    !isTRUE(all.equal(n0$mu_nuisance, n_cov$mu_nuisance)),
    "covid toggle changes annual profile"
  )
  # With both on, year sums should track disclosed annual totals (seasonal shares).
  year_sum_both <- tapply(n_both$mu_nuisance, format(n_both$date, "%Y"), sum)
  ann <- utils::read.csv(paths$annual, stringsAsFactors = FALSE)
  ann <- ann[ann$outcome == "chd", ]
  expect_equal(
    as.numeric(year_sum_both[as.character(ann$year)]),
    as.numeric(ann$total_events),
    "depletion+covid reconstructs disclosed annual totals from components",
    tolerance = 1e-4
  )
}

w <- data.frame(
  date = dh,
  hot_night = xh,
  cold_day = 0L,
  stringsAsFactors = FALSE
)
umh <- unique(midh)
yrsh <- sort(unique(as.integer(substr(umh, 1, 4))))
trend_h <- setNames(9600 - 400 * (yrsh - min(yrsh)), as.character(yrsh))
covid_h <- setNames(rep(1, length(yrsh)), as.character(yrsh))
if (length(yrsh) >= 2L) covid_h[as.character(max(yrsh))] <- 0.85
margins_tiny <- data.frame(
  outcome = "chd",
  year = as.integer(substr(umh, 1, 4)),
  month = as.integer(substr(umh, 6, 7)),
  month_id = umh,
  seasonal_share = 1 / 12,
  annual_total = as.numeric(trend_h[substr(umh, 1, 4)]) *
    as.numeric(covid_h[substr(umh, 1, 4)]),
  trend_annual_total = as.numeric(trend_h[substr(umh, 1, 4)]),
  constant_annual_level = as.numeric(mean(trend_h)),
  covid_year_factor = as.numeric(covid_h[substr(umh, 1, 4)]),
  expected_count_trend = as.numeric(trend_h[substr(umh, 1, 4)]) / 12,
  days_in_month = as.integer(as.numeric(table(midh)[umh])),
  data_status = MD_PROVENANCE_SYNTHETIC,
  margin_source = "test_fixture",
  stringsAsFactors = FALSE
)
sim <- md_simulate_dgp(
  weather_daily = w,
  margins = margins_tiny,
  exposure_col = "hot_night",
  kernel = "cumulative_0_5",
  effect_name = "moderate",
  overdispersion_phi = 0.02,
  ar1_rho = 0.3,
  depletion = TRUE,
  covid_on = TRUE,
  seed = 20260810L
)
expect_equal(sim$data_status, MD_PROVENANCE_SYNTHETIC, "DGP provenance")
expect_true(is.finite(sim$beta_true), "beta_true finite")
expect_equal(
  sim$beta_true,
  log(1.08) / 5,
  "moderate effect target RR1.08/5",
  tolerance = 1e-12
)

# ---------------------------------------------------------------------------
# Scenario builder: 36 core cells + outcome-specific exposures
# ---------------------------------------------------------------------------
core <- md_build_scenarios(include_edge = FALSE)
expect_equal(nrow(core), 36L, "36 primary core cells")
expect_true(
  all(core$exposure_col[core$scale == "chd_like"] == "hot_night"),
  "CHD-like exposure is hot_night for every kernel"
)
expect_true(
  all(core$exposure_col[core$scale == "hf_like"] == "cold_day"),
  "HF-like exposure is cold_day for every kernel"
)
# Including cumulative_0_21 CHD cells must stay on hot_night
expect_true(
  all(core$exposure_col[core$scale == "chd_like" & core$kernel == "cumulative_0_21"] ==
        "hot_night"),
  "CHD lag0-21 still hot_night"
)
full <- md_build_scenarios(include_edge = TRUE)
expect_true(nrow(full) > 36L, "edge cells added")
expect_true(all(full$data_status == MD_PROVENANCE_SYNTHETIC), "scenario provenance")

params_chd <- md_scenario_params(
  data.frame(
    outcome = "chd", overdispersion = "outcome_matched",
    serial_dependence = "outcome_matched", depletion = "outcome_matched",
    covid_shock = "observed_pattern", stringsAsFactors = FALSE
  ),
  core_fit_path = file.path(project_root(), "outputs", "tables", "cvd_core_model_fit.csv")
)
params_hf <- md_scenario_params(
  data.frame(
    outcome = "hf", overdispersion = "outcome_matched",
    serial_dependence = "outcome_matched", depletion = "outcome_matched",
    covid_shock = "observed_pattern", stringsAsFactors = FALSE
  ),
  core_fit_path = file.path(project_root(), "outputs", "tables", "cvd_core_model_fit.csv")
)
expect_equal(params_chd$ar1_rho, 0.50, "CHD AR rho matches diagnostics")
expect_equal(params_hf$ar1_rho, 0.15, "HF AR rho matches diagnostics")
expect_true(params_hf$overdispersion_phi < 0.015, "HF phi is 1/theta without floor")

# Checkpoint separation by mode/reps
expect_true(
  md_checkpoint_path("/tmp", "CORE_01", "pilot", 100) !=
    md_checkpoint_path("/tmp", "CORE_01", "core", 500),
  "pilot and core checkpoints are distinct"
)
expect_equal(
  basename(md_checkpoint_path("/tmp", "CORE_01", "pilot", 100)),
  "CORE_01__mode-pilot__reps-100.csv",
  "checkpoint naming helper"
)

# COVID reference level
Xd <- md_build_daily_design(dh, xh, include_covid = TRUE)
expect_false("covid_pre_covid" %in% colnames(Xd), "pre_covid is design reference")

# Real-fit admission logic
expect_false(
  md_real_fit_admissible(list(converged = FALSE, hessian_pd = TRUE, hessian_condition = 1)),
  "admission requires convergence"
)
expect_false(
  md_real_fit_admissible(list(converged = TRUE, hessian_pd = FALSE, hessian_condition = 1)),
  "admission requires PD Hessian"
)
expect_false(
  md_real_fit_admissible(
    list(converged = TRUE, hessian_pd = TRUE, hessian_condition = 1e9),
    hessian_condition_max = 1e8
  ),
  "admission requires condition below gate"
)
expect_true(
  md_real_fit_admissible(
    list(converged = TRUE, hessian_pd = TRUE, hessian_condition = 1e3),
    hessian_condition_max = 1e8
  ),
  "admission accepts good fit"
)

# Non-finite evaluation fails explicitly (no silent month skip)
expect_true(
  inherits(try(md_month_means(c(NaN, 0), Xh, gh), silent = TRUE), "try-error"),
  "non-finite beta fails explicitly in month means"
)
# Large coefs are clamped to a finite evaluation rather than overflowing to NaN
ll_clamped <- tryCatch(
  md_loglik(c(40, 5), Sh, Xh, gh, include_factorial = FALSE),
  error = function(e) NA_real_
)
expect_true(is.finite(ll_clamped), "clamped large eta remains finite")

# ---------------------------------------------------------------------------
# 2-rep calibration smoke + explicit failures
# ---------------------------------------------------------------------------
rows <- list()
for (r in 1:2) {
  s <- md_simulate_dgp(
    weather_daily = w,
    margins = margins_tiny,
    exposure_col = "hot_night",
    kernel = "same_day",
    effect_name = "null",
    seed = 50L + r,
    depletion = FALSE,
    covid_on = FALSE,
    overdispersion_phi = 0
  )
  est <- md_run_estimators(s, estimators = c("oracle_daily", "md", "monthly_nb"))
  for (nm in names(est)) {
    rows[[length(rows) + 1L]] <- md_estimator_result_to_row(
      est[[nm]], core[1, ], r, s$beta_true
    )
  }
}
raw <- do.call(rbind, rows)
expect_true(all(raw$data_status == MD_PROVENANCE_SYNTHETIC), "raw metrics provenance")
expect_true(all(c("converged", "message", "estimator") %in% names(raw)), "status fields present")

# Forced failure must remain visible
forced <- .md_estimator_fail("md", "unit-test forced failure")
expect_false(forced$ok, "forced failure ok=FALSE")
expect_false(forced$converged, "forced failure converged=FALSE")

# Gate evaluator returns explicit PASS/FAIL without gaming
fake_metrics <- data.frame(
  estimator = "md",
  cell_class = "core",
  effect = "null",
  effect_name = "null",
  serial_dependence = "none",
  depletion = "none",
  covid_shock = "none",
  scenario_id = "CORE_01",
  convergence_rate = 0.5,
  type1 = 0.20,
  coverage = 0.50,
  relative_bias_abs = 0.50,
  false_sign = NA_real_,
  hessian_condition_median = 1e12,
  divergent_or_boundary_rate = 0.5,
  data_status = MD_PROVENANCE_SYNTHETIC,
  stringsAsFactors = FALSE
)
if (file.exists(file.path(project_root(), "analysis_plan", "final_model_registry.yml"))) {
  gates <- md_evaluate_gates(fake_metrics, root = project_root())
  expect_true(all(gates$data_status == MD_PROVENANCE_SYNTHETIC), "gate provenance")
  expect_true(any(grepl("^FAIL", gates$admission_decision)), "failed calibration is valid FAIL")
  expect_false(isTRUE(all(gates$passed)), "gates not gamed on bad metrics")
}

# ---------------------------------------------------------------------------
# No release pollution
# ---------------------------------------------------------------------------
release_after <- if (dir.exists(release_dir)) {
  list.files(release_dir, recursive = TRUE, full.names = TRUE)
} else {
  character(0)
}
expect_equal(
  sort(release_after),
  sort(release_before),
  "test did not write under outputs/release_chd_hf"
)

message("test_md_likelihood.R: all assertions passed.")
