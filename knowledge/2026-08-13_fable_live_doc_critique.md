# Fable live-doc critique — 13 August 2026

**Role:** senior-scientist / methods-editor pass on `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`, written as if Hogan, Roro, and Bishai will read it.
**Sources read:** the live draft, `claim_ledger.md`, `LIVE_DOC_EDITS.md`, the say/must-not-say map, the night-explore note, `table2_core_models.csv`, `table4_uncertainty_ladder.csv`, `table3_robustness_summary.csv`, `cvd_trend_depletion_sensitivity.csv`, `outputs/live_identification/README.md`, and the 12 August insights note.
**Rails observed:** no stroke coefficients, no Gate 3 freeze, no edit to the live file, no Hogan-weather change, no Author 2–4, all twelve core *q* > 0.19 stays. Every number below is `HA_APPROVED_AGGREGATE`, `REAL`, or a cited paper, and already exists in a paid table.
**Version note:** the Opus register pass merged into the draft while this critique was in progress. All quotes and findings below were re-verified against the post-merge text (commit `63d13d1`); every substantive target survives the merge.
**Marking:** replacement sentences are labelled **PASTE-READY** (safe for the live file as written) or **EXPLORE-ONLY** (needs a human nod or further checking).

---

## 0. Verdict

The draft is honest where most drafts lie: estimand, multiplicity, and refusals are stated plainly and repeatedly. It has two real problems that a careful reviewer will find in under an hour. First, the Discussion's justification for the Newey–West display is contradicted by the paper's own Table 3: for CHD hot nights the robust intervals are *narrower* than the model-based interval, so "model-based intervals are too narrow for that series" is backwards for the one contrast it defends. Second, sensitivity reporting is asymmetric: the paper quotes the HF cold-day pre-2020 strengthening with a full interval but hides, inside a bare point-estimate range, that the CHD hot-night association is null before 2020 and under COVID-phase adjustment. Both fixes use numbers we already paid for. Fix those two, kill the undefined word "continuity," and the paper is defensible.

---

## 1. Estimand honesty (count ratio, depletion, DJF)

**Count ratio vs incidence: good, with one slip.** The count-ratio/not-incidence boundary is stated in the Abstract, Study design, Denominators, and Discussion, and Figure 1 shows why the general-population denominator cannot rescue incidence. The slip is the Conclusion: "the **largest positive thermal association** was with hot nights for CHD first hospitalisations and with cold days for HF first hospitalisations." That is a superlative rank claim across an unprotected twelve-contrast panel; ranking is exactly what *q* > 0.19 says we cannot do.

> **PASTE-READY (Conclusion):** "In governed monthly aggregates for people with type 2 diabetes and/or hypertension, CHD first hospitalisations were more closely associated with hot nights, and HF first hospitalisations with cold days, than with the other thermal encodings examined."

**First-event depletion: shown, but its interaction with hot nights is not drawn.** Figure 1 documents that first-event counts halved while the 35+ population rose 17%. What the paper does not say is that depletion and the hot-night exposure are *both* strong monotone trends over the window (official hot nights: 10 in 2013 → 61 in 2021 → 56 in 2023, `REAL` HKO), and both lean on the same 4-df spline for control. The cold-day series gets an identification paragraph and Figure 2; the hot-night series, which has the harder identification problem, gets nothing. The honest evidence already exists: in `outputs/tables/cvd_trend_depletion_sensitivity.csv` (`HA_APPROVED_AGGREGATE`), the CHD hot-night count ratio in the pre-2020 window is 1.011 (0.991–1.032, *p* = 0.29) and under COVID-phase adjustment 1.013 (0.994–1.033, *p* = 0.18). The association is confined to specifications that include 2020–2023 — the same years in which hot nights peaked and care-seeking was disrupted. See Section 4 and Edit 2 for the paste.

**DJF identification: the strongest part of the paper.** The 141/145 December–February concentration, the between-year-winter reading, and the refusal to treat a winter-only restriction as a remedy are all correct and well placed. One sharpening, not required:

> **EXPLORE-ONLY:** only the roughly 33–37 months with any official cold day carry exposure variation for that contrast; the effective information behind the HF cold-day interval is closer to three dozen winter months than to 132. Verify the exact month count from `outputs/live_identification/cold_days_by_month_year.csv` before using.

**Minor:** with calendar-month indicators in the model, the days-in-month offset is nearly collinear with the month dummies and does almost no work. The paper's own offset sensitivity shows this. No edit needed; do not let anyone claim the offset "standardises" anything material.

---

## 2. Do Figures 1–3 earn their place?

