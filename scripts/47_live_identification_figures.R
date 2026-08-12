#!/usr/bin/env Rscript
# 47_live_identification_figures.R
# Identification diagnostics from existing public-climate and approved aggregate
# tables. This script does not fit or update any health-outcome model.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "ggplot2", "readr", "scales", "tidyr"))

out_dir <- file.path(root, "outputs", "live_identification")
fig_dir <- file.path(root, "figures", "live_identification")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(fig_dir, recursive = TRUE, showWarnings = FALSE)

wrap_caption <- function(x, width = 112L) {
  paste(strwrap(x, width = width), collapse = "\n")
}

save_figure <- function(plot, stem, width, height) {
  pdf_device <- if (isTRUE(capabilities("cairo"))) grDevices::cairo_pdf else "pdf"
  ggplot2::ggsave(
    file.path(fig_dir, paste0(stem, ".pdf")),
    plot,
    width = width,
    height = height,
    units = "in",
    device = pdf_device
  )
  ggplot2::ggsave(
    file.path(fig_dir, paste0(stem, ".png")),
    plot,
    width = width,
    height = height,
    units = "in",
    dpi = 320,
    bg = "white"
  )
}

theme_identification <- function(base_size = 10.5) {
  ggplot2::theme_minimal(base_size = base_size) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(
        face = "bold", size = base_size + 2.5, colour = "#202124"
      ),
      plot.subtitle = ggplot2::element_text(
        size = base_size - 0.3, colour = "#42464B", margin = ggplot2::margin(b = 8)
      ),
      plot.caption = ggplot2::element_text(
        size = base_size - 2.2, colour = "#5F6368", hjust = 0,
        margin = ggplot2::margin(t = 8)
      ),
      strip.text = ggplot2::element_text(
        face = "bold", hjust = 0, colour = "#202124"
      ),
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major.x = ggplot2::element_blank(),
      axis.title = ggplot2::element_text(colour = "#303236"),
      axis.text = ggplot2::element_text(colour = "#303236"),
      plot.margin = ggplot2::margin(9, 12, 9, 9)
    )
}

# ---------------------------------------------------------------------------
# Figure A: where monthly cold-day variation occurs
# ---------------------------------------------------------------------------
climate_path <- file.path(
  root, "outputs", "share_for_roro", "temperature_monthly_panel_2013_2023.csv"
)
climate <- readr::read_csv(climate_path, show_col_types = FALSE)
validate_required_columns(
  climate,
  c("month_id", "year", "month", "cold_days", "station"),
  "temperature monthly panel"
)
assert_month_id(climate$month_id)
stopifnot(
  nrow(climate) == 132L,
  !anyDuplicated(climate$month_id),
  identical(as.integer(sort(unique(climate$year))), 2013:2023),
  all(climate$month %in% 1:12),
  all(climate$station == "HKO"),
  all(!is.na(climate$cold_days)),
  all(climate$cold_days >= 0),
  all(climate$cold_days == as.integer(climate$cold_days))
)

cold_month_totals <- climate |>
  dplyr::group_by(month) |>
  dplyr::summarise(cold_days = sum(cold_days), .groups = "drop")
expected_cold_totals <- c(`1` = 54L, `2` = 47L, `3` = 4L, `12` = 40L)
stopifnot(
  sum(climate$cold_days) == 145L,
  sum(climate$cold_days[climate$month %in% c(12L, 1L, 2L)]) == 141L,
  all(
    cold_month_totals$cold_days[match(as.integer(names(expected_cold_totals)),
                                     cold_month_totals$month)] ==
      unname(expected_cold_totals)
  ),
  sum(cold_month_totals$cold_days[!cold_month_totals$month %in% c(1L, 2L, 3L, 12L)]) == 0L
)

