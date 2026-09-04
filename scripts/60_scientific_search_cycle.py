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
import re
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
    "harness_failed_because_q_above_0.19",
)
HUMAN_OWNERS = {"Hogan", "Roro", "Bishai", "Bob"}
ALLOWED_SEARCH_CLASS = {"agent_owned", "human_owned", "refusal_solution"}
REQUIRED_WEATHER = "Meteorological data was obtained from the HKO."
SCIENTIFIC_FAMILIES = {"F01", "F02", "F03"}
PINNED_HUMAN_GATES = {
    "F04": "Hogan",
    "F05": "Roro",
    "F07": "Bishai",
}
HEAT_HUNT_MARKERS = (
    "until significant",
    "until q < 0.05",
    "search harder until",
    "harness failed because q",
)
KILLED_REGISTRY = ROOT / "analysis_plan/scientific_search/killed_registry.yml"


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
        elif by_id[parent].get("status") == "killed":
            failures.append(f"{nid}: child of killed node {parent} — do not extend a dead path")
        if status == "killed":
            if not str(node.get("kill_reason") or "").strip():
                failures.append(f"{nid}: killed node missing kill_reason")
            if node.get("kill_with") not in {
                "table_contradiction",
                "forbidden_claim_hit",
            }:
                failures.append(
                    f"{nid}: kill_with must be table_contradiction or forbidden_claim_hit"
                )
            if not (node.get("evidence") or []):
                failures.append(f"{nid}: killed node missing evidence")
        if status == "blocked_human":
            if node.get("owner") not in HUMAN_OWNERS:
                failures.append(
                    f"{nid}: blocked_human missing owner Hogan/Roro/Bishai/Bob"
                )
            if not str(node.get("blocked_reason") or "").strip():
                failures.append(f"{nid}: blocked_human missing blocked_reason")
        sc = node.get("search_class")
        require_class = bool((tree.get("rails") or {}).get("require_search_class"))
        if require_class and sc not in ALLOWED_SEARCH_CLASS:
            failures.append(f"{nid}: missing or illegal search_class {sc!r}")
        if sc and sc not in ALLOWED_SEARCH_CLASS:
            failures.append(f"{nid}: illegal search_class {sc!r}")
        if status == "blocked_human" and sc and sc != "human_owned":
            failures.append(f"{nid}: blocked_human must be search_class human_owned")
        if status == "alive" and sc == "refusal_solution":
            failures.append(
                f"{nid}: refusal_solution still alive; that is a hunt, not a closed refusal"
            )
        if sc == "human_owned" and status != "blocked_human":
            failures.append(
                f"{nid}: human_owned node must stay blocked_human (agents do not fill human gates)"
            )
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
        fsc = item.get("search_class")
        require_class = bool((tree.get("rails") or {}).get("require_search_class"))
        if require_class and fsc not in ALLOWED_SEARCH_CLASS:
            failures.append(f"frontier {fid}: missing or illegal search_class {fsc!r}")
        if fsc and fsc not in ALLOWED_SEARCH_CLASS:
            failures.append(f"frontier {fid}: illegal search_class {fsc!r}")
        if st == "blocked_human" and fsc and fsc != "human_owned":
            failures.append(f"frontier {fid}: blocked_human must be search_class human_owned")
        if fsc == "human_owned" and st != "blocked_human":
            failures.append(
                f"frontier {fid}: human_owned frontier must stay blocked_human"
            )
    fids = [item.get("id") for item in (tree.get("frontier") or [])]
    if len(fids) != len(set(fids)):
        failures.append("duplicate frontier ids")
    for item in tree.get("frontier") or []:
        job = str(item.get("job") or "").lower()
        fid = item.get("id", "?")
        for mk in HEAT_HUNT_MARKERS:
            if mk in job:
                failures.append(f"frontier {fid}: heat-hunt job {mk!r}")
    seen_kills: dict[tuple[str, tuple[str, ...]], str] = {}
    for nid, node in by_id.items():
        if node.get("status") != "killed":
            continue
        key = (
            str(node.get("kill_reason") or "").strip().lower(),
            tuple(node.get("evidence") or []),
        )
        if key[0] and key in seen_kills:
            failures.append(
                f"{nid}: restates kill {seen_kills[key]} (do not mint depth)"
            )
        elif key[0]:
            seen_kills[key] = str(nid)
    for nid, owner in PINNED_HUMAN_GATES.items():
        if nid not in by_id:
            if "F01-daily-recovery" in by_id:
                failures.append(f"missing pinned human gate {nid} ({owner})")
            continue
        node = by_id[nid]
        if node.get("status") != "blocked_human" or node.get("owner") != owner:
            if not str(node.get("owner_event") or "").strip():
                failures.append(
                    f"{nid}: pinned human gate must stay blocked_human owner={owner}"
                )
    if KILLED_REGISTRY.exists():
        try:
            import yaml  # type: ignore

            reg = yaml.safe_load(KILLED_REGISTRY.read_text(encoding="utf-8")) or {}
        except Exception:
            reg = {}
        for nid in reg.get("killed") or []:
            node = by_id.get(nid)
            if not node or node.get("status") != "killed":
                failures.append(f"killed registry: {nid} missing or not killed")
        for nid in reg.get("closed_lemma") or []:
            node = by_id.get(nid)
            if not node or not str(node.get("status") or "").startswith("closed"):
                failures.append(f"killed registry: {nid} missing or not closed")
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
    lids = [L.get("id") for L in (memory.get("lemmas") or [])]
    if len(lids) != len(set(lids)):
        failures.append("duplicate lemma ids")
    dids = [d.get("id") for d in (memory.get("dead_ends") or [])]
    if len(dids) != len(set(dids)):
        failures.append("duplicate dead_end ids")
    if not (memory.get("dead_ends") or []):
        failures.append("memory has no dead_ends; compounding requires killed paths")
    if not (memory.get("human_gates") or []):
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
    scientific_alive = [f for f in alive_families if f in SCIENTIFIC_FAMILIES]
    width = len(scientific_alive)
    depth = depth_killed_or_closed(by_id)
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
    n_constraints = len(killed) + len(closed) + len(lemmas)
    class_counts = {"agent_owned": 0, "human_owned": 0, "refusal_solution": 0}
    for n in by_id.values():
        sc = n.get("search_class")
        if sc in class_counts:
            class_counts[sc] += 1
    return {
        "alive_families": alive_families,
        "scientific_alive_families": scientific_alive,
        "n_alive_families": len(alive_families),
        "n_scientific_alive_families": len(scientific_alive),
        "n_queued_frontier": len(queued_frontier),
        "queued_frontier_ids": [f.get("id") for f in queued_frontier],
        "blocked_human": blocked_human,
        "killed": killed,
        "closed_lemma": closed,
        "width": width,
        "depth": depth,
        "n_inheritable_lemmas": len(lemmas),
        "n_inheritable_constraints": n_constraints,
        "n_agent_owned": class_counts["agent_owned"],
        "n_human_owned": class_counts["human_owned"],
        "n_refusal_solution": class_counts["refusal_solution"],
        "search_power_proxy": width * depth * n_constraints,
        "notes": (
            "proxy is unique-family width × depth × inheritable constraints; "
            "never a p-value and never a target to maximise"
        ),
        "q_above_0.19_is_not_harness_failure": True,
        "human_gates_remaining_open_is_not_harness_failure": True,
    }


