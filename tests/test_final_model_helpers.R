#!/usr/bin/env Rscript
# tests/test_final_model_helpers.R
# In-memory SYNTHETIC_CALIBRATION fixtures only. Does not write release outputs.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "final_model_helpers.R"))

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

make_synthetic_panel <- function(outcome = "chd", seed = 1L, mean_level = 80) {
  set.seed(seed)
  grid <- make_month_grid(2013L, 1L, 2023L, 12L)
  n <- nrow(grid)
  expect_equal(n, 132L, paste0(outcome, " fixture length"))

  # Seasonal temperature + mild extremes
  mean_temp <- 24 + 6 * sin(2 * pi * (grid$month - 1) / 12) +
    stats::rnorm(n, 0, 0.7)
  mean_tmax <- mean_temp + 3 + stats::rnorm(n, 0, 0.3)
  mean_tmin <- mean_temp - 3 + stats::rnorm(n, 0, 0.3)
  hot_nights <- pmax(0, round(2 + 4 * pmax(mean_tmin - 26, 0) + stats::rpois(n, 0.5)))
  very_hot_days <- pmax(0, round(1 + 3 * pmax(mean_tmax - 31, 0) + stats::rpois(n, 0.3)))
  cold_days <- pmax(0, round(2 + 3 * pmax(14 - mean_tmin, 0) + stats::rpois(n, 0.4)))

  season <- 0.15 * sin(2 * pi * (grid$time_index) / 12)
  trend <- -0.002 * grid$time_index
  heat_eff <- if (identical(outcome, "chd")) 0.02 * (hot_nights / 5) else 0
  cold_eff <- if (identical(outcome, "hf")) 0.03 * (cold_days / 5) else 0
  mu <- exp(log(mean_level) + season + trend + heat_eff + cold_eff +
              log(pmax(grid$days_in_month, 1)) - log(30))
  theta <- if (identical(outcome, "chd")) 12 else 8
  n_events <- stats::rnbinom(n, mu = mu, size = theta)

  covid_phase <- ifelse(grid$year < 2020, "pre",
                        ifelse(grid$year == 2020, "acute", "later"))
  flu <- rep(NA_real_, n)
  # flu covers most but not all months (complete-case rule)
  flu[seq_len(121)] <- pmax(0, stats::rnorm(121, 1, 0.4))

  data.frame(
    month_id = grid$month_id,
    month_date = grid$month_date,
    year = grid$year,
    month = grid$month,
    time_index = grid$time_index,
    days_in_month = grid$days_in_month,
    n_events = as.integer(n_events),
    population = 5000000 + round(seq_len(n) * 50),
    mean_temp = mean_temp,
    mean_tmax = mean_tmax,
    mean_tmin = mean_tmin,
    hot_nights = as.numeric(hot_nights),
    cold_days = as.numeric(cold_days),
    very_hot_days = as.numeric(very_hot_days),
    absolute_humidity = 15 + 5 * sin(2 * pi * grid$month / 12) + stats::rnorm(n, 0, 0.5),
    NO2 = 40 + stats::rnorm(n, 0, 5),
    PM25 = 20 + stats::rnorm(n, 0, 3),
    O3 = 30 + stats::rnorm(n, 0, 4),
    covid_phase = covid_phase,
    flu_indicator = flu,
    data_status = SYNTHETIC_PROVENANCE,
    stringsAsFactors = FALSE
  )
}

# Packages used by helpers (do not install here if missing: parent owns install).
required_pkgs <- c("MASS", "splines", "dplyr", "yaml")
for (p in required_pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) {
    stop("Test requires package ", p, " (parent installs; this file must not install)")
  }
}
has_sandwich <- requireNamespace("sandwich", quietly = TRUE)
has_glarma <- requireNamespace("glarma", quietly = TRUE)

registry <- load_final_model_registry()
specs <- core_exposure_specs(registry)
scenarios <- scenario_defs(registry)

chd_raw <- make_synthetic_panel("chd", seed = 11L, mean_level = 90)
hf_raw <- make_synthetic_panel("hf", seed = 22L, mean_level = 45)

# Real provenance must be rejected for require_real=TRUE on synthetic fixtures.
expect_true(
  inherits(tryCatch(
    prepare_analysis_panel(chd_raw, require_real = TRUE, outcome = "chd"),
    error = function(e) e
  ), "error"),
  "require_real=TRUE rejects SYNTHETIC_CALIBRATION"
)

