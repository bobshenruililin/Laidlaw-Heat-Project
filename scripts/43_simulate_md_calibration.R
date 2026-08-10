#!/usr/bin/env Rscript
# 43_simulate_md_calibration.R
# Synthetic M|D calibration suite.
#
# Environment:
#   MD_PILOT_REPS   default 100
#   MD_CORE_REPS    default 500
#   MD_BOUNDARY_REPS default 1000
#   MD_WORKERS      default 1 (parallel only where safe)
#   MD_RUN_MODE     pilot|core|boundary (default pilot)
#
# Master seed: 20260810. Every output row: SYNTHETIC_CALIBRATION.
# Failed calibration is a valid result — gates are not gamed.
#
# Does not invent real CHD/HF findings.

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "md_likelihood.R"))
source(file.path("scripts", "md_calibration_helpers.R"))
if (file.exists(file.path("scripts", "final_model_helpers.R"))) {
  source(file.path("scripts", "final_model_helpers.R"))
}
root <- project_root()
setwd(root)
ensure_packages(c("yaml", "MASS", "glarma", "digest"))

PILOT_REPS <- as.integer(Sys.getenv("MD_PILOT_REPS", unset = "100"))
CORE_REPS <- as.integer(Sys.getenv("MD_CORE_REPS", unset = "500"))
BOUNDARY_REPS <- as.integer(Sys.getenv("MD_BOUNDARY_REPS", unset = "1000"))
N_WORKERS <- as.integer(Sys.getenv("MD_WORKERS", unset = "1"))
RUN_MODE <- Sys.getenv("MD_RUN_MODE", unset = "pilot")
MASTER_SEED <- MD_MASTER_SEED
DESIGN_VERSION <- "F1.1"
INPUT_HASH <- NA_character_

if (!is.finite(PILOT_REPS) || PILOT_REPS < 1L) PILOT_REPS <- 100L
if (!is.finite(CORE_REPS) || CORE_REPS < 1L) CORE_REPS <- 500L
if (!is.finite(BOUNDARY_REPS) || BOUNDARY_REPS < 1L) BOUNDARY_REPS <- 1000L
if (!is.finite(N_WORKERS) || N_WORKERS < 1L) N_WORKERS <- 1L

n_reps <- switch(
  RUN_MODE,
  pilot = PILOT_REPS,
  core = CORE_REPS,
  boundary = BOUNDARY_REPS,
  PILOT_REPS
)

out_dir <- file.path(root, "outputs", "calibration_md")
ckpt_dir <- file.path(out_dir, "checkpoints")
dir.create(ckpt_dir, recursive = TRUE, showWarnings = FALSE)

run_status_path <- file.path(out_dir, "md_calibration_run_status.csv")
raw_path <- file.path(out_dir, "md_calibration_raw_metrics.csv")
summary_path <- file.path(out_dir, "md_calibration_summary.csv")
gate_path <- file.path(out_dir, "md_calibration_gate_summary.csv")
scenario_path <- file.path(out_dir, "md_calibration_scenarios.csv")
run_tag <- paste0(RUN_MODE, "_", n_reps)
summary_mode_path <- file.path(
  out_dir, paste0("md_calibration_summary_", run_tag, ".csv")
)
gate_mode_path <- file.path(
  out_dir, paste0("md_calibration_gate_summary_", run_tag, ".csv")
)
scenario_mode_path <- file.path(
  out_dir, paste0("md_calibration_scenarios_", run_tag, ".csv")
)

append_run_status <- function(status, message, ...) {
  row <- data.frame(
    timestamp = as.character(Sys.time()),
    status = status,
    message = message,
    run_mode = RUN_MODE,
    n_reps = n_reps,
    n_workers = N_WORKERS,
    master_seed = MASTER_SEED,
    design_version = DESIGN_VERSION,
    input_hash = INPUT_HASH,
    data_status = MD_PROVENANCE_SYNTHETIC,
    stringsAsFactors = FALSE
  )
  dots <- list(...)
  if (length(dots)) row <- cbind(row, as.data.frame(dots, stringsAsFactors = FALSE))
  if (file.exists(run_status_path)) {
    old <- utils::read.csv(run_status_path, stringsAsFactors = FALSE)
    # Align columns
    alln <- union(names(old), names(row))
    for (nm in setdiff(alln, names(old))) old[[nm]] <- NA
    for (nm in setdiff(alln, names(row))) row[[nm]] <- NA
    row <- rbind(old[, alln, drop = FALSE], row[, alln, drop = FALSE])
  }
  write_csv_safe(row, run_status_path)
}

append_run_status("start", paste("Calibration start mode=", RUN_MODE))

