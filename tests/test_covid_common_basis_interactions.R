# SYNTHETIC ONLY: does not touch HA inputs and creates no manuscript results.
source(file.path("scripts","83_covid_common_basis_interactions.R"))
expect_error <- function(expr) {
  happened <- FALSE
  tryCatch(force(expr),error=function(e) happened <<- TRUE)
  stopifnot(happened)
}
# Independent analytic covariance identity; nonzero covariance must change later SE.
j <- joint_slopes(c(.2,-.1),matrix(c(.04,-.015,-.015,.09),nrow=2))
stopifnot(isTRUE(all.equal(j$estimate,c(.2,.1,-.1))))
stopifnot(isTRUE(all.equal(unname(diag(j$covariance)),c(.04,.10,.09))))
stopifnot(isTRUE(all.equal(unname(j$covariance[1,2]),.025)))
expect_error(joint_slopes(c(.2,-.1),diag(c(-1,.1))))
expect_error(parse_cli(c("--chd","a.csv","--hf","b.csv","--output","out")))
expected <- seq(as.Date("2013-01-01"),as.Date("2023-12-01"),by="month")
next_month <- c(expected[-1],as.Date("2024-01-01"))
set.seed(20261002)
t <- seq_along(expected)
m <- as.integer(format(expected,"%m"))
x <- 20 + 8*sin(2*pi*m/12) + rnorm(132,0,2)
# Known +0.04 log slope per C and later-minus-pre difference +0.07.
# The full-series model includes calendar controls and the period intercept.
post <- as.integer(expected >= as.Date("2020-01-01"))
mu <- exp(4 + .04*x + .07*x*post - .2*post)
dat <- data.frame(month_id=format(expected,"%Y-%m"),year=as.integer(format(expected,"%Y")),
  month=m,time_index=t,n_events=rnbinom(132,mu=mu,size=80),data_status="SYNTHETIC_CALIBRATION",
  days_in_month=as.integer(next_month-expected),mean_temp=x,mean_tmax=x+3,mean_tmin=x-3,
  hot_nights=pmin(28,pmax(0,round(x-10))),cold_days=pmax(0,round(12-x)),
  very_hot_days=pmax(0,round(x-25)))
panel <- validate_monthly_panel(dat,synthetic=TRUE)
expect_error(validate_monthly_panel(dat,synthetic=FALSE))
bad <- dat; bad$month_id[2] <- bad$month_id[1]; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$data_status[2] <- "HA_APPROVED_AGGREGATE"; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$n_events[1] <- -1; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$hot_nights[1] <- 40; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$days_in_month[1] <- 30; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$time_index[2] <- 4; expect_error(validate_monthly_panel(bad,TRUE))
bad <- dat; bad$mean_temp[1] <- NA_real_; expect_error(validate_monthly_panel(bad,TRUE))
# Numeric fit tests require installed packages; absence is a failure, never a green skip here.
stopifnot(requireNamespace("MASS",quietly=TRUE),requireNamespace("sandwich",quietly=TRUE))
fit <- fit_scenario(panel,"chd","mean_temp","2020-01",4L)
stopifnot(nrow(fit$contrasts)==12L,nrow(fit$joint)==4L,fit$status$fit_status=="FITTED")
row <- subset(fit$contrasts,se_method=="model" & contrast=="direct_later_minus_pre")
stopifnot(abs(row$log_ratio-.07)<.025)
# All twelve slots must survive multiplicity even when some are failed/NA.
members <- expand.grid(outcome=c("chd","hf"),exposure=names(EXPOSURE_SCALES),stringsAsFactors=FALSE)
family <- do.call(rbind,lapply(1:12,function(i) { z <- fit$contrasts; z$outcome <- members$outcome[i]; z$exposure <- members$exposure[i]; z }))
missing_slot <- family$outcome==members$outcome[12] & family$exposure==members$exposure[12]
family$p_value[missing_slot] <- NA_real_
adjusted <- complete_family_bh(family)
stopifnot(nrow(adjusted)==144L)
expect_error(complete_family_bh(family[!missing_slot,]))
duplicated_family <- family; duplicated_family[missing_slot,c("outcome","exposure")] <- family[1,c("outcome","exposure")]
expect_error(complete_family_bh(duplicated_family))
# An absent support exposure must retain failed slots rather than switch families.
zero <- panel; zero$cold_days <- 0
failed <- fit_scenario(zero,"chd","cold_days","2020-01",4L)
stopifnot(nrow(failed$contrasts)==12L,all(is.na(failed$contrasts$log_ratio)))
cat("SYNTHETIC interface and covariance tests passed; coverage calibration not certified.\n")
