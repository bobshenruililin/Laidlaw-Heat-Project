#!/usr/bin/env Rscript
# 33_cvd_publication_artifacts.R
# Disclosure-minimised manuscript tables, claim ledger and journal figures.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "tidyr", "ggplot2", "scales", "svglite"))

tables_dir <- file.path(root, "outputs", "tables")
figures_dir <- file.path(root, "outputs", "figures")
release_dir <- file.path(root, "outputs", "release_chd_hf")
release_tables <- file.path(release_dir, "tables")
release_figures <- file.path(release_dir, "figures")
release_supp <- file.path(release_dir, "supplement")

if (dir.exists(release_dir)) unlink(release_dir, recursive = TRUE)
dir.create(release_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(release_figures, recursive = TRUE, showWarnings = FALSE)
dir.create(release_supp, recursive = TRUE, showWarnings = FALSE)

read_required <- function(name) {
  path <- file.path(tables_dir, name)
  if (!file.exists(path)) stop("Missing required publication input: ", path)
  utils::read.csv(path, stringsAsFactors = FALSE)
}

core <- read_required("cvd_core_robust_estimates.csv")
trend <- read_required("cvd_trend_depletion_sensitivity.csv")
lag <- read_required("cvd_lag_sensitivity.csv")
influence <- read_required("cvd_influence_sensitivity.csv")
correlations <- read_required("cvd_exposure_correlations.csv")
vif <- read_required("cvd_exposure_vif.csv")
descriptive <- read_required("cvd_descriptive_snapshot.csv")

if (any(grepl("SYNTHETIC", core$data_status, ignore.case = TRUE)) ||
    any(core$data_status != "HA_APPROVED_AGGREGATE")) {
  stop("Publication artifacts require HA_APPROVED_AGGREGATE only")
}

labels <- c(
  P01A = "Mean temperature, per 1 C",
  P02A = "Mean maximum temperature, per 1 C",
  P02B = "Mean minimum temperature, per 1 C",
  P04A = "Hot nights, per 5 days",
  P04B = "Cold days, per 5 days",
  P04C = "Very hot days, per 5 days"
)
outcome_labels <- c(chd = "Coronary heart disease", hf = "Heart failure")

main <- core |>
  dplyr::filter(
    family == "negative_binomial",
    offset_policy == "days_only",
    se_method == "NeweyWest_lag6"
  ) |>
  dplyr::mutate(
    outcome_label = unname(outcome_labels[outcome]),
    exposure_label = unname(labels[pathway_id]),
    contrast = exposure_label,
    count_ratio_95CI = sprintf("%.3f (%.3f–%.3f)", rr, rr_low, rr_high),
    analysis_status = "Exploratory robustness amendment; team freeze pending"
  ) |>
  dplyr::select(
    outcome,
    outcome_label,
    pathway_id,
    exposure,
    contrast,
    rr,
    rr_low,
    rr_high,
    count_ratio_95CI,
    p_value,
    q_value_core_bh,
    n_months,
    family,
    offset_policy,
    se_method,
    data_status,
    analysis_status
  )
if (nrow(main) != 12L) stop("Expected 12 core outcome-exposure rows; found ", nrow(main))

table1 <- descriptive |>
  dplyr::mutate(
    outcome_label = unname(outcome_labels[outcome]),
    period = paste0(year_start, "–", year_end),
    monthly_mean_rounded = round(mean_monthly, 1)
  ) |>
  dplyr::select(
    outcome,
    outcome_label,
    period,
    n_months,
    total_events,
    monthly_mean_rounded,
    cohort,
    event_definition,
    data_status
  )

trend_range <- trend |>
  dplyr::group_by(outcome, pathway_id, exposure) |>
  dplyr::summarise(
    trend_depletion_rr_min = min(rr, na.rm = TRUE),
    trend_depletion_rr_max = max(rr, na.rm = TRUE),
    scenarios_fitted = dplyr::n(),
    .groups = "drop"
  )
offset_range <- core |>
  dplyr::filter(family == "negative_binomial", se_method == "NeweyWest_lag6") |>
  dplyr::group_by(outcome, pathway_id, exposure) |>
  dplyr::summarise(
    offset_rr_min = min(rr, na.rm = TRUE),
    offset_rr_max = max(rr, na.rm = TRUE),
    offsets_fitted = dplyr::n_distinct(offset_policy),
    .groups = "drop"
  )
lag_range <- lag |>
  dplyr::group_by(outcome, pathway_id, exposure) |>
  dplyr::summarise(
    lag_rr_min = min(rr, na.rm = TRUE),
    lag_rr_max = max(rr, na.rm = TRUE),
    lags_fitted = dplyr::n_distinct(lag_months),
    .groups = "drop"
  )
influence_one <- influence |>
  dplyr::select(
    outcome,
    pathway_id,
    influence_rr = rr,
    excluded_month,
    max_cooks_distance
  )
table3 <- main |>
  dplyr::select(outcome, outcome_label, pathway_id, contrast, baseline_rr = rr) |>
  dplyr::left_join(trend_range, by = c("outcome", "pathway_id")) |>
  dplyr::left_join(offset_range, by = c("outcome", "pathway_id")) |>
  dplyr::left_join(lag_range, by = c("outcome", "pathway_id")) |>
  dplyr::left_join(influence_one, by = c("outcome", "pathway_id"))

claim_ledger <- main |>
  dplyr::mutate(
    claim_id = sprintf("CVD-%02d", dplyr::row_number()),
    claim_text = paste0(
      outcome_label, ": ", contrast, "; count ratio ",
      sprintf("%.3f", rr), " (95% CI ", sprintf("%.3f", rr_low), "–",
      sprintf("%.3f", rr_high), ")."
    ),
    provenance = "HA_APPROVED_AGGREGATE",
    source_table = "outputs/release_chd_hf/tables/table2_core_models.csv",
    manuscript_role = "complete-panel result; not designated primary"
  ) |>
  dplyr::select(
    claim_id,
    claim_text,
    outcome,
    pathway_id,
    contrast,
    rr,
    rr_low,
    rr_high,
    p_value,
    q_value_core_bh,
    n_months,
    family,
    offset_policy,
    se_method,
    provenance,
    manuscript_role,
    source_table
  )

write_csv_safe(table1, file.path(release_tables, "table1_outcome_summary.csv"))
write_csv_safe(main, file.path(release_tables, "table2_core_models.csv"))
write_csv_safe(table3, file.path(release_tables, "table3_robustness_summary.csv"))
write_csv_safe(claim_ledger, file.path(release_tables, "claim_ledger.csv"))

copy_supp <- c(
  "combined_pathway_panel_estimates.csv",
  "chd_hm_cm_panel_estimates.csv",
  "hf_hm_cm_panel_estimates.csv",
  "hm_cm_selected_months_audit.csv",
  "cvd_core_robust_estimates.csv",
  "cvd_single_vs_joint_estimates.csv",
  "cvd_core_model_fit.csv",
  "cvd_exposure_correlations.csv",
  "cvd_exposure_vif.csv",
  "cvd_trend_depletion_sensitivity.csv",
  "cvd_lag_sensitivity.csv",
  "cvd_influence_sensitivity.csv",
  "cvd_count_timeseries_sensitivity.csv",
  "chd_pathway_core_diagnostics.csv",
  "hf_pathway_core_diagnostics.csv",
  "chd_pathway_residual_acf.csv",
  "hf_pathway_residual_acf.csv"
)
for (name in copy_supp) {
  src <- file.path(tables_dir, name)
  if (file.exists(src)) file.copy(src, file.path(release_supp, name), overwrite = TRUE)
}

theme_pub <- function() {
  ggplot2::theme_minimal(base_size = 11) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(face = "bold", size = 12),
      plot.subtitle = ggplot2::element_text(colour = "grey30"),
      panel.grid.minor = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(face = "bold"),
      legend.position = "bottom"
    )
}

