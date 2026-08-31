# Sol 5.6 Max — live HHAP routing and Stage 3

**Date:** 29 August 2026  
**Seat:** HHAP-routing and Stage-3 role. Not Sol 5.6 Max (that model is quota-blocked). Same kill-list / mapping / programme-band pass.

**Surfaces read:** `05_hhap_crosswalk.md`; live WHO HHAP paragraph in `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`; Stage 3 Implications, Discussion, and Appendix Table A2 in `reports/laidlaw_stage3/laidlaw_research_report_2026.md`; `tests/test_stage3_hogan_align.py`; `tests/test_storm_physio_hhap.py`.

## Verdict

**GO.** No Stage 3 or live HHAP overclaim that requires a prose edit. Introduction–Conclusion remains 2,989 words (band 2,000–3,000). Models 2–3 stay specified and unfitted. No health coefficients invented. PDFs not rebuilt.

## Checks

| Check | Finding |
|:--|:--|
| Invented municipal HHAP? | **No.** Live: Hong Kong “operates a warning, communication, and shelter bundle rather than a single named municipal plan evaluated here.” Stage 3: “already has a warning, communication and shelter bundle.” Neither file invents a WHO-branded municipal HHAP. |
| Warning evaluation? | **No.** Live: “cannot evaluate any of them”; “mapping, not a test of the alert”; “do not say whether existing warnings work.” Consecutive-days paragraph (test-locked): “These estimates do not evaluate those warnings.” Stage 3 Implications: “do not justify … an evaluation of Hong Kong’s existing warnings.” Table A2 title: “a mapping, not an evaluation.” |
| Table A2 can/cannot honest? | **Yes.** Eight WHO 2026 elements each have an instrument cell, a can cell, and a cannot cell. Positive mapping is elements 2, 3, 4, 6 (hot-night residual vs very-hot-day counts; named at-risk group already includes this cohort; overnight heat and winter cold; indoor night temperature as unmeasured hypothesis). Elements 1, 5, 7, 8 can-cells are negative knowledge (authorities exist; not a surge dashboard; monthly grain cannot activate; evaluation would need daily cause-recorded data). Cannot-cells refuse a new consecutive-day trigger, whether warnings work, a new named group, message-testing, staffing, indoor temperature/shelter use, event-day surveillance, and this report as an evaluation. Cold-weather counterpart is labelled as not a WHO heat element. |
| WHO 2026 eight × HK bundle named? | **Yes, live paragraph.** Governance; heat–health warning system; populations at increased risk; communication; health-system resilience; reducing heat exposure; heat–health surveillance; monitoring, evaluation and learning. Bundle: Very Hot Weather Warning; Hot Weather Special Advisory; Prolonged Heat Special Alert (a few days of very hot days *or* hot nights while that warning is in force); Extremely Hot ~35 °C; HKHI; CHP heart disease or high blood pressure; HAD temporary heat shelters; Cold Weather Warning. Stage 3 Implications names the bundle, Prolonged Heat, and CHP diagnoses, and points to Table A2 for the rest. |
| Stage 3 Model 1/2/3; Models 2–3 unfitted; no invented coefficients? | **Yes.** Abstract: “Reported estimates are from Model 1.” Methods: “Model 2 and Model 3 are specified; they have not been fitted to the governed health panel in this report, and no health coefficients are invented for them.” Limitations item 4 repeats unfitted. Table 2 and Table A1 are Model 1 only. No Model 2/3 count ratios appear. Banned phrases `core panel` / `Gate 3` absent. Poster: “specified, not shown.” Required numbers present: 156,156; 29,681; 1.022; 1.073; 0.192; 1.011; 1.113. |
| Overclaim of 5-day trigger / admissions averted / indoor T? | **No.** Live: “do not set a five-day trigger, do not count admissions averted”; indoor night temperature “was not measured here.” Stage 3: “Five additional official days is a reporting scale, not a consecutive-day trigger”; “I do not count admissions averted”; Table A2 element 6 cannot: “Indoor temperature or shelter use in this series.” `I(count/5)` remains a reporting scale. |
| Heat-only plans miss stronger HF-cold residual? | **Stated, not overclaimed.** Live: “A heat-only plan would omit the stronger HF cold-day residual, which sits with the Cold Weather Warning rather than with summer heat guidance.” Stage 3 Implications: continued attention to both overnight heat and winter cold. Table A2 cold counterpart: “The more coherent residual here is HF × official cold days.” No invented winter coefficient in Table A2. |

## Specific edits

**Applied:** none. No real overclaim in the live HHAP paragraph or in Stage 3 Implications / Table A2 / Discussion.

**Optional (not applied; not required for GO):**

1. Live HHAP: “when that warning is in force” is readable as the Very Hot Weather Warning (the only product in the list named a warning). If a copy-editor worries that the nearest noun is the Hot Weather Special Advisory, replace with “when the Very Hot Weather Warning is in force.” Chong and Law (December 2023) define Prolonged Heat as a few days of very hot days *or* hot nights while VHWW is in force. This is disambiguation, not a claim fix. The Hogan PDF builder would have to stay in lockstep.
2. Table A2 element 2 instrument cell omits “while VHWW is in force.” The live paragraph and `05_hhap_crosswalk.md` already carry it. Adding those five words would match Chong/Law. Appendix is outside the word band. Do not rebuild the PDF unless Bob wants that five-word graft.
3. Stage 3 Implications “They do support continued attention to both overnight heat and winter cold” is the softest policy-adjacent sentence. It is bounded by the preceding refusal of thresholds, a consecutive-day trigger, and evaluation. Replacing it with the live heat-only/HF-cold sentence would add about one word (still inside 3,000) and is a register preference, not a kill.

Do not apply (1)–(3) unless a human asks. Word band is 11 words from the ceiling. A XeLaTeX rebuild is required only if `laidlaw_research_report_2026.md` changes; it did not.

## Stage 3 contract (re-checked)

- Introduction–Conclusion: **2,989** words (test band 2,000–3,000).
- Model 1 shown; Model 2 humidity/rainfall specified, not fitted; Model 3 climatology day-counts specified, not fitted; “no health coefficients are invented.”
- No `core panel`. No `Gate 3`.
- Essay PDF SHA prefix `f55f8f14f214bc92` (unchanged; no markdown edit). Poster SHA prefix `a972206e61932650` (unchanged).
- If form 2a was already signed against `605cd8db43072cb5`, that remains a human decision.

## What this seat does not do

Does not freeze Gate 3. Does not paste into Hogan’s shared file. Does not evaluate VHWW, Prolonged Heat, HKHI, Labour Heat Stress, or Cold Weather Warning. Does not invent Model 2/3 coefficients, indoor temperature, admissions averted, or a five-day consecutive trigger.
