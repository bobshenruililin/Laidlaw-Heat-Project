# release_check_helpers.R
# Shared helpers for final disclosure-minimised release build (38) and checks (34).
# Sourced by scripts and by tests/test_final_release_checks.R.
# Do not run directly. Never writes governed health inputs.

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(x, y) {
    if (is.null(x) || length(x) == 0 || (length(x) == 1 && is.na(x))) y else x
  }
}

RELEASE_REAL_PROVENANCE <- "HA_APPROVED_AGGREGATE"
RELEASE_SYNTHETIC_CALIBRATION <- "SYNTHETIC_CALIBRATION"

CORE_PATHWAY_IDS <- c("P01A", "P02A", "P02B", "P04A", "P04B", "P04C")
CORE_OUTCOMES <- c("chd", "hf")

SE_LADDER_METHODS <- c("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")
SE_LADDER_DISPLAY <- c(
  model = "Model",
  HC1 = "HC1",
  NeweyWest_lag3 = "NW3",
  NeweyWest_lag6 = "NW6"
)

CORE_EXPOSURE_LABELS <- c(
  P01A = "Mean temperature, per 1 C",
  P02A = "Mean maximum temperature, per 1 C",
  P02B = "Mean minimum temperature, per 1 C",
  P04A = "Hot nights, per 5 days",
  P04B = "Cold days, per 5 days",
  P04C = "Very hot days, per 5 days"
)

OUTCOME_LABELS_RELEASE <- c(
  chd = "Coronary heart disease",
  hf = "Heart failure"
)

CALIBRATION_WATERMARK <-
  "SYNTHETIC CALIBRATION — METHOD VALIDATION, NOT HEALTH FINDINGS."

METHODS_FEASIBILITY_RELDIR <- "supplement/methods_feasibility"

# ---------------------------------------------------------------------------
# BH / ledger identity
# ---------------------------------------------------------------------------

recompute_bh_q_values <- function(p_values) {
  as.numeric(stats::p.adjust(as.numeric(p_values), method = "BH"))
}

claim_text_from_row <- function(outcome_label, contrast, rr, rr_low, rr_high,
                                digits = 3L) {
  paste0(
    outcome_label, ": ", contrast, "; count ratio ",
    sprintf(paste0("%.", digits, "f"), rr), " (95% CI ",
    sprintf(paste0("%.", digits, "f"), rr_low), "–",
    sprintf(paste0("%.", digits, "f"), rr_high), ")."
  )
}

table2_claim_ledger_identity <- function(table2, ledger, tol = 1e-10) {
  required_t2 <- c(
    "outcome", "pathway_id", "rr", "rr_low", "rr_high",
    "p_value", "q_value_core_bh", "se_method", "data_status"
  )
  required_cl <- c(
    "claim_id", "outcome", "pathway_id", "rr", "rr_low", "rr_high",
    "p_value", "q_value_core_bh", "se_method", "provenance"
  )
  missing_t2 <- setdiff(required_t2, names(table2))
  missing_cl <- setdiff(required_cl, names(ledger))
  if (length(missing_t2) || length(missing_cl)) {
    return(list(
      ok = FALSE,
      detail = paste0(
        "missing columns; table2=", paste(missing_t2, collapse = ","),
        "; ledger=", paste(missing_cl, collapse = ",")
      )
    ))
  }
  if (!identical(nrow(table2), 12L) || !identical(nrow(ledger), 12L)) {
    return(list(
      ok = FALSE,
      detail = paste0(
        "expected 12 rows each; table2=", nrow(table2),
        " ledger=", nrow(ledger)
      )
    ))
  }

  key_cols <- c("outcome", "pathway_id")
  t2 <- table2[order(table2$outcome, table2$pathway_id), , drop = FALSE]
  cl <- ledger[order(ledger$outcome, ledger$pathway_id), , drop = FALSE]
  if (!identical(as.character(t2$outcome), as.character(cl$outcome)) ||
      !identical(as.character(t2$pathway_id), as.character(cl$pathway_id))) {
    return(list(ok = FALSE, detail = "outcome/pathway_id key mismatch"))
  }

  num_cols <- c("rr", "rr_low", "rr_high", "p_value", "q_value_core_bh")
  for (col in num_cols) {
    if (!isTRUE(all.equal(
      as.numeric(t2[[col]]), as.numeric(cl[[col]]),
      tolerance = tol, check.attributes = FALSE
    ))) {
      return(list(ok = FALSE, detail = paste0("numerical mismatch on ", col)))
    }
  }

  if (!all(t2$se_method == "NeweyWest_lag6") ||
      !all(cl$se_method == "NeweyWest_lag6")) {
    return(list(ok = FALSE, detail = "table2/ledger se_method must be NeweyWest_lag6"))
  }
  if (!all(t2$data_status == RELEASE_REAL_PROVENANCE) ||
      !all(cl$provenance == RELEASE_REAL_PROVENANCE)) {
    return(list(ok = FALSE, detail = "provenance must be HA_APPROVED_AGGREGATE"))
  }

  list(ok = TRUE, detail = "12 rows; rr/CI/p/q/se/provenance identical")
}