save_plot <- function(plot, stem, width, height) {
  ggplot2::ggsave(
    file.path(release_figures, paste0(stem, ".png")),
    plot,
    width = width,
    height = height,
    dpi = 400
  )
  ggplot2::ggsave(
    file.path(release_figures, paste0(stem, ".pdf")),
    plot,
    width = width,
    height = height
  )
  ggplot2::ggsave(
    file.path(release_figures, paste0(stem, ".svg")),
    plot,
    width = width,
    height = height
  )
}

# Figure 1 — indexed first-hospitalisation series (no monthly raw count labels).
panel_list <- lapply(c("chd", "hf"), function(outcome) {
  path <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
  d <- utils::read.csv(path, stringsAsFactors = FALSE) |>
    dplyr::arrange(time_index)
  reference <- mean(d$n_events[d$year == 2013], na.rm = TRUE)
  d$index_2013_mean_100 <- 100 * d$n_events / reference
  d$rolling_12_month <- as.numeric(
    stats::filter(d$index_2013_mean_100, rep(1 / 12, 12), sides = 1)
  )
  d$outcome <- outcome
  d$outcome_label <- unname(outcome_labels[outcome])
  d
})
indexed <- dplyr::bind_rows(panel_list)
p1 <- ggplot2::ggplot(indexed, ggplot2::aes(month_date, index_2013_mean_100)) +
  ggplot2::geom_line(colour = "#8aa5aa", linewidth = 0.45) +
  ggplot2::geom_line(ggplot2::aes(y = rolling_12_month), colour = "#174d5b", linewidth = 0.9, na.rm = TRUE) +
  ggplot2::facet_wrap(~outcome_label, ncol = 1, scales = "free_y") +
  ggplot2::labs(
    title = "Monthly first-hospitalisation counts declined over the study period",
    subtitle = "Index: each outcome's 2013 monthly mean = 100; dark line is a trailing 12-month mean",
    x = NULL,
    y = "Indexed monthly count"
  ) +
  theme_pub()
