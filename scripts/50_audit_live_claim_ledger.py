#!/usr/bin/env python3
"""Audit the live manuscript against the machine claim ledger.

Fails on Hogan-weather drift, forbidden phrases, missing display strings,
missing source files, and CSV contradictions.

Usage:
  python3 scripts/50_audit_live_claim_ledger.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "manuscript/live_collaborative/claim_ledger.yml"
OUT = ROOT / "outputs/auto_research/claim_ledger_audit.json"


def load_yaml(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(text)
    except ImportError:
        pass
    # Minimal fallback: require PyYAML for this file.
    raise SystemExit("PyYAML is required. pip install pyyaml")


def norm_dash(s: str) -> str:
    return (
        s.replace("–", "-")
        .replace("—", "-")
        .replace("−", "-")
        .replace(",", "")
        .replace(" ", "")
    )


def row_matches(row: dict, match: dict) -> bool:
    for k, v in match.items():
        if str(row.get(k, "")).strip() != str(v).strip():
            return False
    return True


def csv_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def as_float(x) -> float:
    return float(str(x).replace(",", "").strip())


def main() -> int:
    spec = load_yaml(LEDGER)
    manuscript = ROOT / spec["manuscript"]
    body = manuscript.read_text(encoding="utf-8")
    failures: list[str] = []
    passes: list[str] = []

    weather = spec["hogan_weather"]["must_contain"]
    if weather not in body:
        failures.append(f"HOGAN_WEATHER missing: {weather!r}")
    else:
        passes.append("hogan_weather_start")
    for extra in spec["hogan_weather"].get("also_must_contain", []):
        if extra not in body:
            failures.append(f"HOGAN_WEATHER fragment missing: {extra!r}")
        else:
            passes.append(f"hogan_weather:{extra[:24]}")

    low = body.lower()
    for phrase in spec.get("forbidden_in_manuscript", []):
        if phrase.lower() in low:
            failures.append(f"FORBIDDEN phrase present: {phrase!r}")
        else:
            passes.append(f"forbidden_absent:{phrase}")

    for claim in spec.get("claims", []):
        cid = claim["id"]
        displays = [claim["display"]]
        alt = claim.get("display_alt")
        if isinstance(alt, str) and alt:
            displays.append(alt)
        elif isinstance(alt, list):
            displays.extend(alt)
        if not any(d in body for d in displays):
            failures.append(f"{cid}: display not in manuscript {displays!r}")
        else:
            passes.append(f"{cid}:display")

        src = claim.get("source")
        if src and claim.get("provenance") != "cited_paper":
            sp = ROOT / src
            if not sp.exists():
                failures.append(f"{cid}: source missing {src}")
                continue
            passes.append(f"{cid}:source_exists")

        csv_spec = claim.get("csv")
        if csv_spec:
            rows = csv_rows(ROOT / src)
            hits = [r for r in rows if row_matches(r, csv_spec["match"])]
            if len(hits) != 1:
                failures.append(f"{cid}: expected 1 CSV row, got {len(hits)} for {csv_spec['match']}")
                continue
            raw = hits[0][csv_spec["column"]]
            if "equals_display" in csv_spec:
                got = norm_dash(str(raw))
                want = norm_dash(csv_spec["equals_display"])
                if got != want:
                    failures.append(f"{cid}: CSV display {raw!r} != {csv_spec['equals_display']!r}")
                else:
                    passes.append(f"{cid}:csv_display")
            elif "equals" in csv_spec:
                rnd = csv_spec.get("round")
                got = as_float(raw)
                want = as_float(csv_spec["equals"])
                if rnd is not None:
                    got = round(got, int(rnd))
                    want = round(want, int(rnd))
                if got != want:
                    failures.append(f"{cid}: CSV {raw!r} != {csv_spec['equals']!r}")
                else:
                    passes.append(f"{cid}:csv_value")

        count_spec = claim.get("csv_count_where")
        if count_spec:
            rows = csv_rows(ROOT / src)
            col = count_spec["column"]
            thr = float(count_spec["value"])
            n_hit = sum(1 for r in rows if as_float(r[col]) >= thr)
            if count_spec.get("n_rows_equals") is not None and len(rows) != int(
                count_spec["n_rows_equals"]
            ):
                failures.append(
                    f"{cid}: row count {len(rows)} != {count_spec['n_rows_equals']}"
                )
            if n_hit != int(count_spec["equals"]):
                failures.append(f"{cid}: count_where got {n_hit} != {count_spec['equals']}")
            else:
                passes.append(f"{cid}:csv_count_where")

        if claim.get("provenance") not in {
            "HA_APPROVED_AGGREGATE",
            "REAL",
            "cited_paper",
            "manuscript_meta",
        }:
            failures.append(f"{cid}: unknown provenance {claim.get('provenance')}")

    report = {
        "manuscript": str(manuscript.relative_to(ROOT)),
        "n_pass": len(passes),
        "n_fail": len(failures),
        "passes": passes,
        "failures": failures,
        "ok": not failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("CLAIM LEDGER AUDIT FAILED")
        for f in failures:
            print(" -", f)
        print(f"wrote {OUT}")
        return 1
    print("CLAIM LEDGER AUDIT PASSED")
    print(f"{len(passes)} checks")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
