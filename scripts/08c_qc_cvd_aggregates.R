#!/usr/bin/env Rscript
# 08c_qc_cvd_aggregates.R
# Outcome-aware QC for HA monthly CVD first-hospitalisation aggregates.
# OUTCOME env: chd | hf | stroke (default chd)

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

outcome <- tolower(Sys.getenv("OUTCOME", unset = "chd"))
mode <- tolower(Sys.getenv("PATHWAY_MODE", unset = "dev"))
if (!outcome %in% c("chd", "hf", "stroke")) {
  stop("OUTCOME must be one of chd, hf, stroke; got: ", outcome)
}

find_outcome_file <- function(outcome) {
  mode <- Sys.getenv("PATHWAY_MODE", unset = "dev")
  ha_dir <- file.path(root, "data_raw", "ha_secure_placeholder")
  override <- Sys.getenv("HA_AGGREGATE_FILE", unset = "")
  if (nzchar(override)) {
    if (!file.exists(override)) stop("HA_AGGREGATE_FILE not found: ", override)
    return(override)
  }

  patterns <- list(
    chd = "ha_chd.*\\.(csv|CSV)$|chd.*monthly.*\\.(csv|CSV)$",
    hf = "ha_hf.*\\.(csv|CSV)$|hf.*monthly.*\\.(csv|CSV)$|heart_failure.*\\.(csv|CSV)$",
    stroke = "stroke.*\\.(csv|CSV)$|ha_.*stroke.*\\.(csv|CSV)$"
  )
  real <- list.files(ha_dir, pattern = patterns[[outcome]], full.names = TRUE)
  real <- real[!grepl("SYNTHETIC|PLACEHOLDER|mock|RECEIPT|long|wide", basename(real), ignore.case = TRUE)]
  # Prefer explicit monthly files
  preferred <- real[grepl(paste0("ha_", outcome, "_monthly"), basename(real), ignore.case = TRUE)]
  if (length(preferred)) return(preferred[1])
  if (length(real)) return(real[1])

  if (identical(mode, "real")) {
    stop(
      "PATHWAY_MODE=real but no approved ", outcome, " CSV in ", ha_dir, "\n",
      "Place ha_", outcome, "_monthly_2013_2023.csv and retry."
    )
  }

  if (identical(outcome, "stroke")) {
    syn <- file.path(root, "data_processed", "samples", "SYNTHETIC_ha_stroke_aggregates.csv")
    if (file.exists(syn)) return(syn)
  }
  NULL
}

path <- find_outcome_file(outcome)
if (is.null(path)) stop("No aggregate CSV found for OUTCOME=", outcome)

df <- utils::read.csv(path, stringsAsFactors = FALSE)
validate_required_columns(df, c("month_id", "n_events"), paste(outcome, "aggregate"))
assert_month_id(df$month_id)

if (!"data_status" %in% names(df)) {
  if (identical(mode, "real")) {
    stop("Real aggregate file must carry an explicit data_status field")
  }
  df$data_status <- "SYNTHETIC"
}
if (identical(mode, "real")) {
  statuses <- unique(as.character(df$data_status))
  if (!identical(statuses, "HA_APPROVED_AGGREGATE")) {
    stop(
      "Real aggregate file requires data_status=HA_APPROVED_AGGREGATE only; found: ",
      paste(statuses, collapse = ", ")
    )
  }
}
if (!"outcome" %in% names(df)) df$outcome <- outcome
# Retain stroke_type column name for pathway compatibility; map outcome
if (!"stroke_type" %in% names(df)) {
  df$stroke_type <- paste0(outcome, "_all")
}
if (!"age_group" %in% names(df)) df$age_group <- "all"
if (!"sex" %in% names(df)) df$sex <- "all"
if (!"cohort" %in% names(df)) df$cohort <- NA_character_
if (!"event_definition" %in% names(df)) df$event_definition <- NA_character_
if (identical(mode, "real")) {
  validate_required_columns(
    df,
    c("outcome", "cohort", "event_definition"),
    paste(outcome, "real aggregate")
  )
  if (!all(df$outcome == outcome)) {
    stop("Outcome column does not match OUTCOME=", outcome)
  }
  if (any(is.na(df$cohort) | !nzchar(df$cohort)) ||
      any(is.na(df$event_definition) | !nzchar(df$event_definition))) {
    stop("Real aggregate requires non-missing cohort and event_definition")
  }
}

has_age <- !all(is.na(df$age_group) | df$age_group %in% c("all", ""))
has_sex <- !all(is.na(df$sex) | df$sex %in% c("all", ""))
grain <- if (has_age && has_sex) "age_sex" else if (has_age) "age" else "territory"

if ("suppression_flag" %in% names(df)) {
  n_supp <- sum(df$suppression_flag %in% TRUE | df$suppression_flag %in% c("TRUE", "1", 1), na.rm = TRUE)
} else {
  n_supp <- 0L
}

