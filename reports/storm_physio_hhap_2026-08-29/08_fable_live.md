# Fable-5 Max CLAIM-AUDIT (live) — 29 August 2026

**Role:** kill-list / overclaim. Not a Max model (quota-blocked). Same ruthlessness.

**Verdict: GO**

No numbered kill-list violation is presently in the live manuscript Discussion–References 23–33, the matching Hogan-builder Discussion strings, or the Laidlaw Discussion / Implications / Conclusion / Appendix Table A2. No manuscript edit. No replacement sentence.

`tests/test_storm_physio_hhap.py`: 10 passed.

---

## Surfaces read

- `reports/storm_physio_hhap_2026-08-29/06_kill_list.md` (items 1–23)
- `reports/storm_physio_hhap_2026-08-29/04_article.md` (authority draft; live STORM paragraphs match)
- `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` (Discussion through References 23–33; Abstract and Table 2 for the lock; Methods/Results only to see whether a kill leaked)
- `reports/laidlaw_stage3/laidlaw_research_report_2026.md` (Discussion, Implications, Conclusion, Appendix Table A2; Methods scanned for Wang/Ho/Gate 3)
- `scripts/64_hogan_20260824_manuscript_docx.py` (Discussion `for para in [...]` block matching the live file; `housing` / `medication` script contract)
- `tests/test_storm_physio_hhap.py`

## Table 2 lock (unchanged)

Live Abstract and Table 2, and Laidlaw Table 2 / Abstract:

- CHD hot nights / 5 days: **1.022 (1.002–1.042)**
- HF cold days / 5 days: **1.073 (1.006–1.144)**
- both *q* = **0.192**

6-df numbers (1.024, 1.005–1.044) appear only as a named robustness check. They do not replace Table 2.

## Numbered kill-list violations

**None.**

## Replacement sentences

**None.** Live markdown and builder left untouched.

---

## Kill-list 1–23 (pass with the quote that saves it)

A fail would have been a live or Laidlaw sentence that *asserts* the banned claim, not a sentence that names the same objects in order to refuse them.

