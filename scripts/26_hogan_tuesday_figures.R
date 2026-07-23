#!/usr/bin/env Rscript
# Hogan Tuesday (28 Jul 2026): exposure-only figures for weather definition lock.
# No stroke outcomes. Credit: weather framing — Hogan; climate build — shared HKO.

source("scripts/utils.R")
root <- project_root()
setwd(root)
ensure_packages(c("ggplot2", "dplyr", "tidyr", "scales", "forcats"))

out_dir <- file.path(root, "figures", "hogan_tuesday")
tab_dir <- file.path(root, "outputs", "tables", "hogan_tuesday")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)

theme_ht <- function(base = 12) {
  ggplot2::theme_minimal(base_size = base) +
    ggplot2::theme(
      legend.position = "bottom",
      panel.grid.minor = ggplot2::element_blank(),
      plot.title = ggplot2::element_text(face = "bold", colour = "#1B2A41"),
      plot.subtitle = ggplot2::element_text(colour = "#3D6B6E"),
      plot.caption = ggplot2::element_text(colour = "#6B7C8A", size = 8, hjust = 0)
    )
}

clim <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                        stringsAsFactors = FALSE)
exp <- utils::read.csv(file.path(root, "data_processed", "exposures_monthly_2013_2023.csv"),
                       stringsAsFactors = FALSE)

# --- Starter-definition prevalence (exposure-only proxies already in panel) ---
# Map available columns to named starters / near-starters for Tuesday discussion.
flags <- exp |>
  dplyr::transmute(
    month_id,
    year,
    month,
    `HM08 mean T ≥ p90` = as.integer(hw_month_mean_temp_ge_p90 == 1),
    `HM15 VHD spell ≥5d touch` = as.integer(days_in_very_hot_spell_ge5 > 0),
    `HM17 HN spell ≥5d touch` = as.integer(days_in_hot_night_spell_ge5 > 0),
    `HM19 2D3N touch` = as.integer(month_has_2d3n_window == 1),
    `CM03 cold days ≥5` = as.integer(cold_days >= 5),
    `CM08 mean T ≤ p05` = as.integer(cold_month_mean_temp_le_p05 == 1),
    `CM15 cold spell ≥3d touch` = as.integer(max_cold_spell_touching >= 3),
    `CM05 any ≤10°C (approx)` = as.integer(cold_days >= 1 & mean_tmin <= 12) # placeholder note: true CD10 needs daily rebuild
  )

# Honest note: CM05 true Tmin≤10 needs daily extract; use CD12 count + note in caption.
# Replace CM05 with official CD12 ≥1 as discussable absolute cold until daily CD10 built.
flags$`CM05 any ≤10°C (approx)` <- NULL
flags$`CM01 any cold day ≤12°C` <- as.integer(exp$cold_days >= 1)

long <- flags |>
  tidyr::pivot_longer(-c(month_id, year, month), names_to = "definition", values_to = "flag")

prev <- long |>
  dplyr::group_by(definition) |>
  dplyr::summarise(
    months_flagged = sum(flag, na.rm = TRUE),
    n_months = dplyr::n(),
    prevalence = months_flagged / n_months,
    .groups = "drop"
  ) |>
  dplyr::mutate(definition = forcats::fct_reorder(definition, months_flagged))

utils::write.csv(prev, file.path(tab_dir, "starter_definition_prevalence.csv"), row.names = FALSE)

p_prev <- ggplot2::ggplot(prev, ggplot2::aes(months_flagged, definition)) +
  ggplot2::geom_col(fill = "#3D6B6E", width = 0.72) +
  ggplot2::geom_text(ggplot2::aes(label = months_flagged), hjust = -0.15, size = 3.3, colour = "#1B2A41") +
  ggplot2::scale_x_continuous(limits = c(0, max(prev$months_flagged) * 1.12), expand = c(0, 0)) +
  ggplot2::labs(
    title = "How often do candidate hot/cold months fire?",
    subtitle = "Exposure-only prevalence across 132 months (2013–2023)",
    x = "Months flagged", y = NULL,
    caption = "HM23 (Hogan Li-HW count→tail) needs daily calendar-day p90 construction — lock with Hogan Tuesday.\nThresholds frozen without stroke outcomes. CM05 (Tmin≤10) requires a daily rebuild; CM01 shown as absolute cold proxy."
  ) +
  theme_ht()
ggplot2::ggsave(file.path(out_dir, "fig_starter_prevalence.pdf"), p_prev, width = 9.4, height = 5.2)
ggplot2::ggsave(file.path(out_dir, "fig_starter_prevalence.png"), p_prev, width = 9.4, height = 5.2, dpi = 170)

# --- Annual extremes coexistence (meeting-ready) ---
ann <- clim |>
  dplyr::group_by(year) |>
  dplyr::summarise(
    hot_nights = sum(hot_nights, na.rm = TRUE),
    very_hot_days = sum(very_hot_days, na.rm = TRUE),
    cold_days = sum(cold_days, na.rm = TRUE),
    months_2d3n = sum(month_has_2d3n_window == 1, na.rm = TRUE),
    .groups = "drop"
  )
utils::write.csv(ann, file.path(tab_dir, "annual_extremes_and_2d3n.csv"), row.names = FALSE)

ann_long <- ann |>
  tidyr::pivot_longer(-year, names_to = "metric", values_to = "value") |>
  dplyr::mutate(
    metric = factor(
      metric,
      levels = c("hot_nights", "very_hot_days", "cold_days", "months_2d3n"),
      labels = c("Hot nights (days)", "Very hot days", "Cold days (≤12°C)", "Months with 2D3N")
    )
  )

