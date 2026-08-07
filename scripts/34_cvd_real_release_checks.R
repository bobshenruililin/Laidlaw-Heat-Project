#!/usr/bin/env Rscript
# 34_cvd_real_release_checks.R
# Fatal provenance and namespace checks for the CHD/HF manuscript release.

source(file.path("scripts", "utils.R"))
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
  if (!identical(status, "PASS")) errors <<- c(errors, paste(check, detail, sep = ": "))
}

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

governed_paths <- c(
  file.path(root, "data_raw", "ha_secure_placeholder", "ha_chd_monthly_2013_2023.csv"),
  file.path(root, "data_raw", "ha_secure_placeholder", "ha_hf_monthly_2013_2023.csv"),
  file.path(root, "data_processed", "chd_aggregates_normalized.csv"),
  file.path(root, "data_processed", "hf_aggregates_normalized.csv"),
  file.path(root, "data_processed", "chd_analysis_panel.csv"),
  file.path(root, "data_processed", "hf_analysis_panel.csv")
)
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
  if (all(ignored_each)) "source aggregates and merged panels" else paste(governed_paths[!ignored_each], collapse = ";")
)

release_files <- list.files(release_dir, recursive = TRUE, full.names = TRUE)
release_files <- release_files[file.info(release_files)$isdir %in% FALSE]
if (length(release_files)) {
  text_like <- release_files[grepl("\\.(csv|md|txt|tex|html)$", release_files, ignore.case = TRUE)]
  synthetic_hits <- vapply(text_like, function(path) {
    txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
    grepl("SYNTHETIC", txt, fixed = TRUE)
  }, logical(1))
  add_check(
    "release_has_no_synthetic_labels",
    if (any(synthetic_hits)) "FAIL" else "PASS",
    if (any(synthetic_hits)) paste(text_like[synthetic_hits], collapse = ";") else "none"
  )
} else {
  add_check("release_directory_populated", "FAIL", release_dir)
}

checks_df <- dplyr::bind_rows(checks)
write_csv_safe(checks_df, file.path(release_dir, "validation_checks.csv"))

manifest_files <- list.files(release_dir, recursive = TRUE, full.names = TRUE)
manifest_files <- manifest_files[
  file.info(manifest_files)$isdir %in% FALSE &
    basename(manifest_files) != "release_manifest.csv"
]
manifest <- data.frame(
  path = sub(paste0("^", normalizePath(release_dir), "/?"), "", normalizePath(manifest_files)),
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
