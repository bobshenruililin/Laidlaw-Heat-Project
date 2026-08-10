#!/usr/bin/env Rscript
# 38_cns_final_release_artifacts.R
# Augment (do not rebuild/delete) the disclosure-minimised CHD/HF release.
#
# Preserves Tables 1–3 and Figures 1–4 from script 33.
# Adds Table 4 uncertainty ladder, analysis availability, claim ledger v2,
# methods-feasibility supplement (weather/spillover/calibration), and figures.
#
# Never renames HA_APPROVED_AGGREGATE → REAL.
# Never treats SYNTHETIC_CALIBRATION as CHD/HF health evidence.
# Never unlinks outputs/release_chd_hf/.
# Never edits outputs/calibration_md/ (read-only copy into supplement).

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "release_check_helpers.R"))
root <- project_root()
setwd(root)
ensure_packages(c("dplyr", "tidyr", "ggplot2", "scales", "svglite", "yaml"))

tables_dir <- file.path(root, "outputs", "tables")
cal_dir <- file.path(root, "outputs", "calibration_md")
release_dir <- file.path(root, "outputs", "release_chd_hf")
release_tables <- file.path(release_dir, "tables")
release_figures <- file.path(release_dir, "figures")
release_supp <- file.path(release_dir, "supplement")
mf_dir <- file.path(release_dir, METHODS_FEASIBILITY_RELDIR)

if (!dir.exists(release_dir)) {
  stop(
    "Canonical release missing: ", release_dir,
    ". Run script 33 before augmentation."
  )
}
# Hard guard: never wipe the existing release.
if (identical(Sys.getenv("FORCE_REBUILD_RELEASE", unset = "0"), "1")) {
  stop("FORCE_REBUILD_RELEASE is forbidden in script 38; augment only")
}

dir.create(release_tables, recursive = TRUE, showWarnings = FALSE)
dir.create(release_figures, recursive = TRUE, showWarnings = FALSE)
dir.create(release_supp, recursive = TRUE, showWarnings = FALSE)
dir.create(mf_dir, recursive = TRUE, showWarnings = FALSE)

# Preserve existing main artifacts (existence check only; do not overwrite).
required_preserved <- c(
  file.path(release_tables, "table1_outcome_summary.csv"),
  file.path(release_tables, "table2_core_models.csv"),
  file.path(release_tables, "table3_robustness_summary.csv"),
  file.path(release_tables, "claim_ledger.csv"),
  file.path(release_figures, "figure1_indexed_outcome_series.svg"),
  file.path(release_figures, "figure2_seasonal_pattern.svg"),
  file.path(release_figures, "figure3_core_forest.svg"),
  file.path(release_figures, "figure4_trend_depletion_sensitivity.svg")
)
missing_preserved <- required_preserved[!file.exists(required_preserved)]
if (length(missing_preserved)) {
  stop(
    "Refusing to augment: missing preserved release artifacts:\n- ",
    paste(missing_preserved, collapse = "\n- ")
  )
}

copy_file_safe <- function(src, dest, overwrite = TRUE) {
  if (!file.exists(src)) return(FALSE)
  dir.create(dirname(dest), recursive = TRUE, showWarnings = FALSE)
  file.copy(src, dest, overwrite = overwrite)
}

theme_pub <- function() {
  ggplot2::theme_minimal(base_size = 11) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(face = "bold", size = 12),
      plot.subtitle = ggplot2::element_text(colour = "grey30"),
      panel.grid.minor = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(face = "bold"),
      legend.position = "bottom"
    )
}

save_plot_multi <- function(plot, stem_dir, stem, width, height) {
  dir.create(stem_dir, recursive = TRUE, showWarnings = FALSE)
  for (ext in c("png", "pdf", "svg")) {
    ggplot2::ggsave(
      file.path(stem_dir, paste0(stem, ".", ext)),
      plot,
      width = width,
      height = height,
      dpi = if (identical(ext, "png")) 400 else 300
    )
  }
}

palette_outcome <- c(
  "Coronary heart disease" = "#bd5a32",
  "Heart failure" = "#276b79",
  chd = "#bd5a32",
  hf = "#276b79"
)
palette_se <- c(
  Model = "#4d4d4d",
  HC1 = "#2b6f91",
  NW3 = "#5b8c5a",
  NW6 = "#174d5b"
)

