#!/usr/bin/env Rscript
# 19b_build_hm_cm_exposures.R
# Registry-driven hot/cold month flags from analysis_plan/hot_cold_month_registry.yml
#
# IMPORTANT: threshold_policy.reference_period is still null in the registry.
# This builder uses the study window (2013-2023) as a PROVISIONAL reference and
# labels outputs accordingly. Do not claim Hogan-locked HM23 until Playbook 01 closes.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr"))

reg <- yaml::read_yaml(file.path(root, "analysis_plan", "hot_cold_month_registry.yml"))
clim <- utils::read.csv(file.path(root, "data_processed", "climate_monthly_2013_2023.csv"), stringsAsFactors = FALSE)
exp <- utils::read.csv(file.path(root, "data_processed", "exposures_monthly_2013_2023.csv"), stringsAsFactors = FALSE)

# Prefer daily extract if present for event-based definitions
daily_candidates <- c(
  file.path(root, "data_processed", "climate_daily_hko.csv"),
  file.path(root, "data_raw", "hko", "daily_extract", "hko_daily_2012_2023.csv"),
  file.path(root, "data_processed", "hko_daily_panel.csv")
)
daily_path <- daily_candidates[file.exists(daily_candidates)][1]
has_daily <- !is.na(daily_path) && nzchar(daily_path)
if (has_daily) {
  daily <- utils::read.csv(daily_path, stringsAsFactors = FALSE)
  message("Daily HKO file: ", daily_path)
} else {
  daily <- NULL
  message("No daily HKO file found — event-start HM23 will use monthly proxies where possible.")
}

starters <- unique(c(reg$starter_codes$core %||% character(), reg$starter_codes$first_wave %||% character()))
defs <- reg$definitions

# Provisional reference: study-window months (document as not Hogan-locked)
clim <- clim |>
  dplyr::mutate(
    month_id = sprintf("%04d-%02d", year, month),
    season_warm = month %in% 5:9
  )

qtile <- function(x, p) as.numeric(stats::quantile(x, probs = p / 100, na.rm = TRUE, type = 7))

out <- data.frame(month_id = clim$month_id, stringsAsFactors = FALSE)
audit <- list()

# --- Implementable starters with monthly climate ---
# HM08: mean_temp >= p90 of all months in study window
if ("HM08" %in% starters && !is.null(defs$HM08)) {
  thr <- qtile(clim$mean_temp, 90)
  out$HM08 <- as.integer(clim$mean_temp >= thr)
  audit$HM08 <- list(threshold = thr, n_selected = sum(out$HM08), status = "provisional_study_window")
}

# HM15: mean_tmax >= p95
if ("HM15" %in% starters && !is.null(defs$HM15)) {
  thr <- qtile(clim$mean_tmax, 95)
  out$HM15 <- as.integer(clim$mean_tmax >= thr)
  audit$HM15 <- list(threshold = thr, n_selected = sum(out$HM15), status = "provisional_study_window")
}

# HM17: very_hot_days count >= p90 of monthly VHD counts
if ("HM17" %in% starters && !is.null(defs$HM17) && "very_hot_days" %in% names(clim)) {
  thr <- qtile(clim$very_hot_days, 90)
  out$HM17 <- as.integer(clim$very_hot_days >= thr)
  audit$HM17 <- list(threshold = thr, n_selected = sum(out$HM17), status = "provisional_study_window")
}

# HM19: hot_nights count >= p90
if ("HM19" %in% starters && !is.null(defs$HM19) && "hot_nights" %in% names(clim)) {
  thr <- qtile(clim$hot_nights, 90)
  out$HM19 <- as.integer(clim$hot_nights >= thr)
  audit$HM19 <- list(threshold = thr, n_selected = sum(out$HM19), status = "provisional_study_window")
}

# HM27: month has any days_in_very_hot_spell_ge5 > 0 (spell presence)
if ("HM27" %in% starters && "days_in_very_hot_spell_ge5" %in% names(clim)) {
  out$HM27 <- as.integer(clim$days_in_very_hot_spell_ge5 > 0)
  audit$HM27 <- list(threshold = 0, n_selected = sum(out$HM27), status = "spell_presence_proxy")
}

