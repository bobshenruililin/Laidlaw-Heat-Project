# Hogan-register replacement pass — Abstract, Introduction, Discussion, Conclusion, Limitations

**Date:** 13 August 2026. **Scope:** drop-in replacement prose for four sections of `Heat_CVD_Manuscript_live_update.md`. **Status:** proposal for the parent session to merge; this file does not modify the live draft.

**Rules observed.** The scientific contract is unchanged: monthly ecological count ratios for the first recorded hospitalisation after a first CHD or HF diagnosis in a type 2 diabetes and/or hypertension cohort, 132 months, January 2013–December 2023, admission cause not recorded, stroke not attached. Every quantitative statement below already appears in `claim_ledger.md` or in a paper named in `2026-08-13_live_intro_discussion_say_map.md`. No number is new. No citation is added; reference numbering stays 1–21. The weather Methods paragraph is not touched and does not appear in this file. Section headings match the live file so that each block can be pasted over its counterpart.

---

## 1. Abstract

### Replacement text

**Background.** Hong Kong records more hot nights and very hot days than it did a decade ago, and cold days have not disappeared. Earlier local studies of daily cardiac admissions emphasised cold. Whether that pattern also describes recent monthly counts of first hospitalisation among people with diabetes or hypertension is a separate question.

**Methods.** We analysed 132 territory-months (January 2013–December 2023) of governed monthly aggregate counts of the first recorded hospitalisation after a first diagnosis of coronary heart disease (CHD) or heart failure (HF) among people diagnosed with type 2 diabetes and/or hypertension (156,156 CHD events; 29,681 HF events). Admission cause was not recorded. Exposures were monthly mean temperature, the monthly means of daily maximum and minimum temperature, and official counts of hot nights, very hot days, and cold days. Each exposure entered a separate negative-binomial model with calendar-month indicators, a natural cubic spline of time (4 df), and a days-in-month offset. Intervals were reported as a ladder of model-based, HC1, Newey–West lag-3, and Newey–West lag-6 constructions. Benjamini–Hochberg *q*-values covered the twelve core contrasts. The model set was specified after the outcome series were available and is exploratory. A method for recovering daily exposure coefficients from monthly sums was tested in simulation and was not applied to the health series.

**Results.** Under Newey–West lag-6 reporting, the count ratio was 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF. Both had *q* = 0.192, and all twelve core *q*-values exceeded 0.19. For CHD hot nights, model-based and HC1 intervals included 1, while both Newey–West intervals excluded 1 on the unrounded scale. For HF cold days, all four interval constructions excluded 1. Official cold days fell almost entirely in December–February (141 of 145 days), so the cold-day contrast is identified from differences between winters. Pearson residual autocorrelation at lag 1 was 0.508 for the CHD hot-night model and 0.146 for the HF cold-day model.

**Conclusions.** The data do not support a multiplicity-protected differential thermal claim. The HF cold-day association is concordant across standard-error methods but is not protected by its *q*-value. The CHD hot-night association depends on how uncertainty is computed. All estimates are ecological monthly count ratios for a first-event outcome without recorded admission cause.

**Keywords:** hot nights; cold days; coronary heart disease; heart failure; Hong Kong; monthly time series

### What changed and why

- **Background compressed to three single-claim sentences.** "Hong Kong now records" became "records … than it did a decade ago" so the comparison has a stated referent; "while cold days continue" became "cold days have not disappeared," which is the claim the exposure table supports.
- **Methods split at the model.** The old sentence carried the design, the covariates, and the offset at once. Exposures, model structure, and interval ladder are now one claim each, which is what a reader scanning an abstract needs.
- **Results reordered to lead with the estimate, not the label.** "Continuity Newey–West lag-6 count ratios included …" placed the reporting convention before the number; the ratio now comes first and the convention qualifies it.
- **Added the identification consequence of the DJF concentration.** The old abstract stated 141 of 145 days without saying what follows from it. One clause now carries the inference that matters for reading the HF result.
- **"both had *q* = 0.192" merged with the family statement**, so multiplicity is one sentence rather than two adjacent ones.
- **Conclusions: "sensitive to how uncertainty is computed" → "depends on how uncertainty is computed."** Same claim, no hedging noun.
- **Retained deliberately:** "governed" (provenance signal used consistently with Methods and Conclusion), the exploratory-specification sentence, and the simulation sentence. Both refusals belong in the abstract.