# =============================================================================
# Table 4 — uncertainty ladder (12 core contrasts × 4 SE methods)
# =============================================================================
core_path <- file.path(tables_dir, "cvd_core_robust_estimates.csv")
if (!file.exists(core_path)) {
  stop("Missing analysis-of-record robust estimates: ", core_path)
}
core <- utils::read.csv(core_path, stringsAsFactors = FALSE)
ladder <- build_uncertainty_ladder(core)
ladder_check <- validate_uncertainty_ladder(ladder)
if (!isTRUE(ladder_check$ok)) stop("Uncertainty ladder invalid: ", ladder_check$detail)

table4 <- ladder |>
  dplyr::transmute(
    outcome,
    outcome_label,
    pathway_id,
    exposure,
    exposure_label,
    contrast,
    se_method,
    se_method_label,
    rr,
    rr_low,
    rr_high,
    count_ratio_95CI,
    p_value,
    n_months,
    family,
    offset_policy,
    data_status,
    result_class,
    manuscript_role
  )
write_csv_safe(table4, file.path(release_tables, "table4_uncertainty_ladder.csv"))

# =============================================================================
# Analysis availability (ensemble / prediction / M|D) — blockers as facts
# =============================================================================
availability_sources <- list(
  list(
    script_id = "36_cvd_final_model_ensemble",
    analysis = "final_model_ensemble",
    real_candidates = c(
      "cvd_final_ensemble_estimates.csv",
      "cvd_final_ensemble_se_ladder.csv",
      "cvd_final_ensemble_fit_status.csv"
    ),
    blocker = "cvd_final_ensemble_blocker.csv"
  ),
  list(
    script_id = "37_cvd_prediction_specification",
    analysis = "prediction_specification",
    real_candidates = c(
      "cvd_prediction_scores.csv",
      "cvd_prediction_fit_status.csv",
      "cvd_specification_curve_estimates.csv",
      "cvd_specification_curve_summary.csv"
    ),
    blocker = "cvd_prediction_spec_blocker.csv"
  ),
  list(
    script_id = "41_fit_md_constrained",
    analysis = "md_constrained_real",
    real_candidates = c(
      "md_constrained_estimates.csv",
      "md_constrained_fit_status.csv"
    ),
    blocker = "md_constrained_blocker.csv"
  )
)

avail_rows <- list()
copied_real <- list()
for (spec in availability_sources) {
  blocker_path <- file.path(tables_dir, spec$blocker)
  real_hits <- file.path(tables_dir, spec$real_candidates)
  real_present <- real_hits[file.exists(real_hits)]

  # Prefer explicit blocker when real outputs absent.
  if (length(real_present)) {
    # Copy only if every present real file is HA_APPROVED_AGGREGATE (or lacks
    # synthetic labels). Never copy SYNTHETIC into main release tables.
    for (rp in real_present) {
      dat <- tryCatch(
        utils::read.csv(rp, stringsAsFactors = FALSE, nrows = 2000),
        error = function(e) NULL
      )
      if (is.null(dat)) next
      ds <- if ("data_status" %in% names(dat)) unique(as.character(dat$data_status)) else NA_character_
      if (any(grepl("SYNTHETIC", ds, ignore.case = TRUE), na.rm = TRUE)) {
        avail_rows[[paste(spec$analysis, basename(rp), "synth")]] <-
          normalise_availability_row(
            spec$script_id, spec$analysis,
            status = "BLOCKED_SYNTHETIC_CONTENT",
            message = paste0(
              "Refused to copy ", basename(rp),
              "; contains SYNTHETIC provenance"
            ),
            data_status = paste(ds, collapse = ","),
            artifact_path = rp
          )
        next
      }
      if (!all(is.na(ds)) && !all(ds == RELEASE_REAL_PROVENANCE)) {
        # Allow empty data_status only with non-synthetic content for status tables
        if (!all(ds %in% c(RELEASE_REAL_PROVENANCE, ""))) {
          avail_rows[[paste(spec$analysis, basename(rp), "prov")]] <-
            normalise_availability_row(
              spec$script_id, spec$analysis,
              status = "BLOCKED_PROVENANCE",
              message = paste0("Unexpected provenance in ", basename(rp)),
              data_status = paste(ds, collapse = ","),
              artifact_path = rp
            )
          next
        }
      }
      dest <- file.path(release_supp, basename(rp))
      copy_file_safe(rp, dest)
      copied_real[[basename(rp)]] <- dest
      st <- if ("status" %in% names(dat)) {
        paste(unique(as.character(dat$status)), collapse = ";")
      } else {
        "OK"
      }
      avail_rows[[paste(spec$analysis, basename(rp))]] <- normalise_availability_row(
        spec$script_id, spec$analysis,
        status = st,
        message = paste0("Copied real artifact to supplement/", basename(rp)),
        result_class = if ("result_class" %in% names(dat)) {
          paste(unique(as.character(dat$result_class)), collapse = ";")
        } else {
          "EXPLORATORY_POST_OUTCOME"
        },
        data_status = if (all(is.na(ds))) RELEASE_REAL_PROVENANCE else paste(ds, collapse = ","),
        artifact_path = dest,
        availability = "available"
      )
    }
  } else if (file.exists(blocker_path)) {
    br <- read_blocker_or_status(blocker_path, spec$script_id, spec$analysis)
    # Also copy blocker into methods_feasibility as an availability record
    copy_file_safe(
      blocker_path,
      file.path(mf_dir, basename(blocker_path))
    )
    # Mirror into release tables as availability (not a completed analysis)
    avail_rows[[spec$analysis]] <- br
  } else {
    avail_rows[[spec$analysis]] <- normalise_availability_row(
      spec$script_id, spec$analysis,
      status = "ABSENT",
      message = "Neither real outputs nor blocker table present",
      artifact_path = blocker_path
    )
  }
}