save_plot(p1, "figure1_indexed_outcome_series", 8.5, 6.5)

# Figure 2 — seasonal profile on an outcome-specific index.
seasonal <- indexed |>
  dplyr::group_by(outcome, outcome_label, month) |>
  dplyr::summarise(
    mean_index = mean(index_2013_mean_100),
    se_index = stats::sd(index_2013_mean_100) / sqrt(dplyr::n()),
    .groups = "drop"
  )
p2 <- ggplot2::ggplot(
  seasonal,
  ggplot2::aes(month, mean_index, colour = outcome_label, group = outcome_label)
) +
  ggplot2::geom_hline(yintercept = 100, linetype = "dotted", colour = "grey60") +
  ggplot2::geom_ribbon(
    ggplot2::aes(ymin = mean_index - 1.96 * se_index, ymax = mean_index + 1.96 * se_index, fill = outcome_label),
    alpha = 0.12,
    colour = NA
  ) +
  ggplot2::geom_line(linewidth = 0.9) +
  ggplot2::geom_point(size = 1.8) +
  ggplot2::scale_x_continuous(breaks = 1:12, labels = month.abb) +
  ggplot2::scale_colour_manual(values = c("Coronary heart disease" = "#bd5a32", "Heart failure" = "#276b79")) +
  ggplot2::scale_fill_manual(values = c("Coronary heart disease" = "#bd5a32", "Heart failure" = "#276b79")) +
  ggplot2::labs(
    title = "Seasonal pattern in first-hospitalisation counts",
    subtitle = "Outcome-specific indexed mean with 95% confidence bands across study years",
    x = NULL,
    y = "Indexed monthly count",
    colour = NULL,
    fill = NULL
  ) +
  theme_pub()
save_plot(p2, "figure2_seasonal_pattern", 8.5, 5.2)

# Figure 3 — amended core forest, reader labels only.
main_plot <- main |>
  dplyr::mutate(
    exposure_label = factor(exposure_label, levels = rev(unname(labels))),
    outcome_label = factor(outcome_label, levels = unname(outcome_labels))
  )
p3 <- ggplot2::ggplot(
  main_plot,
  ggplot2::aes(rr, exposure_label, xmin = rr_low, xmax = rr_high, colour = outcome_label)
) +
  ggplot2::geom_vline(xintercept = 1, linetype = "dashed", colour = "grey45") +
  ggplot2::geom_errorbarh(height = 0.16, position = ggplot2::position_dodge(width = 0.45)) +
  ggplot2::geom_point(size = 2.1, position = ggplot2::position_dodge(width = 0.45)) +
  ggplot2::scale_x_log10() +
  ggplot2::scale_colour_manual(values = c("Coronary heart disease" = "#bd5a32", "Heart failure" = "#276b79")) +
  ggplot2::labs(
    title = "Core single-exposure monthly models",
    subtitle = "Negative-binomial count ratios; days-in-month offset; Newey–West lag-6 95% CI",
    x = "Count ratio (log scale)",
    y = NULL,
    colour = NULL
  ) +
  theme_pub()
save_plot(p3, "figure3_core_forest", 9.2, 5.8)

# Figure 4 — trend/depletion robustness.
trend_plot <- trend |>
  dplyr::mutate(
    outcome_label = unname(outcome_labels[outcome]),
    exposure_label = unname(labels[pathway_id]),
    scenario_label = dplyr::recode(
      scenario,
      baseline_ns4 = "Baseline: spline df 4",
      trend_ns3 = "Spline df 3",
      trend_ns6 = "Spline df 6",
      trend_ns8 = "Spline df 8",
      year_fixed_effects = "Year fixed effects",
      drop_first_12_months = "Drop first 12 months",
      drop_first_24_months = "Drop first 24 months",
      pre_covid = "Pre-COVID",
      covid_phase_adjusted = "COVID-phase adjusted"
    )
  )
