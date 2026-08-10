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
X <- matrix(1, nrow = length(dates), ncol = 1L)
colnames(X) <- "intercept"
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
expect_true(
  all(paste0("month_", sprintf("%02d", 2:12)) %in% colnames(Xd)),
  "calendar-month indicators present"
)

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
expect_true(
  md_checkpoint_path("/tmp", "CORE_01", "core", 500, "F1.0") !=
    md_checkpoint_path("/tmp", "CORE_01", "core", 500, "F1.1"),
  "calibration design versions use distinct checkpoints"
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
# Warning capture for estimator wrappers
# ---------------------------------------------------------------------------
cap <- .md_with_captured_warnings({
  warning("theta.ml: iteration limit reached")
  "done"
})
expect_equal(cap$value, "done", "warning capture returns expression value")
expect_true(
  any(grepl("theta\\.ml|iteration limit", cap$warnings, ignore.case = TRUE)),
  "captured warning text retained"
)
expect_true(
  .md_serious_fit_warning(c("theta.ml: iteration limit reached")),
  "theta.ml iteration limit classified serious"
)
expect_true(
  .md_serious_fit_warning(c("alternation limit reached")),
  "alternation limit classified serious"
)
expect_false(
  .md_serious_fit_warning(c("harmless calibration note")),
  "ordinary non-convergence note not classified serious"
)
# Deliberate: non-serious warning stays successful but annotated
cap_ok <- .md_with_captured_warnings({
  warning("harmless calibration note")
  42
})
expect_equal(cap_ok$value, 42, "non-serious warning still returns value")
expect_equal(
  .md_message_with_warnings("ok", cap_ok$warnings),
  "ok | warnings: harmless calibration note",
  "non-serious warning annotated into message"
)

# ---------------------------------------------------------------------------
# 2-rep calibration smoke + explicit failures (no console warning flood)
# ---------------------------------------------------------------------------
rows <- list()
leaked <- character(0)
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
  est <- withCallingHandlers(
    md_run_estimators(s, estimators = c("oracle_daily", "md", "monthly_nb")),
    warning = function(w) {
      leaked <<- c(leaked, conditionMessage(w))
      tryInvokeRestart("muffleWarning")
    }
  )
  for (nm in names(est)) {
    rows[[length(rows) + 1L]] <- md_estimator_result_to_row(
      est[[nm]], core[1, ], r, s$beta_true
    )
    # Serious NB warnings must fail explicitly, not masquerade as ok
    if (grepl("theta\\.ml|alternation limit|iteration limit",
              est[[nm]]$message %||% "", ignore.case = TRUE)) {
      expect_false(isTRUE(est[[nm]]$ok), paste(nm, "serious warning => ok=FALSE"))
      expect_false(isTRUE(est[[nm]]$converged), paste(nm, "serious warning => not converged"))
    }
  }
}
expect_equal(length(leaked), 0L, "estimator wrappers emit no console warning flood")
raw <- do.call(rbind, rows)
expect_true(all(raw$data_status == MD_PROVENANCE_SYNTHETIC), "raw metrics provenance")
expect_true(all(c("converged", "message", "estimator") %in% names(raw)), "status fields present")
expect_true(all(nzchar(as.character(raw$message))), "every estimator row has message")

# Forced failure must remain visible
forced <- .md_estimator_fail("md", "unit-test forced failure")
expect_false(forced$ok, "forced failure ok=FALSE")
expect_false(forced$converged, "forced failure converged=FALSE")