| # | Banned claim | Result | Exact quote that decides it |
|---|---|---|---|
| 1 | Spline df 5/6/8 is heatwave duration or a myocardial threshold | PASS | Live Discussion: “The spline degrees of freedom are a model setting, and they do not describe a physiological duration.” Figure 3 caption (Results, not Discussion): “Neither the five-day scale nor the spline degrees of freedom refers to consecutive days.” Methods: “Those checks change the control for slow calendar time, not the length of a heatwave.” |
| 2 | A 5-df time-trend spline exists | PASS | No “5-df” / “5 df spline” in live body or Laidlaw. Trend checks named are 3, 4, 6, and 8 df. “Five days” is the reporting scale only. |
| 3 | Table 2 replaced by 6-df, or 6-df is confirmatory / physiology | PASS | Live Discussion: “If a single more-flexible robustness check is named, it is the 6-df spline, because the 8-df spline opens the HF cold-day interval onto 1. That is an identification property of the time smooth.” Results: “No trend specification is preferred over the 4-df spline in Model 1.” Table 2 remains the 4-df Model 1 lock. |
| 4 | `I(count/5)` is a consecutive-day warning identified from this panel | PASS | Live: “Five additional official days in a month is a reporting scale rather than a consecutive-day trigger.” Laidlaw: “Five additional official days is a reporting scale, not a consecutive-day trigger.” HHAP close: “The estimates do not set a five-day trigger.” |
| 5 | 2018’s 26 hot nights prove a five-night spell | PASS | 2018 appears only as the Model 3 calendar-day example (“For 15 July 2018”). No 26-night / five-night spell claim. |
| 6 | Wang 2019 / Ho 2017 mortality consecutive-night results are this panel | PASS | Ho 2017 absent from live and Laidlaw scientific body. Laidlaw Methods (outside the requested sections, scanned): “More complex heatwave definitions exist [@wang2019ehwe; @li2025heatwaves]; the six measures give the clearest common comparison.” That is a refusal to import, not a collapse. |
| 7 | Guo 2024 hourly nighttime excess heat is replicated by monthly official counts | PASS | Live: “The CHD hot-night residual should likewise be read against Guo et al. rather than as a replication of it [17].” Then: “A difference between monthly mean temperature and monthly official hot-night counts does not identify an intensity mechanism.” Laidlaw: “It should be read against Guo et al. rather than as a replication of that study.” Limitations: “Official hot-night counts are not hourly nighttime excess heat [17].” |
| 8 | Goggins and Chan 2017 RR 2.63 is the same estimand as 1.073 per five official cold days | PASS | 2.63 is in the Introduction only, with “their coefficients do not transfer to monthly counts of first hospitalisation.” Discussion physiology paragraph does not contain 2.63. Live: “Goggins and Chan’s daily Hong Kong HF series remains the local epidemiological neighbour, not a magnitude to import [21].” And: “A cumulative daily relative risk comparing 11 °C with 25 °C is not a monthly count ratio per five official cold days.” Laidlaw: “The comparison is between questions, not magnitudes.” |
| 9 | Law 2026 is an evaluation of VHWW by this panel | PASS | Law 2026 is not cited. Ref 30 is Chong and Law, HKO education page, December 2023, used to name the existing bundle. Live: “These estimates do not evaluate those warnings.” / “cannot evaluate any of them.” / “do not say whether existing warnings work.” |
| 10 | Ioannou n=7 young men *are* the Hong Kong T2D/HTN population | PASS | Live: “In a ten-day confinement study of seven young men, three nights at 26.3 °C left nocturnal core temperature 0.2 °C higher during and after those nights than before them… Those studies do not measure first CHD hospitalisation in Hong Kong.” Laidlaw: “Three laboratory hot nights left core temperature high into recovery in young men… Those papers do not measure first CHD hospitalisation here.” |
| 11 | O’Connor bedroom ≥24 °C *is* HKO Tmin ≥ 28 °C | PASS | Live: “In 47 adults aged 65 years or older, bedroom temperatures above 24 °C were associated with lower heart-rate variability [25]. Those studies… do not measure indoor temperature in this series.” HHAP: “it was not measured here (element 6).” Laidlaw limitations: “Headquarters weather is a territory-level proxy for neighbourhood, indoor and personal exposure.” Table A2 cannot-inform: “Indoor temperature or shelter use in this series.” |
| 12 | Ashe’s three studies prove hot nights abolish nocturnal dipping, raising CHD admissions | PASS | Live: “A scoping review found only three studies that linked extreme heat, sleep, and cardiovascular measures; blood-pressure findings were mixed, and none demonstrated sleep as a mediator of hospitalisation [26].” Laidlaw: “a scoping review found only three extreme-heat–sleep–cardiovascular studies, with mixed blood-pressure findings.” No dipping theorem. |
| 13 | Sleep, afterload, blood pressure, or infection *mediated* the present associations | PASS | Live nights: “The physiological claim is therefore a hypothesis… This panel does not identify that pathway.” Live cold: “The present counts do not measure afterload, blood pressure, or infection.” Limitations: “Physiological mechanisms and heat–health action-plan mappings are not identified from the 132 months.” Laidlaw: “None of these pathways is identified in 132 monthly counts.” |
| 14 | Indoor temperature, air-conditioning, or shelter use was measured | PASS | Indoor temperature: “they do not measure indoor temperature in this series” / “it was not measured here.” Air-conditioning and shelters are named as DH/HAD instruments, not as measured covariates. Table A2 cannot-inform: “Indoor temperature or shelter use in this series.” |
| 15 | Admissions were averted, or will fall if a warning is changed | PASS | Live: “do not count admissions averted.” Laidlaw: “I do not count admissions averted.” “Admissions were averted” is absent. No “will fall if a warning is changed.” |
| 16 | “We evaluated VHWW / Prolonged Heat / HKHI / Labour Heat Stress / Cold Weather Warning / an HHAP.” | PASS | Live: “Hong Kong already operates a warning, communication, and shelter bundle rather than a single named municipal plan evaluated here.” “This panel can inform four of those elements and cannot evaluate any of them.” “That overlap is a mapping, not a test of the alert.” “The estimates do not set a five-day trigger, do not count admissions averted, and do not say whether existing warnings work.” Laidlaw Table A2 header: “This table is a mapping, not an evaluation.” Instruments are named; they are not evaluated. “Six Model 1 measures were evaluated” (Laidlaw Methods) evaluates statistical encodings, not the warning system. |
| 17 | Hong Kong lacks heat–health instruments | PASS | Live: “Hong Kong already operates a warning, communication, and shelter bundle.” Laidlaw: “Hong Kong already has a warning, communication and shelter bundle.” |
| 18 | This panel should adopt or retire a numbered consecutive-day trigger | PASS | Live: “do not set a five-day trigger.” Laidlaw Implications: “The present findings do not justify disease-specific warning thresholds, a consecutive-day trigger, or an evaluation of Hong Kong’s existing warnings.” Table A2 cannot-inform: “A new consecutive-day trigger; whether warnings work.” |
| 19 | Gate 3 is closed; a primary headline is frozen | PASS | “Gate 3” absent from live scientific body and from Laidlaw Introduction–Conclusion / appendix tables. Live: “no model is promoted to a primary result.” “This analysis does not meet that bar.” Laidlaw: “no contrast is promoted to a primary result.” |
| 20 | Word `housing` in Hogan PDF builder output | PASS | Absent from live Discussion–References and from builder Discussion strings. Script still asserts `"housing" not in texts.lower()`. “Heat shelters” is not `housing`. |
| 21 | `medication` in the Hogan PDF | PASS | Absent. Script still asserts `texts.lower().count("medication") == 0`. |
| 22 | Gate 3 / pipeline / Tuesday lock in the scientific body | PASS | None of those tokens in live Discussion–Conclusion or Laidlaw Discussion–Conclusion–Table A2. Builder comment “In our pipeline, rainfall is a monthly total” is a Word comment on Hogan’s averaging sentence, not a body sentence. |
| 23 | Invented HA coefficients, stroke results, Model 2/3 health coefficients, or a real IRB number | PASS | Live IRB remains the placeholder `UW XX-XXX`. “A corresponding stroke series was not available for this analysis.” Laidlaw: “a stroke series was not delivered, and no stroke result is reported.” “Model 2 and Model 3 are specified; they have not been fitted to the governed health panel in this report, and no health coefficients are invented for them.” |