claim_text_rounding_ok <- function(ledger, digits = 3L) {
  if (!all(c("claim_text", "outcome", "contrast", "rr", "rr_low", "rr_high") %in%
           names(ledger))) {
    return(list(ok = FALSE, detail = "ledger missing claim_text fields"))
  }
  outcome_labels <- if ("outcome_label" %in% names(ledger)) {
    ledger$outcome_label
  } else {
    unname(OUTCOME_LABELS_RELEASE[as.character(ledger$outcome)])
  }
  expected <- mapply(
    claim_text_from_row,
    outcome_labels,
    ledger$contrast,
    ledger$rr,
    ledger$rr_low,
    ledger$rr_high,
    MoreArgs = list(digits = digits),
    USE.NAMES = FALSE
  )
  bad <- which(as.character(ledger$claim_text) != expected)
  if (length(bad)) {
    return(list(
      ok = FALSE,
      detail = paste0(
        "claim_text rounding mismatch at rows ",
        paste(bad, collapse = ",")
      )
    ))
  }
  list(ok = TRUE, detail = paste0("claim_text matches ", digits, "-dp rounding"))
}

bh_q_identity <- function(p_values, q_values, tol = 1e-10) {
  recomputed <- recompute_bh_q_values(p_values)
  ok <- isTRUE(all.equal(
    as.numeric(q_values), recomputed,
    tolerance = tol, check.attributes = FALSE
  ))
  list(
    ok = ok,
    recomputed = recomputed,
    detail = if (ok) "BH q values match p.adjust(..., method='BH')" else {
      "BH q values do not match recomputation"
    }
  )
}

# ---------------------------------------------------------------------------
# Uncertainty ladder (Table 4)
# ---------------------------------------------------------------------------

build_uncertainty_ladder <- function(core_robust,
                                     family = "negative_binomial",
                                     offset_policy = "days_only") {
  need <- c(
    "outcome", "pathway_id", "exposure", "family", "offset_policy",
    "se_method", "rr", "rr_low", "rr_high", "p_value", "data_status",
    "n_months"
  )
  missing <- setdiff(need, names(core_robust))
  if (length(missing)) {
    stop("core robust estimates missing columns: ", paste(missing, collapse = ", "))
  }

  ladder <- core_robust[
    core_robust$family == family &
      core_robust$offset_policy == offset_policy &
      core_robust$se_method %in% SE_LADDER_METHODS,
    ,
    drop = FALSE
  ]
  ladder <- ladder[
    ladder$outcome %in% CORE_OUTCOMES &
      ladder$pathway_id %in% CORE_PATHWAY_IDS,
    ,
    drop = FALSE
  ]

  ladder$se_method_label <- unname(SE_LADDER_DISPLAY[as.character(ladder$se_method)])
  ladder$outcome_label <- unname(OUTCOME_LABELS_RELEASE[as.character(ladder$outcome)])
  ladder$exposure_label <- ifelse(
    as.character(ladder$pathway_id) %in% names(CORE_EXPOSURE_LABELS),
    unname(CORE_EXPOSURE_LABELS[as.character(ladder$pathway_id)]),
    as.character(ladder$exposure)
  )
  ladder$contrast <- ladder$exposure_label
  ladder$count_ratio_95CI <- sprintf(
    "%.3f (%.3f-%.3f)", ladder$rr, ladder$rr_low, ladder$rr_high
  )
  ladder$result_class <- "ANALYSIS_OF_RECORD_UNCERTAINTY_LADDER"
  ladder$manuscript_role <- "uncertainty display; SE method not selected by CI exclusion of 1"

  # Stable order: outcome, pathway, SE ladder sequence
  ladder$pathway_id <- factor(ladder$pathway_id, levels = CORE_PATHWAY_IDS)
  ladder$outcome <- factor(ladder$outcome, levels = CORE_OUTCOMES)
  ladder$se_method <- factor(ladder$se_method, levels = SE_LADDER_METHODS)
  ladder <- ladder[order(ladder$outcome, ladder$pathway_id, ladder$se_method), , drop = FALSE]
  ladder$outcome <- as.character(ladder$outcome)
  ladder$pathway_id <- as.character(ladder$pathway_id)
  ladder$se_method <- as.character(ladder$se_method)
  rownames(ladder) <- NULL
  ladder
}

