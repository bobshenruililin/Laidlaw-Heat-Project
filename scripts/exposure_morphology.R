# Pure daily-event helpers for source-locked thermal morphology.
#
# No health outcomes are read here. Functions operate on consecutive daily
# dates and logical weather indicators so they can be unit tested directly.

as_daily_dates <- function(date) {
  out <- as.Date(date)
  if (anyNA(out)) stop("date contains missing or invalid values")
  if (anyDuplicated(out)) stop("date must be unique")
  if (is.unsorted(out, strictly = TRUE)) stop("date must be strictly increasing")
  if (length(out) > 1L && any(diff(out) != 1)) {
    stop("date must be a consecutive daily sequence")
  }
  out
}

as_event_flag <- function(x, n, name = "flag") {
  if (length(x) != n) stop(name, " length must equal date length")
  out <- as.logical(x)
  out[is.na(out)] <- FALSE
  out
}

contiguous_event_runs <- function(date, flag, min_length = 1L) {
  date <- as_daily_dates(date)
  flag <- as_event_flag(flag, length(date))
  min_length <- as.integer(min_length)
  if (min_length < 1L) stop("min_length must be >= 1")
  runs <- rle(flag)
  ends <- cumsum(runs$lengths)
  starts <- ends - runs$lengths + 1L
  keep <- which(runs$values & runs$lengths >= min_length)
  if (!length(keep)) {
    return(data.frame(
      event_id = integer(),
      start_idx = integer(),
      end_idx = integer(),
      start_date = as.Date(character()),
      end_date = as.Date(character()),
      event_days = integer(),
      qualifying_days = integer(),
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    event_id = seq_along(keep),
    start_idx = starts[keep],
    end_idx = ends[keep],
    start_date = date[starts[keep]],
    end_date = date[ends[keep]],
    event_days = runs$lengths[keep],
    qualifying_days = runs$lengths[keep],
    stringsAsFactors = FALSE
  )
}

merge_event_windows <- function(events, max_gap_days = 0L) {
  if (!nrow(events)) return(events)
  required <- c("start_idx", "end_idx", "start_date", "end_date")
  missing <- setdiff(required, names(events))
  if (length(missing)) stop("events missing: ", paste(missing, collapse = ", "))
  max_gap_days <- as.integer(max_gap_days)
  ord <- order(events$start_idx, events$end_idx)
  events <- events[ord, , drop = FALSE]

  groups <- integer(nrow(events))
  group <- 1L
  groups[1] <- group
  current_end <- events$end_idx[1]
  for (i in 2:nrow(events)) {
    gap <- events$start_idx[i] - current_end - 1L
    if (gap <= max_gap_days) {
      groups[i] <- group
      current_end <- max(current_end, events$end_idx[i])
    } else {
      group <- group + 1L
      groups[i] <- group
      current_end <- events$end_idx[i]
    }
  }

  merged <- lapply(split(seq_len(nrow(events)), groups), function(idx) {
    start_i <- min(events$start_idx[idx])
    end_i <- max(events$end_idx[idx])
    qualifying <- if ("qualifying_days" %in% names(events)) {
      sum(events$qualifying_days[idx], na.rm = TRUE)
    } else {
      NA_integer_
    }
    data.frame(
      start_idx = start_i,
      end_idx = end_i,
      start_date = min(events$start_date[idx]),
      end_date = max(events$end_date[idx]),
      event_days = end_i - start_i + 1L,
      qualifying_days = qualifying,
      component_windows = length(idx),
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, merged)
  out$event_id <- seq_len(nrow(out))
  out[, c(
    "event_id", "start_idx", "end_idx", "start_date", "end_date",
    "event_days", "qualifying_days", "component_windows"
  )]
}

event_phase_flags <- function(date, events, early_end = 5L, late_end = 21L) {
  date <- as_daily_dates(date)
  n <- length(date)
  in_event <- rep(FALSE, n)
  post_1_5 <- rep(FALSE, n)
  post_6_21 <- rep(FALSE, n)
  event_id <- integer(n)
  event_start <- rep(FALSE, n)

  if (nrow(events)) {
    for (i in seq_len(nrow(events))) {
      idx <- events$start_idx[i]:events$end_idx[i]
      in_event[idx] <- TRUE
      event_id[idx] <- events$event_id[i]
      event_start[events$start_idx[i]] <- TRUE

      if (early_end > 0L) {
        early <- seq.int(events$end_idx[i] + 1L, events$end_idx[i] + early_end)
        early <- early[early >= 1L & early <= n]
        post_1_5[early] <- TRUE
      }

      if (late_end > early_end) {
        late <- seq.int(
          events$end_idx[i] + early_end + 1L,
          events$end_idx[i] + late_end
        )
        late <- late[late >= 1L & late <= n]
        post_6_21[late] <- TRUE
      }
    }
  }

  # An observed event phase takes precedence over a post-event phase. Early
  # post-event days take precedence over late days when events are close.
  post_1_5[in_event] <- FALSE
  post_6_21[in_event | post_1_5] <- FALSE

  data.frame(
    date = date,
    event_id = event_id,
    event_start = event_start,
    event_day = in_event,
    affected_1_5 = post_1_5,
    affected_6_21 = post_6_21,
    stringsAsFactors = FALSE
  )
}

detect_wang_spells <- function(date, flag, min_length = 5L) {
  events <- contiguous_event_runs(date, flag, min_length = min_length)
  list(
    events = events,
    daily = event_phase_flags(date, events, early_end = 0L, late_end = 0L)
  )
}

detect_wang_2d3n <- function(date, very_hot_day, hot_night) {
  date <- as_daily_dates(date)
  n <- length(date)
  vhd <- as_event_flag(very_hot_day, n, "very_hot_day")
  hn <- as_event_flag(hot_night, n, "hot_night")

  # Wang et al. (2019) NDNDN: two consecutive VHDs with the three
  # corresponding hot nights. With HKO daily minima indexed by calendar date,
  # candidate i uses VHD[i:i+1] and HN[i:i+2].
  starts <- if (n >= 3L) {
    which(
      vhd[seq_len(n - 2L)] &
        vhd[seq.int(2L, n - 1L)] &
        hn[seq_len(n - 2L)] &
        hn[seq.int(2L, n - 1L)] &
        hn[seq.int(3L, n)]
    )
  } else {
    integer()
  }

  if (!length(starts)) {
    events <- data.frame(
      event_id = integer(),
      start_idx = integer(),
      end_idx = integer(),
      start_date = as.Date(character()),
      end_date = as.Date(character()),
      event_days = integer(),
      qualifying_days = integer(),
      component_windows = integer(),
      stringsAsFactors = FALSE
    )
  } else {
    candidates <- data.frame(
      event_id = seq_along(starts),
      start_idx = starts,
      end_idx = starts + 2L,
      start_date = date[starts],
      end_date = date[starts + 2L],
      event_days = 3L,
      qualifying_days = 3L,
      stringsAsFactors = FALSE
    )
    # Overlapping or directly touching NDNDN windows form one continuous
    # compound event; no hot-free day separates them.
    events <- merge_event_windows(candidates, max_gap_days = 0L)
  }

  list(
    events = events,
    daily = event_phase_flags(date, events, early_end = 5L, late_end = 5L)
  )
}

no_leap_calendar_day <- function(date) {
  date <- as.Date(date)
  year <- as.integer(format(date, "%Y"))
  month <- as.integer(format(date, "%m"))
  day <- as.integer(format(date, "%d"))
  yday <- as.integer(format(date, "%j"))
  leap <- (year %% 4L == 0L & year %% 100L != 0L) | year %% 400L == 0L
  out <- yday - as.integer(leap & month > 2L)
  # Feb 29 is not used by the May–September Li definition; mapping it to
  # Feb 28 keeps the helper total for completeness.
  out[month == 2L & day == 29L] <- 59L
  out
}

li_calendar_day_threshold <- function(
    date,
    tmax,
    reference_start = as.Date("1980-01-01"),
    reference_end = as.Date("2023-12-31"),
    half_window = 7L,
    probability = 0.90) {
  date <- as_daily_dates(date)
  if (length(tmax) != length(date)) stop("tmax length must equal date length")
  tmax <- as.numeric(tmax)
  reference <- date >= reference_start & date <= reference_end
  years <- unique(as.integer(format(date[reference], "%Y")))
  expected_years <- seq.int(
    as.integer(format(reference_start, "%Y")),
    as.integer(format(reference_end, "%Y"))
  )
  if (!all(expected_years %in% years)) {
    stop("Li reference requires complete year coverage 1980–2023")
  }

  cal_day <- no_leap_calendar_day(date)
  thresholds <- rep(NA_real_, 365L)
  for (d in seq_len(365L)) {
    window_days <- ((seq.int(d - half_window, d + half_window) - 1L) %% 365L) + 1L
    values <- tmax[reference & cal_day %in% window_days]
    if (sum(is.finite(values)) < 30L) {
      stop("Insufficient Li reference observations for calendar day ", d)
    }
    thresholds[d] <- as.numeric(stats::quantile(
      values,
      probs = probability,
      na.rm = TRUE,
      type = 7
    ))
  }
  thresholds[cal_day]
}

detect_li_heatwaves <- function(
    date,
    tmax,
    reference_start = as.Date("1980-01-01"),
    reference_end = as.Date("2023-12-31"),
    warm_months = 5:9,
    probability = 0.90,
    half_window = 7L,
    min_length = 3L,
    merge_gap_days = 2L) {
  date <- as_daily_dates(date)
  threshold <- li_calendar_day_threshold(
    date,
    tmax,
    reference_start = reference_start,
    reference_end = reference_end,
    half_window = half_window,
    probability = probability
  )
  month <- as.integer(format(date, "%m"))
  exceed <- is.finite(tmax) & tmax > threshold & month %in% warm_months
  base_events <- contiguous_event_runs(date, exceed, min_length = min_length)
  events <- merge_event_windows(base_events, max_gap_days = merge_gap_days)
  daily <- event_phase_flags(date, events, early_end = 0L, late_end = 0L)
  daily$threshold <- threshold
  daily$threshold_exceedance <- exceed
  list(events = events, daily = daily)
}

summarise_event_months <- function(date, events, daily, prefix) {
  date <- as_daily_dates(date)
  if (nrow(daily) != length(date)) stop("daily rows must equal date length")
  month_id <- format(date, "%Y-%m")
  months <- unique(month_id)

  event_starts <- if (nrow(events)) {
    table(format(events$start_date, "%Y-%m"))
  } else {
    integer()
  }

  overlap_count <- setNames(integer(length(months)), months)
  if (nrow(events)) {
    for (i in seq_len(nrow(events))) {
      touched <- unique(format(
        seq(events$start_date[i], events$end_date[i], by = "day"),
        "%Y-%m"
      ))
      overlap_count[touched] <- overlap_count[touched] + 1L
    }
  }

  sum_by_month <- function(x) {
    out <- tapply(as.integer(x), month_id, sum)
    as.integer(out[months])
  }

  result <- data.frame(month_id = months, stringsAsFactors = FALSE)
  result[[paste0(prefix, "_onset_count")]] <- as.integer(event_starts[months])
  result[[paste0(prefix, "_onset_count")]][is.na(result[[paste0(prefix, "_onset_count")]])] <- 0L
  result[[paste0(prefix, "_overlap_count")]] <- as.integer(overlap_count[months])
  result[[paste0(prefix, "_event_days")]] <- sum_by_month(daily$event_day)
  result[[paste0(prefix, "_affected_1_5_days")]] <- sum_by_month(daily$affected_1_5)
  result[[paste0(prefix, "_affected_6_21_days")]] <- sum_by_month(daily$affected_6_21)
  result
}
