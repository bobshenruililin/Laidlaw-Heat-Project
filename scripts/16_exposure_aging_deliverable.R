#!/usr/bin/env Rscript
# 16_exposure_aging_deliverable.R
# Manuscript-ready figures and tables from REAL HKO + C&SD data only.
# No HA outcomes. No placeholder pollution inference.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c(
  "yaml", "dplyr", "tidyr", "readr", "ggplot2", "scales", "lubridate"
))

fig_dir <- file.path(root, "figures", "exposure_aging")
tab_dir <- file.path(root, "outputs", "tables", "exposure_aging")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)

theme_report <- function(base_size = 11) {
  theme_bw(base_size = base_size) %+replace%
    theme(
      plot.title = element_text(face = "bold", hjust = 0, margin = margin(b = 6)),
      plot.subtitle = element_text(colour = "grey30", hjust = 0, margin = margin(b = 8)),
      plot.caption = element_text(colour = "grey40", hjust = 0, size = rel(0.8),
                                 margin = margin(t = 8)),
      panel.grid.minor = element_blank(),
      strip.background = element_rect(fill = "grey95", colour = NA),
      legend.position = "bottom"
    )
}

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
climate <- readr::read_csv(
  file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
  show_col_types = FALSE
) |>
  dplyr::mutate(month_date = as.Date(month_date))

stopifnot(nrow(climate) == 132L)
stopifnot(all(climate$station == "HKO"))

annual_pop <- readr::read_csv(
  file.path(root, "data_raw", "csd_population",
            "csd_population_age_sex_annual_normalized.csv"),
  show_col_types = FALSE
)
stopifnot(all(annual_pop$source_table == "110-01001" |
                grepl("110-01001", annual_pop$source_table)))

# ---------------------------------------------------------------------------
# Table 1: Annual extremes + spell concentration
# ---------------------------------------------------------------------------
annual <- climate |>
  dplyr::group_by(year) |>
  dplyr::summarise(
    hot_nights = sum(hot_nights, na.rm = TRUE),
    very_hot_days = sum(very_hot_days, na.rm = TRUE),
    extremely_hot_days = sum(extremely_hot_days, na.rm = TRUE),
    cold_days = sum(cold_days, na.rm = TRUE),
    days_in_hn_spell_ge5 = sum(days_in_hot_night_spell_ge5, na.rm = TRUE),
    days_in_vhd_spell_ge5 = sum(days_in_very_hot_spell_ge5, na.rm = TRUE),
    months_with_2d3n = sum(month_has_2d3n_window == 1, na.rm = TRUE),
    mean_temp = mean(mean_temp, na.rm = TRUE),
    .groups = "drop"
  ) |>
  dplyr::mutate(
    share_hn_in_spell_ge5 = ifelse(
      hot_nights > 0,
      days_in_hn_spell_ge5 / hot_nights,
      NA_real_
    ),
    share_vhd_in_spell_ge5 = ifelse(
      very_hot_days > 0,
      days_in_vhd_spell_ge5 / very_hot_days,
      NA_real_
    )
  )

v <- validate_hko_annual_extremes(annual)
stopifnot(v$all_ok)

write_csv_safe(annual, file.path(tab_dir, "annual_extremes_and_spell_burden.csv"))

# Period contrast 2013-2018 vs 2019-2023
period_summary <- annual |>
  dplyr::mutate(period = ifelse(year <= 2018, "2013–2018", "2019–2023")) |>
  dplyr::group_by(period) |>
  dplyr::summarise(
    n_years = dplyr::n(),
    mean_hot_nights = mean(hot_nights),
    mean_very_hot_days = mean(very_hot_days),
    mean_cold_days = mean(cold_days),
    mean_share_hn_spell_ge5 = mean(share_hn_in_spell_ge5, na.rm = TRUE),
    mean_months_with_2d3n = mean(months_with_2d3n),
    .groups = "drop"
  )
write_csv_safe(period_summary, file.path(tab_dir, "period_contrast_2013_2018_vs_2019_2023.csv"))

# ---------------------------------------------------------------------------
# Table 2: Mid-year population aging (exact C&SD annual)
# ---------------------------------------------------------------------------
aging <- annual_pop |>
  dplyr::filter(year %in% c(2013L, 2023L)) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop") |>
  tidyr::pivot_wider(names_from = year, values_from = population,
                     names_prefix = "mid_") |>
  dplyr::mutate(
    abs_change = mid_2023 - mid_2013,
    pct_change = 100 * abs_change / mid_2013
  ) |>
  dplyr::arrange(match(age_group, c(
    "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
    "65-69", "70-74", "75-79", "80-84", "85+"
  )))

write_csv_safe(aging, file.path(tab_dir, "csd_midyear_aging_2013_vs_2023.csv"))

older <- aging |>
  dplyr::filter(age_group %in% c("65-69", "70-74", "75-79", "80-84", "85+"))
write_csv_safe(older, file.path(tab_dir, "csd_older_bands_2013_vs_2023.csv"))