# Calibration availability (methods-feasibility only; never a health claim)
cal_summary_path <- file.path(cal_dir, "md_calibration_summary.csv")
cal_gate_path <- file.path(cal_dir, "md_calibration_gate_summary.csv")
cal_fail_note <- file.path(cal_dir, "md_pilot_f1_0_failure_note.md")
cal_f12_report <- file.path(cal_dir, "md_calibration_f1_2_decision_report.md")
cal_available <- file.exists(cal_summary_path) && file.exists(cal_gate_path)
avail_rows[["calibration_md"]] <- normalise_availability_row(
  "43_simulate_md_calibration",
  "synthetic_calibration_methods_feasibility",
  status = if (cal_available) {
    "AVAILABLE_METHODS_FEASIBILITY_ONLY"
  } else {
    "ABSENT"
  },
  message = if (cal_available) {
    paste0(
      "Canonical calibration summary/gates present under ",
      METHODS_FEASIBILITY_RELDIR,
      " only; not a health finding"
    )
  } else {
    "Canonical calibration summary/gates absent; figures deferred"
  },
  result_class = "METHODS_FEASIBILITY",
  # Keep the SYNTHETIC token out of main tables/; quarantine lives in supplement.
  data_status = NA_character_,
  artifact_path = file.path(release_dir, METHODS_FEASIBILITY_RELDIR),
  availability = if (cal_available) {
    "available_methods_feasibility_only"
  } else {
    "blocked"
  }
)

availability <- dplyr::bind_rows(avail_rows)
availability$artifact_path <- sub(
  paste0("^", normalizePath(root, winslash = "/"), "/?"),
  "",
  gsub("\\\\", "/", availability$artifact_path)
)
write_csv_safe(
  availability,
  file.path(release_tables, "analysis_availability.csv")
)

# =============================================================================
# Claim ledger v2 — existing claims + tier + post-outcome/multiplicity/SE
# =============================================================================
ledger_v1 <- utils::read.csv(
  file.path(release_tables, "claim_ledger.csv"),
  stringsAsFactors = FALSE
)
table2 <- utils::read.csv(
  file.path(release_tables, "table2_core_models.csv"),
  stringsAsFactors = FALSE
)

id_check <- table2_claim_ledger_identity(table2, ledger_v1)
if (!isTRUE(id_check$ok)) {
  stop("table2↔claim_ledger identity failed before v2 build: ", id_check$detail)
}
round_check <- claim_text_rounding_ok(ledger_v1)
if (!isTRUE(round_check$ok)) {
  warning("claim_text rounding check: ", round_check$detail)
}
bh_check <- bh_q_identity(ledger_v1$p_value, ledger_v1$q_value_core_bh)
if (!isTRUE(bh_check$ok)) {
  stop("BH q recomputation failed for existing ledger: ", bh_check$detail)
}