months <- sort(unique(df$month_id))
expected <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)$month_id
missing_months <- setdiff(expected, months)
extra_months <- setdiff(months, expected)

# Secular trend diagnostics (critical for first-event cohorts)
by_year <- tapply(df$n_events, substr(df$month_id, 1, 4), sum, na.rm = TRUE)

qc <- list(
  outcome = outcome,
  file = path,
  n_rows = nrow(df),
  grain = grain,
  data_status = paste(unique(df$data_status), collapse = ";"),
  cohort = paste(unique(as.character(df$cohort)), collapse = ";"),
  event_definition = paste(unique(as.character(df$event_definition)), collapse = ";"),
  stroke_types = paste(sort(unique(as.character(df$stroke_type))), collapse = ";"),
  n_months = length(months),
  month_min = months[1],
  month_max = months[length(months)],
  missing_months_n = length(missing_months),
  missing_months = paste(missing_months, collapse = ","),
  extra_months_n = length(extra_months),
  n_events_total = sum(df$n_events, na.rm = TRUE),
  n_events_mean_month = {
    bym <- tapply(df$n_events, df$month_id, sum, na.rm = TRUE)
    round(mean(bym), 2)
  },
  n_events_2013 = unname(by_year["2013"] %||% NA),
  n_events_2023 = unname(by_year["2023"] %||% NA),
  n_suppressed_rows = n_supp,
  any_negative = any(df$n_events < 0, na.rm = TRUE),
  checked_at = as.character(Sys.time())
)

if (isTRUE(qc$any_negative)) stop("Negative n_events found — halt.")
if (qc$missing_months_n > 12) {
  warning("Many missing months (", qc$missing_months_n, "). Review before modelling.")
}

norm_path <- file.path(root, "data_processed", paste0(outcome, "_aggregates_normalized.csv"))
# Also write stroke alias when outcome is stroke for legacy scripts
write_csv_safe(df, norm_path)
if (identical(outcome, "stroke")) {
  write_csv_safe(df, file.path(root, "data_processed", "stroke_aggregates_normalized.csv"))
}

out_dir <- file.path(root, "outputs", "reports")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
tab_dir <- file.path(root, "outputs", "tables")
dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)

receipt <- file.path(out_dir, paste0(outcome, "_data_qc_receipt.md"))
lines <- c(
  paste0("# ", toupper(outcome), " aggregate QC receipt"),
  "",
  paste0("- **Outcome:** `", qc$outcome, "`"),
  paste0("- **File:** `", qc$file, "`"),
  paste0("- **Rows:** ", qc$n_rows),
  paste0("- **Grain:** ", qc$grain),
  paste0("- **data_status:** ", qc$data_status),
  paste0("- **Cohort:** ", qc$cohort),
  paste0("- **Event definition:** ", qc$event_definition),
  paste0("- **Type labels:** ", qc$stroke_types),
  paste0("- **Months:** ", qc$n_months, " (", qc$month_min, " → ", qc$month_max, ")"),
  paste0("- **Missing study months:** ", qc$missing_months_n, if (qc$missing_months_n) paste0(" (", qc$missing_months, ")") else ""),
  paste0("- **Total events:** ", qc$n_events_total),
  paste0("- **Mean events / month:** ", qc$n_events_mean_month),
  paste0("- **Annual totals 2013 → 2023:** ", qc$n_events_2013, " → ", qc$n_events_2023),
  paste0("- **Suppressed rows:** ", qc$n_suppressed_rows),
  paste0("- **Normalized path:** `", norm_path, "`"),
  paste0("- **Checked at:** ", qc$checked_at),
  "",
  "## Denominator caveat",
  "",
  "Events are restricted to patients with T2D and/or HTN (2013–2023) using first hospitalisation after first CVD diagnosis.",
  "C&SD general-population offsets are ecological person-time, **not** cohort at-risk person-time.",
  "",
  if (grepl("SYNTHETIC", qc$data_status)) {
    "**WARNING:** This file is SYNTHETIC — coefficients are not findings."
  } else {
    "**Provenance:** HA_APPROVED_AGGREGATE (monthly). Do not commit microdata."
  },
  "",
  "## Annual event totals",
  "",
  paste0("| Year | Events |"),
  paste0("|---|---|"),
  paste0("| ", names(by_year), " | ", as.integer(by_year), " |")
)
writeLines(lines, receipt)

qc_df <- as.data.frame(qc, stringsAsFactors = FALSE)
write_csv_safe(qc_df, file.path(tab_dir, paste0(outcome, "_qc_summary.csv")))

message("QC OK for ", outcome, ": ", qc$n_months, " months; total events=", qc$n_events_total)
message("Receipt: ", receipt)