validate_uncertainty_ladder <- function(ladder, expected_n = 48L) {
  if (is.null(ladder) || !nrow(ladder)) {
    return(list(ok = FALSE, detail = "ladder empty"))
  }
  if (!identical(as.integer(nrow(ladder)), as.integer(expected_n))) {
    return(list(
      ok = FALSE,
      detail = paste0("expected ", expected_n, " rows (12x4); found ", nrow(ladder))
    ))
  }
  keys <- paste(ladder$outcome, ladder$pathway_id, ladder$se_method, sep = "::")
  expected_keys <- as.vector(outer(
    as.vector(outer(CORE_OUTCOMES, CORE_PATHWAY_IDS, paste, sep = "::")),
    SE_LADDER_METHODS,
    paste,
    sep = "::"
  ))
  # outer order differs; compare as sets
  if (!setequal(keys, expected_keys)) {
    missing <- setdiff(expected_keys, keys)
    extra <- setdiff(keys, expected_keys)
    return(list(
      ok = FALSE,
      detail = paste0(
        "key set mismatch; missing=", paste(utils::head(missing, 6), collapse = ";"),
        " extra=", paste(utils::head(extra, 6), collapse = ";")
      )
    ))
  }
  if (anyDuplicated(keys)) {
    return(list(ok = FALSE, detail = "duplicate outcome/pathway/se_method keys"))
  }
  if (!all(ladder$data_status == RELEASE_REAL_PROVENANCE)) {
    return(list(
      ok = FALSE,
      detail = paste0(
        "non-HA provenance: ",
        paste(unique(ladder$data_status), collapse = ",")
      )
    ))
  }
  if (any(grepl("SYNTHETIC", ladder$data_status, ignore.case = TRUE))) {
    return(list(ok = FALSE, detail = "SYNTHETIC labels forbidden on main ladder"))
  }
  list(ok = TRUE, detail = "48 HA_APPROVED_AGGREGATE ladder rows (12x4)")
}

# ---------------------------------------------------------------------------
# SYNTHETIC_CALIBRATION path policy
# ---------------------------------------------------------------------------

normalise_release_relpath <- function(path, release_dir = NULL) {
  p <- gsub("\\\\", "/", as.character(path)[[1]])
  if (!is.null(release_dir)) {
    root <- gsub("\\\\", "/", normalizePath(release_dir, winslash = "/", mustWork = FALSE))
    full <- gsub("\\\\", "/", normalizePath(p, winslash = "/", mustWork = FALSE))
    if (startsWith(full, paste0(root, "/"))) {
      p <- substring(full, nchar(root) + 2L)
    }
  }
  # strip leading ./
  sub("^\\./", "", p)
}

is_methods_feasibility_path <- function(rel_path) {
  rel <- normalise_release_relpath(rel_path)
  identical(rel, METHODS_FEASIBILITY_RELDIR) ||
    startsWith(rel, paste0(METHODS_FEASIBILITY_RELDIR, "/"))
}

