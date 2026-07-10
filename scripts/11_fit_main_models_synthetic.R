#!/usr/bin/env Rscript
# 11_fit_main_models_synthetic.R
# Fits planned NB models on SYNTHETIC data only — for workflow testing.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines", "sandwich", "lmtest"))

panel <- utils::read.csv(file.path(root, "data_processed", "synthetic_analysis_panel.csv"),
                         stringsAsFactors = FALSE)
stop_if_not_synthetic(panel)

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
  if (!is.null(terms)) {
    keep <- nm[nm %in% terms]
  } else {
    keep <- nm
  }
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

message("Fitting primary NB model (hot nights + cold days)...")
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

focus_terms <- c("I(hot_nights/5)", "I(cold_days/5)")
# MASS may name with spaces differently; match flexibly
rn <- names(coef(model_main))
focus_terms <- rn[grepl("hot_nights|cold_days", rn)]

res_main <- extract_rr(model_main, vcov_tw, terms = focus_terms)
res_main$model <- "main_nb_hot_nights_cold_days"
res_main$data_status <- "SYNTHETIC"

message("Fitting alternative heat model (very hot days + cold days)...")
model_vhd <- MASS::glm.nb(
  n_events ~
    I(very_hot_days / 5) +
    I(cold_days / 5) +
    age_group + sex + diagnosis_group + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  data = panel
)
rn2 <- names(coef(model_vhd))
res_vhd <- extract_rr(model_vhd, terms = rn2[grepl("very_hot_days|cold_days", rn2)])
res_vhd$model <- "alt_nb_very_hot_days_cold_days"
res_vhd$data_status <- "SYNTHETIC"

message("Fitting continuous temperature model...")
model_temp <- MASS::glm.nb(
  n_events ~
    mean_tmin +
    age_group + sex + diagnosis_group + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  data = panel
)
res_temp <- extract_rr(model_temp, terms = "mean_tmin")
res_temp$model <- "cont_mean_tmin"
res_temp$data_status <- "SYNTHETIC"

message("Fitting age-interaction model...")
model_age <- MASS::glm.nb(
  n_events ~
    I(hot_nights / 5) * age_group +
    I(cold_days / 5) * age_group +
    sex + diagnosis_group + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  data = panel
)

message("Fitting diagnosis-interaction model...")
model_dx <- MASS::glm.nb(
  n_events ~
    I(hot_nights / 5) * diagnosis_group +
    I(cold_days / 5) * diagnosis_group +
    age_group + sex + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  data = panel
)

# Staged pollution models (even if pollution is placeholder — workflow only)
message("Fitting staged pollution models...")
model_no_pol <- model_main
model_o3 <- MASS::glm.nb(
  n_events ~
    I(hot_nights / 5) + I(cold_days / 5) + O3 +
    I(hot_nights / 5):O3 +
    age_group + sex + diagnosis_group + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  data = panel
)

# Poisson comparison for overdispersion check
model_pois <- glm(
  n_events ~
    I(hot_nights / 5) + I(cold_days / 5) +
    age_group + sex + diagnosis_group + month_f +
    splines::ns(time_index, df = cfg$modeling$time_trend_df) +
    covid_phase + offset(offset_log),
  family = poisson(),
  data = panel
)
disp <- sum(residuals(model_pois, type = "pearson")^2) / model_pois$df.residual

results <- dplyr::bind_rows(res_main, res_vhd, res_temp)
results$note <- "SYNTHETIC workflow demonstration only; not substantive epidemiologic findings"
write_csv_safe(results, file.path(root, "outputs", "tables", "synthetic_model_results.csv"))

# Save model objects
saveRDS(list(
  model_main = model_main,
  model_vhd = model_vhd,
  model_temp = model_temp,
  model_age = model_age,
  model_dx = model_dx,
  model_o3 = model_o3,
  model_pois = model_pois,
  vcov_main = vcov_tw,
  poisson_dispersion = disp,
  data_status = "SYNTHETIC"
), file.path(root, "outputs", "model_objects", "synthetic_models.rds"))

disp_df <- data.frame(
  poisson_pearson_dispersion = disp,
  nb_theta = model_main$theta,
  nb_converged = model_main$converged,
  data_status = "SYNTHETIC",
  stringsAsFactors = FALSE
)
write_csv_safe(disp_df, file.path(root, "outputs", "tables", "synthetic_dispersion_summary.csv"))

message("Synthetic model fitting complete.")
message("Poisson Pearson dispersion: ", round(disp, 3))
message("NB theta: ", round(model_main$theta, 3))