| Figure | Verdict | Reason |
|---|---|---|
| Figure 1 (depletion vs 35+ population) | **Keep** | Carries the estimand argument no table carries; answers Bishai's stable-risk-set instinct visually. |
| Figure 2 (cold-day year × month) | **Keep** | The identification core for the only SE-concordant residual. This is the figure a referee will cite back at us approvingly. |
| Figure 3 (residual ACF) | **Demote to supplement** | It displays two numbers (0.508, 0.146) that already appear in the Abstract, the Results text, and its own caption — four tellings of two numbers. A two-series ACF display is a table row, not a figure. Worse, its message ("CHD model SEs are too narrow") is contradicted by the Table 3 ladder direction (Section 4). |

If the live file should keep three figures, replace Figure 3 with `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`, which already exists in the validated release and shows all twelve contrasts across nine specifications with Newey–West lag-6 intervals — including the pre-2020 CHD hot-night interval crossing 1. That figure does identification work; Figure 3 does decoration work.

---

## 3. Introduction

**Guo 2024 [17]: used precisely.** The draft states the daily hot-season emergency-hospitalisation design, the official `HNday28` null after mean-temperature adjustment, the hourly 20:00–07:59 excess-heat metric, and the +3.1% (1.5–4.8%) extreme contrast, and it explicitly refuses to treat monthly official counts as a test of the hourly metric. This matches the say map. Two optional tightenings: (a) the null could carry its interval for symmetry with the positive finding — **PASTE-READY:** "showed no overall association with non-cancer, non-external hospitalisation over lags 0–4 days (excess relative risk −0.2%, 95% CI −1.2% to 0.7%)" [17]; (b) "Official monthly counts of hot nights are **therefore** a coarser encoding" — the "therefore" implies Guo tested monthly counts; he did not. Change "therefore" to "thus by construction" or simply drop the connective.

**Goggins 2017 [21]: bounded correctly.** The 2.63 (2.43–2.84) cumulative RR is introduced with period, design, lag window, and the explicit non-transferability sentence, and the Discussion compares "questions, not magnitudes" without repeating the numeral. No change.

**AMI slippage: none found.** AMI appears only as Goggins 2013 history and in the Methods not-identified list. The title, Abstract, and outcome descriptions hold the first-hospitalisation-after-first-diagnosis line throughout. This was the failure mode of the Week-1 framing and it is genuinely gone.

**What is wrong in the Introduction is the citation hygiene, not the science:**

1. Sentence one cites [9,10] for subtropical morbidity, but [10] is Bhaskaran's time-series *methods* tutorial. It supports the Statistical analysis section, not a substantive claim about humid heat. **PASTE-READY:** cite [9] alone in sentence one.
2. References [3] (HKO yearbook 2017), [5] (HKO yearbook 2024), and [6] (HKO Open Data) are never cited in the body. Since references 1–8 are Hogan's block, do not delete them unilaterally: either attach [6] to the Results exposure-context sentence ("At HKO Headquarters, hot nights rose from 10 in 2013 to 61 in 2021 and 56 in 2023 [6]." — **PASTE-READY**) and flag [3]/[5] to Hogan as his call, or ask him to prune. An uncited-reference note from a copy editor is avoidable embarrassment.
3. The Introduction's cold-day sentence now cites [2,4], but those are the 2013 and 2021 yearbooks; neither covers the 2023 value (14 cold days), and the reference list contains no 2023 yearbook. Attach [6] (the Open Data service the derived counts actually came from) to the 2023 values, or add the 2023 yearbook to Hogan's block.

**Register:** the pollution paragraph's "pollution adjustment, when used, is staged rather than screened for attenuation" is Methods content in the Introduction and uses in-house phrasing ("screened for attenuation"). Move the design statement to Methods (it already exists there) and keep only the confounding motivation in the Introduction. One sentence saved, one reviewer question avoided.

---

## 4. Discussion

**It leads with the inferential limit.** Paragraph one opens with "The current data do not support a protected differential thermal claim" before interpreting anything. Correct order; keep.

**The uncertainty sentence must die.** The Discussion states: "Pearson residual autocorrelation at lag 1 is 0.508 in that model, so model-based intervals are too narrow for the CHD series." The paper's own Table 3 refutes this for the contrast it defends. For CHD hot nights the ladder *narrows* monotonically: Model 0.995–1.049 → HC1 0.997–1.047 → NW3 1.0003–1.0439 → NW6 1.002–1.042 (`table4_uncertainty_ladder.csv`, `HA_APPROVED_AGGREGATE`). Under positive residual autocorrelation the usual expectation is the opposite — robust intervals wider, as they in fact are for HF cold days (Model 1.023–1.125 → NW6 1.006–1.144). When the HAC variance comes out *smaller* than the model variance, the Newey–West exclusion of 1 is produced by the smaller robust SE, and small-sample HAC estimates at 132 months are known to be noisy. As written, the sentence hands a referee a one-line rebuttal: "your robust intervals are narrower than your model intervals; your stated rationale predicts the reverse." The paragraph's closing sentence ("No interval construction was chosen because it excluded 1") is right and should stay.

