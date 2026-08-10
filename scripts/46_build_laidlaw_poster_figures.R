#!/usr/bin/env Rscript
# ============================================================================
# 46_build_laidlaw_poster_figures.R
#
# Poster-specific figures for the Laidlaw Stage 3 A0 portrait poster
# (reports/poster/Laidlaw_Stage3_A0_portrait.tex).
#
# Design intent: legibility at 1-2 m viewing distance on A0. Every figure is
# drawn 10 in wide (the physical width of one poster column) with base text at
# 20 pt, so printed labels land at roughly 20-24 pt. Nothing here recomputes
# estimates; values come straight from the validated release CSVs.
#
# Sources (read-only):
#   outputs/release_chd_hf/tables/table2_core_models.csv        (12 contrasts, NW6)
#   outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv (12 x 4 SE methods)
#   outputs/tables/exposure_aging/annual_extremes_and_spell_burden.csv (HKO extremes)
#
# Outputs (reports/poster/figures/):
#   fig_poster_forest12.{pdf,png}     12-contrast core panel (NW6), one page
#   fig_poster_uncertainty.{pdf,png}  2 leading contrasts x 4 SE methods
#   fig_poster_weather.{pdf,png}      annual hot nights vs cold days, 2013-2023
# ============================================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
})

# ---- locate repo root from --file= so the script runs from anywhere ---------
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
repo_root <- if (length(file_arg)) {
  normalizePath(file.path(dirname(sub("^--file=", "", file_arg[[1]])), ".."))
} else {
  normalizePath(getwd())
}

src_core    <- file.path(repo_root, "outputs/release_chd_hf/tables/table2_core_models.csv")
src_ladder  <- file.path(repo_root, "outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv")
src_weather <- file.path(repo_root, "outputs/tables/exposure_aging/annual_extremes_and_spell_burden.csv")
out_dir     <- file.path(repo_root, "reports/poster/figures")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

for (f in c(src_core, src_ladder, src_weather)) {
  if (!file.exists(f)) stop("Missing required source: ", f)
}

# ---- restrained poster palette (mirrors the TeX preamble) -------------------
col_ink   <- "#1B2A33"
col_navy  <- "#0E3A53"
col_teal  <- "#0B5563"
col_heat  <- "#B84A2E"   # warm accent: heat exposures
col_cold  <- "#2F6C9C"   # cool blue: cold exposure
col_slate <- "#5A6B74"   # continuous temperature metrics
col_grid  <- "#D8E0E3"

base_sz <- 21.5  # pt at a 10 in print width; at 249.8 mm column width -> ~20-21 pt printed

theme_poster <- function() {
  theme_minimal(base_size = base_sz, base_family = "sans") +
    theme(
      text               = element_text(colour = col_ink),
      axis.text          = element_text(size = base_sz * 0.95, colour = col_ink),
      axis.text.y        = element_text(size = base_sz, colour = col_ink),
      axis.title         = element_text(size = base_sz * 0.95, colour = col_ink),
      panel.grid.major.y = element_blank(),
      panel.grid.minor   = element_blank(),
      panel.grid.major.x = element_line(colour = col_grid, linewidth = 0.6),
      plot.margin        = margin(8, 14, 8, 8)
    )
}

save_pair <- function(plot, stem, width, height) {
  ggsave(file.path(out_dir, paste0(stem, ".pdf")), plot,
         width = width, height = height, device = cairo_pdf)
  ggsave(file.path(out_dir, paste0(stem, ".png")), plot,
         width = width, height = height, dpi = 300, type = "cairo")
  invisible(TRUE)
}

fmt_est <- function(rr, lo, hi) {
  sprintf("%.3f (%.3f\u2013%.3f)", rr, lo, hi)
}

exposure_order <- c("hot_nights", "very_hot_days", "cold_days",
                    "mean_temp", "mean_tmax", "mean_tmin")
exposure_labels <- c(
  hot_nights    = "Hot nights\nper 5 days",
  very_hot_days = "Very hot days\nper 5 days",
  cold_days     = "Cold days\nper 5 days",
  mean_temp     = "Mean temp.\nper 1 \u00B0C",
  mean_tmax     = "Mean max. temp.\nper 1 \u00B0C",
  mean_tmin     = "Mean min. temp.\nper 1 \u00B0C"
)
exposure_class <- c(
  hot_nights = "heat", very_hot_days = "heat", cold_days = "cold",
  mean_temp = "temp", mean_tmax = "temp", mean_tmin = "temp"
)
class_cols <- c(heat = col_heat, cold = col_cold, temp = col_slate)