p4 <- ggplot2::ggplot(
  trend_plot,
  ggplot2::aes(rr, scenario_label, xmin = rr_low, xmax = rr_high)
) +
  ggplot2::geom_vline(xintercept = 1, linetype = "dashed", colour = "grey55") +
  ggplot2::geom_errorbarh(height = 0.12, colour = "#376d78") +
  ggplot2::geom_point(colour = "#174d5b", size = 1.4) +
  ggplot2::facet_grid(outcome_label ~ exposure_label, scales = "free_x") +
  ggplot2::labs(
    title = "Core estimates across trend and first-event sensitivities",
    subtitle = "Newey–West lag-6 intervals; all models use a days-in-month offset",
    x = "Count ratio",
    y = NULL
  ) +
  theme_pub() +
  ggplot2::theme(axis.text.y = ggplot2::element_text(size = 7))
save_plot(p4, "figure4_trend_depletion_sensitivity", 15, 8)

# Supplementary exposure-correlation heatmap.
cor_plot <- correlations |>
  dplyr::filter(
    outcome == "chd",
    correlation_type == "month_and_trend_residualised"
  ) |>
  dplyr::mutate(
    exposure_1 = factor(exposure_1, levels = rev(unique(exposure_1))),
    exposure_2 = factor(exposure_2, levels = unique(exposure_2))
  )
ps1 <- ggplot2::ggplot(cor_plot, ggplot2::aes(exposure_2, exposure_1, fill = correlation)) +
  ggplot2::geom_tile(colour = "white", linewidth = 0.4) +
  ggplot2::geom_text(ggplot2::aes(label = sprintf("%.2f", correlation)), size = 3) +
  ggplot2::scale_fill_gradient2(low = "#2b6f91", mid = "white", high = "#b84d31", limits = c(-1, 1)) +
  ggplot2::labs(
    title = "Exposure correlation after month and trend adjustment",
    x = NULL,
    y = NULL,
    fill = "Correlation"
  ) +
  theme_pub() +
  ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 35, hjust = 1))
save_plot(ps1, "../supplement/figureS1_exposure_correlation", 7.5, 6.5)

# Supplementary provisional HM/CM month calendar.
hm_path <- file.path(root, "data_processed", "hm_cm_month_flags_2013_2023.csv")
if (file.exists(hm_path)) {
  hm <- utils::read.csv(hm_path, stringsAsFactors = FALSE)
  hm_long <- hm |>
    dplyr::select(month_id, dplyr::matches("^(HM|CM)")) |>
    tidyr::pivot_longer(-month_id, names_to = "definition", values_to = "selected") |>
    dplyr::filter(!grepl("event_starts", definition))
  ps2 <- ggplot2::ggplot(hm_long, ggplot2::aes(month_id, definition, fill = factor(selected))) +
    ggplot2::geom_tile() +
    ggplot2::scale_fill_manual(values = c("0" = "#f0eee8", "1" = "#9c4f32"), na.value = "grey80") +
    ggplot2::scale_x_discrete(breaks = hm$month_id[seq(1, nrow(hm), 12)], guide = ggplot2::guide_axis(angle = 45)) +
    ggplot2::labs(
      title = "Provisional hot/cold-month selections",
      subtitle = "Supplementary only; weather reference rules are not team-locked",
      x = NULL,
      y = NULL,
      fill = "Selected"
    ) +
    theme_pub()
  save_plot(ps2, "../supplement/figureS2_provisional_hm_cm_calendar", 12, 5.5)
}

# Copy real residual figures and full pathway forests into the supplement.
copy_figures <- c(
  file.path(figures_dir, "diagnostics", "chd_core_residual_acf_pacf.png"),
  file.path(figures_dir, "diagnostics", "hf_core_residual_acf_pacf.png"),
  file.path(figures_dir, "pathway", "chd_pathway_panel_forest.png"),
  file.path(figures_dir, "pathway", "hf_pathway_panel_forest.png")
)
for (src in copy_figures[file.exists(copy_figures)]) {
  file.copy(src, file.path(release_supp, basename(src)), overwrite = TRUE)
}

writeLines(
  c(
    "# CHD/HF manuscript release package",
    "",
    "This directory contains disclosure-minimised aggregate tables and figures for the internal manuscript draft.",
    "",
    "- Outcomes: first hospitalisation after a CHD or HF diagnosis record among people with T2D and/or HTN.",
    "- Main model: separate exposure, negative binomial, month factor, natural spline of time (4 df), days-in-month offset.",
    "- Inference: Newey–West lag-6 confidence intervals.",
    "- All health inputs used for this package carry `HA_APPROVED_AGGREGATE`.",
    "- No source monthly HA count file or merged health panel is included.",
    "- External submission still requires team dissemination confirmation."
  ),
  file.path(release_dir, "README.md")
)

message("Publication artifacts written: ", release_dir)