cold_by_month_year <- climate |>
  dplyr::transmute(
    month_id,
    year = as.integer(year),
    month = as.integer(month),
    month_label = factor(month.abb[month], levels = month.abb),
    cold_days = as.integer(cold_days),
    station,
    data_status = "REAL",
    source = "Hong Kong Observatory Headquarters"
  )
readr::write_csv(
  cold_by_month_year,
  file.path(out_dir, "cold_days_by_month_year.csv")
)

p_a <- ggplot2::ggplot(
  cold_by_month_year,
  ggplot2::aes(x = month_label, y = year, fill = cold_days)
) +
  ggplot2::geom_tile(colour = "white", linewidth = 0.45) +
  ggplot2::geom_text(
    ggplot2::aes(
      label = ifelse(cold_days > 0, cold_days, ""),
      colour = cold_days >= 6
    ),
    size = 3.0,
    fontface = "bold",
    show.legend = FALSE
  ) +
  ggplot2::scale_colour_manual(values = c(`FALSE` = "#183143", `TRUE` = "white")) +
  ggplot2::scale_fill_gradientn(
    colours = c("#F7F9FB", "#C8DEEB", "#6FA4C3", "#245E83"),
    values = scales::rescale(c(0, 2, 6, 11)),
    breaks = c(0, 2, 4, 6, 8, 10),
    limits = c(0, 11),
    name = "Cold days"
  ) +
  ggplot2::scale_y_reverse(breaks = 2013:2023) +
  ggplot2::labs(
    title = "Cold days are concentrated in winter",
    subtitle = "141 of 145 days occurred in December–February (Dec 40, Jan 54, Feb 47); the remaining 4 occurred in March",
    x = NULL,
    y = NULL,
    caption = wrap_caption(paste(
      "Environmental provenance: REAL public Hong Kong Observatory Headquarters data;",
      "cold day = daily minimum temperature ≤12°C.",
      "Identification: remaining variation after calendar-month indicators is",
      "between-year winter, not summer-versus-winter."
    ))
  ) +
  theme_identification() +
  ggplot2::theme(
    panel.grid = ggplot2::element_blank(),
    legend.position = "right",
    legend.title = ggplot2::element_text(face = "bold"),
    axis.text.x = ggplot2::element_text(face = "bold")
  )
save_figure(p_a, "figure_A_cold_day_identification", 8.0, 5.8)

# ---------------------------------------------------------------------------
# Figure B: first-event totals versus a broad population denominator
# ---------------------------------------------------------------------------
annual_path <- file.path(root, "outputs", "tables", "cvd_descriptive_annual_totals.csv")
summary_path <- file.path(
  root, "outputs", "release_chd_hf", "tables", "table1_outcome_summary.csv"
)
population_path <- file.path(
  root, "outputs", "tables", "population_midyear_by_age_group.csv"
)

annual <- readr::read_csv(annual_path, show_col_types = FALSE)
outcome_summary <- readr::read_csv(summary_path, show_col_types = FALSE)
population_age <- readr::read_csv(population_path, show_col_types = FALSE)

validate_required_columns(
  annual,
  c("outcome", "year", "data_status", "n_months", "total_events", "mean_population"),
  "annual CHD/HF totals"
)
validate_required_columns(
  outcome_summary,
  c("outcome", "n_months", "total_events", "data_status"),
  "outcome summary"
)
validate_required_columns(
  population_age,
  c("year", "age_group", "population"),
  "population by age group"
)
stopifnot(
  nrow(annual) == 22L,
  all(annual$data_status == "HA_APPROVED_AGGREGATE"),
  all(annual$n_months == 12L),
  all(outcome_summary$data_status == "HA_APPROVED_AGGREGATE"),
  all(outcome_summary$n_months == 132L)
)

annual_sum_check <- annual |>
  dplyr::group_by(outcome) |>
  dplyr::summarise(total_events = sum(total_events), .groups = "drop") |>
  dplyr::inner_join(
    outcome_summary |>
      dplyr::select(outcome, released_total_events = total_events),
    by = "outcome"
  )