# ---------------------------------------------------------------------------
# Figure A: Annual coexistence (reuse style of validated figure, single panel)
# ---------------------------------------------------------------------------
ann_long <- annual |>
  dplyr::select(year, hot_nights, very_hot_days, cold_days) |>
  tidyr::pivot_longer(-year, names_to = "metric", values_to = "days") |>
  dplyr::mutate(
    metric = factor(
      metric,
      levels = c("hot_nights", "very_hot_days", "cold_days"),
      labels = c(
        "Hot nights (Tmin ≥ 28°C)",
        "Very hot days (Tmax ≥ 33°C)",
        "Cold days (Tmin ≤ 12°C)"
      )
    )
  )

cols <- c(
  "Hot nights (Tmin ≥ 28°C)" = "#9C2C2C",
  "Very hot days (Tmax ≥ 33°C)" = "#C46A00",
  "Cold days (Tmin ≤ 12°C)" = "#2C6E9C"
)

p_annual <- ggplot(ann_long, aes(year, days, fill = metric)) +
  geom_col(width = 0.72) +
  facet_wrap(~metric, ncol = 1, scales = "free_y") +
  scale_fill_manual(values = cols, guide = "none") +
  scale_x_continuous(breaks = 2013:2023) +
  labs(
    title = "Official thermal extremes at HKO Headquarters, 2013–2023",
    subtitle = "Annual counts. Pipeline totals match HKO Year's Weather summaries (33/33).",
    x = NULL,
    y = "Days per year",
    caption = "Source: Hong Kong Observatory dailyExtract, Headquarters station. Environmental descriptors only — not health-outcome results."
  ) +
  theme_report()

ggsave(file.path(fig_dir, "fig01_annual_extremes_coexistence.pdf"),
       p_annual, width = 7.2, height = 7.0, device = cairo_pdf)
ggsave(file.path(fig_dir, "fig01_annual_extremes_coexistence.png"),
       p_annual, width = 7.2, height = 7.0, dpi = 300)

# ---------------------------------------------------------------------------
# Figure B: Monthly heat–cold coexistence (selected contrast)
# ---------------------------------------------------------------------------
clim_plot <- climate |>
  dplyr::mutate(
    period = ifelse(year <= 2018, "2013–2018", "2019–2023")
  )

p_monthly <- ggplot(clim_plot, aes(month_date)) +
  geom_col(aes(y = hot_nights), fill = "#9C2C2C", alpha = 0.75, width = 25) +
  geom_line(aes(y = cold_days), colour = "#2C6E9C", linewidth = 0.7) +
  facet_wrap(~period, ncol = 1, scales = "free_x") +
  scale_y_continuous(
    name = "Hot nights (bars)",
    sec.axis = sec_axis(~ ., name = "Cold days (line)")
  ) +
  labs(
    title = "Monthly hot nights and cold days, 2013–2023",
    subtitle = "Bars: hot nights. Line: cold days. Cold exposure persists alongside rising heat.",
    x = NULL,
    caption = "Source: HKO Headquarters. Dual axis uses identical day-count scale for visual comparison within each panel."
  ) +
  theme_report() +
  theme(axis.title.y.right = element_text(colour = "#2C6E9C"),
        axis.title.y.left = element_text(colour = "#9C2C2C"))

ggsave(file.path(fig_dir, "fig02_monthly_hot_nights_cold_days.pdf"),
       p_monthly, width = 7.4, height = 5.6, device = cairo_pdf)
ggsave(file.path(fig_dir, "fig02_monthly_hot_nights_cold_days.png"),
       p_monthly, width = 7.4, height = 5.6, dpi = 300)

# ---------------------------------------------------------------------------
# Figure C: Spell burden — share of hot nights in ≥5-night spells
# ---------------------------------------------------------------------------
spell_long <- annual |>
  dplyr::select(year, hot_nights, days_in_hn_spell_ge5, share_hn_in_spell_ge5)

p_spell <- ggplot(spell_long, aes(year, share_hn_in_spell_ge5)) +
  geom_col(fill = "#7A3E2E", width = 0.7, alpha = 0.9) +
  geom_hline(yintercept = mean(spell_long$share_hn_in_spell_ge5, na.rm = TRUE),
             linetype = "dashed", colour = "grey40") +
  scale_y_continuous(labels = scales::percent_format(accuracy = 1),
                     limits = c(0, 1), expand = c(0, 0.02)) +
  scale_x_continuous(breaks = 2013:2023) +
  labs(
    title = "Concentration of hot nights in multi-day spells (≥5 consecutive)",
    subtitle = "Share of annual hot nights that fall inside spells of five or more consecutive nights.",
    x = NULL,
    y = "Share of annual hot nights",
    caption = "Dashed line: 2013–2023 mean share. Inspired by Wang et al. (2019) spell-structure findings; descriptive only."
  ) +
  theme_report()

ggsave(file.path(fig_dir, "fig03_hot_night_spell_concentration.pdf"),
       p_spell, width = 7.2, height = 4.4, device = cairo_pdf)
