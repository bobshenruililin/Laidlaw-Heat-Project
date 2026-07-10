#!/usr/bin/env Rscript
# 10_descriptive_figures.R
# Exploratory pipeline figures (not manuscript-ready).
# Validated HKO annual extremes figure is produced by scripts/14_*.R → figures/.

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

fig_dir <- file.path(root, "outputs", "figures", "exploratory")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

theme_set(theme_bw(base_size = 12))

# Monthly temperature and hot nights
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

# Pollution trends (placeholder until real EPIC series)
if (all(c("NO2", "O3", "PM25", "PM10") %in% names(pollution))) {
  pollution$month_date <- as.Date(paste0(pollution$month_id, "-01"))
  pol_long <- pollution |>
    tidyr::pivot_longer(cols = c(NO2, O3, PM25, PM10), names_to = "pollutant", values_to = "value")
  is_placeholder <- any(grepl("PLACEHOLDER", pollution$data_status %||% ""))
  subtitle_pol <- if (is_placeholder) {
    "PLACEHOLDER series for pipeline testing — replace with EPIC data"
  } else {
    "Imported EPD-based monthly series"
  }
  p3 <- ggplot(pol_long, aes(x = month_date, y = value, colour = pollutant)) +
    geom_line(alpha = 0.85) +
    labs(title = "Monthly air pollution series", subtitle = subtitle_pol, x = NULL, y = "Concentration", colour = NULL)
  pol_name <- if (is_placeholder) "PLACEHOLDER_pollution_trends.png" else "fig03_pollution_trends.png"
  ggsave(file.path(fig_dir, pol_name), p3, width = 10, height = 5, dpi = 150)
}

# Population aging
pop_mid <- pop |>
  dplyr::filter(month == 6) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop")
pop_mid$age_group <- factor(pop_mid$age_group, levels = cfg$population$preferred_age_groups)
is_synthetic_pop <- any(grepl("SYNTHETIC", pop$data_status %||% ""))
subtitle_pop <- if (is_synthetic_pop) {
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
pop_name <- if (is_synthetic_pop) "SYNTHETIC_population_aging.png" else "fig04_population_aging.png"
ggsave(file.path(fig_dir, pop_name), p4, width = 10, height = 6, dpi = 150)

writeLines(c(
  "# Exploratory figure captions",
  "",
  "These figures support pipeline checks. They are not manuscript figures.",
  "",
  "- `fig02_monthly_temp_hot_nights.png` — monthly mean temperature and hot-night counts (real HKO).",
  "- Pollution / population panels are labeled PLACEHOLDER or SYNTHETIC until real series replace them.",
  "- Validated annual extremes figure: `figures/hko_annual_extremes_2013_2023.pdf` (script 14).",
  "- Admission-rate and exposure–response figures deferred until HA data arrive."
), file.path(fig_dir, "README.md"))

message("Exploratory figures written to ", fig_dir)
