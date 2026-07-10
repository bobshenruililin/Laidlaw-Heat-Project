#!/usr/bin/env Rscript
# 10_descriptive_figures.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr", "ggplot2"))

climate <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                           stringsAsFactors = FALSE)
pollution <- utils::read.csv(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"),
                             stringsAsFactors = FALSE)
pop <- utils::read.csv(file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"),
                       stringsAsFactors = FALSE)
annual <- utils::read.csv(file.path(root, "outputs", "tables", "weather_annual_extremes_2013_2023.csv"),
                          stringsAsFactors = FALSE)

fig_dir <- file.path(root, "outputs", "figures")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

theme_set(theme_bw(base_size = 12))

# Figure 1: annual extremes
ann_long <- annual |>
  tidyr::pivot_longer(cols = c(hot_nights, very_hot_days, extremely_hot_days, cold_days),
                      names_to = "metric", values_to = "days")
p1 <- ggplot(ann_long, aes(x = year, y = days, colour = metric)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  labs(
    title = "Annual thermal extremes at HKO Headquarters",
    subtitle = "Official thresholds; derived from dailyExtract",
    x = NULL, y = "Days per year", colour = NULL
  ) +
  scale_x_continuous(breaks = 2013:2023)
ggsave(file.path(fig_dir, "fig01_annual_thermal_extremes.png"), p1, width = 9, height = 5, dpi = 150)

# Figure 2: monthly temperature and hot nights
climate$month_date <- as.Date(climate$month_date)
p2 <- ggplot(climate, aes(x = month_date)) +
  geom_col(aes(y = hot_nights), fill = "#c45c26", alpha = 0.7) +
  geom_line(aes(y = mean_temp), colour = "#1f4e79", linewidth = 0.8) +
  labs(
    title = "Monthly mean temperature and hot nights",
    subtitle = "Bars: hot nights (Tmin ≥ 28°C); line: mean temperature (°C)",
    x = NULL, y = "Value"
  )
ggsave(file.path(fig_dir, "fig02_monthly_temp_hot_nights.png"), p2, width = 10, height = 5, dpi = 150)

# Figure 3: pollution trends
if (all(c("NO2", "O3", "PM25", "PM10") %in% names(pollution))) {
  pollution$month_date <- as.Date(paste0(pollution$month_id, "-01"))
  pol_long <- pollution |>
    tidyr::pivot_longer(cols = c(NO2, O3, PM25, PM10), names_to = "pollutant", values_to = "value")
  subtitle_pol <- if (any(grepl("PLACEHOLDER", pollution$data_status %||% ""))) {
    "PLACEHOLDER series for pipeline testing — replace with EPIC data"
  } else {
    "Imported EPD-based monthly series"
  }
  p3 <- ggplot(pol_long, aes(x = month_date, y = value, colour = pollutant)) +
    geom_line(alpha = 0.85) +
    labs(title = "Monthly air pollution series", subtitle = subtitle_pol, x = NULL, y = "Concentration", colour = NULL)
  ggsave(file.path(fig_dir, "fig03_pollution_trends.png"), p3, width = 10, height = 5, dpi = 150)
}

# Figure 4: population aging
pop_mid <- pop |>
  dplyr::filter(month == 6) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop")
pop_mid$age_group <- factor(pop_mid$age_group, levels = cfg$population$preferred_age_groups)
subtitle_pop <- if (any(grepl("SYNTHETIC", pop$data_status %||% ""))) {
    "SYNTHETIC denominators for pipeline testing — replace with C&SD"
  } else {
    "C&SD-based mid-year denominators"
  }
p4 <- ggplot(pop_mid, aes(x = year, y = population / 1000, colour = age_group)) +
  geom_line() +
  labs(
    title = "Mid-year population by age group (35+)",
    subtitle = subtitle_pop,
    x = NULL, y = "Population (thousands)", colour = "Age group"
  )
ggsave(file.path(fig_dir, "fig04_population_aging.png"), p4, width = 10, height = 6, dpi = 150)

# Copy figure shells / captions
writeLines(c(
  "# Figure captions (first-stage)",
  "",
  "1. Annual hot nights, very hot days, extremely hot days, and cold days at HKO.",
  "2. Monthly mean temperature and hot-night counts.",
  "3. Pollution trends (real EPD or PLACEHOLDER).",
  "4. Population aging by age group (real C&SD or SYNTHETIC).",
  "5–7. Admission-rate and exposure-response figures deferred until HA data arrive."
), file.path(root, "outputs", "figure_shells", "figure_captions.md"))

message("Descriptive figures written to ", fig_dir)
