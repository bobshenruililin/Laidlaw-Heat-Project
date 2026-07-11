#!/usr/bin/env Rscript
# 11_fit_main_models_real.R
# Twin of the synthetic model script for approved HA panels only.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines", "sandwich", "lmtest"))

panel_path <- file.path(root, "data_processed", "ha_analysis_panel.csv")
if (!file.exists(panel_path)) {
  stop("Missing ", panel_path, " — run 08b_merge_real_ha_panel.R first.")
}

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
stop_if_synthetic(panel)

# Reuse the synthetic script's model ladder by sourcing after binding panel.
# For maintainability we keep an explicit twin rather than silent source tricks.
panel <- panel |>
  dplyr::mutate(
    age_group = factor(age_group, levels = cfg$population$preferred_age_groups),
    sex = factor(sex, levels = cfg$sexes),
    diagnosis_group = factor(diagnosis_group, levels = cfg$diagnosis_groups),
    covid_phase = factor(covid_phase, levels = names(cfg$covid_phases)),
    month_f = factor(month),
    stratum_id = interaction(age_group, sex, diagnosis_group, drop = TRUE)
  )

extract_rr <- function(model, vcov_mat = NULL, terms = NULL) {
  ct <- if (is.null(vcov_mat)) {
    summary(model)$coefficients
  } else {
    as.matrix(lmtest::coeftest(model, vcov. = vcov_mat))
  }
  nm <- rownames(ct)
  keep <- if (!is.null(terms)) nm[nm %in% terms] else nm
  out <- data.frame(
    term = keep,
    estimate = ct[keep, 1],
    std_error = ct[keep, 2],
    statistic = ct[keep, 3],
    p_value = ct[keep, 4],
    stringsAsFactors = FALSE
  )
  out$rr <- exp(out$estimate)
  out$rr_low <- exp(out$estimate - 1.96 * out$std_error)
  out$rr_high <- exp(out$estimate + 1.96 * out$std_error)
  out
}

message("Fitting REAL primary NB model (hot nights + cold days)...")
model_main <- MASS::glm.nb(
  n_events ~
    I(hot_nights / 5) +
    I(cold_days / 5) +
    age_group +
    sex +
    diagnosis_group +
    month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase +
    offset(offset_log),
  data = panel
)

vcov_tw <- tryCatch(
  sandwich::vcovCL(model_main, cluster = ~ month_id + stratum_id, type = "HC1"),
  error = function(e) {
    message("Two-way cluster failed (", conditionMessage(e), "); falling back to HC1.")
    sandwich::vcovHC(model_main, type = "HC1")
  }
)

rn <- names(coef(model_main))
focus_terms <- rn[grepl("hot_nights|cold_days", rn)]
res_main <- extract_rr(model_main, vcov_tw, terms = focus_terms)
res_main$model <- "main_nb_hot_nights_cold_days"
res_main$data_status <- "HA_APPROVED_AGGREGATE"

write_csv_safe(res_main, file.path(root, "outputs", "tables", "ha_model_results.csv"))
saveRDS(
  list(model_main = model_main, vcov = vcov_tw),
  file.path(root, "outputs", "model_objects", "ha_models.rds")
)
message("Real model fit complete. Results: outputs/tables/ha_model_results.csv")