> **PASTE-READY (replace the "too narrow" sentence only):** "Pearson residual autocorrelation at lag 1 is 0.508 in that model, so inference for the CHD series depends on how serial dependence is handled. For this contrast the Newey–West intervals were narrower than the model-based interval, which is atypical under positive residual autocorrelation; the exclusion of 1 therefore rests on the smaller robust variance estimate and is a reason for caution, not confirmation."

> **PASTE-READY (optional companion, end of the Table 3 paragraph in Results):** "For CHD hot nights the ladder narrowed from the model-based to the Newey–West intervals; robust intervals are not automatically wider, and the direction of that change is itself informative."

**Symmetric sensitivity transparency.** The Results robustness paragraph quotes the HF cold-day pre-2020 strengthening with a full interval (1.113, 1.053–1.176) but compresses the CHD hot-night sensitivities into "ranged from 1.011 to 1.025," never revealing that the 1.011 end is the pre-2020 window with an interval spanning 1. The same paid table that supplied 1.113 supplies the missing intervals. This is the difference between reporting a range and reporting what the range means.

> **PASTE-READY (Results, after the HF pre-2020 sentence):** "The CHD hot-night association was weaker and compatible with 1 in the pre-2020 window (1.011, 0.991–1.032) and under COVID-phase adjustment (1.013, 0.994–1.033)." — source `outputs/tables/cvd_trend_depletion_sensitivity.csv`, `HA_APPROVED_AGGREGATE`; prose only, not Table 2.

> **PASTE-READY (Discussion, extend "The CHD hot-night association is smaller and depends on the uncertainty method."):** "The CHD hot-night association is smaller, depends on the uncertainty method, and was not evident in the pre-2020 window."

**Coefficient-magnitude comparisons:** none survive that should die — the Goggins 2.63 and Guo 3.1% comparisons are questions-not-magnitudes in the Discussion, as the ledger requires. The one numeral I would reconsider is the archive flu coefficient 1.673 (1.249–2.243). It is the largest CI-bearing effect anywhere in the paper, it is not from the analysis of record, and skimming reviewers quote large numbers regardless of the disclaimer wrapped around them. Recommendation: keep the fact, move the numeral. **PASTE-READY (option):** "On the 121 months with influenza data, an archive model associated influenza activity with substantially higher CHD counts (estimate in the accompanying release); that model does not adjust Table 2." If the team prefers keeping the numeral for magnitude honesty, the current labelling is adequate — this is a risk call, not an error.

**Missing limitation.** Nothing in Strengths and limitations acknowledges that all exposure comes from one station. **PASTE-READY (Limitations):** "All exposures were measured at a single Observatory station and applied territory-wide; within-territory exposure variation was not modelled." Hogan will add this himself if we do not.

**Register sweep: "continuity" is undefined jargon.** The word appears 15 times in the post-merge draft — Methods, Results, Discussion, Limitations — and is never defined. It is our internal name for the analysis of record; a journal reader meets it cold with no anchor. The cns-writing skill bans internal process language, and this is the largest remaining instance; the Opus pass cleaned the Abstract but left the body. Fix: global replace "continuity" → "core," plus one definitional sentence. **PASTE-READY (Study design, after the exploratory sentence):** "We refer to the twelve separate single-exposure models as the core panel." This is a mandatory item, not a stylistic suggestion.

---

## 5. What the overnight plan missed that would actually help Hogan

1. **The hot-night identification gap.** The night-explore note asks Hogan (open question 2) whether official monthly hot-night counts remain his preferred encoding, but does not give him the one fact that makes the question urgent: under that encoding the CHD association is confined to specifications including 2020–2023. That fact bears directly on his HM/CM lock — an upper-tail definition that behaves differently pre-2020 would be worth his attention; one that reproduces the same post-2020 dependence would not. Give him the sensitivity table, not just the question.
2. **The ladder-direction anomaly.** Every prior note (12 August insights, night explore, claim ledger) records "CHD hot nights are SE-sensitive" as Model/HC1-include-1, and none noticed that the robust intervals are *narrower* — which reverses the draft's stated rationale for the Newey–West display. That is the kind of thing Hogan finds in other people's papers.
3. **`figure4_trend_depletion_sensitivity` was skipped.** `LIVE_DOC_EDITS.md` step 8 offers Hogan the forest (`figure3_core_forest.svg`) and the SE ladder (`figure5_se_method_ladder.svg`) as optional extras, but not `figure4_trend_depletion_sensitivity`, the one release figure that answers an identification question rather than restating Tables 2–3.
4. **Reference hygiene.** Uncited [3]/[5]/[6] and the [10]-in-sentence-one mismatch survived every pass because every pass read the prose and nobody audited citation-to-claim mapping. Cheap to fix now, embarrassing at proof stage.
5. **The "continuity" sweep.** The say map polices literature language exhaustively and never checks our own vocabulary. Fifteen undefined uses of an internal term is a bigger register problem than any single Guo sentence.

