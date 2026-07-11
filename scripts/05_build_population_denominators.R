#!/usr/bin/env Rscript
# 05_build_population_denominators.R
#
# Imports C&SD mid-year population by sex and age group from the public MDT CSV
# (Table 110-01001), or a user-supplied normalized CSV. Falls back to a clearly
# labeled SYNTHETIC_DENOMINATOR only if no real source is available.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "tidyr", "readr", "digest"))

pop_dir <- file.path(root, cfg$population$raw_dir)
dir.create(pop_dir, recursive = TRUE, showWarnings = FALSE)

write_readme_if_absent(file.path(pop_dir, "README_manual_download.md"), c(
  "# C&SD population denominators",
  "",
  "Preferred automated source: C&SD MDT CSV for Table **110-01001**",
  "(Population by sex and age group), mid-year (`H=1`).",
  "",
  "Direct file (also fetched by this script when missing):",
  "",
  "```text",
  cfg$population$mdt_url %||% "https://www.censtatd.gov.hk/data/MDT_76_110-01001_POP_Raw_K_1dp_per_n.csv",
  "```",
  "",
  "Single-year ages (Table 110-01002) are archived for audit but not required",
  "for the primary 5-year-band analysis.",
  "",
  "## Manual alternative",
  "",
  "1. Open https://www.censtatd.gov.hk/en/web_table.html?id=110-01001",
  "2. Download CSV / use Full Series, or place a normalized file here named",
  "   `csd_population_age_sex.csv` with columns:",
  "   `year, sex, age_group, population` (persons, not thousands).",
  "3. Re-run this script.",
  "",
  "Sensitivity (exclude foreign domestic helpers): Table 110-01001A / 110-01002A.",
  "",
  "API docs: https://www.censtatd.gov.hk/datagovhk/WT_data_dict_en.pdf"
))

age_groups <- cfg$population$preferred_age_groups
sexes <- cfg$sexes
months <- make_month_grid(cfg$study$start_year, 1, cfg$study$end_year, 12)