# Weather design (public)
weather_path <- file.path(root, "data_processed", "md_daily_weather_design_2013_2023.csv")
if (!file.exists(weather_path)) {
  message("Weather design missing; building via script 40...")
  rc <- system2(
    Sys.which("Rscript"),
    args = file.path(root, "scripts", "40_build_daily_weather_design.R"),
    stdout = TRUE,
    stderr = TRUE
  )
  writeLines(rc, file.path(out_dir, "md_weather_build_log.txt"))
  if (!file.exists(weather_path)) {
    append_run_status("failed", "Could not build daily weather design")
    stop("Missing ", weather_path)
  }
}
weather <- utils::read.csv(weather_path, stringsAsFactors = FALSE)
weather$date <- as.Date(weather$date)
if (!all(weather$data_status == MD_PROVENANCE_PUBLIC_HKO)) {
  append_run_status("failed", "Weather design provenance not REAL_PUBLIC_HKO")
  stop("Weather design must be REAL_PUBLIC_HKO")
}

# Margins per outcome
margins_chd <- md_parse_expected_monthly_margins("chd", root = root)
margins_hf <- md_parse_expected_monthly_margins("hf", root = root)
core_fit_path <- file.path(root, "outputs", "tables", "cvd_core_model_fit.csv")
estimators <- c(
  "oracle_daily", "md", "monthly_nb", "glarma_ar1",
  "spillover_burden"
)

scenarios <- md_build_scenarios(include_edge = TRUE)
scenarios$n_reps_planned <- n_reps
scenarios$design_version <- DESIGN_VERSION
INPUT_HASH <- digest::digest(
  list(
    weather = weather[, c("date", "hot_night", "cold_day"), drop = FALSE],
    margins_chd = margins_chd,
    margins_hf = margins_hf,
    scenarios = scenarios,
    estimators = estimators
  ),
  algo = "sha256"
)
scenarios$input_hash <- INPUT_HASH
write_csv_safe(scenarios, scenario_path)
write_csv_safe(scenarios, scenario_mode_path)

registry <- if (exists("load_final_model_registry", mode = "function")) {
  load_final_model_registry(root = root)
} else if (requireNamespace("yaml", quietly = TRUE)) {
  yaml::read_yaml(file.path(root, "analysis_plan", "final_model_registry.yml"))
} else {
  stop("yaml required to load admission gates")
}

append_run_status(
  "design_ready",
  paste0("Calibration design hash=", INPUT_HASH)
)

# Deterministic seed stream: master + scenario index + rep
scenario_seed <- function(scenario_index, rep_id) {
  # Keep within 32-bit-ish range for set.seed portability
  as.integer((MASTER_SEED + scenario_index * 10007L + rep_id * 97L) %% 2147483646L + 1L)
}

run_one_rep <- function(scenario_row, scenario_params, scenario_index, rep_id,
                        weather, margins_chd, margins_hf, estimators) {
  params <- scenario_params
  margins <- if (identical(scenario_row$outcome, "hf")) margins_hf else margins_chd
  seed <- scenario_seed(scenario_index, rep_id)
  sim <- tryCatch(
    md_simulate_dgp(
      weather_daily = weather,
      margins = margins,
      exposure_col = scenario_row$exposure_col,
      kernel = scenario_row$kernel,
      effect_name = scenario_row$effect,
      overdispersion_phi = params$overdispersion_phi,
      ar1_rho = params$ar1_rho,
      depletion = params$depletion,
      covid_on = params$covid_on,
      seed = seed,
      outcome = scenario_row$outcome
    ),
    error = function(e) e
  )
  if (inherits(sim, "error")) {
    return(data.frame(
      scenario_id = scenario_row$scenario_id,
      cell_class = scenario_row$cell_class,
      scale = scenario_row$scale,
      outcome = scenario_row$outcome,
      effect = scenario_row$effect,
      effect_name = scenario_row$effect,
      kernel = scenario_row$kernel,
      serial_dependence = scenario_row$serial_dependence,
      depletion = scenario_row$depletion,
      covid_shock = scenario_row$covid_shock,
      overdispersion = scenario_row$overdispersion,
      exposure_col = scenario_row$exposure_col,
      rep_id = as.integer(rep_id),
      estimator = "dgp",
      ok = FALSE,
      message = conditionMessage(sim),
      estimate = NA_real_,
      se = NA_real_,
      conf_low = NA_real_,
      conf_high = NA_real_,
      converged = FALSE,
      hessian_pd = NA,
      hessian_condition = NA_real_,
      dispersion = NA_real_,
      loglik = NA_real_,
      beta_true = NA_real_,
      target_mapping = "dgp_failed",
      data_status = MD_PROVENANCE_SYNTHETIC,
      stringsAsFactors = FALSE
    ))
  }
  fits <- md_run_estimators(sim, estimators = estimators)
  rows <- lapply(fits, function(res) {
    md_estimator_result_to_row(res, scenario_row, rep_id, sim$beta_true)
  })
  do.call(rbind, rows)
}

# Parallel only for independent replicates within a scenario when workers > 1.
# Use PSOCK; each worker re-sources clean-room scripts (no shared RNG).
safe_parallel <- isTRUE(N_WORKERS > 1L) && requireNamespace("parallel", quietly = TRUE)

