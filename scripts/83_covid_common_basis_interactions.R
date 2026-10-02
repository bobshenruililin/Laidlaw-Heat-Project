#!/usr/bin/env Rscript
# Prepared analyst runner; no governed input discovery, automatic installation or egress.
# This fits calendar-period associations, not a causal effect of COVID.

EXPOSURE_SCALES <- c(mean_temp=1, mean_tmax=1, mean_tmin=1,
                     hot_nights=5, cold_days=5, very_hot_days=5)
SE_METHODS <- c("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")
REQUIRED_COLUMNS <- c("month_id", "year", "month", "time_index", "n_events",
                      "data_status", "days_in_month", names(EXPOSURE_SCALES))

validate_monthly_panel <- function(dat, synthetic=FALSE) {
  absent <- setdiff(REQUIRED_COLUMNS, names(dat))
  if (length(absent)) stop("Missing required columns: ", paste(absent, collapse=", "))
  if (nrow(dat) != 132L) stop("Expected exactly 132 monthly rows")
  if (anyNA(dat[REQUIRED_COLUMNS])) stop("Missing required values; no imputation allowed")
  if (anyDuplicated(dat$month_id)) stop("Duplicate month identifier")
  dat <- dat[order(dat$month_id), , drop=FALSE]
  expected <- seq(as.Date("2013-01-01"), as.Date("2023-12-01"), by="month")
  if (!identical(as.character(dat$month_id), format(expected, "%Y-%m"))) {
    stop("Calendar must cover 2013-01 through 2023-12 continuously")
  }
  numeric_columns <- setdiff(REQUIRED_COLUMNS, c("month_id", "data_status"))
  if (!all(vapply(dat[numeric_columns], is.numeric, logical(1)))) stop("Non-numeric required column")
  if (any(!is.finite(as.matrix(dat[numeric_columns])))) stop("Non-finite required value")
  if (any(dat$year != as.integer(format(expected, "%Y"))) ||
      any(dat$month != as.integer(format(expected, "%m"))) ||
      any(dat$time_index != seq_len(132L))) stop("Calendar fields/time index disagree")
  next_month <- c(expected[-1], as.Date("2024-01-01"))
  days <- as.integer(next_month - expected)
  if (any(dat$days_in_month != days)) stop("days_in_month disagrees with calendar")
  integer_columns <- c("n_events", "hot_nights", "cold_days", "very_hot_days")
  for (v in integer_columns) {
    if (any(dat[[v]] < 0 | dat[[v]] != floor(dat[[v]]))) stop("Invalid nonnegative integer ", v)
    if (v != "n_events" && any(dat[[v]] > days)) stop("Official-day count exceeds calendar days")
  }
  status <- unique(as.character(dat$data_status))
  if (length(status) != 1L) stop("Mixed provenance is forbidden")
  allowed <- if (synthetic) c("SYNTHETIC", "SYNTHETIC_CALIBRATION") else "HA_APPROVED_AGGREGATE"
  if (!status %in% allowed) stop("Provenance incompatible with selected mode")
  dat$month_f <- factor(dat$month, levels=1:12)
  dat$offset_log_days <- log(days)
  dat
}

joint_slopes <- function(beta, covariance) {
  # beta = (pre slope, direct later-minus-pre difference), per reporting contrast.
  if (length(beta) != 2L || !all(dim(covariance) == c(2L, 2L))) stop("Invalid joint contrast inputs")
  A <- rbind(pre=c(1,0), later=c(1,1), direct=c(0,1))
  transformed <- A %*% covariance %*% t(A)
  if (any(!is.finite(transformed)) || any(diag(transformed) < -1e-10)) stop("Invalid contrast covariance")
  estimate <- as.vector(A %*% beta)
  se <- sqrt(pmax(diag(transformed), 0))
  p <- ifelse(se > 0, 2*stats::pnorm(-abs(estimate/se)), NA_real_)
  list(estimate=estimate, se=se, p=p, covariance=transformed)
}

covariance_for <- function(model, method) {
  if (method == "model") return(stats::vcov(model))
  if (method == "HC1") return(sandwich::vcovHC(model, type="HC1"))
  lag <- if (method == "NeweyWest_lag3") 3L else if (method == "NeweyWest_lag6") 6L else stop("Unknown SE method")
  sandwich::NeweyWest(model, lag=lag, prewhite=FALSE, adjust=TRUE)
}

safe_acf <- function(x) {
  if (length(x) < 13L || !all(is.finite(x)) || stats::sd(x) == 0) return(rep(NA_real_, 12L))
  as.numeric(stats::acf(x, lag.max=12L, plot=FALSE)$acf)[-1]
}