stopifnot(all(annual_sum_check$total_events == annual_sum_check$released_total_events))

population_annual <- population_age |>
  dplyr::group_by(year) |>
  dplyr::summarise(value = sum(population), .groups = "drop")
population_check <- annual |>
  dplyr::select(year, mean_population) |>
  dplyr::distinct() |>
  dplyr::inner_join(population_annual, by = "year")
stopifnot(
  nrow(population_annual) == 11L,
  nrow(population_check) == 11L,
  max(abs(population_check$mean_population - population_check$value)) < 1
)

annual_health_plot <- annual |>
  dplyr::transmute(
    year = as.integer(year),
    panel = dplyr::recode(
      outcome,
      chd = "CHD first hospitalisations (annual total)",
      hf = "HF first hospitalisations (annual total)"
    ),
    series = dplyr::recode(outcome, chd = "CHD", hf = "HF"),
    value = total_events
  )
population_plot <- population_annual |>
  dplyr::transmute(
    year = as.integer(year),
    panel = "Hong Kong population aged 35+ (persons; contextual only)",
    series = "Population aged 35+",
    value
  )

panel_levels <- c(
  "CHD first hospitalisations (annual total)",
  "HF first hospitalisations (annual total)",
  "Hong Kong population aged 35+ (persons; contextual only)"
)
annual_plot <- dplyr::bind_rows(annual_health_plot, population_plot) |>
  dplyr::mutate(
    panel = factor(panel, levels = panel_levels),
    series = factor(series, levels = c("CHD", "HF", "Population aged 35+"))
  )

endpoints <- annual_plot |>
  dplyr::filter(year %in% c(2013L, 2023L)) |>
  dplyr::mutate(
    endpoint_label = ifelse(
      series == "Population aged 35+",
      sprintf("%.2f m", value / 1e6),
      scales::comma(value)
    ),
    endpoint_hjust = ifelse(year == 2013L, -0.08, 1.08)
  )

change_wide <- annual |>
  dplyr::filter(year %in% c(2013L, 2023L)) |>
  dplyr::select(outcome, year, total_events) |>
  tidyr::pivot_wider(names_from = year, values_from = total_events) |>
  dplyr::mutate(pct_change = (`2023` / `2013` - 1) * 100)
chd_change <- change_wide$pct_change[change_wide$outcome == "chd"]
hf_change <- change_wide$pct_change[change_wide$outcome == "hf"]
pop_change <- with(
  population_annual,
  (value[year == 2023L] / value[year == 2013L] - 1) * 100
)

p_b <- ggplot2::ggplot(
  annual_plot,
  ggplot2::aes(x = year, y = value, colour = series, group = series)
) +
  ggplot2::geom_line(linewidth = 0.9) +
  ggplot2::geom_point(size = 2.1) +
  ggplot2::geom_text(
    data = endpoints,
    ggplot2::aes(label = endpoint_label, hjust = endpoint_hjust),
    vjust = -0.65,
    size = 2.8,
    fontface = "bold",
    show.legend = FALSE
  ) +
  ggplot2::facet_wrap(~panel, ncol = 1, scales = "free_y") +
  ggplot2::scale_colour_manual(
    values = c(
      "CHD" = "#175A68",
      "HF" = "#8A3E4C",
      "Population aged 35+" = "#6C737A"
    ),
    guide = "none"
  ) +
  ggplot2::scale_x_continuous(
    breaks = 2013:2023,
    labels = as.character(2013:2023),
    expand = ggplot2::expansion(add = c(0.35, 0.35))
  ) +
  ggplot2::scale_y_continuous(
    labels = scales::label_comma(),
    expand = ggplot2::expansion(mult = c(0.03, 0.17))
  ) +
  ggplot2::labs(
    title = "First-hospitalisation totals decline while the broad population rises",
    subtitle = sprintf(
      "2013–2023 change: CHD %.0f%%, HF %.0f%%, Hong Kong population aged 35+ +%.0f%%",
      chd_change, hf_change, pop_change
    ),
    x = NULL,
    y = NULL,
    caption = wrap_caption(paste(
      "Health provenance: HA_APPROVED_AGGREGATE annual summaries.",
      "Demographic provenance: REAL public C&SD population aged 35+, which is not the T2D/HTN cohort risk set.",
      "First-event totals fall by about half; this is expected under a 2013–2023 diagnosis window plus",
      "pandemic care-seeking, and is not incidence without still-at-risk person-time."
    ))
  ) +
  theme_identification() +
  ggplot2::theme(
    axis.text.x = ggplot2::element_text(angle = 45, hjust = 1),
    panel.spacing.y = grid::unit(0.75, "lines")
  )
