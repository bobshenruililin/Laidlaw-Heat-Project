#!/usr/bin/env Rscript
# 12_model_diagnostics.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "ggplot2", "MASS"))

panel <- utils::read.csv(file.path(root, "data_processed", "synthetic_analysis_panel.csv"),
                         stringsAsFactors = FALSE)
stop_if_not_synthetic(panel)
mods <- readRDS(file.path(root, "outputs", "model_objects", "synthetic_models.rds"))
model_main <- mods$model_main

diag_dir <- file.path(root, "outputs", "figures", "synthetic_diagnostic_plots")
dir.create(diag_dir, recursive = TRUE, showWarnings = FALSE)

panel$resid_pearson <- residuals(model_main, type = "pearson")
panel$resid_deviance <- residuals(model_main, type = "deviance")
panel$fitted_mu <- fitted(model_main)

# Aggregate residuals to monthly mean across strata for ACF
monthly_resid <- panel |>
  dplyr::group_by(month_id, time_index) |>
  dplyr::summarise(mean_pearson = mean(resid_pearson), .groups = "drop") |>
  dplyr::arrange(time_index)

png(file.path(diag_dir, "acf_monthly_pearson_residuals.png"), width = 800, height = 500)
acf(monthly_resid$mean_pearson, main = "ACF: monthly mean Pearson residuals (SYNTHETIC)")
dev.off()

png(file.path(diag_dir, "pacf_monthly_pearson_residuals.png"), width = 800, height = 500)
pacf(monthly_resid$mean_pearson, main = "PACF: monthly mean Pearson residuals (SYNTHETIC)")
dev.off()

theme_set(theme_bw(base_size = 12))
p1 <- ggplot(panel, aes(x = fitted_mu, y = resid_pearson)) +
  geom_point(alpha = 0.15, size = 0.7) +
  geom_hline(yintercept = 0, colour = "red") +
  scale_x_log10() +
  labs(title = "Pearson residuals vs fitted (SYNTHETIC)", x = "Fitted mean", y = "Pearson residual")
ggsave(file.path(diag_dir, "resid_vs_fitted.png"), p1, width = 8, height = 5, dpi = 150)

p2 <- ggplot(monthly_resid, aes(x = time_index, y = mean_pearson)) +
  geom_line() +
  geom_hline(yintercept = 0, colour = "red") +
  labs(title = "Monthly mean Pearson residuals over time (SYNTHETIC)", x = "Time index", y = "Mean residual")
ggsave(file.path(diag_dir, "monthly_resid_timeseries.png"), p2, width = 9, height = 4.5, dpi = 150)

# Simple Durbin-Watson on monthly residual series
dw <- function(x) {
  e <- x - mean(x)
  sum(diff(e)^2) / sum(e^2)
}
dw_stat <- dw(monthly_resid$mean_pearson)

diag_summary <- data.frame(
  n_obs = nrow(panel),
  poisson_dispersion = mods$poisson_dispersion,
  nb_theta = model_main$theta,
  nb_converged = isTRUE(model_main$converged),
  durbin_watson_monthly_resid = dw_stat,
  recommendation = "If residual ACF persists on real HA data, use clustered SE / GEE / GLARMA sensitivity",
  data_status = "SYNTHETIC",
  stringsAsFactors = FALSE
)
write_csv_safe(diag_summary, file.path(root, "outputs", "tables", "synthetic_diagnostics_summary.csv"))

message("Diagnostics written to ", diag_dir)
message("Durbin-Watson (monthly mean residuals): ", round(dw_stat, 3))
