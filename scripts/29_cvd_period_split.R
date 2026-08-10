#!/usr/bin/env Rscript
# 29_cvd_period_split.R
# Pre-COVID (year < 2020) vs full-period comparison for P02-like Tmax/Tmin model.
# Outcomes: chd, hf. Controls: month_f + ns(time_index, 4); offset = population x days.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("dplyr", "MASS", "splines", "sandwich", "lmtest"))

outcomes <- c("chd", "hf")
trend_df <- cfg$modeling$time_trend_df %||% 4L
periods <- list(
  full_2013_2023 = function(d) d,
  pre_covid_year_lt_2020 = function(d) d[d$year < 2020, , drop = FALSE]
)

extract_rr <- function(model, vcov_mat = NULL, keep_pattern = "mean_t(max|min)") {
  ct <- tryCatch(
    {
      if (is.null(vcov_mat)) summary(model)$coefficients else as.matrix(lmtest::coeftest(model, vcov. = vcov_mat))
    },
    error = function(e) summary(model)$coefficients
  )
  nm <- rownames(ct)
  nm <- nm[grepl(keep_pattern, nm)]
  if (!length(nm)) return(data.frame())
  data.frame(
    term = nm,
    estimate = ct[nm, 1],
    std_error = ct[nm, 2],
    statistic = ct[nm, 3],
    p_value = ct[nm, 4],
    rr = exp(ct[nm, 1]),
    rr_low = exp(ct[nm, 1] - 1.96 * ct[nm, 2]),
    rr_high = exp(ct[nm, 1] + 1.96 * ct[nm, 2]),
    stringsAsFactors = FALSE
  )
}

fit_p02 <- function(dat) {
  fml <- as.formula(paste0(
    "n_events ~ mean_tmax + mean_tmin + month_f + splines::ns(time_index, df = ",
    trend_df, ") + offset(offset_log)"
  ))
  model <- tryCatch(
    MASS::glm.nb(fml, data = dat),
    error = function(e) {
      message("glm.nb failed (", conditionMessage(e), "); quasipoisson")
      stats::glm(fml, data = dat, family = stats::quasipoisson())
    }
  )
  vcov_mat <- tryCatch(sandwich::vcovHC(model, type = "HC1"), error = function(e) NULL)
  list(model = model, est = extract_rr(model, vcov_mat))
}

rows <- list()
for (outcome in outcomes) {
  path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  if (!file.exists(path)) stop("Missing ", path)
  panel <- utils::read.csv(path, stringsAsFactors = FALSE)
  stop_if_synthetic(panel)
  panel <- panel |> dplyr::mutate(month_f = factor(month))

  for (pname in names(periods)) {
    d <- periods[[pname]](panel)
    # Recompute time_index within period so spline is well-defined on the subset
    d$time_index <- match(d$month_id, sort(unique(d$month_id)))
    d$month_f <- factor(d$month)
    message("Fitting P02-like ", outcome, " / ", pname, " (n=", nrow(d), ")")
    res <- fit_p02(d)
    if (!nrow(res$est)) next
    est <- res$est
    est$outcome <- outcome
    est$period <- pname
    est$pathway_like <- "P02"
    est$n_months <- length(unique(d$month_id))
    est$n_rows <- nrow(d)
    est$data_status <- paste(unique(d$data_status), collapse = ";")
    est$family <- paste(class(res$model), collapse = "/")
    est$aic <- tryCatch(AIC(res$model), error = function(e) NA_real_)
    rows[[paste(outcome, pname)]] <- est
  }
}

long <- dplyr::bind_rows(rows) |>
  dplyr::arrange(outcome, term, period)

out_long <- file.path(root, "outputs", "tables", "cvd_period_split_P02.csv")
write_csv_safe(long, out_long)

# Comparison table: full vs pre-COVID side by side
cmp <- long |>
  dplyr::mutate(
    rr_ci = sprintf("%.3f (%.3f-%.3f)", rr, rr_low, rr_high)
  ) |>
  dplyr::select(outcome, term, period, rr_ci, p_value, n_months)

ensure_packages(c("tidyr"))
cmp_wide <- cmp |>
  tidyr::pivot_wider(
    names_from = period,
    values_from = c(rr_ci, p_value, n_months)
  )
write_csv_safe(cmp_wide, file.path(root, "outputs", "tables", "cvd_period_split_P02_comparison.csv"))

message("Period-split P02 comparison written: ", out_long)
