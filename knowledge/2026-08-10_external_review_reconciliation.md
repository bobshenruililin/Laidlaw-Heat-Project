# External review reconciliation — 10 August 2026

**Mode:** Explore → Decide  
**Architect:** GPT 5.6 Sol Max triage of an external review memo on the Stage 3 report and A0 poster.  
**Rule:** The memo contains useful critique and overclaim. Repo evidence governs.

## One-sentence verdict

The CNS gap is evidentiary, not stylistic; several “missing” analyses already exist; monthly first-hospitalisation data cannot identify daily harvesting; and the twelve-model panel must not be called pre-specified.

## Truth table (architect summary)

| Claim | Verdict |
|---|---|
| Specialty-journal prose; CNS gap is evidence/consequence | PARTLY |
| Data scarcity unmistakable and deliberate | PARTLY (imposed by delivery; transparency deliberate) |
| Scarcity visible structurally/architecturally/rhetorically | TRUE |
| M\|D failure can anchor a methods paper | PARTLY — expand first; do not generalise beyond this calibration |
| Climate–health data-contract Comment is CNS-adjacent | PARTLY — untested venue/authorship |
| Exact journal ceiling names | UNKNOWN |
| Rename “continuity uncertainty method” → NW6 | TRUE |
| Fix NW3 rounding (1.000–1.044 vs excludes 1) | TRUE |
| Cut hedging repetitions | PARTLY — keep claim boundaries |
| Add NB dispersion / spline df / ACF / ESS | PARTLY — ESS not defensible; others largely exist |
| Winter-only model resolves cold-day ID | PARTLY — diagnostic only; Dec–Feb support, not Nov–Apr |
| Pollution/humidity sensitivities | PARTLY — need same separate-exposure baseline |
| Population-offset sensitivity “missing” | FALSE — already complete as ecological sensitivity |
| Harvesting/displacement from monthly first events | FALSE as stated |
| Period effect-modification | PARTLY — pre-2020/COVID exist; formal interaction is new exploratory work |
| Multiplicity-under-dependence caveat | TRUE |
| Split Paper 1 / Paper 2 now | PARTLY — Paper 2 needs expansion first |
| Promote calibration refusal | TRUE with bounds |
| 3–6× timeline compression as fact | UNKNOWN — do not repeat |

## Rejected advice

1. Calling the twelve-model panel **pre-specified**.
2. Improvising an **effective sample size**.
3. Labelling monthly lag attenuation as **harvesting**.
4. Claiming the Basagaña–Ballester method fails **in general**.
5. Announcing journal ceilings or two papers before human gates.

## Accepted immediate fixes (P0)

1. Stage 3 report: name Newey–West lag 6; print NW3 as 1.0003–1.0439; state exclusion only unrounded.
2. State `ns(time, 4)` and residual ACF once where useful.
3. Honest F1.1/F1.2 amendment timing.
4. Manuscript: one BH dependence caveat.
5. Supplement: verified theta / Pearson dispersion for leading models; no ESS.
6. Public cold-day identification audit (done): `reports/cold_day_identification_audit.md`.

## Completed numerical and methods audits

- The CHD hot-night NW3 discrepancy was confined to the Stage 3 report. The
  exact interval is 1.000253–1.043860 (displayed as 1.0003–1.0439); the poster's
  existing NW3 wording is correct and remains unchanged.
- Population-offset and pre-2020 sensitivity analyses already exist in the
  released robustness materials. They are not missing-analysis requests.
- Effective sample size was rejected because no defensible ESS calculation is
  available for this model and dependence structure.
- Official cold-day support is concentrated in December–February. If a future
  governed winter-window sensitivity is fitted, December–February is preferred
  to November–April; restriction is not an identification cure.
- The F1.1 500-replicate run failed admission criteria. F1.2 was a post-run
  re-summary of the same fits under unchanged numerical thresholds and
  worst-cell rules; admission remained fail.

## Public cold-day audit headline

Official cold days in 2013–2023 Headquarters data concentrate in Dec–Feb (sparse March; zero Apr–Nov). After `factor(month)+ns(time,4)`, residual cold-day variance remains, especially in Dec–Feb. A winter-only health model is deferred until the governed panel is restored; Nov–Apr is a weak window here.

## Sensitivity scout (Sol-commanded)

Population-offset, pre-2020/COVID, lag, and core BH multiplicity already have continuity-aligned released results. Pollution, humidity, and influenza covariates exist publicly, but continuity-aligned coefficients require the absent governed CHD/HF panel. Temperature–AH residual correlation remains high after season/trend removal; ozone may mediate hot-sunny pathways. Monthly lags are not harvesting. Report only released continuity sensitivities from this checkout; do not promote legacy P11/P12/P14 as adjusted continuity estimates.

## M|D methods-paper audit (Sol-commanded)

**Verdict: EXPAND FIRST.** Current work justifies withholding real M|D coefficients under this project-specific calibration. It does not yet support a standalone methods paper or a claim that Basagaña–Ballester fails generally. Keep calibration in the supplement until implementation validity is separated from nuisance misspecification and aggregation information loss. Exact Stage 3 / manuscript prose should say F1.2 was a post-run re-summarisation of F1.1 fits, not a gate frozen before the 500-replicate run.

## Strategic learning kept

- Evidence ceiling = outcome grain + event semantics + missing risk set + post-outcome timing.
- Positive contribution = aggregation-aware inference under a constrained contract, not radical transparency alone.
- Next delivery must change the estimand and freeze contrasts before inspection.

## Related artifacts

- Stage 3 report: `reports/laidlaw_stage3/laidlaw_research_report_2026.md`
- Poster: `reports/poster/Laidlaw_Stage3_A0_portrait.tex`
- Cold-day audit: `reports/cold_day_identification_audit.md`
- Final protocol: `analysis_plan/final_reanalysis_protocol_2026-08-10.md`
- M\|D decision: `outputs/calibration_md/md_calibration_f1_2_decision_report.md`