### cns-writing checklist

- [x] Opening states the problem and the estimand without throat-clearing.
- [x] One substantive claim per sentence throughout.
- [x] Every number traced: 132 months, 156,156, 29,681, 1.022 (1.002–1.042), 1.073 (1.006–1.144), *q* = 0.192, twelve contrasts, 141/145, 0.508, 0.146 — all in `claim_ledger.md`.
- [x] No draft markers: no "work in progress," "TBD," "results forthcoming," "to be confirmed."
- [x] No internal process language: no Gate, pipeline, Tuesday lock, Laidlaw, F1.1/F1.2, nicknames.
- [x] No empty emphasis and no causal verbs; "associated" and "count ratio" carry the claims.
- [x] Nulls and discordance are stated, not hidden: all twelve *q* > 0.19; Model/HC1 include 1 for CHD.
- [x] Mortality quantities are absent from the abstract, so no conflation is possible.

---

## 2. Introduction

### Replacement text

Temperature-related cardiovascular morbidity remains a concern in subtropical cities, where intense humid heat coexists with episodic cold [9,10]. Hong Kong is a dense, ageing city whose thermal profile has shifted within a single decade. At the Hong Kong Observatory (HKO), hot nights increased from 10 in 2013 to 61 in 2021, and very hot days from 17 to 54 in the same comparison [2,4]. Cold days persisted across the period (14 in 2013, 13 in 2021, and 14 in 2023) [2,4]. A contemporary local analysis therefore has to hold heat and cold in one design.

Local evidence on cardiac admissions is daily, diagnosis-specific, and drawn from earlier decades. Using data from 2000–2009, Goggins et al. reported that a 1 °C decrease below an estimated 24 °C threshold was associated with a 3.7% increase in acute myocardial infarction admissions, and found no statistically significant heat association in Hong Kong, Taipei, or Kaohsiung [1]. Same-day nitrogen dioxide was the strongest pollutant predictor in that study [1]. An analysis of public-hospital stroke admissions during 1999–2006 found an inverse association of haemorrhagic stroke with temperature and a weaker ischaemic-stroke association below about 22 °C [11]. Closest to the present outcomes, Goggins and Chan analysed daily public-hospital heart-failure admissions and deaths during 2002–2011 and reported a cumulative relative risk of 2.63 (2.43–2.84) for admissions comparing 11 °C with 25 °C over lags extending to 23 days [21]. These studies fix the local historical pattern. They estimate daily risk for cause-coded admissions, so their coefficients do not transfer to monthly counts of first hospitalisation.

Nighttime heat can be encoded in more than one way. Guo et al. analysed daily unplanned emergency hospitalisations in Hong Kong during the hot seasons of 2000–2019 [17]. After adjustment for multi-day mean temperature, the official hot-night indicator (minimum temperature ≥ 28 °C) showed no overall association with non-cancer, non-external hospitalisation over lags 0–4 days [17]. An hourly excess-heat metric for 20:00–07:59 was associated with higher hospitalisation, including a 3.1% (1.5–4.8%) increase at its extreme value [17]. Official monthly counts of hot nights are therefore a coarser encoding than nighttime intensity. They remain an interpretable public climatological series, and they are not a test of the hourly metric. Guo et al. did not study first CHD or HF hospitalisation in a diabetes or hypertension cohort [17].