save_figure(p_b, "figure_B_first_event_depletion", 8.0, 8.2)

# ---------------------------------------------------------------------------
# Figure C: existing residual ACF diagnostics for the two manuscript contrasts
# ---------------------------------------------------------------------------
chd_acf_path <- file.path(root, "outputs", "tables", "chd_pathway_residual_acf.csv")
hf_acf_path <- file.path(root, "outputs", "tables", "hf_pathway_residual_acf.csv")
core_path <- file.path(
  root, "outputs", "release_chd_hf", "tables", "table2_core_models.csv"
)
uncertainty_path <- file.path(
  root, "outputs", "release_chd_hf", "tables", "table4_uncertainty_ladder.csv"
)

chd_acf <- readr::read_csv(chd_acf_path, show_col_types = FALSE)
hf_acf <- readr::read_csv(hf_acf_path, show_col_types = FALSE)
core <- readr::read_csv(core_path, show_col_types = FALSE)
uncertainty <- readr::read_csv(uncertainty_path, show_col_types = FALSE)

validate_required_columns(chd_acf, c("outcome", "pathway_id", "lag", "acf"), "CHD ACF")
validate_required_columns(hf_acf, c("outcome", "pathway_id", "lag", "acf"), "HF ACF")
validate_required_columns(
  core,
  c("outcome", "pathway_id", "exposure", "n_months", "data_status"),
  "core model table"
)
validate_required_columns(
  uncertainty,
  c("outcome", "pathway_id", "se_method", "data_status"),
  "uncertainty ladder"
)

key_specs <- core |>
  dplyr::filter(
    (outcome == "chd" & exposure == "hot_nights") |
      (outcome == "hf" & exposure == "cold_days")
  ) |>
  dplyr::select(outcome, pathway_id, exposure, n_months, data_status)
stopifnot(
  nrow(key_specs) == 2L,
  all(key_specs$n_months == 132L),
  all(key_specs$data_status == "HA_APPROVED_AGGREGATE")
)

nw_check <- uncertainty |>
  dplyr::inner_join(
    key_specs |>
      dplyr::select(outcome, pathway_id),
    by = c("outcome", "pathway_id")
  ) |>
  dplyr::filter(se_method %in% c("NeweyWest_lag3", "NeweyWest_lag6"))
stopifnot(
  nrow(nw_check) == 4L,
  all(nw_check$data_status == "HA_APPROVED_AGGREGATE")
)

acf_selected <- dplyr::bind_rows(chd_acf, hf_acf) |>
  dplyr::inner_join(key_specs, by = c("outcome", "pathway_id")) |>
  dplyr::filter(lag %in% 1:12) |>
  dplyr::mutate(
    series = dplyr::case_when(
      outcome == "chd" ~ "CHD hot nights (P04A)",
      outcome == "hf" ~ "HF cold days (P04B)"
    ),
    series = factor(series, levels = c(
      "CHD hot nights (P04A)",
      "HF cold days (P04B)"
    ))
  )
stopifnot(
  nrow(acf_selected) == 24L,
  all(table(acf_selected$series) == 12L)
)

