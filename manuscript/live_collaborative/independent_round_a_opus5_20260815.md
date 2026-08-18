# Independent Round A review — manuscript architecture

**Reviewer.** Opus-5 Max acting as manuscript architect. Round A, independent: no favoured thesis was supplied, and no other reviewer's file in this session was read.

**Read for this review.** `hogan_skeleton_20260728.md`; `Heat_CVD_Manuscript_live_update.md`; `claim_ledger.md`; `hogan_comment_responses.md`; `analysis_plan/writing_standards_hogan.md`; the checklist in `.cursor/skills/cns-writing/SKILL.md`. Two cited tables were opened to test claims: `outputs/live_identification/hot_nights_by_month_year.csv`, and Table 2 / Table 3 values as printed in the draft.

**Scope.** No manuscript file was edited. No new model was fitted, no number was created, and no citation or collaborator decision was invented. Every replacement sentence below reuses numbers already in the draft.

---

## Central argument (as the draft currently reads)

The draft argues a negative thesis with four planks.

1. **The panel is exploratory and unprotected.** Twelve separate single-exposure negative-binomial models cover two outcomes and six monthly thermal encodings. Every Benjamini–Hochberg *q*-value exceeds 0.19, the model set was specified after the outcome series existed, and no contrast is promoted.
2. **Two associations remain, and they differ in kind.** The HF cold-day ratio is concordant across all four standard-error constructions, survives exclusion of the most influential month, and is unchanged in the joint extreme-day model. The CHD hot-night ratio depends on which variance estimator is used, is absent before 2020, and attenuates at lag one month.
3. **What identifies each coefficient is displayed rather than assumed.** After calendar-month indicators, cold days are a between-winter contrast (141 of 145 days in December–February) and hot nights are a summer-intensity contrast (June–September always contained at least one; July 2013 one night, July 2022 twenty-five).
4. **Two refusals bound the paper.** No daily coefficient is recovered from monthly sums, because a frozen calibration failed; no stroke result is reported, because no stroke series was delivered.

The Conclusion states the contribution as hypotheses plus an explicit account of what monthly aggregate counts cannot settle. That is a coherent argument and it matches the tables.

One qualification. The argument as *stated* is design-limiting, but the Abstract Results as *ordered* read as two positive findings followed by a caveat, because the first sentence gives the two count ratios and the second gives the family-wide *q*. A reader who stops after one sentence takes away a heat signal for CHD and a cold signal for HF. That is an ordering defect, not a data defect, and it is the single change with the largest effect on how the paper is received.

A second qualification. The paper has two centres of gravity that are never ranked: the residual associations (Results §Core panel, §Uncertainty ladder, and the first three Discussion paragraphs) and the identification-and-limits account (Results §Exposure context, §Joint models, Strengths and limitations). The draft alternates between them. Choosing which is the spine is the outstanding architectural decision, and the next section sets out the options.

---

## Alternative thesis formulations (at least four, including ones you do not recommend)

These are formulations of the same evidence. None adds a claim the tables do not carry.

**A. Identification-first.** *After calendar-month adjustment, monthly official extreme-day counts are identified by between-winter variation for cold days and by summer intensity for hot nights; on that variation, a governed monthly panel yields no multiplicity-protected thermal association in this cohort.* Recommended as the spine. It is the plank the draft supports most fully, it is carried by Figures 2 and 4 and by the design paragraphs, and it makes the null informative rather than apologetic. Cost: it demands that the two remaining associations be presented as what the design can produce, not as near-misses.

**B. Estimator-dependence.** *The inferential status of a monthly thermal coefficient can depend on the variance estimator, and the dependence is not in the direction usually assumed.* Recommended as a subordinate plank, not as the headline. It is well evidenced: the CHD hot-night standard error falls monotonically from the model-based to the Newey–West lag-6 construction, while the HF cold-day standard error rises across the same ladder, so the ladder distinguishes the two contrasts rather than merely widening both. As a headline it converts an epidemiology paper into a statistical-practice paper on a single series.

**C. Denominator and risk-set depletion.** *First-event counts in a diagnosis-window cohort fall by about half while the general adult population rises, so monthly first-event aggregates without still-at-risk person-time cannot support incidence claims.* Recommended as a plank. It is already stated in Results and Limitations and it is the most transferable warning for other teams using similar extracts. It cannot be the headline, because the share of the decline attributable to depletion is not quantifiable from the delivered data, and the draft correctly says so.