---

## Near-misses (not kills; no edit)

These were the only sentences that could have been stretched into a kill. They do not meet the list as written. They are recorded so the next audit does not re-promote them without new text.

1. **Identification vs physiology (live Discussion).**  
   Quote: “The contribution of this analysis is identification rather than estimation.”  
   Why not a kill: the same paragraph defines the four identification *displays* (which months, depletion, SE ladder, specification dependence). Limitations already say physiological mappings “are not identified from the 132 months.” Item 13 requires claiming mediation of the present associations. This sentence does not.

2. **Hypothesis “because” (live nights paragraph; `04_article.md` identical).**  
   Quote: “The physiological claim is therefore a hypothesis: nights may matter for CHD because overnight recovery of core temperature, sleep, and autonomic tone can fail, whereas a monthly very-hot-day count does not encode that failure. This panel does not identify that pathway.”  
   Why not a kill: the mechanism sits inside an explicit hypothesis label and is closed by the identification refusal. Item 13 is the mediation claim. It is not made.

3. **Laidlaw Implications hortatory clause.**  
   Quote: “They do support continued attention to both overnight heat and winter cold.”  
   Table A2 element 4 can-inform: “Overnight heat and winter cold both deserve continued attention.”  
   Why not a kill: the preceding Laidlaw sentence already refuses thresholds, a consecutive-day trigger, and warning evaluation (items 16 and 18). “Attention” is not “we evaluated VHWW” and is not “adopt a numbered trigger.”

4. **Table A2 drops the live hedge on the CHD residual.**  
   Quote: “CHD residual sits with official hot-night counts, not very-hot-day counts; Prolonged Heat already names nights.”  
   Live HHAP has “The CHD residual, such as it is.” The appendix table does not.  
   Why not a kill: Table A2 is headed “This table is a mapping, not an evaluation,” and the cannot-inform cell is “A new consecutive-day trigger; whether warnings work.” Mapping an unprotected residual onto an already-named instrument is not item 16.

5. **Laidlaw Ioannou compression.**  
   Quote: “Three laboratory hot nights left core temperature high into recovery in young men.”  
   Omits n=7, 26.3 °C, and 0.2 °C. Still “young men,” still “Those papers do not measure first CHD hospitalisation here.” Item 10 is identity with this cohort. It is not made. Live keeps the full numbers and is the journal surface.

6. **Guo “therefore” in the nights paragraph.**  
   Quote: “Guo et al. already showed that an official hot-night flag can be null after mean temperature while hourly nighttime excess heat is not [17]. The physiological claim is therefore a hypothesis…”  
   Why not a kill: Guo is cited for a published daily finding, then this panel’s claim is labeled hypothesis and not identified. The prior paragraph already refuses replication and intensity identification. Item 7 is “replicated by monthly official counts.” That sentence is not here.

---

## Builder ↔ live Discussion sync (STORM block)

These live openings are present in `scripts/64_hogan_20260824_manuscript_docx.py`:

- “A monthly official-day total does not distinguish consecutive days from days scattered through the month.”
- “Candidate mechanisms for a night residual sit outside this design.”
- “A corresponding hypothesis for HF is haemodynamic rather than nocturnal.”
- “This panel can inform four of those elements and cannot evaluate any of them.”
- “That overlap is a mapping, not a test of the alert.”
- Conclusion graft: “Physiological accounts of overnight recovery and cold-related afterload, and a mapping onto published heat–health action-plan elements, are interpretation. They are not identified effects and not an evaluation of Hong Kong’s warnings.”

Typographic only (not a kill): builder uses ASCII apostrophes and hyphenated “heat-health”; live markdown uses Unicode apostrophes and en-dashes. Wording of the claims is the same.

## Manuscript edits this pass

None. No kill-list violation is currently in the live file.

## Out of scope (not a live kill; do not treat as this verdict)

`00_topic.md` still says first CHD hospitalisation rose 1.022 “per five additional official hot-night days in a month after mean monthly temperature and other official warning counts.” Model 1 is separate-exposure. That sentence is not in the live manuscript, the builder Discussion, or the Laidlaw report. It is not part of this GO/NO-GO.
