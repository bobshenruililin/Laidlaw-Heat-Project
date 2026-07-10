#!/usr/bin/env Rscript
# 05_build_population_denominators.R
#
# C&SD Table 110-01002 API requires an interactive encrypted `param` string.
# This script:
# 1) imports a user-supplied CSV if present in data_raw/csd_population/;
# 2) otherwise builds a clearly labeled SYNTHETIC_DENOMINATOR panel shaped like
#    the expected age-sex structure, scaled to published broad 65+ growth patterns,
#    for pipeline testing only.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr", "readr"))

pop_dir <- file.path(root, cfg$population$raw_dir)
dir.create(pop_dir, recursive = TRUE, showWarnings = FALSE)

writeLines(c(
  "# C&SD population denominators — import instructions",
  "",
  "Preferred source: Census and Statistics Department Table 110-01002",
  "(Population by sex and age), or 110-01001 / single-year age tables that can",
  "construct 65–69 and 70–74 separately.",
  "",
  "## How to obtain",
  "",
  "1. Open https://www.censtatd.gov.hk/en/web_table.html?id=110-01002",
  "2. Customise to mid-year (or half-yearly) population by sex and age for 2012–2024.",
  "3. Use the page API button to copy the GET URL (includes encrypted `param`), OR download CSV/XLSX.",
  "4. Save into this folder as `csd_population_age_sex.csv` with columns such as:",
  "   year, sex, age, population   OR   year, sex, age_group, population",
  "5. Re-run this script.",
  "",
  "Alternative table excluding foreign domestic helpers: 110-01002A — useful as sensitivity",
  "if HA residency definitions suggest FDH exclusion.",
  "",
  "API docs: https://www.censtatd.gov.hk/datagovhk/WT_data_dict_en.pdf"
), file.path(pop_dir, "README_manual_download.md"))

age_groups <- cfg$population$preferred_age_groups
sexes <- cfg$sexes

candidate <- list.files(pop_dir, pattern = "csd_population.*\\.(csv|CSV)$", full.names = TRUE)
candidate <- candidate[!grepl("SYNTHETIC|PLACEHOLDER", basename(candidate), ignore.case = TRUE)]

months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

assign_age_group <- function(age) {
  age <- as.integer(age)
  dplyr::case_when(
    age >= 35 & age <= 39 ~ "35-39",
    age >= 40 & age <= 44 ~ "40-44",
    age >= 45 & age <= 49 ~ "45-49",
    age >= 50 & age <= 54 ~ "50-54",
    age >= 55 & age <= 59 ~ "55-59",
    age >= 60 & age <= 64 ~ "60-64",
    age >= 65 & age <= 69 ~ "65-69",
    age >= 70 & age <= 74 ~ "70-74",
    age >= 75 & age <= 79 ~ "75-79",
    age >= 80 & age <= 84 ~ "80-84",
    age >= 85 ~ "85+",
    TRUE ~ NA_character_
  )
}

interpolate_monthly <- function(annual_df) {
  # annual_df: year, age_group, sex, population (mid-year)
  grid <- tidyr::expand_grid(
    month_id = months$month_id,
    age_group = age_groups,
    sex = sexes
  ) |>
    dplyr::left_join(months[, c("month_id", "month_date", "year", "month")], by = "month_id")

  # For each age-sex, interpolate between mid-year points
  pieces <- lapply(split(annual_df, list(annual_df$age_group, annual_df$sex), drop = TRUE), function(g) {
    g <- dplyr::arrange(g, year)
    # mid-year dates
    g$mid_date <- as.Date(sprintf("%04d-06-30", g$year))
    target <- grid[grid$age_group == g$age_group[1] & grid$sex == g$sex[1], , drop = FALSE]
    # month midpoint
    target$month_mid <- target$month_date + floor(as.integer(format(target$month_date + 32 - as.integer(format(target$month_date + 32, "%d")), "%d")) / 2)
    # simpler: 15th of month
    target$month_mid <- as.Date(format(target$month_date, "%Y-%m-15"))
    target$population <- approx(
      x = as.numeric(g$mid_date),
      y = g$population,
      xout = as.numeric(target$month_mid),
      rule = 2
    )$y
    target
  })
  dplyr::bind_rows(pieces)
}