# Load claim-tier definitions if present (informational; do not invent claims).
tier_path <- file.path(root, "analysis_plan", "final_claim_tiers.yml")
tier_note <- if (file.exists(tier_path)) {
  "tiers from analysis_plan/final_claim_tiers.yml"
} else {
  "tiers.yml absent; using protocol defaults"
}

# Supported = complete real estimates in release tables.
# Exploratory qualifier retained because Gate 3 is open / post-outcome protocol.
claim_ledger_v2 <- ledger_v1 |>
  dplyr::mutate(
    claim_tier = "supported",
    claim_tier_qualifier = "exploratory_complete_panel",
    post_outcome_context = paste0(
      "Post-outcome exploratory protocol (frozen 2026-08-10); ",
      "not prospectively confirmatory; Gate 3 headline unset"
    ),
    multiplicity_context = paste0(
      "Benjamini-Hochberg q_value_core_bh across the 12 amended-core ",
      "NW6 contrasts (CHD+HF × six exposures); q recomputed in release checks"
    ),
    se_context = paste0(
      "Primary display SE = NeweyWest_lag6 (analysis of record). ",
      "Table 4 shows the full Model/HC1/NW3/NW6 ladder; ",
      "SE method is not selected because a CI excludes 1"
    ),
    result_class = "ANALYSIS_OF_RECORD",
    data_status = provenance,
    source_table_v2 = "outputs/release_chd_hf/tables/table2_core_models.csv",
    uncertainty_ladder_table = "outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv",
    tier_source = tier_note
  )

# Do not append new real claims for blocked ensemble/prediction/M|D analyses.
write_csv_safe(
  claim_ledger_v2,
  file.path(release_tables, "claim_ledger_v2.csv")
)

# =============================================================================
# Methods-feasibility supplement copies (provenance intact)
# =============================================================================
mf_copies <- list()
record_mf <- function(src, dest_name, data_status, result_class, note) {
  dest <- file.path(mf_dir, dest_name)
  ok <- copy_file_safe(src, dest)
  mf_copies[[dest_name]] <<- data.frame(
    artifact = dest_name,
    source_path = src,
    copied = isTRUE(ok),
    data_status = data_status,
    result_class = result_class,
    note = note,
    stringsAsFactors = FALSE
  )
  invisible(ok)
}

# Public weather source lock / validation
record_mf(
  file.path(tables_dir, "weather_definition_source_lock.csv"),
  "weather_definition_source_lock.csv",
  "REAL_PUBLIC_HKO", "EXPOSURE_AUDIT",
  "Source-locked definition implementations"
)
record_mf(
  file.path(tables_dir, "weather_definition_source_validation.csv"),
  "weather_definition_source_validation.csv",
  "REAL_PUBLIC_HKO", "EXPOSURE_AUDIT",
  "Primary-source reproduction checks"
)
record_mf(
  file.path(tables_dir, "weather_event_morphology_audit.csv"),
  "weather_event_morphology_audit.csv",
  "REAL_PUBLIC_HKO", "EXPOSURE_AUDIT",
  "Spillover event morphology audit"
)
record_mf(
  file.path(root, "data_processed", "exposures_spillover_monthly_2013_2023.csv"),
  "exposures_spillover_monthly_2013_2023.csv",
  "REAL_PUBLIC_HKO", "EXPOSURE_AUDIT",
  "Calendar-spillover monthly weather exposure audit (no health outcomes)"
)
record_mf(
  file.path(root, "outputs", "reports", "weather_spillover_exposure_build.md"),
  "weather_spillover_exposure_build.md",
  "REAL_PUBLIC_HKO", "EXPOSURE_AUDIT",
  "Spillover build note"
)

