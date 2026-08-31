#!/usr/bin/env Rscript
# 68_hogan_model3_climatology.R
# Hogan 24 Aug 2026 Model 3: replace official extreme-day counts with
# leave-one-year-out same-calendar-day warmer/cooler day counts of daily mean
# temperature. Primary scale is per 5 days. Tmax-above and Tmin-below counts
# are sensitivities. Does not overwrite Table 2 (Model 1). Does not invent
# coefficients when the governed panel is absent.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "final_model_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "yaml", "MASS", "splines", "sandwich", "lmtest"))

registry <- load_final_model_registry(root = root)
outcomes <- registry$outcomes %||% c("chd", "hf")
out_dir <- file.path(root, "outputs", "tables")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

panel_paths <- setNames(
  file.path(root, "data_processed", paste0(outcomes, "_analysis_panel.csv")),
  outcomes
)
missing <- !file.exists(panel_paths)
if (any(missing)) {
  blocker <- missing_governed_panel_blocker(
    outcomes = outcomes,
    root = root,
    script_id = "68_hogan_model3_climatology"
  )
  handle_missing_governed_panels(
    blocker,
    file.path(out_dir, "hogan_model3_climatology_blocker.csv")
  )
}

clim_path <- file.path(root, "data_processed", "hogan_climatology_day_counts_2013_2023.csv")
if (!file.exists(clim_path)) {
  stop("Missing climatology day-count file: ", clim_path)
}
clim <- utils::read.csv(clim_path, stringsAsFactors = FALSE)
need <- c(
  "month_id",
  "days_warmer_than_climatology",
  "days_cooler_than_climatology",
  "days_tmax_above_climatology",
  "days_tmin_below_climatology"
)
missing_clim <- setdiff(need, names(clim))
if (length(missing_clim)) {
  stop("climatology file missing columns: ", paste(missing_clim, collapse = ", "))
}
clim_keep <- clim[, need, drop = FALSE]

m3_specs <- registry$model3_exposures
if (is.null(m3_specs) || !length(m3_specs)) {
  stop("final_model_registry.yml is missing model3_exposures")
}

baseline <- list(
  scenario_id = "Model3_climatology",
  controls = c("calendar_month_factor", "ns_time_df4")
)

panels <- lapply(outcomes, function(outcome) {
  dat <- utils::read.csv(panel_paths[[outcome]], stringsAsFactors = FALSE)
  extra <- setdiff(names(clim_keep), names(dat))
  if (length(extra)) {
    dat <- merge(
      dat,
      clim_keep[, c("month_id", extra), drop = FALSE],
      by = "month_id",
      all.x = TRUE,
      sort = FALSE
    )
  }
  prepare_analysis_panel(dat, require_real = TRUE, outcome = outcome)
})
names(panels) <- outcomes

estimate_rows <- list()
status_rows <- list()

for (outcome in outcomes) {
  dat <- panels[[outcome]]
  for (id in names(m3_specs)) {
    s <- m3_specs[[id]]
    spec <- list(
      pathway_id = id,
      variable = s$variable,
      contrast = as.numeric(s$contrast),
      unit = s$unit %||% "days",
      pole = s$pole %||% NA_character_
    )
    if (!spec$variable %in% names(dat)) {
      stop("Panel missing Model 3 column ", spec$variable)
    }
    key <- paste(outcome, id, sep = "::")
    fit <- fit_scenario_nb(
      dat = dat,
      pathway_id = id,
      exposure_spec = spec,
      scenario = baseline,
      registry = registry,
      offset_policy = "days_only",
      model_id = sprintf("Model3_%s_%s", outcome, id),
      result_class = RESULT_CLASS_EXPLORATORY,
      data_status = REAL_PROVENANCE
    )
    st <- fit$status
    st$outcome <- outcome
    st$model3_id <- id
    st$role <- s$role %||% "primary"
    status_rows[[key]] <- st
    if (!is.null(fit$estimates) && nrow(fit$estimates)) {
      est <- fit$estimates
      est$outcome <- outcome
      est$model3_id <- id
      est$role <- s$role %||% "primary"
      est$result_class <- RESULT_CLASS_EXPLORATORY
      est$data_status <- REAL_PROVENANCE
      estimate_rows[[key]] <- est
    }
  }
}

status_df <- dplyr::bind_rows(status_rows)
utils::write.csv(
  status_df,
  file.path(out_dir, "hogan_model3_climatology_status.csv"),
  row.names = FALSE,
  na = ""
)

if (!length(estimate_rows)) {
  stop("Model 3 produced no estimates")
}
est_df <- dplyr::bind_rows(estimate_rows)
utils::write.csv(
  est_df,
  file.path(out_dir, "hogan_model3_climatology_ladder.csv"),
  row.names = FALSE,
  na = ""
)

primary <- est_df[
  est_df$se_method == "NeweyWest_lag6" &
    (is.na(est_df$role) | est_df$role == "primary" | est_df$role == ""),
  ,
  drop = FALSE
]
# Four primary rows: 2 outcomes × warmer/cooler. Sensitivities have role=sensitivity.
primary <- est_df[
  est_df$se_method == "NeweyWest_lag6" &
    est_df$model3_id %in% c("M3W", "M3C"),
  ,
  drop = FALSE
]
if (nrow(primary) != 4L) {
  stop("Expected 4 Model 3 primary Newey–West lag-6 rows, found ", nrow(primary))
}
primary$q_value_bh_model3_primary4 <- stats::p.adjust(primary$p_value, method = "BH")
utils::write.csv(
  primary,
  file.path(out_dir, "table_model3_climatology_primary.csv"),
  row.names = FALSE,
  na = ""
)

message(
  "Wrote Model 3 climatology estimates to ",
  file.path(out_dir, "table_model3_climatology_primary.csv")
)
