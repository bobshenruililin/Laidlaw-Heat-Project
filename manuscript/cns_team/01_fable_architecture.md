# Paper architecture and remaining referee-kill list — Fable (senior scientist / methods editor)

**Date:** 15 August 2026. **Mode:** Ship.
**Scope:** architecture only. Opus writes CNS-register prose from this; Sol maps the supplement. This file does not edit `Heat_CVD_Manuscript_live_update.md`.
**Rails observed:** no new numbers (every scientific numeral below traces to `manuscript/live_collaborative/claim_ledger.md`; word counts and occurrence counts are file statistics, not scientific quantities); no Gate 3 freeze; Hogan's weather paragraph stays verbatim; Stage 3 PDF and A0 poster stay byte-locked; no stroke coefficients; the health-econ Monte Carlo (`SYNTHETIC_THEORY`) stays out of the paper.
**Verified against the live file at commit `4828e34`:** the 13 August honesty pass is fully absorbed — "continuity" has zero occurrences, the pre-2020 CHD hot-night intervals are in Results and Discussion, the ladder-direction sentences are in Results and Discussion, the Conclusion is comparative, the single-station limitation is present, the Guo null carries its interval, and Introduction sentence one cites [9] alone.

---

## 1. Honest venue

Ranked: **(c) Lancet Planetary Health / Environmental Health Perspectives / International Journal of Epidemiology** — winnable; **(b) Nature Communications / PNAS as a methods paper** — not with this evidence; **(a) Nature / Science / Cell main journal** — not honest.

One paragraph why. A CNS main-journal paper requires a generalisable discovery; this dataset forbids one by its own arithmetic — all twelve core *q*-values exceed 0.19 (minimum 0.192), the model set was specified after the outcome series were available, the design is ecological and monthly in a single city, and the outcome has no recorded admission cause. Tier (b) requires a portable methods contribution; what we have is a project-specific calibration refusal (the 500-replicate M|D run failed its frozen gates: null Type I error 0.048–0.150, minimum coverage 0.840, maximum relative bias 32.8, maximum false-sign rate 0.808) plus a reporting discipline — valuable, but a negative feasibility result on one series does not carry Nature Communications or PNAS. Tier (c) is where this paper wins: a complete-panel, uncertainty-ladder, identification-explicit analysis of governed first-event aggregates is exactly what EHP and IJE publish well, and Lancet Planetary Health is the in-class reach because the Basagaña–Ballester aggregation framework [15,16] is that journal's own literature and our calibration refusal speaks directly to it. Expected outcome: EHP or IJE; LPH worth one submission if the team wants the reach.

**CNS register ≠ CNS venue.** The prose standard in `.cursor/skills/cns-writing/SKILL.md` is portable to any journal and should be applied in full. The evidence class is not portable. Write at CNS standard; submit to the venue the evidence supports. No repo note, cover letter, or meeting slide should say or imply CNS suitability (the claim ledger already lists "CNS-journal suitability" under *Not claimed*).

---

## 2. Paper thesis in one sentence

Under monthly aggregation, thermal-exposure definition and uncertainty construction — not effect size — decide what may be claimed: this paper reports the complete twelve-contrast panel, shows where the identifying variation actually lives (between winters for cold days, 141 of 145 in December–February; the post-2020 window for CHD hot nights), and declines every promotion the data cannot support, including recovery of daily coefficients from monthly sums.

That is what the paper is *about*. It is not a discovery headline about hot nights or cold days; the two leading estimates (CHD hot nights 1.022, 1.002–1.042; HF cold days 1.073, 1.006–1.144; both *q* = 0.192) are the worked example, not the thesis.

---

## 3. Title options

| # | Title | Class |
|---|---|---|
| T1 | *Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023* (current) | Descriptive; keep-current |
| T2 | *Aggregation-aware inference for monthly thermal exposures and first cardiac hospitalisation in Hong Kong, 2013–2023* | Methods-forward |
| T3 | *Monthly thermal-exposure definitions and uncertainty constructions yield discordant associations with first cardiac hospitalisation: Hong Kong, 2013–2023* | Identification-forward |

**Recommendation for the live Hogan file: T1, unchanged.** It is descriptive, claim-free, and already Hogan's; churn on his title buys nothing at tier (c), where descriptive titles are the norm. If Hogan himself wants the cohort visible at first glance, the completion is "… diagnosis among people with type 2 diabetes or hypertension in Hong Kong, 2013–2023" — his call, not ours.