chd <- prepare_analysis_panel(chd_raw, require_real = FALSE, outcome = "chd")
hf <- prepare_analysis_panel(hf_raw, require_real = FALSE, outcome = "hf")
expect_equal(nrow(chd), 132L, "chd prepared rows")
expect_equal(nrow(hf), 132L, "hf prepared rows")
expect_equal(panel_provenance_label(chd), SYNTHETIC_PROVENANCE, "synthetic label")
expect_true(
  !identical(panel_provenance_label(chd), REAL_PROVENANCE),
  "synthetic is never HA_APPROVED_AGGREGATE"
)

# Term naming
expect_equal(exposure_term_name("mean_temp", 1), "mean_temp", "term scale 1")
expect_equal(exposure_term_name("hot_nights", 5), "I(hot_nights/5)", "term scale 5")

# ---- NB SE ladder ------------------------------------------------------------
if (has_sandwich) {
  ladder <- fit_nb_se_ladder(
    chd,
    exposure_term_name("hot_nights", 5),
    control_terms_from_registry(c("calendar_month_factor", "ns_time_df4")),
    offset_policy = "days_only",
    metadata = list(
      outcome = "chd",
      pathway_id = "P04A",
      data_status = SYNTHETIC_PROVENANCE,
      result_class = "SYNTHETIC_TEST"
    )
  )
  expect_true(isTRUE(ladder$ok), "NB SE ladder OK")
  expect_true(all(SE_METHODS_LADDER %in% ladder$estimates$se_method), "all SE methods present")
  expect_equal(unique(ladder$estimates$data_status), SYNTHETIC_PROVENANCE, "ladder provenance")
  expect_true(identical(ladder$status$status, "OK"), "ladder status OK")
} else {
  message("SKIP NB SE ladder assertions: sandwich not installed")
}

# ---- Scenarios including cold-only flu skip ---------------------------------
r12 <- scenarios[["R12_influenza_cold"]]
skip_heat <- apply_scenario(chd, r12, "P04A", specs[["P04A"]], registry)
expect_true(isTRUE(skip_heat$skip), "R12 skips non-cold exposure")
expect_equal(skip_heat$status, "SKIPPED", "R12 skip status")

fit_r12_cold <- fit_scenario_nb(
  hf, "P04B", specs[["P04B"]], r12, registry,
  data_status = SYNTHETIC_PROVENANCE,
  result_class = "SYNTHETIC_TEST"
)
expect_true(
  fit_r12_cold$status$status %in% c("OK", "FAILED"),
  "R12 cold returns status (never silent)"
)
expect_true(!is.null(fit_r12_cold$status$message), "R12 cold status has message field")

# Spot-check a few other frozen scenarios return status rows
for (sid in c(
  "R01_baseline_ns4", "R05_calendar_month_anomaly", "R06_season_restricted",
  "R08_pre_covid", "R15_lead_1_placebo", "R16_lead_2_placebo", "R14_exclude_max_cooks"
)) {
  fit <- fit_scenario_nb(
    chd, "P04A", specs[["P04A"]], scenarios[[sid]], registry,
    data_status = SYNTHETIC_PROVENANCE,
    result_class = "SYNTHETIC_TEST"
  )
  expect_true(
    fit$status$status %in% c("OK", "FAILED", "SKIPPED"),
    paste0(sid, " returns explicit status")
  )
  if (identical(fit$status$status, "OK") && !is.null(fit$estimates)) {
    expect_true(
      all(fit$estimates$data_status == SYNTHETIC_PROVENANCE),
      paste0(sid, " keeps synthetic provenance")
    )
  }
}

# ---- Stacked contrast --------------------------------------------------------
if (has_sandwich) {
  stacked <- fit_stacked_heat_cold_contrast(
    chd, hf,
    result_class = "SYNTHETIC_TEST"
  )
  expect_true(isTRUE(stacked$ok), paste0(
    "stacked contrast fits fixture: ", stacked$status$message
  ))
  expect_true("estimate" %in% names(stacked$contrast), "stacked delta present")
  expect_equal(
    stacked$contrast$data_status, SYNTHETIC_PROVENANCE,
    "stacked synthetic provenance"
  )
  expect_true(
    !identical(stacked$contrast$data_status, REAL_PROVENANCE),
    "stacked never labelled HA_APPROVED_AGGREGATE on synthetic"
  )
} else {
  message("SKIP stacked contrast assertions: sandwich not installed")
}