is_release_doc_path <- function(rel_path) {
  rel <- normalise_release_relpath(rel_path)
  rel %in% c(
    "README.md",
    "RELEASE_INDEX.md",
    "README_ADDENDUM.md",
    "validation_checks.csv",
    "release_manifest.csv"
  )
}

is_main_claim_surface_path <- function(rel_path) {
  rel <- normalise_release_relpath(rel_path)
  if (is_methods_feasibility_path(rel)) return(FALSE)
  # Machine-readable claim tables and main figures are the hard surfaces.
  startsWith(rel, "tables/") || startsWith(rel, "figures/")
}

# Allowed only under methods_feasibility, and only when the artifact carries
# an explicit data_status / result_class declaring SYNTHETIC_CALIBRATION.
synthetic_calibration_path_policy <- function(rel_path,
                                              data_status = NULL,
                                              result_class = NULL,
                                              text_has_synthetic = FALSE) {
  rel <- normalise_release_relpath(rel_path)
  in_mf <- is_methods_feasibility_path(rel)
  statuses <- unique(as.character(data_status %||% character(0)))
  statuses <- statuses[nzchar(statuses) & !is.na(statuses)]
  classes <- unique(as.character(result_class %||% character(0)))
  classes <- classes[nzchar(classes) & !is.na(classes)]

  has_synth_status <- any(statuses == RELEASE_SYNTHETIC_CALIBRATION) ||
    any(grepl("SYNTHETIC_CALIBRATION", statuses, fixed = TRUE))
  has_synth_class <- any(grepl("SYNTHETIC|METHODS_FEASIBILITY|CALIBRATION",
                               classes, ignore.case = TRUE))

  if (!isTRUE(text_has_synthetic) && !has_synth_status) {
    return(list(ok = TRUE, allowed = TRUE, detail = "no synthetic content"))
  }

  # Release docs may name the quarantine token when pointing readers to
  # methods_feasibility; they are not claim tables.
  if (is_release_doc_path(rel)) {
    return(list(
      ok = TRUE,
      allowed = TRUE,
      detail = "release doc may name SYNTHETIC_CALIBRATION quarantine"
    ))
  }

  if (!in_mf) {
    return(list(
      ok = FALSE,
      allowed = FALSE,
      detail = paste0(
        "SYNTHETIC_CALIBRATION forbidden outside ",
        METHODS_FEASIBILITY_RELDIR, ": ", rel
      )
    ))
  }

  # Inside methods_feasibility: require explicit data_status when tabular,
  # or an explicit result_class / watermark context for notes/figures.
  if (grepl("\\.(csv)$", rel, ignore.case = TRUE)) {
    if (!has_synth_status) {
      return(list(
        ok = FALSE,
        allowed = FALSE,
        detail = paste0(
          "methods_feasibility CSV with synthetic content must set data_status=",
          RELEASE_SYNTHETIC_CALIBRATION, ": ", rel
        )
      ))
    }
  } else if (!has_synth_status && !has_synth_class && !isTRUE(text_has_synthetic)) {
    return(list(
      ok = FALSE,
      allowed = FALSE,
      detail = paste0("methods_feasibility artifact lacks explicit synthetic label: ", rel)
    ))
  }

  list(
    ok = TRUE,
    allowed = TRUE,
    detail = paste0("allowed under ", METHODS_FEASIBILITY_RELDIR)
  )
}

