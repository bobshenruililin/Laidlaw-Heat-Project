"""Annual recorded first stays beside published Hong Kong inpatient throughput.

Only released annual counts and transcribed public statistics enter the join.
An index is an individual series divided by its own 2019 count and times 100.
"""

import csv
from pathlib import Path


YEARS = tuple(range(2013, 2024))
BASE_YEAR = 2019
OUTCOMES = ("chd", "hf")
CONTEXT = ("all_hospital_episodes", "circulatory_episodes", "ha_episodes")
CELL_FIELDS = (*CONTEXT, "private_episodes", "correctional_episodes")
SOURCE_FILE = "hk_inpatient_digest_cells.csv"


def _rows(path, required):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        if len(columns) != len(set(columns)) or not set(required).issubset(columns):
            raise ValueError(f"{Path(path).name}: invalid header; expected {required}")
        yield from reader


def _integer(row, field):
    value = row[field]
    if not value or not value.isascii() or not value.isdigit():
        raise ValueError(f"Expected a nonnegative integer for {field}")
    return int(value)


def load_annual_counts(path):
    """Read the 22 released totals; years index the two lower-case outcomes."""
    result = {outcome: {} for outcome in OUTCOMES}
    for row in _rows(path, ("outcome", "year", "data_status", "n_months", "total_events")):
        outcome = row["outcome"]
        year = _integer(row, "year")
        if row["data_status"] != "HA_APPROVED_AGGREGATE" or _integer(row, "n_months") != 12:
            raise ValueError(f"{outcome} {year}: expected approved annual record covering 12 months")
        if outcome not in result or year not in YEARS or year in result[outcome]:
            raise ValueError(f"Unexpected or duplicate outcome/year: {outcome} {year}")
        result[outcome][year] = _integer(row, "total_events")
    for outcome in OUTCOMES:
        if set(result[outcome]) != set(YEARS):
            raise ValueError(f"{outcome} requires one annual record in each year 2013–2023")
    return result


def _service_counts(path):
    # Each study year appears in at least two editions. Separately, the three
    # provider totals in table 13.10 must add to the table 13.9 all-cause count.
    counts = {}
    editions = {year: set() for year in YEARS}
    for row in _rows(path, ("edition", "year", *CELL_FIELDS)):
        year = _integer(row, "year")
        edition = _integer(row, "edition")
        if year not in editions or edition not in (2019, 2021, 2024, 2025) or edition <= year:
            raise ValueError(f"Unexpected digest edition/year: {edition} {year}")
        if edition in editions[year]:
            raise ValueError(f"Duplicate digest row: {edition} {year}")
        cells = {key: _integer(row, key) for key in CELL_FIELDS}
        provider_sum = cells["ha_episodes"] + cells["private_episodes"] + cells["correctional_episodes"]
        if cells["all_hospital_episodes"] != provider_sum:
            raise ValueError(f"{edition} {year}: table 13.10 provider sum differs from table 13.9 total")
        if cells["circulatory_episodes"] > provider_sum:
            raise ValueError(f"{edition} {year}: circulatory count exceeds the all-hospital total")
        if year in counts and counts[year] != cells:
            raise ValueError(f"{edition} {year}: cells disagree across editions")
        counts[year] = cells
        editions[year].add(edition)
    if any(len(vintages) < 2 for vintages in editions.values()):
        raise ValueError("Each study year requires matching cells in at least two distinct digest editions")
    return counts


def analyse(annual_path, sources_dir=None):
    """Return all five annual series and unrounded within-series 2019 indices."""
    cohort = load_annual_counts(annual_path)
    directory = Path(sources_dir) if sources_dir is not None else Path(__file__).with_name("sources")
    external = _service_counts(directory / SOURCE_FILE)
    rows = []
    for year in YEARS:
        row = {"year": year, **{key: cohort[key][year] for key in OUTCOMES}}
        row.update({key: external[year][key] for key in CONTEXT})
        rows.append(row)
    baseline = rows[YEARS.index(BASE_YEAR)]
    for key in (*OUTCOMES, *CONTEXT):
        if baseline[key] == 0:
            raise ValueError(f"{key}: zero 2019 count cannot anchor an index")
        for row in rows:
            row[f"{key}_index"] = 100 * row[key] / baseline[key]
    return rows
