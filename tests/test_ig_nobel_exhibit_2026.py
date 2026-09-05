"""Kill-list and data-contract tests for the Ig Nobel mycelium exhibit."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "exhibits" / "ig_nobel_fruiting_body"
HTML = EX / "index.html"
DATA = EX / "js" / "data.js"
README = EX / "README.md"
SCRIPT = EX / "CEREMONY_60S.md"
TITLE_B = (
    "Hot nights rose. Cold days stayed. "
    "The first heart admission did not settle the argument."
)


def _hud() -> str:
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in (HTML, DATA, EX / "js" / "main.js", EX / "js" / "ceremony.js")
    )


def test_files_exist() -> None:
    assert HTML.is_file()
    assert DATA.is_file()
    assert (EX / "js" / "mycelium.js").is_file()
    assert (EX / "js" / "airplanes.js").is_file()
    assert README.is_file()
    assert SCRIPT.is_file()


def test_twelve_nodes_in_data() -> None:
    text = DATA.read_text(encoding="utf-8")
    assert "OUTCOMES" in text
    assert "EXPOSURES" in text
    assert text.count("Hot nights") >= 1
    assert "Tmean" in text and "Cold days" in text
    assert "NODES = OUTCOMES.flatMap" in text


def test_title_b_and_award() -> None:
    html = HTML.read_text(encoding="utf-8")
    assert TITLE_B in html
    assert "confirmatory mushroom still will not fruit" in html
    assert "every q exceeds 0.19" in html
    assert "Not an Ig Nobel submission" in html


def test_real_provenance_and_counts() -> None:
    data = DATA.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    assert 'PROVENANCE = "REAL"' in data
    assert "156,156" in html
    assert "29,681" in html
    assert "132" in html
    assert "0.19" in html
    assert "0.192" in html
    assert r"\log \mathrm{E}(Y_t)" in html


def test_1022_only_with_q() -> None:
    html = HTML.read_text(encoding="utf-8")
    assert "1.022" in html
    assert "0.192" in html
    assert "1.073" in html
    assert "1.113" in html
    assert "not twins" in html.lower()


def test_kill_list_on_hud() -> None:
    hud = _hud().lower()
    for banned in (
        "gate 3",
        "pipeline",
        "warnings work",
        "twin confirmatory",
        "admissions averted",
        "ioannou",
        "admissions rose",
    ):
        assert banned not in hud, banned
    assert re.search(r"\biq\b", hud) is None
    assert re.search(r"\bami\b", hud) is None
    assert "afterload" not in hud
    assert "overnight" not in hud


def test_weather_copy() -> None:
    html = HTML.read_text(encoding="utf-8").lower()
    assert "official hot nights increased" in html
    assert "official cold days persisted" in html
    assert "admissions rose" not in html


def test_chrome_not_science() -> None:
    html = HTML.read_text(encoding="utf-8")
    assert "fungi as chrome, not as data" in html
    readme = README.read_text(encoding="utf-8")
    assert "not a gate 3 freeze" in readme.lower()
    assert "unless he asks" in readme.lower()


def test_spoken_physiology_only_in_script() -> None:
    script = SCRIPT.read_text(encoding="utf-8")
    low = script.lower()
    assert "afterload" in low
    assert "overnight" in low
    assert "ami" in low
    assert "spoken only" in low


def test_2018_ruler_in_data() -> None:
    data = DATA.read_text(encoding="utf-8")
    assert "2018" in data
    assert "officialHotNights: 26" in data
    assert "daysInFiveNightSpells: 0" in data
    assert "DAILY_REPLICATES = 500" in data
