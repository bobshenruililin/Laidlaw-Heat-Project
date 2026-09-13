# COVID-period development track (wording authority for the candidate article)

**Audience:** Bob, then Sol/Astra. **Not** a send to Hogan until Bob pastes. **Not** Stage 3.

Hogan (10 September 2026) asked to change the angle from thermal extremes to the pre- vs
post-COVID contrast, and to use thermal extremes to say weather is not why the period
difference appears.

**This folder is where that candidate article is written.** Playbook 99
([`../../reports/incident_2026-09-10_scientific_angle_covid.md`](../../reports/incident_2026-09-10_scientific_angle_covid.md))
opened it for exactly that purpose and said not to rewrite
[`../live_collaborative/`](../live_collaborative/) in place. The live folder was rewritten in
place anyway on 10 September, which produced two authorities and one confused article; the
independent review in [`INDEPENDENT_REVIEW.md`](INDEPENDENT_REVIEW.md) records that
diagnosis. The 12 September repair rebuilt the draft here and left `live_collaborative/`
and the thermal archive untouched.

| Object | Where | Status |
|---|---|---|
| Candidate wording authority | [`Manuscript_covid_period_draft.md`](Manuscript_covid_period_draft.md) | Edit here |
| Hogan paste target | [`../live_collaborative/Heat_CVD_Manuscript_live_update.md`](../live_collaborative/Heat_CVD_Manuscript_live_update.md) | Do not edit; Bob pastes when he chooses |
| Thermal predecessor | [`../archive/thermal_extremes_2026-08/`](../archive/thermal_extremes_2026-08/) | Heritage; byte-locked |

Confirmatory freeze has not been declared. Agents did not paste into or send Hogan's shared
Word file.

## Rails

- Same extract: territory-month CHD/HF first hospitalisation among T2D/HTN, Hong Kong,
  January 2013–December 2023 (132 months). Admission cause absent. Stroke not delivered.
- Estimand class remains a negative-binomial **count ratio** with calendar-month factors,
  `ns(time, 4)`, days-in-month offset. Not TWFE. Not incidence.
- The nested window is January 2013–December 2019 (84 months), **contained in** the 132.
  It is not a fitted pre/post effect, and interval overlap is not a test of a window
  difference. There is **no** post-only 48-month Model 1 table on file.
- Hogan's HKO paragraph is **verbatim**, including the averaging sentence.
- `I(count/5)` is a reporting scale, not a consecutive spell.
- Gate 3 is **open**. This folder does not freeze a confirmatory primary.
- Do not write "health improved." Window-dependent count ratios and falling first-event
  totals are different objects from physiology.
- Playbook 08 synthetic lab output is **not** a result in the scientific body. Methods may
  warn, labelled SYNTHETIC, without quoting lab coefficients as Hong Kong estimates.

## Files

| File | Role |
|---|---|
| [`Manuscript_covid_period_draft.md`](Manuscript_covid_period_draft.md) | Candidate IMRD; the scientific object |
| [`INDEPENDENT_REVIEW.md`](INDEPENDENT_REVIEW.md) | August vs 10 September rewrite vs this draft; diagnosis, then 13 September hostile-read FIXes |
| [`claim_ledger.yml`](claim_ledger.yml) | Every numeral → existing CSV or parked live file; reference, figure, and print bindings |
| [`Heat_CVD_Manuscript_covid_period.docx`](Heat_CVD_Manuscript_covid_period.docx) | Word view, built by [`../../scripts/78_covid_period_manuscript_docx.py`](../../scripts/78_covid_period_manuscript_docx.py) |
| [`Heat_CVD_Manuscript_covid_period.pdf`](Heat_CVD_Manuscript_covid_period.pdf) | Print view from the same builder |
| [`PRINT_PAGE_MAP.md`](PRINT_PAGE_MAP.md) | Page-by-page fill map and the float contract |
| [`../../analysis_plan/prompts/GOAL_covid_period_astra_hostile_read.md`](../../analysis_plan/prompts/GOAL_covid_period_astra_hostile_read.md) | Paste-ready hostile-read prompt for after this repair |
| [`../../analysis_plan/covid_period/fable_gates_2026-09-10.md`](../../analysis_plan/covid_period/fable_gates_2026-09-10.md) | Two Fable 5.1 keep/cut gates |
| [`../../analysis_plan/covid_period/night_shift_checkpoint_2026-09-10.md`](../../analysis_plan/covid_period/night_shift_checkpoint_2026-09-10.md) | Killed-paradigm checkpoint |
| [`../archive/thermal_extremes_2026-08/`](../archive/thermal_extremes_2026-08/) | Parked thermal paper |

## Rebuild and check

```bash
python3 scripts/78_covid_period_manuscript_docx.py   # Word, PDF, page map
python3 scripts/79_covid_period_rails_checks.py      # ledger, citations, rails, page map
python3 -m pytest tests/test_covid_period_imrd_repair.py tests/test_covid_period_redirection_2026.py
```

Do **not** run `scripts/77_hogan_20260910_live_docx.py` for this track: it rebuilds the live
Hogan Word and PDF and forces a page break after every table and figure.

## Next human step

Hogan confirms whether "improved" meant point-estimate attenuation, the count trajectory, or
physiology. Bishai decides whether this candidate may replace thermal extremes as the journal
primary and whether to open a new governed extract. Bob pastes the Astra hostile-read prompt
after this repair; no agent consults Astra on his behalf. A 13 September in-repo hostile read
already applied the FIX list in [`INDEPENDENT_REVIEW.md`](INDEPENDENT_REVIEW.md) §8.
