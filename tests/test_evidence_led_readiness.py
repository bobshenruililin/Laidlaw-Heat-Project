"""Readiness-contract checks; R numerical tests remain explicitly skipped without R.

No HA data are opened. The contract is a proposal, not a delivery or approval receipt.
"""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadinessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(
            (ROOT / "analysis_plan/covid_period/readiness_contract.json").read_text()
        )

    def test_proposed_fields_cannot_be_treated_as_delivered_or_approved(self):
        self.assertEqual(self.contract["status"], "PROPOSED_NOT_DELIVERED_NOT_FROZEN")
        current = self.contract["current_transfer"]
        self.assertEqual(current["admission_cause"], "ABSENT")
        self.assertEqual(current["risk_person_time"], "NOT_DELIVERED")
        self.assertEqual(current["labs"], "NOT_DELIVERED")
        self.assertEqual(self.contract["freeze"]["status"], "NOT_FROZEN")
        self.assertEqual(
            self.contract["execution_receipt"]["status"],
            "TEMPLATE_ONLY_DO_NOT_TREAT_AS_APPROVAL",
        )
        self.assertEqual(
            self.contract["output_contract"]["release_status"],
            "AWAITING_DISCLOSURE_REVIEW",
        )

    def test_complete_panel_interface_matches_scientific_target(self):
        analysis = self.contract["analysis"]
        members = {
            (outcome, exposure["name"])
            for outcome in analysis["outcomes"]
            for exposure in analysis["exposures"]
        }
        self.assertEqual(len(members), analysis["interaction_family_size"])
        self.assertEqual(len(members), 12)
        self.assertEqual(analysis["splits"], ["2020-01", "2020-02"])
        self.assertEqual(analysis["trend_df"], [4, 6, 8])
        self.assertEqual(
            analysis["claim_class"], "EXPLORATORY_ASSOCIATION_NOT_CAUSAL_COVID_EFFECT"
        )
        self.assertIn("not cohort person-time", self.contract["monthly_runner_input"]["offset"])
        required = self.contract["monthly_runner_input"]["required_columns"]
        self.assertEqual(len(required), len(set(required)))
        self.assertTrue({"n_events", "data_status", "days_in_month"}.issubset(required))

    @unittest.skipUnless(shutil.which("Rscript"), "Rscript unavailable: numeric runner execution NOT VERIFIED")
    def test_synthetic_r_covariance_input_rejection_and_family(self):
        process = subprocess.run(
            [shutil.which("Rscript"), "tests/test_covid_common_basis_interactions.R"],
            cwd=ROOT, capture_output=True, text=True, timeout=180,
        )
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn("SYNTHETIC", process.stdout)
        self.assertIn("coverage calibration not certified", process.stdout)


if __name__ == "__main__":
    unittest.main()
