#!/usr/bin/env Rscript
# 20_fit_pathway_panel.R
# Fit all enabled pathways from analysis_plan/pathway_registry.yml on the stroke panel.

source(file.path("scripts", "utils.R"))
root <- project_root()
setwd(root)
cfg <- load_config(root)
ensure_packages(c("yaml", "dplyr", "MASS", "splines", "sandwich", "lmtest"))

panel_path <- file.path(root, "data_processed", "stroke_analysis_panel.csv")
if (!file.exists(panel_path)) stop("Missing ", panel_path, " — run 08d_merge_stroke_panel.R first")

panel <- utils::read.csv(panel_path, stringsAsFactors = FALSE)
reg <- yaml::read_yaml(file.path(root, "analysis_plan", "pathway_registry.yml"))

is_synthetic <- any(grepl("SYNTHETIC", panel$data_status %||% ""))
has_age_sex <- !all(panel$age_group %in% c("all", "", NA)) && !all(panel$sex %in% c("all", "", NA))
has_subtype <- length(unique(na.omit(panel$stroke_type))) > 1 &&
  !all(panel$stroke_type %in% c("stroke_all", "unspecified", NA))
has_flu <- "flu_indicator" %in% names(panel) && any(!is.na(panel$flu_indicator))
pol_ok <- all(c("NO2", "O3", "PM25") %in% names(panel)) &&
  !any(grepl("PLACEHOLDER", panel$pollution_data_status %||% ""))

panel <- panel |>
  dplyr::mutate(
    month_f = factor(month),
    covid_phase = if ("covid_phase" %in% names(panel)) factor(covid_phase) else NA,
    age_group = factor(age_group),
    sex = factor(sex),
    stroke_type = factor(stroke_type),
    age_band65 = factor(age_band65)
  )

extract_rr <- function(model, vcov_mat = NULL, keep_pattern = NULL) {
  ct <- tryCatch(
    {
      if (is.null(vcov_mat)) summary(model)$coefficients else as.matrix(lmtest::coeftest(model, vcov. = vcov_mat))
    },
    error = function(e) summary(model)$coefficients
  )
  nm <- rownames(ct)
  if (!is.null(keep_pattern)) nm <- nm[grepl(keep_pattern, nm)]
  if (!length(nm)) return(data.frame())
  data.frame(
    term = nm,
    estimate = ct[nm, 1],
    std_error = ct[nm, 2],
    statistic = ct[nm, 3],
    p_value = ct[nm, 4],
    rr = exp(ct[nm, 1]),
    rr_low = exp(ct[nm, 1] - 1.96 * ct[nm, 2]),
    rr_high = exp(ct[nm, 1] + 1.96 * ct[nm, 2]),
    stringsAsFactors = FALSE
  )
}

build_rhs <- function(exposures, scale = NULL, extras = character(), dat) {
  terms <- character()
  for (ex in exposures) {
    if (!ex %in% names(dat)) next
    if (!is.null(scale) && !is.na(scale)) {
      terms <- c(terms, sprintf("I(%s / %s)", ex, scale))
    } else {
      terms <- c(terms, ex)
    }
  }
  # core controls
  terms <- c(terms, "month_f", paste0("splines::ns(time_index, df = ", cfg$modeling$time_trend_df %||% 4, ")"))
  if (has_age_sex) terms <- c(terms, "age_group", "sex")

  if ("covid_phase" %in% extras && "covid_phase" %in% names(dat)) terms <- c(terms, "covid_phase")
  if ("public_holiday_days" %in% extras && "public_holiday_days" %in% names(dat)) terms <- c(terms, "public_holiday_days")
  if ("chinese_new_year_month" %in% extras && "chinese_new_year_month" %in% names(dat)) terms <- c(terms, "chinese_new_year_month")
  if ("absolute_humidity" %in% extras && "absolute_humidity" %in% names(dat)) terms <- c(terms, "absolute_humidity")
  if ("flu_indicator" %in% extras && has_flu) terms <- c(terms, "flu_indicator")
  if ("age_band65" %in% extras && has_age_sex) {
    # replace age_group with band interaction on first exposure
    terms <- setdiff(terms, "age_group")
    if (length(exposures)) {
      terms <- c(terms, "age_band65", sprintf("%s:age_band65", exposures[[1]]))
    } else {
      terms <- c(terms, "age_band65")
    }
  }
  unique(terms)
}

