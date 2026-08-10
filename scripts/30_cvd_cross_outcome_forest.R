#!/usr/bin/env Rscript
# 30_cvd_cross_outcome_forest.R
# Combined forest for CHD vs HF on shared pathway terms.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "ggplot2"))

est_path <- file.path(root, "outputs", "tables", "combined_pathway_panel_estimates.csv")
if (!file.exists(est_path)) stop("Missing ", est_path)

est <- utils::read.csv(est_path, stringsAsFactors = FALSE)
stop_if_synthetic(est)

# Prefer pollution_stage none; keep CHD and HF only
est <- est |>
  dplyr::filter(outcome %in% c("chd", "hf")) |>
  dplyr::filter(is.na(pollution_stage) | pollution_stage %in% c("none", "")) |>
  dplyr::filter(!grepl("^month_f|^splines|^age_group|^sex|^covid", term))

# Shared terms present for both outcomes (same pathway_id + term)
shared_keys <- est |>
  dplyr::distinct(pathway_id, term, outcome) |>
  dplyr::count(pathway_id, term, name = "n_outcomes") |>
  dplyr::filter(n_outcomes >= 2L)

est <- est |>
  dplyr::inner_join(shared_keys[, c("pathway_id", "term")], by = c("pathway_id", "term")) |>
  dplyr::mutate(
    label = paste(pathway_id, term, sep = " · "),
    outcome = factor(outcome, levels = c("chd", "hf"))
  ) |>
  dplyr::arrange(pathway_id, term, outcome) |>
  dplyr::mutate(label = factor(label, levels = rev(unique(label))))

if (!nrow(est)) stop("No shared CHD/HF terms found in combined estimates")

# Prefer headline pathways for a cleaner figure; still write full shared table
headline <- est |>
  dplyr::filter(pathway_id %in% c("P01", "P02", "P03", "P04", "P05"))

fig_dir <- file.path(root, "outputs", "figures", "pathway")
tab_dir <- file.path(root, "outputs", "tables")
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

plot_forest <- function(dat, title) {
  ggplot2::ggplot(
    dat,
    ggplot2::aes(x = rr, y = label, xmin = rr_low, xmax = rr_high, colour = outcome)
  ) +
    ggplot2::geom_vline(xintercept = 1, linetype = "dashed", colour = "grey40") +
    ggplot2::geom_errorbar(
      ggplot2::aes(xmin = rr_low, xmax = rr_high),
      width = 0.25, orientation = "y",
      position = ggplot2::position_dodge(width = 0.55)
    ) +
    ggplot2::geom_point(
      size = 1.8,
      position = ggplot2::position_dodge(width = 0.55)
    ) +
    ggplot2::scale_x_log10() +
    ggplot2::scale_colour_manual(
      values = c(chd = "#0b3d4a", hf = "#8b3a3a"),
      labels = c(chd = "CHD", hf = "HF")
    ) +
    ggplot2::labs(
      title = title,
      subtitle = "Shared pathway terms; HA_APPROVED_AGGREGATE; 95% CI (Gate 3 open)",
      x = "Incidence rate ratio (log scale)",
      y = NULL,
      colour = "Outcome"
    ) +
    ggplot2::theme_minimal(base_size = 10) +
    ggplot2::theme(
      panel.grid.minor = ggplot2::element_blank(),
      plot.title = ggplot2::element_text(face = "bold"),
      legend.position = "bottom"
    )
}

p_head <- plot_forest(
  headline,
  "Cross-outcome forest (headline pathways) - CHD vs HF"
)
p_all <- plot_forest(
  est,
  "Cross-outcome forest (all shared terms) - CHD vs HF"
)

h_head <- max(5, 0.22 * dplyr::n_distinct(headline$label) + 1.5)
h_all <- max(6, 0.2 * dplyr::n_distinct(est$label) + 1.5)

ggplot2::ggsave(
  file.path(fig_dir, "cvd_cross_outcome_forest_headline.png"),
  p_head, width = 10, height = h_head, dpi = 150
)
ggplot2::ggsave(
  file.path(fig_dir, "cvd_cross_outcome_forest_headline.pdf"),
  p_head, width = 10, height = h_head
)
ggplot2::ggsave(
  file.path(fig_dir, "cvd_cross_outcome_forest_all.png"),
  p_all, width = 10, height = h_all, dpi = 150
)
ggplot2::ggsave(
  file.path(fig_dir, "cvd_cross_outcome_forest_all.pdf"),
  p_all, width = 10, height = h_all
)

# Table of shared estimates for manuscript prep
out_tab <- est |>
  dplyr::mutate(
    rr_ci = sprintf("%.3f (%.3f-%.3f)", rr, rr_low, rr_high)
  ) |>
  dplyr::select(
    pathway_id, pathway_title, term, outcome, rr, rr_low, rr_high, rr_ci,
    p_value, n_months, data_status
  )
write_csv_safe(out_tab, file.path(tab_dir, "cvd_cross_outcome_shared_estimates.csv"))

message(
  "Cross-outcome forest written (", nrow(shared_keys), " shared terms; ",
  dplyr::n_distinct(headline$label), " headline labels)"
)
