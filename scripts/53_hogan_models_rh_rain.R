#!/usr/bin/env Rscript
# 53_hogan_models_rh_rain.R
# Hogan 24 Aug 2026: Models 1–12 with monthly mean RH and monthly total rainfall.
# Primary extreme-day scale is per 5 days; also writes per-1-day and per-3-day
# sensitivities (KW15). Does not invent coefficients when the governed panel is
# absent. Does not overwrite outputs/release_chd_hf/tables/table2_core_models.csv
# (that file is the 10 Aug specification without RH/rainfall).

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "final_model_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "yaml", "MASS", "splines", "sandwich", "lmtest"))

registry <- load_final_model_registry(root = root)
specs <- core_exposure_specs(registry)
outcomes <- registry$outcomes %||% c("chd", "hf")
out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

hogan_scenario <- list(
  scenario_id = "Hogan_RH_rain",
  controls = c(
    "calendar_month_factor",
    "ns_time_df4",
    "relative_humidity",
    "rainfall"
  )
)

model_index <- data.frame(
  model_n = 1:12,
  outcome = rep(c("chd", "hf"), each = 6L),
  pathway_id = rep(c("P01A", "P02A", "P02B", "P04A", "P04B", "P04C"), 2L),
  stringsAsFactors = FALSE
)

panel_paths <- setNames(
  file.path(root, "data_processed", paste0(outcomes, "_analysis_panel.csv")),
  outcomes
)
missing <- !file.exists(panel_paths)
if (any(missing)) {
  blocker <- missing_governed_panel_blocker(
    outcomes = outcomes,
    root = root,
    script_id = "53_hogan_models_rh_rain"
  )
  handle_missing_governed_panels(
    blocker,
    file.path(out_dir, "hogan_models_rh_rain_blocker.csv")
  )
}

climate_path <- file.path(root, "data_processed", "climate_monthly_2013_2023.csv")
if (!file.exists(climate_path)) {
  stop("Missing climate monthly file: ", climate_path)
}
clim <- utils::read.csv(climate_path, stringsAsFactors = FALSE)
need_clim <- c("month_id", "relative_humidity", "rainfall")
missing_clim <- setdiff(need_clim, names(clim))
if (length(missing_clim)) {
  stop("climate_monthly missing columns: ", paste(missing_clim, collapse = ", "))
}
clim_keep <- clim[, need_clim, drop = FALSE]

attach_weather_covariates <- function(dat) {
  out <- dat
  if (!"relative_humidity" %in% names(out) || !"rainfall" %in% names(out)) {
    out <- merge(out, clim_keep, by = "month_id", all.x = TRUE, sort = FALSE)
  }
  missing_cov <- setdiff(c("relative_humidity", "rainfall"), names(out))
  if (length(missing_cov)) {
    stop("Panel still missing ", paste(missing_cov, collapse = ", "))
  }
  out
}

doy_path <- file.path(root, "data_processed", "hogan_abnormal_day_counts_2013_2023.csv")
doy <- NULL
if (file.exists(doy_path)) {
  doy <- utils::read.csv(doy_path, stringsAsFactors = FALSE)
}

panels <- lapply(outcomes, function(outcome) {
  dat <- utils::read.csv(panel_paths[[outcome]], stringsAsFactors = FALSE)
  dat <- attach_weather_covariates(dat)
  if (!is.null(doy)) {
    extra <- setdiff(names(doy), c("month_id", "year", "month", "n_days"))
    extra <- extra[!grepl("relative_humidity|rainfall", extra)]
    dat <- merge(
      dat,
      doy[, c("month_id", extra), drop = FALSE],
      by = "month_id",
      all.x = TRUE,
      sort = FALSE
    )
  }
  prepare_analysis_panel(dat, require_real = TRUE, outcome = outcome)
})
names(panels) <- outcomes

extreme_pathways <- c("P04A", "P04B", "P04C")

estimate_rows <- list()
status_rows <- list()

for (i in seq_len(nrow(model_index))) {
  row <- model_index[i, ]
  dat <- panels[[row$outcome]]
  spec <- specs[[row$pathway_id]]
  contrast_set <- if (row$pathway_id %in% extreme_pathways) {
    list(primary = 5, sensitivity_1 = 1, sensitivity_3 = 3)
  } else {
    list(primary = spec$contrast)
  }
  for (cname in names(contrast_set)) {
    spec_i <- spec
    spec_i$contrast <- as.numeric(contrast_set[[cname]])
    key <- paste(row$model_n, cname, sep = "::")
    fit <- fit_scenario_nb(
      dat = dat,
      pathway_id = row$pathway_id,
      exposure_spec = spec_i,
      scenario = hogan_scenario,
      registry = registry,
      offset_policy = "days_only",
      model_id = sprintf("Model_%02d", row$model_n),
      result_class = RESULT_CLASS_EXPLORATORY,
      data_status = REAL_PROVENANCE
    )
    st <- fit$status
    st$model_n <- row$model_n
    st$scale <- cname
    status_rows[[key]] <- st
    if (!is.null(fit$estimates) && nrow(fit$estimates)) {
      est <- fit$estimates
      est$model_n <- row$model_n
      est$scale <- cname
      est$result_class <- RESULT_CLASS_EXPLORATORY
      est$data_status <- REAL_PROVENANCE
      estimate_rows[[key]] <- est
    }
  }
}

status_df <- dplyr::bind_rows(status_rows)
utils::write.csv(
  status_df,
  file.path(out_dir, "hogan_models_rh_rain_status.csv"),
  row.names = FALSE,
  na = ""
)

if (!length(estimate_rows)) {
  stop("Models 1–12 with RH/rainfall produced no estimates")
}
est_df <- dplyr::bind_rows(estimate_rows)

nw6 <- est_df[
  est_df$se_method == "NeweyWest_lag6" & est_df$scale == "primary",
  ,
  drop = FALSE
]
nw6 <- nw6[order(nw6$model_n), , drop = FALSE]
if (nrow(nw6) != 12L) {
  stop("Expected 12 Newey–West lag-6 primary rows, found ", nrow(nw6))
}
nw6$q_value_bh_models_1_12 <- stats::p.adjust(nw6$p_value, method = "BH")

utils::write.csv(
  nw6,
  file.path(out_dir, "table2_models_1_12_rh_rain.csv"),
  row.names = FALSE,
  na = ""
)
utils::write.csv(
  est_df,
  file.path(out_dir, "hogan_models_rh_rain_ladder.csv"),
  row.names = FALSE,
  na = ""
)

message(
  "Wrote Models 1–12 with RH and rainfall to ",
  file.path(out_dir, "table2_models_1_12_rh_rain.csv")
)
