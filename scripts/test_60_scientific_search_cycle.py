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
        self.assertEqual(m["width"], 3)
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

    def test_killed_nodes_cannot_vanish(self):
        prev = {"metrics": {"killed": ["F01-k"], "closed_lemma": ["L"]}}
        ok = MOD.compounding_invariants(
            prev, {"killed": ["F01-k"], "closed_lemma": ["L"]}
        )
        self.assertEqual(ok, [])
        bad = MOD.compounding_invariants(
            prev, {"killed": [], "closed_lemma": ["L"]}
        )
        self.assertTrue(any("vanished" in f for f in bad))

    def test_human_gate_cannot_close_without_owner_event(self):
        prev = {"metrics": {"killed": ["F01-k"], "closed_lemma": [], "blocked_human": ["F04"]}}
        bad = MOD.compounding_invariants(
            prev,
            {"killed": ["F01-k"], "closed_lemma": [], "blocked_human": []},
            {"F04": {"status": "alive", "search_class": "agent_owned"}},
        )
        self.assertTrue(any("owner_event" in f for f in bad))

    def test_require_search_class_rejects_missing_label(self):
        tree = mini_tree()
        tree["rails"]["require_search_class"] = True
        fails = MOD.validate_tree(tree)
        self.assertTrue(any("search_class" in f for f in fails))

    def test_harness_debt_rewalk_is_debt(self):
        tree = mini_tree()
        tree["frontier"][0]["job"] = "retune F1.2 until q < 0.05"
        memory = mini_memory()
        memory["dead_ends"][0]["rewalk_markers"] = ["retune f1.2", "until q < 0.05"]
        debt = MOD.harness_debt(tree, memory)
        self.assertTrue(any("rewalks" in d for d in debt))

    def test_q_bar_and_open_human_gate_are_not_debt(self):
        tree = MOD.load_yaml(MOD.DEFAULT_TREE)
        memory = MOD.load_yaml(MOD.DEFAULT_MEMORY)
        debt = MOD.harness_debt(tree, memory)
        self.assertEqual(debt, [])
        blob = " ".join(debt).lower()
        self.assertNotIn("q > 0.19", blob)
        self.assertNotIn("q_above", blob)
        m = MOD.compute_metrics(tree, memory)
        self.assertTrue(m.get("q_above_0.19_is_not_harness_failure"))
        self.assertTrue(m.get("human_gates_remaining_open_is_not_harness_failure"))
        self.assertIn("F04", m["blocked_human"])
        self.assertGreaterEqual(m["n_refusal_solution"], 1)

    def test_refusal_kept_alive_is_debt(self):
        tree = mini_tree()
        tree["nodes"][1]["search_class"] = "refusal_solution"
        tree["nodes"][1]["status"] = "alive"
        debt = MOD.harness_debt(tree, mini_memory())
        self.assertTrue(any("refusal_solution kept alive" in d for d in debt))

    def test_human_gate_labelled_agent_owned_is_debt(self):
        tree = mini_tree()
        tree["nodes"][5]["search_class"] = "agent_owned"
        debt = MOD.harness_debt(tree, mini_memory())
        self.assertTrue(any("human gate treated as agent-owned" in d for d in debt))

    def test_skipped_auditor_is_not_green(self):
        tree = mini_tree()
        memory = mini_memory()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            tpath = td / "tree.yml"
            mpath = td / "mem.yml"
            live = td / "live.md"
            dump_yaml(tpath, tree)
            dump_yaml(mpath, memory)
            live.write_text(
                "Meteorological data was obtained from the HKO.\n", encoding="utf-8"
            )
            payload = MOD.run_cycle(
                tree_path=tpath,
                memory_path=mpath,
                live_path=live,
                skip_auditor=True,
                when="2099-01-02",
                root=td,
                write=False,
            )
            self.assertFalse(payload["ok"])
            self.assertTrue(any("auditor skipped" in f for f in payload["failures"]))

    def test_pinned_human_gate_cannot_close(self):
        tree = MOD.load_yaml(MOD.DEFAULT_TREE)
        for node in tree["nodes"]:
            if node["id"] == "F04":
                node["status"] = "closed_lemma"
                node.pop("owner", None)
        fails = MOD.validate_tree(tree)
        self.assertTrue(any("F04" in f and "pinned" in f for f in fails))

    def test_scientific_width_excludes_public_surfaces(self):
        tree = MOD.load_yaml(MOD.DEFAULT_TREE)
        memory = MOD.load_yaml(MOD.DEFAULT_MEMORY)
        m = MOD.compute_metrics(tree, memory)
        self.assertEqual(m["scientific_alive_families"], ["F01", "F02", "F03"])
        self.assertEqual(m["width"], 3)
        self.assertIn("F06", m["alive_families"])


if __name__ == "__main__":
    unittest.main()