**Recommendation for a methods journal: T2.** The stale repo draft (`manuscript/chd_hf_thermal_associations_2013_2023.md`) already carries a version of it; T2 is that title cleaned of internal vocabulary. T3 is defensible (the discordance claim is supported by the ladder and the panel) but reads as a result-title on a paper whose Conclusion refuses protected results; hold it in reserve.

---

## 4. Figure architecture

Main text: three figures. Supplement: three figures. No new model runs; every artefact already exists.

| Slot | Content | Action |
|---|---|---|
| Figure 1 | First-event depletion vs 35+ population | **Keep.** Carries the estimand argument no table carries. |
| Figure 2 | Cold-day year × month heatmap | **Keep.** The identification core for the only SE-concordant residual. |
| Figure 3 | Trend / depletion / COVID-phase sensitivity forest | **Promote** from `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`. This does identification work: it shows the pre-2020 CHD hot-night interval crossing 1 in a display, not only in prose. *Render note for Sol:* the repo copy is `figure4_trend_depletion_sensitivity.svg`; export the PNG to the live file's figure path convention. |
| Supp. Fig. S1 | Residual ACF (current main Figure 3) | **Demote.** It displays two numbers (0.508, 0.146) that already appear in the Results text and the Limitations; a two-series ACF is a table row, not a main figure. |
| Supp. Fig. S2 | Twelve-contrast forest (`figure3_core_forest.svg`) | Optional; include. |
| Supp. Fig. S3 | SE-method ladder (`figure5_se_method_ladder.svg`) | Optional; include. |

Paste-ready captions (one sentence each):

> **Figure 1.** Indexed annual first-event counts (CHD 23,830 to 12,323; HF 4,336 to 2,296) against the general population aged 35 years or older (+17%), 2013–2023.

> **Figure 2.** Official cold days (T~min~ ≤ 12 °C) by year and month, Hong Kong Observatory Headquarters, 2013–2023: 141 of 145 days fell in December–February, so the cold-day contrast is identified from differences between winters.

> **Figure 3.** Count ratios for the twelve core contrasts across trend, window, and COVID-phase specifications (Newey–West lag-6 intervals): the pre-2020 CHD hot-night interval includes 1, while the pre-2020 HF cold-day association strengthens.

> **Supplementary Figure S1.** Pearson residual autocorrelation after month and trend adjustment; lag-1 autocorrelation is 0.508 for the CHD hot-night model and 0.146 for the HF cold-day model.

> **Supplementary Figure S2.** Forest plot of the twelve core count ratios under the days-in-month offset with Newey–West lag-6 intervals; all Benjamini–Hochberg *q*-values exceed 0.19.

> **Supplementary Figure S3.** Model-based, HC1, Newey–West lag-3, and Newey–West lag-6 intervals for the twelve core contrasts; no interval construction was selected by null exclusion.

---

## 5. What to cut from the live draft

Current section word counts (file statistics, measured 15 August): Abstract 388, Introduction 627, Methods 1,289, Results 1,312, Discussion 626, Conclusion 111, Strengths and limitations 275.

**Targets:** Abstract **≤ 300** (most tier-(c) journals cap structured abstracts there); Introduction **≤ 550**; Methods **≤ 1,200** (soft — methods honesty outranks the budget); Results **≤ 1,150**; Discussion **≤ 700**; Conclusion unchanged.

Specific cuts, in order of value:

1. **Flu numeral out of the Discussion.** 1.673 (1.249–2.243) is the largest CI-bearing effect anywhere in the paper, it is not from the analysis of record, and skimming reviewers quote large numbers regardless of the disclaimer around them. Keep the fact; move the numeral to Supplementary Table S7 (see §10). Paste-ready sentence in kill K1 below.
2. **The Abstract's ACF sentence.** Lag-1 autocorrelation (0.508 / 0.146) currently appears in the Abstract, the Results text, and the Limitations, and moves to the S1 caption — four tellings of two numbers. Cut it from the Abstract; that alone recovers roughly a tenth of the overage.
3. **Abstract Background compression.** Two sentences suffice: the thermal-profile shift and the question. The sentence contrasting earlier daily studies belongs in the Introduction, where it already lives.
4. **The unsourced Observatory-record superlative** in Results exposure context (kill K3 below) — cut or cite; either way it stops being a free-floating claim.
5. **Ceremony sweep for Opus:** the draft is already spare; the remaining candidates are restatements of the multiplicity refusal (it appears in the Abstract, after Table 2, after Table 3, in the Discussion opening, and in the Conclusion — five tellings; three carry information, keep Abstract + Table 2 + Discussion opening and let the Table 3 and Conclusion instances carry only their new content). Do not cut any refusal outright; consolidate repetitions.

