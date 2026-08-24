#!/usr/bin/env python3
"""Tests for the compounding scientific-search harness."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_mod():
    path = ROOT / "scripts/60_scientific_search_cycle.py"
    spec = importlib.util.spec_from_file_location("search_cycle", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


MOD = load_mod()


def dump_yaml(path: Path, data: dict) -> None:
    import yaml

    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def mini_tree(**overrides) -> dict:
    base = {
        "rails": {
            "gate_3": "open",
            "contribution_type": "aggregation_identifiability_calibrated_refusal",
            "hogan_weather_must_contain": "Meteorological data was obtained from the HKO.",
            "stage3_pdfs": "byte_locked_on_main",
        },
        "forbidden_success_metrics": ["found_significant_heat_effect"],
        "nodes": [
            {
                "id": "ROOT",
                "parent": None,
                "family": "ROOT",
                "title": "root",
                "status": "alive",
                "success_metric": "identification_defensibility",
                "evidence": [],
            },
            {
                "id": "F01",
                "parent": "ROOT",
                "family": "F01",
                "title": "id",
                "status": "alive",
                "success_metric": "identification_defensibility",
                "evidence": [],
            },
            {
                "id": "F01-k",
                "parent": "F01",
                "family": "F01",
                "title": "killed daily",
                "status": "killed",
                "success_metric": "named_gap_closed_without_invention",
                "kill_reason": "calibration failed",
                "kill_with": "table_contradiction",
                "evidence": [],
            },
            {
                "id": "F02",
                "parent": "ROOT",
                "family": "F02",
                "title": "mult",
                "status": "alive",
                "success_metric": "identification_defensibility",
                "evidence": [],
            },
            {
                "id": "F03",
                "parent": "ROOT",
                "family": "F03",
                "title": "hist",
                "status": "alive",
                "success_metric": "identification_defensibility",
                "evidence": [],
            },
            {
                "id": "F04",
                "parent": "ROOT",
                "family": "F04",
                "title": "weather",
                "status": "blocked_human",
                "owner": "Hogan",
                "blocked_reason": "no lock",
                "success_metric": "rails_intact",
                "evidence": [],
            },
        ],
        "frontier": [
            {
                "id": "P1",
                "family": "F01",
                "status": "queued",
                "job": "keep families",
                "success_metric": "family_diversity",
            }
        ],
    }
    base.update(overrides)
    return base


def mini_memory() -> dict:
    return {
        "lemmas": [
            {
                "id": "L01",
                "text": "all q > 0.19",
                "evidence": None,
                "next_paper": "inherit",
            }
        ],
        "dead_ends": [{"id": "D01", "text": "retune F1.2", "why": "illegal"}],
        "human_gates": [{"id": "H1", "owner": "Hogan", "hole": "weather"}],
    }


class SearchCycleTests(unittest.TestCase):
    def test_real_tree_validates(self):
        tree = MOD.load_yaml(MOD.DEFAULT_TREE)
        memory = MOD.load_yaml(MOD.DEFAULT_MEMORY)
        fails = MOD.validate_tree(tree) + MOD.validate_memory(memory)
        self.assertEqual(fails, [])

    def test_killed_without_reason_fails(self):
        tree = mini_tree()
        tree["nodes"][2]["kill_reason"] = ""
        fails = MOD.validate_tree(tree)
        self.assertTrue(any("kill_reason" in f for f in fails))

    def test_forbidden_success_metric_fails(self):
        tree = mini_tree()
        tree["nodes"][1]["success_metric"] = "found_significant_heat_effect"
        fails = MOD.validate_tree(tree)
        self.assertTrue(any("forbidden" in f or "illegal" in f for f in fails))

    def test_blocked_human_without_owner_fails(self):
        tree = mini_tree()
        tree["nodes"][5]["owner"] = None
        fails = MOD.validate_tree(tree)
        self.assertTrue(any("owner" in f for f in fails))

    def test_width_and_depth(self):
        m = MOD.compute_metrics(mini_tree(), mini_memory())
        self.assertGreaterEqual(m["n_alive_families"], 3)
        self.assertEqual(m["depth"], 2)
        self.assertNotIn("p", m["notes"].lower()[:1] and "")
        self.assertIn("never a p-value", m["notes"])

    def test_cycle_rejects_heat_hunt_metric_on_disk(self):
        tree = mini_tree()
        tree["frontier"][0]["success_metric"] = "found_significant_heat_effect"
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            tpath = td / "tree.yml"
            mpath = td / "mem.yml"
            live = td / "live.md"
            dump_yaml(tpath, tree)
            dump_yaml(mpath, mini_memory())
            live.write_text(
                "Meteorological data was obtained from the HKO.\n", encoding="utf-8"
            )
            payload = MOD.run_cycle(
                tree_path=tpath,
                memory_path=mpath,
                live_path=live,
                skip_auditor=True,
                when="2099-01-01",
                root=td,
                write=False,
            )
            self.assertFalse(payload["ok"])


if __name__ == "__main__":
    unittest.main()