if (length(candidate)) {
  message("Importing C&SD file: ", basename(candidate[1]))
  raw <- utils::read.csv(candidate[1], stringsAsFactors = FALSE)
  names(raw) <- tolower(names(raw))
  if ("age" %in% names(raw) && !"age_group" %in% names(raw)) {
    raw$age_group <- assign_age_group(raw$age)
    raw <- raw |>
      dplyr::filter(!is.na(age_group)) |>
      dplyr::group_by(year, sex, age_group) |>
      dplyr::summarise(population = sum(as.numeric(population), na.rm = TRUE), .groups = "drop")
  } else {
    raw <- raw |>
      dplyr::mutate(
        age_group = as.character(age_group),
        population = as.numeric(population),
        year = as.integer(year),
        sex = as.character(sex)
      )
  }
  # Harmonize sex labels
  raw$sex <- ifelse(tolower(substr(raw$sex, 1, 1)) == "f", "Female",
                    ifelse(tolower(substr(raw$sex, 1, 1)) == "m", "Male", raw$sex))
  annual <- raw |>
    dplyr::filter(age_group %in% age_groups) |>
    dplyr::select(year, sex, age_group, population)
  pop_monthly <- interpolate_monthly(annual) |>
    dplyr::mutate(data_status = "CSD_IMPORTED", source_table = cfg$population$source_table)
} else {
  message("No C&SD CSV found. Building SYNTHETIC_DENOMINATOR for pipeline testing.")
  message("Replace with real C&SD extract before substantive rate analyses.")
  set.seed(cfg$project$seed)

  # Rough age-structure scaffold (not official counts). Levels chosen only to
  # produce plausible relative sizes and aging growth for code tests.
  base_pop <- c(
    `35-39` = 520000, `40-44` = 530000, `45-49` = 540000, `50-54` = 560000,
    `55-59` = 550000, `60-64` = 480000, `65-69` = 360000, `70-74` = 250000,
    `75-79` = 180000, `80-84` = 120000, `85+` = 110000
  )
  # Stronger growth in older bands over 2013-2023
  growth <- c(
    `35-39` = -0.05, `40-44` = -0.02, `45-49` = 0.00, `50-54` = 0.02,
    `55-59` = 0.05, `60-64` = 0.12, `65-69` = 0.35, `70-74` = 0.45,
    `75-79` = 0.30, `80-84` = 0.28, `85+` = 0.40
  )

  years <- 2012:2024
  annual_rows <- list()
  for (ag in age_groups) {
    for (sx in sexes) {
      sex_share <- if (sx == "Female") 0.52 else 0.48
      for (i in seq_along(years)) {
        y <- years[i]
        # linear growth from 2013 baseline across decade
        frac <- (y - 2013) / 10
        pop <- base_pop[[ag]] * sex_share * (1 + growth[[ag]] * frac)
        pop <- pop * rnorm(1, 1, 0.002)
        annual_rows[[length(annual_rows) + 1]] <- data.frame(
          year = y, sex = sx, age_group = ag, population = as.numeric(pop),
          stringsAsFactors = FALSE
        )
      }
    }
  }
  annual <- dplyr::bind_rows(annual_rows)
  write_csv_safe(annual, file.path(pop_dir, "csd_population_age_sex_SYNTHETIC_ANNUAL.csv"))
  pop_monthly <- interpolate_monthly(annual) |>
    dplyr::mutate(
      data_status = "SYNTHETIC_DENOMINATOR",
      source_table = "SYNTHETIC_NOT_CSD",
      notes = "Pipeline scaffold only; replace with C&SD Table 110-01002"
    )
}

pop_monthly <- pop_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  ) |>
  dplyr::select(month_id, year, month, month_date, age_group, sex, population, dplyr::any_of(c("data_status", "source_table", "notes")))

# Checks
stopifnot(!any(duplicated(pop_monthly[, c("month_id", "age_group", "sex")])))
stopifnot(!any(is.na(pop_monthly$population)))
stopifnot(all(pop_monthly$population > 0))

write_csv_safe(pop_monthly, file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"))

# Aging summary table
aging <- pop_monthly |>
  dplyr::filter(month == 6) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop")
write_csv_safe(aging, file.path(root, "outputs", "tables", "population_midyear_by_age_group.csv"))

message("Population denominator build complete. Rows: ", nrow(pop_monthly))
if (any(grepl("SYNTHETIC", pop_monthly$data_status %||% ""))) {
  message("WARNING: synthetic denominators in use.")
}