---

## 6. Remaining referee kills after the 13 August pass

Verified status of the 13 August items first, so nobody re-fixes fixed things:

- **K-fixed-1. Ladder-direction rationale** ("model-based intervals are too narrow") — **already fixed**; the Results Table 3 paragraph and the Discussion now state that the Newey–West intervals are narrower and that the null exclusion "rests on the smaller robust variance estimate and is a reason for caution, not confirmation."
- **K-fixed-2. Asymmetric sensitivity reporting** — **already fixed**; pre-2020 CHD hot nights (1.011, 0.991–1.032) and COVID-phase adjustment (1.013, 0.994–1.033) are in the Results prose, and the Discussion says "not evident in the pre-2020 window."
- **K-fixed-3. "Continuity" vocabulary** — **already fixed in the live file** (zero occurrences; the core-panel definitional sentence is in Study design). Twenty-two occurrences remain in the stale repo draft — Sol's item, §10.
- **K-fixed-4. Superlative Conclusion** — **already fixed** ("more closely associated … than with the other thermal encodings examined").
- **K-fixed-5. Guo null without interval** — **already fixed** (−0.2%, 95% CI −1.2% to 0.7%).
- **K-fixed-6. [10] in Introduction sentence one** — **already fixed** ([9] alone).
- **K-fixed-7. Single-station limitation** — **already fixed** (present in Limitations).

Remaining kills, numbered:

**K1. Flu numeral placement (Discussion).** The archive influenza coefficient sits in the core paper's Discussion with only a disclaimer between it and a pull-quote. **PASTE-READY (replace the existing sentence):**
> "On the 121 months with influenza data, an archive model associated influenza activity with substantially higher CHD counts (Supplementary Table S7); that model is not an adjusted version of the core panel and does not adjust Table 2."

**K2. Uncited references [3] and [5].** The HKO 2017 and 2024 yearbooks appear in the reference list and are cited nowhere in the body. A copy editor will flag this at proof stage. References 1–8 are Hogan's block, so do not delete unilaterally. **Action (not a paste):** flag to Hogan with the exact sentence "References 3 and 5 are currently uncited in the body; prune or attach as you prefer." **Already fixed** for [6], which is now attached to the Results exposure-context sentence.

**K3. Unsourced Observatory-record superlative (Results, exposure context).** "The 2021 total was the highest annual number of hot nights in the Observatory record through the study window" carries no citation, and the claim ledger has no row for it. A referee who checks one exposure claim will check this one. **PASTE-READY (default): delete the sentence.** If Hogan confirms the 2021 yearbook [4] states a record, the alternative is to append "[4]" and keep it — his block, his call.

**K4. Abstract omits the pre-2020 null.** The Abstract reports the CHD hot-night NW6 interval and the ladder discordance but not that the association was absent before 2020 — a hostile referee will read the Results and call the Abstract selectively framed. **PASTE-READY (extend the existing Abstract Conclusions sentence):**
> "The CHD hot-night association depends on how uncertainty is computed and was not evident in the pre-2020 window."

**K5. Figure re-architecture text edits (Results).** With the §4 swap, two references change. **PASTE-READY (Results, residuals paragraph):** replace "(Figure 3)" with "(Supplementary Figure S1)". **PASTE-READY (Results, robustness paragraph, first sentence):**
> "Figure 3 shows the twelve contrasts across trend, window, and COVID-phase specifications; offset choice changed core count ratios only trivially."

**K6. Post-2020 entanglement made explicit (Discussion; optional but referee-preempting).** The Discussion states the pre-2020 null; it does not say why the full-window estimate should be read cautiously in one clause. **PASTE-READY (append to the "not evident in the pre-2020 window" sentence):**
> "The association is therefore confined to specifications that include 2020–2023, the years in which care patterns were most disrupted and, as the exposure context records, hot nights were most frequent."

**K7. Abstract over length.** 388 words against a ~300-word cap at every tier-(c) journal. Not a science kill, but desk editors bounce on it. Cuts specified in §5, items 2–3; Opus executes.

