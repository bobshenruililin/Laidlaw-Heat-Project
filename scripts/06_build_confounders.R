#!/usr/bin/env Rscript
# 06_build_confounders.R — COVID phases, holidays scaffold, optional flu placeholder

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

covid_phase <- assign_covid_phase(months$month_id, cfg$covid_phases)

# Approximate Chinese New Year month (lunar; provisional — Bob should replace with exact calendar)
# Common CNY months 2013-2023 (Feb except occasional Jan):
cny_month_ids <- c(
  "2013-02", "2014-01", "2015-02", "2016-02", "2017-01",
  "2018-02", "2019-02", "2020-01", "2021-02", "2022-02", "2023-01"
)

# Public holiday day counts: provisional monthly scaffold (not official).
# Replace with official HK holiday calendar before substantive analysis.
set.seed(cfg$project$seed)
holiday_days <- ifelse(months$month %in% c(1, 2, 4, 5, 7, 10, 12),
                       sample(c(1, 2, 3), size = nrow(months), replace = TRUE),
                       0L)
# Boost CNY months
holiday_days[months$month_id %in% cny_month_ids] <- pmax(holiday_days[months$month_id %in% cny_month_ids], 3L)

confounders <- months |>
  dplyr::mutate(
    covid_phase = covid_phase,
    chinese_new_year_month = as.integer(month_id %in% cny_month_ids),
    public_holiday_days = as.integer(holiday_days),
    flu_indicator = NA_real_,  # optional; fill from CHP later
    typhoon_signal_days = NA_real_,
    holiday_data_status = "PROVISIONAL_HOLIDAY_SCAFFOLD",
    flu_data_status = "NOT_YET_LOADED",
    notes = "Replace holiday/flu/typhoon fields with official calendars before final models"
  )

# Optional flu import — prefer CHP Flu Express monthly file
flu_dir <- file.path(root, "data_raw", "chp_flu")
flu_candidates <- c(
  file.path(flu_dir, "flu_for_confounders.csv"),
  file.path(flu_dir, "flu_monthly_2013_2023.csv")
)
flu_files <- flu_candidates[file.exists(flu_candidates)]
if (!length(flu_files)) {
  flu_files <- list.files(flu_dir, pattern = "\\.csv$", full.names = TRUE)
  flu_files <- flu_files[!grepl("flux_data", basename(flu_files))]
}
if (length(flu_files)) {
  flu <- utils::read.csv(flu_files[1], stringsAsFactors = FALSE)
  names(flu) <- tolower(names(flu))
  if (all(c("month_id", "flu_indicator") %in% names(flu))) {
    confounders$flu_indicator <- NULL
    confounders <- dplyr::left_join(confounders, flu[, c("month_id", "flu_indicator")], by = "month_id")
    confounders$flu_data_status <- "CHP_FLU_EXPRESS_MONTHLY"
    confounders$notes <- paste(
      confounders$notes,
      "| flu from CHP Flu Express AandB_proportion monthly mean"
    )
  }
}

write_csv_safe(confounders, file.path(root, "data_processed", "confounders_monthly_2013_2023.csv"))
message(
  "Confounders build complete. flu_status=",
  paste(unique(confounders$flu_data_status), collapse = ",")
)