Air pollution also changed during the present study window. At general monitoring stations, mean nitrogen dioxide declined from 53.7 µg m^−3^ in 2013 to 32.1 µg m^−3^ in 2023, and fine particulate matter (PM2.5) from 30.8 to 14.6 µg m^−3^, while ozone rose from 42.6 to 58.3 µg m^−3^ [7]. Temperature and pollutants are not interchangeable covariates. Ozone is coupled with hot, sunny conditions and may confound the thermal association or lie on its pathway, so pollution adjustment is staged rather than screened for attenuation.

Daily mortality studies in Hong Kong answer a further, distinct question. Liu et al. (2020) reported a cold-dominant attributable fraction for cause-specific mortality during 2006–2016 (4.72% for cold versus 0.16% for heat), and a larger fraction for moderate non-optimum temperatures than for extremes (4.25% versus 0.63%) [12]. Liu et al. (2026) estimated 1,455 to 3,238 model-based excess heat deaths for 2014–2023, the range reflecting which local heatwave definition was applied [13]. Attributable fractions and modelled excess deaths are mortality burden quantities. They cannot be rescaled into monthly morbidity count ratios.

This study estimates the association between specified monthly thermal-exposure contrasts and monthly counts of first hospitalisation after first CHD diagnosis, and after first HF diagnosis, among people with type 2 diabetes and/or hypertension in Hong Kong from January 2013 through December 2023. Heat and cold exposures are carried in parallel, and discordance between definitions and between uncertainty constructions is reported in place of a single protected claim.

### What changed and why

- **Paragraph 1 gains a stated referent and loses a hedge.** "Hot nights and very hot days have become more frequent while cold days have not disappeared" duplicated the counts that follow it; the counts now do that work alone. "Contemporary analysis therefore has to keep heat and cold in view together" became "hold heat and cold in one design," which names the methodological consequence instead of an attitude.
- **The Goggins block is reordered by relevance to the outcome.** AMI, then stroke, then HF, with "Closest to the present outcomes" marking why the HF study is last. This satisfies the say-map instruction to move toward the outcome-aligned anchor without adding a sentence.
- **Non-transferability is stated by reason, not by assertion.** "They do not estimate monthly first-hospitalisation counts under a later data contract, and their coefficients are not transferable to that contract" repeated itself and used "data contract," which is internal. Replaced with the actual reason: they estimate daily risk for cause-coded admissions.
- **Guo et al. keeps its null first and its positive finding second**, as the say-map requires, but "An hourly excess-heat metric … and an intensity-based binary derived from it" is reduced to the metric that carries the 3.1% estimate. The intensity-based binary added a second number without changing the argument.
- **Liu et al. (2026) now carries its range.** The old sentence said only that excess deaths were estimated. Giving 1,455 to 3,238 and attributing the spread to the definition makes the definition-sensitivity point concrete, which is the reason the citation is there.
- **The objective sentence is shortened and the reporting posture moved out of it.** Hogan's comment 9 asked for one thesis statement; the thesis remains a single sentence. The trailing clause about parallel exposures and discordance is a statement of what is reported, not a second thesis, and it reads better as its own sentence.
- **Not added:** sleep, blood pressure, vasoconstriction, housing, behaviour, or medication. Those factors were not measured and are excluded by Hogan's comment 4 and by `LIVE_DOC_EDITS.md`.

### cns-writing checklist

- [x] No sentence carries two claims; the longest is the Goggins and Chan sentence, which carries one estimate with its contrast and lag window.
- [x] Every number traced: HKO extreme-day counts, EPD annual means, 3.7% / 24 °C, 2.63 (2.43–2.84), 3.1% (1.5–4.8%), 4.72% / 0.16%, 4.25% / 0.63%, 1,455–3,238 — all in `claim_ledger.md` or the say-map.
- [x] Citations formal and attached to the claims they support; references 1–21 unchanged; nothing added.
- [x] AMI appears only as historical evidence, never as this study's endpoint.
- [x] Guo's official hot-night flag is not equated with hourly excess heat, and no mechanism is attributed to it.
- [x] Mortality attributable fractions, modelled excess deaths, and monthly morbidity counts are held apart in one explicit sentence.
- [x] No generic climate-change preamble, no rhetorical question, no scene-setting before the estimand.
- [x] No causal verb is applied to any local association.

