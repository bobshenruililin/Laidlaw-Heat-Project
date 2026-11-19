"""Arithmetic checks on the approved release. Each input row has an explicit role."""

import csv
import math
from pathlib import Path

from .service_context import BASE_YEAR, CONTEXT, OUTCOMES
from .weather_design import EXPOSURES


ANNUAL = "outputs/tables/cvd_descriptive_annual_totals.csv"
ESTIMATES = "outputs/tables/cvd_core_robust_estimates.csv"
METHODS = ("model", "HC1", "NeweyWest_lag3", "NeweyWest_lag6")


def annual_changes(context):
    """Outcome years also carry the break-even, outcome-specific person-time ratio."""
    baseline = next(row for row in context if row["year"] == BASE_YEAR)
    rows = []
    for index, year in enumerate(context):
        for series in (*OUTCOMES, *CONTEXT):
            count = year[series]
            previous = context[index - 1][series] if index else None
            rows.append({
                "year": year["year"], "series": series, "count": count,
                "previous_count": previous,
                "year_on_year_pct": 100 * (count / previous - 1) if previous else None,
                "break_even_person_time_vs_2019": count / baseline[series] if series in OUTCOMES else None,
            })
    return rows


def bh_adjust(p_values):
    """Benjamini–Hochberg for the supplied complete family; preserve input order."""
    if not p_values or any(not 0 <= p <= 1 for p in p_values):
        raise ValueError("A complete finite set of p-values in [0,1] is required")
    order = sorted(range(len(p_values)), key=p_values.__getitem__)
    adjusted = [0.0] * len(order)
    bound = 1.0
    for rank in range(len(order), 0, -1):
        index = order[rank - 1]
        bound = min(bound, p_values[index] * len(order) / rank)
        adjusted[index] = bound
    return adjusted


def weather_models(path: Path):
    """Reconstruct the exact twelve-member family and its 48 published intervals."""
    rows = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for record in csv.DictReader(stream):
            if (record["family"], record["model_structure"], record["offset_policy"]) != (
                "negative_binomial", "single_exposure", "days_only"
            ):
                continue
            key = record["outcome"], record["exposure"], record["se_method"]
            if key in rows:
                raise ValueError(f"Duplicate baseline cell: {key}")
            if record["data_status"] != "HA_APPROVED_AGGREGATE" or record["n_months"] != "132":
                raise ValueError(f"Unexpected baseline provenance or calendar length: {key}")
            rows[key] = record
    required = [(o, x, s) for o in OUTCOMES for x in EXPOSURES for s in METHODS]
    if set(rows) != set(required):
        raise ValueError("The full two-outcome, six-exposure, four-covariance panel is required")
    lag_six = [key for key in required if key[-1] == "NeweyWest_lag6"]
    q_values = dict(zip(lag_six, bh_adjust([float(rows[key]["p_value"]) for key in lag_six])))
    result = []
    for outcome, exposure, method in required:
        key = outcome, exposure, method
        row = rows[key]
        increment = EXPOSURES[exposure][1]
        if int(row["scale"]) != increment:
            raise ValueError(f"Wrong reporting increment: {key}")
        rr, low, high, p = (float(row[k]) for k in ("rr", "rr_low", "rr_high", "p_value"))
        if not (0 < low <= rr <= high and math.isfinite(high) and 0 <= p <= 1):
            raise ValueError(f"Invalid interval or p-value: {key}")
        # Script 31 fits X/increment. Its exported coefficient is already on the reporting scale.
        if not math.isclose(math.exp(float(row["estimate"])), rr, rel_tol=1e-10):
            raise ValueError(f"Count ratio disagrees with coefficient: {key}")
        q = q_values.get(key)
        if q is not None and not math.isclose(q, float(row["q_value_core_bh"]), abs_tol=1e-12):
            raise ValueError(f"Released adjusted p-value disagrees with the complete family: {key}")
        result.append({"outcome": outcome, "exposure": exposure, "increment": increment,
                       "se_method": method, "rr": rr, "rr_low": low, "rr_high": high,
                       "p_value": p, "q_value": q})
    return result