**D. Aggregation-recovery negative calibration.** *A published method for recovering daily exposure coefficients from temporally aggregated outcomes failed a frozen pre-specified calibration against this city's weather, so no daily coefficient was admitted.* Viable and honest, but not recommended for this paper: it would displace the epidemiological question, and its natural home is a short methods report where the failing cells can be characterised properly. Listed again as a research extension.

**E. Dual-hazard preparedness.** *Warming has not removed cold-associated cardiac burden in Hong Kong, so preparedness must carry both tails.* Not recommended as the thesis. The exposure side is solid, but the health side rests on one contrast with *q* = 0.192, identified from differences between winters. The framing would put a policy conclusion on an unprotected estimate.

**F. Differential thermal aetiology (CHD heat, HF cold).** *CHD and HF respond to opposite thermal tails.* Not recommended, and the draft is right to refuse it. All twelve *q*-values exceed 0.19, no test of difference between outcomes or between encodings was performed, and the CHD hot-night coefficient doubles on the log scale when very hot days enter jointly. This is the formulation the paper must keep resisting.

**G. Informative null.** *A decade of monthly territory data was unable to detect a thermal association of plausible size.* Not recommended as written, because no power or minimum-detectable-effect analysis is reported. It would become available if such an analysis were added, and it would then reinforce formulation A rather than replace it.

---

## Structure, transitions, novelty, consistency

**Checks that pass.** Hogan's weather paragraph is character-identical to the origin file once subscript markup is normalised. Every interval in Table 2 reproduces its printed *p*-value to rounding. The twelve *q*-values reproduce exactly under a Benjamini–Hochberg step-up on the printed *p*-values, including the monotone adjustment that gives the smallest *p* the same *q* = 0.192 as the second smallest. The reported annual declines are 48% and 47%, so "about half" holds; the population rise is 17.1%. The claim that the Newey–West intervals are narrower than the model-based interval for CHD hot nights is correct, and the corresponding standard errors move in the opposite direction for HF cold days.

**Figure citation order.** Figures are first cited in the order 1, 2, 4, 3. Renumber the hot-night display as Figure 3 and the residual autocorrelation display as Figure 4. Affected mentions: the hot-night display's in-text call in Results §Exposure context, its caption and image line, its call in the Discussion identification paragraph; and the residual display's in-text call in §Joint models, its caption and image line. The hot-night caption's sentence "The layout matches Figure 2" stays correct after renumbering. Image file names need not change.

**Section order.** Strengths and limitations currently follows the Conclusion, so the paper ends on limitations. Move it before the Conclusion. No text change is required.

**Introduction paragraph order.** The pollution paragraph sits between the nighttime-heat paragraph and the mortality-baseline paragraph, interrupting the health-evidence arc. Moving it after the mortality paragraph groups local health evidence first and covariate context second, and leaves it adjacent to the objective. It does not affect the substance of the reply to Hogan's comment on that paragraph.

**Novelty placement.** The gap statement is one sentence inside the nighttime-heat paragraph: Guo et al. did not study first CHD or HF hospitalisation in a diabetes or hypertension cohort. It is the only sentence that says what is new, and it is three paragraphs away from the objective. Consider relocating it to immediately precede the estimand sentence. It is verifiable as written, since it states only what a cited study did not do; do not strengthen it into a priority claim without a documented search.

**Robustness in prose only.** The robustness paragraph carries the whole sensitivity set in running text, across trend, period, COVID-phase, lag, and influence specifications. A supplementary table drawn from the existing outputs would be easier to check and would let the Discussion cite rows instead of restating numbers.

**Reporting asymmetry.** The influenza coefficient in the Discussion is the only estimate in the paper whose interval excludes 1 without qualification, and it appears outside Results, on 121 months, under a different offset, and outside the multiplicity family. A paper this disciplined about the core panel should not leave that number less guarded than the contrasts it declines to promote.

**Uncited references.** Entries 3 and 5 (the 2017 and 2024 annual weather summaries) are never cited in the text. Separately, the 2023 annual exposure counts are attributed to the open-data reference rather than to an annual summary for that year, and no such entry exists in the list. Both need a human decision: cite, replace, or remove. Do not add a reference that has not been checked.

**Register items.** Internal provenance tokens appear in four figure captions, and "archive" appears four times as a noun for unreported models. "Refusal" carries a project meaning that a journal reader will not have. Replacements are proposed below and are safe to defer while the file is circulating internally.

**Term collision.** The Discussion calls the two remaining associations "residual signals" two paragraphs before discussing Pearson residual autocorrelation. Different senses of "residual", adjacent.

---

## Statements that extend beyond available evidence

