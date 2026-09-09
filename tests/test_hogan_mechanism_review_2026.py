"""Bob-only mechanism discussion brief: six papers, ~200 words each.

Do not restore the 500–1000-word seven-point cards. Bob rejected that PDF.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "reports" / "hogan_2026-09-04" / "mechanism_review"
REVIEW = PACK / "REVIEW.md"
PDF = PACK / "REVIEW.pdf"
FIGURES = PACK / "figures"
LIVE = ROOT / "manuscript" / "live_collaborative" / "Heat_CVD_Manuscript_live_update.md"
HOGAN_WX = "Meteorological data was obtained from the HKO."


def _strip_noise(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", _strip_noise(text)))


def _paper_bodies(md: str) -> list[str]:
    parts = re.split(r"(?=^## Paper )", md, flags=re.M)
    papers = []
    for part in parts:
        if not part.startswith("## Paper "):
            continue
        papers.append(re.split(r"(?=^## (?!Paper ))", part, flags=re.M)[0])
    return papers


class TestHoganMechanismReview(unittest.TestCase):
    def test_six_papers_are_human_length(self) -> None:
        md = REVIEW.read_text(encoding="utf-8")
        papers = _paper_bodies(md)
        self.assertEqual(len(papers), 6, [p.splitlines()[0] for p in papers])
        for body in papers:
            n = _word_count(body)
            self.assertGreaterEqual(n, 160, (body.splitlines()[0], n))
            self.assertLessEqual(n, 240, (body.splitlines()[0], n))
            self.assertIn("**The question.**", body)
            self.assertIn("**What they found.**", body)
            self.assertIn("**What our file has.**", body)
            self.assertIn("**What we do.**", body)
        self.assertNotIn("## Point ", md)
        self.assertNotIn("500–1000", md)
        self.assertNotIn('<div class="card', md)

    def test_discussion_map_is_first(self) -> None:
        md = REVIEW.read_text(encoding="utf-8")
        self.assertIn("What are we discussing?", md)
        self.assertIn("On the table", md)
        self.assertIn("**Keep**", md)
        self.assertIn("**Drop**", md)
        self.assertIn("**No**", md)
        self.assertIn("do not send this pdf to hogan", md.lower())
        self.assertIn("bob review only", md.lower())
        self.assertLess(md.find("# What are we discussing?"), md.find("## Paper 1."))

    def test_science_rails_in_brief(self) -> None:
        md = REVIEW.read_text(encoding="utf-8")
        self.assertIn("1.022", md)
        self.assertIn("1.073", md)
        self.assertIn("0.192", md)
        self.assertIn("26 official hot nights", md)
        self.assertIn("failing heart", md)
        self.assertIn("I(count/5)", md)
        self.assertNotIn("failing left ventricle", md.lower())
        self.assertNotIn("gate 3 is closed", md.lower())
        self.assertIn("admissions averted", md.lower())

    def test_live_file_still_has_old_discussion(self) -> None:
        live = LIVE.read_text(encoding="utf-8")
        self.assertIn("confinement study of seven men", live)
        self.assertIn(HOGAN_WX, live)

    def test_pdf_exists(self) -> None:
        self.assertTrue(PDF.is_file())
        self.assertGreater(PDF.stat().st_size, 80_000)
        self.assertEqual(PDF.read_bytes()[:4], b"%PDF")

    def test_figures_still_on_disk(self) -> None:
        for name in (
            "fig_nights_vs_spells.png",
            "fig_ioannou_mismatch.png",
            "fig_indoor_outdoor.png",
        ):
            self.assertTrue((FIGURES / name).is_file(), name)

    def test_readme_says_two_hundred_words(self) -> None:
        readme = (PACK / "README.md").read_text(encoding="utf-8")
        parent = (ROOT / "reports" / "hogan_2026-09-04" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("200 words", readme)
        self.assertNotIn("500–1000", readme)
        self.assertIn("200 words per paper", parent)
        self.assertNotIn("500–1000", parent)


if __name__ == "__main__":
    unittest.main()
