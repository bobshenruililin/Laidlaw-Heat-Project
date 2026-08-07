#!/usr/bin/env Rscript
# 27_cvd_descriptives_real.R
# Descriptive tables/figures for REAL CHD and HF monthly first-hospitalisation aggregates.
# Provenance: HA_APPROVED_AGGREGATE. Does NOT dump full month-level HA count tables to markdown.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "tidyr", "ggplot2"))

outcomes <- c("chd", "hf")
tab_dir <- file.path(root, "outputs", "tables")
fig_dir <- file.path(root, "outputs", "figures", "descriptives")
dir.create(tab_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

load_panel <- function(outcome) {
  path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  if (!file.exists(path)) stop("Missing ", path)
  d <- utils::read.csv(path, stringsAsFactors = FALSE)
  stop_if_synthetic(d)
  if (!all(d$data_status == "HA_APPROVED_AGGREGATE")) {
    stop(outcome, " panel is not uniformly HA_APPROVED_AGGREGATE")
  }
  d$month_date <- as.Date(paste0(d$month_id, "-01"))
  d$outcome <- outcome
  d
}

panels <- lapply(outcomes, load_panel)
names(panels) <- outcomes
all_df <- dplyr::bind_rows(panels)

# --- Annual totals (safe summary; not month-level dump) ---
annual <- all_df |>
  dplyr::group_by(outcome, year, data_status) |>
  dplyr::summarise(
    n_months = dplyr::n(),
    total_events = sum(n_events, na.rm = TRUE),
    mean_monthly_events = mean(n_events, na.rm = TRUE),
    sd_monthly_events = sd(n_events, na.rm = TRUE),
    mean_population = mean(population, na.rm = TRUE),
    crude_rate_per_100k_person_years =
      sum(n_events, na.rm = TRUE) /
        sum(population * days_in_month, na.rm = TRUE) * 365.25 * 1e5,
    .groups = "drop"
  )
write_csv_safe(annual, file.path(tab_dir, "cvd_descriptive_annual_totals.csv"))

# --- Seasonality by month-of-year ---
season <- all_df |>
  dplyr::group_by(outcome, month, data_status) |>
  dplyr::summarise(
    n_years = dplyr::n(),
    mean_events = mean(n_events, na.rm = TRUE),
    sd_events = sd(n_events, na.rm = TRUE),
    mean_temp = mean(mean_temp, na.rm = TRUE),
    mean_tmax = mean(mean_tmax, na.rm = TRUE),
    mean_tmin = mean(mean_tmin, na.rm = TRUE),
    .groups = "drop"
  )
write_csv_safe(season, file.path(tab_dir, "cvd_descriptive_seasonality_by_month.csv"))

# --- COVID-era means ---
covid_means <- all_df |>
  dplyr::mutate(
    period = dplyr::case_when(
      year < 2020 ~ "pre_covid_2013_2019",
      year <= 2022 ~ "covid_2020_2022",
      TRUE ~ "post_reopening_2023"
    )
  ) |>
  dplyr::group_by(outcome, period, data_status) |>
  dplyr::summarise(
    n_months = dplyr::n(),
    mean_events = mean(n_events, na.rm = TRUE),
    sd_events = sd(n_events, na.rm = TRUE),
    mean_temp = mean(mean_temp, na.rm = TRUE),
    mean_tmax = mean(mean_tmax, na.rm = TRUE),
    mean_tmin = mean(mean_tmin, na.rm = TRUE),
    mean_hot_nights = mean(hot_nights, na.rm = TRUE),
    mean_cold_days = mean(cold_days, na.rm = TRUE),
    mean_very_hot_days = mean(very_hot_days, na.rm = TRUE),
    crude_rate_per_100k_person_years =
      sum(n_events, na.rm = TRUE) /
        sum(population * days_in_month, na.rm = TRUE) * 365.25 * 1e5,
    .groups = "drop"
  )
write_csv_safe(covid_means, file.path(tab_dir, "cvd_descriptive_covid_era_means.csv"))

# --- Correlations with temperature (Pearson; monthly series) ---
cor_rows <- list()
for (o in outcomes) {
  d <- panels[[o]]
  for (ex in c("mean_temp", "mean_tmax", "mean_tmin")) {
    ct <- suppressWarnings(cor.test(d$n_events, d[[ex]], use = "pairwise.complete.obs"))
    cor_rows[[paste(o, ex)]] <- data.frame(
      outcome = o,
      exposure = ex,
      pearson_r = unname(ct$estimate),
      p_value = ct$p.value,
      n_months = sum(complete.cases(d$n_events, d[[ex]])),
      data_status = "HA_APPROVED_AGGREGATE",
      stringsAsFactors = FALSE
    )
  }
}
cors <- dplyr::bind_rows(cor_rows)
write_csv_safe(cors, file.path(tab_dir, "cvd_descriptive_temp_correlations.csv"))

# --- Overall snapshot (one row per outcome; no month dump) ---
snapshot <- all_df |>
  dplyr::group_by(outcome, data_status, cohort = dplyr::first(cohort),
                  event_definition = dplyr::first(event_definition),
                  denominator_note = dplyr::first(denominator_note)) |>
  dplyr::summarise(
    n_months = dplyr::n(),
    year_start = min(year),
    year_end = max(year),
    total_events = sum(n_events, na.rm = TRUE),
    mean_monthly = mean(n_events, na.rm = TRUE),
    min_monthly = min(n_events, na.rm = TRUE),
    max_monthly = max(n_events, na.rm = TRUE),
    .groups = "drop"
  )
write_csv_safe(snapshot, file.path(tab_dir, "cvd_descriptive_snapshot.csv"))

# --- Figures ---
theme_set(ggplot2::theme_bw(base_size = 11))

# Monthly time series (figure OK; not a markdown dump of counts)
p_ts <- ggplot2::ggplot(all_df, ggplot2::aes(x = month_date, y = n_events, colour = outcome)) +
  ggplot2::geom_line(linewidth = 0.7) +
  ggplot2::facet_wrap(~ outcome, ncol = 1, scales = "free_y") +
  ggplot2::scale_colour_manual(values = c(chd = "#0b3d4a", hf = "#8b3a3a"), guide = "none") +
  ggplot2::labs(
    title = "Monthly first-hospitalisation counts (HA_APPROVED_AGGREGATE)",
    subtitle = "CHD and HF among T2D/HTN cohort; ecological C&SD 35+ denominator (not cohort at-risk)",
    x = NULL, y = "Monthly events"
  )
ggplot2::ggsave(file.path(fig_dir, "cvd_monthly_timeseries.png"), p_ts, width = 10, height = 6, dpi = 150)

# Seasonality
p_season <- ggplot2::ggplot(season, ggplot2::aes(x = month, y = mean_events, colour = outcome)) +
  ggplot2::geom_line(linewidth = 0.8) +
  ggplot2::geom_point(size = 2) +
  ggplot2::scale_x_continuous(breaks = 1:12) +
  ggplot2::scale_colour_manual(values = c(chd = "#0b3d4a", hf = "#8b3a3a")) +
  ggplot2::labs(
    title = "Seasonality: mean monthly events by month-of-year",
    subtitle = "HA_APPROVED_AGGREGATE; 2013-2023",
    x = "Month", y = "Mean events", colour = "Outcome"
  )
ggplot2::ggsave(file.path(fig_dir, "cvd_seasonality_by_month.png"), p_season, width = 8, height = 4.5, dpi = 150)

# Annual totals
p_ann <- ggplot2::ggplot(annual, ggplot2::aes(x = year, y = total_events, fill = outcome)) +
  ggplot2::geom_col(position = "dodge", width = 0.7) +
  ggplot2::scale_fill_manual(values = c(chd = "#0b3d4a", hf = "#8b3a3a")) +
  ggplot2::labs(
    title = "Annual first-hospitalisation totals",
    subtitle = "HA_APPROVED_AGGREGATE; CHD vs HF",
    x = NULL, y = "Annual events", fill = "Outcome"
  )
ggplot2::ggsave(file.path(fig_dir, "cvd_annual_totals.png"), p_ann, width = 9, height = 4.5, dpi = 150)

# Event vs mean temperature scatter
p_sc <- ggplot2::ggplot(all_df, ggplot2::aes(x = mean_temp, y = n_events, colour = outcome)) +
  ggplot2::geom_point(alpha = 0.55, size = 1.6) +
  ggplot2::geom_smooth(method = "lm", se = TRUE, linewidth = 0.7) +
  ggplot2::facet_wrap(~ outcome, scales = "free_y") +
  ggplot2::scale_colour_manual(values = c(chd = "#0b3d4a", hf = "#8b3a3a"), guide = "none") +
  ggplot2::labs(
    title = "Monthly events vs mean temperature",
    subtitle = "HA_APPROVED_AGGREGATE; descriptive only (not model IRRs)",
    x = "Mean temperature (C)", y = "Monthly events"
  )
ggplot2::ggsave(file.path(fig_dir, "cvd_events_vs_mean_temp.png"), p_sc, width = 9, height = 5, dpi = 150)

# Short note (summaries only — no month-by-month HA counts)
note_path <- file.path(root, "outputs", "reports", "cvd_descriptives_note.md")
dir.create(dirname(note_path), recursive = TRUE, showWarnings = FALSE)
lines <- c(
  "# CVD descriptives note (CHD / HF)",
  "",
  paste0("- Run at: ", as.character(Sys.time())),
  "- Provenance: **HA_APPROVED_AGGREGATE**",
  "- Stroke file: not delivered (excluded).",
  "- Denominator caveat: C&SD population 35+ is ecological person-time, **not** T2D/HTN cohort at-risk.",
  "- Month-level HA count tables are **not** printed here (summaries and figures only).",
  "",
  "## Snapshot",
  "",
  paste0(
    "| Outcome | Months | Years | Total events | Mean monthly |",
    ""
  ),
  "|---|---:|---|---:|---:|",
  paste0(
    "| ", snapshot$outcome, " | ", snapshot$n_months, " | ",
    snapshot$year_start, "-", snapshot$year_end, " | ",
    snapshot$total_events, " | ", round(snapshot$mean_monthly, 1), " |"
  ),
  "",
  "## Temperature correlations (events vs exposure)",
  "",
  "| Outcome | Exposure | Pearson r | p |",
  "|---|---|---:|---:|",
  paste0(
    "| ", cors$outcome, " | ", cors$exposure, " | ",
    sprintf("%.3f", cors$pearson_r), " | ", signif(cors$p_value, 3), " |"
  ),
  "",
  "## Outputs",
  "",
  "- `outputs/tables/cvd_descriptive_*.csv`",
  "- `outputs/figures/descriptives/cvd_*.png`",
  "",
  "Gate 3 remains open; descriptives are not primary manuscript claims."
)
writeLines(lines, note_path)
message("Descriptives written to ", tab_dir, " and ", fig_dir)
