#!/usr/bin/env python3
"""Audit the live manuscript against the machine claim ledger.

Fails on Hogan-weather drift, forbidden phrases, missing display strings,
missing source files, and CSV contradictions.

Usage:
  python3 scripts/50_audit_live_claim_ledger.py
  python3 scripts/50_audit_live_claim_ledger.py --ledger PATH --live PATH --out PATH
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "manuscript/live_collaborative/claim_ledger.yml"
DEFAULT_OUT = ROOT / "outputs/auto_research/claim_ledger_audit.json"


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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit live manuscript against claim_ledger.yml")
    p.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    p.add_argument("--live", type=Path, default=None, help="Override manuscript path in the YAML")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return p.parse_args(argv)


def fmt_rr_ci(row: dict, decimals: int) -> str:
    rr = round(as_float(row["rr"]), decimals)
    lo = round(as_float(row["rr_low"]), decimals)
    hi = round(as_float(row["rr_high"]), decimals)
    return f"{rr:.{decimals}f} ({lo:.{decimals}f}-{hi:.{decimals}f})"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ledger_path = args.ledger if args.ledger.is_absolute() else ROOT / args.ledger
    spec = load_yaml(ledger_path)
    manuscript = args.live if args.live is not None else ROOT / spec["manuscript"]
    if not manuscript.is_absolute():
        manuscript = ROOT / manuscript
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
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

        excl_spec = claim.get("csv_ci_excludes_one")
        if excl_spec:
            rows = csv_rows(ROOT / src)
            subset = [r for r in rows if row_matches(r, excl_spec.get("match") or {})]
            if excl_spec.get("n_rows_equals") is not None and len(subset) != int(
                excl_spec["n_rows_equals"]
            ):
                failures.append(
                    f"{cid}: ci subset {len(subset)} != {excl_spec['n_rows_equals']}"
                )
            lo_col = excl_spec.get("low_column", "rr_low")
            hi_col = excl_spec.get("high_column", "rr_high")
            n_excl = 0
            for r in subset:
                lo = as_float(r[lo_col])
                hi = as_float(r[hi_col])
                if lo > 1.0 or hi < 1.0:
                    n_excl += 1
            if n_excl != int(excl_spec["equals"]):
                failures.append(
                    f"{cid}: csv_ci_excludes_one got {n_excl} != {excl_spec['equals']}"
                )
            else:
                passes.append(f"{cid}:csv_ci_excludes_one")

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

        min_spec = claim.get("csv_min")
        if min_spec:
            rows = csv_rows(ROOT / src)
            if min_spec.get("n_rows_equals") is not None and len(rows) != int(
                min_spec["n_rows_equals"]
            ):
                failures.append(
                    f"{cid}: row count {len(rows)} != {min_spec['n_rows_equals']}"
                )
            vals = [as_float(r[min_spec["column"]]) for r in rows]
            got = min(vals)
            want = as_float(min_spec["equals"])
            rnd = min_spec.get("round")
            if rnd is not None:
                got = round(got, int(rnd))
                want = round(want, int(rnd))
            if got != want:
                failures.append(f"{cid}: csv_min got {got!r} != {want!r}")
            else:
                passes.append(f"{cid}:csv_min")

        rr_spec = claim.get("csv_rr_ci")
        if rr_spec:
            rows = csv_rows(ROOT / src)
            hits = [r for r in rows if row_matches(r, rr_spec["match"])]
            if len(hits) != 1:
                failures.append(
                    f"{cid}: expected 1 CSV row, got {len(hits)} for {rr_spec['match']}"
                )
            else:
                decimals = int(rr_spec.get("decimals", 3))
                got = norm_dash(fmt_rr_ci(hits[0], decimals))
                want = norm_dash(rr_spec["equals"])
                if got != want:
                    failures.append(
                        f"{cid}: csv_rr_ci {got!r} != {want!r}"
                    )
                else:
                    passes.append(f"{cid}:csv_rr_ci")

        sum_spec = claim.get("csv_sum_where")
        if sum_spec:
            rows = csv_rows(ROOT / src)
            col = sum_spec["column"]
            subset = rows
            for k, allowed in (sum_spec.get("where_in") or {}).items():
                allowed_s = {str(x).strip() for x in allowed}
                subset = [r for r in subset if str(r.get(k, "")).strip() in allowed_s]
            got = sum(as_float(r[col]) for r in subset)
            total = sum(as_float(r[col]) for r in rows)
            want = as_float(sum_spec["equals"])
            if got != want:
                failures.append(f"{cid}: csv_sum_where got {got} != {want}")
            else:
                passes.append(f"{cid}:csv_sum_where")
            if sum_spec.get("total_equals") is not None:
                want_total = as_float(sum_spec["total_equals"])
                if total != want_total:
                    failures.append(
                        f"{cid}: csv_sum total {total} != {want_total}"
                    )
                else:
                    passes.append(f"{cid}:csv_sum_total")

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
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("CLAIM LEDGER AUDIT FAILED")
        for f in failures:
            print(" -", f)
        print(f"wrote {out_path}")
        return 1
    print("CLAIM LEDGER AUDIT PASSED")
    print(f"{len(passes)} checks")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
