# Fable — research contribution decision — 14 August 2026

**Mode:** Decide + Teach. One file; no code shipped at this milestone.
**Provenance:** everything cited is `REAL_PUBLIC` exposure work already in this repository (scripts 57–59, the threshold instrument, the monthly bridge). No HA rows, no coefficients, no Gate 3 movement, no frozen-PDF rebuild, no edit to Hogan's weather paragraph. The live paper stays on HKO.

Companions: [`2026-08-14_fable_ias_mentorship.md`](2026-08-14_fable_ias_mentorship.md), [`2026-08-14_two_instruments_one_field.md`](2026-08-14_two_instruments_one_field.md).

---

## 1. The research object

Name: **the identification profile** — one supplementary table, six rows (one per exposure), four columns: residual identifying share after month indicators; intensive/extensive split of that share; effective-rank family membership; single-instrument dependency (means corroborated by ERA5 at r = 0.986, or Headquarters-only).

Why: the paper already reports uncertainty — the Model/HC1/NW3/NW6 ladder and the q-values — but nowhere states *what variation identifies each contrast*, and this table is the one object that turns three overnight scripts into architecture rather than a fourth Leaflet.

It changes no estimate. It is Hogan-first, supplement-grade, and monthly-grain in everything it prints. It makes the null-ish hot-night interval interpretable — intensive variation inside an always-on summer, on one instrument — instead of decorative.

## 2. Daily grain: companion versus paper

Strict rule. The companion may hold any **exposure-only, public-source, day-level object**: daily flags from the two instruments, Jaccard-by-threshold curves, the fourteen-night scrubber, per-night temperature ledgers, the reliability curve of §3. Both series are `REAL_PUBLIC`; no health data may touch them.

The live monthly paper admits **no daily-grain number at all**: not 0.031, not 14/449, not 449-versus-17, not the reliability curve, and no daily exposure series feeding any health model — the clean-room monthly-outcome/daily-exposure method already failed 500-replicate F1.2 calibration, so no real daily coefficient is admitted. The paper may describe how flags are *constructed* from daily HKO records (definition, not inference) and may carry at most the two parked monthly-grain limitation sentences, each pasted only after Hogan answers.

Test for a borderline object: if deleting every date from it changes nothing, it is monthly and may be proposed; if the dates are load-bearing, it is companion-only.

## 3. The reliability curve

Proposal: P(ERA5 Tmin ≥ 28°C | HKO Tmin in bin), forward direction, matched days 2013–2023.

**Decision: yes — a legitimate exposure diagnostic, companion only, forward only.** It is a property of two fully observed instruments, not of days as exposure; HKO is complete over the study window, so the curve recovers nothing the paper needs. It states in one line that the disagreement is not a threshold shift, which the shipped maximum Jaccard (0.471 at 26.3°C) suggests and script 59's missed ≥29°C station nights make concrete. Do not pre-state bin values; the script reports them.

It becomes a daily-recovery backdoor at exactly two moves, both forbidden: **inversion** — fitting P(HKO | ERA5) to impute Headquarters-style flags where HKO does not exist (PRD cells, peer cities, other decades) — and **correction** — using the curve as a measurement-error model to adjust any health coefficient. Forward and descriptive: diagnostic. Inverted or attached to outcomes: misconduct.

## 4. Layout law for interactive pages

Bob's complaint is real; the fix is mechanical. Eight rules, exposure pages only, no health overlays at any width:

1. Flow text in one column, `max-width: 68ch`; charts are block-level `<figure>` siblings, never floated beside or under text.
2. Every SVG declares `viewBox` and `preserveAspectRatio="xMidYMid meet"`, with CSS `width: 100%; height: auto`; no fixed pixel `width`/`height` attributes.
3. Reserve label space inside the viewBox with an explicit margin object (e.g. `{top:16, right:24, bottom:44, left:56}`); never draw ticks or axis titles outside it, and never rescue them with `overflow: visible` — enlarge the viewBox instead.
4. Titles, captions, and legends are HTML (`<figcaption>`, a flex legend), not SVG `<text>`: HTML reflows, SVG text does not.
5. Absolutely positioned annotations and tooltips live only inside a `position: relative` figure wrapper, with `pointer-events: none` and coordinates clamped to the wrapper's box.
6. In-chart SVG labels are collision-checked with `getBBox()` — nudge, then drop; when in doubt drop the label and let the tooltip carry it.
7. Fixed vertical rhythm: `figure { margin-block: 2.5rem; }`; minimum 12 px SVG type; no text within 8 px of a plotted mark.
8. Test at 360 px and 1280 px; anything needing horizontal room at 360 px gets `overflow-x: auto` on the figure, never on the page.

## 5. Unfinished honestly, versus misconduct

Parked and honest (not this milestone):

1. **Station replicates** — rerun script 59 against King's Park and Waglan records to split siting from instrument; exposure-only.
2. **Population-weighted lattice** — public gridded population over the PRD cells, asking where the marine-south hot-night mass sits relative to people; exposure-only.
3. **Year-shifted negative control** on the identification profile — shifted flags should collapse the identifying shares; diagnostic-only.

Misconduct here:

1. Refitting the CHD/HF panel on ERA5 or "calibrated" exposures and keeping whichever ladder moves q below 0.19.
2. Imputing daily flags via the inverted curve and attaching hospitalisation ratios anywhere.
3. Reporting 0.045 as measured attenuation of a health effect, or using effective rank 3.92 to re-open the multiplicity ledger after seeing results.

## 6. The bounce question for Bob

"Does the identification profile enter the live paper's supplement as one Hogan-first table — and if so, which single Discussion sentence does it license: the intensive-margin sentence, the single-instrument sentence, or neither yet?"

That is the milestone. Stop here.

— Fable, IAS mentor, 14 August 2026