# Calibration summary / gates / F1.0 failure note (SYNTHETIC_CALIBRATION only)
if (file.exists(cal_summary_path)) {
  record_mf(
    cal_summary_path,
    "md_calibration_summary.csv",
    RELEASE_SYNTHETIC_CALIBRATION, "METHODS_FEASIBILITY",
    "Synthetic calibration summary; not CHD/HF health findings"
  )
} else {
  mf_copies[["md_calibration_summary.csv"]] <- data.frame(
    artifact = "md_calibration_summary.csv",
    source_path = cal_summary_path,
    copied = FALSE,
    data_status = RELEASE_SYNTHETIC_CALIBRATION,
    result_class = "METHODS_FEASIBILITY",
    note = "ABSENT: canonical calibration summary not yet available",
    stringsAsFactors = FALSE
  )
}
if (file.exists(cal_gate_path)) {
  record_mf(
    cal_gate_path,
    "md_calibration_gate_summary.csv",
    RELEASE_SYNTHETIC_CALIBRATION, "METHODS_FEASIBILITY",
    "Synthetic calibration admission gates"
  )
} else {
  mf_copies[["md_calibration_gate_summary.csv"]] <- data.frame(
    artifact = "md_calibration_gate_summary.csv",
    source_path = cal_gate_path,
    copied = FALSE,
    data_status = RELEASE_SYNTHETIC_CALIBRATION,
    result_class = "METHODS_FEASIBILITY",
    note = "ABSENT: canonical calibration gate summary not yet available",
    stringsAsFactors = FALSE
  )
}
if (file.exists(cal_fail_note)) {
  record_mf(
    cal_fail_note,
    "md_pilot_f1_0_failure_note.md",
    RELEASE_SYNTHETIC_CALIBRATION, "METHODS_FEASIBILITY",
    "F1.0 pilot nuisance-seasonality failure note"
  )
}
if (file.exists(cal_f12_report)) {
  record_mf(
    cal_f12_report,
    "md_calibration_f1_2_decision_report.md",
    RELEASE_SYNTHETIC_CALIBRATION, "METHODS_FEASIBILITY",
    "Strict worst-cell F1.2 gate decision; no real coefficient admitted"
  )
}
# Optional pilot gate echo (still synthetic / methods only)
pilot_gate <- file.path(cal_dir, "md_pilot_f1_0_gate_summary.csv")
if (file.exists(pilot_gate)) {
  record_mf(
    pilot_gate,
    "md_pilot_f1_0_gate_summary.csv",
    RELEASE_SYNTHETIC_CALIBRATION, "METHODS_FEASIBILITY",
    "F1.0 pilot gate summary retained for audit"
  )
}

mf_manifest <- dplyr::bind_rows(mf_copies)
write_csv_safe(mf_manifest, file.path(mf_dir, "methods_feasibility_manifest.csv"))

# =============================================================================
# Figures
# =============================================================================

# Figure 5 — SE-method ladder forest (real HA ladder; companion to Table 4)
ladder_plot <- table4 |>
  dplyr::mutate(
    exposure_label = factor(
      exposure_label,
      levels = rev(unname(CORE_EXPOSURE_LABELS))
    ),
    outcome_label = factor(
      outcome_label,
      levels = unname(OUTCOME_LABELS_RELEASE)
    ),
    se_method_label = factor(
      se_method_label,
      levels = unname(SE_LADDER_DISPLAY)
    )
  )
p5 <- ggplot2::ggplot(
  ladder_plot,
  ggplot2::aes(
    rr, exposure_label,
    xmin = rr_low, xmax = rr_high,
    colour = se_method_label
  )
) +
  ggplot2::geom_vline(xintercept = 1, linetype = "dashed", colour = "grey45") +
  ggplot2::geom_errorbar(
    orientation = "y",
    width = 0.18,
    position = ggplot2::position_dodge(width = 0.7)
  ) +
  ggplot2::geom_point(
    size = 1.7,
    position = ggplot2::position_dodge(width = 0.7)
  ) +
  ggplot2::facet_wrap(~outcome_label, ncol = 1) +
  ggplot2::scale_x_log10() +
  ggplot2::scale_colour_manual(values = palette_se) +
  ggplot2::labs(
    title = "Uncertainty ladder across SE methods",
    subtitle = "Negative binomial; days-in-month offset; Model, HC1, NW3, NW6",
    x = "Count ratio (log scale)",
    y = NULL,
    colour = "SE method"
  ) +
  theme_pub()
save_plot_multi(p5, release_figures, "figure5_se_method_ladder", 9.5, 7.2)

