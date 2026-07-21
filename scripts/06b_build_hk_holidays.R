#!/usr/bin/env Rscript
# 06b_build_hk_holidays.R
# Replace provisional random holiday scaffold with a deterministic HK holiday-day count
# for 2013–2023 (statutory/general holidays by month). Lunar New Year months retained
# from known calendar months. Not a substitute for an official gazette scrape, but
# removes RNG noise from confounders.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

conf_path <- file.path(root, "data_processed", "confounders_monthly_2013_2023.csv")
conf <- utils::read.csv(conf_path, stringsAsFactors = FALSE)

# Approximate statutory holiday day counts by calendar month (HK), excluding CNY boost.
# Typical pattern: Jan (NYD), Apr (Ching Ming/Easter/Labour vicinity), May (Buddha/Labour),
# Jul (HKSAR), Oct (National Day/Chung Yeung), Dec (Christmas). Exact days vary by year.
base_holiday <- c(
  `1` = 1L, `2` = 0L, `3` = 0L, `4` = 2L, `5` = 2L, `6` = 1L,
  `7` = 1L, `8` = 0L, `9` = 0L, `10` = 2L, `11` = 0L, `12` = 2L
)

cny_month_ids <- c(
  "2013-02", "2014-01", "2015-02", "2016-02", "2017-01",
  "2018-02", "2019-02", "2020-01", "2021-02", "2022-02", "2023-01"
)

conf <- conf |>
  dplyr::mutate(
    public_holiday_days = as.integer(base_holiday[as.character(month)]),
    public_holiday_days = ifelse(
      month_id %in% cny_month_ids,
      pmax(public_holiday_days, 3L),
      public_holiday_days
    ),
    chinese_new_year_month = as.integer(month_id %in% cny_month_ids),
    holiday_data_status = "DETERMINISTIC_HK_HOLIDAY_SCAFFOLD_V2",
    notes = "Deterministic monthly holiday-day scaffold (not gazette scrape); CNY months boosted to >=3 days"
  )

write_csv_safe(conf, conf_path)
message("Updated holiday scaffold (deterministic). CNY months=", length(cny_month_ids))
