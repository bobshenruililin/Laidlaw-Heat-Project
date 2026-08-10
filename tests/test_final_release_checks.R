#!/usr/bin/env Rscript
# tests/test_final_release_checks.R
# Lightweight fixture tests for release-check helpers.
# Does not modify outputs/release_chd_hf/ and does not read governed panels.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "release_check_helpers.R"))

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

# Guard: never touch the canonical release from this test file.
release_dir <- file.path(project_root(), "outputs", "release_chd_hf")
release_before <- if (dir.exists(release_dir)) {
  info <- file.info(list.files(release_dir, recursive = TRUE, full.names = TRUE))
  sum(info$size, na.rm = TRUE)
} else {
  NA_real_
}

# ---- BH / ledger identity ----------------------------------------------------
p <- c(0.04, 0.20, 0.01, 0.50)
q <- recompute_bh_q_values(p)
expect_equal(q, p.adjust(p, method = "BH"), "BH helper matches p.adjust")

bh <- bh_q_identity(p, q)
expect_true(bh$ok, "bh_q_identity PASS on matching q")
bh_bad <- bh_q_identity(p, q + 0.01)
expect_false(bh_bad$ok, "bh_q_identity FAIL on drifted q")

table2 <- data.frame(
  outcome = rep(c("chd", "hf"), each = 6),
  pathway_id = rep(CORE_PATHWAY_IDS, 2),
  rr = seq(0.95, 1.06, length.out = 12),
  rr_low = seq(0.90, 1.01, length.out = 12),
  rr_high = seq(1.00, 1.11, length.out = 12),
  p_value = p[c(1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4)],
  q_value_core_bh = NA_real_,
  se_method = "NeweyWest_lag6",
  data_status = RELEASE_REAL_PROVENANCE,
  stringsAsFactors = FALSE
)
table2$q_value_core_bh <- recompute_bh_q_values(table2$p_value)
table2$outcome_label <- unname(OUTCOME_LABELS_RELEASE[table2$outcome])
table2$contrast <- unname(CORE_EXPOSURE_LABELS[table2$pathway_id])

ledger <- table2
ledger$claim_id <- sprintf("CVD-%02d", seq_len(12))
ledger$provenance <- RELEASE_REAL_PROVENANCE
ledger$claim_text <- mapply(
  claim_text_from_row,
  ledger$outcome_label,
  ledger$contrast,
  ledger$rr,
  ledger$rr_low,
  ledger$rr_high,
  USE.NAMES = FALSE
)

id_ok <- table2_claim_ledger_identity(table2, ledger)
expect_true(id_ok$ok, "table2↔ledger identity on fixture")

ledger_bad <- ledger
ledger_bad$rr[[1]] <- ledger_bad$rr[[1]] + 0.001
id_bad <- table2_claim_ledger_identity(table2, ledger_bad)
expect_false(id_bad$ok, "table2↔ledger detects rr drift")

round_ok <- claim_text_rounding_ok(ledger)
expect_true(round_ok$ok, "claim_text rounding OK")
ledger_round_bad <- ledger
ledger_round_bad$claim_text[[1]] <- sub("0\\.", "0,", ledger_round_bad$claim_text[[1]])
round_bad <- claim_text_rounding_ok(ledger_round_bad)
expect_false(round_bad$ok, "claim_text rounding detects mismatch")

# Manuscript claim markers map one-to-one to ledger RR/CI/q values.
claim_fixture <- tempfile(fileext = ".md")
claim_lines <- unlist(lapply(seq_len(nrow(ledger)), function(i) {
  c(
    paste0("<!-- claim:", ledger$claim_id[[i]], " -->"),
    paste0(
      "Estimate ", sprintf("%.3f", ledger$rr[[i]]),
      " (", sprintf("%.3f", ledger$rr_low[[i]]), "–",
      sprintf("%.3f", ledger$rr_high[[i]]), "); q = ",
      sprintf("%.3f", ledger$q_value_core_bh[[i]]), ".",
      ""
    )
  )
}))
writeLines(claim_lines, claim_fixture, useBytes = TRUE)
ms_ok <- manuscript_claim_ledger_identity(claim_fixture, ledger)
expect_true(ms_ok$ok, "manuscript claim markers match ledger")
claim_bad <- readLines(claim_fixture, warn = FALSE)
claim_bad[claim_bad == claim_lines[[2]]] <- "Estimate 9.999; q = 0.999."
writeLines(claim_bad, claim_fixture, useBytes = TRUE)
ms_bad <- manuscript_claim_ledger_identity(claim_fixture, ledger)
expect_false(ms_bad$ok, "manuscript claim checker detects numeric drift")
unlink(claim_fixture)

# ---- Uncertainty ladder builder / validator ---------------------------------
core_rows <- list()
for (outcome in CORE_OUTCOMES) {
  for (pid in CORE_PATHWAY_IDS) {
    for (se in SE_LADDER_METHODS) {
      core_rows[[length(core_rows) + 1L]] <- data.frame(
        outcome = outcome,
        pathway_id = pid,
        exposure = pid,
        family = "negative_binomial",
        offset_policy = "days_only",
        se_method = se,
        rr = 1.01,
        rr_low = 0.99,
        rr_high = 1.03,
        p_value = 0.2,
        data_status = RELEASE_REAL_PROVENANCE,
        n_months = 132L,
        stringsAsFactors = FALSE
      )
    }
  }
}
core <- dplyr::bind_rows(core_rows)
ladder <- build_uncertainty_ladder(core)
ladder_chk <- validate_uncertainty_ladder(ladder)
expect_true(ladder_chk$ok, "ladder 12×4 validates")
expect_equal(nrow(ladder), 48L, "ladder row count")

