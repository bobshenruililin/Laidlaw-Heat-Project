# COVID-period journal track (candidate)

**Audience:** Bob and later Sol/Astra. **Not** a send to Hogan until Bob pastes. **Not** Stage 3.

Hogan (10 September 2026) asked to change the angle from thermal extremes to the pre- vs post-COVID contrast, and to use thermal extremes to say weather is not why the period difference appears.

This folder is the **candidate** Hogan-register article. Confirmatory freeze has not been declared. The thermal paper is parked at [`../archive/thermal_extremes_2026-08/`](../archive/thermal_extremes_2026-08/). Hogan’s shared Word remains the live collaborative file until Bob owns paste. Agents do not paste into that Word.

## Rails

- Same extract: territory-month CHD/HF first hospitalisation among T2D/HTN, Hong Kong, January 2013–December 2023 (132 months). Admission cause absent. Stroke not delivered.
- Estimand class remains a negative-binomial **count ratio** with calendar-month factors, `ns(time, 4)`, days-in-month offset. Not TWFE. Not incidence.
- Pre-2020 = January 2013–December 2019 (84 months). There is **no** post-only 48-month Model 1 table on file.
- Hogan’s HKO paragraph is **verbatim**.
- `I(count/5)` is a reporting scale, not a consecutive spell.
- Gate 3 is **open**. This folder does not freeze a confirmatory primary.
- Do not write “health improved.” Window-dependent count ratios and falling first-event totals are different objects from physiology.
- Playbook 08 synthetic lab output is **not** a result in the scientific body. Methods may warn, labelled SYNTHETIC, without quoting lab coefficients as Hong Kong estimates.

## Files

| File | Role |
|---|---|
| [`Manuscript_covid_period_draft.md`](Manuscript_covid_period_draft.md) | Hogan-register IMRD (scientific body: no Gate jargon) |
| [`Heat_CVD_Manuscript_covid_period.docx`](Heat_CVD_Manuscript_covid_period.docx) | Word export (`scripts/74_covid_period_manuscript_docx.py`) |
| [`claim_ledger.yml`](claim_ledger.yml) | Every numeral → existing CSV or parked live file |
| [`../../analysis_plan/covid_period/fable_gates_2026-09-10.md`](../../analysis_plan/covid_period/fable_gates_2026-09-10.md) | Two Fable 5.1 keep/cut gates |
| [`../../analysis_plan/covid_period/night_shift_checkpoint_2026-09-10.md`](../../analysis_plan/covid_period/night_shift_checkpoint_2026-09-10.md) | Killed-paradigm checkpoint |
| [`../archive/thermal_extremes_2026-08/`](../archive/thermal_extremes_2026-08/) | Parked thermal paper |

## Next human step

Bob confirms Hogan’s “improved” means CR attenuation (Figure 3), not raw counts and not labs. Bishai decides whether the journal paper may leave thermal as primary after Stage 3.