# HM32: 2D3N window days > 0
if ("HM32" %in% starters && "days_in_2d3n_window" %in% names(clim)) {
  out$HM32 <- as.integer(clim$days_in_2d3n_window > 0)
  audit$HM32 <- list(threshold = 0, n_selected = sum(out$HM32), status = "2d3n_presence_proxy")
}

# CM03: mean_temp <= p10
if ("CM03" %in% starters && !is.null(defs$CM03)) {
  thr <- qtile(clim$mean_temp, 10)
  out$CM03 <- as.integer(clim$mean_temp <= thr)
  audit$CM03 <- list(threshold = thr, n_selected = sum(out$CM03), status = "provisional_study_window")
}

# CM08: mean_tmin <= p05
if ("CM08" %in% starters && !is.null(defs$CM08)) {
  thr <- qtile(clim$mean_tmin, 5)
  out$CM08 <- as.integer(clim$mean_tmin <= thr)
  audit$CM08 <- list(threshold = thr, n_selected = sum(out$CM08), status = "provisional_study_window")
}

# CM15: cold_days count >= p90 of monthly cold-day counts
if ("CM15" %in% starters && "cold_days" %in% names(clim)) {
  thr <- qtile(clim$cold_days, 90)
  out$CM15 <- as.integer(clim$cold_days >= thr)
  audit$CM15 <- list(threshold = thr, n_selected = sum(out$CM15), status = "provisional_study_window")
}

# CM05: absolute Tmin proxy — months with mean_tmin <= 10 (sensitivity; not daily Tmin≤10 count)
if ("CM05" %in% starters) {
  out$CM05 <- as.integer(clim$mean_tmin <= 10)
  audit$CM05 <- list(threshold = 10, n_selected = sum(out$CM05), status = "mean_tmin_proxy_not_daily_CM05")
}

# CM30: max_cold_spell_touching >= 3
if ("CM30" %in% starters && "max_cold_spell_touching" %in% names(clim)) {
  out$CM30 <- as.integer(clim$max_cold_spell_touching >= 3)
  audit$CM30 <- list(threshold = 3, n_selected = sum(out$CM30), status = "spell_length_proxy")
}

# HM23: Li-HW style — requires daily; provisional from warm-season monthly VHD spell starts if daily absent
if ("HM23" %in% starters) {
  if (has_daily && all(c("date", "tmax") %in% names(daily))) {
    # Simplified provisional HM23: count days tmax > calendar-day p90 within warm season runs >=3
    # Full Li-HW calendar-day percentile with 15-day window is deferred to Hogan lock.
    d <- daily
    d$date <- as.Date(d$date)
    d$year <- as.integer(format(d$date, "%Y"))
    d$month <- as.integer(format(d$date, "%m"))
    d$yday <- as.integer(format(d$date, "%j"))
    d <- d[d$year >= 2013 & d$year <= 2023, ]
    # calendar-day p90 of tmax across years
    cal <- tapply(d$tmax, d$yday, function(z) qtile(z, 90))
    d$thr <- cal[as.character(d$yday)]
    d$hot <- as.integer(!is.na(d$tmax) & !is.na(d$thr) & d$tmax > d$thr)
    # event starts: hot run >=3 in May-Sep; gap join <=2 treated later as optional
    d$month_id <- format(d$date, "%Y-%m")
    # mark runs
    r <- rle(d$hot)
    ends <- cumsum(r$lengths)
    starts <- ends - r$lengths + 1
    event_start_idx <- integer()
    for (i in seq_along(r$values)) {
      if (isTRUE(r$values[i] == 1L) && r$lengths[i] >= 3 && d$month[starts[i]] %in% 5:9) {
        event_start_idx <- c(event_start_idx, starts[i])
      }
    }
    starts_mid <- d$month_id[event_start_idx]
    tab <- table(starts_mid)
    # monthly counts for warm months; p90 of those monthly counts
    warm <- clim$month_id[clim$month %in% 5:9]
    counts <- setNames(rep(0, length(warm)), warm)
    for (nm in names(tab)) if (nm %in% names(counts)) counts[nm] <- as.integer(tab[nm])
    thr_m <- qtile(as.numeric(counts), 90)
    flag <- setNames(rep(0L, nrow(clim)), clim$month_id)
    for (nm in names(counts)) if (counts[nm] >= thr_m) flag[nm] <- 1L
    out$HM23 <- as.integer(flag[out$month_id])
    out$HM23_event_starts <- as.numeric(counts[match(out$month_id, names(counts))])
    out$HM23_event_starts[is.na(out$HM23_event_starts)] <- 0
    audit$HM23 <- list(
      threshold_monthly_p90 = thr_m,
      n_selected = sum(out$HM23),
      status = "provisional_daily_calendar_p90_study_window_NOT_hogan_locked"
    )
  } else if ("hw_month_mean_temp_ge_p90" %in% names(exp)) {
    out$HM23 <- as.integer(exp$hw_month_mean_temp_ge_p90[match(out$month_id, exp$month_id)])
    audit$HM23 <- list(threshold = NA, n_selected = sum(out$HM23, na.rm = TRUE), status = "fallback_exposure_p90_proxy_NOT_true_HM23")
  } else {
    out$HM23 <- NA_integer_
    audit$HM23 <- list(status = "unavailable")
  }
}

