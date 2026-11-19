import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research_lab import challenge, release, weather_design
from research_lab.__main__ import ROOT, compare, proposal, save_new


class ReleaseContracts(unittest.TestCase):
    def test_adjustment_reorders_and_handles_ties(self):
        expected = [0.04, 0.02, 0.02, 0.04]
        actual = release.bh_adjust([0.03, 0.01, 0.01, 0.04])
        for ours, reference in zip(actual, expected):
            self.assertAlmostEqual(ours, reference)
        with self.assertRaises(ValueError):
            release.bh_adjust([float("nan")])

    def test_partial_or_duplicated_families_cannot_pass(self):
        path = ROOT / release.ESTIMATES
        verified = release.weather_models(path)
        self.assertEqual(len(verified), 48)
        self.assertEqual(sum(row["q_value"] is not None for row in verified), 12)
        with path.open() as source:
            rows = list(csv.DictReader(source))
        with TemporaryDirectory() as temp:
            candidate = Path(temp) / "estimates.csv"
            for changed in (rows[1:], [*rows, rows[0]]):
                with candidate.open("w", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(changed)
                with self.assertRaises(ValueError):
                    release.weather_models(candidate)

    def test_weather_challenge_works_without_any_outcome_file(self):
        card = ROOT / "research_lab/questions/later_weather_support.json"
        with TemporaryDirectory() as temp:
            sandbox = Path(temp)
            for source in weather_design.SOURCE_SHA256:
                target = sandbox / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / source).read_bytes())
            payload, verdict = proposal(sandbox, card)
            self.assertEqual(verdict["cells_evaluated"], 12)
            self.assertEqual(verdict["grid_rows_returned"], 72)
            self.assertFalse(verdict["all_selected_cells_meet_criterion"])
            self.assertEqual(set(json.loads(payload["manifest.json"])["inputs_sha256"]),
                             set(weather_design.SOURCE_SHA256))

    def test_question_contract_rejects_undeclared_dimensions(self):
        original = json.loads((ROOT / "research_lab/questions/later_weather_support.json").read_text())
        with TemporaryDirectory() as temp:
            path = Path(temp) / "card.json"
            for field, value in (("outcome", "chd"), ("metric", "p_value"), ("spline_df", [4, 4]),
                                 ("threshold", True), ("family", []), ("threshold", float("nan"))):
                path.write_text(json.dumps({**original, field: value}))
                with self.assertRaises(ValueError):
                    challenge.read_card(path)

    def test_outputs_are_idempotent_and_preserve_a_different_run(self):
        with TemporaryDirectory() as temp:
            dest = Path(temp) / "run"
            save_new(dest, {"test.csv": b"x\n1\n"})
            save_new(dest, {"test.csv": b"x\n1\n"})
            with self.assertRaises(ValueError):
                save_new(dest, {"test.csv": b"x\n2\n"})
            compare(dest, {"test.csv": b"x\n1\n"})


if __name__ == "__main__":
    unittest.main()