# Spillover event counts (public weather audit)
events_path <- file.path(mf_dir, "weather_event_morphology_audit.csv")
if (file.exists(events_path)) {
  events <- utils::read.csv(events_path, stringsAsFactors = FALSE)
  event_counts <- events |>
    dplyr::count(definition_id, name = "n_events") |>
    dplyr::mutate(
      definition_id = factor(
        definition_id,
        levels = c("wang_vhd5", "wang_hn5", "wang_2d3n", "li_hw")
      )
    )
  p_sp <- ggplot2::ggplot(
    event_counts,
    ggplot2::aes(definition_id, n_events, fill = definition_id)
  ) +
    ggplot2::geom_col(width = 0.7, colour = NA) +
    ggplot2::scale_fill_manual(
      values = c(
        wang_vhd5 = "#bd5a32",
        wang_hn5 = "#276b79",
        wang_2d3n = "#5b8c5a",
        li_hw = "#8a6a3d"
      ),
      guide = "none"
    ) +
    ggplot2::labs(
      title = "Source-locked heat-event counts, 2013-2023",
      subtitle = "Public HKO morphology audit; no health outcomes",
      x = NULL,
      y = "Events"
    ) +
    theme_pub()
  save_plot_multi(
    p_sp, mf_dir, "figure_spillover_event_counts", 7.5, 4.8
  )
}

# Calibration coverage / type-I and gate panel (only when summary exists)
mf_summary <- file.path(mf_dir, "md_calibration_summary.csv")
mf_gates <- file.path(mf_dir, "md_calibration_gate_summary.csv")

if (file.exists(mf_summary)) {
  cal <- utils::read.csv(mf_summary, stringsAsFactors = FALSE)
  if (!"data_status" %in% names(cal) ||
      !all(cal$data_status == RELEASE_SYNTHETIC_CALIBRATION)) {
    warning(
      "Calibration summary missing uniform SYNTHETIC_CALIBRATION; ",
      "skipping calibration figures"
    )
  } else {
    # Prefer M|D estimator rows for the method under evaluation
    cal_md <- cal
    if ("estimator" %in% names(cal_md)) {
      cal_md <- cal_md[cal_md$estimator == "md", , drop = FALSE]
    }
    if ("effect" %in% names(cal_md)) {
      cal_null <- cal_md[cal_md$effect == "null" | cal_md$effect_name == "null", , drop = FALSE]
    } else {
      cal_null <- cal_md
    }
    if (nrow(cal_null)) {
      plot_df <- cal_null |>
        dplyr::group_by(outcome, kernel) |>
        dplyr::summarise(
          coverage = mean(coverage, na.rm = TRUE),
          type1 = mean(type1, na.rm = TRUE),
          n_scenarios = dplyr::n(),
          .groups = "drop"
        ) |>
        dplyr::mutate(
          outcome = factor(outcome, levels = c("chd", "hf")),
          kernel = factor(
            kernel,
            levels = c("same_day", "cumulative_0_5", "cumulative_0_21")
          )
        )
      p_cal <- ggplot2::ggplot(plot_df, ggplot2::aes(kernel, coverage, fill = outcome)) +
        ggplot2::geom_col(
          position = ggplot2::position_dodge(width = 0.75),
          width = 0.7
        ) +
        ggplot2::geom_hline(yintercept = 0.9, linetype = "dashed", colour = "grey40") +
        ggplot2::scale_fill_manual(
          values = c(chd = "#bd5a32", hf = "#276b79"),
          labels = c(chd = "CHD-like", hf = "HF-like")
        ) +
        ggplot2::labs(
          title = "Synthetic calibration coverage by outcome and kernel",
          subtitle = CALIBRATION_WATERMARK,
          x = NULL,
          y = "Coverage",
          fill = NULL
        ) +
        theme_pub() +
        ggplot2::annotate(
          "text",
          x = Inf, y = Inf,
          label = CALIBRATION_WATERMARK,
          hjust = 1.02, vjust = 1.4,
          size = 2.6, colour = "#8a3b2b"
        )
      save_plot_multi(
        p_cal, mf_dir, "figure_calibration_coverage_by_outcome_kernel", 8.5, 5.2
      )

      if ("type1" %in% names(plot_df)) {
        p_t1 <- ggplot2::ggplot(plot_df, ggplot2::aes(kernel, type1, fill = outcome)) +
          ggplot2::geom_col(
            position = ggplot2::position_dodge(width = 0.75),
            width = 0.7
          ) +
          ggplot2::geom_hline(yintercept = 0.05, linetype = "dotted", colour = "grey50") +
          ggplot2::geom_hline(yintercept = 0.03, linetype = "dashed", colour = "grey60") +
          ggplot2::geom_hline(yintercept = 0.08, linetype = "dashed", colour = "grey60") +
          ggplot2::scale_fill_manual(
            values = c(chd = "#bd5a32", hf = "#276b79"),
            labels = c(chd = "CHD-like", hf = "HF-like")
          ) +
          ggplot2::labs(
            title = "Synthetic null type-I error by outcome and kernel",
            subtitle = CALIBRATION_WATERMARK,
            x = NULL,
            y = "Type-I error",
            fill = NULL
          ) +
          theme_pub() +
          ggplot2::annotate(
            "text",
            x = Inf, y = Inf,
            label = CALIBRATION_WATERMARK,
            hjust = 1.02, vjust = 1.4,
            size = 2.6, colour = "#8a3b2b"
          )
        save_plot_multi(
          p_t1, mf_dir, "figure_calibration_type1_by_outcome_kernel", 8.5, 5.2
        )
      }
    }
  }
} else {
  writeLines(
    c(
      "# Calibration figures deferred",
      "",
      paste0("**Provenance:** `", RELEASE_SYNTHETIC_CALIBRATION, "`"),
      paste0("**Result class:** `METHODS_FEASIBILITY`"),
      "",
      "Canonical `md_calibration_summary.csv` was absent at release augmentation.",
      "No coverage or type-I figure was drawn.",
      "",
      CALIBRATION_WATERMARK
    ),
    file.path(mf_dir, "calibration_figures_availability.md")
  )
}

