#!/usr/bin/env Rscript
# 44_md_smoke_checks.R
# Fast manual smoke checks for clean-room M|D suite.
# Does not write SYNTHETIC artifacts under outputs/release_chd_hf.
# Asserts no agr_* vendored copies.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
source(file.path("scripts", "md_calibration_helpers.R"))
root <- project_root()
setwd(root)

failures <- character(0)
ok <- function(msg) message("OK  ", msg)
fail <- function(msg) {
  message("FAIL  ", msg)
  failures <<- c(failures, msg)
}

expect_true <- function(x, label) {
  if (!isTRUE(x)) fail(label) else ok(label)
}

# ---------------------------------------------------------------------------
# No vendored agr_* / aggregated copies; no synthetic under release_chd_hf
# ---------------------------------------------------------------------------
agr_hits <- list.files(
  root,
  pattern = "(^agr_)|(/agr_)",
  recursive = TRUE,
  full.names = TRUE
)
# Ignore this smoke script's own pattern string if any file match is only docs
agr_code <- agr_hits[grepl("\\.(R|r|c|cpp|h|py|jl)$", agr_hits)]
expect_true(length(agr_code) == 0L, "no agr_* source files vendored")

release_dir <- file.path(root, "outputs", "release_chd_hf")
if (dir.exists(release_dir)) {
  syn_rel <- list.files(
    release_dir,
    pattern = "SYNTHETIC",
    recursive = TRUE,
    full.names = TRUE
  )
  expect_true(
    length(syn_rel) == 0L,
    "no SYNTHETIC artifacts under outputs/release_chd_hf"
  )
} else {
  ok("release_chd_hf absent (nothing to pollute)")
}

# ---------------------------------------------------------------------------
# Likelihood identity on a tiny known example
# ---------------------------------------------------------------------------
# Two months: Jan 31 days, Feb 28 days; constant lambda.
dates <- c(seq(as.Date("2013-01-01"), as.Date("2013-01-31"), by = "day"),
           seq(as.Date("2013-02-01"), as.Date("2013-02-28"), by = "day"))
month_id <- format(dates, "%Y-%m")
X <- matrix(1, nrow = length(dates), ncol = 1L)
colnames(X) <- "intercept"
beta <- log(2)
offset <- rep(1, length(dates))
groups <- md_prepare_groups(month_id, offset)
# True month means: 31*2 and 28*2
S <- c(62, 56)
names(S) <- groups$month_id
ll <- md_loglik(beta, S, X, groups, include_factorial = TRUE)
ll_manual <- dpois(62, 62, log = TRUE) + dpois(56, 56, log = TRUE)
expect_true(
  isTRUE(all.equal(ll, ll_manual, tolerance = 1e-8)),
  "manual likelihood identity at true beta"
)

# ---------------------------------------------------------------------------
# Analytic gradient vs finite differences
# ---------------------------------------------------------------------------
set.seed(1)
n <- 120L
dates2 <- seq(as.Date("2013-01-01"), by = "day", length.out = n)
mid2 <- format(dates2, "%Y-%m")
X2 <- cbind(
  intercept = 1,
  x1 = rnorm(n),
  x2 = rnorm(n)
)
beta2 <- c(0.2, 0.1, -0.05)
g <- md_prepare_groups(mid2, rep(1, n))
lam <- exp(as.numeric(X2 %*% beta2))
S2 <- vapply(g$indices, function(idx) sum(rpois(length(idx), lam[idx])), numeric(1))
names(S2) <- g$month_id
sc <- md_score(beta2, S2, X2, g)
eps <- 1e-5
fd <- numeric(3)
for (j in 1:3) {
  bp <- bm <- beta2
  bp[j] <- bp[j] + eps
  bm[j] <- bm[j] - eps
  fd[j] <- (md_loglik(bp, S2, X2, g) - md_loglik(bm, S2, X2, g)) / (2 * eps)
}
expect_true(
  isTRUE(all.equal(sc, fd, tolerance = 1e-4)),
  "analytic score matches finite differences"
)

# ---------------------------------------------------------------------------
# Hessian symmetry
# ---------------------------------------------------------------------------
H <- md_hessian(beta2, S2, X2, g)
expect_true(
  isTRUE(all.equal(H, t(H), tolerance = 1e-10)),
  "Hessian symmetry"
)

# ---------------------------------------------------------------------------
# Known-beta recovery with high counts
# ---------------------------------------------------------------------------
set.seed(42)
n3 <- 365L * 3L
dates3 <- seq(as.Date("2013-01-01"), by = "day", length.out = n3)
mid3 <- format(dates3, "%Y-%m")
xexp <- as.numeric(rbinom(n3, 1, 0.2))
X3 <- cbind(intercept = 1, exposure = xexp)
beta_true <- c(log(50), 0.08)  # high daily mean
lam3 <- exp(as.numeric(X3 %*% beta_true))
g3 <- md_prepare_groups(mid3, rep(1, n3))
# Use expected counts (near-deterministic high counts) for recovery check
S3 <- vapply(g3$indices, function(idx) sum(lam3[idx]), numeric(1))
names(S3) <- g3$month_id
fit <- md_fit(S3, X3, mid3)
expect_true(isTRUE(fit$converged), "high-count fit converged")
expect_true(
  isTRUE(all.equal(unname(fit$beta["exposure"]), beta_true[2], tolerance = 5e-3)),
  "known-beta recovery (exposure)"
)