def harness_debt(tree: dict, memory: dict) -> list[str]:
    """Agent-owned inefficiency. Human gates and refusal-solutions are not debt."""
    debt: list[str] = []
    by_id = node_map(tree)
    markers: list[tuple[str, str]] = []
    for dead in memory.get("dead_ends") or []:
        did = str(dead.get("id") or "?")
        for mk in dead.get("rewalk_markers") or []:
            markers.append((did, str(mk).lower()))
    for nid, node in by_id.items():
        if node.get("status") == "alive" and node.get("search_class") == "refusal_solution":
            debt.append(f"{nid}: refusal_solution kept alive (significance hunt)")
        if node.get("status") == "blocked_human" and node.get("search_class") == "agent_owned":
            debt.append(f"{nid}: human gate treated as agent-owned search")
        blob = " ".join(
            str(node.get(k) or "") for k in ("title", "note", "job", "kill_reason")
        ).lower()
        if node.get("status") in {"alive", "queued"}:
            for did, mk in markers:
                if mk and mk in blob:
                    debt.append(f"{nid} rewalks {did} via {mk!r}")
    for item in tree.get("frontier") or []:
        if item.get("status") != "queued":
            continue
        job = str(item.get("job") or "").lower()
        fid = item.get("id", "?")
        for did, mk in markers:
            if mk and mk in job:
                debt.append(f"frontier {fid} rewalks {did} via {mk!r}")
        if item.get("search_class") == "refusal_solution":
            debt.append(
                f"frontier {fid}: queues a refusal_solution (searching past a found constraint)"
            )
    return debt