if (file.exists(mf_gates)) {
  gates <- utils::read.csv(mf_gates, stringsAsFactors = FALSE)
  if ("data_status" %in% names(gates) &&
      all(gates$data_status == RELEASE_SYNTHETIC_CALIBRATION)) {
    gates$passed_f <- factor(
      ifelse(as.logical(gates$passed), "Pass", "Fail"),
      levels = c("Pass", "Fail")
    )
    decision <- if ("admission_decision" %in% names(gates)) {
      unique(as.character(gates$admission_decision))[[1]]
    } else {
      "UNKNOWN"
    }
    p_g <- ggplot2::ggplot(
      gates,
      ggplot2::aes(gate_id, 1, fill = passed_f)
    ) +
      ggplot2::geom_tile(colour = "white", linewidth = 0.6) +
      ggplot2::scale_fill_manual(
        values = c(Pass = "#5b8c5a", Fail = "#a0483a")
      ) +
      ggplot2::labs(
        title = "Synthetic calibration admission gates",
        subtitle = paste0(CALIBRATION_WATERMARK, " Decision: ", decision),
        x = NULL,
        y = NULL,
        fill = NULL
      ) +
      theme_pub() +
      ggplot2::theme(
        axis.text.y = ggplot2::element_blank(),
        axis.ticks.y = ggplot2::element_blank(),
        axis.text.x = ggplot2::element_text(angle = 35, hjust = 1)
      )
    save_plot_multi(p_g, mf_dir, "figure_calibration_gate_passfail", 9.5, 3.8)
  }
} else {
  writeLines(
    c(
      "# Calibration gate figure deferred",
      "",
      paste0("**Provenance:** `", RELEASE_SYNTHETIC_CALIBRATION, "`"),
      paste0("**Result class:** `METHODS_FEASIBILITY`"),
      "",
      "Canonical `md_calibration_gate_summary.csv` was absent at release augmentation.",
      "",
      CALIBRATION_WATERMARK
    ),
    file.path(mf_dir, "calibration_gate_figure_availability.md")
  )
}

# Methods-feasibility README
writeLines(
  c(
    "# Methods-feasibility supplement",
    "",
    paste0("**Provenance quarantine:** `", RELEASE_SYNTHETIC_CALIBRATION, "` artifacts"),
    "may appear only in this folder. They are method-validation materials,",
    "not CHD/HF health findings.",
    "",
    "- Weather source-lock, validation, and spillover morphology: `REAL_PUBLIC_HKO`.",
    "- Calibration summary, strict F1.2 gates/decision, and F1.0 failure note: `SYNTHETIC_CALIBRATION`.",
    "- Ensemble / prediction / M|D blockers may be mirrored here as availability facts.",
    "",
    "Do not promote calibration coefficients or gate outcomes into main Tables 1–4",
    "or into manuscript-real claim surfaces.",
    "",
    CALIBRATION_WATERMARK,
    "",
    "See `methods_feasibility_manifest.csv` for source paths and copy status."
  ),
  file.path(mf_dir, "README.md")
)