# ---------------------------------------------------------------------------
# Unequal month lengths handled by daily sum
# ---------------------------------------------------------------------------
mu_hat <- md_predict(fit, type = "month")
expect_true(length(mu_hat) == length(S3), "prediction length = n_months")
# February means should be smaller than January when rates equal — check structure
jan <- grepl("-01$", names(S3))
feb <- grepl("-02$", names(S3))
if (any(jan) && any(feb)) {
  expect_true(
    mean(mu_hat[jan]) > mean(mu_hat[feb]),
    "unequal month lengths: Jan mean > Feb mean under steady daily rate"
  )
}

# ---------------------------------------------------------------------------
# p / rank guards
# ---------------------------------------------------------------------------
set.seed(2)
Xp <- matrix(rnorm(n * 21), n, 21)
colnames(Xp) <- paste0("b", seq_len(21))
fit_p <- md_fit(S2, Xp, mid2)
expect_true(
  identical(fit_p$status, "rank_or_p_guard") || !isTRUE(fit_p$converged),
  "p>20 guard rejects oversized design"
)

Xrank <- cbind(1, x = X2[, 2], x_dup = X2[, 2])
colnames(Xrank) <- c("intercept", "x", "x_dup")
fit_r <- md_fit(S2, Xrank, mid2)
expect_true(
  identical(fit_r$status, "rank_or_p_guard") || !isTRUE(fit_r$converged),
  "rank guard rejects singular design"
)

# ---------------------------------------------------------------------------
# Constrained kernel weight sums
# ---------------------------------------------------------------------------
expect_true(md_kernel_weight_sum("same_day") == 1, "same_day weight sum 1")
expect_true(md_kernel_weight_sum("cumulative_0_5") == 1, "0-5 weight sum 1")
expect_true(md_kernel_weight_sum("cumulative_0_21") == 1, "0-21 weight sum 1")
ev <- c(1, 0, 0, 0, 0, 0, 0)
k5 <- md_kernel_cumulative_0_5(ev)
expect_true(
  isTRUE(all.equal(k5[1], 1 / 6, tolerance = 1e-12)),
  "normalized cumulative 0-5 on single event day"
)
expect_true(
  isTRUE(all.equal(k5[6], 1 / 6, tolerance = 1e-12)),
  "normalized cumulative 0-5 lag-5 day"
)
expect_true(isTRUE(all.equal(k5[7], 0, tolerance = 1e-12)), "zero after window")

# ---------------------------------------------------------------------------
# DGP provenance + toggleable depletion/COVID margins
# ---------------------------------------------------------------------------
# Tiny synthetic weather
w <- data.frame(
  date = dates3,
  hot_night = as.integer(xexp > 0.5),
  cold_day = 0L,
  stringsAsFactors = FALSE
)
um3 <- unique(mid3)
yrs3 <- sort(unique(as.integer(substr(um3, 1, 4))))
# Declining trend + COVID dip in last year of fixture window
trend_map <- setNames(12000 - 500 * (yrs3 - min(yrs3)), as.character(yrs3))
covid_map <- setNames(rep(1, length(yrs3)), as.character(yrs3))
if (length(yrs3) >= 3L) covid_map[as.character(max(yrs3))] <- 0.8
margins <- data.frame(
  outcome = "chd",
  year = as.integer(substr(um3, 1, 4)),
  month = as.integer(substr(um3, 6, 7)),
  month_id = um3,
  seasonal_share = 1 / 12,
  annual_total = as.numeric(trend_map[substr(um3, 1, 4)]) *
    as.numeric(covid_map[substr(um3, 1, 4)]),
  trend_annual_total = as.numeric(trend_map[substr(um3, 1, 4)]),
  constant_annual_level = as.numeric(mean(trend_map)),
  covid_year_factor = as.numeric(covid_map[substr(um3, 1, 4)]),
  expected_count_trend = as.numeric(trend_map[substr(um3, 1, 4)]) / 12,
  days_in_month = as.integer(as.numeric(table(mid3)[um3])),
  data_status = MD_PROVENANCE_SYNTHETIC,
  margin_source = "smoke_fixture",
  stringsAsFactors = FALSE
)
nuis_base <- md_daily_nuisance_mean(margins, dates3, depletion = FALSE, covid_on = FALSE)
nuis_dep <- md_daily_nuisance_mean(margins, dates3, depletion = TRUE, covid_on = FALSE)
nuis_cov <- md_daily_nuisance_mean(margins, dates3, depletion = FALSE, covid_on = TRUE)
expect_true(
  !isTRUE(all.equal(nuis_base$mu_nuisance, nuis_dep$mu_nuisance)),
  "depletion=TRUE changes daily nuisance vs flat level"
)
expect_true(
  !isTRUE(all.equal(nuis_base$mu_nuisance, nuis_cov$mu_nuisance)),
  "covid_on=TRUE changes daily nuisance vs no COVID factor"
)
sim <- md_simulate_dgp(
  weather_daily = w,
  margins = margins,
  exposure_col = "hot_night",
  kernel = "same_day",
  effect_name = "small",
  overdispersion_phi = 0.01,
  ar1_rho = 0,
  depletion = FALSE,
  covid_on = FALSE,
  seed = 7L
)
expect_true(
  identical(sim$data_status, MD_PROVENANCE_SYNTHETIC),
  "DGP provenance SYNTHETIC_CALIBRATION"
)
expect_true(length(sim$S) == length(unique(mid3)), "DGP month aggregation length")