support_for <- function(dat, outcome, exposure, split) {
  later <- dat$month_id >= split
  rows <- list()
  for (m in 1:12) {
    pre <- dat[[exposure]][dat$month == m & !later]
    post <- dat[[exposure]][dat$month == m & later]
    overlap_low <- max(min(pre), min(post))
    overlap_high <- min(max(pre), max(post))
    for (period in c("pre", "later")) {
      x <- if (period == "pre") pre else post
      rows[[length(rows)+1L]] <- data.frame(outcome=outcome, exposure=exposure, split=split,
        month=m, period=period, n_months=length(x), n_positive=sum(x>0), n_zero=sum(x==0),
        exposure_min=min(x), exposure_max=max(x), exposure_sd=stats::sd(x),
        ranges_overlap=overlap_low <= overlap_high, overlap_low=overlap_low,
        overlap_high=overlap_high, stringsAsFactors=FALSE)
    }
  }
  do.call(rbind, rows)
}

fit_scenario <- function(dat, outcome, exposure, split, trend_df) {
  dat$exposure_scaled <- dat[[exposure]] / EXPOSURE_SCALES[[exposure]]
  dat$later <- as.integer(dat$month_id >= split)
  # Exactly one whole-series basis; the pre/later slopes share all its columns.
  basis <- splines::ns(dat$time_index, df=trend_df)
  basis_names <- paste0("trend_", seq_len(ncol(basis)))
  dat[basis_names] <- basis
  fml <- stats::as.formula(paste("n_events ~ exposure_scaled * later + month_f +",
                                 paste(basis_names, collapse=" + "), "+ offset(offset_log_days)"))
  warns <- character()
  error <- NULL
  model <- tryCatch(withCallingHandlers(
    MASS::glm.nb(fml, data=dat, control=stats::glm.control(maxit=100)),
    warning=function(w) { warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning") }),
    error=function(e) { error <<- conditionMessage(e); NULL })
  term <- "exposure_scaled:later"
  if (!is.null(model) && (!isTRUE(model$converged) || anyNA(stats::coef(model)) ||
                         !is.finite(model$theta) || model$theta <= 0)) {
    error <- "Nonconverged, aliased or invalid negative-binomial fit"; model <- NULL
  }
  if (!is.null(model) && !all(c("exposure_scaled", term) %in% names(stats::coef(model)))) {
    error <- "Required slope/interaction is not identified"; model <- NULL
  }
  if (!is.null(model) && length(warns)) {
    # Numeric warnings remain explicit; do not certify the fit as a clean result.
    error <- paste("Fit warning:", paste(unique(warns), collapse="; ")); model <- NULL
  }
  rows <- list(); joint <- list(); dep <- list()
  for (method in SE_METHODS) {
    computation_error <- error
    result <- NULL
    if (!is.null(model)) {
      result <- tryCatch({
        V <- covariance_for(model, method)
        keep <- c("exposure_scaled", term)
        joint_slopes(stats::coef(model)[keep], V[keep, keep, drop=FALSE])
      }, error=function(e) { computation_error <<- conditionMessage(e); NULL })
    }
    for (j in 1:3) {
      rows[[length(rows)+1L]] <- data.frame(outcome=outcome, exposure=exposure,
        scale=EXPOSURE_SCALES[[exposure]], split=split, trend_df=trend_df, se_method=method,
        contrast=c("pre", "later", "direct_later_minus_pre")[j],
        log_ratio=if (is.null(result)) NA_real_ else result$estimate[j],
        std_error=if (is.null(result)) NA_real_ else result$se[j],
        ratio=if (is.null(result)) NA_real_ else exp(result$estimate[j]),
        low=if (is.null(result)) NA_real_ else exp(result$estimate[j]-stats::qnorm(.975)*result$se[j]),
        high=if (is.null(result)) NA_real_ else exp(result$estimate[j]+stats::qnorm(.975)*result$se[j]),
        p_value=if (is.null(result)) NA_real_ else result$p[j], q_interaction=NA_real_,
        status=if (is.null(result)) "FAILED_OR_UNSUPPORTED" else "FIT_REQUIRES_CRITICISM",
        reason=if (is.null(result)) computation_error else "", stringsAsFactors=FALSE)
    }
    joint[[length(joint)+1L]] <- data.frame(outcome=outcome, exposure=exposure, split=split,
      trend_df=trend_df, se_method=method,
      variance_pre=if (is.null(result)) NA_real_ else result$covariance[1,1],
      variance_later=if (is.null(result)) NA_real_ else result$covariance[2,2],
      covariance_pre_later=if (is.null(result)) NA_real_ else result$covariance[1,2],
      variance_direct=if (is.null(result)) NA_real_ else result$covariance[3,3])
  }
  if (!is.null(model)) {
    scores <- sandwich::estfun(model)
    series <- c(list(pearson_residual=stats::residuals(model, type="pearson")),
                lapply(seq_len(ncol(scores)), function(j) scores[,j]))
    names(series)[-1] <- paste0("score:", colnames(scores))
    for (nm in names(series)) {
      dep[[length(dep)+1L]] <- data.frame(outcome=outcome, exposure=exposure, split=split,
        trend_df=trend_df, series=nm, lag=1:12, autocorrelation=safe_acf(series[[nm]]))
    }
  }
  list(contrasts=do.call(rbind,rows), joint=do.call(rbind,joint),
       dependence=if (length(dep)) do.call(rbind,dep) else NULL,
       status=data.frame(outcome=outcome, exposure=exposure, split=split, trend_df=trend_df,
                         fit_status=if (is.null(model)) "FAILED_OR_UNSUPPORTED" else "FITTED",
                         reason=if (is.null(error)) "" else error,
                         n_pre=sum(!dat$later), n_later=sum(dat$later)))
}

complete_family_bh <- function(dat) {
  for (split in unique(dat$split)) for (df in unique(dat$trend_df)) for (se in SE_METHODS) {
    idx <- which(dat$split==split & dat$trend_df==df & dat$se_method==se &
                   dat$contrast=="direct_later_minus_pre")
    expected <- expand.grid(outcome=c("chd", "hf"), exposure=names(EXPOSURE_SCALES), stringsAsFactors=FALSE)
    members <- paste(dat$outcome[idx], dat$exposure[idx], sep=":")
    target <- paste(expected$outcome, expected$exposure, sep=":")
    if (length(idx) != 12L || anyDuplicated(members) || !setequal(members, target)) {
      stop("Incomplete/duplicated interaction family; missing slots cannot be discarded")
    }
    dat$q_interaction[idx] <- stats::p.adjust(dat$p_value[idx], method="BH", n=12L)
  }
  dat
}

parse_cli <- function(args) {
  result <- list(synthetic=FALSE)
  i <- 1L
  while (i <= length(args)) {
    key <- args[i]
    if (key == "--synthetic-calibration") { result$synthetic <- TRUE; i <- i+1L; next }
    allowed <- c("--chd", "--hf", "--output", "--approval-receipt")
    if (!key %in% allowed || i == length(args) || startsWith(args[i+1L], "--")) stop("Invalid CLI argument")
    name <- sub("^--", "", key)
    if (!is.null(result[[name]])) stop("Duplicate CLI argument")
    result[[name]] <- args[i+1L]; i <- i+2L
  }
  for (key in c("chd", "hf", "output")) if (is.null(result[[key]])) stop("Explicit --", key, " required")
  if (!result$synthetic && is.null(result[["approval-receipt"]])) stop("Real mode requires human-approved execution receipt")
  result
}

run_common_basis <- function(args=commandArgs(trailingOnly=TRUE)) {
  opt <- parse_cli(args)
  packages <- c("MASS", "sandwich", "jsonlite", "digest")
  absent <- packages[!vapply(packages, requireNamespace, logical(1), quietly=TRUE)]
  if (length(absent)) stop("Required packages unavailable; no automatic installation: ", paste(absent,collapse=", "))
  sha256 <- function(path) digest::digest(file=path, algo="sha256", serialize=FALSE)
  inputs <- c(chd=normalizePath(opt$chd, mustWork=TRUE), hf=normalizePath(opt$hf, mustWork=TRUE))
  hashes <- vapply(inputs, sha256, character(1))
  receipt_hash <- NULL
  if (!opt$synthetic) {
    receipt_path <- normalizePath(opt[["approval-receipt"]], mustWork=TRUE)
    receipt <- jsonlite::fromJSON(receipt_path)
    if (!identical(receipt$schema_version, "analyst-execution-v1") ||
        !identical(receipt$authorisation_status, "APPROVED_ANALYST_EXECUTION") ||
        !identical(as.character(receipt$input_sha256$chd), unname(hashes["chd"])) ||
        !identical(as.character(receipt$input_sha256$hf), unname(hashes["hf"]))) stop("Execution receipt does not authorise these inputs")
    receipt_hash <- sha256(receipt_path)
  }
  panels <- lapply(inputs, function(path) validate_monthly_panel(utils::read.csv(path, stringsAsFactors=FALSE), opt$synthetic))
  if (!identical(vapply(inputs, sha256, character(1)), hashes)) stop("Input changed during validation")
  compare_cols <- setdiff(REQUIRED_COLUMNS, c("n_events", "data_status"))
  if (!isTRUE(all.equal(panels$chd[compare_cols], panels$hf[compare_cols], check.attributes=FALSE))) stop("CHD/HF calendar or exposures disagree")
  if (!identical(unique(panels$chd$data_status), unique(panels$hf$data_status))) stop("CHD/HF provenance differs")
  output <- path.expand(opt$output)
  if (!startsWith(output, "/")) stop("Use an explicit absolute analyst output directory")
  if (!dir.exists(dirname(output))) stop("Output parent directory must already exist")
  output <- if (dir.exists(output)) normalizePath(output, mustWork=TRUE) else file.path(normalizePath(dirname(output), mustWork=TRUE), basename(output))
  if (file.exists(output) && !dir.exists(output)) stop("Output path is not a directory")
  if (dir.exists(output) && length(list.files(output, all.files=TRUE, no..=TRUE))) stop("Use an empty output directory; no overwrite")
  # Require real outputs outside the project checkout. Execution authority is not egress authority.
  file_arg <- grep("^--file=", commandArgs(), value=TRUE)
  script_path <- if (length(file_arg)) normalizePath(sub("^--file=", "", file_arg[1]), mustWork=TRUE) else NULL
  if (!opt$synthetic && (is.null(script_path) || basename(script_path) != "83_covid_common_basis_interactions.R")) {
    stop("Real execution must invoke the versioned runner with Rscript so source lineage is explicit")
  }
  script_hash <- if (is.null(script_path)) NULL else sha256(script_path)
  if (!opt$synthetic && !is.null(script_path)) {
    repository <- dirname(dirname(script_path))
    target <- normalizePath(output, mustWork=FALSE)
    if (identical(target, repository) || startsWith(target, paste0(repository, "/"))) stop("Real outputs must stay outside repository pending disclosure review")
  }
  fitted <- list(); supports <- list()
  for (outcome in c("chd", "hf")) for (exposure in names(EXPOSURE_SCALES)) for (split in c("2020-01", "2020-02")) {
    supports[[length(supports)+1L]] <- support_for(panels[[outcome]], outcome, exposure, split)
    for (df in c(4L,6L,8L)) fitted[[length(fitted)+1L]] <- fit_scenario(panels[[outcome]], outcome, exposure, split, df)
  }
  bind <- function(key) { rows <- lapply(fitted, `[[`, key); rows <- Filter(Negate(is.null), rows); if (length(rows)) do.call(rbind,rows) else data.frame() }
  contrasts <- complete_family_bh(bind("contrasts"))
  status <- bind("status")
  provenance <- if (opt$synthetic) "SYNTHETIC_CALIBRATION" else "HA_APPROVED_AGGREGATE"
  claim_class <- if (opt$synthetic) "CALIBRATION_ONLY_NOT_A_FINDING" else "EXPLORATORY_ASSOCIATION_NOT_CAUSAL"
  artifacts <- list(contrasts=contrasts, joint_uncertainty=bind("joint"),
                    exposure_support=do.call(rbind,supports), dependence=bind("dependence"), fit_status=status)
  dir.create(output, recursive=TRUE, showWarnings=FALSE)
  for (key in names(artifacts)) {
    n <- nrow(artifacts[[key]])
    artifacts[[key]]$data_status <- rep(provenance, n)
    artifacts[[key]]$claim_class <- rep(claim_class, n)
    artifacts[[key]]$output_status <- rep("AWAITING_DISCLOSURE_REVIEW", n)
    utils::write.csv(artifacts[[key]], file.path(output,paste0(key,".csv")),row.names=FALSE,na="NA")
  }
  manifest <- list(schema_version="common-basis-run-v1", created_utc=format(Sys.time(),tz="UTC",usetz=TRUE),
    data_status=provenance, output_status="AWAITING_DISCLOSURE_REVIEW", input_sha256=as.list(hashes),
    execution_receipt_sha256=receipt_hash, script_sha256=script_hash,
    runtime=R.version.string, packages=as.list(vapply(packages,function(x) as.character(utils::packageVersion(x)),character(1))),
    cuts=c("2020-01","2020-02"), trend_df=c(4L,6L,8L), exposure_scales=as.list(EXPOSURE_SCALES),
    offset="log(days_in_month)", se_methods=SE_METHODS, nw_prewhite=FALSE, nw_adjust=TRUE,
    family_size=12L, complete_family_membership=expand.grid(outcome=c("chd","hf"),exposure=names(EXPOSURE_SCALES)),
    multiplicity="BH12 per split/trend/SE including failed slots; no cross-sensitivity confirmatory claim",
    calendar_basis="one complete-series natural spline per trend scenario; shared pre/later",
    output_files=names(artifacts),
    output_sha256=as.list(vapply(names(artifacts), function(key) sha256(file.path(output,paste0(key,".csv"))), character(1))),
    fit_status=status, calibration_status="NOT_CERTIFIED",
    scientific_status="EXPLORATORY_UNTIL_HUMAN_LOCK_NO_CAUSAL_COVID_EFFECT")
  jsonlite::write_json(manifest,file.path(output,"run_manifest.json"),pretty=TRUE,auto_unbox=TRUE,na="null")
  invisible(artifacts)
}

if (sys.nframe() == 0L) run_common_basis()
