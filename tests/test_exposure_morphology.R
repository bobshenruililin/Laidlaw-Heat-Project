#!/usr/bin/env Rscript

source(file.path("scripts", "utils.R"))
source(file.path("scripts", "exposure_morphology.R"))

expect_true <- function(x, label) {
  if (!isTRUE(x)) stop("FAILED: ", label)
}

expect_equal <- function(x, y, label, tolerance = 1e-10) {
  if (!isTRUE(all.equal(x, y, tolerance = tolerance, check.attributes = FALSE))) {
    stop(
      "FAILED: ", label, "\nexpected: ", paste(y, collapse = ","),
      "\nactual: ", paste(x, collapse = ",")
    )
  }
}

dates <- seq(as.Date("2020-01-01"), as.Date("2020-01-12"), by = "day")

# Wang five-or-more spell rule.
spell5 <- detect_wang_spells(
  dates,
  c(FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, rep(FALSE, 6)),
  min_length = 5L
)
expect_equal(nrow(spell5$events), 1L, "five-day spell detected")
expect_equal(spell5$events$event_days, 5L, "five-day spell length")
spell4 <- detect_wang_spells(
  dates,
  c(FALSE, TRUE, TRUE, TRUE, TRUE, rep(FALSE, 7)),
  min_length = 5L
)
expect_equal(nrow(spell4$events), 0L, "four-day spell rejected")

# Exact NDNDN event: VHD on days 3–4, HN on days 3–5.
vhd <- rep(FALSE, length(dates))
hn <- rep(FALSE, length(dates))
vhd[3:4] <- TRUE
hn[3:5] <- TRUE
compound <- detect_wang_2d3n(dates, vhd, hn)
expect_equal(nrow(compound$events), 1L, "2D3N event detected")
expect_equal(compound$events$start_idx, 3L, "2D3N start")
expect_equal(compound$events$end_idx, 5L, "2D3N end")
expect_equal(which(compound$daily$event_day), 3:5, "2D3N event days")
expect_equal(which(compound$daily$affected_1_5), 6:10, "2D3N post days 1-5")
expect_true(!any(
  compound$daily$event_day & compound$daily$affected_1_5
), "event and post-event phases exclusive")

# Two non-consecutive VHDs must not satisfy NDNDN.
vhd_bad <- rep(FALSE, length(dates))
vhd_bad[c(3, 5)] <- TRUE
bad_compound <- detect_wang_2d3n(dates, vhd_bad, hn)
expect_equal(nrow(bad_compound$events), 0L, "non-consecutive VHDs rejected")

# Overlapping NDNDN windows merge into one continuous compound event.
vhd_long <- rep(FALSE, length(dates))
hn_long <- rep(FALSE, length(dates))
vhd_long[3:5] <- TRUE
hn_long[3:6] <- TRUE
merged <- detect_wang_2d3n(dates, vhd_long, hn_long)
expect_equal(nrow(merged$events), 1L, "overlapping 2D3N windows merged")
expect_equal(
  c(merged$events$start_idx, merged$events$end_idx),
  c(3L, 6L),
  "merged 2D3N span"
)
expect_equal(merged$events$component_windows, 2L, "component-window count")

# Legacy monthly-weather helper now follows the exact NDNDN rule.
expect_equal(
  which(flag_2d3n_window(vhd, hn)),
  3:5,
  "utils exact 2D3N helper"
)
expect_true(
  !any(flag_2d3n_window(vhd_bad, hn)),
  "utils rejects approximate five-day count proxy"
)

# Calendar-spillover assignment: Jan 30–Feb 1 event, five post days in Feb.
boundary_dates <- seq(as.Date("2020-01-25"), as.Date("2020-02-10"), by = "day")
boundary_vhd <- boundary_dates %in% as.Date(c("2020-01-30", "2020-01-31"))
boundary_hn <- boundary_dates %in% as.Date(c(
  "2020-01-30", "2020-01-31", "2020-02-01"
))
boundary <- detect_wang_2d3n(boundary_dates, boundary_vhd, boundary_hn)
boundary_month <- summarise_event_months(
  boundary_dates,
  boundary$events,
  boundary$daily,
  "test"
)
jan <- boundary_month[boundary_month$month_id == "2020-01", ]
feb <- boundary_month[boundary_month$month_id == "2020-02", ]
expect_equal(jan$test_onset_count, 1L, "boundary onset in January")
expect_equal(jan$test_overlap_count, 1L, "boundary January overlap")
expect_equal(feb$test_overlap_count, 1L, "boundary February overlap")
expect_equal(jan$test_event_days, 2L, "boundary January event days")
expect_equal(feb$test_event_days, 1L, "boundary February event days")
expect_equal(feb$test_affected_1_5_days, 5L, "post-event days assigned to February")

# Li threshold and event-merge test on a complete 1980–2023 reference.
li_dates <- seq(as.Date("1980-01-01"), as.Date("2023-12-31"), by = "day")
cal <- no_leap_calendar_day(li_dates)
li_tmax <- 24 + 6 * sin(2 * pi * (cal - 172) / 365)
target_hot <- li_dates %in% c(
  seq(as.Date("2023-07-01"), as.Date("2023-07-03"), by = "day"),
  seq(as.Date("2023-07-05"), as.Date("2023-07-07"), by = "day")
)
li_tmax[target_hot] <- li_tmax[target_hot] + 12
li <- detect_li_heatwaves(li_dates, li_tmax)
li_2023 <- li$events[
  li$events$start_date >= as.Date("2023-01-01"),
  ,
  drop = FALSE
]
expect_equal(nrow(li_2023), 1L, "Li events with interval of two days merged")
expect_equal(li_2023$start_date, as.Date("2023-07-01"), "Li merged start")
expect_equal(li_2023$end_date, as.Date("2023-07-07"), "Li merged end")

# Leap-day normalization does not shift March and later calendar days.
expect_equal(
  no_leap_calendar_day(as.Date(c("2019-03-01", "2020-03-01"))),
  c(60L, 60L),
  "no-leap calendar alignment"
)

cat("test_exposure_morphology: PASS\n")