scan_release_synthetic_policy <- function(release_dir) {
  release_dir <- normalizePath(release_dir, winslash = "/", mustWork = TRUE)
  files <- list.files(release_dir, recursive = TRUE, full.names = TRUE)
  files <- files[file.info(files)$isdir %in% FALSE]
  violations <- character(0)
  allowed <- character(0)

  for (path in files) {
    rel <- normalise_release_relpath(path, release_dir)
    ext <- tolower(tools::file_ext(path))
    text_like <- ext %in% c("csv", "md", "txt", "tex", "html", "svg")
    if (!text_like) next

    txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
    has_synth <- grepl("SYNTHETIC", txt, fixed = TRUE)
    if (!has_synth) next

    data_status <- NULL
    result_class <- NULL
    if (identical(ext, "csv")) {
      dat <- tryCatch(
        utils::read.csv(path, stringsAsFactors = FALSE, nrows = 5000),
        error = function(e) NULL
      )
      if (!is.null(dat)) {
        if ("data_status" %in% names(dat)) data_status <- dat$data_status
        if ("result_class" %in% names(dat)) result_class <- dat$result_class
      }
    }

    # Markdown/SVG under methods_feasibility: watermark / provenance prose
    if (!identical(ext, "csv") && is_methods_feasibility_path(rel)) {
      result_class <- c(result_class, "METHODS_FEASIBILITY")
      if (grepl("SYNTHETIC_CALIBRATION", txt, fixed = TRUE) ||
          grepl("SYNTHETIC CALIBRATION", txt, fixed = TRUE)) {
        data_status <- c(data_status, RELEASE_SYNTHETIC_CALIBRATION)
      }
    }

    pol <- synthetic_calibration_path_policy(
      rel,
      data_status = data_status,
      result_class = result_class,
      text_has_synthetic = TRUE
    )
    if (!isTRUE(pol$ok)) {
      violations <- c(violations, paste0(rel, " [", pol$detail, "]"))
    } else {
      allowed <- c(allowed, rel)
    }

    # Extra: main claim surfaces must never carry synthetic labels
    if (is_main_claim_surface_path(rel) && has_synth) {
      violations <- c(
        violations,
        paste0(rel, " [synthetic label on main claim surface]")
      )
    }
  }

  list(
    ok = !length(violations),
    violations = unique(violations),
    allowed = unique(allowed),
    detail = if (!length(violations)) {
      paste0(
        "synthetic path policy OK; allowed=",
        if (length(allowed)) paste(allowed, collapse = ";") else "none"
      )
    } else {
      paste(violations, collapse = " | ")
    }
  )
}

# ---------------------------------------------------------------------------
# Forbidden raw monthly descriptives / governed tracking
# ---------------------------------------------------------------------------

looks_like_raw_monthly_counts <- function(df) {
  if (is.null(df) || !nrow(df)) return(FALSE)
  nm <- tolower(names(df))
  has_month <- any(nm %in% c("month_id", "month_date", "ym", "year_month"))
  count_cols <- c(
    "n_events", "event_count", "monthly_count", "count",
    "chd_count", "hf_count", "n_stroke", "admissions"
  )
  has_count <- any(nm %in% count_cols)
  # Indexed series / means are allowed; raw event columns at month grain are not.
  has_month && has_count
}

scan_release_raw_monthly_counts <- function(release_dir) {
  release_dir <- normalizePath(release_dir, winslash = "/", mustWork = TRUE)
  csvs <- list.files(release_dir, recursive = TRUE, full.names = TRUE, pattern = "\\.csv$")
  hits <- character(0)
  for (path in csvs) {
    rel <- normalise_release_relpath(path, release_dir)
    # Spillover monthly exposure audits are weather counts, not HA outcomes.
    if (is_methods_feasibility_path(rel) &&
        grepl("spillover|weather|morphology|exposure", rel, ignore.case = TRUE)) {
      next
    }
    dat <- tryCatch(
      utils::read.csv(path, stringsAsFactors = FALSE, nrows = 5),
      error = function(e) NULL
    )
    if (is.null(dat)) next
    if (looks_like_raw_monthly_counts(dat)) {
      hits <- c(hits, rel)
    }
  }
  list(
    ok = !length(hits),
    hits = hits,
    detail = if (!length(hits)) "no raw monthly-count descriptives" else {
      paste(hits, collapse = ";")
    }
  )
}

governed_paths_default <- function(root) {
  c(
    file.path(root, "data_raw", "ha_secure_placeholder", "ha_chd_monthly_2013_2023.csv"),
    file.path(root, "data_raw", "ha_secure_placeholder", "ha_hf_monthly_2013_2023.csv"),
    file.path(root, "data_processed", "chd_aggregates_normalized.csv"),
    file.path(root, "data_processed", "hf_aggregates_normalized.csv"),
    file.path(root, "data_processed", "chd_analysis_panel.csv"),
    file.path(root, "data_processed", "hf_analysis_panel.csv")
  )
}

