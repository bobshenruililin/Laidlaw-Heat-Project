"""Prospective check of how prior-stay history changes a first-stay count.

The secure analyst defines one candidate per person, outcome and month: the
earliest qualifying episode in that month after the required diagnoses and
entry have been established. Both arms must consume the very same candidate
relation. Freeze the source version, eligibility, care setting, episode and
same-day rules. Use only information available through the candidate episode.
Neither future diagnoses nor future follow-up may establish today's eligibility.

Vary one rule only. Search for earlier qualifying stays from either (a) the
first day K calendar months before the candidate month or (b) the earliest
available history. Both searches stop immediately before the candidate episode.
The analyst must verify continuous observation across the fixed window for
every included candidate, date ordering, and identity of the two base sets.
The eligible base may therefore differ from the original release. A short
lookback can count someone again after an old stay. Its count is a sensitivity
measure. A restricted common base cannot validate the original whole population.

In the secure system independently count the members exclusive to each arm,
and verify that a documented older stay explains every fixed-only member.
Return same-month aggregates locally; an unavailable or suppressed cell is
missing, never zero. Matching identifiers attest to declared rules: the source
analyst must verify what the queries actually implement. If an arm reproduces
the full original definition and scope, independently obtain the original
monthly counts where available and the released totals for complete years.
Reconcile the original extraction separately if neither arm matches it.

An observed paired gap measures sensitivity to this particular prior-stay
rule at a fixed date. Its absence cannot validate diagnosis timing, record
capture, or an underlying incidence trend. Risk-set size, mortality, care
contact and true health can change with either pattern. This module reads and
writes no files. Its executable example uses invented aggregate counts only.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class BaseRules:
    source_snapshot_id: str
    population_and_entry_query_id: str
    candidate_episode_query_id: str


@dataclass(frozen=True, slots=True)
class HistoryDesign:
    outcome: str
    first_month: str
    last_month: str
    source_start: str
    fixed_months: int
    fixed_base: BaseRules
    available_base: BaseRules
    as_of_and_coverage_attestation: str
    original_arm: str | None = None
    original_scope_attestation: str | None = None


@dataclass(frozen=True, slots=True)
class PairedMonth:
    month: str
    candidates: int
    fixed: int
    available: int
    fixed_only_with_older_stay: int
    available_only: int
    original: int | None = None


@dataclass(frozen=True, slots=True)
class HistoryComparison:
    outcome: str
    # Counts fixed minus available. Every difference compares the same month.
    paired_differences: tuple[tuple[str, int], ...]
    reconciled_months: tuple[str, ...]
    reconciled_years: tuple[int, ...]
    complete_years_without_annual_check: tuple[int, ...]


def _month_number(month: str) -> int:
    if not isinstance(month, str) or len(month) != 7:
        raise ValueError("Expected an ISO calendar month YYYY-MM")
    first_day = date.fromisoformat(month + "-01")
    if first_day.isoformat()[:7] != month:
        raise ValueError("Expected an ISO calendar month YYYY-MM")
    return (first_day.year - 1) * 12 + first_day.month - 1


def _valid_count(value: int) -> bool:
    return type(value) is int and value >= 0


def _has_reference(value: str | None) -> bool:
    return isinstance(value, str) and bool(value.strip())


def compare_history(
    design: HistoryDesign,
    months: Sequence[PairedMonth],
    released_annual: Mapping[int, int] | None = None,
) -> HistoryComparison:
    """Check a prespecified consecutive panel for one outcome, entirely in memory.

    Provide original counts only when a versioned attestation links an arm to
    the original extraction, including its population. Annual references may
    span other years. Only complete common calendar years can be reconciled.
    Matching an annual sum does not establish month-by-month agreement.
    """
    if design.outcome not in ("chd", "hf"):
        raise ValueError("Choose one outcome-specific series")
    base = design.fixed_base
    if not isinstance(base, BaseRules) or not isinstance(design.available_base, BaseRules):
        raise ValueError("Supply the base-rule references for both arms")
    references = (
        base.source_snapshot_id, base.population_and_entry_query_id,
        base.candidate_episode_query_id, design.as_of_and_coverage_attestation,
    )
    if base != design.available_base or not all(_has_reference(v) for v in references):
        raise ValueError("Both arms need identical, documented base rules and as-of coverage")
    if design.original_arm not in (None, "fixed", "available"):
        raise ValueError("The original arm must be fixed, available, or unverified (None)")
    if design.original_arm is None:
        if design.original_scope_attestation is not None or released_annual is not None:
            raise ValueError("Original counts require an independently linked original arm")
    elif not _has_reference(design.original_scope_attestation):
        raise ValueError("The original arm needs a source and population scope attestation")

    first = _month_number(design.first_month)
    last = _month_number(design.last_month)
    if not _valid_count(design.fixed_months) or design.fixed_months == 0:
        raise ValueError("Fixed lookback must be a positive whole number of months")
    source_start = _month_number(design.source_start)
    if first - source_start < design.fixed_months:
        raise ValueError("Source coverage cannot supply the complete prespecified fixed lookback")
    if last < first or len(months) != last - first + 1:
        raise ValueError("Supply every prespecified month exactly once, in order")

    differences = []
    matched_months = []
    months_by_year: Counter[int] = Counter()
    arm_totals: Counter[int] = Counter()
    for offset, row in enumerate(months):
        if not isinstance(row, PairedMonth):
            raise ValueError("Supply paired aggregate month records")
        if _month_number(row.month) != first + offset:
            raise ValueError("Supply every prespecified month exactly once, in order")
        counts = (row.candidates, row.fixed, row.available, row.fixed_only_with_older_stay, row.available_only)
        if not all(_valid_count(v) for v in counts):
            raise ValueError(f"Missing or invalid aggregate count in {row.month}")
        gap = row.fixed - row.available
        if not 0 <= row.available <= row.fixed <= row.candidates:
            raise ValueError(f"Nested count or candidate totals disagree in {row.month}")
        if row.available_only != 0 or gap != row.fixed_only_with_older_stay:
            raise ValueError(f"Independent membership reconciliation failed in {row.month}")
        if first + offset - source_start == design.fixed_months and gap:
            raise ValueError(f"The two history windows are identical in {row.month}")
        differences.append((row.month, gap))
        year = int(row.month[:4])
        months_by_year[year] += 1
        if row.original is not None and design.original_arm is None:
            raise ValueError("An original monthly count requires a linked original arm")
        if design.original_arm is not None:
            original_arm_count = row.fixed if design.original_arm == "fixed" else row.available
            arm_totals[year] += original_arm_count
            if row.original is not None:
                if not _valid_count(row.original) or row.original != original_arm_count:
                    raise ValueError(f"Original monthly count disagrees in {row.month}")
                matched_months.append(row.month)

    full_years = {year for year, month_count in months_by_year.items() if month_count == 12}
    matched_years = []
    if released_annual is not None:
        for year, count in released_annual.items():
            if type(year) is not int or not 1 <= year <= 9999 or not _valid_count(count):
                raise ValueError("Invalid original annual reference")
            if year in full_years:
                if count != arm_totals[year]:
                    raise ValueError(f"Original annual count disagrees in {year}")
                matched_years.append(year)
    return HistoryComparison(
        design.outcome, tuple(differences), tuple(matched_months),
        tuple(sorted(matched_years)), tuple(sorted(full_years.difference(matched_years))),
    )


def synthetic_fixture(world: str) -> tuple[HistoryDesign, tuple[PairedMonth, ...], dict[int, int]]:
    """Two invented worlds with identical available-history counts in 2001–2002.

    In 'older_stays', 20 people have their first qualifying stay every month
    indefinitely. Among each cohort, two return once after six months and one
    returns once at each lag from 13 to 24 months; six never return. Thus 34
    candidates appear each month. A 12-month search excludes the two recent
    returns. An expanding search beginning January 2000 also finds one more
    old return per month until all twelve are visible. No future row is used.

    In 'changing_first_stays', nobody returns. New candidates number 32 in
    January 2001, one fewer per month until 20, and 20 thereafter. Both
    history rules now count genuine changes in first stays in this invented
    world. The available arm is identical to that in the first world.
    Independent arithmetic anchors are 32+31+...+21 = 318 and 12×20 = 240.
    Neither construction uses a patient record or estimates a health effect.
    """
    if world not in ("older_stays", "changing_first_stays"):
        raise ValueError("Unknown synthetic world")
    base = BaseRules("synthetic-v1", "synthetic-as-of-entry", "synthetic-candidate-relation")
    design = HistoryDesign(
        "hf", "2001-01", "2002-12", "2000-01", 12, base, base,
        "synthetic-construction", "available", "synthetic-available-arm-reference",
    )
    months = []
    for offset in range(24):
        month = f"{2001 + offset // 12}-{1 + offset % 12:02}"
        history_months = _month_number(month) - _month_number(design.source_start)
        if world == "older_stays":
            observed_old = sum(lag <= history_months for lag in range(13, 25))
            row = PairedMonth(month, 34, 32, 32 - observed_old, observed_old, 0)
        else:
            first_stays = max(20, 32 - offset)
            row = PairedMonth(month, first_stays, first_stays, first_stays, 0, 0)
        months.append(row)
    return design, tuple(months), {2001: 318, 2002: 240}


def synthetic_self_test() -> dict:
    """Run the public counterexample and independent annual anchors, with no inputs."""
    panels = [synthetic_fixture(world) for world in ("older_stays", "changing_first_stays")]
    results = [compare_history(*panel) for panel in panels]
    observed = [tuple(row.available for row in panel[1]) for panel in panels]
    expected_gaps = tuple(min(i, 12) for i in range(24))
    if observed[0] != observed[1]:
        raise AssertionError("The two synthetic observed series should be identical")
    gaps = [tuple(value for _, value in result.paired_differences) for result in results]
    if gaps != [expected_gaps, (0,) * 24]:
        raise AssertionError("The prespecified history comparison should distinguish the worlds")
    if any(result.reconciled_years != (2001, 2002) for result in results):
        raise AssertionError("Annual synthetic reconciliation is incomplete")
    return {
        "status": "PASS", "provenance": "SYNTHETIC",
        "checks": ["identical observed counts", "distinct paired differences", "annual anchors"],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(synthetic_self_test(), indent=2))
