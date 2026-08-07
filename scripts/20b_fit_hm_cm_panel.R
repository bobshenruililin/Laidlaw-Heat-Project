#!/usr/bin/env Rscript
# 20b_fit_hm_cm_panel.R
# Fit provisional HM/CM binary month flags as exposures for a given OUTCOME.
# Labels estimates as provisional / not Hogan-locked.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines", "sandwich", "lmtest"))

outcome <- tolower(Sys.getenv("OUTCOME", unset = "chd"))
panel_path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
hm_path <- file.path(root, "data_processed", "hm_cm_month_flags_2013_2023.csv")
if (!file.exists(panel_path)) stop("Missing panel: ", panel_path)
if (!file.exists(hm_path)) stop("Run 19b_build_hm_cm_exposures.R first")

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
hm <- utils::read.csv(hm_path, stringsAsFactors = FALSE)
panel <- panel |> dplyr::left_join(hm, by = "month_id")
panel$month_f <- factor(panel$month)

defs <- setdiff(names(hm), c("month_id", "HM23_event_starts"))
trend_df <- cfg$modeling$time_trend_df %||% 4

extract_rr <- function(model, vcov_mat, term) {
  ct <- tryCatch(
    if (is.null(vcov_mat)) summary(model)$coefficients else as.matrix(lmtest::coeftest(model, vcov. = vcov_mat)),
    error = function(e) summary(model)$coefficients
  )
  if (!term %in% rownames(ct)) return(NULL)
  data.frame(
    term = term,
    estimate = ct[term, 1],
    std_error = ct[term, 2],
    statistic = ct[term, 3],
    p_value = ct[term, 4],
    rr = exp(ct[term, 1]),
    rr_low = exp(ct[term, 1] - 1.96 * ct[term, 2]),
    rr_high = exp(ct[term, 1] + 1.96 * ct[term, 2]),
    stringsAsFactors = FALSE
  )
}

est_list <- list()
stat_list <- list()
for (d in defs) {
  if (!d %in% names(panel) || all(is.na(panel[[d]]))) {
    stat_list[[d]] <- data.frame(definition_id = d, status = "skipped_missing", stringsAsFactors = FALSE)
    next
  }
  if (length(unique(stats::na.omit(panel[[d]]))) < 2) {
    stat_list[[d]] <- data.frame(definition_id = d, status = "skipped_no_variation", stringsAsFactors = FALSE)
    next
  }
  message("Fitting HM/CM ", d, " on ", outcome)
  fml <- as.formula(paste0(
    "n_events ~ ", d, " + month_f + splines::ns(time_index, df = ", trend_df, ") + offset(offset_log)"
  ))
  model <- tryCatch(
    MASS::glm.nb(fml, data = panel),
    error = function(e) stats::glm(fml, data = panel, family = stats::quasipoisson())
  )
  vcov_mat <- tryCatch(sandwich::vcovHC(model, type = "HC1"), error = function(e) NULL)
  est <- extract_rr(model, vcov_mat, d)
  if (is.null(est)) {
    stat_list[[d]] <- data.frame(definition_id = d, status = "failed_no_coef", stringsAsFactors = FALSE)
    next
  }
  est$definition_id <- d
  est$outcome <- outcome
  est$data_status <- paste(unique(panel$data_status), collapse = ";")
  est$n_months <- length(unique(panel$month_id))
  est$n_flagged_months <- sum(panel[[d]] == 1, na.rm = TRUE)
  est$reference_policy <- "PROVISIONAL_study_window_not_Hogan_locked"
  est_list[[d]] <- est
  stat_list[[d]] <- data.frame(definition_id = d, status = "ok", stringsAsFactors = FALSE)
}

est_df <- dplyr::bind_rows(est_list)
stat_df <- dplyr::bind_rows(stat_list)
out_tab <- file.path(root, "outputs", "tables")
write_csv_safe(est_df, file.path(out_tab, paste0(outcome, "_hm_cm_panel_estimates.csv")))
write_csv_safe(stat_df, file.path(out_tab, paste0(outcome, "_hm_cm_panel_status.csv")))

rep <- file.path(root, "outputs", "reports", paste0(outcome, "_hm_cm_panel_summary.md"))
writeLines(c(
  paste0("# HM/CM panel summary — ", toupper(outcome)),
  "",
  paste0("- Run at: ", Sys.time()),
  paste0("- Definitions OK: ", sum(stat_df$status == "ok"), " / ", nrow(stat_df)),
  "- **All estimates are provisional** until Hogan locks reference-period thresholds.",
  "",
  "| ID | Status |",
  "|---|---|",
  paste0("| ", stat_df$definition_id, " | ", stat_df$status, " |")
), rep)

message("HM/CM panel complete for ", outcome, "; OK=", sum(stat_df$status == "ok"))
