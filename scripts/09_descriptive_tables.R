#!/usr/bin/env Rscript
# 09_descriptive_tables.R

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr"))

climate <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                           stringsAsFactors = FALSE)
pollution <- utils::read.csv(file.path(root, "data_processed", "pollution_monthly_2013_2023.csv"),
                             stringsAsFactors = FALSE)
pop <- utils::read.csv(file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"),
                       stringsAsFactors = FALSE)
panel <- utils::read.csv(file.path(root, "data_processed", "synthetic_analysis_panel.csv"),
                         stringsAsFactors = FALSE)

out_dir <- file.path(root, "outputs", "tables")

# Weather by period
climate$period <- dplyr::case_when(
  climate$month_id <= "2020-01" ~ "pre_covid",
  climate$month_id <= "2022-12" ~ "covid_2020_2022",
  TRUE ~ "post_reopening_2023"
)

weather_period <- climate |>
  dplyr::group_by(period) |>
  dplyr::summarise(
    n_months = dplyr::n(),
    mean_temp = mean(mean_temp, na.rm = TRUE),
    mean_hot_nights = mean(hot_nights, na.rm = TRUE),
    mean_very_hot_days = mean(very_hot_days, na.rm = TRUE),
    mean_extremely_hot_days = mean(extremely_hot_days, na.rm = TRUE),
    mean_cold_days = mean(cold_days, na.rm = TRUE),
    .groups = "drop"
  )
write_csv_safe(weather_period, file.path(out_dir, "descriptive_weather_by_period.csv"))

# Annual extremes already written in 02; refresh correlation table
cor_vars <- climate[, c("hot_nights", "very_hot_days", "extremely_hot_days",
                        "cold_days", "mean_temp", "mean_tmin", "mean_tmax")]
cors <- as.data.frame(as.table(cor(cor_vars, use = "pairwise.complete.obs")))
names(cors) <- c("var1", "var2", "correlation")
write_csv_safe(cors, file.path(out_dir, "weather_exposure_correlations.csv"))

# Pollution period means
if (all(c("NO2", "O3", "PM25", "PM10") %in% names(pollution))) {
  pollution$period <- dplyr::case_when(
    pollution$month_id <= "2020-01" ~ "pre_covid",
    pollution$month_id <= "2022-12" ~ "covid_2020_2022",
    TRUE ~ "post_reopening_2023"
  )
  pol_period <- pollution |>
    dplyr::group_by(period) |>
    dplyr::summarise(
      NO2 = mean(NO2, na.rm = TRUE),
      O3 = mean(O3, na.rm = TRUE),
      PM25 = mean(PM25, na.rm = TRUE),
      PM10 = mean(PM10, na.rm = TRUE),
      .groups = "drop"
    )
  write_csv_safe(pol_period, file.path(out_dir, "descriptive_pollution_by_period.csv"))
}

# Population aging: 2013 vs 2023 mid-year
pop_aging <- pop |>
  dplyr::filter(year %in% c(2013, 2023), month == 6) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop") |>
  tidyr::pivot_wider(names_from = year, values_from = population, names_prefix = "pop_") |>
  dplyr::mutate(
    abs_change = pop_2023 - pop_2013,
    pct_change = 100 * (pop_2023 - pop_2013) / pop_2013
  )
write_csv_safe(pop_aging, file.path(out_dir, "population_aging_2013_vs_2023.csv"))

# Synthetic outcome crude rates (labeled)
stop_if_not_synthetic(panel)
synth_rates <- panel |>
  dplyr::group_by(age_group, diagnosis_group) |>
  dplyr::summarise(
    events = sum(n_events),
    person_days = sum(population * days_in_month),
    rate_per_100k_person_years = events / person_days * 365.25 * 1e5,
    .groups = "drop"
  ) |>
  dplyr::mutate(data_status = "SYNTHETIC")
write_csv_safe(synth_rates, file.path(out_dir, "SYNTHETIC_crude_rates_by_age_dx.csv"))

# Missingness inventory
miss <- data.frame(
  dataset = c("climate", "pollution", "population", "analysis_panel"),
  n_rows = c(nrow(climate), nrow(pollution), nrow(pop), nrow(panel)),
  n_months = c(dplyr::n_distinct(climate$month_id), dplyr::n_distinct(pollution$month_id),
               dplyr::n_distinct(pop$month_id), dplyr::n_distinct(panel$month_id)),
  stringsAsFactors = FALSE
)
write_csv_safe(miss, file.path(out_dir, "data_inventory_counts.csv"))

message("Descriptive tables written to ", out_dir)