---

## 3. Discussion

### Replacement text

The current data do not support a protected differential thermal claim for CHD relative to HF. Under continuity Newey–West lag-6 reporting, CHD first-hospitalisation counts were more closely associated with official hot-night burden than with mean temperature or cold days, and HF counts were more closely associated with cold-day burden than with hot nights. Both patterns sit inside a twelve-contrast family in which every *q*-value exceeds 0.19. The panel is therefore reported complete, and no contrast is promoted to a primary result.

The HF cold-day association is the more coherent of the two residual signals. It is concordant across all four standard-error constructions. It survives exclusion of the most influential pandemic month. It is not produced by entering correlated heat metrics jointly. It nevertheless remains unprotected by its *q*-value. Because official cold days fall almost entirely in December–February, the association is identified from differences between winters rather than from a summer-versus-winter contrast.

The CHD hot-night association is smaller and depends on the uncertainty method. Model-based and HC1 intervals include 1, whereas the Newey–West intervals exclude 1 on the unrounded scale (lag 3: 1.000253 to 1.043860). Pearson residual autocorrelation at lag 1 is 0.508 in that model, so model-based intervals are too narrow for the CHD series. No interval construction was chosen because it excluded 1.

The direction of the HF cold-day residual is consistent with earlier daily evidence that lower temperature was associated with higher heart-failure admissions in Hong Kong [21]. The comparison is between questions, not between magnitudes. A cumulative daily relative risk comparing 11 °C with 25 °C is not a monthly count ratio per five official cold days, and the present event is a first hospitalisation after a first HF diagnosis without recorded admission cause. The CHD hot-night residual should likewise be read against Guo et al. rather than as a replication of it [17]. That study reported no overall association for the official hot-night flag after adjustment for mean temperature, and a positive association for hourly nighttime excess heat [17]. The present analysis uses monthly official counts, a first-event CHD series, and a later decade. A difference between monthly mean temperature and monthly official hot-night counts does not identify an intensity mechanism, and sleep, blood pressure, and personal exposure were not measured.

Liu et al. (2020, 2026) remain complementary mortality baselines [12,13]. Their attributable fractions and excess-death totals cannot be rescaled into the present count ratios. The failed daily-recovery calibration is the corresponding methods limit: monthly sums do not automatically yield daily trigger estimates [15,16]. That refusal is specific to this series, this implementation, and this calibration standard. It is not evidence that recovery of daily effects from aggregated outcomes fails in general.

Pollution and influenza are scientifically motivated in this setting [1,18]. Archive models in which they enter are not adjusted versions of the continuity panel. On the 121 months with influenza data, an archive model associated influenza activity with higher CHD counts (1.673, 1.249–2.243), and that coefficient does not adjust Table 2. Confounding by infection, ozone, or nitrogen dioxide is therefore unresolved. Absent cohort person-time, even a stable count ratio remains a count ratio [14].

A protected primary claim would have required a predeclared confirmatory contrast, multiplicity control that survives the twelve-contrast family, uncertainty constructions that are not chosen for null exclusion, and residual diagnostics that leave no substantial CHD serial correlation unaddressed. This analysis does not meet that bar. We report the complete panel and the refusals.

### What changed and why