1. **Comparative language without a test of difference.** The Discussion and the Conclusion both say one outcome was "more closely associated" with one encoding "than with" others. No test comparing coefficients across encodings or across outcomes is described; the joint models are declared collinearity diagnostics. With every *q* above 0.19 and overlapping intervals, this is a comparison of point estimates and should say so.
2. **The Guo comparison rests on an unstated non-comparability.** Guo et al. reported a null for the official hot-night flag *after adjustment for mean temperature*. The present hot-night models carry one exposure at a time and are not adjusted for monthly mean temperature; no adjusted analogue is reported. The draft lists three differences (monthly counts, first-event series, later decade) and omits the one that matters most for that specific comparison. Relatedly, "consistent with" asserts agreement that no formal comparison establishes.
3. **A record claim outside the ledger.** "The 2021 total was the highest annual number of hot nights in the Observatory record through the study window" mixes a within-window maximum with the full station record. The project's monthly table supports the within-window statement (2021 is the maximum of the eleven annual totals); the full record is not in evidence here.
4. **A 2023 exposure sourcing gap.** The 2023 annual counts are reported against the open-data reference, with no annual summary for 2023 in the reference list. This is a citation-hygiene item, not a numerical error.
5. **An implied analysis that is not reported.** The Introduction says pollution adjustment "is staged rather than screened for attenuation", which reads as though staged adjusted estimates are part of this paper. None is reported, and Limitations states that pollution confounding is unresolved.
6. **An unqualified emphasis.** The CHD hot-night coefficient doubles on the log scale when very hot days enter jointly (1.022 to 1.045, variance inflation near 1.96). The draft labels joint coefficients as diagnostics and stops there. Whatever interpretation the team prefers, the sensitivity of that coefficient to co-adjustment belongs beside the emphasis it qualifies.
7. **Watch item, not a defect.** Inpatient-only semantics are inferred from delivered column labels. That is properly hedged in Methods and Limitations, and it is invisible in the Abstract. If the confirmation does not arrive before submission, the Abstract should carry the qualification too.

---

## Hogan-comment coverage from a readability standpoint

| Thread | Readability verdict |
|:--|:--|
| Title, amend once results exist | Amended to the delivered estimand, and clearer than the skeleton title. It still omits the cohort, so the title reads as a general-population study. This is the moment his comment anticipated. |
| Authors 2–4 | Placeholders and a role note. Reads as an internal note, which is correct for a live file. |
| Remove "Acute myocardial infarction and" | Fully resolved and readable. AMI now appears only as cited local history, and the closer heart-failure admissions anchor was added with an explicit non-transferability sentence. |
| Cite the listed factors; drop housing and behaviour | Resolved in the direction he asked. The Introduction no longer names unmeasured individual factors, and the reader meets unmeasured factors only in Limitations and in one Discussion sentence, which is the intended effect. Two wording defects live in the response file rather than the manuscript: it reports the closing thesis as one sentence when the paragraph has two, and it credits Bhaskaran et al. (2013) as physiological motivation when the draft cites that paper for the time-series model. Ye et al. (2012) carries the mechanism citation alone. |
| "Environmental context has also evolved" | Answered directly, with 2013–2023 general-station means and an explicit statement that no 2000–2009 reconstruction was attempted. The paragraph is dense but each sentence carries one claim. One implication defect, item 5 above. |
| Combine the thesis into one sentence | Partially met. The paragraph is now an estimand sentence plus a reporting-posture sentence. Compressing both into one sentence would produce a fifty-word sentence and would violate his own one-claim-per-sentence bar. Recommendation: keep two sentences and correct the response file to say so, rather than compress the manuscript. |
| Yang C-Y to Yang CY | Correct in reference 1. |
| Weather paragraph verbatim | Verified identical, including "Meteorological data was obtained". The processing paragraph that follows does not touch his sentences. |

---

## Proposed paste-ready replacement sentences

Each item quotes the current text exactly and reuses only numbers already in the draft.

**1. Title — name the cohort.**

Current: `Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023`

Replacement: `Thermal extremes and first hospitalisation after coronary heart disease or heart failure diagnosis among people with type 2 diabetes or hypertension in Hong Kong, 2013–2023`

The working-title note already reserves a shorter running head.

**2. Abstract, Background — cohort precision.**

Current: `Whether that pattern also describes recent monthly counts of first hospitalisation among people with diabetes or hypertension is a separate question.`

Replacement: `Whether that pattern also describes recent monthly counts of first hospitalisation among people with type 2 diabetes or hypertension is a separate question.`