# Gate evaluator: worst-cell F1.2 rules (averages must not rescue a bad cell)
fake_goodish <- data.frame(
  estimator = "md",
  cell_class = "core",
  effect = c("null", "null", "small", "moderate"),
  effect_name = c("null", "null", "small", "moderate"),
  serial_dependence = c("none", "outcome_matched", "none", "none"),
  depletion = "outcome_matched",
  covid_shock = "observed_pattern",
  scenario_id = c("CORE_A", "CORE_B", "CORE_C", "CORE_D"),
  convergence_rate = c(0.99, 0.99, 0.99, 0.99),
  type1 = c(0.05, 0.20, NA_real_, NA_real_),  # CORE_B fails Type I
  coverage = c(0.95, 0.95, 0.94, 0.93),
  relative_bias_abs = c(NA_real_, NA_real_, 0.05, 0.05),
  false_sign = c(NA_real_, NA_real_, NA_real_, 0.02),
  hessian_condition_median = c(10, 10, 10, 10),
  divergent_or_boundary_rate = c(0.01, 0.01, 0.01, 0.01),
  data_status = MD_PROVENANCE_SYNTHETIC,
  stringsAsFactors = FALSE
)
# Add explicit stress edge with low coverage
fake_stress <- data.frame(
  estimator = "md",
  cell_class = "edge",
  effect = "null",
  effect_name = "null",
  serial_dependence = "none",
  depletion = "none",
  covid_shock = "none",
  scenario_id = "EDGE_covid_off",
  convergence_rate = 0.99,
  type1 = 0.05,
  coverage = 0.70,  # fails stress coverage if selected
  relative_bias_abs = NA_real_,
  false_sign = NA_real_,
  hessian_condition_median = 10,
  divergent_or_boundary_rate = 0.01,
  data_status = MD_PROVENANCE_SYNTHETIC,
  stringsAsFactors = FALSE
)
fake_metrics <- rbind(fake_goodish, fake_stress)
if (file.exists(file.path(project_root(), "analysis_plan", "final_model_registry.yml"))) {
  gates <- md_evaluate_gates(fake_metrics, root = project_root())
  expect_true(all(gates$data_status == MD_PROVENANCE_SYNTHETIC), "gate provenance")
  expect_true(any(grepl("^FAIL", gates$admission_decision)), "failed calibration is valid FAIL")
  expect_false(isTRUE(all(gates$passed)), "gates not gamed on bad metrics")
  type1_row <- gates[gates$gate_id == "type1_range", , drop = FALSE]
  expect_true(nrow(type1_row) == 1L && isFALSE(type1_row$passed[[1]]), "Type I fails on worst null cell")
  expect_true(
    grepl("CORE_B", type1_row$failing_scenario_ids[[1]]),
    "Type I detail lists failing scenario ID"
  )
  # Average Type I would be (0.05+0.20)/2=0.125 still fail, but ensure worst-cell
  # also catches when only one cell is out of band while mean might look ok:
  fake_mean_ok <- fake_metrics
  fake_mean_ok$type1[fake_mean_ok$scenario_id == "CORE_A"] <- 0.04
  fake_mean_ok$type1[fake_mean_ok$scenario_id == "CORE_B"] <- 0.09
  fake_mean_ok$coverage[fake_mean_ok$scenario_id == "EDGE_covid_off"] <- 0.90
  fake_mean_ok$relative_bias_abs[fake_mean_ok$effect != "null"] <- 0.05
  fake_mean_ok$false_sign[fake_mean_ok$effect == "moderate"] <- 0.02
  g2 <- md_evaluate_gates(fake_mean_ok, root = project_root())
  expect_false(
    g2$passed[g2$gate_id == "type1_range"][[1]],
    "Type I fails when any null cell is outside [0.03,0.08] even if others are fine"
  )
  stress <- md_stress_metric_rows(fake_metrics)
  expect_true(
    all(c("CORE_B", "EDGE_covid_off") %in% stress$scenario_id) &&
      !"CORE_A" %in% stress$scenario_id,
    "stress set is AR-on core + EDGE depletion/covid/stress only"
  )
  rep_lines <- md_format_f12_decision_report(fake_metrics, gates)
  expect_true(any(grepl("FAIL_METHODS_FEASIBILITY_ONLY", rep_lines)), "report shows FAIL")
  expect_true(any(grepl("Per-cell null Type I", rep_lines)), "report has null Type I section")
}