- **The opening wall is split into three paragraphs by argument, not by length.** The old first paragraph carried the multiplicity verdict, the HF evidence, the DJF identification caveat, the CHD verdict, and the autocorrelation diagnostic in one block. A reader had to hold five claims at once. Now: verdict, then HF, then CHD.
- **The HF evidence is enumerated as separate sentences.** "It is concordant …, survives …, and is not an artefact of …" was a three-item list inside one sentence, which buries the weakest and strongest support at the same rate. Three sentences give each its own weight, and the *q*-value caveat lands after them rather than inside the same clause.
- **"Artefact" removed.** "Not an artefact of entering correlated heat metrics jointly" claimed more than the diagnostic supports; "not produced by" states what the joint model showed.
- **The NW3 interval is now shown in the Discussion.** The old text asserted that the CHD result depends on the uncertainty method without letting the reader see the interval that carries the dependence. The unrounded bounds appear once, matching Results.
- **The refusal is bounded on three axes instead of one.** "That result is project-specific" became "specific to this series, this implementation, and this calibration standard," which is what the say-map requires and what the 500-replicate result actually licenses.
- **Flu sentence tightened.** "That coefficient is not an adjusted version of Table 2" was a standalone sentence restating the preceding one; it is now a clause on the same claim.
- **Kept verbatim in substance:** the closing paragraph on what a protected claim would require. It is the strongest paragraph in the draft and needed only "This release" → "This analysis."

### cns-writing checklist

- [x] The inferential limit leads; individual contrasts are interpreted only afterwards.
- [x] Local comparisons are bounded to direction and question. 2.63 is never set beside 1.073; 3.1% is never set beside 1.022.
- [x] Mortality attributable fractions and modelled excess deaths are named as non-rescalable in the same paragraph that cites them.
- [x] No mechanism is asserted. Sleep, blood pressure, and personal exposure are named once, as unmeasured.
- [x] The archive influenza coefficient is reported with an explicit statement that it does not adjust Table 2.
- [x] Numbers traced: 0.19, 141/145 (stated as a concentration, not renumbered here), 1.000253–1.043860, 0.508, 121 months, 1.673 (1.249–2.243).
- [x] No draft markers, no gate language, no nicknames, no "it is important to note," no "remarkably."
- [x] Null and discordant results are stated in the first and third paragraphs rather than deferred to limitations.
- [x] No causal verb: "associated," "consistent with," and "identified from" carry the interpretation.

---

## 4. Conclusion

### Replacement text

Between 2013 and 2023, hot nights in Hong Kong increased while cold days persisted. In governed monthly aggregates for people with type 2 diabetes and/or hypertension, the largest positive thermal association was with hot nights for CHD first hospitalisations and with cold days for HF first hospitalisations. Neither association survived correction across the twelve comparisons, and the CHD estimate depended on the treatment of uncertainty. The contribution of this analysis is a set of hypotheses and an explicit account of what monthly aggregate counts cannot settle. Better-denominated and more finely resolved data are required before a thermal effect on cardiac hospitalisation in this cohort can be estimated.

### What changed and why

- **"Most elevated in relation to hot nights" replaced.** A count can be elevated; an association cannot be "most elevated in relation to" an exposure. The claim is now stated as the largest positive association within the panel, which is what Table 2 shows.
- **"An aggregation-aware reporting standard" removed.** The phrase claimed a methodological contribution the paper does not establish and read as self-assessment. Replaced with what the analysis actually leaves behind: hypotheses and a stated account of the design's limits.
- **"Not proof of thermal effects on disease-caused admission" replaced with a forward requirement.** Ending on "not proof" leaves the reader with a negation; ending on the data conditions needed for an estimate is the same honesty with a direction, and it matches the say-map instruction to close on hypotheses for better-denominated and temporally resolved data.
- **Length reduced from five sentences to five shorter ones**; no claim was dropped.

### cns-writing checklist

- [x] Every claim in the conclusion appears earlier in Results or Discussion.
- [x] No new number, no new citation.
- [x] No causal language and no proof language in either direction.
- [x] The estimand qualifier ("first hospitalisations," "count ratios" by implication of the preceding text) is preserved.
- [x] No self-congratulation, no ceremony, no forward-looking programme statement beyond the data requirement.

---

## 5. Strengths and limitations

### Replacement text

