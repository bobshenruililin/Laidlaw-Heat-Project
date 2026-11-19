"""Evaluate a declarative weather-design question without reading hospital counts."""

import json
import math
from pathlib import Path

from . import weather_design


METRICS = {"months_for_half_ss", "residual_share", "largest_month_share"}
FAMILIES = {"threshold_days": "days", "temperatures": "degC", "all_six": None}
CALENDAR_DF = {3, 4, 6, 8}
FIELDS = {"question", "spline_df", "window", "family", "metric", "comparison", "threshold"}


def read_card(path: Path):
    if path.stat().st_size > 4096:
        raise ValueError("Use a single JSON question card under 4 KiB")
    def unique_keys(pairs):
        if len(dict(pairs)) != len(pairs):
            raise ValueError("Duplicate JSON field")
        return dict(pairs)
    spec = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    if not isinstance(spec, dict) or set(spec) != FIELDS:
        raise ValueError(f"Question card requires exactly {sorted(FIELDS)}")
    if not isinstance(spec["question"], str) or not 1 <= len(spec["question"].strip()) <= 300:
        raise ValueError("Write one question in 1–300 characters")
    degrees = spec["spline_df"]
    if not isinstance(degrees, list) or not degrees or any(type(x) != int or x not in CALENDAR_DF for x in degrees):
        raise ValueError("Calendar df must be a nonempty subset of [3,4,6,8]")
    if degrees != sorted(set(degrees)):
        raise ValueError("List calendar settings in increasing order without duplicates")
    for key, options in (("family", FAMILIES), ("window", [w[0] for w in weather_design.WINDOWS]),
                         ("comparison", ["at_least", "at_most"]), ("metric", METRICS)):
        if not isinstance(spec[key], str) or spec[key] not in options:
            raise ValueError(f"Unknown {key}: {spec[key]!r}")
    limit = spec["threshold"]
    if type(limit) not in (int, float) or not math.isfinite(limit):
        raise ValueError("The threshold must be a finite number")
    if spec["metric"] == "months_for_half_ss":
        length = next(12 * (last - first + 1) for label, first, last in weather_design.WINDOWS if label == spec["window"])
        if not float(limit).is_integer() or not 1 <= limit <= length:
            raise ValueError("Month thresholds must be whole numbers within the chosen window")
    elif not 0 <= limit <= 1:
        raise ValueError("Share thresholds are fractions in [0,1]")
    return spec


def evaluate(root: Path, spec):
    grid = weather_design.design_grid(root, tuple(spec["spline_df"]))
    unit = FAMILIES[spec["family"]]
    decisions = []
    for row in grid:
        if row["window"] != spec["window"] or (unit and row["unit"] != unit):
            continue
        value = row[spec["metric"]]
        met = value >= spec["threshold"] if spec["comparison"] == "at_least" else value <= spec["threshold"]
        decisions.append({"spline_df": row["spline_df"], "exposure": row["exposure"],
                          "window": row["window"], "metric": spec["metric"],
                          "value": value, "criterion_met": bool(met)})
    n_exposures = sum(unit is None or units == unit for units, _ in weather_design.EXPOSURES.values())
    if len(grid) != 18 * len(spec["spline_df"]) or len(decisions) != n_exposures * len(spec["spline_df"]):
        raise ValueError("Incomplete design grid")
    verdict = {
        "question": spec["question"], "scope": "Unweighted exposure geometry; no health outcomes.",
        "all_selected_cells_meet_criterion": all(row["criterion_met"] for row in decisions),
        "cells_meeting_criterion": sum(row["criterion_met"] for row in decisions),
        "cells_evaluated": len(decisions), "grid_rows_returned": len(grid),
    }
    return grid, decisions, verdict