**3. Abstract, Results — lead with the family result.**

Current: `Under Newey–West lag-6 reporting, the count ratio was 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF. Both had *q* = 0.192, and all twelve core *q*-values exceeded 0.19.`

Replacement: `No contrast in the twelve-model panel reached a multiplicity-protected threshold: all twelve Benjamini–Hochberg *q*-values exceeded 0.19. The two largest associations, under Newey–West lag-6 reporting, were 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF, both with *q* = 0.192.`

**4. Results, core panel — decimal place.**

Current: `The HF mean-minimum-temperature interval included 1 at the fourth decimal place (unrounded upper bound 1.00005).`

Replacement: `The HF mean-minimum-temperature interval included 1, with an unrounded upper bound of 1.00005.`

The exceedance appears at the fifth decimal, so the current phrasing misstates it.

**5. Introduction — do not imply staged adjusted estimates.**

Current: `Entering ozone in the same model as temperature can change the meaning of the thermal coefficient, so pollution adjustment is staged rather than screened for attenuation.`

Replacement: `Entering ozone in the same model as temperature can change the meaning of the thermal coefficient, so the core models carry one thermal exposure at a time and no pollutant is used as a screening covariate.`

**6. Results, exposure context — keep the record claim inside the window.**

Current: `The 2021 total was the highest annual number of hot nights in the Observatory record through the study window.`

Replacement: `The 2021 total was the highest annual number of hot nights at Headquarters during 2013–2023.`

**7. Discussion, opening — match the Abstract's wording.**

Current: `The current data do not support a protected differential thermal claim for CHD relative to HF.`

Replacement: `The current data do not support a multiplicity-protected differential thermal claim for CHD relative to HF.`

**8. Discussion, opening — comparison of point estimates.**

Current: `Under Newey–West lag-6 reporting for the core panel, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or cold days, and HF counts were more closely associated with cold-day burden than with hot nights.`

Replacement: `Under Newey–West lag-6 reporting for the core panel, the largest CHD count ratio was for official hot-night burden rather than for mean temperature or cold days, and the largest HF count ratio was for cold-day burden rather than for hot nights; differences between exposure encodings were not formally tested.`

The same defect appears in the Conclusion, which is the paper's last word on the point.

Current: `In governed monthly aggregates for people with type 2 diabetes and/or hypertension, CHD first hospitalisations were more closely associated with hot nights, and HF first hospitalisations with cold days, than with the other thermal encodings examined.`

Replacement: `In governed monthly aggregates for people with type 2 diabetes and/or hypertension, the largest count ratios were for hot nights in CHD and for cold days in HF; differences between exposure encodings were not formally tested.`

**9. Discussion — term collision.**

Current: `The HF cold-day association is the more coherent of the two residual signals.`

Replacement: `The HF cold-day association is the more coherent of the two remaining associations.`

**10. Discussion — state the adjustment asymmetry with Guo et al.**

Current: `A q-unprotected hot-night count ratio is consistent with that design and with the official-flag result in Guo et al. [17].`

Replacement: `A *q*-unprotected hot-night count ratio is what that design can support, and it does not conflict with the official-flag result in Guo et al. [17].`

Current: `The present analysis uses monthly official counts, a first-event CHD series, and a later decade.`

Replacement: `The present analysis uses monthly official counts, a first-event CHD series, a later decade, and models that carry hot nights without adjustment for monthly mean temperature.`

**11. Discussion — guard the influenza coefficient.**

Current: `That coefficient does not adjust Table 2.`

Replacement: `That coefficient does not adjust Table 2 and lies outside the twelve-contrast multiplicity correction.`

**12. Discussion, closing — plain wording for "refusals".**

Current: `We report the complete panel and the refusals.`

Replacement: `We report the complete panel and state where we declined to produce an estimate.`

**13. Table 3 caption — define the columns.**

Current: `**Table 3. Uncertainty ladder for the two leading exploratory contrasts.**`

Replacement: `**Table 3. Uncertainty ladder for the two largest exploratory contrasts. Columns are model-based, HC1, Newey–West lag-3 (NW3), and Newey–West lag-6 (NW6) intervals.**`

**14. Strengths — plain wording.**

Current: `The daily-recovery analysis is reported as a refusal rather than as a coefficient.`

Replacement: `The daily-recovery analysis is reported as a failed calibration rather than as a coefficient.`

**15. Register pass, safe to defer while the file circulates internally.** Replace internal provenance tokens in the four figure captions, and the noun "archive".