ggsave(file.path(fig_dir, "fig03_hot_night_spell_concentration.png"),
       p_spell, width = 7.2, height = 4.4, dpi = 300)

# ---------------------------------------------------------------------------
# Figure D: Aging — mid-year population change in older bands
# ---------------------------------------------------------------------------
age_order <- c("35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
               "65-69", "70-74", "75-79", "80-84", "85+")
aging_plot <- aging |>
  dplyr::mutate(
    age_group = factor(age_group, levels = age_order),
    highlight = age_group %in% c("65-69", "70-74")
  )

p_aging <- ggplot(aging_plot, aes(age_group, pct_change, fill = highlight)) +
  geom_col(width = 0.75) +
  geom_hline(yintercept = 0, colour = "grey30") +
  scale_fill_manual(
    values = c("FALSE" = "grey70", "TRUE" = "#1F4E79"),
    labels = c("FALSE" = "Other ages 35+", "TRUE" = "65–69 and 70–74"),
    name = NULL
  ) +
  labs(
    title = "Mid-year population change by age group, Hong Kong 2013–2023",
    subtitle = "Percent change in C&SD mid-year population (Table 110-01001). Highlighted bands are intervention-relevant.",
    x = "Age group",
    y = "Percent change, mid-2013 to mid-2023",
    caption = "Source: Census and Statistics Department, Table 110-01001 (both sexes). Exact mid-year counts, not monthly interpolations."
  ) +
  theme_report() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

ggsave(file.path(fig_dir, "fig04_population_aging_pct_change.pdf"),
       p_aging, width = 7.4, height = 4.8, device = cairo_pdf)
ggsave(file.path(fig_dir, "fig04_population_aging_pct_change.png"),
       p_aging, width = 7.4, height = 4.8, dpi = 300)

# Absolute levels for 65-69 and 70-74 over time
older_ts <- annual_pop |>
  dplyr::filter(age_group %in% c("65-69", "70-74"),
                year >= 2013, year <= 2023) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop")

p_older_ts <- ggplot(older_ts, aes(year, population / 1000, colour = age_group)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_colour_manual(values = c("65-69" = "#1F4E79", "70-74" = "#5B8C5A"),
                      name = NULL) +
  scale_x_continuous(breaks = 2013:2023) +
  labs(
    title = "Growth in ages 65–69 and 70–74, mid-year 2013–2023",
    subtitle = "These cohorts nearly doubled and are practically reachable for heat–cold preparedness.",
    x = NULL,
    y = "Population (thousands)",
    caption = "Source: C&SD Table 110-01001, mid-year, both sexes."
  ) +
  theme_report()

ggsave(file.path(fig_dir, "fig05_older_cohorts_timeseries.pdf"),
       p_older_ts, width = 7.2, height = 4.2, device = cairo_pdf)
ggsave(file.path(fig_dir, "fig05_older_cohorts_timeseries.png"),
       p_older_ts, width = 7.2, height = 4.2, dpi = 300)

# ---------------------------------------------------------------------------
# Summary JSON-ish text for LaTeX authors
# ---------------------------------------------------------------------------
summary_lines <- c(
  sprintf("hko_validation: %d/%d MATCH", v$n_metric_checks_ok, v$n_metric_checks),
  sprintf("hot_nights_2013: %d", annual$hot_nights[annual$year == 2013]),
  sprintf("hot_nights_2021: %d", annual$hot_nights[annual$year == 2021]),
  sprintf("cold_days_2013: %d", annual$cold_days[annual$year == 2013]),
  sprintf("cold_days_2021: %d", annual$cold_days[annual$year == 2021]),
  sprintf("mean_hn_2013_2018: %.1f", period_summary$mean_hot_nights[1]),
  sprintf("mean_hn_2019_2023: %.1f", period_summary$mean_hot_nights[2]),
  sprintf("mean_cold_2013_2018: %.1f", period_summary$mean_cold_days[1]),
  sprintf("mean_cold_2019_2023: %.1f", period_summary$mean_cold_days[2]),
  sprintf("pop_65_69_2013: %.0f", aging$mid_2013[aging$age_group == "65-69"]),
  sprintf("pop_65_69_2023: %.0f", aging$mid_2023[aging$age_group == "65-69"]),
  sprintf("pct_65_69: %.1f", aging$pct_change[aging$age_group == "65-69"]),
  sprintf("pop_70_74_2013: %.0f", aging$mid_2013[aging$age_group == "70-74"]),
  sprintf("pop_70_74_2023: %.0f", aging$mid_2023[aging$age_group == "70-74"]),
  sprintf("pct_70_74: %.1f", aging$pct_change[aging$age_group == "70-74"]),
  sprintf("mean_spell_share: %.3f", mean(annual$share_hn_in_spell_ge5, na.rm = TRUE))
)
writeLines(summary_lines, file.path(tab_dir, "key_numbers.txt"))
message("Exposure–aging deliverable figures written to ", fig_dir)
message(paste(summary_lines, collapse = "\n"))
