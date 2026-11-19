"""One-year-ahead benchmarks for released first-hospitalisation counts.

The three rules are fixed across endpoints and target years. Forecasts for
2017–2019 check performance before the 2020 stress case. The first target
has four available years of history. The log-linear rules extrapolate OLS
fits on log counts and exponentiate directly (geometric-trend benchmarks).
The signed difference is 100 × (observed / benchmark − 1). The three
historical checks do not calibrate a prediction interval or a causal effect.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import exp, fsum, isfinite, log
from pathlib import Path

from .service_context import load_annual_counts


FIRST_YEAR = 2013
VALIDATION_YEARS = (2017, 2018, 2019)
STRESS_YEAR = 2020
BENCHMARKS = ("last_observation", "expanding_log_linear", "trailing_3_log_linear")


def _point_benchmark(
    history: Sequence[tuple[int, int]], target_year: int, benchmark: str
) -> float:
    """Make a one-year-ahead prediction using exactly the supplied fit window."""
    if not history or history[-1][0] != target_year - 1:
        raise ValueError("Forecast history must end in the year before the target")
    if tuple(year for year, _ in history) != tuple(range(history[0][0], target_year)):
        raise ValueError("Forecast history must contain consecutive ordered years")
    if any(type(count) is not int or count <= 0 for _, count in history):
        raise ValueError("These count benchmarks require positive integer training counts")
    if benchmark == "last_observation" and len(history) == 1:
        return float(history[-1][1])
    trailing = benchmark == "trailing_3_log_linear" and len(history) == 3
    expanding = (
        benchmark == "expanding_log_linear"
        and history[0][0] == FIRST_YEAR
        and len(history) >= 4
    )
    if not (trailing or expanding):
        raise ValueError(f"Unexpected fit window for benchmark {benchmark!r}")

    years, counts = zip(*history)
    logs = [log(count) for count in counts]
    center = fsum(years) / len(years)
    mean_log = fsum(logs) / len(logs)
    slope = fsum((x - center) * (y - mean_log) for x, y in zip(years, logs)) / fsum(
        (x - center) ** 2 for x in years
    )
    return exp(mean_log + slope * (target_year - center))


def benchmark_rows(counts: Mapping[str, Mapping[int, int]]) -> list[dict]:
    """Evaluate the fixed rules; the prediction function never sees a target count."""
    rows = []
    for target in (*VALIDATION_YEARS, STRESS_YEAR):
        for outcome in ("chd", "hf"):
            history = [(year, counts[outcome][year]) for year in range(FIRST_YEAR, target)]
            windows = (history[-1:], history, history[-3:])
            for benchmark, window in zip(BENCHMARKS, windows):
                prediction = _point_benchmark(window, target, benchmark)
                if not isfinite(prediction) or prediction <= 0:
                    raise ValueError("The count benchmark must be positive and finite")
                observed = counts[outcome][target]
                rows.append(
                    {
                        "target_year": target,
                        "phase": "2020_stress_case" if target == STRESS_YEAR else "pre_2020_validation",
                        "outcome": outcome,
                        "benchmark": benchmark,
                        "training_start": window[0][0],
                        "training_end": window[-1][0],
                        "training_years": len(window),
                        "observed_count": observed,
                        "benchmark_count": round(prediction, 6),
                        "observed_minus_benchmark_pct": round(100 * (observed / prediction - 1), 6),
                    }
                )
    return rows


def analyze(annual_path: Path) -> list[dict]:
    """Build all 24 comparisons from the release's validated 22 annual totals."""
    return benchmark_rows(load_annual_counts(annual_path))
