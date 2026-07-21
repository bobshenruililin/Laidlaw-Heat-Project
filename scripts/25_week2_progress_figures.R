#!/usr/bin/env Rscript
# Build Week-2 progress figures (public environmental data only).

source("scripts/utils.R")
root <- project_root()
setwd(root)
ensure_packages(c("ggplot2", "dplyr", "tidyr", "scales"))

out_dir <- file.path(root, "figures", "week2_progress")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

clim <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                        stringsAsFactors = FALSE)
pol <- utils::read.csv(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"),
                       stringsAsFactors = FALSE)
exp <- utils::read.csv(file.path(root, "data_processed", "exposures_monthly_2013_2023.csv"),
                       stringsAsFactors = FALSE)

# --- Fig A: annual extremes coexistence (clean for slides) ---
ann <- clim |>
  dplyr::group_by(year) |>
  dplyr::summarise(
    hot_nights = sum(hot_nights, na.rm = TRUE),
    very_hot_days = sum(very_hot_days, na.rm = TRUE),
    cold_days = sum(cold_days, na.rm = TRUE),
    .groups = "drop"
  ) |>
  tidyr::pivot_longer(-year, names_to = "metric", values_to = "days") |>
  dplyr::mutate(
    metric = factor(
      metric,
      levels = c("hot_nights", "very_hot_days", "cold_days"),
      labels = c("Hot nights", "Very hot days", "Cold days")
    )
  )

p_a <- ggplot2::ggplot(ann, ggplot2::aes(year, days, colour = metric)) +
  ggplot2::geom_line(linewidth = 1.05) +
  ggplot2::geom_point(size = 2.1) +
  ggplot2::scale_colour_manual(values = c("#A85A3A", "#C4873A", "#3D6B6E")) +
  ggplot2::scale_x_continuous(breaks = seq(2013, 2023, 2)) +
  ggplot2::labs(
    title = "Official thermal extremes at HKO Headquarters",
    subtitle = "Annual counts, 2013-2023 (environmental data only)",
    x = NULL, y = "Days per year", colour = NULL
  ) +
  ggplot2::theme_minimal(base_size = 12) +
  ggplot2::theme(
    legend.position = "bottom",
    panel.grid.minor = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold", colour = "#1B2A41"),
    plot.subtitle = ggplot2::element_text(colour = "#3D6B6E")
  )
ggplot2::ggsave(file.path(out_dir, "fig_annual_extremes.pdf"), p_a, width = 9.2, height = 4.4)
ggplot2::ggsave(file.path(out_dir, "fig_annual_extremes.png"), p_a, width = 9.2, height = 4.4, dpi = 160)

# --- Fig B: pollution annual means ---
pol$year <- as.integer(substr(pol$month_id, 1, 4))
pol_ann <- pol |>
  dplyr::group_by(year) |>
  dplyr::summarise(
    NO2 = mean(NO2, na.rm = TRUE),
    O3 = mean(O3, na.rm = TRUE),
    PM25 = mean(PM25, na.rm = TRUE),
    PM10 = mean(PM10, na.rm = TRUE),
    .groups = "drop"
  ) |>
  tidyr::pivot_longer(-year, names_to = "pollutant", values_to = "ug") |>
  dplyr::mutate(
    pollutant = factor(pollutant, levels = c("NO2", "O3", "PM25", "PM10"),
                       labels = c("NO2", "O3", "PM2.5", "PM10"))
  )

p_b <- ggplot2::ggplot(pol_ann, ggplot2::aes(year, ug, colour = pollutant)) +
  ggplot2::geom_line(linewidth = 1.05) +
  ggplot2::geom_point(size = 2) +
  ggplot2::scale_colour_manual(values = c("#1B2A41", "#A85A3A", "#3D6B6E", "#6B7C8A")) +
  ggplot2::scale_x_continuous(breaks = seq(2013, 2023, 2)) +
  ggplot2::labs(
    title = "EPD EPIC general-station pollution (REAL)",
    subtitle = "Annual means of monthly averages, 2013-2023",
    x = NULL, y = expression(mu*g/m^3), colour = NULL
  ) +
  ggplot2::theme_minimal(base_size = 12) +
  ggplot2::theme(
    legend.position = "bottom",
    panel.grid.minor = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold", colour = "#1B2A41"),
    plot.subtitle = ggplot2::element_text(colour = "#3D6B6E")
  )