# ============================================================================
# Figure 1: the 12-contrast core panel (NW6 intervals)
# Two side-by-side outcome panels (CHD | HF), six rows each; estimate column
# on the right of each panel. Wide + short so it dominates a full-width
# results band while keeping labels large.
# ============================================================================
core <- read.csv(src_core, stringsAsFactors = FALSE) |>
  mutate(
    exposure = factor(exposure, levels = exposure_order),
    est_txt  = fmt_est(rr, rr_low, rr_high),
    eclass   = unname(exposure_class[as.character(exposure)]),
    outcome_lab = ifelse(outcome == "chd",
                         "Coronary heart disease (CHD)", "Heart failure (HF)")
  ) |>
  arrange(outcome, exposure)
core$outcome_lab <- factor(core$outcome_lab,
                           levels = c("Coronary heart disease (CHD)",
                                      "Heart failure (HF)"))
core$y <- rep(6:1, 2)  # row order within each panel: exposure_order top->bottom

est_hdr <- data.frame(
  outcome_lab = factor(c("Coronary heart disease (CHD)", "Heart failure (HF)"),
                       levels = levels(core$outcome_lab)),
  y = 6.62,
  label = rep("Count ratio (95% CI)", 2)
)

p_forest <- ggplot(core, aes(x = rr, y = y, colour = eclass)) +
  facet_wrap(~outcome_lab, ncol = 2) +
  geom_vline(xintercept = 1, colour = col_ink, linewidth = 0.9,
             linetype = "dashed") +
  geom_errorbar(aes(xmin = rr_low, xmax = rr_high),
                orientation = "y", width = 0.42, linewidth = 1.8) +
  geom_point(size = 5.5) +
  geom_text(aes(x = 1.162, label = est_txt),
            hjust = 0, size = base_sz * 0.95 / .pt, colour = col_ink,
            family = "sans") +
  geom_text(data = est_hdr, aes(x = 1.162, y = y, label = label),
            inherit.aes = FALSE, hjust = 0, vjust = 0.5,
            fontface = "bold", size = base_sz * 0.9 / .pt,
            colour = col_navy, family = "sans") +
  scale_x_continuous(
    trans  = "log10",
    limits = c(0.9335, 1.32),
    breaks = c(0.95, 1.00, 1.05, 1.10, 1.15),
    labels = sprintf("%.2f", c(0.95, 1.00, 1.05, 1.10, 1.15))
  ) +
  scale_y_continuous(
    breaks = 6:1,
    labels = unname(exposure_labels[exposure_order]),
    limits = c(0.4, 6.9),
    expand = c(0, 0)
  ) +
  scale_colour_manual(values = class_cols, guide = "none") +
  labs(x = "Count ratio per exposure increment (log scale)", y = NULL) +
  coord_cartesian(clip = "off") +
  theme_poster() +
  theme(
    axis.text.y = element_text(hjust = 1),
    strip.text  = element_text(face = "bold", size = base_sz * 1.12,
                               colour = col_navy),
    strip.background = element_blank(),
    panel.spacing.x = unit(16, "mm")
  )

save_pair(p_forest, "fig_poster_forest12", width = 18, height = 11.6)

# ============================================================================
# Figure 2: uncertainty ladder for the two leading contrasts (8 rows)
# ============================================================================
leads <- list(
  list(outcome = "chd", exposure = "hot_nights", eclass = "heat",
       header = "CHD \u00D7 hot nights, per 5 days"),
  list(outcome = "hf",  exposure = "cold_days",  eclass = "cold",
       header = "HF \u00D7 cold days, per 5 days")
)

ladder <- read.csv(src_ladder, stringsAsFactors = FALSE)
method_order  <- c("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")
method_labels <- c(model = "Model", HC1 = "HC1",
                   NeweyWest_lag3 = "NW3", NeweyWest_lag6 = "NW6")