# =============================================================================
# Release index / README addendum (preserve original README body)
# =============================================================================
readme_path <- file.path(release_dir, "README.md")
addendum <- c(
  "",
  "## Final augmentation (script 38)",
  "",
  "- Tables 1–3 and Figures 1–4 are unchanged from the script-33 analysis of record.",
  "- Table 4 (`tables/table4_uncertainty_ladder.csv`) shows Model/HC1/NW3/NW6 for the 12 core contrasts.",
  "- Figure 5 (`figures/figure5_se_method_ladder.*`) is the SE-method ladder forest.",
  "- `tables/analysis_availability.csv` records ensemble, prediction, and M|D blockers as non-completed analyses.",
  "- `tables/claim_ledger_v2.csv` extends the existing claim ledger with claim tier,",
  "  post-outcome, multiplicity, and SE context. No new real claims were added without real outputs.",
  "- `supplement/methods_feasibility/` holds public weather audits and",
  "  `SYNTHETIC_CALIBRATION` method-validation materials only.",
  "- Calibration outputs are never health findings for CHD/HF.",
  "- Health provenance remains `HA_APPROVED_AGGREGATE` (never renamed to REAL).",
  "",
  "See `RELEASE_INDEX.md` for the file map."
)
readme_txt <- if (file.exists(readme_path)) {
  readLines(readme_path, warn = FALSE)
} else {
  character(0)
}
# Replace prior addendum if re-run
cut <- grep("^## Final augmentation \\(script 38\\)", readme_txt)
if (length(cut)) {
  readme_txt <- readme_txt[seq_len(cut[[1]] - 1L)]
  while (length(readme_txt) && !nzchar(readme_txt[[length(readme_txt)]])) {
    readme_txt <- readme_txt[-length(readme_txt)]
  }
}
writeLines(c(readme_txt, addendum), readme_path)

index_lines <- c(
  "# CHD/HF release index (augmented)",
  "",
  "Disclosure-minimised release package. Analysis of record remains the amended",
  "monthly negative-binomial panel with Newey-West lag-6 intervals.",
  "",
  "## Preserved (script 33)",
  "",
  "| Artifact | Role |",
  "|---|---|",
  "| `tables/table1_outcome_summary.csv` | Outcome summary |",
  "| `tables/table2_core_models.csv` | Twelve core contrasts |",
  "| `tables/table3_robustness_summary.csv` | Robustness ranges |",
  "| `tables/claim_ledger.csv` | Claim ledger v1 |",
  "| `figures/figure1_indexed_outcome_series.*` | Indexed series |",
  "| `figures/figure2_seasonal_pattern.*` | Seasonality |",
  "| `figures/figure3_core_forest.*` | Core forest |",
  "| `figures/figure4_trend_depletion_sensitivity.*` | Trend/depletion |",
  "",
  "## Added (script 38)",
  "",
  "| Artifact | Role | Provenance |",
  "|---|---|---|",
  "| `tables/table4_uncertainty_ladder.csv` | SE ladder (12×4) | HA_APPROVED_AGGREGATE |",
  "| `tables/analysis_availability.csv` | Ensemble/prediction/M|D status | blockers or HA |",
  "| `tables/claim_ledger_v2.csv` | Tiered claim ledger | HA_APPROVED_AGGREGATE |",
  "| `figures/figure5_se_method_ladder.*` | SE ladder forest | HA_APPROVED_AGGREGATE |",
  "| `supplement/methods_feasibility/` | Weather + calibration quarantine | mixed; see manifest |",
  "",
  "## Methods-feasibility quarantine",
  "",
  paste0("`", METHODS_FEASIBILITY_RELDIR, "/` is the only release location"),
  "allowed to carry `SYNTHETIC_CALIBRATION`. Those materials validate methods;",
  "they are not CHD/HF effect evidence.",
  "",
  CALIBRATION_WATERMARK
)
writeLines(index_lines, file.path(release_dir, "RELEASE_INDEX.md"))

message(
  "Release augmentation complete (no unlink). ",
  "Table4 rows=", nrow(table4),
  "; availability rows=", nrow(availability),
  "; methods-feasibility artifacts=", nrow(mf_manifest)
)