acf_lag1 <- acf_selected |>
  dplyr::filter(lag == 1L) |>
  dplyr::mutate(label = sprintf("ACF(1) = %.2f", acf))
chd_acf1 <- acf_lag1$acf[acf_lag1$outcome == "chd"]
hf_acf1 <- acf_lag1$acf[acf_lag1$outcome == "hf"]
white_noise_bound <- 1.96 / sqrt(132)

p_c <- ggplot2::ggplot(
  acf_selected,
  ggplot2::aes(x = lag, y = acf, colour = series, group = series)
) +
  ggplot2::geom_hline(yintercept = 0, colour = "#6C737A", linewidth = 0.45) +
  ggplot2::geom_hline(
    yintercept = c(-white_noise_bound, white_noise_bound),
    colour = "#A4A9AE",
    linewidth = 0.45,
    linetype = "dashed"
  ) +
  ggplot2::geom_segment(
    ggplot2::aes(xend = lag, y = 0, yend = acf),
    linewidth = 0.65,
    alpha = 0.80
  ) +
  ggplot2::geom_point(size = 2.3) +
  ggplot2::geom_label(
    data = acf_lag1,
    ggplot2::aes(label = label),
    hjust = -0.08,
    vjust = ifelse(acf_lag1$outcome == "chd", -0.65, 1.35),
    size = 2.8,
    label.size = 0,
    fill = "white",
    show.legend = FALSE
  ) +
  ggplot2::scale_colour_manual(
    values = c(
      "CHD hot nights (P04A)" = "#175A68",
      "HF cold days (P04B)" = "#8A3E4C"
    ),
    name = NULL
  ) +
  ggplot2::scale_x_continuous(breaks = 1:12) +
  ggplot2::scale_y_continuous(
    breaks = seq(-0.2, 0.6, by = 0.2),
    limits = c(-0.24, 0.60),
    labels = scales::label_number(accuracy = 0.1)
  ) +
  ggplot2::labs(
    title = "Residual persistence is stronger for CHD than HF",
    subtitle = sprintf(
      "Lag-1 residual ACF: CHD %.2f versus HF %.2f; dashed lines are ±1.96/√132 reference bounds",
      chd_acf1, hf_acf1
    ),
    x = "Lag (months)",
    y = "Residual autocorrelation",
    caption = wrap_caption(paste(
      "Health provenance: existing HA_APPROVED_AGGREGATE model diagnostics for the two manuscript contrasts.",
      "The stronger CHD residual persistence supports the serial-correlation-robust Newey–West uncertainty display,",
      "especially for CHD; this script fits no new model."
    ))
  ) +
  theme_identification() +
  ggplot2::theme(
    legend.position = "top",
    legend.justification = "left"
  )
save_figure(p_c, "figure_C_residual_acf", 8.0, 5.4)

