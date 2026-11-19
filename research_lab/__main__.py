"""Run, verify, or challenge the descriptive evidence release from a checkout."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import time

from . import challenge, hindcast, release, service_context, weather_design, weather_sources


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode()


def csv_bytes(rows):
    if not rows:
        raise ValueError("An experiment produced no rows")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        # Keep outputs portable across BLAS implementations, well beyond paper precision.
        writer.writerow({k: format(v, ".10g") if isinstance(v, float) else v for k, v in row.items()})
    return buffer.getvalue().encode("utf-8")


def check_inputs(root, expected):
    for rel, sha in expected.items():
        if digest((root / rel).read_bytes()) != sha:
            raise ValueError(f"Input digest mismatch: {rel}")


def with_manifest(payload, sources, code_paths, kind):
    manifest = {
        "kind": kind, "inputs_sha256": sources,
        "code_sha256": {name: digest((PACKAGE / name).read_bytes()) for name in code_paths},
        "output_sha256": {name: digest(content) for name, content in payload.items()},
    }
    return {**payload, "manifest.json": json_bytes(manifest)}


def study(root):
    protocol = json.loads((PACKAGE / "protocol.json").read_bytes())
    check_inputs(root, protocol["inputs"])
    annual = root / release.ANNUAL
    context = service_context.analyse(annual, root / "research_lab/sources")
    tables = {"service_context": context, "hindcast": hindcast.analyze(annual),
              "weather_design": weather_design.analyze(root),
              "weather_models": release.weather_models(root / release.ESTIMATES),
              "annual_changes": release.annual_changes(context)}
    if tables.keys() != protocol["experiments"].keys():
        raise ValueError("Executed studies differ from the protocol")
    payload = {f"{name}.csv": csv_bytes(rows) for name, rows in tables.items()}
    payload["weather_source_agreement.json"] = json_bytes(weather_sources.compare_daily_sources(root))
    return with_manifest(
        payload, {**protocol["inputs"], **weather_sources.SOURCE_SHA256},
        ["__main__.py", "protocol.json", "release.py", "hindcast.py", "service_context.py",
         "weather_design.py", "weather_sources.py"], "November descriptive research release",
    )


def proposal(root, card):
    spec = challenge.read_card(card)
    grid, decisions, verdict = challenge.evaluate(root, spec)
    payload = {"question.json": json_bytes(spec), "all_designs.csv": csv_bytes(grid),
               "selected_checks.csv": csv_bytes(decisions), "verdict.json": json_bytes(verdict)}
    bundle = with_manifest(payload, weather_design.SOURCE_SHA256,
                           ["__main__.py", "challenge.py", "weather_design.py"], "Weather-only question card")
    return bundle, verdict


def compare(directory, payload):
    if not directory.is_dir():
        raise ValueError(f"Missing result directory: {directory}")
    names = {p.name for p in directory.iterdir()}
    if names != set(payload):
        raise ValueError(f"Result inventory differs at {directory}: {sorted(names ^ set(payload))}")
    for name, data in payload.items():
        if (directory / name).read_bytes() != data:
            raise ValueError(f"Result differs: {directory / name}")


def save_new(directory, payload):
    """Commit a complete result directory. An existing different result is preserved."""
    directory = directory.resolve()
    if directory.exists():
        compare(directory, payload)
        return
    directory.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=directory.parent) as temp:
        draft = Path(temp) / "completed"
        draft.mkdir()
        for name, data in payload.items():
            (draft / name).write_bytes(data)
        try:
            draft.rename(directory)
        except OSError:
            if not directory.is_dir():
                raise
            compare(directory, payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("check", help="Recompute the published tables and the example challenge")
    run = commands.add_parser("run", help="Write the complete study to a new directory")
    run.add_argument("--out", type=Path, required=True)
    probe = commands.add_parser("challenge", help="Evaluate an outcome-blind JSON question")
    probe.add_argument("card", type=Path)
    probe.add_argument("--out", type=Path, required=True, help="Parent directory for content-addressed runs")
    args = parser.parse_args()
    start = time.perf_counter()
    try:
        if args.action == "challenge":
            payload, verdict = proposal(ROOT, args.card)
            run_id = digest(payload["manifest.json"])[:20]
            dest = args.out / run_id
            save_new(dest, payload)
            print(f"{verdict['cells_meeting_criterion']}/{verdict['cells_evaluated']} selected cells meet "
                  f"the criterion. Saved all {verdict['grid_rows_returned']} designs in {dest}")
        elif args.action == "run":
            save_new(args.out, study(ROOT))
            print(f"Wrote verified-source results to {args.out}")
        else:
            compare(PACKAGE / "results", study(ROOT))
            sample, verdict = proposal(ROOT, PACKAGE / "questions/later_weather_support.json")
            compare(PACKAGE / "questions/later_weather_support", sample)
            print(f"Reproduced the study and {verdict['grid_rows_returned']} question-card designs.")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Research check failed: {exc}\n")
    print(f"Elapsed {time.perf_counter() - start:.2f} s")


if __name__ == "__main__":
    main()