fit_one <- function(pathway_id, spec, dat) {
  extras <- spec$extras %||% list()
  if (is.null(extras)) extras <- list()
  extras <- unlist(extras)

  if (identical(spec$grain, "age_sex_required") && !has_age_sex) {
    return(list(status = "skipped_no_age_sex", estimates = NULL, fit = NULL))
  }
  if ("subtype_strata" %in% extras && !has_subtype) {
    return(list(status = "skipped_no_subtype", estimates = NULL, fit = NULL))
  }
  if ("flu_indicator" %in% extras && !has_flu) {
    return(list(status = "skipped_no_flu", estimates = NULL, fit = NULL))
  }
  if ("pollution_staged" %in% extras && !pol_ok) {
    return(list(status = "skipped_no_pollution", estimates = NULL, fit = NULL))
  }

  d <- dat
  if ("pre_covid_only" %in% extras) {
    d <- d |> dplyr::filter(year < 2020)
  }

  # Pollution staged: fit nested models; return final multi-pollutant as primary row set + stage tag
  stages <- list(none = character())
  if ("pollution_staged" %in% extras) {
    stages <- list(
      none = character(),
      NO2 = "NO2",
      PM25 = "PM25",
      O3 = "O3",
      multi = c("NO2", "PM25", "O3")
    )
  }

  out_est <- list()
  out_fit <- list()
  for (st in names(stages)) {
    rhs_terms <- build_rhs(spec$exposures, spec$scale, setdiff(extras, "pollution_staged"), d)
    rhs_terms <- c(rhs_terms, stages[[st]])
    # drop missing columns
    rhs_terms <- rhs_terms[vapply(rhs_terms, function(t) {
      # allow I() and interactions and splines
      if (grepl("splines::|I\\(|:", t)) return(TRUE)
      t %in% names(d)
    }, logical(1))]

    if (!length(intersect(spec$exposures, names(d)))) {
      return(list(status = "skipped_missing_exposure", estimates = NULL, fit = NULL))
    }

    fml <- as.formula(paste("n_events ~", paste(rhs_terms, collapse = " + "), "+ offset(offset_log)"))
    model <- tryCatch(
      MASS::glm.nb(fml, data = d),
      error = function(e) {
        message(pathway_id, " glm.nb failed (", conditionMessage(e), "); trying quasipoisson")
        stats::glm(fml, data = d, family = stats::quasipoisson())
      }
    )

    vcov_mat <- tryCatch(
      {
        if (has_age_sex) {
          sandwich::vcovCL(model, cluster = ~ month_id, type = "HC1")
        } else {
          sandwich::vcovHC(model, type = "HC1")
        }
      },
      error = function(e) NULL
    )

    keep_pat <- paste0("(", paste(c(spec$exposures, stages[[st]], "age_band65"), collapse = "|"), ")")
    est <- extract_rr(model, vcov_mat, keep_pattern = keep_pat)
    if (!nrow(est)) next
    est$pathway_id <- pathway_id
    est$pathway_title <- spec$title
    est$pollution_stage <- st
    est$data_status <- paste(unique(d$data_status), collapse = ";")
    est$n_rows <- nrow(d)
    est$n_months <- length(unique(d$month_id))
    out_est[[st]] <- est
    out_fit[[st]] <- data.frame(
      pathway_id = pathway_id,
      pollution_stage = st,
      aic = tryCatch(AIC(model), error = function(e) NA_real_),
      theta = tryCatch(model$theta, error = function(e) NA_real_),
      converged = tryCatch(model$converged, error = function(e) NA),
      family = paste(class(model), collapse = "/"),
      stringsAsFactors = FALSE
    )
  }

  if (!length(out_est)) return(list(status = "failed", estimates = NULL, fit = NULL))
  list(
    status = "ok",
    estimates = dplyr::bind_rows(out_est),
    fit = dplyr::bind_rows(out_fit)
  )
}

results_est <- list()
results_fit <- list()
status_rows <- list()

for (pid in names(reg$pathways)) {
  spec <- reg$pathways[[pid]]
  if (!isTRUE(spec$enabled)) {
    status_rows[[pid]] <- data.frame(pathway_id = pid, status = "disabled", stringsAsFactors = FALSE)
    next
  }
  message("Fitting ", pid, " — ", spec$title)
  res <- fit_one(pid, spec, panel)
  status_rows[[pid]] <- data.frame(pathway_id = pid, status = res$status, stringsAsFactors = FALSE)
  if (!is.null(res$estimates)) results_est[[pid]] <- res$estimates
  if (!is.null(res$fit)) results_fit[[pid]] <- res$fit
}

est_df <- dplyr::bind_rows(results_est)
fit_df <- dplyr::bind_rows(results_fit)
stat_df <- dplyr::bind_rows(status_rows)

out_tab <- file.path(root, "outputs", "tables")
dir.create(out_tab, recursive = TRUE, showWarnings = FALSE)
write_csv_safe(est_df, file.path(out_tab, "pathway_panel_estimates.csv"))
write_csv_safe(fit_df, file.path(out_tab, "pathway_panel_fit_stats.csv"))
write_csv_safe(stat_df, file.path(out_tab, "pathway_panel_status.csv"))

# Human summary
out_rep <- file.path(root, "outputs", "reports")
dir.create(out_rep, recursive = TRUE, showWarnings = FALSE)
headline <- paste(reg$headline_proposal %||% c("P02", "P04"), collapse = ", ")
lines <- c(
  "# Pathway panel summary",
  "",
  paste0("- **Run at:** ", as.character(Sys.time())),
  paste0("- **Panel rows:** ", nrow(panel)),
  paste0("- **Synthetic:** ", is_synthetic),
  paste0("- **Age×sex grain:** ", has_age_sex),
  paste0("- **Headline proposal:** ", headline),
  "",
  "## Pathway status",
  "",
  paste0("| ID | Status |"),
  paste0("|---|---|"),
  paste0("| ", stat_df$pathway_id, " | ", stat_df$status, " |"),
  "",
  "## Notes",
  "",
  if (is_synthetic) {
    "**SYNTHETIC dry-run — do not interpret coefficients as findings.**"
  } else {
    "Real aggregate run. Apply Gate 3 before treating any single pathway as primary."
  },
  "",
  "Full estimates: `outputs/tables/pathway_panel_estimates.csv`"
)
writeLines(lines, file.path(out_rep, "pathway_panel_summary.md"))

message(
  "Pathway panel complete. OK=", sum(stat_df$status == "ok"),
  " / enabled attempts; estimates rows=", nrow(est_df)
)
if (is_synthetic) message("WARNING: SYNTHETIC coefficients — not for manuscript claims.")
