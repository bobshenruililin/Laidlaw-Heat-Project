#!/usr/bin/env Rscript
# 08c_qc_stroke_aggregates.R
# QC for stroke aggregate files (real or synthetic). Writes a receipt note.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

find_stroke_file <- function() {
  mode <- Sys.getenv("PATHWAY_MODE", unset = "dev")
  # Prefer real approved files in ha_secure_placeholder
  ha_dir <- file.path(root, "data_raw", "ha_secure_placeholder")
  real <- list.files(ha_dir, pattern = "stroke.*\\.(csv|CSV)$|ha_.*stroke.*\\.(csv|CSV)$", full.names = TRUE)
  real <- real[!grepl("SYNTHETIC|PLACEHOLDER|mock", basename(real), ignore.case = TRUE)]
  if (length(real)) return(real[1])

  if (identical(mode, "real")) {
    stop(
      "PATHWAY_MODE=real but no non-synthetic stroke CSV in ", ha_dir, "\n",
      "Place an approved aggregate (e.g. ha_stroke_aggregates_2013_2023.csv) and retry."
    )
  }

  # Dev synthetic
  syn <- file.path(root, "data_processed", "samples", "SYNTHETIC_ha_stroke_aggregates.csv")
  if (file.exists(syn)) return(syn)
  syn2 <- list.files(file.path(root, "data_processed", "samples"), pattern = "SYNTHETIC_stroke.*\\.csv$", full.names = TRUE)
  if (length(syn2)) return(syn2[1])
  NULL
}

path <- find_stroke_file()
if (is.null(path)) {
  stop(
    "No stroke aggregate CSV found.\n",
    "Place real file in data_raw/ha_secure_placeholder/ (e.g. ha_stroke_aggregates_2013_2023.csv)\n",
    "or run scripts/07b_simulate_stroke_aggregates.R for dry-run."
  )
}

df <- utils::read.csv(path, stringsAsFactors = FALSE)
validate_required_columns(df, c("month_id", "n_events"), "stroke aggregate")
assert_month_id(df$month_id)

if (!"data_status" %in% names(df)) df$data_status <- "HA_APPROVED_AGGREGATE"
if (!"stroke_type" %in% names(df)) df$stroke_type <- "stroke_all"
if (!"age_group" %in% names(df)) df$age_group <- "all"
if (!"sex" %in% names(df)) df$sex <- "all"

# Detect grain
has_age <- !all(is.na(df$age_group) | df$age_group %in% c("all", ""))
has_sex <- !all(is.na(df$sex) | df$sex %in% c("all", ""))
grain <- if (has_age && has_sex) "age_sex" else if (has_age) "age" else "territory"

# Suppression
if ("suppression_flag" %in% names(df)) {
  n_supp <- sum(df$suppression_flag %in% TRUE | df$suppression_flag %in% c("TRUE", "1", 1), na.rm = TRUE)
} else {
  n_supp <- 0L
}

months <- sort(unique(df$month_id))
expected <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)$month_id
missing_months <- setdiff(expected, months)
extra_months <- setdiff(months, expected)

qc <- list(
  file = path,
  n_rows = nrow(df),
  grain = grain,
  data_status = paste(unique(df$data_status), collapse = ";"),
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
  n_suppressed_rows = n_supp,
  any_negative = any(df$n_events < 0, na.rm = TRUE),
  checked_at = as.character(Sys.time())
)

if (isTRUE(qc$any_negative)) stop("Negative n_events found — halt.")
if (qc$missing_months_n > 12) {
  warning("Many missing months (", qc$missing_months_n, "). Review before modelling.")
}

# Persist normalized copy for merge
norm_path <- file.path(root, "data_processed", "stroke_aggregates_normalized.csv")
write_csv_safe(df, norm_path)

out_dir <- file.path(root, "outputs", "reports")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
receipt <- file.path(out_dir, "stroke_data_qc_receipt.md")
lines <- c(
  "# Stroke aggregate QC receipt",
  "",
  paste0("- **File:** `", qc$file, "`"),
  paste0("- **Rows:** ", qc$n_rows),
  paste0("- **Grain:** ", qc$grain),
  paste0("- **data_status:** ", qc$data_status),
  paste0("- **stroke_type values:** ", qc$stroke_types),
  paste0("- **Months:** ", qc$n_months, " (", qc$month_min, " → ", qc$month_max, ")"),
  paste0("- **Missing study months:** ", qc$missing_months_n, if (qc$missing_months_n) paste0(" (", qc$missing_months, ")") else ""),
  paste0("- **Total events:** ", qc$n_events_total),
  paste0("- **Mean events / month:** ", qc$n_events_mean_month),
  paste0("- **Suppressed rows:** ", qc$n_suppressed_rows),
  paste0("- **Normalized path:** `", norm_path, "`"),
  paste0("- **Checked at:** ", qc$checked_at),
  "",
  if (grepl("SYNTHETIC", qc$data_status)) {
    "**WARNING:** This file is SYNTHETIC — coefficients are not findings."
  } else {
    "Real/approved aggregate detected. Proceed to merge + pathway panel under decision gates."
  }
)
writeLines(lines, receipt)

# Machine-readable sidecar
utils::write.csv(
  as.data.frame(qc, stringsAsFactors = FALSE),
  file.path(root, "outputs", "tables", "stroke_qc_summary.csv"),
  row.names = FALSE
)

message("QC complete. Grain=", grain, " receipt=", receipt)
