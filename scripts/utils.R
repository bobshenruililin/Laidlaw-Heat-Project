# Shared helpers for the HK thermal-CVD pipeline
# Sourced by scripts; do not run directly.

`%||%` <- function(x, y) {
  if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
}

project_root <- function() {
  if (file.exists("config.yml") || file.exists("scripts/00_setup.R")) {
    return(normalizePath(".", winslash = "/", mustWork = TRUE))
  }
  this_file <- sys.frames()[[1]]$ofile
  if (!is.null(this_file)) {
    return(normalizePath(file.path(dirname(this_file), ".."), winslash = "/", mustWork = TRUE))
  }
  normalizePath(".", winslash = "/", mustWork = TRUE)
}

ensure_packages <- function(pkgs) {
  user_lib <- Sys.getenv("R_LIBS_USER", unset = file.path(Sys.getenv("HOME"), "R", "library"))
  dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
  .libPaths(c(user_lib, .libPaths()))
  missing <- pkgs[!vapply(pkgs, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))]
  if (length(missing)) {
    message("Installing missing packages: ", paste(missing, collapse = ", "))
    install.packages(missing, repos = "https://cloud.r-project.org", lib = user_lib)
  }
  invisible(lapply(pkgs, function(p) {
    suppressPackageStartupMessages(library(p, character.only = TRUE))
  }))
}

load_config <- function(root = project_root()) {
  cfg_path <- file.path(root, "config.yml")
  if (!file.exists(cfg_path)) stop("config.yml not found at ", cfg_path)
  user_lib <- Sys.getenv("R_LIBS_USER", unset = file.path(Sys.getenv("HOME"), "R", "library"))
  dir.create(user_lib, recursive = TRUE, showWarnings = FALSE)
  .libPaths(c(user_lib, .libPaths()))
  if (!requireNamespace("yaml", quietly = TRUE)) {
    install.packages("yaml", repos = "https://cloud.r-project.org", lib = user_lib)
  }
  yaml::read_yaml(cfg_path)
}

pipeline_mode <- function(cfg = NULL) {
  if (is.null(cfg)) cfg <- load_config()
  mode <- cfg$pipeline$mode %||% "dev"
  if (!mode %in% c("dev", "real")) stop("pipeline.mode must be 'dev' or 'real', got: ", mode)
  mode
}

make_month_grid <- function(start_year, start_month, end_year, end_month) {
  start <- as.Date(sprintf("%04d-%02d-01", start_year, start_month))
  end <- as.Date(sprintf("%04d-%02d-01", end_year, end_month))
  month_date <- seq(start, end, by = "month")
  next_month <- c(month_date[-1], seq(end, by = "month", length.out = 2)[2])
  days_in_month <- as.integer(next_month - month_date)
  data.frame(
    month_date = month_date,
    year = as.integer(format(month_date, "%Y")),
    month = as.integer(format(month_date, "%m")),
    month_id = format(month_date, "%Y-%m"),
    time_index = seq_along(month_date),
    days_in_month = days_in_month,
    stringsAsFactors = FALSE
  )
}

longest_true_run <- function(x) {
  x <- as.logical(x)
  x[is.na(x)] <- FALSE
  if (!any(x)) return(0L)
  runs <- rle(x)
  as.integer(max(runs$lengths[runs$values]))
}

# Absolute humidity (g/m^3) via Tetens vapour pressure from air temperature (°C)
# and relative humidity (%). Preferred over RH alone for cold/infection pathways
# (see Yang/Chong et al. 2025 weekly stroke analysis).
absolute_humidity_gm3 <- function(temp_c, rh_pct) {
  temp_c <- as.numeric(temp_c)
  rh_pct <- as.numeric(rh_pct)
  es <- 6.112 * exp((17.67 * temp_c) / (temp_c + 243.5))
  e <- es * (rh_pct / 100)
  216.7 * e / (temp_c + 273.15)
}

# Flag days belonging to a simple 2D3N-type window: within a 5-day window,
# at least 2 very-hot days and 3 hot nights (Wang et al. 2019-inspired).
flag_2d3n_window <- function(very_hot_day, hot_night, window = 5L) {
  vhd <- as.logical(very_hot_day)
  hn <- as.logical(hot_night)
  vhd[is.na(vhd)] <- FALSE
  hn[is.na(hn)] <- FALSE
  n <- length(vhd)
  out <- rep(FALSE, n)
  if (n < window) return(out)
  for (i in seq_len(n - window + 1L)) {
    idx <- i:(i + window - 1L)
    if (sum(vhd[idx]) >= 2L && sum(hn[idx]) >= 3L) {
      out[idx] <- TRUE
    }
  }
  out
}

