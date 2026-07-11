#!/usr/bin/env Rscript
# 14_hko_annual_extremes_figure.R
# Publication-quality three-panel annual thermal-extreme figure (2013–2023).
# Environmental exposure descriptors only — not health-outcome results.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
ensure_packages(c("ggplot2", "dplyr", "tidyr", "readr", "lubridate", "scales"))

climate <- readr::read_csv(
  file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
  show_col_types = FALSE
)

stopifnot("month_date" %in% names(climate))
stopifnot(all(c("hot_nights", "very_hot_days", "cold_days") %in% names(climate)))
stopifnot(nrow(climate) == 132L)
stopifnot(!any(duplicated(climate$month_id)))
stopifnot(all(climate$station == "HKO"))
assert_month_id(climate$month_id)

climate <- climate |>
  mutate(
    month_date = as.Date(month_date),
    year = lubridate::year(month_date)
  )

# Monthly counts must lie within days in month
stopifnot(all(climate$hot_nights >= 0 & climate$hot_nights <= climate$expected_days))
stopifnot(all(climate$very_hot_days >= 0 & climate$very_hot_days <= climate$expected_days))
stopifnot(all(climate$cold_days >= 0 & climate$cold_days <= climate$expected_days))
stopifnot(!any(is.na(climate$hot_nights)))
stopifnot(!any(is.na(climate$very_hot_days)))
stopifnot(!any(is.na(climate$cold_days)))

annual_extremes <- climate |>
  filter(year >= 2013, year <= 2023) |>
  group_by(year) |>
  summarise(
    hot_nights = sum(hot_nights, na.rm = TRUE),
    very_hot_days = sum(very_hot_days, na.rm = TRUE),
    cold_days = sum(cold_days, na.rm = TRUE),
    extremely_hot_days = sum(extremely_hot_days, na.rm = TRUE),
    n_months = n_distinct(month_date),
    .groups = "drop"
  )

stopifnot(all(annual_extremes$n_months == 12))
stopifnot(nrow(annual_extremes) == 11L)

# Shared official totals live in utils::hko_official_annual_extremes()
official <- hko_official_annual_extremes() |>
  mutate(official_source = sprintf("HKO The Year's Weather – %d", year))

v <- validate_hko_annual_extremes(annual_extremes)
if (!v$all_ok) {
  warning("HKO validation mismatches detected — see validation table.")
} else {
  message(sprintf(
    "All validated annual totals MATCH official HKO Year's Weather summaries (%d/%d).",
    v$n_metric_checks_ok, v$n_metric_checks
  ))
}

validation_long <- annual_extremes |>
  select(year, hot_nights, very_hot_days, cold_days) |>
  pivot_longer(
    cols = c(hot_nights, very_hot_days, cold_days),
    names_to = "metric",
    values_to = "pipeline_total"
  ) |>
  left_join(
    official |>
      pivot_longer(
        cols = c(hot_nights_official, very_hot_days_official, cold_days_official),
        names_to = "metric_raw",
        values_to = "official_hko_total"
      ) |>
      mutate(
        metric = dplyr::recode(
          metric_raw,
          hot_nights_official = "hot_nights",
          very_hot_days_official = "very_hot_days",
          cold_days_official = "cold_days"
        )
      ) |>
      select(year, metric, official_hko_total, official_source),
    by = c("year", "metric")
  ) |>
  mutate(
    difference = pipeline_total - official_hko_total,
    validation_status = ifelse(
      is.na(official_hko_total),
      "NOT YET VERIFIED",
      ifelse(difference == 0, "MATCH", "MISMATCH")
    ),
    notes = "Station = HKO Headquarters; thresholds Tmin>=28, Tmax>=33, Tmin<=12"
  )

annual_long <- annual_extremes |>
  select(year, hot_nights, very_hot_days, cold_days) |>
  pivot_longer(
    cols = c(hot_nights, very_hot_days, cold_days),
    names_to = "metric",
    values_to = "days"
  ) |>
  mutate(
    metric = factor(
      metric,
      levels = c("hot_nights", "very_hot_days", "cold_days"),
      labels = c(
        "Hot nights (daily minimum ≥ 28°C)",
        "Very hot days (daily maximum ≥ 33°C)",
        "Cold days (daily minimum ≤ 12°C)"
      )
    )
  )

metric_colours <- c(
  "Hot nights (daily minimum ≥ 28°C)" = "#9C2C2C",
  "Very hot days (daily maximum ≥ 33°C)" = "#D97904",
  "Cold days (daily minimum ≤ 12°C)" = "#2C6E9C"
)

p <- ggplot(
  annual_long,
  aes(x = year, y = days, group = metric, colour = metric)
) +
  geom_line(linewidth = 0.8) +
  geom_point(size = 2.2) +
  facet_wrap(~ metric, ncol = 1, scales = "free_y") +
  scale_colour_manual(values = metric_colours, guide = "none") +
  scale_x_continuous(
    breaks = 2013:2023,
    labels = as.character(2013:2023),
    expand = expansion(mult = c(0.015, 0.03))
  ) +
  scale_y_continuous(
    breaks = pretty_breaks(n = 5),
    expand = expansion(mult = c(0, 0.10))
  ) +
  labs(
    title = "Annual thermal extremes in Hong Kong, 2013–2023",
    subtitle = paste(
      "Counts derived from daily Hong Kong Observatory Headquarters observations",
      "using official temperature thresholds"
    ),
    x = NULL,
    y = "Number of days or nights",
    caption = paste(
      "Source: Hong Kong Observatory.",
      "These are environmental exposure descriptors,",
      "not cardiovascular or other health-outcome results."
    )
  ) +
  theme_minimal(base_size = 10.5) +
  theme(
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(size = 10),
    strip.text = element_text(face = "bold", hjust = 0, colour = "#222222"),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    axis.text.x = element_text(angle = 45, hjust = 1),
    plot.caption = element_text(size = 8, colour = "#555555", hjust = 0),
    plot.margin = margin(8, 10, 8, 8)
  )

dir.create("figures", showWarnings = FALSE, recursive = TRUE)
dir.create("outputs/tables", showWarnings = FALSE, recursive = TRUE)

# Prefer cairo_pdf when available; fall back to pdf()
pdf_device <- if (isTRUE(capabilities("cairo"))) cairo_pdf else "pdf"

ggsave(
  "figures/hko_annual_extremes_2013_2023.pdf",
  p,
  width = 7.2,
  height = 7.4,
  units = "in",
  device = pdf_device
)

ggsave(
  "figures/hko_annual_extremes_2013_2023.png",
  p,
  width = 7.2,
  height = 7.4,
  units = "in",
  dpi = 320,
  bg = "white"
)

write_csv(annual_extremes, "outputs/tables/hko_annual_extremes_2013_2023.csv")
write_csv(validation_long, "outputs/tables/hko_annual_extremes_validation.csv")

message("Wrote figures/hko_annual_extremes_2013_2023.pdf/.png")
message("Wrote outputs/tables/hko_annual_extremes_2013_2023.csv")
message("Wrote outputs/tables/hko_annual_extremes_validation.csv")
print(validation_long |> count(validation_status))
