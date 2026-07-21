#!/usr/bin/env Rscript
# 07b_simulate_stroke_aggregates.R
# SYNTHETIC stroke aggregates for pathway dry-run (territory-month + age×sex grains).
# Explicitly NOT diagnosis-stratified AMI/IS/HS — matches post-meeting reality.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr"))

set.seed(cfg$synthetic$seed %||% cfg$project$seed)

exp_path <- file.path(root, "data_processed", "exposures_monthly_2013_2023.csv")
if (!file.exists(exp_path)) {
  message("Exposures missing; running 19_build_analysis_exposures.R ...")
  rc <- system2("Rscript", file.path(root, "scripts", "19_build_analysis_exposures.R"))
  if (rc != 0) stop("Failed to build exposures")
}

exposures <- utils::read.csv(exp_path, stringsAsFactors = FALSE)
pop <- utils::read.csv(
  file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"),
  stringsAsFactors = FALSE
)

# Territory-month population 35+
pop35 <- pop |>
  dplyr::filter(age_group %in% cfg$population$preferred_age_groups) |>
  dplyr::group_by(month_id) |>
  dplyr::summarise(population = sum(population, na.rm = TRUE), .groups = "drop")

days <- exposures |>
  dplyr::transmute(
    month_id,
    days_in_month = as.integer(expected_days)
  )

# Synthetic rate model: cold and heat both contribute modestly + seasonality
panel_t <- exposures |>
  dplyr::left_join(pop35, by = "month_id") |>
  dplyr::left_join(days, by = "month_id") |>
  dplyr::mutate(
    person_time = population * days_in_month,
    # baseline ~ 8 per 100k person-months (synthetic scale)
    log_rate = log(8e-5) +
      0.012 * (24 - mean_temp) +                 # colder → higher
      0.008 * pmax(mean_tmax - 30, 0) +          # hot tail
      0.015 * (cold_days / 5) +
      0.010 * (hot_nights / 5) +
      0.006 * (days_in_2d3n_window / 5) +
      0.05 * sin(2 * pi * (month - 1) / 12) +
      dplyr::case_when(
        covid_phase == "early_covid" ~ -0.18,
        covid_phase == "fifth_wave" ~ -0.30,
        covid_phase == "late_2022" ~ -0.10,
        TRUE ~ 0
      ),
    mu = person_time * exp(log_rate),
    n_events = stats::rnbinom(dplyr::n(), mu = mu, size = 20),
    age_group = "all",
    sex = "all",
    stroke_type = "stroke_all",
    data_status = "SYNTHETIC",
    notes = "SYNTHETIC territory-month stroke aggregates for pathway dry-run only"
  )

territory <- panel_t |>
  dplyr::select(
    month_id, age_group, sex, stroke_type, n_events, data_status, notes
  )

# Age×sex grain: distribute territory counts by age-sex population weights × age risk
age_rr <- c(
  `35-39` = 0.25, `40-44` = 0.35, `45-49` = 0.50, `50-54` = 0.75,
  `55-59` = 1.10, `60-64` = 1.60, `65-69` = 2.20, `70-74` = 3.00,
  `75-79` = 4.00, `80-84` = 5.20, `85+` = 6.50
)
sex_rr <- c(Female = 0.9, Male = 1.1)

age_sex <- tidyr::expand_grid(
  month_id = exposures$month_id,
  age_group = cfg$population$preferred_age_groups,
  sex = cfg$sexes
) |>
  dplyr::left_join(pop, by = c("month_id", "age_group", "sex")) |>
  dplyr::left_join(territory[, c("month_id", "n_events")], by = "month_id") |>
  dplyr::mutate(
    w = population * age_rr[age_group] * sex_rr[sex],
    stroke_type = "stroke_all",
    data_status = "SYNTHETIC",
    notes = "SYNTHETIC age-sex stroke aggregates (allocated from territory month)"
  ) |>
  dplyr::group_by(month_id) |>
  dplyr::mutate(
    w = w / sum(w, na.rm = TRUE),
    n_events = as.integer(round(n_events * w))
  ) |>
  dplyr::ungroup() |>
  dplyr::select(month_id, age_group, sex, stroke_type, n_events, data_status, notes)

out_dir <- file.path(root, "data_processed", "samples")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
# Also stage under ha_secure_placeholder as MOCK for schema tests (still SYNTHETIC)
ha_dir <- file.path(root, "data_raw", "ha_secure_placeholder")
dir.create(ha_dir, recursive = TRUE, showWarnings = FALSE)

write_csv_safe(territory, file.path(out_dir, "SYNTHETIC_stroke_territory_month.csv"))
write_csv_safe(age_sex, file.path(out_dir, "SYNTHETIC_stroke_age_sex_month.csv"))

# Dev default input for pathway pipeline (explicitly synthetic)
write_csv_safe(
  age_sex,
  file.path(out_dir, "SYNTHETIC_ha_stroke_aggregates.csv")
)

message(
  "Wrote SYNTHETIC stroke aggregates. Territory months=", nrow(territory),
  " age-sex rows=", nrow(age_sex),
  " mean monthly events≈", round(mean(territory$n_events), 1)
)
