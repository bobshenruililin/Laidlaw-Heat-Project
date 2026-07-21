#!/usr/bin/env Rscript
# 24_pathway_forest_figure.R
# Forest-style panel figure for pathway IRR estimates (manuscript-ready layout).

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "ggplot2"))

est_path <- file.path(root, "outputs", "tables", "pathway_panel_estimates.csv")
if (!file.exists(est_path)) stop("Missing ", est_path)

est <- utils::read.csv(est_path, stringsAsFactors = FALSE)
is_synthetic <- any(grepl("SYNTHETIC", est$data_status %||% ""))

# Prefer pollution_stage none when staged
est <- est |>
  dplyr::filter(is.na(pollution_stage) | pollution_stage %in% c("none", "")) |>
  dplyr::mutate(
    label = paste(pathway_id, term, sep = " · "),
    pathway_id = factor(pathway_id, levels = unique(pathway_id))
  )

# Keep exposure-like terms (drop pure confounder interactions noise if any slipped)
est <- est |>
  dplyr::filter(!grepl("^month_f|^splines|^age_group|^sex|^covid", term))

# Order for plot
est <- est |>
  dplyr::arrange(pathway_id, term) |>
  dplyr::mutate(label = factor(label, levels = rev(unique(label))))

out_dir <- file.path(root, "outputs", "figures", "pathway")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

p <- ggplot2::ggplot(est, ggplot2::aes(x = rr, y = label, xmin = rr_low, xmax = rr_high)) +
  ggplot2::geom_vline(xintercept = 1, linetype = "dashed", colour = "grey40") +
  ggplot2::geom_errorbar(ggplot2::aes(xmin = rr_low, xmax = rr_high), width = 0.2, colour = "#1f4e5f", orientation = "y") +
  ggplot2::geom_point(size = 1.8, colour = "#0b3d4a") +
  ggplot2::scale_x_log10() +
  ggplot2::labs(
    title = if (is_synthetic) {
      "Pathway panel IRRs (SYNTHETIC dry-run - not findings)"
    } else {
      "Pathway panel IRRs - stroke aggregates x thermal exposures"
    },
    subtitle = "Negative binomial / quasi-Poisson monthly models; 95% CI",
    x = "Incidence rate ratio (log scale)",
    y = NULL
  ) +
  ggplot2::theme_minimal(base_size = 10) +
  ggplot2::theme(
    panel.grid.minor = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold")
  )

png_path <- file.path(out_dir, "pathway_panel_forest.png")
pdf_path <- file.path(out_dir, "pathway_panel_forest.pdf")
ggplot2::ggsave(png_path, p, width = 10, height = max(6, 0.28 * nrow(est)), dpi = 150)
ggplot2::ggsave(pdf_path, p, width = 10, height = max(6, 0.28 * nrow(est)))

message("Forest figure written: ", png_path)
if (is_synthetic) message("WARNING: SYNTHETIC forest — formatting check only.")
