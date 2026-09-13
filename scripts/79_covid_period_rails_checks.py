#!/usr/bin/env python3
"""Rails checks for the covid_period candidate manuscript.

This is the documented equivalent of `scripts/50_audit_live_claim_ledger.py` for the
covid_period track. That script cannot audit this ledger: it reads a `claims:` schema
with `display`/`csv` keys, while `manuscript/covid_period/claim_ledger.yml` uses a
`numerals:` schema. Pointed at the covid ledger it reports a vacuous pass (one check),
which is worse than no audit. This script reads the covid schema instead.

Checks
  1. Claim ledger — every ledger numeral appears in the draft; every named source file
     exists; no source is a governed panel.
  2. Citation order — Vancouver order of first appearance, no orphan entries, no
     in-text number missing from the list.
  3. Hogan weather — the HKO opening and the averaging sentence are verbatim.
  4. Forbidden phrases — the ledger stop list, plus Gate 3 freeze language.
  5. Invented coefficients — no count ratio in a sentence about stroke or laboratory
     fields, which were never delivered.
  6. Figures — every referenced figure file exists and every figure is named in text.
  7. Print page map — the recorded map exists and no interior page is under-filled.
  8. Frozen neighbours — no diff against the base branch under
     manuscript/live_collaborative/ or manuscript/archive/.

Usage
  python3 scripts/79_covid_period_rails_checks.py
  python3 scripts/79_covid_period_rails_checks.py --base main --out PATH
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVID_DIR = ROOT / "manuscript" / "covid_period"
DRAFT = COVID_DIR / "Manuscript_covid_period_draft.md"
LEDGER = COVID_DIR / "claim_ledger.yml"
PAGE_MAP = COVID_DIR / "PRINT_PAGE_MAP.md"
MAIN_PDF = COVID_DIR / "Heat_CVD_Manuscript_covid_period.pdf"
BUILDER = ROOT / "scripts" / "78_covid_period_manuscript_docx.py"
DEFAULT_OUT = ROOT / "outputs" / "covid_period" / "rails_checks.json"

FROZEN_PATHS = ("manuscript/live_collaborative", "manuscript/archive")
GOVERNED_MARKERS = (
    "chd_analysis_panel",
    "hf_analysis_panel",
    "ha_secure_placeholder",
    "aggregates_normalized",
    "synthetic_analysis_panel",
)

HOGAN_OPEN = "Meteorological data was obtained from the HKO."
HOGAN_AVG = (
    "All monthly data were derived by taking the average of daily data in each calendar month."
)

GATE_FREEZE_PATTERNS = (
    r"gate\s*3",
    r"confirmatory freeze (?:has been|is) declared",
    r"we (?:therefore )?freeze",
    r"frozen confirmatory primary",
)

UNDELIVERED_TOPICS = ("stroke", "laborator", "hba1c", "ldl", "person-time coefficient")
CR_PATTERN = re.compile(r"\d\.\d{2,3}\s*\(")

MIN_INTERIOR_FILL = 0.45
MIN_MEAN_FILL = 0.80

RESULTS_HEADINGS = (
    "### Outcome series",
    "### Exposure context",
    "### Nested-window official-day panel",
    "### Twelve-fit thermal exhibit",
    "### Uncertainty ladder",
)

CUT_RESIDUE = (
    "The main reported interval is Newey–West",
    "Nine of the twelve",
    "left to the supplement",
    "### Specification and diagnostic checks",
)


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment guard
        raise SystemExit("PyYAML is required: pip install pyyaml") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def norm(text: str) -> str:
    """Normalise dashes, thin spaces, and thousands separators for numeral matching."""
    for dash in ("–", "—", "−"):
        text = text.replace(dash, "-")
    return text.replace(",", "").replace("\u2009", " ").replace("\u00a0", " ")


def split_body_refs(text: str) -> tuple[str, str]:
    if "## References" not in text:
        raise SystemExit("draft has no References section")
    body, refs = text.split("## References", 1)
    return body, refs


def cited_numbers(body: str) -> list[int]:
    """In-text citation numbers in order of appearance, ranges expanded."""
    order: list[int] = []
    for match in re.finditer(r"\[([\d,\s\u2013\-]+)\]", body):
        for part in match.group(1).replace("–", "-").split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                low, high = (piece.strip() for piece in part.split("-", 1))
                if low.isdigit() and high.isdigit():
                    order.extend(range(int(low), int(high) + 1))
            elif part.isdigit():
                order.append(int(part))
    return order


def listed_numbers(refs: str) -> list[int]:
    return [int(match.group(1)) for match in re.finditer(r"^(\d+)\.\s", refs, re.M)]


def check_claim_ledger(draft: str, ledger: dict) -> tuple[list[str], list[str]]:
    passes: list[str] = []
    failures: list[str] = []
    normalised = norm(draft)

    weather = ledger.get("hogan_weather", {})
    for key in ("must_contain", "averaging"):
        needle = weather.get(key)
        if not needle:
            failures.append(f"ledger hogan_weather.{key} missing")
        elif needle not in draft:
            failures.append(f"hogan_weather.{key} not verbatim in draft: {needle!r}")
        else:
            passes.append(f"hogan_weather:{key}")

    if str(ledger.get("gate_3", "")).strip().lower() != "open":
        failures.append(f"ledger gate_3 is {ledger.get('gate_3')!r}, expected open")
    else:
        passes.append("ledger:gate_3_open")

    numerals = ledger.get("numerals") or []
    if len(numerals) < 40:
        failures.append(f"ledger has only {len(numerals)} numerals; expected the full set")
    for item in numerals:
        name = item.get("name", "<unnamed>")
        display = item.get("display") or item.get("value")
        if display is None:
            failures.append(f"{name}: no value or display")
            continue
        if norm(str(display)) not in normalised:
            failures.append(f"{name}: {display!r} not found in the draft")
        else:
            passes.append(f"numeral:{name}")
        source = item.get("source")
        if not source:
            failures.append(f"{name}: no source")
            continue
        if any(marker in source for marker in GOVERNED_MARKERS):
            failures.append(f"{name}: source is a governed panel ({source})")
            continue
        if not (ROOT / source).exists():
            failures.append(f"{name}: source missing ({source})")
        else:
            passes.append(f"source:{name}")
    return passes, failures


def check_forbidden(draft: str, ledger: dict) -> tuple[list[str], list[str]]:
    passes: list[str] = []
    failures: list[str] = []
    low = draft.lower()
    phrases = set()
    for key in ("scientific_body_forbids", "forbidden_in_this_track"):
        for phrase in ledger.get(key) or []:
            phrase = str(phrase).strip()
            # Ledger prose entries describe a rule rather than a literal string.
            if len(phrase.split()) <= 4 and "as author of" not in phrase:
                phrases.add(phrase)
    for phrase in sorted(phrases):
        if phrase.lower() in low:
            failures.append(f"forbidden phrase present: {phrase!r}")
        else:
            passes.append(f"forbidden_absent:{phrase}")

    for pattern in GATE_FREEZE_PATTERNS:
        if re.search(pattern, low):
            failures.append(f"gate-freeze language present: /{pattern}/")
        else:
            passes.append(f"no_gate_freeze:/{pattern}/")

    # The 2022 Annals paper is by Wai et al., not Hung et al.
    doi = "10.1016/j.annemergmed.2021.09.424"
    if doi in draft:
        preceding = draft.split(doi)[0][-160:]
        if "Hung KK" in preceding:
            failures.append("Hung KK attributed to the Wai et al. Annals paper")
        else:
            passes.append("attribution:wai_annals")
    return passes, failures


def check_citation_order(draft: str) -> tuple[list[str], list[str], dict]:
    passes: list[str] = []
    failures: list[str] = []
    body, refs = split_body_refs(draft)
    cited = cited_numbers(body)
    listed = listed_numbers(refs)

    first_appearance: list[int] = []
    for number in cited:
        if number not in first_appearance:
            first_appearance.append(number)

    missing = sorted(set(cited) - set(listed))
    orphans = sorted(set(listed) - set(cited))
    if missing:
        failures.append(f"in-text numbers with no reference entry: {missing}")
    else:
        passes.append("citations:no_missing_entries")
    if orphans:
        failures.append(f"reference entries never cited: {orphans}")
    else:
        passes.append("citations:no_orphans")
    if listed != list(range(1, len(listed) + 1)):
        failures.append(f"reference list is not numbered 1..N: {listed}")
    else:
        passes.append("citations:list_is_sequential")
    if first_appearance != list(range(1, len(first_appearance) + 1)):
        failures.append(f"citations are not in order of appearance: {first_appearance}")
    else:
        passes.append("citations:vancouver_order_of_appearance")

    facts = {
        "n_listed": len(listed),
        "n_cited": len(first_appearance),
        "first_appearance_order": first_appearance,
        "orphans": orphans,
        "missing": missing,
    }
    return passes, failures, facts


def check_no_invented_coefficients(draft: str) -> tuple[list[str], list[str]]:
    passes: list[str] = []
    failures: list[str] = []
    body, _ = split_body_refs(draft)
    for sentence in re.split(r"(?<=[.!?])\s+", body):
        low = sentence.lower()
        if any(topic in low for topic in UNDELIVERED_TOPICS) and CR_PATTERN.search(sentence):
            failures.append(f"coefficient in an undelivered-topic sentence: {sentence.strip()[:120]}")
    if not failures:
        passes.append("no_invented_coefficients")
    return passes, failures


def check_figures(draft: str) -> tuple[list[str], list[str]]:
    passes: list[str] = []
    failures: list[str] = []
    images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", draft)
    if len(images) != 3:
        failures.append(f"expected 3 figure embeds, found {len(images)}")
    for alt, rel in images:
        path = (DRAFT.parent / rel).resolve()
        if not path.is_file():
            failures.append(f"figure file missing: {rel}")
        else:
            passes.append(f"figure_file:{path.name}")
        label = alt.strip()
        if label and f"**{label}." not in draft:
            failures.append(f"{label} has no bold caption")
        elif label:
            passes.append(f"figure_caption:{label}")
    for number in (1, 2, 3):
        body, _ = split_body_refs(draft)
        prose = re.sub(r"\*\*Figure \d[^*]*\*\*", "", body)
        if f"Figure {number}" not in prose:
            failures.append(f"Figure {number} is never named in the prose")
        else:
            passes.append(f"figure_named:{number}")
    return passes, failures


def check_imrd_spine(draft: str) -> tuple[list[str], list[str]]:
    """One IMRD: named Results headings, no thermal-glue residue, Strengths before Conclusion."""
    passes: list[str] = []
    failures: list[str] = []
    body, _ = split_body_refs(draft)

    positions = []
    for heading in RESULTS_HEADINGS:
        idx = body.find(heading)
        if idx < 0:
            failures.append(f"missing Results heading: {heading}")
        else:
            positions.append(idx)
            passes.append(f"results_heading:{heading}")
    if len(positions) == len(RESULTS_HEADINGS) and positions != sorted(positions):
        failures.append(f"Results headings out of order: {RESULTS_HEADINGS}")
    elif len(positions) == len(RESULTS_HEADINGS):
        passes.append("results_headings:august_scan_order")

    extra = re.findall(r"^### .+$", body, re.M)
    extra = [h for h in extra if h not in RESULTS_HEADINGS]
    # Methods subheads and other IMRD h2s are ##, so ### should be Results only
    # plus Methods h3 (####) is not ###. Data-source #### is h3. Statistical
    # analysis is ### under Methods.
    allowed_methods = {
        "### Data sources",
        "### Statistical analysis",
        "### Sensitivity analysis",
        "### Software",
    }
    unexpected = [h for h in extra if h not in allowed_methods]
    if unexpected:
        failures.append(f"unexpected ### headings: {unexpected}")
    else:
        passes.append("results:no_sixth_heading")

    for residue in CUT_RESIDUE:
        if residue in draft:
            failures.append(f"cut residue present: {residue!r}")
        else:
            passes.append(f"cut_absent:{residue}")

    strengths = body.find("## Strengths and limitations")
    conclusion = body.find("## Conclusion")
    if strengths < 0 or conclusion < 0:
        failures.append("missing Strengths or Conclusion heading")
    elif strengths > conclusion:
        failures.append("Strengths and limitations follows Conclusion")
    else:
        passes.append("imrd:strengths_before_conclusion")
    return passes, failures


def check_ledger_bindings(ledger: dict, citation_facts: dict) -> tuple[list[str], list[str]]:
    """The ledger binds the reference count, the figure files, and the print outputs."""
    passes: list[str] = []
    failures: list[str] = []

    manuscript = ledger.get("manuscript")
    if manuscript != str(DRAFT.relative_to(ROOT)):
        failures.append(f"ledger manuscript is {manuscript!r}, expected the covid_period draft")
    else:
        passes.append("ledger:manuscript_path")

    references = ledger.get("references") or {}
    if references.get("numbering") != "vancouver_order_of_appearance":
        failures.append("ledger references.numbering is not vancouver_order_of_appearance")
    else:
        passes.append("ledger:reference_numbering")
    if references.get("n_entries") != citation_facts["n_listed"]:
        failures.append(
            f"ledger references.n_entries {references.get('n_entries')} != "
            f"{citation_facts['n_listed']} entries in the draft"
        )
    else:
        passes.append("ledger:reference_count")

    figures = ledger.get("figures") or []
    if len(figures) != 3:
        failures.append(f"ledger binds {len(figures)} figures, expected 3")
    for figure in figures:
        rel = figure.get("file", "")
        if not (ROOT / rel).is_file():
            failures.append(f"ledger figure file missing: {rel}")
        else:
            passes.append(f"ledger:figure_file:{figure.get('label')}")

    print_spec = ledger.get("print") or {}
    if print_spec.get("page_break_after_every_float") is not False:
        failures.append("ledger print contract does not forbid a break after every float")
    else:
        passes.append("ledger:no_break_after_every_float")
    for key in ("builder", "word", "pdf", "page_map"):
        rel = print_spec.get(key)
        if not rel or not (ROOT / rel).exists():
            failures.append(f"ledger print.{key} missing on disk: {rel}")
        else:
            passes.append(f"ledger:print_{key}")
    return passes, failures


def _load_builder():
    spec = importlib.util.spec_from_file_location("covid_builder", BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # The builder defines a dataclass, which needs the module registered first.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def check_page_map() -> tuple[list[str], list[str], dict]:
    passes: list[str] = []
    failures: list[str] = []
    facts: dict = {}
    if not PAGE_MAP.is_file():
        failures.append("PRINT_PAGE_MAP.md missing; run scripts/78_covid_period_manuscript_docx.py")
        return passes, failures, facts
    passes.append("page_map:exists")
    text = PAGE_MAP.read_text(encoding="utf-8")
    for needed in ("No page break is emitted after a table or a figure", "Float contract"):
        if needed not in text:
            failures.append(f"page map does not record the float contract: {needed!r}")
        else:
            passes.append("page_map:float_contract_recorded")
    if not MAIN_PDF.is_file():
        failures.append("built PDF missing; run scripts/78_covid_period_manuscript_docx.py")
        return passes, failures, facts
    try:
        builder = _load_builder()
        page_facts = builder.page_facts(MAIN_PDF)
        summary = builder._fill_summary(page_facts)
    except Exception as exc:  # pragma: no cover - dependency guard
        failures.append(f"page map could not be recomputed: {exc}")
        return passes, failures, facts
    facts = {
        "pages": summary["pages"],
        "mean_fill_interior": summary["mean_fill_interior"],
        "pages_below_45pct": summary["pages_below_45pct"],
    }
    if summary["pages_below_45pct"]:
        failures.append(f"interior pages under {MIN_INTERIOR_FILL} fill: {summary['pages_below_45pct']}")
    else:
        passes.append("page_map:no_underfilled_interior_page")
    if summary["mean_fill_interior"] < MIN_MEAN_FILL:
        failures.append(
            f"mean interior fill {summary['mean_fill_interior']} below {MIN_MEAN_FILL}"
        )
    else:
        passes.append("page_map:mean_fill")
    if f"**Pages:** {summary['pages']}." not in PAGE_MAP.read_text(encoding="utf-8"):
        failures.append("page map page count is stale")
    else:
        passes.append("page_map:page_count_current")
    return passes, failures, facts


def check_frozen_neighbours(base: str) -> tuple[list[str], list[str]]:
    passes: list[str] = []
    failures: list[str] = []
    for path in FROZEN_PATHS:
        proc = subprocess.run(
            ["git", "diff", "--name-only", base, "--", path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            failures.append(f"could not diff {path} against {base}: {proc.stderr.strip()}")
            continue
        changed = [line for line in proc.stdout.splitlines() if line.strip()]
        if changed:
            failures.append(f"{path} changed against {base}: {changed}")
        else:
            passes.append(f"frozen:{path}")
    return passes, failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="covid_period rails checks")
    parser.add_argument("--base", default="main", help="branch to diff frozen paths against")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--skip-frozen-diff",
        action="store_true",
        help="skip the git diff against the base branch",
    )
    args = parser.parse_args(argv)

    draft = DRAFT.read_text(encoding="utf-8")
    ledger = load_yaml(LEDGER)

    passes: list[str] = []
    failures: list[str] = []
    facts: dict = {}

    for fn in (
        lambda: check_claim_ledger(draft, ledger),
        lambda: check_forbidden(draft, ledger),
        lambda: check_no_invented_coefficients(draft),
        lambda: check_figures(draft),
        lambda: check_imrd_spine(draft),
    ):
        ok, bad = fn()
        passes += ok
        failures += bad

    ok, bad, citation_facts = check_citation_order(draft)
    passes += ok
    failures += bad
    facts["citations"] = citation_facts

    ok, bad = check_ledger_bindings(ledger, citation_facts)
    passes += ok
    failures += bad

    ok, bad, page_facts_summary = check_page_map()
    passes += ok
    failures += bad
    facts["page_map"] = page_facts_summary

    if not args.skip_frozen_diff:
        ok, bad = check_frozen_neighbours(args.base)
        passes += ok
        failures += bad

    if HOGAN_OPEN not in draft or HOGAN_AVG not in draft:
        failures.append("Hogan HKO paragraph drifted")
    else:
        passes.append("hogan_weather:verbatim")

    report = {
        "draft": str(DRAFT.relative_to(ROOT)),
        "ledger": str(LEDGER.relative_to(ROOT)),
        "n_pass": len(passes),
        "n_fail": len(failures),
        "facts": facts,
        "passes": passes,
        "failures": failures,
        "ok": not failures,
    }
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if failures:
        print("COVID_PERIOD RAILS CHECKS FAILED")
        for failure in failures:
            print(" -", failure)
        print(f"wrote {out_path}")
        return 1
    print("COVID_PERIOD RAILS CHECKS PASSED")
    print(f"{len(passes)} checks")
    print(
        "citations: "
        f"{citation_facts['n_cited']} cited of {citation_facts['n_listed']} listed, "
        "in order of appearance"
    )
    if page_facts_summary:
        print(
            f"page map: {page_facts_summary['pages']} pages, mean interior fill "
            f"{page_facts_summary['mean_fill_interior']}"
        )
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
