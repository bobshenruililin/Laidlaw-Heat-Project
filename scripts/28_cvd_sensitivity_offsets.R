#!/usr/bin/env Rscript
# 28_cvd_sensitivity_offsets.R
# Offset sensitivity for CHD/HF headline exposures:
#   (a) population x days (baseline offset_log)
#   (b) days-only (offset_log_days)
#   (c) no offset (raw counts)
# Controls: month_f + ns(time_index, 4). Same across variants.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("dplyr", "tidyr", "MASS", "splines", "sandwich", "lmtest"))

outcomes <- c("chd", "hf")
trend_df <- cfg$modeling$time_trend_df %||% 4L

# Headline continuous exposures as-is; extreme-day counts per 5 days (P04 scale)
exposure_specs <- list(
  list(id = "P01A", name = "mean_temp", rhs = "mean_temp", keep = "mean_temp"),
  list(id = "P02A", name = "mean_tmax", rhs = "mean_tmax", keep = "mean_tmax"),
  list(id = "P02B", name = "mean_tmin", rhs = "mean_tmin", keep = "mean_tmin"),
  list(id = "P04A", name = "hot_nights", rhs = "I(hot_nights/5)", keep = "hot_nights"),
  list(id = "P04B", name = "cold_days", rhs = "I(cold_days/5)", keep = "cold_days"),
  list(id = "P04C", name = "very_hot_days", rhs = "I(very_hot_days/5)", keep = "very_hot_days")
)
joint_specs <- list(
  list(
    id = "P02",
    name = "joint_tmax_tmin",
    rhs = "mean_tmax + mean_tmin",
    keep = "mean_tmax|mean_tmin"
  ),
  list(
    id = "P04",
    name = "joint_extreme_days",
    rhs = "I(hot_nights/5) + I(cold_days/5) + I(very_hot_days/5)",
    keep = "hot_nights|cold_days|very_hot_days"
  )
)

offset_specs <- list(
  list(id = "pop_x_days", label = "population_x_days", offset_term = "offset(offset_log)"),
  list(id = "days_only", label = "days_only", offset_term = "offset(offset_log_days)"),
  list(id = "no_offset", label = "no_offset_counts", offset_term = NULL)
)

extract_rr <- function(model, vcov_mat = NULL, keep_pattern) {
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

fit_one <- function(dat, exposure_rhs, keep_pattern, offset_term) {
  ctrl <- paste0("month_f + splines::ns(time_index, df = ", trend_df, ")")
  rhs <- paste(exposure_rhs, ctrl, sep = " + ")
  if (!is.null(offset_term)) {
    fml <- as.formula(paste("n_events ~", rhs, "+", offset_term))
  } else {
    fml <- as.formula(paste("n_events ~", rhs))
  }
  model <- tryCatch(
    MASS::glm.nb(fml, data = dat),
    error = function(e) {
      message("glm.nb failed (", conditionMessage(e), "); quasipoisson")
      stats::glm(fml, data = dat, family = stats::quasipoisson())
    }
  )
  vcov_mat <- tryCatch(
    sandwich::NeweyWest(model, lag = 6, prewhite = FALSE, adjust = TRUE),
    error = function(e) NULL
  )
  list(model = model, est = extract_rr(model, vcov_mat, keep_pattern))
}

rows <- list()
for (outcome in outcomes) {
  path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  if (!file.exists(path)) stop("Missing ", path)
  panel <- utils::read.csv(path, stringsAsFactors = FALSE)
  stop_if_synthetic(panel)
  if (!identical(unique(as.character(panel$data_status)), "HA_APPROVED_AGGREGATE")) {
    stop("Offset sensitivity requires HA_APPROVED_AGGREGATE only")
  }
  panel <- panel |>
    dplyr::mutate(month_f = factor(month))

  for (ex in c(exposure_specs, joint_specs)) {
    for (off in offset_specs) {
      message("Fitting ", outcome, " / ", ex$name, " / ", off$id)
      res <- fit_one(panel, ex$rhs, ex$keep, off$offset_term)
      if (!nrow(res$est)) {
        warning("No estimate for ", outcome, " ", ex$name, " ", off$id)
        next
      }
      est <- res$est
      est$outcome <- outcome
      est$pathway_id <- ex$id
      est$exposure <- ex$name
      est$model_structure <- if (grepl("^joint_", ex$name)) "joint_exploratory" else "single_exposure"
      est$exposure_rhs <- ex$rhs
      est$offset_type <- off$id
      est$offset_label <- off$label
      est$n_months <- length(unique(panel$month_id))
      est$data_status <- paste(unique(panel$data_status), collapse = ";")
      est$family <- paste(class(res$model), collapse = "/")
      est$se_method <- "NeweyWest_lag6"
      est$aic <- tryCatch(AIC(res$model), error = function(e) NA_real_)
      rows[[paste(outcome, ex$name, off$id)]] <- est
    }
  }
}

out <- dplyr::bind_rows(rows)
out <- out |>
  dplyr::select(
    outcome, pathway_id, exposure, model_structure, exposure_rhs, offset_type, offset_label, term,
    estimate, std_error, statistic, p_value, rr, rr_low, rr_high,
    n_months, data_status, family, se_method, aic
  ) |>
  dplyr::arrange(outcome, exposure, offset_type)

out_path <- file.path(root, "outputs", "tables", "cvd_offset_sensitivity.csv")
write_csv_safe(out, out_path)

# Wide RR comparison for quick reading
wide <- out |>
  dplyr::mutate(rr_ci = sprintf("%.3f (%.3f-%.3f)", rr, rr_low, rr_high)) |>
  dplyr::select(outcome, pathway_id, exposure, model_structure, term, offset_type, rr_ci, p_value)

wide_rr <- tidyr::pivot_wider(
  wide |> dplyr::select(outcome, pathway_id, exposure, model_structure, term, offset_type, rr_ci),
  names_from = offset_type, values_from = rr_ci
)
wide_p <- tidyr::pivot_wider(
  wide |> dplyr::select(outcome, pathway_id, exposure, model_structure, term, offset_type, p_value),
  names_from = offset_type, values_from = p_value, names_prefix = "p_"
)
wide_out <- dplyr::left_join(
  wide_rr,
  wide_p,
  by = c("outcome", "pathway_id", "exposure", "model_structure", "term")
)
write_csv_safe(wide_out, file.path(root, "outputs", "tables", "cvd_offset_sensitivity_wide.csv"))

message("Offset sensitivity complete: ", nrow(out), " rows -> ", out_path)
