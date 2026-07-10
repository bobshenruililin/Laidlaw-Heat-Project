# Shared helpers for the HK thermal-CVD pipeline
# Sourced by scripts; do not run directly.

`%||%` <- function(x, y) {
  if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
}

project_root <- function() {
  # Prefer current working directory if it looks like the project root
  if (file.exists("config.yml") || file.exists("scripts/00_setup.R")) {
    return(normalizePath(".", winslash = "/", mustWork = TRUE))
  }
  # Fallback: directory containing this file's parent
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
  # Trace rainfall treated as 0
  x[tolower(x) == "trace"] <- "0"
  suppressWarnings(as.numeric(x))
}

assign_covid_phase <- function(month_id, phases) {
  # phases: named list of c(start_month_id, end_month_id)
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

sha256_file <- function(path) {
  if (!file.exists(path)) return(NA_character_)
  if (requireNamespace("digest", quietly = TRUE)) {
    return(digest::digest(file = path, algo = "sha256"))
  }
  # Fallback via openssl/sha256sum if available
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
    # replace rows with same file_path
    old <- old[!old$file_path %in% records$file_path, , drop = FALSE]
    out <- rbind(old, records)
  } else {
    out <- records
  }
  utils::write.csv(out, path, row.names = FALSE)
  invisible(path)
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