def rails_checks(tree: dict, live_text: str) -> list[str]:
    failures: list[str] = []
    rails = tree.get("rails") or {}
    if rails.get("hogan_weather_must_contain") != REQUIRED_WEATHER:
        failures.append(
            f"rails.hogan_weather_must_contain must equal {REQUIRED_WEATHER!r}"
        )
    if REQUIRED_WEATHER not in live_text:
        failures.append(f"Hogan weather start string missing from live file: {REQUIRED_WEATHER!r}")
    g3 = rails.get("gate_3")
    if g3 == "open":
        pass
    elif (
        isinstance(g3, dict)
        and g3.get("state") == "frozen"
        and g3.get("by") == "team"
        and g3.get("artifact")
        and (ROOT / str(g3.get("artifact"))).exists()
    ):
        pass
    else:
        failures.append(
            "rails.gate_3 must be open, or frozen by team with an existing artifact "
            "(agents do not freeze Gate 3)"
        )
    contrib = rails.get("contribution_type")
    expected_contrib = 'aggregation_identifiability_calibrated_refusal'
    if contrib != expected_contrib:
        failures.append(f"rails.contribution_type drifted: {contrib!r}")
    weather = None
    for k, v in rails.items():
        if "weather" in k or "hogan" in k:
            if isinstance(v, str) and "Meteorological" in v:
                weather = v
    if weather and weather != REQUIRED_WEATHER:
        failures.append(f"Hogan weather rail drifted: {weather!r}")
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
    if payload.get("ok"):
        JSON_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    m = payload["metrics"]
    lines = [
        f"# Scientific-search cycle {when}",
        "",
        "Playbook 06. Not a Gate 3 freeze. Not a confirmatory primary. Not a heat finding.",
        "",
        f"- Auditor: {'SKIPPED' if payload['auditor'].get('skipped') else ('PASSED' if payload['auditor']['ok'] else 'FAILED')}",
        f"- Tree/memory/rails: {'PASSED' if payload['ok'] else 'FAILED'}",
        f"- Width (unique families): {m['width']} (alive {m['n_alive_families']}; queued jobs {m['n_queued_frontier']} not added to width)",
        f"- Depth (killed/closed path): {m['depth']}",
        f"- Inheritable constraints: {m['n_inheritable_constraints']}",
        f"- Search-power proxy (not a p-value): {m['search_power_proxy']}",
        f"- Alive families: {', '.join(m['alive_families'])}",
        f"- Blocked human: {', '.join(m['blocked_human'])}",
        f"- Killed: {', '.join(m['killed'])}",
        f"- Search class: agent_owned={m.get('n_agent_owned', 0)} human_owned={m.get('n_human_owned', 0)} refusal_solution={m.get('n_refusal_solution', 0)}",
        f"- Harness debt: {payload.get('harness_debt_n', 0)} (rewalks/mislabelled gates; not 'q > 0.19')",
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
        f"proxy={m['search_power_proxy']} auditor={'SKIP' if payload['auditor'].get('skipped') else ('PASS' if payload['auditor']['ok'] else 'FAIL')} "
        f"ok={payload['ok']} |\n"
    )
    if log.exists():
        text = log.read_text(encoding="utf-8")
        log.write_text(upsert_log_row(text, when, row), encoding="utf-8")
    else:
        log.write_text(
            "# Scientific-search cycle log\n\n| Date | Metrics |\n|---|---|\n" + row,
            encoding="utf-8",
        )
    return md, JSON_OUT


def upsert_log_row(text: str, when: str, row: str) -> str:
    """Replace the same-date log row instead of skipping it.

    Earlier same-calendar-day numbers stay only if they used a different date key
    (e.g. 2026-08-24-first). A second run with the same `when` overwrites that row.
    """
    line = row if row.endswith("\n") else row + "\n"
    pattern = re.compile(rf"^\| {re.escape(when)} \|.*\n?", re.MULTILINE)
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    if text and not text.endswith("\n"):
        text += "\n"
    return text + line



def compounding_invariants(
    previous: dict | None, metrics: dict, by_id: dict | None = None
) -> list[str]:
    """Killed and closed nodes must not vanish. That is the no-reset rule."""
    if not previous:
        return []
    old = previous.get("metrics") or {}
    fails = []
    for key, label in (("killed", "killed"), ("closed_lemma", "closed")):
        vanished = set(old.get(key) or []) - set(metrics.get(key) or [])
        if vanished:
            fails.append(f"{label} nodes vanished (reset forbidden): {sorted(vanished)}")
    gates_left = set(old.get("blocked_human") or []) - set(metrics.get("blocked_human") or [])
    for nid in sorted(gates_left):
        node = (by_id or {}).get(nid) or {}
        if not str(node.get("owner_event") or "").strip():
            fails.append(
                f"{nid}: left blocked_human without owner_event (agents do not fill human gates)"
            )
    return fails


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
    previous = None
    if JSON_OUT.exists():
        try:
            previous = json.loads(JSON_OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = None
    failures.extend(compounding_invariants(previous, m, node_map(tree)))
    debt = harness_debt(tree, memory)
    failures.extend(debt)
    if m.get("n_scientific_alive_families", m["n_alive_families"]) < 3:
        failures.append(
            f"width collapse: only {m.get('n_scientific_alive_families', m['n_alive_families'])} scientific families alive; keep F01–F03"
        )
    if skip_auditor:
        auditor = {"ok": False, "skipped": True, "stdout": "", "stderr": ""}
        failures.append("auditor skipped; cycle is not green")
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
        "harness_debt": debt,
        "harness_debt_n": len(debt),
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
        f"proxy={m['search_power_proxy']} "
        f"harness_debt={payload.get('harness_debt_n', 0)}"
    )
    print("alive_families:", ", ".join(m["alive_families"]))
    if payload["failures"]:
        for fail in payload["failures"]:
            print(" -", fail)
        return 1
    if not args.no_write:
        print(f"wrote {JSON_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