# ---------------------------------------------------------------------------
# Outcome-specific exposure mapping + checkpoint separation
# ---------------------------------------------------------------------------
core_sc <- md_build_scenarios(include_edge = FALSE)
expect_true(
  all(core_sc$exposure_col[core_sc$scale == "chd_like"] == "hot_night"),
  "CHD-like uses hot_night for all kernels"
)
expect_true(
  all(core_sc$exposure_col[core_sc$scale == "hf_like"] == "cold_day"),
  "HF-like uses cold_day for all kernels"
)
expect_true(
  md_checkpoint_path("x", "CORE_01", "pilot", 100) !=
    md_checkpoint_path("x", "CORE_01", "core", 500),
  "checkpoint paths differ by mode/reps"
)

# ---------------------------------------------------------------------------
# 2-rep calibration smoke (in-memory; no release writes)
# ---------------------------------------------------------------------------
set.seed(20260810)
sc <- core_sc[1, , drop = FALSE]
expect_true(nrow(core_sc) == 36L, "36 core scenarios")
reps <- lapply(1:2, function(r) {
  s <- md_simulate_dgp(
    weather_daily = w,
    margins = margins,
    exposure_col = "hot_night",
    kernel = sc$kernel[[1]],
    effect_name = sc$effect[[1]],
    seed = 1000L + r,
    depletion = FALSE,
    covid_on = FALSE,
    overdispersion_phi = 0.01
  )
  md_fit_md_estimator(s)
})
expect_true(
  all(vapply(reps, function(z) is.logical(z$converged), logical(1))),
  "2-rep calibration smoke returns explicit convergence flags"
)
# Failures must be explicit
bad <- .md_estimator_fail("md", "forced failure")
expect_true(isFALSE(bad$ok) && identical(bad$converged, FALSE), "explicit failure preserved")

# Real-fit Hessian admission helper
expect_true(
  isFALSE(md_real_fit_admissible(list(
    converged = TRUE, hessian_pd = FALSE, hessian_condition = 1
  ))),
  "admission rejects non-PD Hessian"
)
expect_true(
  isFALSE(md_real_fit_admissible(list(
    converged = TRUE, hessian_pd = TRUE, hessian_condition = 1e12
  ), hessian_condition_max = 1e8)),
  "admission rejects condition above gate"
)
expect_true(
  isTRUE(md_real_fit_admissible(list(
    converged = TRUE, hessian_pd = TRUE, hessian_condition = 10
  ), hessian_condition_max = 1e8)),
  "admission accepts converged PD fit under condition gate"
)

# COVID design reference is pre_covid (not alphabetical first)
Xd_cov <- md_build_daily_design(dates3, xexp, include_covid = TRUE)
cov_cols <- grep("^covid_", colnames(Xd_cov), value = TRUE)
expect_true(
  !"covid_pre_covid" %in% cov_cols,
  "pre_covid is reference (no dummy column)"
)
expect_true(
  any(grepl("early_covid|fifth_wave|late_2022|post_reopening", cov_cols)),
  "non-reference COVID levels present"
)

# ---------------------------------------------------------------------------
# Design p<=20
# ---------------------------------------------------------------------------
covid_fixture <- rep("pre_covid", length(dates3))
covid_fixture[seq.int(floor(length(dates3) / 2), length(dates3))] <- "early_covid"
Xd <- md_build_daily_design(
  dates3,
  xexp,
  covid_phase = covid_fixture,
  include_covid = TRUE
)
expect_true(ncol(Xd) <= MD_MAX_PARAMETERS, "daily design p<=20")

if (length(failures)) {
  message("SMOKE FAILED: ", length(failures), " checks")
  for (f in failures) message("  - ", f)
  quit(save = "no", status = 1)
}
message("All M|D smoke checks passed.")