**Strengths.** The twelve-contrast panel is reported in full rather than filtered to its largest estimates. Uncertainty is shown as an explicit four-construction ladder rather than as a single interval. Extreme-day exposures use published official thresholds. Identification displays show where cold-day variation and first-event decline come from. The daily-recovery analysis is reported as a refusal rather than as a coefficient.

**Limitations.** Admission cause was not recorded, so an event is a first hospitalisation after a first diagnosis and not a cardiac-caused admission. Inpatient-only semantics are inferred from the delivered column labels and are not yet confirmed. Monthly counts of cohort members still at risk of a first event were unavailable, so the estimates are count ratios rather than incidence-rate ratios [14]. The design is ecological and monthly, so individual-level and daily-triggering interpretations are not identified [14]. Age, sex, and disease-subtype strata were not delivered. Residual serial correlation remains material for CHD, with lag-1 Pearson autocorrelation of 0.508 in the hot-night model. Official cold days are concentrated in December–February, so the HF cold-day estimate rests on differences between winters. Official hot-night counts are not hourly nighttime excess heat [17]. Reference rules for monthly hot-tail and cold-tail indicators are not yet fixed, and no such indicator was used as a confirmatory exposure. Pollution, humidity, and influenza confounding is unresolved in the continuity panel. A stroke series was named in correspondence but was not delivered, and no stroke result is reported. External dissemination of the governed aggregates requires confirmation from the outcome and supervising investigators.

### What changed and why

- **Strengths converted from a comma list to sentences.** A five-item list in one sentence reads as a claim of merit; five short sentences read as a description of what was done. Each item now says what the alternative would have been ("rather than filtered," "rather than a single interval," "rather than as a coefficient").
- **Limitations given their consequences.** "Admission cause was not recorded" and "The analysis is ecological and monthly" were bare facts; each now states what it costs the interpretation. This is the difference between listing limitations and stating them.
- **The CHD autocorrelation limitation carries its value (0.508)**, which was previously only in Results and Discussion.
- **"Weather hot-month and cold-month reference rules remain unlocked" rewritten.** "Unlocked" is internal process vocabulary. The replacement states the scientific fact and the protective consequence: no such indicator was used as a confirmatory exposure.
- **The absent stroke series is stated once here**, which is the correct place for it. It was previously visible only in Methods, where a reader looking for scope limits will not find it.
- **"Cohort person-time still at risk of a first event was unavailable" made specific to monthly counts**, matching the say-map rule that the days offset standardises exposure time and does not supply cohort person-time.

### cns-writing checklist

- [x] Limitations match the monthly ecological design and the governed aggregate data; none is generic.
- [x] Each limitation is named once, with its consequence, and is not repeated for emphasis.
- [x] No uncertainty theatre and no apology; no "unfortunately," no "further work is needed" beyond the stated data requirement in the Conclusion.
- [x] Numbers traced: 0.508 (`chd_pathway_residual_acf.csv`), December–February concentration (temperature panel).
- [x] Governance is stated as a required confirmation from named roles, not as internal process.
- [x] No stroke result, no subtype, no age or sex claim, and no ICD detail.

---

## Merge notes for the parent session

- These five blocks replace the Abstract, Introduction, Discussion, Conclusion, and Strengths and limitations sections of `Heat_CVD_Manuscript_live_update.md`. Results, Methods, Tables 1–3, Figures 1–3, and the weather paragraph are unchanged and are not reproduced here.
- Reference numbering is unchanged. No citation is added, so `LIVE_DOC_EDITS.md` step 10 does not change.
- Three cross-section consistency points to preserve if the blocks are merged selectively: the NW3 unrounded bounds appear in Results and in Discussion paragraph 3; the 141/145 concentration appears in Results, Abstract, Discussion paragraph 2, and Limitations; and 0.508 appears in Results, Abstract, Discussion paragraph 3, and Limitations. Each is a deliberate repetition of an identification fact, not redundancy.
- If the parent prefers Hogan's comment 9 read strictly as a single closing statement, delete the final sentence of the Introduction. The objective sentence stands alone without it.