# Nonadmissible M|D (non-PD / ill-conditioned) counts as divergent, excluded from Type I
adm_met <- md_metrics_from_replicates(
  estimates = c(0.01, -0.02, 0.00, 0.03),
  se = c(0.01, 0.01, 0.01, 0.01),
  conf_low = c(-0.01, -0.04, -0.02, 0.01),
  conf_high = c(0.03, 0.00, 0.02, 0.05),
  beta_true = 0,
  effect_name = "null",
  converged = c(TRUE, TRUE, TRUE, TRUE),
  hessian_pd = c(TRUE, TRUE, FALSE, TRUE),
  hessian_condition = c(10, 10, 10, 1e12),
  estimator = "md",
  target_comparable = TRUE,
  hessian_condition_max = 1e8
)
expect_equal(adm_met$n_converged, 2L, "only PD+condition-ok M|D rows admissible")
expect_true(adm_met$divergent_or_boundary_rate == 0.5, "nonadmissible counted as divergent")
# Among admissible (rows 1-2): reject only if CI excludes 0 -> row1 no, row2 no => type1 0
# row2: conf_high=0 so (lo>0)|(hi<0) is FALSE; type1 uses admissible only
expect_true(is.finite(adm_met$type1), "Type I computed on admissible subset")
expect_true(isTRUE(adm_met$target_comparable), "M|D target comparable")

# Comparator noncomparability
nb_met <- md_metrics_from_replicates(
  estimates = c(0.1, 0.2),
  se = c(0.05, 0.05),
  conf_low = c(0, 0.1),
  conf_high = c(0.2, 0.3),
  beta_true = 0,
  effect_name = "null",
  converged = c(TRUE, TRUE),
  estimator = "monthly_nb",
  target_comparable = FALSE
)
expect_false(isTRUE(nb_met$target_comparable[[1]]), "monthly_nb not target-comparable")
expect_true(is.na(nb_met$bias) && is.na(nb_met$coverage) && is.na(nb_met$type1),
            "noncomparable beta metrics are NA")
expect_true(is.finite(nb_met$convergence_rate) && is.finite(nb_met$se_mean),
            "noncomparable still reports convergence/SE")
expect_false(md_estimator_target_comparable("spillover_burden"), "spillover noncomparable")
expect_false(md_estimator_target_comparable("glarma_ar1"), "glarma noncomparable")
expect_true(md_estimator_target_comparable("oracle_daily"), "oracle comparable")

# summarise helper factors out of script 43
tiny_raw <- data.frame(
  scenario_id = "CORE_01",
  cell_class = "core",
  scale = "chd_like",
  outcome = "chd",
  effect = "null",
  effect_name = "null",
  kernel = "same_day",
  serial_dependence = "none",
  depletion = "outcome_matched",
  covid_shock = "observed_pattern",
  overdispersion = "outcome_matched",
  exposure_col = "hot_night",
  rep_id = 1:2,
  estimator = c("md", "monthly_nb"),
  ok = TRUE,
  message = "ok",
  estimate = c(0.01, 0.5),
  se = c(0.02, 0.1),
  conf_low = c(-0.03, 0.3),
  conf_high = c(0.05, 0.7),
  converged = TRUE,
  hessian_pd = TRUE,
  hessian_condition = 5,
  dispersion = 1,
  loglik = c(-10, -12),
  beta_true = 0,
  target_mapping = c("md", "monthly"),
  data_status = MD_PROVENANCE_SYNTHETIC,
  stringsAsFactors = FALSE
)
summ_tiny <- md_summarise_scenario_raw(tiny_raw)
expect_true(nrow(summ_tiny) == 2L, "summarise returns one row per estimator")
expect_true(
  isTRUE(summ_tiny$target_comparable[summ_tiny$estimator == "md"]) &&
    !isTRUE(summ_tiny$target_comparable[summ_tiny$estimator == "monthly_nb"]),
  "summarise sets target_comparable by estimator"
)

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