parse_hko_number <- function(x) {
  x <- trimws(as.character(x))
  x[x %in% c("", "***", "----", "--", "NA", "N/A")] <- NA_character_
  x[tolower(x) == "trace"] <- "0"
  suppressWarnings(as.numeric(x))
}

assign_covid_phase <- function(month_id, phases) {
  out <- rep(NA_character_, length(month_id))
  for (nm in names(phases)) {
    rng <- phases[[nm]]
    out[month_id >= rng[1] & month_id <= rng[2]] <- nm
  }
  out
}

write_csv_safe <- function(x, path) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(x, path, row.names = FALSE, na = "")
  message("Wrote ", path, " (", nrow(x), " rows)")
}

# Write a README only once so human edits are not clobbered on every pipeline run.
write_readme_if_absent <- function(path, lines) {
  if (file.exists(path)) {
    message("README exists, leaving unchanged: ", path)
    return(invisible(FALSE))
  }
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  writeLines(lines, path)
  message("Wrote README: ", path)
  invisible(TRUE)
}

sha256_file <- function(path) {
  if (!file.exists(path)) return(NA_character_)
  if (requireNamespace("digest", quietly = TRUE)) {
    return(digest::digest(file = path, algo = "sha256"))
  }
  res <- tryCatch(
    system2("sha256sum", path, stdout = TRUE),
    error = function(e) NA_character_
  )
  if (length(res) == 1 && !is.na(res)) sub(" .*", "", res) else NA_character_
}

append_source_manifest <- function(root, records) {
  path <- file.path(root, "data_raw", "source_manifest.csv")
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  if (file.exists(path)) {
    old <- utils::read.csv(path, stringsAsFactors = FALSE)
    old <- old[!old$file_path %in% records$file_path, , drop = FALSE]
    out <- rbind(old, records)
  } else {
    out <- records
  }
  utils::write.csv(out, path, row.names = FALSE)
  invisible(path)
}

download_if_absent <- function(url, dest) {
  if (file.exists(dest) && file.info(dest)$size > 0) {
    message("Exists, skipping download: ", dest)
    return(invisible(FALSE))
  }
  dir.create(dirname(dest), recursive = TRUE, showWarnings = FALSE)
  message("Downloading ", url)
  ok <- tryCatch({
    utils::download.file(url, dest, mode = "wb", quiet = TRUE)
    TRUE
  }, error = function(e) {
    message("Download failed: ", conditionMessage(e))
    FALSE
  })
  invisible(ok)
}

# Refresh a remote file when missing or when force=TRUE.
download_or_refresh <- function(url, dest, force = FALSE) {
  if (!force && file.exists(dest) && file.info(dest)$size > 0) {
    message("Exists, skipping download: ", dest)
    return(invisible(FALSE))
  }
  dir.create(dirname(dest), recursive = TRUE, showWarnings = FALSE)
  message(if (force) "Refreshing " else "Downloading ", url)
  ok <- tryCatch({
    utils::download.file(url, dest, mode = "wb", quiet = TRUE)
    TRUE
  }, error = function(e) {
    message("Download failed: ", conditionMessage(e))
    FALSE
  })
  invisible(ok)
}

assert_month_id <- function(x, arg = "month_id") {
  bad <- !grepl("^[0-9]{4}-(0[1-9]|1[0-2])$", as.character(x))
  if (any(bad, na.rm = TRUE) || any(is.na(x))) {
    stop(arg, " must match YYYY-MM; first bad: ",
         paste(utils::head(unique(as.character(x[bad | is.na(x)])), 5), collapse = ", "))
  }
  invisible(TRUE)
}

validate_required_columns <- function(df, required, context = "input") {
  missing <- setdiff(required, names(df))
  if (length(missing)) {
    stop(context, " missing required columns: ", paste(missing, collapse = ", "))
  }
  invisible(TRUE)
}