p_ann <- ggplot2::ggplot(ann_long, ggplot2::aes(year, value, colour = metric)) +
  ggplot2::geom_line(linewidth = 1.05) +
  ggplot2::geom_point(size = 2) +
  ggplot2::scale_colour_manual(values = c("#A85A3A", "#C4873A", "#3D6B6E", "#1B2A41")) +
  ggplot2::scale_x_continuous(breaks = seq(2013, 2023, 2)) +
  ggplot2::labs(
    title = "Heat rose; cold did not vanish",
    subtitle = "HKO Headquarters extremes + Wang/Ren-style 2D3N months, 2013–2023",
    x = NULL, y = "Count", colour = NULL,
    caption = "Environmental descriptives only. Weather definitions to be locked with Hogan."
  ) +
  theme_ht()
ggplot2::ggsave(file.path(out_dir, "fig_annual_coexistence.pdf"), p_ann, width = 9.4, height = 4.8)
ggplot2::ggsave(file.path(out_dir, "fig_annual_coexistence.png"), p_ann, width = 9.4, height = 4.8, dpi = 170)

# --- Monthly mean temperature with p90 / p05 lines (HM08 / CM08 intuition) ---
p90 <- unique(stats::na.omit(exp$hw_p90_threshold_c))[1]
p05 <- unique(stats::na.omit(exp$cold_p05_threshold_c))[1]
ts <- exp |>
  dplyr::mutate(date = as.Date(paste0(month_id, "-01")))

p_ts <- ggplot2::ggplot(ts, ggplot2::aes(date, mean_temp)) +
  ggplot2::geom_ribbon(ggplot2::aes(ymin = mean_tmin, ymax = mean_tmax), fill = "#E8EAED", alpha = 0.9) +
  ggplot2::geom_line(colour = "#1B2A41", linewidth = 0.7) +
  ggplot2::geom_hline(yintercept = p90, colour = "#A85A3A", linetype = "dashed", linewidth = 0.7) +
  ggplot2::geom_hline(yintercept = p05, colour = "#3D6B6E", linetype = "dashed", linewidth = 0.7) +
  ggplot2::annotate("text", x = min(ts$date), y = p90, label = sprintf("HM08 p90 ≈ %.1f°C", p90),
                    hjust = 0, vjust = -0.4, size = 3, colour = "#A85A3A") +
  ggplot2::annotate("text", x = min(ts$date), y = p05, label = sprintf("CM08 p05 ≈ %.1f°C", p05),
                    hjust = 0, vjust = 1.3, size = 3, colour = "#3D6B6E") +
  ggplot2::scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  ggplot2::labs(
    title = "Monthly mean temperature and relative tails",
    subtitle = "Ribbon = mean Tmin–Tmax; dashed lines = study-period monthly p90 / p05",
    x = NULL, y = "°C",
    caption = "Reference-period freeze is a Tuesday decision with Hogan (2013–2019 vs full window)."
  ) +
  theme_ht()
ggplot2::ggsave(file.path(out_dir, "fig_monthly_temp_tails.pdf"), p_ts, width = 9.4, height = 4.8)
ggplot2::ggsave(file.path(out_dir, "fig_monthly_temp_tails.png"), p_ts, width = 9.4, height = 4.8, dpi = 170)

# --- Definition-family comparison: months flagged by family ---
fam <- data.frame(
  family = c(
    "Official HKO day counts\n(HN / VHD / CD)",
    "Wang/Ren spells & 2D3N\n(HM15 / HM17 / HM19)",
    "Relative monthly tails\n(HM08 / CM08)",
    "Hogan Li-HW count→tail\n(HM23)",
    "Roro HWD_* mortality defs\n(as monthly siblings)"
  ),
  status = c("Ready to discuss", "Ready to discuss", "Ready to discuss",
             "Needs Hogan lock", "Name as siblings?"),
  months_example = c(
    sum(exp$hot_nights >= 1 | exp$very_hot_days >= 1 | exp$cold_days >= 1),
    sum(exp$days_in_very_hot_spell_ge5 > 0 | exp$days_in_hot_night_spell_ge5 > 0 | exp$month_has_2d3n_window == 1),
    sum(exp$hw_month_mean_temp_ge_p90 == 1 | exp$cold_month_mean_temp_le_p05 == 1),
    NA_integer_,
    NA_integer_
  ),
  stringsAsFactors = FALSE
)
utils::write.csv(fam, file.path(tab_dir, "definition_family_status.csv"), row.names = FALSE)

fam$family <- factor(fam$family, levels = rev(fam$family))
p_fam <- ggplot2::ggplot(fam, ggplot2::aes(family, fill = status)) +
  ggplot2::geom_bar(ggplot2::aes(y = 1), stat = "identity", width = 0.65) +
  ggplot2::coord_flip() +
  ggplot2::scale_fill_manual(values = c(
    "Ready to discuss" = "#3D6B6E",
    "Needs Hogan lock" = "#A85A3A",
    "Name as siblings?" = "#C4873A"
  )) +
  ggplot2::labs(
    title = "Definition families on Tuesday’s table",
    subtitle = "None replace each other — Hogan chooses which to freeze as co-primary",
    x = NULL, y = NULL, fill = NULL,
    caption = "HM23 and exact Roro monthly transport still need parameter freeze with Hogan."
  ) +
  theme_ht() +
  ggplot2::theme(axis.text.x = ggplot2::element_blank(), panel.grid = ggplot2::element_blank())
ggplot2::ggsave(file.path(out_dir, "fig_definition_families.pdf"), p_fam, width = 9.0, height = 4.4)
ggplot2::ggsave(file.path(out_dir, "fig_definition_families.png"), p_fam, width = 9.0, height = 4.4, dpi = 170)

message("Hogan Tuesday figures written to ", out_dir)
