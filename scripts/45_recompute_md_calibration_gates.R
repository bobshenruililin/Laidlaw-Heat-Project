#!/usr/bin/env Rscript
# 45_recompute_md_calibration_gates.R
# Protocol amendment F1.2: reprocess completed F1.1 raw metrics under strict
# worst-cell gates. Never re-fits models. Never modifies
# outputs/calibration_md/md_calibration_raw_metrics.csv.
#
# Writes:
#   md_calibration_summary.csv                      (canonical F1.2)
#   md_calibration_gate_summary.csv                 (canonical F1.2)
#   md_calibration_summary_core_500_f1_2.csv
#   md_calibration_gate_summary_core_500_f1_2.csv
#   md_calibration_f1_2_decision_report.md
# and appends a run-status row. Every row: SYNTHETIC_CALIBRATION.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
source(file.path("scripts", "md_calibration_helpers.R"))
if (file.exists(file.path("scripts", "final_model_helpers.R"))) {
  source(file.path("scripts", "final_model_helpers.R"))
}
root <- project_root()
setwd(root)
ensure_packages("yaml")

out_dir <- file.path(root, "outputs", "calibration_md")
raw_path <- file.path(out_dir, "md_calibration_raw_metrics.csv")
if (!file.exists(raw_path)) {
  stop("Missing completed raw metrics: ", raw_path)
}

# Refuse to overwrite/truncate the canonical raw file.
raw_info_before <- file.info(raw_path)
raw <- utils::read.csv(raw_path, stringsAsFactors = FALSE)
if (!nrow(raw)) stop("Raw metrics table is empty")
if (!"data_status" %in% names(raw) ||
    any(raw$data_status != MD_PROVENANCE_SYNTHETIC)) {
  stop("Raw metrics must be labelled SYNTHETIC_CALIBRATION exclusively")
}

registry <- if (exists("load_final_model_registry", mode = "function")) {
  load_final_model_registry(root = root)
} else {
  yaml::read_yaml(file.path(root, "analysis_plan", "final_model_registry.yml"))
}
hess_max <- registry$md_feasibility$admission_gates$hessian_condition_max %||%
  MD_HESSIAN_CONDITION_MAX
hess_max <- as.numeric(hess_max)

message(
  "Recomputing F1.2 summaries from ", nrow(raw),
  " raw rows (no re-fit). hessian_condition_max=", hess_max
)

summary_all <- md_summarise_raw_metrics(raw, hessian_condition_max = hess_max)
summary_all$protocol_amendment <- "F1.2"
summary_all$raw_source <- "md_calibration_raw_metrics.csv"
summary_all$data_status <- MD_PROVENANCE_SYNTHETIC

gates <- md_evaluate_gates(summary_all, registry = registry, root = root)
gates$protocol_amendment <- "F1.2"
gates$raw_source <- "md_calibration_raw_metrics.csv"
gates$data_status <- MD_PROVENANCE_SYNTHETIC

summary_path <- file.path(out_dir, "md_calibration_summary.csv")
gate_path <- file.path(out_dir, "md_calibration_gate_summary.csv")
summary_named <- file.path(out_dir, "md_calibration_summary_core_500_f1_2.csv")
gate_named <- file.path(out_dir, "md_calibration_gate_summary_core_500_f1_2.csv")
report_path <- file.path(out_dir, "md_calibration_f1_2_decision_report.md")
run_status_path <- file.path(out_dir, "md_calibration_run_status.csv")

write_csv_safe(summary_all, summary_path)
write_csv_safe(summary_all, summary_named)
write_csv_safe(gates, gate_path)
write_csv_safe(gates, gate_named)

report_lines <- md_format_f12_decision_report(
  summary_all,
  gates,
  raw_note = paste0(
    "F1.1 500-rep raw metrics at ",
    "outputs/calibration_md/md_calibration_raw_metrics.csv",
    " (untouched; n_rows=", nrow(raw), ")"
  )
)
dir.create(dirname(report_path), recursive = TRUE, showWarnings = FALSE)
writeLines(report_lines, report_path)
message("Wrote ", report_path)

# Append run status without rewriting history.
status_row <- data.frame(
  timestamp = as.character(Sys.time()),
  status = "f1_2_recompute_complete",
  message = paste0(
    "F1.2 recompute from untouched raw; admission_decision=",
    paste(unique(gates$admission_decision), collapse = ","),
    "; all_passed=", all(gates$passed)
  ),
  run_mode = "core",
  n_reps = NA_integer_,
  n_workers = NA_integer_,
  master_seed = MD_MASTER_SEED,
  design_version = "F1.2",
  admission_decision = paste(unique(gates$admission_decision), collapse = ","),
  all_gates_passed = all(gates$passed),
  data_status = MD_PROVENANCE_SYNTHETIC,
  stringsAsFactors = FALSE
)
if (file.exists(run_status_path)) {
  old <- utils::read.csv(run_status_path, stringsAsFactors = FALSE)
  alln <- union(names(old), names(status_row))
  for (nm in setdiff(alln, names(old))) old[[nm]] <- NA
  for (nm in setdiff(alln, names(status_row))) status_row[[nm]] <- NA
  status_row <- rbind(old[, alln, drop = FALSE], status_row[, alln, drop = FALSE])
}
write_csv_safe(status_row, run_status_path)

raw_info_after <- file.info(raw_path)
if (!identical(as.character(raw_info_before$mtime), as.character(raw_info_after$mtime)) ||
    !identical(as.numeric(raw_info_before$size), as.numeric(raw_info_after$size))) {
  stop("Raw metrics file changed unexpectedly during F1.2 recompute")
}

message(
  "F1.2 complete. Decision: ",
  paste(unique(gates$admission_decision), collapse = ","),
  " (raw untouched)"
)
