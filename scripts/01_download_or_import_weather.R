#!/usr/bin/env Rscript
# 01_download_or_import_weather.R
# Downloads HKO dailyExtract JSON/XML files and open-data temperature CSVs.
# Never overwrites an existing raw file; writes alongside with timestamp if needed.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "jsonlite", "digest"))

years <- seq(cfg$study$start_year - 1L, cfg$study$optional_extension_year %||% cfg$study$end_year)
extract_dir <- file.path(root, cfg$weather$sources$daily_extract_dir)
dir.create(extract_dir, recursive = TRUE, showWarnings = FALSE)

download_if_absent <- function(url, dest) {
  if (file.exists(dest) && file.info(dest)$size > 0) {
    message("Exists, skipping download: ", dest)
    return(invisible(FALSE))
  }
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

manifest_rows <- list()

for (y in years) {
  url <- sprintf("https://www.hko.gov.hk/cis/dailyExtract/dailyExtract_%d.xml", y)
  dest <- file.path(extract_dir, sprintf("dailyExtract_%d.xml", y))
  download_if_absent(url, dest)
  if (file.exists(dest)) {
    manifest_rows[[length(manifest_rows) + 1]] <- data.frame(
      source = "HKO dailyExtract",
      url = url,
      file_path = dest,
      retrieved_at = as.character(Sys.time()),
      sha256 = sha256_file(dest),
      notes = "JSON content despite .xml extension; HKO Headquarters daily climate",
      stringsAsFactors = FALSE
    )
  }
}

# Also keep open-data max/min/mean temperature CSVs as audit companions
open_dir <- file.path(root, cfg$weather$sources$open_data_dir)
dir.create(open_dir, recursive = TRUE, showWarnings = FALSE)
for (dt in c("CLMTEMP", "CLMMAXT", "CLMMINT")) {
  url <- sprintf(
    "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=%s&rformat=csv&station=HKO",
    dt
  )
  dest <- file.path(open_dir, sprintf("%s_HKO.csv", dt))
  download_if_absent(url, dest)
  if (file.exists(dest)) {
    manifest_rows[[length(manifest_rows) + 1]] <- data.frame(
      source = paste("HKO open data", dt),
      url = url,
      file_path = dest,
      retrieved_at = as.character(Sys.time()),
      sha256 = sha256_file(dest),
      notes = "Full historical series; used for cross-checks",
      stringsAsFactors = FALSE
    )
  }
}

if (length(manifest_rows)) {
  append_source_manifest(root, do.call(rbind, manifest_rows))
}

message("Weather import step complete.")
message("NOTE: Relative humidity and rainfall are taken from dailyExtract files.")
message("Open-data API currently exposes CLMTEMP/CLMMAXT/CLMMINT for station series.")