stop_if_not_synthetic <- function(df) {
  if (!"data_status" %in% names(df)) {
    stop("analysis panel missing data_status column")
  }
  if (!all(df$data_status == "SYNTHETIC")) {
    stop("Refusing to run synthetic modeling scripts on non-SYNTHETIC data")
  }
  invisible(TRUE)
}

stop_if_synthetic <- function(df) {
  if (!"data_status" %in% names(df)) {
    stop("analysis panel missing data_status column")
  }
  if (any(grepl("SYNTHETIC", df$data_status))) {
    stop("Refusing real-mode inference on SYNTHETIC outcome rows")
  }
  invisible(TRUE)
}

# Official HKO Year's Weather annual extremes at Headquarters (2013–2023).
hko_official_annual_extremes <- function() {
  data.frame(
    year = 2013:2023,
    hot_nights_official = c(10L, 34L, 37L, 36L, 41L, 26L, 46L, 50L, 61L, 52L, 56L),
    very_hot_days_official = c(17L, 33L, 28L, 38L, 29L, 36L, 33L, 47L, 54L, 52L, 54L),
    cold_days_official = c(14L, 21L, 7L, 21L, 9L, 21L, 1L, 11L, 13L, 13L, 14L),
    stringsAsFactors = FALSE
  )
}

validate_hko_annual_extremes <- function(annual_df) {
  required <- c("year", "hot_nights", "very_hot_days", "cold_days")
  validate_required_columns(annual_df, required, "HKO annual extremes")
  official <- hko_official_annual_extremes()
  merged <- merge(annual_df[, required, drop = FALSE], official, by = "year", all.y = TRUE)
  merged$hot_match <- merged$hot_nights == merged$hot_nights_official
  merged$vhd_match <- merged$very_hot_days == merged$very_hot_days_official
  merged$cold_match <- merged$cold_days == merged$cold_days_official
  merged$all_match <- merged$hot_match & merged$vhd_match & merged$cold_match
  n_ok <- sum(merged$all_match, na.rm = TRUE)
  n_tot <- nrow(merged) * 3L
  n_metric_ok <- sum(c(merged$hot_match, merged$vhd_match, merged$cold_match), na.rm = TRUE)
  list(
    table = merged,
    n_years_ok = n_ok,
    n_metric_checks_ok = n_metric_ok,
    n_metric_checks = n_tot,
    all_ok = isTRUE(n_metric_ok == n_tot)
  )
}

# Weather daily-parse cache keyed by SHA of source dailyExtract files.
weather_cache_paths <- function(root) {
  cache_dir <- file.path(root, "data_processed", ".cache")
  list(
    dir = cache_dir,
    daily = file.path(cache_dir, "climate_daily_parsed.rds"),
    manifest = file.path(cache_dir, "daily_extract_sha.csv")
  )
}

daily_extract_manifest <- function(extract_dir, years) {
  paths <- file.path(extract_dir, sprintf("dailyExtract_%d.xml", years))
  data.frame(
    year = years,
    file_path = paths,
    exists = file.exists(paths),
    sha256 = vapply(paths, sha256_file, character(1)),
    stringsAsFactors = FALSE
  )
}

weather_cache_is_valid <- function(root, extract_dir, years) {
  paths <- weather_cache_paths(root)
  if (!file.exists(paths$daily) || !file.exists(paths$manifest)) return(FALSE)
  current <- daily_extract_manifest(extract_dir, years)
  if (!all(current$exists)) return(FALSE)
  old <- utils::read.csv(paths$manifest, stringsAsFactors = FALSE)
  if (!all(c("year", "sha256") %in% names(old))) return(FALSE)
  merged <- merge(current[, c("year", "sha256")], old[, c("year", "sha256")],
                  by = "year", suffixes = c("_new", "_old"), all = TRUE)
  all(!is.na(merged$sha256_new) & !is.na(merged$sha256_old) &
        merged$sha256_new == merged$sha256_old)
}

save_weather_daily_cache <- function(root, weather_daily, extract_dir, years) {
  paths <- weather_cache_paths(root)
  dir.create(paths$dir, recursive = TRUE, showWarnings = FALSE)
  saveRDS(weather_daily, paths$daily)
  utils::write.csv(daily_extract_manifest(extract_dir, years), paths$manifest, row.names = FALSE)
  message("Wrote weather daily cache: ", paths$daily)
}

load_weather_daily_cache <- function(root) {
  paths <- weather_cache_paths(root)
  readRDS(paths$daily)
}