# ---- Prediction folds --------------------------------------------------------
term <- exposure_term_name("hot_nights", 5)
controls <- control_terms_from_registry(c("calendar_month_factor", "ns_time_df4"))
loyo <- score_loyo_nb(
  chd, term, controls, "days_only",
  metadata = list(outcome = "chd", pathway_id = "P04A", data_status = SYNTHETIC_PROVENANCE)
)
expect_true(!is.null(loyo$status), "loyo status present")
expect_true(nrow(loyo$status) >= 1L, "loyo status rows")
expect_true(!is.null(loyo$scores) && nrow(loyo$scores) == 11L, "all LOYO folds score")
expect_true(all(c("log_score_diff", "deviance_baseline", "mae_exposure") %in% names(loyo$scores)),
            "loyo score columns")
expect_true(all(loyo$scores$data_status == SYNTHETIC_PROVENANCE), "loyo provenance")

roll <- score_rolling_origin_nb(
  chd, term, controls, "days_only",
  horizon = 12L, min_train = 60L,
  metadata = list(outcome = "chd", pathway_id = "P04A", data_status = SYNTHETIC_PROVENANCE)
)
expect_true(!is.null(roll$status), "rolling status present")
expect_true(!is.null(roll$scores) && nrow(roll$scores) > 10L, "rolling folds score")

# ---- Serial-null generation --------------------------------------------------
base <- fit_baseline_nb_mu_theta(chd, controls, "days_only")
sims <- simulate_serial_null_counts(base$mu, base$theta, n_reps = 3L, seed = 99L)
expect_equal(dim(sims), c(132L, 3L), "serial-null sim shape")
expect_true(all(sims >= 0), "serial-null non-negative counts")

block_sims <- simulate_block_residual_null(
  chd$n_events, base$mu, base$theta, n_reps = 2L, block_length = 6L, seed = 5L
)
expect_equal(dim(block_sims), c(132L, 2L), "block-null sim shape")

# Tiny max-stat loop (does not write files)
if (has_sandwich) {
  tiny <- run_serial_null_max_stat(
    chd,
    fit_one_rep = function(d) {
      fit_nb_se_ladder(
        d, term, controls, "days_only",
        se_methods = "model",
        metadata = list(data_status = SYNTHETIC_PROVENANCE)
      )
    },
    n_reps = 2L,
    method = "parametric_nb",
    seed = 7L
  )
  expect_equal(length(tiny$max_stats), 2L, "max-stat length")
  expect_true(nrow(tiny$status) == 2L, "max-stat status rows")
}

# ---- GLARMA helper (if available) --------------------------------------------
if (has_glarma) {
  gfit <- fit_nb_glarma_ensemble(
    chd, term, controls, "days_only",
    metadata = list(
      outcome = "chd", pathway_id = "P04A",
      data_status = SYNTHETIC_PROVENANCE, result_class = "SYNTHETIC_TEST"
    )
  )
  expect_true(!is.null(gfit$status), "glarma status present")
  expect_true(!is.null(gfit$diagnostics), "glarma diagnostics present")
  expect_true(
    all(gfit$diagnostics$model_id %in% c(
      "M02_GLARMA_AR1", "M03_GLARMA_MA1", "M04_GLARMA_ARMA11"
    )),
    "glarma candidate ids"
  )
  if (!is.null(gfit$estimates)) {
    expect_true(
      all(gfit$estimates$data_status == SYNTHETIC_PROVENANCE),
      "glarma synthetic provenance"
    )
  }
} else {
  # Helper must still return a FAILED status without throwing.
  g_one <- fit_glarma_negbin_candidate(
    chd, term, controls, "days_only",
    phi_lags = 1L, model_id = "M02_GLARMA_AR1"
  )
  expect_equal(g_one$diagnostics$status, "FAILED", "glarma missing-package status")
  expect_true(grepl("glarma", g_one$diagnostics$message, ignore.case = TRUE),
              "glarma missing-package message")
  message("SKIP full GLARMA ensemble assertions: glarma not installed")
}

# ---- No writes to release_chd_hf ---------------------------------------------
release_after <- if (dir.exists(release_dir)) {
  list.files(release_dir, recursive = TRUE, full.names = TRUE)
} else {
  character(0)
}
expect_equal(release_after, release_before, "no writes under outputs/release_chd_hf")

message("test_final_model_helpers.R: ALL CHECKS PASSED")