rows <- list()
hdrs <- list()
y_next <- 9
for (ld in leads) {
  hdrs[[length(hdrs) + 1]] <- data.frame(y = y_next, label = ld$header,
                                         eclass = ld$eclass)
  sub <- ladder[ladder$outcome == ld$outcome & ladder$exposure == ld$exposure, ]
  sub <- sub[match(method_order, sub$se_method), ]
  sub$y      <- (y_next - 1):(y_next - 4)
  sub$eclass <- ld$eclass
  sub$method_label <- unname(method_labels[sub$se_method])
  sub$est_txt <- fmt_est(sub$rr, sub$rr_low, sub$rr_high)
  # CHD hot-night NW3 rounds to 1.000 at 3 dp; show 4 dp so readers can see
  # why it narrowly excludes 1 before rounding (raw: 1.000253-1.043860).
  is_chd_nw3 <- ld$outcome == "chd" & ld$exposure == "hot_nights" &
    sub$se_method == "NeweyWest_lag3"
  if (any(is_chd_nw3)) {
    sub$est_txt[is_chd_nw3] <- sprintf(
      "%.3f (%.4f\u2013%.4f)", sub$rr[is_chd_nw3],
      sub$rr_low[is_chd_nw3], sub$rr_high[is_chd_nw3]
    )
  }
  rows[[length(rows) + 1]] <- sub
  y_next <- y_next - 5
}
lad  <- do.call(rbind, rows)
hdrs <- do.call(rbind, hdrs)

p_ladder <- ggplot(lad, aes(x = rr, y = y, colour = eclass)) +
  geom_vline(xintercept = 1, colour = col_ink, linewidth = 0.9,
             linetype = "dashed") +
  geom_errorbar(aes(xmin = rr_low, xmax = rr_high),
                orientation = "y", width = 0.4, linewidth = 1.8) +
  geom_point(size = 5.5) +
  geom_text(aes(x = 1.157, label = est_txt),
            hjust = 0, size = base_sz * 0.92 / .pt, colour = col_ink,
            family = "sans") +
  geom_text(data = hdrs, aes(x = 0.989, y = y, label = label),
            inherit.aes = FALSE, hjust = 0, fontface = "bold",
            size = base_sz * 1.02 / .pt, colour = col_navy, family = "sans") +
  scale_x_continuous(
    trans  = "log10",
    limits = c(0.989, 1.30),
    breaks = c(1.00, 1.05, 1.10, 1.15),
    labels = sprintf("%.2f", c(1.00, 1.05, 1.10, 1.15))
  ) +
  scale_y_continuous(
    breaks = lad$y[order(-lad$y)],
    labels = lad$method_label[order(-lad$y)],
    limits = c(-0.6, 9.6),
    expand = c(0, 0)
  ) +
  scale_colour_manual(values = class_cols, guide = "none") +
  labs(x = "Count ratio (95% CI, log scale)", y = NULL) +
  coord_cartesian(clip = "off") +
  theme_poster()

save_pair(p_ladder, "fig_poster_uncertainty", width = 10, height = 10.8)

# ============================================================================
# Figure 3: weather context - hot nights climb, cold days persist
# ============================================================================
wx <- read.csv(src_weather, stringsAsFactors = FALSE)

p_wx <- ggplot(wx, aes(x = year)) +
  geom_col(aes(y = hot_nights, fill = "Hot nights (Tmin \u2265 28 \u00B0C)"),
           width = 0.66, alpha = 0.92) +
  geom_line(aes(y = cold_days, colour = "Cold days (Tmin \u2264 12 \u00B0C)"),
            linewidth = 2.2) +
  geom_point(aes(y = cold_days, colour = "Cold days (Tmin \u2264 12 \u00B0C)"),
             size = 5) +
  scale_fill_manual(values = c("Hot nights (Tmin \u2265 28 \u00B0C)" = col_heat),
                    name = NULL) +
  scale_colour_manual(values = c("Cold days (Tmin \u2264 12 \u00B0C)" = col_cold),
                      name = NULL) +
  scale_x_continuous(breaks = 2013:2023, expand = expansion(mult = c(0.01, 0.01))) +
  scale_y_continuous(limits = c(0, 68), expand = expansion(mult = c(0, 0.02))) +
  labs(x = NULL, y = "Days per year") +
  theme_poster() +
  theme(
    legend.position  = c(0.02, 0.98),
    legend.justification = c(0, 1),
    legend.text      = element_text(size = base_sz * 0.95),
    legend.key.width = unit(1.6, "lines"),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(colour = col_grid, linewidth = 0.6)
  )

save_pair(p_wx, "fig_poster_weather", width = 12.5, height = 7.0)

message("Poster figures written to ", out_dir)
