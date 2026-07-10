#!/usr/bin/env Rscript
# 07_simulate_ha_outcomes.R
# Creates an explicitly SYNTHETIC HA-like outcome panel for pipeline testing only.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr"))

set.seed(cfg$synthetic$seed %||% cfg$project$seed)

climate <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"),
                           stringsAsFactors = FALSE)
pop <- utils::read.csv(file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"),
                       stringsAsFactors = FALSE)
conf <- utils::read.csv(file.path(root, "data_processed", "confounders_monthly_2013_2023.csv"),
                        stringsAsFactors = FALSE)
months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

age_groups <- cfg$population$preferred_age_groups
sexes <- cfg$sexes
dx <- cfg$diagnosis_groups

# Relative baseline rates per 100,000 person-months (synthetic)
age_rr <- c(
  `35-39` = 0.25, `40-44` = 0.35, `45-49` = 0.50, `50-54` = 0.75,
  `55-59` = 1.10, `60-64` = 1.60, `65-69` = 2.20, `70-74` = 3.00,
  `75-79` = 4.00, `80-84` = 5.20, `85+` = 6.50
)
dx_rr <- c(AMI = 1.0, ischemic_stroke = 1.3, hemorrhagic_stroke = 0.45)
sex_rr <- c(Female = 0.85, Male = 1.15)

panel <- tidyr::expand_grid(
  month_id = climate$month_id,
  age_group = age_groups,
  sex = sexes,
  diagnosis_group = dx
) |>
  dplyr::left_join(climate, by = "month_id") |>
  dplyr::left_join(pop, by = c("month_id", "age_group", "sex"), suffix = c("", "_pop")) |>
  dplyr::left_join(conf[, c("month_id", "covid_phase", "chinese_new_year_month", "public_holiday_days")],
                   by = "month_id") |>
  dplyr::left_join(months[, c("month_id", "days_in_month", "time_index", "year", "month", "month_date")],
                   by = "month_id", suffix = c("", "_m"))

# Prefer month grid calendar fields when duplicates exist
if ("year_m" %in% names(panel)) panel$year <- panel$year_m
if ("month_m" %in% names(panel)) panel$month <- panel$month_m
if ("month_date_m" %in% names(panel)) panel$month_date <- panel$month_date_m
if (!"days_in_month" %in% names(panel) && "expected_days" %in% names(panel)) {
  panel$days_in_month <- panel$expected_days
}

# COVID utilization multipliers (synthetic disruption)
covid_mult <- c(
  pre_covid = 1.00,
  early_covid = 0.82,
  fifth_wave = 0.70,
  late_2022 = 0.88,
  post_reopening = 0.97
)

# Synthetic log-rate model with cold effect > heat effect (historically plausible scaffold)
# NOT a claim about real HA associations.
panel <- panel |>
  dplyr::mutate(
    base_rate = 8e-5 * age_rr[age_group] * dx_rr[diagnosis_group] * sex_rr[sex],
    # winter seasonality residual beyond cold_days
    season = 0.08 * sin(2 * pi * (month - 1) / 12 + pi),
    # cold increases admissions; modest hot-night effect among oldest
    heat_age = dplyr::case_when(
      age_group %in% c("75-79", "80-84", "85+") ~ 0.010,
      age_group %in% c("65-69", "70-74") ~ 0.006,
      TRUE ~ 0.002
    ),
    log_mu = log(pmax(population, 1) * days_in_month * base_rate) +
      season +
      0.035 * cold_days +
      heat_age * hot_nights +
      0.004 * very_hot_days +
      log(covid_mult[covid_phase]) -
      0.04 * chinese_new_year_month,
    mu = exp(log_mu),
    # Negative-binomial-like noise via Poisson-gamma mixture
    n_events = rnbinom(dplyr::n(), size = 12, mu = mu),
    n_patients = pmax(1L, as.integer(round(n_events * runif(dplyr::n(), 0.85, 1.0)))),
    n_deaths_in_hospital = rbinom(dplyr::n(), size = n_events, prob = 0.04),
    bed_days = as.integer(round(n_events * rnorm(dplyr::n(), mean = 6, sd = 1.2))),
    care_setting = "inpatient",
    coding_system = "PROVISIONAL_ICD9CM_ASSUMED",
    suppression_flag = 0L,
    data_status = cfg$synthetic$label %||% "SYNTHETIC",
    synthetic_seed = as.integer(cfg$synthetic$seed %||% cfg$project$seed),
    notes = "SYNTHETIC outcomes for pipeline testing only; not HA data"
  )

stop_if_not_synthetic(panel)
stopifnot(!any(duplicated(panel[, c("month_id", "age_group", "sex", "diagnosis_group", "care_setting")])))

out_cols <- c(
  "month_id", "year", "month", "month_date", "time_index",
  "age_group", "sex", "diagnosis_group", "care_setting",
  "n_events", "n_patients", "n_deaths_in_hospital", "bed_days",
  "population", "days_in_month",
  "suppression_flag", "coding_system",
  "data_status", "synthetic_seed", "notes"
)
# time_index may be missing if climate join didn't carry it
if (!"time_index" %in% names(panel)) {
  panel <- panel |>
    dplyr::left_join(
      make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)[, c("month_id", "time_index")],
      by = "month_id"
    )
}
if (!"days_in_month" %in% names(panel)) {
  panel <- panel |>
    dplyr::left_join(
      make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)[, c("month_id", "days_in_month")],
      by = "month_id"
    )
}

write_csv_safe(panel[, intersect(out_cols, names(panel))],
               file.path(root, "data_processed", "synthetic_ha_outcomes.csv"))
message("Synthetic HA outcomes written. Rows: ", nrow(panel))
message("THIS FILE IS SYNTHETIC AND MUST NOT BE REPORTED AS SUBSTANTIVE FINDINGS.")
