# Live manuscript — analysis-window sensitivity

This folder is the repository wording authority for the candidate journal
article. On 10 September 2026, Bob authorised an in-place rewrite around
analysis-window sensitivity during pandemic-era disruption. The rewrite does
not close Gate 3 and is not a tested pre/post effect.

The complete thermal-extremes object that preceded this rewrite is frozen at
[`../archive/thermal_extremes_2026-08/`](../archive/thermal_extremes_2026-08/),
including the exact Word, PDF, live folder, builder, and SHA-256 manifest.
Stage 3 outputs remain byte-locked.

## Authority and outputs

| File | Role |
|:--|:--|
| `Heat_CVD_Manuscript_live_update.md` | Scientific wording authority |
| `claim_ledger.md` | Human-readable claim map |
| `claim_ledger.yml` | Machine ledger for `scripts/50_audit_live_claim_ledger.py` |
| `supplement_live_track.md` | Assembled live supplement, including S1–S10 |
| `supplement_inventory.md` | Supplement numbering and provenance |
| `Heat_CVD_Manuscript_20260910_hogan.docx` | Current Hogan-format Word output |
| `Heat_CVD_Manuscript_20260910_hogan.pdf` | Current Hogan-format print output |

The dated 24 August Word/PDF remain in this folder for continuity and are also
copied byte-for-byte into the thermal archive. They are not the scientific
authority for the new angle.

## Scientific reading

- Outcome: monthly count of first hospitalisation after first CHD or HF
  diagnosis among people with T2D and/or HTN.
- Full window: January 2013–December 2023 (132 months).
- Nested window: January 2013–December 2019 (84 months).
- The two fits do not estimate a post-only effect or a period interaction.
- Official-day exposures use `I(count/5)` as a reporting scale, not consecutive
  duration.
- Model 1 remains the separate-exposure negative-binomial model with
  calendar-month factors, `ns(time, 4)`, and a days-in-month offset.
- The uncertainty ladder is Model / HC1 / Newey–West lag 3 / Newey–West lag 6.
- All twelve full-window Model 1 *q*-values exceed 0.19.
- Admission cause, still-at-risk person-time, laboratory data, infection,
  vaccination, serology, age strata, and stroke were not delivered.

## Hogan constraints

Hogan’s HKO paragraph remains verbatim, including:

> Meteorological data was obtained from the HKO.

and:

> All monthly data were derived by taking the average of daily data in each calendar month.

Bob owns any paste into Hogan’s shared Word. The repository output is a
candidate article, not an email attachment sent by an agent.

## Human-owned remainder

- Bishai: whether this candidate replaces thermal extremes as the journal
  primary; whether a new governed extract is in scope; IRB and dissemination.
- Hogan: what “improved” meant (point-estimate attenuation, count decline, or
  physiology).
- Roro, only after Bishai: outcome semantics, stroke, person-time, age bands,
  and any approved new extract.
- Team: authorship and Gate 3.

Prepared questions:
[`../../analysis_plan/covid_period/bishai_roro_metadata_decision_2026-09-10.md`](../../analysis_plan/covid_period/bishai_roro_metadata_decision_2026-09-10.md).