Current: `Provenance: HA_APPROVED_AGGREGATE annual totals; REAL C&SD mid-year population aged 35+.`
Replacement: `Sources: governed Hospital Authority monthly aggregates; Census and Statistics Department mid-year population aged 35 years or older.`

Current: `Provenance: REAL HKO official flags (Tmin ≤ 12 °C) rolled to calendar months.`
Replacement: `Source: Hong Kong Observatory official cold-day flags (Tmin ≤ 12 °C) aggregated to calendar months.`

Current: `Provenance: REAL HKO official flags (Tmin ≥ 28 °C) rolled to calendar months.`
Replacement: `Source: Hong Kong Observatory official hot-night flags (Tmin ≥ 28 °C) aggregated to calendar months.`

Current: `Provenance: REAL residuals from already-fitted core models.`
Replacement: `Source: Pearson residuals from the fitted core models.`

Current: `Staged pollution models exist in the archive; they are not adjusted versions of the separate core panel and were not used to claim that confounding is resolved.`
Replacement: `Staged pollution models were fitted but are not adjusted versions of the separate core panel, and were not used to claim that confounding is resolved.`

Current: `Archive models that entered pollution, humidity, or influenza are not adjusted versions of the separate core panel.`
Replacement: `Models that entered pollution, humidity, or influenza are not adjusted versions of the separate core panel.`

Current: `Archive models in which they enter are not adjusted versions of the core panel.`
Replacement: `Models in which they enter are not adjusted versions of the core panel.`

Current: `an archive model that used a general-population × days offset`
Replacement: `a supplementary model that used a general-population × days offset`

**Not proposed as sentences, because they require a human decision:** figure renumbering, moving Strengths and limitations before the Conclusion, moving the Introduction pollution paragraph, relocating the gap sentence, adding a supplementary robustness table, and resolving references 3 and 5 together with the 2023 exposure source.

---

## Research extensions portfolio

Separate from this paper. Each entry states the question and why it is not this paper.

**1. Daily cause-coded admissions.** Do thermal exposures trigger admissions whose recorded reason is cardiac, at daily resolution with distributed lags? Not this paper: the delivered outcome is monthly, admission cause is not recorded, and 132 monthly sums do not identify a daily lag curve.

**2. Cohort person-time denominators.** What are the incidence-rate ratios once monthly counts of cohort members still at risk of a first event are available? Not this paper: those denominators were unavailable, so every estimate here is a count ratio, and the share of the first-event decline attributable to risk-set depletion cannot be quantified.

**3. Nighttime heat intensity in this cohort.** Does an hourly excess-heat metric, rather than an official nightly flag, associate with first cardiac hospitalisation among people with diabetes or hypertension? Not this paper: the exposure requires hourly series and a daily outcome, and the monthly official count is a coarser encoding by construction.

**4. Stroke, when a series is delivered.** Do monthly first stroke hospitalisations in the same cohort behave like the CHD or the HF series? Not this paper: the series was named in correspondence and never attached, and nothing about it may be pre-empted.

**5. Effect modification by age, sex, and disease subtype.** Which strata carry any thermal association? Not this paper: strata were not delivered, and the ecological monthly design would not license individual-level modification claims even if they were.

**6. Exposure measurement error across the territory.** How much does single-station exposure misclassify monthly extreme-day counts, and in which direction does that bias a health coefficient? Not this paper: the station-versus-reanalysis mismatch is documented here as a limitation, and turning it into a bias estimate needs a daily multi-station design and a population-weighting scheme.

**7. Designed temperature–pollution analysis.** Does staged entry of nitrogen dioxide, particulate matter, and then ozone change the thermal coefficient, and is ozone better treated as a modifier than as a covariate? Not this paper: the core panel is unadjusted, the existing pollution models are not adjusted versions of it, and a designed analysis needs its own pre-specification.

**8. Methods report on recovering daily effects from aggregated outcomes.** Under which data-generating conditions does the aggregation-recovery estimator fail, and what diagnostics warn a user in advance? Not this paper: it would displace the epidemiological question, and a useful answer needs a simulation grid built for the purpose rather than one city's calibration.

**9. Infection and temperature together.** Does influenza activity confound or modify thermal associations with cardiac hospitalisation? Not this paper: coverage is 121 of 132 months, the existing coefficient uses a different offset, and it sits outside the multiplicity-controlled family.

**10. Care-seeking as an outcome-ascertainment problem.** How much of the 2020 trough reflects changed care-seeking rather than changed risk? Not this paper: the monthly counts cannot separate the two, and the draft correctly declines to apportion them.