ladder_synth <- ladder
ladder_synth$data_status[[1]] <- RELEASE_SYNTHETIC_CALIBRATION
expect_false(
  validate_uncertainty_ladder(ladder_synth)$ok,
  "ladder rejects SYNTHETIC_CALIBRATION provenance"
)

# Never rename HA → REAL
expect_true(
  all(ladder$data_status == RELEASE_REAL_PROVENANCE),
  "ladder keeps HA_APPROVED_AGGREGATE"
)
expect_false(
  any(ladder$data_status == "REAL"),
  "ladder never uses REAL token"
)

# ---- Synthetic path policy ---------------------------------------------------
pol_main <- synthetic_calibration_path_policy(
  "tables/table2_core_models.csv",
  data_status = RELEASE_SYNTHETIC_CALIBRATION,
  text_has_synthetic = TRUE
)
expect_false(pol_main$ok, "synthetic forbidden on main table path")

pol_fig <- synthetic_calibration_path_policy(
  "figures/figure3_core_forest.svg",
  text_has_synthetic = TRUE
)
expect_false(pol_fig$ok, "synthetic forbidden on main figure path")

pol_readme <- synthetic_calibration_path_policy(
  "README.md",
  text_has_synthetic = TRUE
)
expect_true(pol_readme$ok, "README may name synthetic quarantine")

pol_mf <- synthetic_calibration_path_policy(
  file.path(METHODS_FEASIBILITY_RELDIR, "md_calibration_summary.csv"),
  data_status = RELEASE_SYNTHETIC_CALIBRATION,
  result_class = "METHODS_FEASIBILITY",
  text_has_synthetic = TRUE
)
expect_true(pol_mf$ok, "synthetic allowed under methods_feasibility with status")

pol_mf_bare <- synthetic_calibration_path_policy(
  file.path(METHODS_FEASIBILITY_RELDIR, "mystery.csv"),
  data_status = NULL,
  text_has_synthetic = TRUE
)
expect_false(pol_mf_bare$ok, "methods_feasibility CSV requires data_status")

# Temp directory scan: do not touch canonical release
tmpdir <- file.path(tempdir(), paste0("release_check_fixture_", as.integer(Sys.time())))
dir.create(file.path(tmpdir, "tables"), recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(tmpdir, "figures"), recursive = TRUE, showWarnings = FALSE)
dir.create(
  file.path(tmpdir, METHODS_FEASIBILITY_RELDIR),
  recursive = TRUE,
  showWarnings = FALSE
)

utils::write.csv(
  data.frame(x = 1, data_status = RELEASE_REAL_PROVENANCE),
  file.path(tmpdir, "tables", "table2_core_models.csv"),
  row.names = FALSE
)
# Contaminated main surface
writeLines(
  "SYNTHETIC_CALIBRATION should not appear here",
  file.path(tmpdir, "tables", "claim_ledger.csv")
)
# Allowed methods-feasibility calibration table
utils::write.csv(
  data.frame(
    coverage = 0.9,
    data_status = RELEASE_SYNTHETIC_CALIBRATION,
    result_class = "METHODS_FEASIBILITY"
  ),
  file.path(tmpdir, METHODS_FEASIBILITY_RELDIR, "md_calibration_summary.csv"),
  row.names = FALSE
)

scan_bad <- scan_release_synthetic_policy(tmpdir)
expect_false(scan_bad$ok, "scan detects main-surface synthetic contamination")
expect_true(
  any(grepl("claim_ledger", scan_bad$violations)),
  "violation names claim_ledger"
)

# Clean main surface; keep methods_feasibility synthetic
unlink(file.path(tmpdir, "tables", "claim_ledger.csv"))
scan_ok <- scan_release_synthetic_policy(tmpdir)
expect_true(scan_ok$ok, "scan allows quarantined synthetic calibration")

# Raw monthly count detection
raw_df <- data.frame(
  month_id = "2013-01",
  n_events = 10L,
  stringsAsFactors = FALSE
)
expect_true(looks_like_raw_monthly_counts(raw_df), "detects raw monthly counts")
expect_false(
  looks_like_raw_monthly_counts(data.frame(outcome = "chd", total_events = 100)),
  "summary totals are not raw monthly series"
)

# Blocker availability disposition
br <- normalise_availability_row(
  "36_cvd_final_model_ensemble",
  "final_model_ensemble",
  status = "NOT_RUN_MISSING_GOVERNED_PANEL",
  message = "panel absent"
)
expect_equal(br$check_disposition, "non_fail_availability_fact", "blocker non-fail")
expect_equal(br$availability, "blocked", "blocker availability label")

# Cleanup fixture dir
unlink(tmpdir, recursive = TRUE)

# Canonical release unchanged by this test
if (!is.na(release_before) && dir.exists(release_dir)) {
  info_after <- file.info(list.files(release_dir, recursive = TRUE, full.names = TRUE))
  release_after <- sum(info_after$size, na.rm = TRUE)
  expect_equal(release_after, release_before, "canonical release untouched by tests")
}

message("test_final_release_checks.R: all assertions passed")
