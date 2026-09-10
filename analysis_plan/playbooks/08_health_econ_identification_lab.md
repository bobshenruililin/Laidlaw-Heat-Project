# Playbook 08 — Health-economics identification lab

## Trigger

Run when Bob (or an agent under `/playbook-08-health-econ-lab`) wants **PhD-style** causal-inference, DUA-safe pipeline, or HTA *practice* on this repository — DAG pressure-tests, IV/RDD *teaching*, synthetic Monte Carlo, CEAC sketches — **without** putting any of it in the journal-track live manuscript.

This is **Explore**. Closed [PR 54](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/54) (`cursor/health-econ-night-engine-b75b`) is prior residue: SEW/RTE/ADR were escalation **statistics**, never findings. Do not revive that engine into `Heat_CVD_Manuscript_live_update.md`.

## Preconditions

- [`knowledge/CONTEXT_BOOTSTRAP.md`](../../knowledge/CONTEXT_BOOTSTRAP.md) and [`.cursorrules`](../../.cursorrules) have been read.
- The live wording authority is [`manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`](../../manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md). Hogan’s weather paragraph is already in that file.
- Gate 3 is **open**. This lab does not close it.
- Governed panels are **not** required and must **not** be opened. Use [`data_processed/samples/SYNTHETIC_chd_hf_schema.csv`](../../data_processed/samples/SYNTHETIC_chd_hf_schema.csv) (≤10 mock rows, `data_status = SYNTHETIC`) or other files under `data_processed/samples/`.
- Named Max seats (Fable 5 Max / Opus 5 Max / Sol 5.6 Max) may be unavailable. Use inherit `generalPurpose` auditors and the tripwire script. Unlimited tokens are not a licence to invent HA coefficients.

## Adapted stop rule

Return only when all three hold:

1. Every quantitative sentence from this lab is labelled `SYNTHETIC` or `SYNTHETIC_THEORY`.
2. The live collaborative manuscript, Hogan PDF builder, and Stage 3 essay **were not edited** by this playbook (unless Bob named a separate Ship for a *hypothesis sentence* that already exists in the live file).
3. No TWFE / Callaway / Medicaid / QALY paragraph was copied into Methods or Discussion.

## What this lab may do

| PhD-advice item | Allowed here | Forbidden |
|---|---|---|
| DAG / collider / bad-control review | Teach against **this** extract (season, COVID, care-seeking, diagnosed T2D/HTN cohort as a selected sample) | Claiming the DAG identifies a causal Medicaid-style effect |
| IV / RDD / placebo list | Critique *why they are not identified* on 132 months without a running variable or instrument | Inventing an instrument or donut-hole RDD |
| Robust staggered DiD | Only if Bob names a **future** policy extract with a treatment date | Defaulting this paper to Callaway & Sant'Anna |
| Clustered SEs | Explain why Newey–West lag-6 is the project ladder | Switching Table 2 to state-clustered OLS |
| Synthetic schema mocking | Write cleaning/estimation against the 8-row schema | Opening `*_analysis_panel.csv` |
| Markov / PSA / CEAC / tornado | Vectorized Monte Carlo on **synthetic costs/QALYs** under `analysis_plan/health_econ/` | Pasting CEA into the live Discussion |
| Quarto / LaTeX tables | `modelsummary` / `etable` on **synthetic** fits; Hogan builder stays the journal PDF path | Overwriting Hogan HKO sentences |

## Identification review prompt (this extract)

Use this, not a Medicaid expansion prompt:

> Review identification in `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`. The estimand is a within-calendar-month, year-to-year weather-anomaly count ratio for first recorded hospitalisation after first CHD/HF diagnosis in a T2D/HTN cohort, 132 months, days-in-month offset, `ns(time, 4)`. Staggered adoption is not the design. Critique confounders (season, trend, COVID care-seeking, humidity/rainfall as Model 2 — specified not fitted, flu coverage 121/132 months). Suggest three **falsification or placebo** checks that do not require undelivered stroke or person-time files. Do not recommend TWFE. Do not freeze Gate 3.

A worked DAG sketch lives in [`analysis_plan/health_econ/dag_this_extract.md`](../health_econ/dag_this_extract.md).

## Steps

1. Read the lab prompt [`analysis_plan/health_econ/identification_lab_prompt.txt`](../health_econ/identification_lab_prompt.txt) and the DAG sketch.
2. Bind code to the synthetic schema only. Refuse missing governed panels the same way `scripts/62_fit_hogan_model2_model3.py` does.
3. If running Monte Carlo or CEA, write under `analysis_plan/health_econ/` and `outputs/health_econ/` with `SYNTHETIC` in every table title. Do not start a parallel manuscript.
4. Pressure-test with inherit auditors (WORSE is allowed). Run `python3 scripts/71_objective_audit_tripwires.py` if any live-file edit was requested in a *different* playbook; this playbook should leave the live file untouched.
5. Deposit residue: dated note under `analysis_plan/health_econ/`, a `context_compound_log.md` row, and pointers in INDEX. Label dead ends dead.

## Done when

- A dated lab note exists under `analysis_plan/health_econ/`.
- Outputs are `SYNTHETIC`.
- Live manuscript, Hogan builder, and Stage 3 PDF hashes are unchanged **by this playbook**.
- Gate 3 remains OPEN.

## Failure modes

- Writing health-econ Monte Carlo or `SYNTHETIC_THEORY` into the journal-track live file (already a Playbook 05 failure mode).
- Defaulting to TWFE / Callaway because a generic PhD checklist said so.
- Opening HA panels “just to get column names” (names are in `final_model_helpers.R` and the synthetic schema).
- Treating closed PR 54 coefficients as real.

## Which files to update

- `analysis_plan/health_econ/lab_note_YYYY-MM-DD.md` (create when the lab is actually run)
- `analysis_plan/context_compound_log.md`
- Optional `outputs/health_econ/` synthetic artifacts
- 10 Sep 2026 run: `lab_note_2026-09-10.md`; `scripts/72_synthetic_utilisation_shock.py`; `scripts/73_synthetic_mnar_selection.py`
- Not `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`
- Not `manuscript/covid_period/Manuscript_covid_period_draft.md` as a findings dump
- Not `scripts/64_hogan_20260824_manuscript_docx.py` Hogan strings

## Claim boundaries

This playbook trains identification hygiene and DUA-safe engineering. It produces no CHD/HF finding, no QALY for Hong Kong, and no Gate 3 freeze.
