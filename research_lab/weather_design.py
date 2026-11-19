"""Unweighted calendar-adjusted variation in the six Hong Kong weather exposures.

The unit is the territory-month. All sums of squares use the original °C or day
scale. A share is unchanged by the paper's per-five-day reporting increment.
These projections describe the weather design alone. Negative-binomial weights,
outcomes and model-frame observation metadata do not enter this calculation.

The archived outputs of scripts 48 and 49 used a truncated-power basis padded
with a quadratic. The current scripts share the natural cubic basis here. The
four-df full-period projection is checked against the correlations released
by the R analysis.
"""

from __future__ import annotations

import calendar
import csv
import hashlib
import io
from pathlib import Path

import numpy as np


CLIMATE = "data_processed/climate_monthly_2013_2023.csv"
R_CORRELATIONS = "outputs/tables/cvd_exposure_correlations.csv"
# Both files are present at b3380ded3c9c65e47c69be2984d32cf404504a11.
SOURCE_SHA256 = {
    CLIMATE: "85acacff8597d67232db34acfba2442329526b9891b392ea8e87f92e0175af52",
    R_CORRELATIONS: "dbf2a4af2ab3f8616898cfd5a6bffce47c00da8cd51e80326d660a0ec09a1cff",
}
# Order, units and increments follow core_specs in scripts/31_cvd_core_robustness.R.
EXPOSURES = {
    "mean_temp": ("degC", 1), "mean_tmax": ("degC", 1), "mean_tmin": ("degC", 1),
    "hot_nights": ("days", 5), "cold_days": ("days", 5), "very_hot_days": ("days", 5),
}
# One full design and the two disjoint windows delimited by January 2020 in
# the parent paper. Each window has its own month effects, knots and boundaries.
WINDOWS = (("2013-2023", 2013, 2023), ("2013-2019", 2013, 2019), ("2020-2023", 2020, 2023))
REGISTERED_DF = (3, 4, 6, 8)


def _source_rows(root: Path, relative: str) -> list[dict[str, str]]:
    content = (root / relative).read_bytes()
    if hashlib.sha256(content).hexdigest() != SOURCE_SHA256[relative]:
        raise ValueError(f"Unrecognised source revision: {relative}")
    return list(csv.DictReader(io.StringIO(content.decode("utf-8"))))


def _weather_matrix(rows: list[dict[str, str]]) -> np.ndarray:
    calendar_months = [(yr, mo) for yr in range(2013, 2024) for mo in range(1, 13)]
    if len(rows) != len(calendar_months):
        raise ValueError("Expected one HKO row per month from 2013-01 to 2023-12")
    for row, (year, month) in zip(rows, calendar_months):
        month_id = f"{year:04}-{month:02}"
        days = calendar.monthrange(year, month)[1]
        if (row["month_id"], row["month_date"], row["station"]) != (month_id, month_id + "-01", "HKO"):
            raise ValueError(f"Calendar or station mismatch at {month_id}")
        if (int(row["year"]), int(row["month"])) != (year, month):
            raise ValueError(f"Year/month fields disagree at {month_id}")
        if any(int(row[key]) != days for key in ("expected_days", "observed_days", "observed_tmin", "observed_tmax")):
            raise ValueError(f"Incomplete daily coverage at {month_id}")
        if not float(row["mean_tmin"]) <= float(row["mean_temp"]) <= float(row["mean_tmax"]):
            raise ValueError(f"Inconsistent temperature summaries at {month_id}")
        for name, (unit, _) in EXPOSURES.items():
            if unit == "days":
                count = float(row[name])
                if not count.is_integer() or not 0 <= count <= days:
                    raise ValueError(f"Invalid {name} at {month_id}")
    values = np.array([[float(row[name]) for name in EXPOSURES] for row in rows])
    if not np.isfinite(values).all():
        raise ValueError("Non-finite monthly exposure in the declared weather panel")
    return values


def natural_spline(time: np.ndarray, df: int = 4) -> np.ndarray:
    """Columns spanning R splines::ns(time, df=df), given an intercept.

    Use the linear term and df-1 independent differences of truncated cubics
    formed from all knots, including the left boundary. Subtracting the
    penultimate-knot function makes the spline linear beyond the right
    boundary. R uses interior quantiles at k/df and knots on both boundaries.
    """
    time = np.asarray(time, dtype=float)
    if isinstance(df, bool) or not isinstance(df, (int, np.integer)) or df < 1:
        raise ValueError("Spline df must be a positive integer")
    if time.ndim != 1 or len(time) < df + 1 or not np.isfinite(time).all() or time.min() == time.max():
        raise ValueError(f"The spline needs at least {df + 1} finite observations on a nonconstant time axis")
    x = (time - time.min()) / (time.max() - time.min())
    knots = np.quantile(x, np.linspace(0, 1, df + 1))
    if np.any(np.diff(knots) <= 0):
        raise ValueError("The observed time distribution must produce distinct spline knots")
    right = knots[-1]

    def divided_cubic(knot: float) -> np.ndarray:
        return (np.maximum(x - knot, 0) ** 3 - np.maximum(x - right, 0) ** 3) / (right - knot)

    reference = divided_cubic(knots[-2])
    return np.column_stack([x] + [divided_cubic(knot) - reference for knot in knots[:-2]])


