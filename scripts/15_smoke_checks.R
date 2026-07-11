#!/usr/bin/env Rscript
# 15_smoke_checks.R — fast integrity checks after a pipeline run

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

failures <- character(0)
ok <- function(msg) message("OK  ", msg)
fail <- function(msg) {
  message("FAIL  ", msg)
  failures <<- c(failures, msg)
}

# Config
if (!file.exists("config.yml")) fail("config.yml missing") else ok("config.yml present")
mode <- cfg$pipeline$mode %||% "dev"
ok(paste("pipeline.mode =", mode))

# Weather
clim_path <- file.path(root, "data_processed", "climate_monthly_2013_2023.csv")
if (!file.exists(clim_path)) {
  fail("climate_monthly_2013_2023.csv missing")
} else {
  clim <- utils::read.csv(clim_path, stringsAsFactors = FALSE)
  if (nrow(clim) != 132L) fail(paste("climate rows != 132:", nrow(clim))) else ok("climate 132 months")
  assert_month_id(clim$month_id)
  annual <- clim |>
    dplyr::group_by(year) |>
    dplyr::summarise(
      hot_nights = sum(hot_nights, na.rm = TRUE),
      very_hot_days = sum(very_hot_days, na.rm = TRUE),
      cold_days = sum(cold_days, na.rm = TRUE),
      .groups = "drop"
    )
  v <- validate_hko_annual_extremes(annual)
  if (!v$all_ok) {
    fail(sprintf("HKO validation %d/%d metric checks failed",
                 v$n_metric_checks - v$n_metric_checks_ok, v$n_metric_checks))
  } else {
    ok(sprintf("HKO annual extremes %d/%d MATCH", v$n_metric_checks_ok, v$n_metric_checks))
  }
}

# Population
pop_path <- file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv")
if (!file.exists(pop_path)) {
  fail("population_monthly missing")
} else {
  pop <- utils::read.csv(pop_path, stringsAsFactors = FALSE)
  st <- unique(pop$data_status)
  if (any(grepl("CSD_IMPORTED", st))) {
    ok(paste("population status:", paste(st, collapse = ",")))
    annual_path <- file.path(root, "data_raw", "csd_population",
                             "csd_population_age_sex_annual_normalized.csv")
    if (file.exists(annual_path)) {
      ann <- utils::read.csv(annual_path, stringsAsFactors = FALSE)
      p6569 <- ann |>
        dplyr::filter(year == 2013, age_group == "65-69") |>
        dplyr::summarise(p = sum(population)) |>
        dplyr::pull(p)
      if (length(p6569) == 1 && abs(p6569 - 295100) < 1) {
        ok(sprintf("mid-2013 ages 65-69 annual = %.0f (C&SD 295.1 thousand)", p6569))
      } else {
        fail(sprintf("mid-2013 ages 65-69 annual unexpected: %s", paste(p6569, collapse = ",")))
      }
    } else {
      # Fallback: monthly June should be near mid-year
      p6569 <- pop |>
        dplyr::filter(year == 2013, month == 6, age_group == "65-69") |>
        dplyr::summarise(p = sum(population)) |>
        dplyr::pull(p)
      if (length(p6569) == 1 && p6569 > 250000 && p6569 < 350000) {
        ok(sprintf("mid-2013 ages 65-69 monthly ≈ %.0f", p6569))
      } else {
        fail(sprintf("mid-2013 ages 65-69 unexpected: %s", paste(p6569, collapse = ",")))
      }
    }
  } else {
    fail(paste("population not CSD_IMPORTED:", paste(st, collapse = ",")))
  }
}

# Pollution labeled
pol_path <- file.path(root, "data_processed", "pollution_monthly_2013_2023.csv")
if (file.exists(pol_path)) {
  pol <- utils::read.csv(pol_path, stringsAsFactors = FALSE)
  validate_required_columns(pol, c("month_id", "NO2", "O3", "PM25", "PM10"), "pollution")
  ok(paste("pollution status:", paste(unique(pol$data_status), collapse = ",")))
} else {
  fail("pollution_monthly missing")
}

# Schemas present
for (s in c(
  "schemas/ha_monthly_aggregate.schema.json",
  "schemas/epd_monthly.schema.json",
  "schemas/csd_population_annual.schema.json"
)) {
  if (file.exists(s)) ok(s) else fail(paste("missing", s))
}

# Synthetic safety: if synthetic panel exists, must be labeled
syn <- file.path(root, "data_processed", "synthetic_analysis_panel.csv")
if (file.exists(syn)) {
  p <- utils::read.csv(syn, nrows = 5, stringsAsFactors = FALSE)
  if (!"data_status" %in% names(p)) fail("synthetic panel missing data_status")
  else if (!all(p$data_status == "SYNTHETIC")) fail("synthetic panel mislabeled")
  else ok("synthetic panel labeled SYNTHETIC")
}

if (length(failures)) {
  message("\nSmoke checks FAILED:")
  for (f in failures) message(" - ", f)
  quit(status = 1)
}

message("\nAll smoke checks passed.")
