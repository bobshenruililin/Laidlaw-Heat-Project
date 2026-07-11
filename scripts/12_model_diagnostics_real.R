#!/usr/bin/env Rscript
# 12_model_diagnostics_real.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "ggplot2", "MASS"))

panel_path <- file.path(root, "data_processed", "ha_analysis_panel.csv")
mod_path <- file.path(root, "outputs", "model_objects", "ha_models.rds")
if (!file.exists(panel_path) || !file.exists(mod_path)) {
  stop("Real diagnostics require ha_analysis_panel.csv and ha_models.rds")
}

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
stop_if_synthetic(panel)
mods <- readRDS(mod_path)
model_main <- mods$model_main

diag_dir <- file.path(root, "outputs", "figures", "ha_diagnostic_plots")
dir.create(diag_dir, recursive = TRUE, showWarnings = FALSE)

panel$resid_pearson <- residuals(model_main, type = "pearson")
panel$fitted_mu <- fitted(model_main)

monthly_resid <- panel |>
  dplyr::group_by(month_id, time_index) |>
  dplyr::summarise(mean_pearson = mean(resid_pearson), .groups = "drop") |>
  dplyr::arrange(time_index)

png(file.path(diag_dir, "acf_monthly_pearson_residuals.png"), width = 800, height = 500)
acf(monthly_resid$mean_pearson, main = "ACF: monthly mean Pearson residuals (HA)")
dev.off()

png(file.path(diag_dir, "pacf_monthly_pearson_residuals.png"), width = 800, height = 500)
pacf(monthly_resid$mean_pearson, main = "PACF: monthly mean Pearson residuals (HA)")
dev.off()

disp <- data.frame(
  residual_df = df.residual(model_main),
  deviance = deviance(model_main),
  aic = AIC(model_main),
  theta = model_main$theta,
  stringsAsFactors = FALSE
)
write_csv_safe(disp, file.path(root, "outputs", "tables", "ha_dispersion_summary.csv"))
message("Real diagnostics written to ", diag_dir)
