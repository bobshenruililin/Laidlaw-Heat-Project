# Playbook 01 — Hogan definition lock

## Trigger

Run after the Tuesday weather meeting with Hogan, or after Hogan returns written corrections to that meeting record.

## Preconditions

- Actual notes or a completed [`hogan_tuesday_decision_sheet.md`](../hogan_tuesday_decision_sheet.md) are available.
- The recorder can distinguish Hogan’s words, team decisions, proposals, and unresolved questions.
- The current [`hot_cold_month_registry.yml`](../hot_cold_month_registry.yml), [`hot_cold_month_catalogue.md`](../hot_cold_month_catalogue.md), and [`canon_weather_definitions.md`](../../knowledge/canon_weather_definitions.md) have been read.
- A blank decision sheet is not evidence of a lock.

## Steps

1. Create `reports/meeting_debrief_YYYY-MM-DD.md`. Record: before → after; newly fixed choices; newly allowed work; work now out of scope; open questions with owner; and the next executable action.
2. Transcribe decisions in Hogan’s language. Mark unmade decisions `pending`; do not resolve them from the current registry defaults.
3. For `HM23`, record every agreed operator: station; season; calendar-day percentile reference period and method; comparison and tie rule; moving window; minimum duration; event-gap rule; missing-day tolerance; cross-month assignment; monthly-count reference distribution; monthly percentile method; and discrete tie handling.
4. Update `threshold_policy` and `definitions.HM23.parameters` in [`hot_cold_month_registry.yml`](../hot_cold_month_registry.yml). Change `implementation_status` only for decisions actually closed.
5. Reconcile the human-readable definition and status in [`hot_cold_month_catalogue.md`](../hot_cold_month_catalogue.md) and [`canon_weather_definitions.md`](../../knowledge/canon_weather_definitions.md). Preserve the credit split: Li et al. define the atmospheric event; Hogan proposed count by month → upper-tail month.
6. Record the agreed role of `HM23`, the cold starter, `CM05`, Roro’s four `HWD_*` siblings, station choice, and age-band visibility. A weather nomination is not the final Gate 3 freeze unless the team explicitly made that decision.
7. Update the relevant rows in [`assumption_ledger.md`](../assumption_ledger.md), [`decision_gates.md`](../decision_gates.md), and [`open_questions_log.md`](../../knowledge/open_questions_log.md). Preserve old decisions and dates when recording amendments.
8. Check whether the locked parameters are implemented. Rebuild exposure-only flags and selected-month audits only from code that matches the registry. If implementation is absent or differs, log the mismatch and keep the definition unimplemented.
9. Prepare a correction-friendly summary for Bob to circulate to Hogan and Roro. Do not mark disputed wording final until a correction or explicit acceptance is recorded.
10. Update [`PROJECT_STATE.md`](../PROJECT_STATE.md), [`CONTEXT_BOOTSTRAP.md`](../../knowledge/CONTEXT_BOOTSTRAP.md), the knowledge index, and a dated knowledge entry or arc compound with the decision and its provenance.

## Done when

- A dated debrief distinguishes decisions from open questions.
- `HM23` is either fully executable with all parameters recorded or explicitly remains pending.
- Registry, catalogue, canon, ledger, gates, state, and knowledge agree.
- The selected-month audit can be reproduced without hand edits.
- Hogan and Roro have a concise record to correct.

## Failure modes

- Treating the working option on the decision sheet as Hogan’s decision.
- Freezing only `p90` while leaving reference period, ties, gaps, or month mapping implicit.
- Calling a weather nomination the team’s Gate 3 headline freeze.
- Overwriting a source rule with a project adaptation or erasing contributor credit.
- Rebuilding flags from stale code after updating only prose.

## Which files to update

- `reports/meeting_debrief_YYYY-MM-DD.md`
- `analysis_plan/hot_cold_month_registry.yml`
- `analysis_plan/hot_cold_month_catalogue.md`
- `knowledge/canon_weather_definitions.md`
- `analysis_plan/assumption_ledger.md`
- `analysis_plan/decision_gates.md`
- `knowledge/open_questions_log.md`
- `analysis_plan/PROJECT_STATE.md`
- `knowledge/CONTEXT_BOOTSTRAP.md`
- `knowledge/INDEX.md`

## Claim boundaries

This playbook locks exposure definitions and roles. It creates no health finding. Exposure prevalence, selected months, and event counts are not stroke associations. Do not infer biological thresholds, genetic adaptation, or stroke effects from the weather lock.
