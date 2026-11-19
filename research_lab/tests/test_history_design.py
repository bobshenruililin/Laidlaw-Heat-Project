"""Only invented aggregates are used in this prospective design test."""

import unittest
from dataclasses import replace

from research_lab.history_design import (
    PairedMonth, compare_history, synthetic_fixture, synthetic_self_test,
)


class HistoryDesignTests(unittest.TestCase):
    def setUp(self):
        self.design, self.months, self.annual = synthetic_fixture("older_stays")

    def test_identical_observations_can_arise_from_distinct_processes(self):
        self.assertEqual(synthetic_self_test()["provenance"], "SYNTHETIC")
        _, alternative, _ = synthetic_fixture("changing_first_stays")
        self.assertEqual([r.available for r in self.months], [r.available for r in alternative])
        january, december, next_january = self.months[0], self.months[11], self.months[12]
        self.assertEqual([r.available for r in (january, december, next_january)], [32, 21, 20])
        self.assertTrue(all(r.fixed == 32 for r in self.months))
        self.assertTrue(all(r.fixed == r.available for r in alternative))

    def test_same_month_comparisons_do_not_depend_on_future_aggregate_rows(self):
        expected = compare_history(self.design, self.months).paired_differences
        zeroes = tuple(PairedMonth(r.month, 0, 0, 0, 0, 0) for r in self.months[7:])
        altered = compare_history(self.design, self.months[:7] + zeroes)
        truncated = compare_history(replace(self.design, last_month="2001-07"), self.months[:7])
        self.assertEqual(altered.paired_differences[:7], expected[:7])
        self.assertEqual(truncated.paired_differences, expected[:7])
        self.assertEqual(altered.paired_differences[-1], ("2002-12", 0))

    def test_base_equality_references_and_window_coverage_are_enforced(self):
        for field in ("source_snapshot_id", "population_and_entry_query_id", "candidate_episode_query_id"):
            different = replace(self.design.available_base, **{field: "different"})
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "identical"):
                compare_history(replace(self.design, available_base=different), self.months)
        for edit in (
            {"as_of_and_coverage_attestation": " "}, {"fixed_months": True},
            {"fixed_months": 0}, {"source_start": "2000-02"}, {"outcome": "combined"},
        ):
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                compare_history(replace(self.design, **edit), self.months)

    def test_requires_complete_ordered_observed_months(self):
        for records in (
            self.months[1:], (self.months[1],) + self.months[1:],
            (replace(self.months[0], month="2001-1"),) + self.months[1:],
        ):
            with self.subTest(first=records[0]), self.assertRaises(ValueError):
                compare_history(self.design, records)

    def test_counts_memberships_and_common_start_sentinel_are_checked(self):
        for edit in (
            {"fixed": None}, {"available": True}, {"candidates": -1}, {"fixed": 35},
            {"available": 33}, {"available_only": 1}, {"fixed_only_with_older_stay": 1},
            # The count identity alone holds but sources begin on the same date here.
            {"available": 31, "fixed_only_with_older_stay": 1},
        ):
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                compare_history(self.design, (replace(self.months[0], **edit),) + self.months[1:])

    def test_independent_reconciliation_requires_link_to_original_scope(self):
        unknown = replace(self.design, original_arm=None, original_scope_attestation=None)
        unlinked = compare_history(unknown, self.months)
        self.assertEqual(unlinked.reconciled_years, ())
        self.assertEqual(unlinked.complete_years_without_annual_check, (2001, 2002))
        with self.assertRaisesRegex(ValueError, "linked"):
            compare_history(unknown, self.months, self.annual)
        with self.assertRaisesRegex(ValueError, "linked"):
            compare_history(unknown, (replace(self.months[0], original=32),) + self.months[1:])
        with self.assertRaisesRegex(ValueError, "attestation"):
            compare_history(replace(self.design, original_scope_attestation=""), self.months)
        with self.assertRaisesRegex(ValueError, "2002"):
            compare_history(self.design, self.months, {2001: 318, 2002: 241})

    def test_monthly_matching_is_stricter_than_annual_reconciliation(self):
        baseline = compare_history(self.design, self.months, self.annual)
        self.assertEqual(baseline.reconciled_months, ())
        swapped = (
            replace(self.months[0], original=31), replace(self.months[1], original=32),
            *self.months[2:],
        )
        with self.assertRaisesRegex(ValueError, "2001-01"):
            compare_history(self.design, swapped, self.annual)
        documented = (replace(self.months[0], original=32),) + self.months[1:]
        linked = compare_history(self.design, documented, self.annual)
        self.assertEqual(linked.reconciled_months, ("2001-01",))
        self.assertEqual(linked.reconciled_years, (2001, 2002))

    def test_partial_years_never_reconcile_against_whole_year_totals(self):
        truncated = replace(self.design, first_month="2001-02")
        result = compare_history(truncated, self.months[1:], {2001: 318, 2002: 240})
        self.assertEqual(result.reconciled_years, (2002,))
        missing = compare_history(self.design, self.months, {2002: 240})
        self.assertEqual(missing.complete_years_without_annual_check, (2001,))
        fixed_link = replace(self.design, original_arm="fixed", original_scope_attestation="synthetic-fixed")
        self.assertEqual(
            compare_history(fixed_link, self.months, {2001: 384, 2002: 384}).reconciled_years,
            (2001, 2002),
        )


if __name__ == "__main__":
    unittest.main()
