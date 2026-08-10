#!/usr/bin/env Rscript
# 24_pathway_forest_figure.R
# Forest-style panel figure for pathway IRR estimates (manuscript-ready layout).

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
outcome <- tolower(Sys.getenv("OUTCOME", unset = "stroke"))
mode <- tolower(Sys.getenv("PATHWAY_MODE", unset = "dev"))
ensure_packages(c("dplyr", "ggplot2"))

est_path <- file.path(root, "outputs", "tables", paste0(outcome, "_pathway_panel_estimates.csv"))
if (!file.exists(est_path)) stop("Missing ", est_path)

est <- utils::read.csv(est_path, stringsAsFactors = FALSE)
is_synthetic <- any(grepl("SYNTHETIC", est$data_status %||% ""))
if (identical(mode, "real") && is_synthetic) {
  stop("Real pathway forest refused SYNTHETIC rows for ", outcome)
}

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
      paste0("Pathway panel IRRs - ", toupper(outcome), " aggregates x thermal exposures")
    },
    subtitle = "Negative-binomial / quasi-Poisson monthly models; 95% CI",
    x = "Exponentiated count/rate ratio (log scale)",
    y = NULL
  ) +
  ggplot2::theme_minimal(base_size = 10) +
  ggplot2::theme(
    panel.grid.minor = ggplot2::element_blank(),
    plot.title = ggplot2::element_text(face = "bold")
  )

out_png <- file.path(out_dir, paste0(outcome, "_pathway_panel_forest.png"))
out_pdf <- file.path(out_dir, paste0(outcome, "_pathway_panel_forest.pdf"))
h <- max(6, 0.28 * nrow(est))
ggplot2::ggsave(out_png, p, width = 10, height = h, dpi = 300)
ggplot2::ggsave(out_pdf, p, width = 10, height = h)

message("Forest figure written: ", out_png)
if (is_synthetic) message("WARNING: SYNTHETIC forest — formatting check only.")
