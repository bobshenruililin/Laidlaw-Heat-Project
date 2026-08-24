#!/usr/bin/env python3
"""One scientific-search cycle for the heat–CHD/HF extract.

Loads the persistent tree and memory, validates rails, runs the claim-ledger
auditor as a hard gate, writes width/depth/residue metrics, and proposes
frontier jobs. Does not mint a confirmatory primary.

Usage:
  python3 scripts/60_scientific_search_cycle.py
  python3 scripts/60_scientific_search_cycle.py --skip-auditor
  python3 scripts/60_scientific_search_cycle.py --date 2026-08-24
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TREE = ROOT / "analysis_plan/scientific_search/search_tree.yml"
DEFAULT_MEMORY = ROOT / "analysis_plan/scientific_search/memory.yml"
DEFAULT_LIVE = ROOT / "manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md"
AUDITOR = ROOT / "scripts/50_audit_live_claim_ledger.py"
CYCLE_DIR = ROOT / "analysis_plan/scientific_search/cycles"
JSON_OUT = ROOT / "outputs/scientific_search/cycle_latest.json"

ALLOWED_STATUS = {'blocked_human', 'killed', 'queued', 'alive', 'closed_lemma'}
ALLOWED_METRICS = {'residue_for_next_cycle', 'family_diversity', 'named_gap_closed_without_invention', 'rails_intact', 'identification_defensibility', 'cycle_shortening'}
FORBIDDEN_METRIC_TOKENS = (
    "found_significant_heat_effect",
    "confirmatory_primary",
    "minted_stroke_coefficient",
    "minted_daily_dlnm_coefficient",
    "minted_ami_principal_dx",
    "minted_heatwave_excess_death",
    "minted_monetisation",
    "gate_3_frozen_by_agent",
    "hogan_weather_rewritten",
    "filled_human_gate",
    "smaller_p_or_q",
    "found_heat_effect",
)
HUMAN_OWNERS = {"Hogan", "Roro", "Bishai", "Bob", "Bob"}


def load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyYAML is required. pip install pyyaml") from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} did not parse as a mapping")
    return data


def node_map(tree: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for node in tree.get("nodes") or []:
        nid = node.get("id")
        if not nid or nid in out:
            raise ValueError(f"duplicate or missing node id: {nid!r}")
        out[str(nid)] = node
    return out


def validate_tree(tree: dict, *, root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    nodes = tree.get("nodes") or []
    if not nodes:
        return ["tree has no nodes"]
    try:
        by_id = node_map(tree)
    except ValueError as exc:
        return [str(exc)]

    if "ROOT" not in by_id:
        failures.append("missing ROOT node")

    forbidden = set(tree.get("forbidden_success_metrics") or []) | set(
        FORBIDDEN_METRIC_TOKENS
    )
    for nid, node in by_id.items():
        status = node.get("status")
        metric = str(node.get("success_metric") or "")
        if status not in ALLOWED_STATUS:
            failures.append(f"{nid}: bad status {status!r}")
        if metric not in ALLOWED_METRICS:
            failures.append(f"{nid}: illegal success_metric {metric!r}")
        if metric in forbidden or any(tok in metric for tok in forbidden):
            failures.append(f"{nid}: forbidden success_metric {metric!r}")
        parent = node.get("parent")
        if nid == "ROOT":
            if parent not in (None, "", "null"):
                failures.append("ROOT parent must be null")
        elif parent not in by_id:
            failures.append(f"{nid}: missing parent {parent!r}")
        if status == "killed":
            if not str(node.get("kill_reason") or "").strip():
                failures.append(f"{nid}: killed node missing kill_reason")
            if node.get("kill_with") not in {
                "table_contradiction",
                "forbidden_claim_hit",
                None,
            }:
                failures.append(
                    f"{nid}: kill_with must be table_contradiction or forbidden_claim_hit"
                )
        if status == "blocked_human":
            if node.get("owner") not in HUMAN_OWNERS:
                failures.append(
                    f"{nid}: blocked_human missing owner Hogan/Roro/Bishai/Bob"
                )
            if not str(node.get("blocked_reason") or "").strip():
                failures.append(f"{nid}: blocked_human missing blocked_reason")
        for ev in node.get("evidence") or []:
            if ev and not (root / ev).exists():
                failures.append(f"{nid}: missing evidence {ev}")

    for item in tree.get("frontier") or []:
        fid = item.get("id", "?")
        metric = str(item.get("success_metric") or "")
        if metric not in ALLOWED_METRICS:
            failures.append(f"frontier {fid}: illegal success_metric {metric!r}")
        if metric in forbidden:
            failures.append(f"frontier {fid}: forbidden success_metric {metric!r}")
        st = item.get("status")
        if st == "blocked_human" and item.get("owner") not in HUMAN_OWNERS:
            failures.append(f"frontier {fid}: blocked_human missing owner")
        if st not in ALLOWED_STATUS:
            failures.append(f"frontier {fid}: bad status {st!r}")
    return failures


def validate_memory(memory: dict, *, root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for lemma in memory.get("lemmas") or []:
        lid = lemma.get("id", "?")
        ev = lemma.get("evidence")
        if ev and not (root / ev).exists():
            failures.append(f"{lid}: missing evidence {ev}")
        if not str(lemma.get("text") or "").strip():
            failures.append(f"{lid}: empty lemma")
    if not (memory.get("dead_ends") or memory.get("dead_ends") or []):
        failures.append("memory has no dead_ends; compounding requires killed paths")
    if not (memory.get("human_gates") or memory.get("human_gates") or []):
        failures.append("memory has no human_gates")
    return failures


def depth_killed_or_closed(by_id: dict[str, dict]) -> int:
    """Longest edge-distance from ROOT to a killed or closed node."""
    def is_constraint(status: str) -> bool:
        st = str(status or "")
        return st == "killed" or st.startswith("closed")

    def walk(nid: str, seen: frozenset[str], dist: int) -> int:
        if nid in seen or nid not in by_id:
            return 0
        node = by_id[nid]
        here = dist if is_constraint(node.get("status")) else 0
        kids = [k for k, v in by_id.items() if v.get("parent") == nid]
        if not kids:
            return here
        return max([here] + [walk(k, seen | {nid}, dist + 1) for k in kids])

    return walk("ROOT", frozenset(), 0) if "ROOT" in by_id else 0


def compute_metrics(tree: dict, memory: dict) -> dict:
    by_id = node_map(tree)
    alive_families = sorted(
        {
            n["family"]
            for n in by_id.values()
            if n.get("status") == "alive" and n.get("family") not in {None, "ROOT"}
        }
    )
    queued_frontier = [
        f for f in (tree.get("frontier") or []) if f.get("status") == "queued"
    ]
    blocked_human = [
        n["id"] for n in by_id.values() if n.get("status") == "blocked_human"
    ]
    killed = [n["id"] for n in by_id.values() if n.get("status") == "killed"]
    closed = [n["id"] for n in by_id.values() if str(n.get("status") or "").startswith("closed")]
    lemmas = [
        L["id"]
        for L in (memory.get("lemmas") or [])
        if L.get("next_paper") == "inherit"
    ]
    width = len(alive_families) + len(queued_frontier)
    depth = depth_killed_or_closed(by_id)
    n_constraints = len(killed) + len(closed) + len(lemmas)
    return {
        "alive_families": alive_families,
        "n_alive_families": len(alive_families), "n_alive_families": len(alive_families),
        "n_queued_frontier": len(queued_frontier), "n_queued_frontier": len(queued_frontier),
        "queued_frontier_ids": [f.get("id") for f in queued_frontier],
        "blocked_human": blocked_human,
        "killed": killed,
        "closed_lemma": closed,
        "width": width,
        "depth": depth,
        "n_inheritable_lemmas": len(lemmas),
        "n_inheritable_constraints": n_constraints,
        "search_power_proxy": width * depth * n_constraints,
        "notes": "proxy is width × depth × inheritable constraints; never a p-value",
    }


def rails_checks(tree: dict, live_text: str) -> list[str]:
    failures: list[str] = []
    rails = tree.get("rails") or {}
    if rails.get("gate_3") != "open":
        failures.append("rails.gate_3 must be open")
    contrib = rails.get("contribution_type")
    expected_contrib = 'aggregation_identifiability_calibrated_refusal'
    if contrib != expected_contrib:
        failures.append(f"rails.contribution_type drifted: {contrib!r}")
    weather = None
    for k, v in rails.items():
        if "weather" in k or "hogan" in k:
            if isinstance(v, str) and "Meteorological" in v:
                weather = v
    if weather and weather not in live_text:
        failures.append(f"Hogan weather start string missing from live file: {weather!r}")
    stage = rails.get("stage3_pdfs")
    expected_stage = 'byte_locked_on_main'
    if stage != expected_stage:
        failures.append(f"rails.stage3_pdfs drifted: {stage!r}")
    return failures


def run_auditor() -> dict:
    if not AUDITOR.exists():
        return {"ok": False, "stdout": "", "stderr": f"missing auditor {AUDITOR}"}
    proc = subprocess.run(
        [sys.executable, str(AUDITOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-1000:],
    }


def proposals(tree: dict) -> list[dict]:
    return [
        {
            "id": item.get("id"),
            "family": item.get("family"),
            "status": item.get("status"),
            "owner": item.get("owner"),
            "job": item.get("job"),
        }
        for item in (tree.get("frontier") or [])
    ]


def write_cycle(payload: dict, when: str) -> tuple[Path, Path]:
    CYCLE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    md = CYCLE_DIR / f"{when}.md"
    JSON_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    m = payload["metrics"]
    lines = [
        f"# Scientific-search cycle {when}",
        "",
        "Playbook 06. Not a Gate 3 freeze. Not a confirmatory primary. Not a heat finding.",
        "",
        f"- Auditor: {'PASSED' if payload['auditor']['ok'] else 'FAILED'}",
        f"- Tree/memory/rails: {'PASSED' if payload['ok'] else 'FAILED'}",
        f"- Width: {m['width']} (alive families {m['n_alive_families']} + queued frontier {m['n_queued_frontier']})",
        f"- Depth (killed/closed path): {m['depth']}",
        f"- Inheritable constraints: {m['n_inheritable_constraints']}",
        f"- Search-power proxy (not a p-value): {m['search_power_proxy']}",
        f"- Alive families: {', '.join(m['alive_families'])}",
        f"- Blocked human: {', '.join(m['blocked_human'])}",
        f"- Killed: {', '.join(m['killed'])}",
        "",
        "## Frontier (do not fill human jobs)",
        "",
    ]
    for item in payload["proposals"]:
        owner = f" owner={item.get('owner')}" if item.get("owner") else ""
        lines.append(
            f"- `{item['id']}` [{item['status']}/{item['family']}]{owner}: {item['job']}"
        )
    lines.extend(["", "## Failures", ""])
    fails = payload.get("failures") or []
    if not fails:
        lines.append("None.")
    else:
        for fail in fails:
            lines.append(f"- {fail}")
    lines.extend(
        [
            "",
            "## Compounding",
            "",
            "Next paper loads `CONSTITUTION.md`, `memory.yml`, and `search_tree.yml` before any new coefficient search.",
            "Killed nodes stay killed. Human gates stay human.",
            "",
        ]
    )
    md.write_text("\n".join(lines), encoding="utf-8")
    log = ROOT / "analysis_plan/scientific_search/CYCLE_LOG.md"
    row = (
        f"| {when} | width={m['width']} depth={m['depth']} "
        f"proxy={m['search_power_proxy']} auditor={'PASS' if payload['auditor']['ok'] else 'FAIL'} "
        f"ok={payload['ok']} |\n"
    )
    if log.exists():
        text = log.read_text(encoding="utf-8")
        if when not in text:
            log.write_text(text.rstrip() + "\n" + row, encoding="utf-8")
    else:
        log.write_text(
            "# Scientific-search cycle log\n\n| Date | Metrics |\n|---|---|\n" + row,
            encoding="utf-8",
        )
    return md, JSON_OUT


def run_cycle(
    *,
    tree_path: Path = DEFAULT_TREE,
    memory_path: Path = DEFAULT_MEMORY,
    live_path: Path = DEFAULT_LIVE,
    skip_auditor: bool = False,
    when: str | None = None,
    root: Path = ROOT,
    write: bool = True,
) -> dict:
    when = when or date.today().isoformat()
    tree = load_yaml(tree_path)
    memory = load_yaml(memory_path)
    live_text = live_path.read_text(encoding="utf-8") if live_path.exists() else ""
    failures: list[str] = []
    failures.extend(validate_tree(tree, root=root))
    failures.extend(validate_memory(memory, root=root))
    failures.extend(rails_checks(tree, live_text))
    m = compute_metrics(tree, memory)
    if m["n_alive_families"] < 3:
        failures.append(
            f"width collapse: only {m['n_alive_families']} alive families; keep incompatible families"
        )
    if skip_auditor:
        auditor = {"ok": True, "skipped": True, "stdout": "", "stderr": ""}
    else:
        auditor = run_auditor()
        if not auditor["ok"]:
            failures.append(
                "claim-ledger auditor red; stop, do not invent a matching number"
            )
    payload = {
        "date": when,
        "ok": not failures,
        "failures": failures,
        "metrics": m,
        "auditor": {
            "ok": auditor["ok"],
            "skipped": bool(auditor.get("skipped")),
            "stdout_tail": auditor.get("stdout", ""),
            "stderr_tail": auditor.get("stderr", ""),
        },
        "proposals": proposals(tree),
        "rails": tree.get("rails"),
        "objective": "identification_defensibility",
        "not_objective": "found_significant_heat_effect",
    }
    if write:
        write_cycle(payload, when)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run one compounding scientific-search cycle")
    p.add_argument("--skip-auditor", action="store_true")
    p.add_argument("--date", default=None)
    p.add_argument("--tree", type=Path, default=DEFAULT_TREE)
    p.add_argument("--memory", type=Path, default=DEFAULT_MEMORY)
    p.add_argument("--live", type=Path, default=DEFAULT_LIVE)
    p.add_argument("--no-write", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_cycle(
        tree_path=args.tree if args.tree.is_absolute() else ROOT / args.tree,
        memory_path=args.memory if args.memory.is_absolute() else ROOT / args.memory,
        live_path=args.live if args.live.is_absolute() else ROOT / args.live,
        skip_auditor=args.skip_auditor,
        when=args.date,
        write=not args.no_write,
    )
    print("SCIENTIFIC SEARCH CYCLE", "PASSED" if payload["ok"] else "FAILED")
    m = payload["metrics"]
    print(
        f"width={m['width']} depth={m['depth']} "
        f"constraints={m['n_inheritable_constraints']} "
        f"proxy={m['search_power_proxy']}"
    )
    print("alive_families:", ", ".join(m["alive_families"]))
    if payload["failures"]:
        for fail in payload["failures"]:
            print(" -", fail)
        return 1
    print(f"wrote {JSON_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