# summarise_scenario_raw lives in md_calibration_helpers.R as md_summarise_scenario_raw

all_raw <- list()
all_summary <- list()

for (i in seq_len(nrow(scenarios))) {
  sc <- scenarios[i, , drop = FALSE]
  sc_params <- md_scenario_params(sc, core_fit_path = core_fit_path)
  ckpt <- md_checkpoint_path(
    ckpt_dir,
    sc$scenario_id[[1]],
    RUN_MODE,
    n_reps,
    design_version = paste0(
      DESIGN_VERSION, "-", substr(INPUT_HASH, 1L, 12L)
    )
  )
  message(
    sprintf(
      "[%d/%d] %s (%s) reps=%d ckpt=%s",
      i, nrow(scenarios), sc$scenario_id[[1]], sc$cell_class[[1]], n_reps,
      basename(ckpt)
    )
  )

  if (file.exists(ckpt)) {
    message("  checkpoint hit: ", ckpt)
    raw_sc <- utils::read.csv(ckpt, stringsAsFactors = FALSE)
  } else {
    if (safe_parallel) {
      # Parallel over reps; each rep has deterministic seed — safe.
      # Workers re-source clean-room scripts (no shared mutable RNG stream).
      cl <- NULL
      raw_sc <- tryCatch(
        {
          cl <- parallel::makeCluster(N_WORKERS)
          parallel::clusterExport(
            cl,
            varlist = c(
              "root", "run_one_rep", "scenario_seed", "sc", "i", "weather",
              "margins_chd", "margins_hf", "sc_params", "estimators",
              "MASTER_SEED"
            ),
            envir = environment()
          )
          parallel::clusterEvalQ(cl, {
            setwd(root)
            source(file.path(root, "scripts", "utils.R"))
            source(file.path(root, "scripts", "md_likelihood.R"))
            source(file.path(root, "scripts", "md_calibration_helpers.R"))
            suppressPackageStartupMessages({
              if (requireNamespace("splines", quietly = TRUE)) library(splines)
              if (requireNamespace("MASS", quietly = TRUE)) library(MASS)
            })
            NULL
          })
          parts <- parallel::parLapply(cl, seq_len(n_reps), function(r) {
            run_one_rep(
              scenario_row = sc,
              scenario_params = sc_params,
              scenario_index = i,
              rep_id = r,
              weather = weather,
              margins_chd = margins_chd,
              margins_hf = margins_hf,
              estimators = estimators
            )
          })
          do.call(rbind, parts)
        },
        error = function(e) {
          append_run_status(
            "parallel_failed",
            paste(sc$scenario_id[[1]], conditionMessage(e)),
            scenario_id = sc$scenario_id[[1]]
          )
          stop(e)
        },
        finally = {
          if (!is.null(cl) && inherits(cl, "cluster")) {
            try(parallel::stopCluster(cl), silent = TRUE)
          }
        }
      )
    } else {
      parts <- vector("list", n_reps)
      for (r in seq_len(n_reps)) {
        parts[[r]] <- run_one_rep(
          scenario_row = sc,
          scenario_params = sc_params,
          scenario_index = i,
          rep_id = r,
          weather = weather,
          margins_chd = margins_chd,
          margins_hf = margins_hf,
          estimators = estimators
        )
      }
      raw_sc <- do.call(rbind, parts)
    }
    raw_sc$data_status <- MD_PROVENANCE_SYNTHETIC
    write_csv_safe(raw_sc, ckpt)
  }

  all_raw[[i]] <- raw_sc
  summ <- md_summarise_scenario_raw(raw_sc)
  if (!is.null(summ)) all_summary[[i]] <- summ
  append_run_status(
    "scenario_complete",
    paste("Finished", sc$scenario_id[[1]]),
    scenario_id = sc$scenario_id[[1]],
    n_rows = nrow(raw_sc)
  )
}

raw_all <- do.call(rbind, all_raw)
raw_all$data_status <- MD_PROVENANCE_SYNTHETIC
write_csv_safe(raw_all, raw_path)

summary_all <- do.call(rbind, all_summary)
summary_all$data_status <- MD_PROVENANCE_SYNTHETIC
write_csv_safe(summary_all, summary_path)
write_csv_safe(summary_all, summary_mode_path)

gates <- md_evaluate_gates(summary_all, registry = registry, root = root)
gates$data_status <- MD_PROVENANCE_SYNTHETIC
write_csv_safe(gates, gate_path)
write_csv_safe(gates, gate_mode_path)

admission <- unique(as.character(gates$admission_decision))
append_run_status(
  "complete",
  paste0(
    "Calibration complete. admission_decision=",
    paste(admission, collapse = ","),
    "; all_passed=", all(gates$passed)
  ),
  admission_decision = paste(admission, collapse = ","),
  all_gates_passed = all(gates$passed)
)

message(
  "Calibration finished. Gate decision: ",
  paste(admission, collapse = ","),
  " (failed calibration is a valid result)"
)