def _adjust(months: np.ndarray, values: np.ndarray, df: int = 4) -> np.ndarray:
    # One column per calendar month incorporates the intercept. Time is
    # consecutive here because the complete, ordered calendar was verified.
    month_indicators = (months[:, None] == np.arange(1, 13)).astype(float)
    controls = np.column_stack((month_indicators, natural_spline(np.arange(len(months)), df)))
    coefficients, _, rank, _ = np.linalg.lstsq(controls, values, rcond=None)
    if rank != 12 + df:
        raise ValueError(f"Expected {12 + df} independent calendar columns, found {rank}")
    return values - controls @ coefficients


def _check_r_reference(rows: list[dict[str, str]], values: np.ndarray, residuals: np.ndarray) -> None:
    # Script 31 already exported both full-period exposure-correlation matrices
    # from R. Every cell is checked for both CHD and HF source labels.
    types = {
        "raw": np.corrcoef(values.T),
        "month_and_trend_residualised": np.corrcoef(residuals.T),
    }
    reference = {}
    for row in rows:
        key = row["outcome"], row["correlation_type"], row["exposure_1"], row["exposure_2"]
        if key in reference:
            raise ValueError(f"Duplicate R exposure-correlation cell: {key}")
        reference[key] = float(row["correlation"])
    names = tuple(EXPOSURES)
    for outcome in ("chd", "hf"):
        for kind, matrix in types.items():
            for i, first in enumerate(names):
                for j, second in enumerate(names):
                    key = outcome, kind, first, second
                    expected = reference.pop(key, None)
                    if expected is None or not np.isclose(matrix[i, j], expected, rtol=0, atol=1e-10):
                        raise ValueError(f"R exposure-correlation benchmark failed: {key}")
    if reference:
        raise ValueError("Unexpected cells in R exposure-correlation reference")


def _summary(window: str, name: str, labels: list[str], values: np.ndarray, residuals: np.ndarray) -> dict:
    raw_ss = float(np.sum((values - values.mean()) ** 2))
    residual_ss = float(residuals @ residuals)
    if raw_ss <= 0 or residual_ss <= np.finfo(float).eps * raw_ss:
        raise ValueError(f"Insufficient residual variation for {name} in {window}")
    shares = residuals**2 / residual_ss
    order = np.argsort(-shares, kind="stable")
    # Minimum number of largest squared residuals accounting for >=50%.
    half = int(np.searchsorted(np.cumsum(shares[order]), 0.5, side="left") + 1)
    unit, increment = EXPOSURES[name]
    return {
        "window": window, "exposure": name, "n_months": len(labels), "unit": unit,
        "reporting_increment": increment, "raw_ss": round(raw_ss, 10),
        "residual_ss": round(residual_ss, 10), "residual_share": round(residual_ss / raw_ss, 10),
        "residual_sd": round(float(np.std(residuals, ddof=1)), 10),
        "top_month": labels[int(order[0])], "largest_month_share": round(float(shares[order[0]]), 10),
        "months_for_half_ss": half,
    }


def design_grid(repo_root: Path, degrees: tuple[int, ...]) -> list[dict]:
    """Evaluate every exposure and window for each requested registered calendar."""
    if not degrees or any(type(df) is not int or df not in REGISTERED_DF for df in degrees):
        raise ValueError(f"Choose one or more registered spline degrees from {REGISTERED_DF}")
    if len(set(degrees)) != len(degrees):
        raise ValueError("Each spline degree may appear once")
    rows = _source_rows(repo_root, CLIMATE)
    weather = _weather_matrix(rows)
    reference = _source_rows(repo_root, R_CORRELATIONS) if 4 in degrees else []
    years = np.array([int(row["year"]) for row in rows])
    months = np.array([int(row["month"]) for row in rows])
    results = []
    for df in degrees:
        for label, first, last in WINDOWS:
            indices = (years >= first) & (years <= last)
            values = weather[indices]
            residuals = _adjust(months[indices], values, df)
            if df == 4 and first == 2013 and last == 2023:
                _check_r_reference(reference, values, residuals)
            dates = [row["month_id"] for row, use in zip(rows, indices) if use]
            for j, name in enumerate(EXPOSURES):
                result = _summary(label, name, dates, values[:, j], residuals[:, j])
                result["spline_df"] = df
                results.append(result)
    return results


def analyze(repo_root: Path) -> list[dict]:
    """Return the four-df analysis of record in each of the three fixed windows."""
    results = design_grid(repo_root, (4,))
    for row in results:
        del row["spline_df"]
    return results