---

## 6. Plan changes (Keep / Change / Drop)

| Item | Verdict | Note |
|---|---|---|
| Paste order and do-not-touch list in `LIVE_DOC_EDITS.md` | **Keep** | Sound; Hogan weather verbatim, no parallel Word file. |
| Refusal architecture (no protected claim, all twelve *q* > 0.19, failed daily-recovery reported) | **Keep** | The paper's spine; nothing here weakens it. |
| Guo/Goggins bounded usage per the say map | **Keep** | Executed correctly. |
| **Laidlaw Stage 3 PDFs / A0 poster frozen** | **Keep frozen** | Nothing in this critique touches the programme track. The two fixes in Section 4 change journal-track prose only; the frozen PDFs make no Newey–West-rationale claim and no pre-2020 hot-night claim, so no new inconsistency is created. Unfreeze only if Bob supplies a new lock. |
| Discussion uncertainty sentence | **Change (mandatory)** | Edit 1 below; currently self-contradicted by Table 3. |
| Robustness reporting symmetry | **Change (mandatory)** | Edit 2 below; add the CHD pre-2020 and COVID-adjusted intervals to Results prose and one Discussion clause. Not Table 2. |
| "Continuity" vocabulary | **Change (mandatory)** | Edit 3 below; route through the Opus register pass. |
| Figure 3 (residual ACF) | **Change** | Demote to supplement; if a third figure is wanted, use `figure4_trend_depletion_sensitivity.png` from the release. |
| Reference list [3]/[5]/[6], [9,10] sentence | **Change** | Attach [6] in Results exposure context; fix sentence one to [9]; flag [3]/[5] to Hogan since 1–8 are his block. |
| Single-station exposure limitation | **Change** | One added sentence in Limitations. |
| Archive flu numeral in Discussion | **Change (optional)** | Direction in text, numeral in the release; team's call. |
| Conclusion "most elevated in relation to" | **Change** | Superlative → comparative; sentence provided in Section 1. |
| Sleep/blood-pressure mechanism paragraph | **Drop stays dropped** | The overnight decision was right; Hogan's rule holds. |
| HM/CM provisional estimates in the paper | **Drop stays dropped** | Unlocked family; meeting material only. |
| Numerical 2.63-vs-1.073 or 3.1%-vs-1.022 comparisons | **Drop stays dropped** | Correctly dead. |

No change to the overall overnight strategy: the live file remains the single authority, Roro keeps the health-data paragraph, and no new health model is fitted. The plan change I am proposing is narrow — three mandatory text edits, one figure swap, and adding the sensitivity display to what Shen pastes — all from existing tables.

---

## 7. Existing identification display not yet in the paper

- **Table:** `outputs/tables/cvd_trend_depletion_sensitivity.csv` (`HA_APPROVED_AGGREGATE`). One-sentence caption: "Count ratios (Newey–West lag-6) for the twelve core contrasts across nine trend, window, and COVID-phase specifications, showing the CHD hot-night association confined to specifications that include 2020–2023 and the HF cold-day association strongest before 2020."
- **Ready-rendered figure (same content):** `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`. One-sentence caption: "Core count ratios across trend and first-event sensitivities (Newey–West lag-6 intervals): the pre-2020 CHD hot-night interval includes 1 while the pre-2020 HF cold-day interval strengthens."

No new health model is needed; both artefacts already exist. Nothing here goes into Table 2.

---

## 8. Three highest-leverage edits

1. **Replace the Discussion uncertainty sentence** ("model-based intervals are too narrow for that series") with the ladder-direction-honest version in Section 4. It is currently refuted by the paper's own Table 3 and is the single easiest hostile-review target in the draft.
2. **Add symmetric pre-2020 / COVID-phase reporting for CHD hot nights** (1.011, 0.991–1.032; 1.013, 0.994–1.033) to the Results robustness prose and one Discussion clause, matching the prominence already given to the HF pre-2020 strengthening. Existing `HA_APPROVED_AGGREGATE` numbers; prose only.
3. **Define-and-replace "continuity"** (15 undefined uses → "core" plus one definitional sentence in Study design), folded into the next register pass.

---

*Residue: this memo. No live-file edit was made. The three PASTE-READY blocks in Section 4, the Conclusion sentence in Section 1, and the citation fixes in Section 3 are ready for `LIVE_DOC_EDITS.md` once the parent session accepts them; EXPLORE-ONLY items need verification or a human nod first.*
