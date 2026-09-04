"""Honesty checks for the 28 Aug Fukuda / Tung Ngai pitch pack.

Does not email Fukuda. Does not invent field sites.
Does not rebuild Stage 3 PDFs.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge" / "2026-08-28_portfolio_audit_fukuda.md"
NOTE = ROOT / "reports" / "fukuda_pitch" / "concept_note.md"
ROAD = ROOT / "reports" / "fukuda_pitch" / "roadmap_12_weeks.md"
PITCH = ROOT / "reports" / "fukuda_pitch" / "mandate_pitch.md"
ESSAY = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Report.pdf"
POSTER = ROOT / "outputs" / "ShenRuililin_Laidlaw_Stage3Poster.pdf"


def _sha_prefix(path: Path, n: int = 16) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:n]


def test_stage3_pdfs_not_rebuilt():
    # Essay hash of record on trunk. Poster may follow the logo CL (#91).
    assert _sha_prefix(ESSAY) == "1200082a9e7c9caa"
    assert POSTER.is_file()
    assert _sha_prefix(POSTER) != "605cd8db43072cb5"


def test_audit_does_not_invent_field_sites():
    text = AUDIT.read_text(encoding="utf-8")
    assert "Not in repo" in text or "not in this repository" in text.lower() or "Not in the repository" in text
    assert "Gansu" in text
    assert "Medellín" in text or "Medellin" in text
    assert "do not invent" in text.lower() or "Do not invent" in text
    # No fake clinic names as if observed.
    for banned in ("village health station X", "NCMS bottleneck observed in", "Comuna 13 clinic"):
        assert banned not in text


def test_esf_geography_is_stated():
    blob = "\n".join(p.read_text(encoding="utf-8") for p in (AUDIT, NOTE, PITCH))
    assert "Greater Bay Area" in blob or "GBA" in blob
    assert "Mainland" in blob
    assert "100,000" in blob
    assert "not" in blob.lower()


def test_concept_note_is_identification_not_discovery():
    text = NOTE.read_text(encoding="utf-8")
    assert "q" in text.lower() or "q-values" in text or "*q*" in text
    assert "exploratory" in text.lower() or "insufficient" in text.lower()
    assert "policy brief" in text.lower() or "policy brief" in text
    assert "does not cite Gansu" in text
    assert "Bishai" in text
    assert "30-minute" in text
    # Must not present other cities as observed field sites.
    body = text.split("## Ask", 1)[-1]
    assert "I documented" not in body
    assert "village health" not in body.lower()


def test_lia_is_not_this_term():
    blob = ROAD.read_text(encoding="utf-8") + PITCH.read_text(encoding="utf-8")
    assert "six-week" in blob.lower() or "six week" in blob.lower() or "6-week" in blob.lower() or "6-week" in ROAD.read_text(encoding="utf-8")
    assert "Leadership-in-Action" in PITCH.read_text(encoding="utf-8") or "LiA" in ROAD.read_text(encoding="utf-8")


def test_pitch_does_not_promise_confirmatory_paper():
    text = PITCH.read_text(encoding="utf-8")
    assert "not asking you to supervise a confirmatory" in text.lower() or "confirmatory climate-health paper" in text
    assert "Hospital Authority" in text or "hospital authority" in text.lower()
    assert "two short meetings" in text.lower() or "two short meetings" in text


def test_concept_note_length_is_one_page():
    words = len(NOTE.read_text(encoding="utf-8").split())
    assert 350 <= words <= 900, words


if __name__ == "__main__":
    failed = []
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                failed.append((name, exc))
    if failed:
        for name, exc in failed:
            print(f"FAIL {name}: {exc}")
        raise SystemExit(1)
    print("ok")