check_governed_not_tracked <- function(paths) {
  repo_root <- tryCatch(
    normalizePath(
      system2("git", c("rev-parse", "--show-toplevel"), stdout = TRUE)[1],
      winslash = "/",
      mustWork = TRUE
    ),
    error = function(e) normalizePath(".", winslash = "/", mustWork = TRUE)
  )
  tracked <- character(0)
  for (path in paths) {
    full <- normalizePath(path, winslash = "/", mustWork = FALSE)
    rel <- if (startsWith(full, paste0(repo_root, "/"))) {
      substring(full, nchar(repo_root) + 2L)
    } else {
      path
    }
    # git ls-files --error-unmatch returns 0 if tracked
    code <- tryCatch(
      as.integer(system2(
        "git",
        c("-C", repo_root, "ls-files", "--error-unmatch", "--", rel),
        stdout = FALSE,
        stderr = FALSE
      )),
      error = function(e) 1L
    )
    if (identical(code, 0L)) tracked <- c(tracked, path)
  }
  list(
    ok = !length(tracked),
    tracked = tracked,
    detail = if (!length(tracked)) {
      "no governed inputs tracked"
    } else {
      paste(tracked, collapse = ";")
    }
  )
}

# ---------------------------------------------------------------------------
# Availability / blocker facts (non-fail when status is explicit blocker)
# ---------------------------------------------------------------------------

blocker_status_tokens <- c(
  "NOT_RUN_MISSING_GOVERNED_PANEL",
  "BLOCKED_CALIBRATION_GATE_ABSENT",
  "BLOCKED_CALIBRATION_GATE_FAIL",
  "FAILED",
  "SKIPPED",
  "ABSENT"
)

normalise_availability_row <- function(script_id, analysis, status, message = "",
                                       result_class = NA_character_,
                                       data_status = NA_character_,
                                       artifact_path = NA_character_,
                                       availability = NA_character_) {
  status <- as.character(status %||% "ABSENT")
  is_blocker <- status %in% blocker_status_tokens ||
    grepl("NOT_RUN|BLOCKED|ABSENT|MISSING", status, ignore.case = TRUE)
  if (is.na(availability) || !nzchar(availability)) {
    availability <- if (is_blocker) "blocked" else if (grepl("^OK|COMPLETE|PASS", status)) {
      "available"
    } else {
      "status_recorded"
    }
  }
  data.frame(
    script_id = as.character(script_id),
    analysis = as.character(analysis),
    status = status,
    availability = availability,
    message = as.character(message %||% ""),
    result_class = as.character(result_class %||% NA_character_),
    data_status = as.character(data_status %||% NA_character_),
    artifact_path = as.character(artifact_path %||% NA_character_),
    check_disposition = if (is_blocker) {
      "non_fail_availability_fact"
    } else {
      "recorded"
    },
    stringsAsFactors = FALSE
  )
}

read_blocker_or_status <- function(path, script_id, analysis) {
  if (!file.exists(path)) {
    return(normalise_availability_row(
      script_id, analysis,
      status = "ABSENT",
      message = paste0("Artifact not present: ", path),
      artifact_path = path
    ))
  }
  dat <- utils::read.csv(path, stringsAsFactors = FALSE)
  if (!nrow(dat)) {
    return(normalise_availability_row(
      script_id, analysis,
      status = "ABSENT",
      message = "Empty status table",
      artifact_path = path
    ))
  }
  status_col <- if ("status" %in% names(dat)) dat$status else "OK"
  msg_col <- if ("message" %in% names(dat)) dat$message else ""
  rc <- if ("result_class" %in% names(dat)) dat$result_class else NA_character_
  ds <- if ("data_status" %in% names(dat)) dat$data_status else NA_character_
  # One row per distinct status line; collapse duplicates
  out <- lapply(seq_len(nrow(dat)), function(i) {
    normalise_availability_row(
      script_id = if ("script_id" %in% names(dat)) dat$script_id[[i]] else script_id,
      analysis = analysis,
      status = status_col[[i]],
      message = msg_col[[i]],
      result_class = rc[[i]],
      data_status = ds[[i]],
      artifact_path = path
    )
  })
  if (requireNamespace("dplyr", quietly = TRUE)) {
    dplyr::bind_rows(out)
  } else {
    do.call(rbind, out)
  }
}
