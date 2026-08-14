#!/usr/bin/env Rscript
# 63_year_shift_health.R
# Gate-3-open diagnostic. Re-fit the twelve core contrasts with exposure
# displaced by 12 and 24 months. Does not invent HA rows. Exits 0 with a
# PARKED_NO_PANEL JSON if gitignored panels are absent (A60).
#
# A pass does not upgrade any q and is not a headline.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "MASS", "splines", "sandwich"))

out_dir <- file.path(root, "outputs", "year_shift")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

chd_path <- file.path(root, "data_processed", "chd_analysis_panel.csv")
hf_path <- file.path(root, "data_processed", "hf_analysis_panel.csv")
status_path <- file.path(out_dir, "health_refit_status.json")

write_status <- function(status, extra = "") {
  line <- sprintf(
    '{"status":"%s","gate3":"open","headline":false%s}\n',
    status,
    extra
  )
  writeLines(line, status_path, sep = "")
}

if (!file.exists(chd_path) || !file.exists(hf_path)) {
  write_status(
    "PARKED_NO_PANEL",
    paste0(
      ',"detail":"gitignored CHD/HF analysis panels are not on disk; no HA rows invented"'
    )
  )
  message("PARKED_NO_PANEL: analysis panels absent (A60).")
  quit(save = "no", status = 0)
}

core_specs <- list(
  P01A = list(exposure = "mean_temp", scale = 1, label = "Mean temperature, per 1 C"),
  P02A = list(exposure = "mean_tmax", scale = 1, label = "Mean maximum temperature, per 1 C"),
  P02B = list(exposure = "mean_tmin", scale = 1, label = "Mean minimum temperature, per 1 C"),
  P04A = list(exposure = "hot_nights", scale = 5, label = "Hot nights, per 5 days"),
  P04B = list(exposure = "cold_days", scale = 5, label = "Cold days, per 5 days"),
  P04C = list(exposure = "very_hot_days", scale = 5, label = "Very hot days, per 5 days")
)

fit_one <- function(dat, exposure, scale) {
  term <- if (identical(scale, 1)) exposure else sprintf("I(%s/%s)", exposure, scale)
  fml <- stats::as.formula(
    paste(
      "n_events ~", term,
      "+ month_f + splines::ns(time_index, df = 4) + offset(offset_log_days)"
    )
  )
  model <- MASS::glm.nb(fml, data = dat)
  vm <- sandwich::NeweyWest(model, lag = 6L, prewhite = FALSE, adjust = TRUE)
  b <- unname(stats::coef(model)[term])
  se <- sqrt(diag(vm))[term]
  data.frame(
    estimate = b,
    std_error = unname(se),
    rr = exp(b),
    rr_low = exp(b - 1.96 * se),
    rr_high = exp(b + 1.96 * se),
    p_value = 2 * stats::pnorm(abs(b / se), lower.tail = FALSE),
    n_months = nrow(dat),
    stringsAsFactors = FALSE
  )
}

rows <- list()
for (outcome in c("chd", "hf")) {
  panel_path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  dat0 <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
  dat0 <- dat0[order(dat0$time_index), ]
  dat0$month_f <- factor(dat0$month)
  stopifnot(nrow(dat0) == 132L, identical(unique(as.character(dat0$data_status)), "HA_APPROVED_AGGREGATE"))
  for (lag in c(0L, 12L, 24L)) {
    for (pid in names(core_specs)) {
      spec <- core_specs[[pid]]
      dat <- dat0
      if (lag > 0L) {
        dat[[spec$exposure]] <- dplyr::lag(dat[[spec$exposure]], n = lag)
        dat <- dat[stats::complete.cases(dat[, spec$exposure, drop = FALSE]), ]
      }
      est <- fit_one(dat, spec$exposure, spec$scale)
      est$outcome <- outcome
      est$pathway_id <- pid
      est$exposure <- spec$exposure
      est$exposure_label <- spec$label
      est$year_shift <- lag
      est$family <- "negative_binomial"
      est$offset_policy <- "days_only"
      est$se_method <- "NeweyWest_lag6"
      est$data_status <- "HA_APPROVED_AGGREGATE"
      est$analysis_status <- "Gate-3-open diagnostic; not a headline; q not upgraded"
      rows[[length(rows) + 1L]] <- est
    }
  }
}

out <- dplyr::bind_rows(rows)
utils::write.csv(out, file.path(out_dir, "year_shift_core_models.csv"), row.names = FALSE)
write_status("RAN", sprintf(',"n_rows":%d', nrow(out)))
message("Wrote ", file.path(out_dir, "year_shift_core_models.csv"))