No other kills found. The estimand boundary (count ratio, not incidence), the DJF identification, the M|D refusal, the joint-model diagnostics framing, and the Goggins/Guo questions-not-magnitudes comparisons all survive hostile reading as written.

---

## 7. Must-say / must-not-say

**Abstract.**
- Must say: exploratory, specified after outcomes were available; all twelve *q* > 0.19; count ratios, not incidence-rate ratios; admission cause not recorded; ladder discordance for CHD hot nights; four-construction concordance but *q* = 0.192 for HF cold days; the pre-2020 absence of the CHD association (K4); the between-winter identification of cold days; the M|D method was tested in simulation and not applied to the health series.
- Must not say: any causal verb (caused, triggered, drove, demonstrated); "significant" as an adjective of importance; "Gate 3" or any internal process term; stroke; daily DLNM or any daily-lag language for our estimates; any comparison of 2.63 with 1.073 or of 3.1% with 1.022; "novel," "first to," "robust" as praise.

**Discussion.**
- Must say: the opening stays "the data do not support a protected differential thermal claim"; the ladder-direction caution (narrower robust intervals; null exclusion rests on the smaller robust variance); the pre-2020 null for CHD hot nights; Goggins 2017 and Guo 2024 compared as questions, not magnitudes; confounding by pollution, influenza, and humidity unresolved; the "what a protected claim would have required" paragraph stays.
- Must not say: mechanism claims (sleep, blood pressure, personal exposure were not measured — the draft already says so; do not soften it); that concordance across SE methods confers protection; that the joint-model 1.045 is a preferred estimate; that the M|D failure generalises beyond this series; any Gate 3, stroke, or daily-DLNM content; the flu numeral (K1); numerical equality or rescaling between literature daily estimates and our monthly ratios.

**Conclusion.**
- Must say: comparative phrasing only ("more closely associated … than with the other encodings examined"); neither association survived multiplicity correction; the CHD estimate depends on the treatment of uncertainty; the contribution is hypotheses plus an explicit account of what monthly aggregate counts cannot settle; better-denominated, more finely resolved data are required.
- Must not say: any superlative rank claim; any promotion of HF cold days to a finding; policy or clinical recommendations; future-work inflation ("this opens the door to…"); causal verbs; stroke; Gate 3.

---

## 8. What would make this a worse paper

1. **Promoting a primary.** Declaring HF cold days a finding because four SE constructions exclude 1 — concordance is not multiplicity protection, and the paper says so; contradicting its own spine is the fastest route to rejection with prejudice.
2. **Hiding the pre-2020 null.** Removing or burying the CHD hot-night 1.011 (0.991–1.032) sensitivity would turn an honest identification statement into a discoverable omission; a referee with the release tables finds it in minutes.
3. **Claiming CNS discovery.** Any framing of the panel as a discovery about nighttime heat converts a defensible tier-(c) paper into an undefendable tier-(a) submission and burns the team's credibility with the exact reviewers who will see the resubmission.
4. **Letting the synthetic in.** The health-econ Monte Carlo (HE-01, ς = −0.438) is `SYNTHETIC_THEORY`; one synthetic numeral in a results section poisons every real numeral in the paper.
5. **Renaming count ratios as incidence,** adding stroke content, choosing a single interval construction after seeing which excludes 1, or rewriting Hogan's weather paragraph — each violates a boundary the draft currently keeps and each is independently fatal under review.

---

## 9. Opus instructions (section-level constraints)

