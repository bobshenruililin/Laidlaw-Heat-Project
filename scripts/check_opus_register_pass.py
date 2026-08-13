"""Provenance and register check for manuscript/live_collaborative/opus_hogan_register_pass.md.

Checks only the paste-ready blocks under each "### Replacement text" heading:
  1. every numeric token appears in the claim ledger, the live draft, or the say-map;
  2. the four headline estimates match outputs/release_chd_hf tables;
  3. no cns-writing forbidden phrase or internal process term is present.
"""

import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASS_FILE = ROOT / "manuscript/live_collaborative/opus_hogan_register_pass.md"
PROVENANCE_SOURCES = [
    ROOT / "manuscript/live_collaborative/claim_ledger.md",
    ROOT / "manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md",
    ROOT / "knowledge/2026-08-13_live_intro_discussion_say_map.md",
]
LADDER = ROOT / "outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv"
CORE = ROOT / "outputs/release_chd_hf/tables/table2_core_models.csv"

FORBIDDEN = [
    "TBD", "placeholder", "results forthcoming", "insert result",
    "to be confirmed", "work in progress", "Gate 3", "Tuesday lock",
    "Laidlaw", "F1.1", "F1.2", "very interesting", "remarkably",
    "groundbreaking", "novel and important", "it is important to note",
    "needless to say", "Hogan", "Roro", "Jasmine", "Bob",
]


def replacement_blocks(text):
    blocks = {}
    for chunk in re.split(r"\n(?=## )", text):
        head = re.match(r"## \d\.\s*(.+)", chunk)
        body = re.search(r"### Replacement text\n(.*?)\n### What changed", chunk, re.S)
        if head and body:
            blocks[head.group(1).strip()] = body.group(1).strip()
    return blocks


def word_count(block):
    block = re.sub(r"\*+", "", block)
    block = re.sub(r"\[\d+(,\d+)*\]", "", block)
    return len([w for w in block.split() if re.search(r"\w", w)])


def main():
    text = PASS_FILE.read_text(encoding="utf-8")
    blocks = replacement_blocks(text)
    if len(blocks) != 5:
        print(f"FAIL: expected 5 replacement blocks, found {len(blocks)}")
        return 1
    prose = "\n".join(blocks.values())
    failures = []

    print("== word counts (paste-ready prose only) ==")
    for name, block in blocks.items():
        print(f"{name:28s} {word_count(block):5d} words")
    print(f"{'TOTAL':28s} {word_count(prose):5d} words\n")

    haystack = "\n".join(p.read_text(encoding="utf-8") for p in PROVENANCE_SOURCES)
    haystack = haystack.replace(",", "").replace("\u2013", "-").replace("\u2212", "-")
    unsourced = []
    tokens = sorted(set(re.findall(r"\d[\d,\.]*", prose)))
    for token in tokens:
        if token.rstrip(".").replace(",", "") not in haystack:
            unsourced.append(token)
    print(f"== provenance: {len(tokens)} distinct numeric tokens ==")
    print("unsourced:", unsourced or "none", "\n")
    if unsourced:
        failures.append("numeric tokens without a ledger, live-draft, or say-map source")

    ladder = {
        (r["outcome"], r["exposure"], r["se_method"]): r
        for r in csv.DictReader(LADDER.open(encoding="utf-8-sig"))
    }
    print("== headline estimates against release tables ==")
    expected = [
        ("chd", "hot_nights", "NeweyWest_lag6", "1.022 (1.002-1.042)"),
        ("chd", "hot_nights", "NeweyWest_lag3", "1.022 (1.000-1.044)"),
        ("hf", "cold_days", "NeweyWest_lag6", "1.073 (1.006-1.144)"),
        ("hf", "cold_days", "model", "1.073 (1.023-1.125)"),
    ]
    for outcome, exposure, method, display in expected:
        row = ladder[(outcome, exposure, method)]
        ok = row["count_ratio_95CI"] == display
        print(f"{outcome:4s} {exposure:10s} {method:15s} {row['count_ratio_95CI']:22s} {'ok' if ok else 'MISMATCH'}")
        if not ok:
            failures.append(f"{outcome}/{exposure}/{method} display mismatch")

    nw3 = ladder[("chd", "hot_nights", "NeweyWest_lag3")]
    for label, value, quoted in (
        ("NW3 lower", nw3["rr_low"], "1.000253"),
        ("NW3 upper", nw3["rr_high"], "1.043860"),
    ):
        ok = float(value) == float(quoted) or f"{float(value):.6f}" == quoted
        print(f"{label} unrounded {value} quoted as {quoted}: {'ok' if ok else 'MISMATCH'}")
        if not ok:
            failures.append(f"{label} unrounded quotation mismatch")

    core = list(csv.DictReader(CORE.open(encoding="utf-8-sig")))
    min_q = min(float(r["q_value_core_bh"]) for r in core)
    print(f"minimum core BH q = {min_q:.6f} over {len(core)} contrasts: "
          f"{'ok' if min_q > 0.19 and len(core) == 12 else 'MISMATCH'}\n")
    if not (min_q > 0.19 and len(core) == 12):
        failures.append("core q-value family does not match the reported twelve contrasts above 0.19")

    print("== forbidden phrases and internal process terms ==")
    hits = [f for f in FORBIDDEN if f.lower() in prose.lower()]
    print("hits:", hits or "none")
    if hits:
        failures.append(f"forbidden phrases present: {hits}")

    print()
    if failures:
        for f in failures:
            print("FAIL:", f)
        return 1
    print("PASS: all provenance, estimate, and register checks succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
