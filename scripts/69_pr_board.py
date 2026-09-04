#!/usr/bin/env python3
"""Classify open GitHub PRs against analysis_plan/pr_board_policy.yml.

Does not merge. Does not close. Closing is Playbook 07 after the unique-file check.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "analysis_plan" / "pr_board_policy.yml"
REPORTS = ROOT / "reports"


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def load_policy() -> dict:
    return yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))


def list_open_prs() -> list[dict]:
    proc = _run(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,isDraft,mergeable,headRefName,url,updatedAt",
        ]
    )
    return json.loads(proc.stdout)


def unique_paths(head_ref: str, living_ref: str) -> list[str]:
    living_files = set(
        _run(["git", "ls-tree", "-r", "--name-only", living_ref]).stdout.splitlines()
    )
    try:
        head_files = _run(
            ["git", "ls-tree", "-r", "--name-only", head_ref], check=True
        ).stdout.splitlines()
    except subprocess.CalledProcessError:
        # Origin ref may be absent locally.
        fetched = _run(["git", "ls-tree", "-r", "--name-only", f"origin/{head_ref}"], check=False)
        if fetched.returncode != 0:
            return ["<ref missing: cannot compute unique files>"]
        head_files = fetched.stdout.splitlines()
    return sorted(p for p in head_files if p not in living_files)


def classify(pr: dict, policy: dict) -> dict:
    by_number = {int(row["number"]): row for row in policy.get("classified", [])}
    row = by_number.get(int(pr["number"]))
    if row is None:
        return {
            "action": policy.get("default_action", "KEEP_REVIEW"),
            "note": "Unclassified. Inspect unique files before any close.",
            "superseded_by": None,
        }
    return {
        "action": row["action"],
        "note": row.get("note", ""),
        "superseded_by": row.get("superseded_by"),
    }


def closable(action: str, unique: list[str]) -> bool:
    if action != "CLOSE_SUPERSEDED":
        return False
    if unique and unique[0].startswith("<ref missing"):
        return False
    return len(unique) == 0


def render(prs: list[dict], policy: dict, unique_map: dict[int, list[str]], today: str) -> str:
    living = policy["living_science_pr"]
    merged = policy.get("living_science_merged", False)
    living_line = (
        f"**Living science tip:** `{policy['living_science_ref']}` "
        f"(PR #{living} merged)."
        if merged
        else f"**Living science PR:** #{living} (`{policy['living_science_ref']}`)."
    )
    lines = [
        f"# Open PR board — {today}",
        "",
        living_line,
        "**Rule:** do not merge. Close only `CLOSE_SUPERSEDED` rows with zero unique files versus the living tip.",
        f"**Gate 3:** remains open. Playbook: `analysis_plan/playbooks/07_pr_board.md`.",
        "",
        "| PR | Draft | Mergeable | Action | Unique vs living tip | Note |",
        "|---|---|---|---|---|---|",
    ]
    close_ready = []
    keep = []
    for pr in sorted(prs, key=lambda p: -int(p["number"])):
        meta = classify(pr, policy)
        uniq = unique_map.get(int(pr["number"]), [])
        n_u = (
            "unknown"
            if uniq and str(uniq[0]).startswith("<ref missing")
            else str(len(uniq))
        )
        draft = "yes" if pr.get("isDraft") else "no"
        lines.append(
            f"| [#{pr['number']}]({pr['url']}) {pr['title']} | {draft} | {pr.get('mergeable')} | "
            f"`{meta['action']}` | {n_u} | {meta['note']} |"
        )
        if closable(meta["action"], uniq):
            close_ready.append(pr["number"])
        else:
            keep.append(pr["number"])
    lines.extend(
        [
            "",
            "## Close-ready (zero unique files)",
            "",
        ]
    )
    if close_ready:
        lines.append(", ".join(f"#{n}" for n in close_ready))
    else:
        lines.append("_None._")
    lines.extend(
        [
            "",
            "## Keep open",
            "",
            ", ".join(f"#{n}" for n in keep) if keep else "_None._",
            "",
            "## Unique paths (close-ready should be empty)",
            "",
        ]
    )
    for pr in sorted(prs, key=lambda p: -int(p["number"])):
        meta = classify(pr, policy)
        uniq = unique_map.get(int(pr["number"]), [])
        if meta["action"] != "CLOSE_SUPERSEDED":
            continue
        lines.append(f"### #{pr['number']}")
        if not uniq:
            lines.append("None.")
        else:
            lines.extend(f"- `{p}`" for p in uniq[:30])
            if len(uniq) > 30:
                lines.append(f"- … +{len(uniq) - 30} more")
        lines.append("")
    lines.extend(
        [
            "## Policy",
            "",
            "Do not merge. Do not freeze Gate 3. Playbook 06 lives on PR #68; this branch uses Playbooks 07 and 08 so the numbers do not collide.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def resolve_head(pr: dict) -> str:
    name = pr["headRefName"]
    for candidate in (f"origin/{name}", name):
        chk = _run(["git", "rev-parse", "--verify", candidate], check=False)
        if chk.returncode == 0:
            return candidate
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--json", action="store_true", help="also write reports/pr_board_latest.json")
    args = parser.parse_args()
    policy = load_policy()
    prs = list_open_prs()
    living_ref = policy["living_science_ref"]
    unique_map: dict[int, list[str]] = {}
    close_ready: list[int] = []
    for pr in prs:
        head = resolve_head(pr)
        uniq = unique_paths(head, living_ref)
        unique_map[int(pr["number"])] = uniq
        meta = classify(pr, policy)
        if closable(meta["action"], uniq):
            close_ready.append(int(pr["number"]))
    md = render(prs, policy, unique_map, args.date)
    REPORTS.mkdir(exist_ok=True)
    dated = REPORTS / f"pr_board_{args.date}.md"
    latest = REPORTS / "pr_board_latest.md"
    dated.write_text(md, encoding="utf-8")
    latest.write_text(md, encoding="utf-8")
    payload = {
        "date": args.date,
        "living_science_pr": policy["living_science_pr"],
        "open_count": len(prs),
        "close_ready": close_ready,
        "numbers": [int(p["number"]) for p in prs],
    }
    if args.json:
        (REPORTS / "pr_board_latest.json").write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8"
        )
    print(md)
    print(f"Wrote {dated} ({len(prs)} open; close-ready {close_ready})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