ggplot2::ggsave(file.path(out_dir, "fig_pollution_annual.pdf"), p_b, width = 9.2, height = 4.4)
ggplot2::ggsave(file.path(out_dir, "fig_pollution_annual.png"), p_b, width = 9.2, height = 4.4, dpi = 160)

# --- Fig C: readiness arc (simple annotated bars) ---
ready <- data.frame(
  layer = factor(
    c("HKO climate", "C&SD population", "EPD pollution", "CHP flu",
      "Pathway panel", "Stroke aggregates"),
    levels = rev(c("HKO climate", "C&SD population", "EPD pollution", "CHP flu",
                   "Pathway panel", "Stroke aggregates"))
  ),
  status = c("Ready", "Ready", "Ready", "Ready (121/132)", "Ready (dry-run)", "Awaiting"),
  score = c(1, 1, 1, 0.92, 1, 0.15)
)

p_c <- ggplot2::ggplot(ready, ggplot2::aes(score, layer, fill = score > 0.5)) +
  ggplot2::geom_col(width = 0.62) +
  ggplot2::geom_text(ggplot2::aes(label = status), hjust = -0.05, size = 3.4, colour = "#1B2A41") +
  ggplot2::scale_fill_manual(values = c("#C9B8A8", "#3D6B6E"), guide = "none") +
  ggplot2::scale_x_continuous(limits = c(0, 1.45), breaks = NULL) +
  ggplot2::labs(
    title = "Week 2 readiness: one missing piece",
    subtitle = "Public layers and analysis plumbing are ready; stroke aggregates unlock inference",
    x = NULL, y = NULL
  ) +
  ggplot2::theme_minimal(base_size = 12) +
  ggplot2::theme(
    panel.grid = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold", colour = "#1B2A41"),
    plot.subtitle = ggplot2::element_text(colour = "#3D6B6E"),
    axis.text.y = ggplot2::element_text(face = "bold")
  )
ggplot2::ggsave(file.path(out_dir, "fig_readiness.pdf"), p_c, width = 9.0, height = 4.0)
ggplot2::ggsave(file.path(out_dir, "fig_readiness.png"), p_c, width = 9.0, height = 4.0, dpi = 160)

# --- Fig D: heatwave-month indicator counts ---
hw <- data.frame(
  definition = c("p90 month", "p95 month", "p97.5 month", "VHD spell >=3", "2D3N month"),
  months = c(
    sum(exp$hw_month_mean_temp_ge_p90),
    sum(exp$hw_month_mean_temp_ge_p95),
    sum(exp$hw_month_mean_temp_ge_p975),
    sum(exp$hw_month_has_vhd_spell_ge3),
    sum(exp$month_has_2d3n_window)
  )
)
hw$definition <- factor(hw$definition, levels = rev(hw$definition))

p_d <- ggplot2::ggplot(hw, ggplot2::aes(months, definition)) +
  ggplot2::geom_col(fill = "#1B2A41", width = 0.62) +
  ggplot2::geom_text(ggplot2::aes(label = months), hjust = -0.2, size = 3.6, colour = "#1B2A41") +
  ggplot2::scale_x_continuous(limits = c(0, max(hw$months) * 1.18)) +
  ggplot2::labs(
    title = "Heatwave-month definitions disagree by design",
    subtitle = "Number of study months flagged (N = 132); motivates the multi-pathway panel",
    x = "Months flagged", y = NULL
  ) +
  ggplot2::theme_minimal(base_size = 12) +
  ggplot2::theme(
    panel.grid.minor = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold", colour = "#1B2A41"),
    plot.subtitle = ggplot2::element_text(colour = "#3D6B6E")
  )
ggplot2::ggsave(file.path(out_dir, "fig_hw_month_defs.pdf"), p_d, width = 8.8, height = 3.8)
ggplot2::ggsave(file.path(out_dir, "fig_hw_month_defs.png"), p_d, width = 8.8, height = 3.8, dpi = 160)

message("Week-2 figures written to ", out_dir)