# Join to exposures file and write
hmcm_path <- file.path(root, "data_processed", "hm_cm_month_flags_2013_2023.csv")
write_csv_safe(out, hmcm_path)

# Selected-month audit
sel_rows <- list()
for (id in names(out)) {
  if (id == "month_id" || id == "HM23_event_starts") next
  if (!is.numeric(out[[id]]) && !is.integer(out[[id]])) next
  mids <- out$month_id[!is.na(out[[id]]) & out[[id]] == 1]
  if (length(mids)) {
    sel_rows[[id]] <- data.frame(
      definition_id = id,
      n_selected = length(mids),
      selected_months = paste(mids, collapse = ","),
      implementation_status = audit[[id]]$status %||% "built",
      stringsAsFactors = FALSE
    )
  } else {
    sel_rows[[id]] <- data.frame(
      definition_id = id,
      n_selected = 0L,
      selected_months = "",
      implementation_status = audit[[id]]$status %||% "built_zero",
      stringsAsFactors = FALSE
    )
  }
}
audit_df <- dplyr::bind_rows(sel_rows)
write_csv_safe(audit_df, file.path(root, "outputs", "tables", "hm_cm_selected_months_audit.csv"))

# Parameter snapshot
snap <- data.frame(
  built_at = as.character(Sys.time()),
  reference_period_policy = "PROVISIONAL study window 2013-2023; registry reference_period still null",
  hogan_locked = FALSE,
  daily_file = if (has_daily) daily_path else NA_character_,
  n_definitions_built = ncol(out) - 1L,
  stringsAsFactors = FALSE
)
write_csv_safe(snap, file.path(root, "outputs", "tables", "hm_cm_build_snapshot.csv"))

rep <- file.path(root, "outputs", "reports", "hm_cm_exposure_build.md")
lines <- c(
  "# Hot/cold month exposure build",
  "",
  paste0("- Built at: ", snap$built_at),
  paste0("- **Reference period:** ", snap$reference_period_policy),
  paste0("- Hogan-locked: ", snap$hogan_locked),
  paste0("- Daily file: ", snap$daily_file),
  paste0("- Output: `", hmcm_path, "`"),
  "",
  "## Selected-month counts",
  "",
  "| ID | n_selected | status |",
  "|---|---|---|",
  paste0("| ", audit_df$definition_id, " | ", audit_df$n_selected, " | ", audit_df$implementation_status, " |"),
  "",
  "These flags are **provisional**. Gate 3 must not treat HM23 as locked until Playbook 01 closes."
)
writeLines(lines, rep)
message("HM/CM flags written: ", hmcm_path, " (", ncol(out) - 1, " definition columns)")
