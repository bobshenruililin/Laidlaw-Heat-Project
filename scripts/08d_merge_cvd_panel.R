#!/usr/bin/env Rscript
# 08d_merge_cvd_panel.R
# Merge normalized CVD aggregates with exposures + population offsets.
# OUTCOME env: chd | hf | stroke

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

outcome <- tolower(Sys.getenv("OUTCOME", unset = "chd"))
agg_path <- file.path(root, "data_processed", paste0(outcome, "_aggregates_normalized.csv"))
exp_path <- file.path(root, "data_processed", "exposures_monthly_2013_2023.csv")
pop_path <- file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv")

if (!file.exists(agg_path)) stop("Run 08c_qc_cvd_aggregates.R first (", agg_path, " missing)")
if (!file.exists(exp_path)) stop("Run 19_build_analysis_exposures.R first")

agg <- utils::read.csv(agg_path, stringsAsFactors = FALSE)
exposures <- utils::read.csv(exp_path, stringsAsFactors = FALSE)
pop <- utils::read.csv(pop_path, stringsAsFactors = FALSE)

has_age <- !all(agg$age_group %in% c("all", "", NA))
has_sex <- !all(agg$sex %in% c("all", "", NA))

if (has_age && has_sex) {
  pop_use <- pop |>
    dplyr::filter(age_group %in% cfg$population$preferred_age_groups) |>
    dplyr::select(month_id, age_group, sex, population)
  panel <- agg |>
    dplyr::left_join(pop_use, by = c("month_id", "age_group", "sex"))
} else {
  pop35 <- pop |>
    dplyr::filter(age_group %in% cfg$population$preferred_age_groups) |>
    dplyr::group_by(month_id) |>
    dplyr::summarise(population = sum(population, na.rm = TRUE), .groups = "drop")
  panel <- agg |>
    dplyr::left_join(pop35, by = "month_id")
}

if ("expected_days" %in% names(exposures)) {
  days <- exposures[, c("month_id", "expected_days")]
  names(days)[2] <- "days_in_month"
} else {
  days <- data.frame(
    month_id = exposures$month_id,
    days_in_month = as.integer(
      format(
        as.Date(paste0(exposures$month_id, "-01")) + 32 -
          as.integer(format(as.Date(paste0(exposures$month_id, "-01")) + 32, "%d")),
        "%d"
      )
    ),
    stringsAsFactors = FALSE
  )
}

panel <- panel |>
  dplyr::left_join(days, by = "month_id") |>
  dplyr::left_join(exposures, by = "month_id", suffix = c("", "_exp")) |>
  dplyr::mutate(
    population = as.numeric(population),
    days_in_month = as.numeric(days_in_month),
    offset_log = log(pmax(population, 1) * pmax(days_in_month, 1)),
    # Secondary offset without population (days only) for sensitivity
    offset_log_days = log(pmax(days_in_month, 1)),
    time_index = match(month_id, sort(unique(month_id))),
    month = as.integer(substr(month_id, 6, 7)),
    year = as.integer(substr(month_id, 1, 4)),
    age_band65 = if (has_age) {
      ifelse(age_group %in% c("65-69", "70-74", "75-79", "80-84", "85+", "65+"), "65plus", "under65")
    } else {
      NA_character_
    },
    analysis_outcome = outcome,
    denominator_note = "CSD_population_35plus_ecological_not_T2D_HTN_cohort"
  )

panel <- panel |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  )

if (anyNA(panel$offset_log)) {
  warning("Some offsets are NA (population/days missing). Check age/sex labels vs C&SD.")
}

out <- file.path(root, "data_processed", paste0(outcome, "_analysis_panel.csv"))
write_csv_safe(panel, out)
if (identical(outcome, "stroke")) {
  write_csv_safe(panel, file.path(root, "data_processed", "stroke_analysis_panel.csv"))
}

message(
  "Merged ", outcome, " analysis panel: ", nrow(panel), " rows; grain age=", has_age,
  " sex=", has_sex, "; status=", paste(unique(panel$data_status), collapse = ","),
  "; events=", sum(panel$n_events, na.rm = TRUE)
)
