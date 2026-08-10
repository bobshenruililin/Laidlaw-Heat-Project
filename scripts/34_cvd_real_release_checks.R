#!/usr/bin/env Rscript
# 34_cvd_real_release_checks.R
# Fatal provenance and namespace checks for the CHD/HF manuscript release.
# Strengthened for the script-38 final augmentation:
#   - table2 ↔ claim ledger numerical identity + claim-text rounding
#   - BH q recomputation
#   - Table 4 uncertainty ladder 12×4 with exact HA provenance
#   - weather source validation all pass
#   - SYNTHETIC_CALIBRATION only under supplement/methods_feasibility/
#   - no governed inputs tracked; no raw monthly-count descriptives
#   - blocker statuses as non-fail availability facts
#   - hash manifest rebuilt after all checks

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "release_check_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "digest"))

outcomes <- c("chd", "hf")
tables_dir <- file.path(root, "outputs", "tables")
reports_dir <- file.path(root, "outputs", "reports")
release_dir <- file.path(root, "outputs", "release_chd_hf")
dir.create(release_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(reports_dir, recursive = TRUE, showWarnings = FALSE)

errors <- character()
checks <- list()
add_check <- function(check, status, detail) {
  checks[[length(checks) + 1L]] <<- data.frame(
    check = check,
    status = status,
    detail = detail,
    stringsAsFactors = FALSE
  )
  if (!identical(status, "PASS")) {
    errors <<- c(errors, paste(check, detail, sep = ": "))
  }
}
add_pass_fail <- function(check, ok, detail) {
  add_check(check, if (isTRUE(ok)) "PASS" else "FAIL", detail)
}

# ---------------------------------------------------------------------------
# Legacy real-panel estimate / diagnostic provenance (when present)
# ---------------------------------------------------------------------------
for (outcome in outcomes) {
  est_path <- file.path(tables_dir, paste0(outcome, "_pathway_panel_estimates.csv"))
  diag_path <- file.path(tables_dir, paste0(outcome, "_pathway_core_diagnostics.csv"))

  if (!file.exists(est_path)) {
    add_check(paste0(outcome, "_estimates_exist"), "FAIL", est_path)
  } else {
    est <- utils::read.csv(est_path, stringsAsFactors = FALSE)
    bad_status <- !grepl("^HA_APPROVED_AGGREGATE$", est$data_status)
    add_check(
      paste0(outcome, "_estimate_provenance"),
      if (any(bad_status)) "FAIL" else "PASS",
      paste(unique(est$data_status), collapse = ";")
    )
    add_check(
      paste0(outcome, "_estimate_month_bound"),
      if (any(est$n_months > 132 | est$n_months < 1, na.rm = TRUE)) "FAIL" else "PASS",
      paste0("range=", min(est$n_months, na.rm = TRUE), "-", max(est$n_months, na.rm = TRUE))
    )
  }

  if (!file.exists(diag_path)) {
    add_check(paste0(outcome, "_diagnostics_exist"), "FAIL", diag_path)
  } else {
    diag <- utils::read.csv(diag_path, stringsAsFactors = FALSE)
    contaminated <- any(diag$synthetic %in% TRUE) ||
      any(diag$n > 132) ||
      any(!grepl("^HA_APPROVED_AGGREGATE$", diag$data_status))
    add_check(
      paste0(outcome, "_diagnostics_real_only"),
      if (contaminated) "FAIL" else "PASS",
      paste0(
        "n_range=", min(diag$n), "-", max(diag$n),
        "; synthetic=", paste(unique(diag$synthetic), collapse = ","),
        "; status=", paste(unique(diag$data_status), collapse = ",")
      )
    )
  }
}

ambiguous <- c(
  file.path(tables_dir, "pathway_panel_estimates.csv"),
  file.path(tables_dir, "pathway_panel_fit_stats.csv"),
  file.path(tables_dir, "pathway_panel_status.csv"),
  file.path(tables_dir, "pathway_headline_diagnostics.csv"),
  file.path(reports_dir, "pathway_panel_summary.md"),
  file.path(reports_dir, "pathway_diagnostics_note.md"),
  file.path(root, "outputs", "figures", "pathway", "pathway_panel_forest.png")
)
present_ambiguous <- ambiguous[file.exists(ambiguous)]
add_check(
  "no_ambiguous_generic_outputs",
  if (length(present_ambiguous)) "FAIL" else "PASS",
  if (length(present_ambiguous)) paste(present_ambiguous, collapse = ";") else "none"
)

# ---------------------------------------------------------------------------
# Governed inputs: gitignored AND not tracked
# ---------------------------------------------------------------------------
governed_paths <- governed_paths_default(root)
ignored_each <- vapply(governed_paths, function(path) {
  identical(
    tryCatch(
      as.integer(system2("git", c("check-ignore", "-q", path))),
      error = function(e) 1L
    ),
    0L
  )
}, logical(1))
add_check(
  "governed_inputs_gitignored",
  if (all(ignored_each)) "PASS" else "FAIL",
  if (all(ignored_each)) {
    "source aggregates and merged panels"
  } else {
    paste(governed_paths[!ignored_each], collapse = ";")
  }
)

tracked_chk <- check_governed_not_tracked(governed_paths)
add_pass_fail("governed_inputs_not_tracked", tracked_chk$ok, tracked_chk$detail)

# ---------------------------------------------------------------------------
# Release populated
# ---------------------------------------------------------------------------
if (!dir.exists(release_dir) || !length(list.files(release_dir))) {
  add_check("release_directory_populated", "FAIL", release_dir)
} else {
  add_check("release_directory_populated", "PASS", release_dir)
}

release_tables <- file.path(release_dir, "tables")
table2_path <- file.path(release_tables, "table2_core_models.csv")
ledger_path <- file.path(release_tables, "claim_ledger.csv")
ledger_v2_path <- file.path(release_tables, "claim_ledger_v2.csv")
table4_path <- file.path(release_tables, "table4_uncertainty_ladder.csv")
avail_path <- file.path(release_tables, "analysis_availability.csv")

# ---------------------------------------------------------------------------
# table2 ↔ claim ledger identity + rounding + BH
# ---------------------------------------------------------------------------
if (!file.exists(table2_path) || !file.exists(ledger_path)) {
  add_check(
    "table2_claim_ledger_identity",
    "FAIL",
    "missing table2 and/or claim_ledger"
  )
} else {
  table2 <- utils::read.csv(table2_path, stringsAsFactors = FALSE)
  ledger <- utils::read.csv(ledger_path, stringsAsFactors = FALSE)

  id_chk <- table2_claim_ledger_identity(table2, ledger)
  add_pass_fail("table2_claim_ledger_identity", id_chk$ok, id_chk$detail)

  round_chk <- claim_text_rounding_ok(ledger)
  add_pass_fail("claim_text_rounding", round_chk$ok, round_chk$detail)

  bh_chk <- bh_q_identity(ledger$p_value, ledger$q_value_core_bh)
  add_pass_fail("bh_q_recompute", bh_chk$ok, bh_chk$detail)

  manuscript_path <- file.path(
    root,
    "manuscript",
    "chd_hf_thermal_associations_2013_2023.md"
  )
  manuscript_chk <- manuscript_claim_ledger_identity(
    manuscript_path,
    ledger
  )
  add_pass_fail(
    "manuscript_claim_ledger_identity",
    manuscript_chk$ok,
    manuscript_chk$detail
  )

  # Never rename HA → REAL on claim surfaces
  if ("provenance" %in% names(ledger)) {
    add_pass_fail(
      "claim_ledger_ha_not_real",
      all(ledger$provenance == RELEASE_REAL_PROVENANCE) &&
        !any(grepl("^REAL$", ledger$provenance)),
      paste(unique(ledger$provenance), collapse = ";")
    )
  }
}

if (file.exists(ledger_v2_path)) {
  v2 <- utils::read.csv(ledger_v2_path, stringsAsFactors = FALSE)
  need_v2 <- c(
    "claim_id", "claim_tier", "post_outcome_context",
    "multiplicity_context", "se_context", "rr", "provenance"
  )
  missing_v2 <- setdiff(need_v2, names(v2))
  add_pass_fail(
    "claim_ledger_v2_columns",
    !length(missing_v2),
    if (length(missing_v2)) {
      paste(missing_v2, collapse = ",")
    } else {
      "tier/post-outcome/multiplicity/SE present"
    }
  )
  if (file.exists(ledger_path)) {
    v1 <- utils::read.csv(ledger_path, stringsAsFactors = FALSE)
    # v2 must not invent extra real numeric claims beyond v1 without real outputs
    add_pass_fail(
      "claim_ledger_v2_no_extra_real_claims",
      identical(nrow(v2), nrow(v1)) &&
        setequal(as.character(v2$claim_id), as.character(v1$claim_id)),
      paste0("v1=", nrow(v1), " v2=", nrow(v2))
    )
  }
  if ("data_status" %in% names(v2)) {
    add_pass_fail(
      "claim_ledger_v2_no_synthetic",
      !any(grepl("SYNTHETIC", v2$data_status, ignore.case = TRUE)),
      paste(unique(v2$data_status), collapse = ";")
    )
  }
}

# ---------------------------------------------------------------------------
# Uncertainty ladder (Table 4)
# ---------------------------------------------------------------------------
if (!file.exists(table4_path)) {
  add_check(
    "uncertainty_ladder_12x4",
    "FAIL",
    "missing tables/table4_uncertainty_ladder.csv (run script 38)"
  )
} else {
  ladder <- utils::read.csv(table4_path, stringsAsFactors = FALSE)
  ladder_chk <- validate_uncertainty_ladder(ladder)
  add_pass_fail("uncertainty_ladder_12x4", ladder_chk$ok, ladder_chk$detail)
  add_pass_fail(
    "uncertainty_ladder_ha_provenance",
    all(ladder$data_status == RELEASE_REAL_PROVENANCE),
    paste(unique(ladder$data_status), collapse = ";")
  )
}

# ---------------------------------------------------------------------------
# Weather source validation: all pass
# ---------------------------------------------------------------------------
weather_val_candidates <- c(
  file.path(
    release_dir, METHODS_FEASIBILITY_RELDIR,
    "weather_definition_source_validation.csv"
  ),
  file.path(tables_dir, "weather_definition_source_validation.csv")
)
weather_val_path <- weather_val_candidates[file.exists(weather_val_candidates)][1]
if (is.na(weather_val_path) || !nzchar(weather_val_path %||% "")) {
  add_check("weather_source_validation_all_pass", "FAIL", "validation file absent")
} else {
  wv <- utils::read.csv(weather_val_path, stringsAsFactors = FALSE)
  if (!"pass" %in% names(wv)) {
    add_check("weather_source_validation_all_pass", "FAIL", "missing pass column")
  } else {
    ok <- all(as.logical(wv$pass) %in% TRUE)
    add_pass_fail(
      "weather_source_validation_all_pass",
      ok,
      paste0("n=", nrow(wv), "; all_pass=", ok, "; file=", weather_val_path)
    )
  }
}

# ---------------------------------------------------------------------------
# SYNTHETIC_CALIBRATION path policy
# ---------------------------------------------------------------------------
if (dir.exists(release_dir) && length(list.files(release_dir))) {
  synth_chk <- scan_release_synthetic_policy(release_dir)
  add_pass_fail(
    "synthetic_calibration_path_policy",
    synth_chk$ok,
    synth_chk$detail
  )

  # Explicit main-surface contamination check (tables/figures claim surfaces)
  main_hits <- character(0)
  main_files <- list.files(
    c(file.path(release_dir, "tables"), file.path(release_dir, "figures")),
    recursive = TRUE, full.names = TRUE
  )
  main_files <- main_files[file.info(main_files)$isdir %in% FALSE]
  text_main <- main_files[grepl("\\.(csv|md|txt|svg)$", main_files, ignore.case = TRUE)]
  for (path in text_main) {
    txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
    if (grepl("SYNTHETIC", txt, fixed = TRUE)) {
      main_hits <- c(
        main_hits,
        normalise_release_relpath(path, release_dir)
      )
    }
  }
  add_pass_fail(
    "no_synthetic_on_main_claim_surfaces",
    !length(main_hits),
    if (length(main_hits)) paste(main_hits, collapse = ";") else "none"
  )
}

# ---------------------------------------------------------------------------
# No raw monthly-count descriptives in release
# ---------------------------------------------------------------------------
if (dir.exists(release_dir) && length(list.files(release_dir))) {
  raw_chk <- scan_release_raw_monthly_counts(release_dir)
  add_pass_fail(
    "no_raw_monthly_count_descriptives",
    raw_chk$ok,
    raw_chk$detail
  )
}

# ---------------------------------------------------------------------------
# Analysis availability: blockers are non-fail facts
# ---------------------------------------------------------------------------
if (file.exists(avail_path)) {
  avail <- utils::read.csv(avail_path, stringsAsFactors = FALSE)
  need_av <- c("script_id", "analysis", "status", "availability", "check_disposition")
  missing_av <- setdiff(need_av, names(avail))
  add_pass_fail(
    "analysis_availability_schema",
    !length(missing_av),
    if (length(missing_av)) paste(missing_av, collapse = ",") else "schema OK"
  )
  blocker_rows <- avail[
    grepl("NOT_RUN|BLOCKED|ABSENT|MISSING", avail$status, ignore.case = TRUE),
    ,
    drop = FALSE
  ]
  if (nrow(blocker_rows)) {
    dispositions_ok <- all(
      blocker_rows$check_disposition == "non_fail_availability_fact"
    )
    add_pass_fail(
      "blocker_statuses_non_fail_facts",
      dispositions_ok,
      paste0(
        "blocker_rows=", nrow(blocker_rows),
        "; disposition_ok=", dispositions_ok
      )
    )
  } else {
    add_check(
      "blocker_statuses_non_fail_facts",
      "PASS",
      "no blocker rows (analyses available or absent table empty)"
    )
  }
  # Blockers must not be mislabelled as completed real estimates
  fake_complete <- avail$availability == "available" &
    grepl("NOT_RUN|BLOCKED|ABSENT|MISSING", avail$status, ignore.case = TRUE)
  add_pass_fail(
    "blockers_not_fake_completed_analyses",
    !any(fake_complete, na.rm = TRUE),
    if (any(fake_complete, na.rm = TRUE)) {
      paste(avail$analysis[fake_complete], collapse = ";")
    } else {
      "no fake completions"
    }
  )
} else {
  add_check(
    "analysis_availability_present",
    "FAIL",
    "missing tables/analysis_availability.csv (run script 38)"
  )
}

# ---------------------------------------------------------------------------
# Preserved Tables 1–3 / Figures 1–4 still present
# ---------------------------------------------------------------------------
preserved <- c(
  "tables/table1_outcome_summary.csv",
  "tables/table2_core_models.csv",
  "tables/table3_robustness_summary.csv",
  "figures/figure1_indexed_outcome_series.svg",
  "figures/figure2_seasonal_pattern.svg",
  "figures/figure3_core_forest.svg",
  "figures/figure4_trend_depletion_sensitivity.svg"
)
missing_pres <- preserved[
  !file.exists(file.path(release_dir, preserved))
]
add_pass_fail(
  "preserved_tables1to3_figures1to4",
  !length(missing_pres),
  if (length(missing_pres)) paste(missing_pres, collapse = ";") else "present"
)

# ---------------------------------------------------------------------------
# Write checks, then rebuild hash manifest AFTER all checks
# ---------------------------------------------------------------------------
checks_df <- dplyr::bind_rows(checks)
write_csv_safe(checks_df, file.path(release_dir, "validation_checks.csv"))

manifest_files <- list.files(release_dir, recursive = TRUE, full.names = TRUE)
manifest_files <- manifest_files[
  file.info(manifest_files)$isdir %in% FALSE &
    basename(manifest_files) != "release_manifest.csv"
]
manifest <- data.frame(
  path = sub(
    paste0("^", normalizePath(release_dir), "/?"),
    "",
    normalizePath(manifest_files)
  ),
  bytes = file.info(manifest_files)$size,
  sha256 = vapply(
    manifest_files,
    digest::digest,
    character(1),
    algo = "sha256",
    file = TRUE
  ),
  stringsAsFactors = FALSE
)
write_csv_safe(manifest, file.path(release_dir, "release_manifest.csv"))

report <- file.path(reports_dir, "cvd_real_release_validation.md")
writeLines(
  c(
    "# CHD/HF real-release validation",
    "",
    paste0("- Checked: ", Sys.time()),
    paste0("- Release directory: `", release_dir, "`"),
    paste0("- Passed: ", sum(checks_df$status == "PASS"), " / ", nrow(checks_df)),
    "",
    "| Check | Status | Detail |",
    "|---|---|---|",
    paste0("| ", checks_df$check, " | ", checks_df$status, " | ", checks_df$detail, " |"),
    "",
    if (length(errors)) "**RELEASE BLOCKED.**" else "**RELEASE VALIDATED.**"
  ),
  report
)

if (length(errors)) {
  stop("CHD/HF real-release checks failed:\n- ", paste(errors, collapse = "\n- "))
}
message("CHD/HF real-release checks passed: ", nrow(checks_df), " checks")
