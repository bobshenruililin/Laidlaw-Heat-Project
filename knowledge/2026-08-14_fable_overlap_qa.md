# Fable — overlap QA — 14 August 2026

**Mode:** Decide. Kimi k3 is not launchable in this environment; Fable is the layout auditor of record for this pass.
**Provenance:** `REAL_PUBLIC` exposure pages and figures only. No health numbers appear here or on the audited pages. No email sent. Nothing here touches Hogan's weather paragraph, form 2a, or Gate 3.

**Audited state:** working tree on `cursor/hogan-identification-paste-1754` after the SVG fix — `docs/id/index.html`, `docs/id/era5_reliability_given_hko_web.svg`, `figures/identification_lab/era5_reliability_given_hko.svg`, `figures/live_identification/figure_D_hot_night_identification.svg` — against the four screenshots `id_lab_desktop_after_svg_fix.png`, `id_lab_mobile_after_svg_fix.png`, `era5_reliability_curve.png`, `figure_D_hot_nights_paper.png`. The eight rules are §4 of [`2026-08-14_fable_research_contribution.md`](2026-08-14_fable_research_contribution.md).

---

## 1. Pass / fail per rule

| # | Rule | Verdict | Evidence |
|---|---|---|---|
| 1 | Flow text one column, `max-width: 68ch`; charts are block-level `<figure>` siblings | **Pass** | `.lede`, `.prose`, `figcaption`/`.caption` all carry `max-width: 68ch`; every chart sits in its own `<figure>`; nothing is floated. Confirmed visually at both widths. |
| 2 | `viewBox` + `preserveAspectRatio="xMidYMid meet"`, CSS `width: 100%; height: auto`, no fixed pixel attributes | **Pass** | All three SVGs declare `viewBox` (920×480, 920×480, 920×520) and `preserveAspectRatio="xMidYMid meet"` with no `width`/`height` attributes; the page sets `figure img, figure svg { width: 100%; height: auto; }`. |
| 3 | Reserved label margins inside the viewBox; no `overflow: visible` rescue | **Pass** | Web curve reserves left 64 / top 28 / right 28 / bottom 56 user units; every tick and tick label sits inside those bands; marks are clipped to the plot rect via `clipPath`, not rescued with `overflow: visible`. Same construction in both paper SVGs. Cosmetic note in §2 on edge-marker half-clipping. |
| 4 | Titles, captions, legends are HTML, not SVG `<text>` | **Pass (page)** | On `docs/id/` the titles are `<h2>`, captions are `<figcaption>`/`.caption`, the legend is a flex `.legend` div, and the web SVG contains axis ticks only. The two paper SVGs carry their own SVG-text title/subtitle/footer by design — they are standalone manuscript figures, and their text sits in reserved bands (≥18 user units clear of the plot), so nothing collides. |
| 5 | Absolutely positioned annotations only inside a `position: relative` wrapper | **Pass** | Trivially: the stylesheet contains no `position: absolute` at all. Every annotation, including the bin readout, is in normal flow under the figure. |
| 6 | In-chart labels collision-checked with `getBBox()`; nudge then drop | **Pass by construction** | The web curve has zero in-plot labels — bin rates went to the HTML chips readout (`#binReadout`), exactly the "drop the label, let the interaction carry it" branch. Figure D's only in-plot text is the cell's own value (≤2 characters, 10-unit type, centred in a 63.7×30.2 cell, fill switched at v ≥ 12); empty cells get no label. Static generation means no runtime `getBBox()`, and nothing remains that could collide. |
| 7 | `figure { margin-block: 2.5rem; }`; minimum 12 px SVG type; no text within 8 px of a mark | **Fail (type floor)** | `margin-block: 2.5rem` is present and the 8 px clearance holds everywhere I measured. But all three SVGs set tick/label type at 10–11 user units. Because SVG type scales with the viewBox, the web curve's ticks render ≈10.5 px at 1280 and ≈3.5 px at 360 — visibly illegible in the mobile screenshot. Under the 12 px floor at every tested width. |
| 8 | Test at 360 and 1280; horizontal room via `overflow-x: auto` on the figure, never the page | **Pass** | Both screenshots exist and show no page-level horizontal scroll. `.heatwrap` and `.tablewrap` carry `overflow-x: auto` with 640 px min-widths; the mobile screenshot shows the heatmap scrolling inside its wrapper. (The mobile capture ends before the two tables; the CSS mechanism is the same one visibly working for the heatmap.) |

## 2. Remaining overlap

- **Text on points:** none. Bin rates are reported only in the HTML readout under the figure; the plot carries markers and the polyline only.
- **Caption on cells:** none. Figure D's footer caption sits at y = 508, below the last row (ends 438), month labels (456), and bracket (468–482); the HTML heatmap's captions are flow elements outside the grid.
- **28°C label on the curve:** gone. Both curve SVGs keep only the dashed rule at the 28°C x-position; "28°C" appears solely as an x-axis tick in the reserved bottom margin, and the "official 28°C cut (dashed)" entry lives in the HTML flex legend.
- **Always-on bracket on month names:** clear. In the HTML heatmap the bracket is its own grid row below the cells; in paper Figure D the bracket line sits at y = 468 against month-label baselines at y = 456, ~8–9 px below the descenders — separated in the render.
- **Table overflow:** contained. Both tables sit in `.tablewrap { overflow-x: auto; }` with `min-width: 640px`, so at 360 px they scroll inside the figure, not the page.
- **Cosmetic, not overlap:** markers whose centres sit exactly on the plot edge (the 0% baseline points and the 100% point at cy = clip-top) lose half the circle to the `clipPath`. Visually they read as half-dots on the axis; acceptable, but enlarging the clip rect by one marker radius would finish it.

## 3. Is the reliability chart rendering?

**Yes.** The `<img>` now points at `./era5_reliability_given_hko_web.svg`, the file exists inside `docs/id/`, and the desktop screenshot shows the curve rendering inline with its HTML legend and chips. One deployment caveat: at audit time that web SVG was **untracked** in git (`??` in status). It renders locally, but the 404 returns on the published page unless the file is committed with the rest of the fix.

## 4. Verdict

One mechanical fix still required, then ship: regenerate the three SVGs with the type floor respected — axis ticks ≥16 user units (Figure D cell values ≥14) and, per rule 8, give the reliability `<img>` the same 640 px min-width `overflow-x: auto` wrapper the heatmap already uses so those units land at ≥12 px on a 360 px screen — and commit the untracked web SVG so the fix survives deploy.

**Applied the same day:** script 60 now emits 16-unit axis ticks and 14-unit cell values; the reliability `<img>` sits in `.heatwrap` with `min-width: 640px`; `docs/id/era5_reliability_given_hko_web.svg` is a first-class page asset. Re-audit is a screenshot, not a new research object.

— Fable, IAS mentor, 14 August 2026
