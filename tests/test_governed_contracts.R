#!/usr/bin/env Rscript
# Synthetic inputs only. Run at the repository root. No governed runner is sourced.
source(file.path("scripts", "cvd_rerun_contracts.R"))
for (pkg in c("MASS", "sandwich", "tscount")) {
  if (!requireNamespace(pkg, quietly = TRUE)) stop("Missing test dependency: ", pkg)
}
expect_error <- function(expr) {
  stopifnot(inherits(try(force(expr), silent = TRUE), "try-error"))
}
equal <- function(a, b) isTRUE(all.equal(a, b, tolerance = 1e-10))
for (script in c("08c_qc_cvd_aggregates", "23_pathway_diagnostics", "27_cvd_descriptives_real",
                 "31_cvd_core_robustness", "32_cvd_trend_depletion_lag")) {
  parse(file = file.path("scripts", paste0(script, ".R")))
}

months <- format(seq(as.Date("2013-01-01"), by = "month", length.out = 132L), "%Y-%m")
counts <- seq_along(months) - 1L
assert_cvd_event_calendar(rev(months), rev(counts), months)
expect_error(assert_cvd_event_calendar(months[-1], counts[-1], months))
expect_error(assert_cvd_event_calendar(replace(months, 1, months[2]), counts, months))
expect_error(assert_cvd_event_calendar(replace(months, 1, "2024-01"), counts, months))
for (bad in c(NA, Inf, -1, 1.5)) {
  expect_error(assert_cvd_event_calendar(months, replace(counts, 3, bad), months))
}
expect_error(assert_cvd_outcome(data.frame(analysis_outcome = c("chd", "hf")), "hf"))

exposures <- c(P01A = "mean_temp", P02A = "mean_tmax", P02B = "mean_tmin",
               P04A = "hot_nights", P04B = "cold_days", P04C = "very_hot_days")
family <- expand.grid(outcome = c("chd", "hf"), pathway_id = names(exposures),
                      stringsAsFactors = FALSE)
family$exposure <- unname(exposures[family$pathway_id])
family$p_value <- c(.001, .1, .9, .023, .051, .6, .42, .2, .72, .999, 0, .11)
shuffled <- family[c(11:1, 12), ]
stopifnot(equal(cvd_core_bh(shuffled), stats::p.adjust(shuffled$p_value, "BH", n = 12L)))
expect_error(cvd_core_bh(family[-1, ]))
expect_error(cvd_core_bh(rbind(family[-1, ], family[2, ])))
wrong <- family
wrong$exposure[1] <- "cold_days"
expect_error(cvd_core_bh(wrong))
wrong <- family
wrong$p_value[1] <- NA_real_
expect_error(cvd_core_bh(wrong))

# Anchor diagnostic rows to the original model frame, including an early omission.
set.seed(9012)
d <- data.frame(time_index = seq_along(months), x = rnorm(length(months)), row.names = months)
d$y <- 2 + .8 * d$x + rnorm(nrow(d), sd = .1)
d$x[2] <- NA_real_
d$y[42] <- 200
fit <- stats::lm(y ~ x, data = d, na.action = stats::na.omit)
selected <- cvd_max_cook_row(fit, d)
stopifnot(selected$index == 42L, length(cvd_fitted_rows(fit, d)) == 131L,
          !2L %in% cvd_fitted_rows(fit, d),
          rownames(d)[selected$index] == names(which.max(stats::cooks.distance(fit))))
flip <- d[rev(seq_len(nrow(d))), ]
stopifnot(rownames(flip)[cvd_max_cook_row(fit, flip)$index] == months[42])
expect_error(cvd_fitted_rows(fit, d[-42, ]))

# Independent padded-score lag summation. With a deletion, the zero vector
# only marks the missing calendar position. Bread and n-k use the fitted rows.
padded_reference <- function(m, times, lag = 6L) {
  scores <- sandwich::estfun(m)
  grid <- matrix(0, nrow = diff(range(times)) + 1L, ncol = ncol(scores))
  grid[times - min(times) + 1L, ] <- scores
  total <- crossprod(grid)
  for (h in seq_len(lag)) {
    left <- seq_len(nrow(grid) - h)
    pair <- crossprod(grid[left, , drop = FALSE], grid[left + h, , drop = FALSE])
    total <- total + (1 - h / (lag + 1L)) * (pair + t(pair))
  }
  sandwich::sandwich(m, meat. = total / (nrow(scores) - ncol(scores)))
}
d$x[2] <- .1
d$n_events <- rnbinom(nrow(d), size = 5, mu = 100 * exp(.15 * d$x))
d$offset_log_days <- log(30)
full <- fit_nb_nw(d, "x", "time_index")
drop <- d[-45, ]
reduced <- fit_nb_nw(drop, "x", "time_index")
stopifnot(full$row$n_fitted == 132L, reduced$row$n_fitted == 131L,
          equal(reduced$row$std_error_nw6, unname(sqrt(diag(padded_reference(reduced$model, drop$time_index)))["x"])),
          equal(padded_reference(full$model, d$time_index),
                sandwich::NeweyWest(full$model, lag = 6L, prewhite = FALSE, adjust = TRUE)))
bad_fit <- full$model
bad_fit$th.warn <- "iteration limit reached"
stopifnot(!cvd_converged(NULL), !cvd_converged(bad_fit))
d$x[2] <- NA_real_
expect_error(fit_nb_nw(d, "x", "time_index"))
expect_error(cvd_monthly_nw(reduced$model, rev(drop$time_index)))

res <- c(1.5, -1, .2, .4)
stopifnot(equal(cvd_monthly_acf1(res, 1:4), as.numeric(stats::acf(res, plot = FALSE)$acf[2])))
centered <- res - mean(res)
stopifnot(equal(cvd_monthly_acf1(res, c(1, 2, 4, 5)),
                (centered[1]*centered[2] + centered[3]*centered[4]) / sum(centered^2)))

# Exercise the registered tscount method with a non-Poisson information pair.
coef_names <- list(c("a", "b"), c("a", "b"))
H <- matrix(c(4, 1, 1, 3), 2, dimnames = coef_names)
B <- matrix(c(12, 2, 2, 8), 2, dimnames = coef_names)
mock <- structure(list(info.matrix = H, info.matrix_corrected = B), class = "tsglm")
stopifnot(equal(cvd_ingarch_vcov(mock), solve(H) %*% B %*% solve(H)),
          !equal(cvd_ingarch_vcov(mock), solve(B)))
missing <- mock
missing$info.matrix_corrected <- NULL
singular <- mock
singular$info.matrix[,] <- 1
stopifnot(is.null(cvd_ingarch_vcov(missing)), is.null(cvd_ingarch_vcov(singular)))
cat("PASS: synthetic calendar, count, multiplicity, influence and covariance regressions.\n")