# Reproducible interpretation note. Keep claims bounded to identification and
# outcome construction; these diagnostics do not create confirmatory evidence.
readme_lines <- c(
  "# Live-manuscript identification figures",
  "",
  "**Scope:** diagnostic displays from existing tables only. The script fits no new health model, contains no stroke result, and does not export month-level HA counts.",
  "",
  "## Figure A — cold-day identification",
  "",
  "- **What it shows:** 141 of 145 cold days occurred in December–February (December 40, January 54, February 47); four occurred in March. With calendar-month indicators, the identifying cold-day variation is between winters across years, not the crude summer–winter contrast.",
  "- **Source:** `outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv` (`REAL`, public Hong Kong Observatory Headquarters).",
  "- **Do not claim:** a health effect, a daily lag structure, or that the model compares summer with winter.",
  "",
  "## Figure B — first-event depletion and the population contrast",
  "",
  sprintf(
    "- **What it shows:** CHD annual first-hospitalisation totals changed from 23,830 to 12,323 (%.0f%%), and HF from 4,336 to 2,296 (%.0f%%), while the public population aged 35+ rose by %.0f%%.",
    chd_change, hf_change, pop_change
  ),
  "- **Sources:** `outputs/tables/cvd_descriptive_annual_totals.csv` and `outputs/release_chd_hf/tables/table1_outcome_summary.csv` (`HA_APPROVED_AGGREGATE`); `outputs/tables/population_midyear_by_age_group.csv` (`REAL`, public C&SD).",
  "- **Do not claim:** incidence, a stable T2D/HTN risk set, or that depletion and pandemic care-seeking uniquely explain the decline. Incidence requires still-at-risk cohort person-time.",
  "",
  "## Figure C — residual autocorrelation",
  "",
  sprintf(
    "- **What it shows:** existing residual ACF(1) is %.3f for the CHD hot-night contrast and %.3f for the HF cold-day contrast; CHD has materially stronger serial persistence.",
    chd_acf1, hf_acf1
  ),
  "- **Sources:** `outputs/tables/chd_pathway_residual_acf.csv`, `outputs/tables/hf_pathway_residual_acf.csv`, `outputs/release_chd_hf/tables/table2_core_models.csv`, and `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` (existing `HA_APPROVED_AGGREGATE` diagnostics).",
  "- **Do not claim:** that this script fitted a model, that Newey–West uncertainty confirms either thermal association, or that residual ACF establishes causality.",
  "",
  "## Files",
  "",
  "- `figures/live_identification/figure_A_cold_day_identification.pdf` and `.png`",
  "- `figures/live_identification/figure_B_first_event_depletion.pdf` and `.png`",
  "- `figures/live_identification/figure_C_residual_acf.pdf` and `.png`",
  "- `outputs/live_identification/cold_days_by_month_year.csv`",
  "",
  "Figure captions distinguish public environmental/demographic data from approved health aggregates."
)
writeLines(readme_lines, file.path(out_dir, "README.md"))

message("Wrote ", file.path(out_dir, "cold_days_by_month_year.csv"))
message("Wrote ", file.path(out_dir, "README.md"))
message("Wrote three PDF/PNG figure pairs under ", fig_dir)
#!/usr/bin/env Rscript
# 47_live_identification_figures.R
# Identification figures for Hogan's live manuscript.
# No new health models. Provenance labelled in captions.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("ggplot2", "dplyr", "tidyr", "readr", "scales"))

dir.create("figures/live_identification", showWarnings = FALSE, recursive = TRUE)
dir.create("outputs/live_identification", showWarnings = FALSE, recursive = TRUE)

pdf_device <- if (isTRUE(capabilities("cairo"))) cairo_pdf else "pdf"

# ---------------------------------------------------------------------------
# Figure A. Cold-day identification (REAL public HKO)
# ---------------------------------------------------------------------------
temp <- readr::read_csv(
  file.path(root, "outputs/share_for_roro/temperature_monthly_panel_2013_2023.csv"),
  show_col_types = FALSE
)
stopifnot(nrow(temp) == 132L)
stopifnot(sum(temp$cold_days) == 145L)

by_month <- temp |>
  group_by(month) |>
  summarise(cold_days = sum(cold_days), .groups = "drop")
stopifnot(as.integer(by_month$cold_days[by_month$month == 12]) == 40L)
stopifnot(as.integer(by_month$cold_days[by_month$month == 1]) == 54L)
stopifnot(as.integer(by_month$cold_days[by_month$month == 2]) == 47L)
stopifnot(as.integer(by_month$cold_days[by_month$month == 3]) == 4L)

readr::write_csv(
  temp |>
    select(month_id, year, month, cold_days, hot_nights, very_hot_days) |>
    mutate(data_status = "REAL"),
  "outputs/live_identification/cold_days_by_month_year.csv"
)