age_map <- c(
  `35-39` = "35-39", `40-44` = "40-44", `45-49` = "45-49",
  `50-54` = "50-54", `55-59` = "55-59", `60-64` = "60-64",
  `65-69` = "65-69", `70-74` = "70-74", `75-79` = "75-79",
  `80-84` = "80-84", `85_and_over` = "85+", `85+` = "85+",
  `85 and over` = "85+"
)

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
  grid <- tidyr::expand_grid(
    month_id = months$month_id,
    age_group = age_groups,
    sex = sexes
  ) |>
    dplyr::left_join(months[, c("month_id", "month_date", "year", "month")], by = "month_id")

  pieces <- lapply(split(annual_df, list(annual_df$age_group, annual_df$sex), drop = TRUE), function(g) {
    g <- dplyr::arrange(g, year)
    g$mid_date <- as.Date(sprintf("%04d-06-30", g$year))
    target <- grid[grid$age_group == g$age_group[1] & grid$sex == g$sex[1], , drop = FALSE]
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

parse_mdt_age_group <- function(path, reference_h = "1", values_thousands = TRUE) {
  raw <- utils::read.csv(path, stringsAsFactors = FALSE)
  validate_required_columns(raw, c("SEX", "AGE", "CCYY", "H", "obs_value"), basename(path))
  raw <- raw |>
    dplyr::filter(
      as.character(H) == as.character(reference_h),
      SEX %in% c("F", "M"),
      AGE %in% names(age_map)
    ) |>
    dplyr::mutate(
      year = as.integer(CCYY),
      sex = ifelse(SEX == "F", "Female", "Male"),
      age_group = unname(age_map[as.character(AGE)]),
      population = as.numeric(obs_value) * if (values_thousands) 1000 else 1
    ) |>
    dplyr::filter(!is.na(age_group), !is.na(population), population > 0) |>
    dplyr::group_by(year, sex, age_group) |>
    dplyr::summarise(population = sum(population), .groups = "drop")
  validate_required_columns(raw, c("year", "sex", "age_group", "population"), "parsed MDT")
  raw
}

# --- Resolve annual source ---------------------------------------------------
annual <- NULL
source_label <- NULL
data_status <- NULL

normalized_candidates <- list.files(
  pop_dir,
  pattern = "^csd_population_age_sex\\.csv$",
  full.names = TRUE
)

mdt_name <- "MDT_76_110-01001_POP_Raw_K_1dp_per_n.csv"
mdt_path <- file.path(pop_dir, mdt_name)
mdt_url <- cfg$population$mdt_url %||%
  "https://www.censtatd.gov.hk/data/MDT_76_110-01001_POP_Raw_K_1dp_per_n.csv"

# Always try to ensure primary MDT is present (and optional single-year archive).
download_or_refresh(mdt_url, mdt_path, force = isTRUE(cfg$pipeline$refresh_csd))
single_url <- cfg$population$mdt_single_year_url
if (!is.null(single_url) && nzchar(single_url)) {
  download_or_refresh(
    single_url,
    file.path(pop_dir, "MDT_76_110-01002_POP_Raw_K_1dp_per_n.csv"),
    force = isTRUE(cfg$pipeline$refresh_csd)
  )
}

if (length(normalized_candidates)) {
  message("Importing normalized C&SD CSV: ", basename(normalized_candidates[1]))
  raw <- utils::read.csv(normalized_candidates[1], stringsAsFactors = FALSE)
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
  raw$sex <- ifelse(tolower(substr(raw$sex, 1, 1)) == "f", "Female",
                    ifelse(tolower(substr(raw$sex, 1, 1)) == "m", "Male", raw$sex))
  annual <- raw |>
    dplyr::filter(age_group %in% age_groups, sex %in% sexes) |>
    dplyr::select(year, sex, age_group, population)
  source_label <- "csd_population_age_sex.csv"
  data_status <- "CSD_IMPORTED"
} else if (file.exists(mdt_path) && file.info(mdt_path)$size > 0) {
  message("Importing C&SD MDT: ", basename(mdt_path))
  annual <- parse_mdt_age_group(
    mdt_path,
    reference_h = cfg$population$reference_time_code %||% "1",
    values_thousands = isTRUE(cfg$population$values_are_thousands %||% TRUE)
  ) |>
    dplyr::filter(age_group %in% age_groups, sex %in% sexes)
  source_label <- cfg$population$source_table %||% "110-01001"
  data_status <- "CSD_IMPORTED"
  append_source_manifest(root, data.frame(
    source = "C&SD MDT 110-01001",
    url = mdt_url,
    file_path = mdt_path,
    retrieved_at = as.character(Sys.time()),
    sha256 = sha256_file(mdt_path),
    notes = "Mid-year population ('000) converted to persons; H=1",
    stringsAsFactors = FALSE
  ))
}

if (is.null(annual) || !nrow(annual)) {
  message("No C&SD source available. Building SYNTHETIC_DENOMINATOR for pipeline testing.")
  set.seed(cfg$project$seed)
  base_pop <- c(
    `35-39` = 520000, `40-44` = 530000, `45-49` = 540000, `50-54` = 560000,
    `55-59` = 550000, `60-64` = 480000, `65-69` = 360000, `70-74` = 250000,
    `75-79` = 180000, `80-84` = 120000, `85+` = 110000
  )
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
      for (y in years) {
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
  source_label <- "SYNTHETIC_NOT_CSD"
  data_status <- "SYNTHETIC_DENOMINATOR"
}

# Persist normalized annual extract for audit / schema consumers
annual_out <- annual |>
  dplyr::mutate(
    source_table = source_label,
    reference_time = "Mid-year"
  ) |>
  dplyr::arrange(year, sex, age_group)
write_csv_safe(annual_out, file.path(pop_dir, "csd_population_age_sex_annual_normalized.csv"))

# Need 2012 (or earlier) and 2024 anchors when possible for edge interpolation
stopifnot(all(age_groups %in% unique(annual$age_group)))
stopifnot(all(sexes %in% unique(annual$sex)))
stopifnot(min(annual$year) <= cfg$study$start_year)
stopifnot(max(annual$year) >= cfg$study$end_year)

pop_monthly <- interpolate_monthly(annual) |>
  dplyr::mutate(
    data_status = .env$data_status,
    source_table = .env$source_label,
    notes = if (identical(.env$data_status, "CSD_IMPORTED")) {
      "Linear interpolation between mid-year C&SD estimates"
    } else {
      "Pipeline scaffold only; replace with C&SD Table 110-01001"
    }
  )

pop_monthly <- pop_monthly |>
  dplyr::filter(
    month_id >= sprintf("%04d-%02d", cfg$study$start_year, cfg$study$start_month),
    month_id <= sprintf("%04d-%02d", cfg$study$end_year, cfg$study$end_month)
  ) |>
  dplyr::select(
    month_id, year, month, month_date, age_group, sex, population,
    dplyr::any_of(c("data_status", "source_table", "notes"))
  )

stopifnot(!any(duplicated(pop_monthly[, c("month_id", "age_group", "sex")])))
stopifnot(!any(is.na(pop_monthly$population)))
stopifnot(all(pop_monthly$population > 0))
assert_month_id(pop_monthly$month_id)

write_csv_safe(pop_monthly, file.path(root, "data_processed", "population_monthly_age_sex_2013_2023.csv"))

aging <- pop_monthly |>
  dplyr::filter(month == 6) |>
  dplyr::group_by(year, age_group) |>
  dplyr::summarise(population = sum(population), .groups = "drop")
write_csv_safe(aging, file.path(root, "outputs", "tables", "population_midyear_by_age_group.csv"))

aging_compare <- aging |>
  dplyr::filter(year %in% c(cfg$study$start_year, cfg$study$end_year)) |>
  tidyr::pivot_wider(names_from = year, values_from = population, names_prefix = "pop_")
write_csv_safe(aging_compare, file.path(root, "outputs", "tables", "population_aging_2013_vs_2023.csv"))

message("Population denominator build complete. Rows: ", nrow(pop_monthly),
        " | status: ", data_status, " | source: ", source_label)
if (grepl("SYNTHETIC", data_status)) {
  message("WARNING: synthetic denominators in use.")
} else {
  # Sanity: published mid-2013 both-sexes 65-69 was ~295.1 thousand
  y2013_6569 <- annual |>
    dplyr::filter(year == 2013, age_group == "65-69") |>
    dplyr::summarise(p = sum(population)) |>
    dplyr::pull(p)
  if (length(y2013_6569) == 1 && is.finite(y2013_6569)) {
    message(sprintf("QC mid-2013 ages 65-69 (both sexes): %.0f persons", y2013_6569))
  }
}