- Produce paste-ready blocks for Bob following the `LIVE_DOC_EDITS.md` conventions; do not edit `Heat_CVD_Manuscript_live_update.md` directly, do not touch Hogan's weather paragraph, do not touch the Stage 3 PDF or the A0 poster.
- Every numeral must match a `claim_ledger.md` row exactly; no new numbers, no re-derived numbers, no new model runs.
- Apply `.cursor/skills/cns-writing/SKILL.md` in full, including its completion checklist, and Hogan's standard in `analysis_plan/writing_standards_hogan.md`: spare English, one claim per sentence, no ceremony.
- **Abstract:** cut to ≤ 300 words per §5 (drop the ACF sentence; compress Background to two sentences); add the K4 clause; keep both refusals (multiplicity; M|D not applied).
- **Introduction:** ≤ 550 words; keep the four-paragraph literature spine (Goggins history, Guo encoding, pollution context, Liu mortality boundary); no mechanism speculation; no new citations — reference-list changes go to Hogan as flags (K2), never as silent edits to his block [1–8].
- **Methods:** leave the weather paragraph byte-identical; keep the exploratory declaration and the core-panel definitional sentence; keep the M|D refusal paragraph intact.
- **Results:** execute the K5 figure-reference edits and the K3 deletion (pending Hogan on the [4] alternative); keep the symmetric pre-2020 / COVID-phase prose and the unrounded NW3 bound (1.000253–1.043860) exactly as written.
- **Discussion:** ≤ 700 words; keep the ladder-direction caution sentence verbatim; execute K1 (flu numeral out) and optionally K6; keep the "what a protected claim would have required" paragraph.
- **Conclusion:** comparative only; no additions beyond register polish.
- Consolidate the five tellings of the multiplicity refusal to three per §5 item 5; do not delete the refusal anywhere it carries new content.
- Forbidden everywhere: causal verbs, Gate 3, stroke, daily DLNM claims, 2.63-vs-1.073, 3.1%-vs-1.022, HE-01 / ς numerals, HM/CM provisional estimates, "continuity."

---

## 10. Sol instructions (supplement map; repo cleanup; journal-target honesty)

**Supplement map** (every item exists; sources are the ledger's source column; no new model runs):

| Item | Content | Existing source |
|---|---|---|
| Fig. S1 | Residual ACF (demoted main Fig. 3) | `figures/live_identification/figure_C_residual_acf.png` + `*_pathway_residual_acf.csv` |
| Fig. S2 | Twelve-contrast forest | `outputs/release_chd_hf/figures/figure3_core_forest.svg` |
| Fig. S3 | SE-method ladder | `outputs/release_chd_hf/figures/figure5_se_method_ladder.svg` |
| Table S1 | Full 48-row uncertainty ladder | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` |
| Table S2 | Trend / depletion / COVID-phase sensitivity | `outputs/tables/cvd_trend_depletion_sensitivity.csv` |
| Table S3 | Lag-0/1/2 sensitivity | `outputs/tables/cvd_lag_sensitivity.csv` |
| Table S4 | Influence (Cook's distance) sensitivity | `outputs/tables/cvd_influence_sensitivity.csv` |
| Table S5 | VIF and Ljung–Box diagnostics | `cvd_exposure_vif.csv`; `*_pathway_core_diagnostics.csv` |
| Table S6 | M\|D calibration gate summary | `md_calibration_gate_summary.csv` |
| Table S7 | Archive influenza model (receives the 1.673, 1.249–2.243 numeral from K1), labelled **not core-adjusted**, 121 months | `combined_pathway_panel_estimates.csv` (P14) |
| Table S8 | COVID-phase definitions | Methods text; no computation |

**Figure logistics.** Export `figure4_trend_depletion_sensitivity.svg` to PNG for the live file's path convention (the brief and the 13 August critique both name the `.png`; only the `.svg` is in the repo). Separately, the live file references `figures/live_identification/*.png`, and that directory is not in the repo — confirm where the rendered PNGs live and either commit them or record their location in `outputs/live_identification/README.md` so the live file's image links resolve for every collaborator.

**Repo-draft "continuity" cleanup.** `manuscript/chd_hf_thermal_associations_2013_2023.md` still contains 22 occurrences of "continuity," a stale Table 3/Table 4/Figure 5 numbering scheme, and an Abstract that predates the honesty pass. Do not paste any of it into Hogan's file. Either (i) sweep continuity → core with the same definitional sentence the live file uses and re-align its numbers to the ledger, or (ii) add a superseded-by banner at the top pointing to `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` and freeze it. Option (ii) is cheaper and safer unless the methods-journal track (title T2) is activated, in which case that file becomes the T2 vehicle and needs the full sweep.

**Journal-target honesty.** Target notes, cover-letter drafts, and any repo planning file must name the §1 tier-(c) class and must not claim or imply CNS suitability. The supplement must contain no `SYNTHETIC_THEORY` material (the uncommitted `outputs/health_econ/` stays out), no stroke placeholders, no HM/CM provisional estimates, and no Gate language. Where a supplement caption describes the M|D failure, keep the live file's boundary sentence: the refusal is specific to this series and implementation, not a general verdict on the Basagaña–Ballester method.

---

*Residue: this file. Next step in-repo: Opus drafts the paste blocks against §§5–7 and 9; Sol executes §10; Bob carries K2 and the K3 alternative to Hogan.*