temp <- temp |>
  mutate(
    month_lab = factor(
      month,
      levels = 1:12,
      labels = c("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    )
  )

p_a <- ggplot(temp, aes(x = month_lab, y = factor(year), fill = cold_days)) +
  geom_tile(colour = "white", linewidth = 0.3) +
  geom_text(
    aes(label = ifelse(cold_days > 0, cold_days, "")),
    size = 2.4,
    colour = "#1a1a1a"
  ) +
  scale_fill_gradient(
    name = "Cold days",
    low = "#f7fbff",
    high = "#08519c",
    limits = c(0, max(temp$cold_days))
  ) +
  labs(
    title = "Official cold days by month, Hong Kong Observatory Headquarters, 2013-2023",
    subtitle = "141 of 145 cold days fell in December-February (December 40, January 54, February 47; March 4).",
    x = NULL,
    y = NULL,
    caption = paste(
      "REAL public HKO daily flags (Tmin <= 12 C) rolled to calendar months.",
      "After calendar-month indicators, remaining cold-day variation is between-year winter,",
      "not summer versus winter. Environmental descriptors only; not hospitalisation results."
    )
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 12),
    plot.subtitle = element_text(size = 9.5),
    plot.caption = element_text(size = 8, colour = "#555555", hjust = 0),
    panel.grid = element_blank(),
    legend.position = "right"
  )

ggsave(
  "figures/live_identification/figA_cold_days_year_month.pdf",
  p_a, width = 8.2, height = 5.4, units = "in", device = pdf_device
)
ggsave(
  "figures/live_identification/figA_cold_days_year_month.png",
  p_a, width = 8.2, height = 5.4, units = "in", dpi = 300, bg = "white"
)

# ---------------------------------------------------------------------------
# Figure B. First-event depletion (HA_APPROVED_AGGREGATE annual totals)
# ---------------------------------------------------------------------------
ann <- readr::read_csv(
  file.path(root, "outputs/tables/cvd_descriptive_annual_totals.csv"),
  show_col_types = FALSE
)
stopifnot(ann$total_events[ann$outcome == "chd" & ann$year == 2013] == 23830)
stopifnot(ann$total_events[ann$outcome == "chd" & ann$year == 2023] == 12323)

pop <- ann |>
  filter(outcome == "chd") |>
  transmute(
    year,
    series = "C&SD population aged 35+ (index, 2013 = 1)",
    value = mean_population / mean_population[year == 2013]
  )

events_idx <- ann |>
  group_by(outcome) |>
  mutate(value = total_events / total_events[year == 2013]) |>
  ungroup() |>
  transmute(
    year,
    series = recode(
      outcome,
      chd = "CHD first hospitalisations (index, 2013 = 1)",
      hf = "HF first hospitalisations (index, 2013 = 1)"
    ),
    value
  )

idx <- bind_rows(events_idx, pop) |>
  mutate(
    series = factor(
      series,
      levels = c(
        "CHD first hospitalisations (index, 2013 = 1)",
        "HF first hospitalisations (index, 2013 = 1)",
        "C&SD population aged 35+ (index, 2013 = 1)"
      )
    )
  )

p_b <- ggplot(idx, aes(x = year, y = value, colour = series, linetype = series)) +
  geom_hline(yintercept = 1, colour = "#bbbbbb", linewidth = 0.3) +
  geom_line(linewidth = 0.85) +
  geom_point(size = 2) +
  scale_colour_manual(
    values = c(
      "CHD first hospitalisations (index, 2013 = 1)" = "#9C2C2C",
      "HF first hospitalisations (index, 2013 = 1)" = "#2C6E9C",
      "C&SD population aged 35+ (index, 2013 = 1)" = "#555555"
    )
  ) +
  scale_linetype_manual(
    values = c(
      "CHD first hospitalisations (index, 2013 = 1)" = "solid",
      "HF first hospitalisations (index, 2013 = 1)" = "solid",
      "C&SD population aged 35+ (index, 2013 = 1)" = "dashed"
    )
  ) +
  scale_x_continuous(breaks = 2013:2023) +
  scale_y_continuous(labels = scales::label_number(accuracy = 0.1)) +
  labs(
    title = "First-event hospitalisation totals fell while the general population aged 35+ rose",
    subtitle = "CHD 23,830 to 12,323; HF 4,336 to 2,296 (2013 to 2023). 2020 is a further trough.",
    x = NULL,
    y = "Index (2013 = 1)",
    colour = NULL,
    linetype = NULL,
    caption = paste(
      "HA_APPROVED_AGGREGATE annual first-hospitalisation totals among the T2D/HTN cohort;",
      "C&SD Table 110-01001 interpolated mid-year population aged 35+ (ecological, not the cohort still at risk).",
      "The decline is the expected shape of a first-event construction in a 2013-2023 diagnosis window,",
      "plus pandemic care-seeking. Without still-at-risk person-time these are not incidence rates."
    )
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 12),
    plot.subtitle = element_text(size = 9.5),
    plot.caption = element_text(size = 8, colour = "#555555", hjust = 0),
    legend.position = "bottom",
    legend.direction = "vertical",
    panel.grid.minor = element_blank(),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )

ggsave(
  "figures/live_identification/figB_first_event_depletion.pdf",
  p_b, width = 8.0, height = 5.6, units = "in", device = pdf_device
)
ggsave(
  "figures/live_identification/figB_first_event_depletion.png",
  p_b, width = 8.0, height = 5.6, units = "in", dpi = 300, bg = "white"
)

# ---------------------------------------------------------------------------
# Figure C. Residual ACF (from already-fitted continuity models)
# ---------------------------------------------------------------------------
chd_acf <- readr::read_csv(
  file.path(root, "outputs/tables/chd_pathway_residual_acf.csv"),
  show_col_types = FALSE
)
hf_acf <- readr::read_csv(
  file.path(root, "outputs/tables/hf_pathway_residual_acf.csv"),
  show_col_types = FALSE
)

lead <- bind_rows(
  chd_acf |> filter(pathway_id == "P04A") |> mutate(series = "CHD, hot nights"),
  hf_acf |> filter(pathway_id == "P04B") |> mutate(series = "HF, cold days")
)

band <- 1.96 / sqrt(132)

p_c <- ggplot(lead, aes(x = lag, y = acf, colour = series)) +
  geom_hline(yintercept = 0, colour = "#888888") +
  geom_hline(yintercept = c(-band, band), linetype = "dashed", colour = "#aaaaaa") +
  geom_col(position = position_dodge(width = 0.7), width = 0.65, alpha = 0.9) +
  scale_colour_manual(
    values = c("CHD, hot nights" = "#9C2C2C", "HF, cold days" = "#2C6E9C")
  ) +
  scale_x_continuous(breaks = 1:12) +
  labs(
    title = "Pearson residual autocorrelation after month and trend",
    subtitle = "Lag-1 autocorrelation 0.508 (CHD hot nights) versus 0.146 (HF cold days). Dashed lines: +/- 1.96 / sqrt(132).",
    x = "Lag (months)",
    y = "Autocorrelation",
    colour = NULL,
    caption = paste(
      "From already-fitted separate negative-binomial continuity models (days-in-month offset).",
      "Not a new regression. Serial dependence is why Newey-West intervals are shown for CHD",
      "alongside model-based intervals, not because an interval excluded 1."
    )
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 12),
    plot.subtitle = element_text(size = 9.5),
    plot.caption = element_text(size = 8, colour = "#555555", hjust = 0),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

ggsave(
  "figures/live_identification/figC_residual_acf.pdf",
  p_c, width = 8.0, height = 4.8, units = "in", device = pdf_device
)
ggsave(
  "figures/live_identification/figC_residual_acf.png",
  p_c, width = 8.0, height = 4.8, units = "in", dpi = 300, bg = "white"
)

message("Wrote figures/live_identification/ fig A-C")
message("Wrote outputs/live_identification/cold_days_by_month_year.csv")
