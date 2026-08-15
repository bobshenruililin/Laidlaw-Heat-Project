# CNS writing checklist — `02_opus_prose.md`

**Target of the check:** `manuscript/cns_team/02_opus_prose.md` (drop-ins for `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md`).
**Standards applied:** `.cursor/skills/cns-writing/SKILL.md` (voice rules, forbidden phrases, completion checklist) and `analysis_plan/writing_standards_hogan.md`.
**Method of check:** each numeral was recomputed or re-read from the source CSV named in the audit table below; each rule was checked by reading the drop-in text and by pattern search.

---

## 1. Skill completion checklist

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Opening states the problem and estimand without throat-clearing | **PASS** | Abstract Background is two sentences and names the gap. Introduction sentence 1 states the setting; the estimand ("count ratio ... conditional on calendar month and a smooth function of time") appears in the first Methods paragraph. No scene-setting paragraph precedes either. |
| 2 | Each sentence carries one claim; redundant clauses cut | **PASS** | Methods, Results, and Limitations sentences were split at every "and ... and" junction. Abstract fell from 296 to 250 words; the daily-recovery sentence and the two autocorrelation values were removed from it because Methods, Results, and Supplement carry them. |
| 3 | Every quantitative statement checked against a source or verified real output | **PASS** | Section 4 below traces every quantitative claim to an `HA_APPROVED_AGGREGATE` or `REAL` table, or to a cited paper, one row per claim. Two fidelity corrections were made where the live draft did not survive the check (Section 5, items 1 and 3). |
| 4 | Citations formal, complete, attached to the claims they support | **PASS** | Introduction sentence 1 now cites [9] alone; [10] (Bhaskaran) appears only in Statistical analysis. [6] is attached to the 2023 exposure counts in the Introduction and in Results. [4] is attached to the 2021 record-count claim. [3] and [5] remain uncited and are flagged to the weather co-investigator rather than deleted, because references 1–8 are his block. |
| 5 | Collaborator contributions credited by role in the body | **PASS** | "the outcome co-investigator" (Health data), "a clinical collaborator" (diagnosis-record construction), "the weather co-investigator" (heatwave-spell and hot-month rules). Personal names stay in Acknowledgements, which this pass does not change. |
| 6 | No draft markers, process gossip, internal gate language, or admin logistics in the scientific body | **PASS** | Pattern search for `continuity`, `pipeline`, `Gate 3`, `F1.x`, `Laidlaw`, `TBD`, `work in progress`, `placeholder` returns no hit inside any prose section. "Frozen calibration gates" became "frozen calibration criteria" (Methods) and "worst-cell criteria" (Results). The two remaining editorial instructions are HTML comments (`HOGAN_WEATHER_VERBATIM`, `OUTCOME_CO-I_TO_CONFIRM`), which do not render. |
| 7 | Results distinguish effect estimates, CIs, exposure prevalence, missingness, diagnostics | **PASS** | Separate Results subsections: outcome series, exposure context, core panel (Table 2), uncertainty ladder (Table 3), joint models and residual diagnostics, sensitivity analyses (Figure 3), daily-recovery calibration. Influenza coverage (121 of 132) and the pollutant 75% completeness rule are in Methods. |
| 8 | Null, discordant, and sensitivity estimates are not hidden | **PASS** | All twelve contrasts are tabulated, including ten near-null ones. The CHD hot-night pre-2020 (1.011, 0.991–1.032) and COVID-phase (1.013, 0.994–1.033) intervals now appear in Results, Abstract, Discussion, and Limitations, matching the prominence given to the HF pre-2020 strengthening. The HF minimum-temperature upper bound of 1.00005 is stated. |
| 9 | Daily mortality, modelled excess mortality, and monthly morbidity not conflated | **PASS** | Liu et al. (2020) attributable fractions and Liu et al. (2026) excess deaths are labelled mortality burden quantities in the Introduction, and "cannot be rescaled into the present count ratios" in the Discussion. Goggins and Chan's cumulative daily relative risk is compared as a question, not a magnitude, and the numeral 2.63 does not appear in the Discussion. |
| 10 | Limitations match the monthly ecological design and governed aggregate data | **PASS** | Limitations name admission cause, inferred inpatient semantics, missing at-risk person-time, ecological grain, absent strata, CHD serial correlation, December–February cold-day concentration, window instability of the CHD estimate, the single measurement station, unfixed tail definitions, unresolved confounding, the undelivered stroke series, and the release requirement. |
| 11 | No claim exceeds the provenance of the data | **PASS** | No causal verb is attached to any monthly estimate; the words "caused", "proved", and "demonstrated" do not appear in reference to our estimates. The Conclusion claims hypotheses and an account of limits, not an effect. The contribution paragraph claims reporting practice. |
| 12 | Register matches `essay_lit_methods.md` and Hogan's standard | **PASS** | Spare declaratives, no metaphor, no rhetorical question, no self-congratulation. The Stage 3 essay was used for register only: its stroke framing, future-tense planned methods, and multi-definition family tables were not imported. |
| 13 | Mode does not make incomplete science sound complete | **PASS** | Exploratory status is stated in Abstract, Study design, Statistical analysis, and Results. No team freeze is declared, and no contrast is promoted to a primary result. |

## 2. Non-negotiable voice rules

| Rule | Verdict | Evidence |
|---|---|---|
| Plain, digestible academic English | **PASS** | Measured per section: longest sentence is 35 words in Results (an enumeration of four calibration criteria), 40 in Discussion, 37 in the Abstract, 36 in the Conclusion, and 25 in Limitations. The one 49-word sentence is inside the weather co-investigator's verbatim paragraph and was not touched. |
| One substantive claim per sentence | **PASS** | Sentences carrying two claims were split during the check: the autocorrelation and Ljung–Box sentence, the two-outcome Discussion comparison, the pollution trend sentence, the Goggins and Chan design-and-estimate sentence, and the four-display contribution sentence. |
| Concrete estimands, effect sizes, CIs, exposure counts, limitations over rhetorical summary | **PASS** | Every Results paragraph carries either an estimate with interval, an exposure count, or a diagnostic. |
| No ceremony sentences | **PASS** | Removed "These findings establish ..."-style bridges where they added no information; removed the Abstract's method sentence duplicated from Methods. |
| Consistent numbered citations | **PASS** | [1]–[21] retained as in the live draft; no reference added, renumbered, or invented. |
| Mortality AF / excess deaths / monthly morbidity kept distinct | **PASS** | See item 9 above. |
| Collaborators credited by scientific role | **PASS** | See item 5 above. |
| Completed procedures in past tense | **PASS** | Methods are uniformly past tense; no planned-procedure future tense survives from the Stage 3 exemplar. |
| Associations described as associations | **PASS** | "was associated with", "count ratio", "residual signal". No mechanism is asserted. |
| Uncertainty preserved without theatre | **PASS** | Each limitation is named once, in Limitations, with at most one echo where it decides interpretation (CHD serial correlation and window dependence). |

## 3. Brief-specific rails

| Rail | Verdict | Evidence |
|---|---|---|
| Hogan's weather paragraph verbatim, including "Meteorological data was obtained from the HKO." | **PASS** | Enclosed in `HOGAN_WEATHER_VERBATIM` markers. String comparison of the enclosed block against the weather paragraph in the live file returns exact equality, including the non-breaking punctuation and the `T~min~`/`T~max~` subscript markup. |
| Author 2–4 placeholders stay | **PASS** | Author line reproduced unchanged, including the footnote on author order. |
| No Gate 3 freeze, no discovery claim, no journal-suitability claim | **PASS** | No freeze language anywhere; Conclusion claims hypotheses; the contribution paragraph claims reporting practice. |
| Forbidden vocabulary (Gate 3, pipeline, F1.1, continuity, Laidlaw, "remarkably", "novel", "it is important to note") | **PASS** | Pattern search returns no hit in prose. "Core panel" is used throughout and is defined once in Study design. |
| Forbidden content: stroke coefficients; AMI as our endpoint; HM/CM estimates; health-economic parameters; daily DLNM coefficients; 2.63 vs 1.073; 3.1% vs 1.022; sleep/BP mediation; 2019 as a health experiment; 2024 as a health year | **PASS** | No stroke estimate appears; AMI appears only as Goggins et al. (2013) history and in the not-identified list; no HM/CM or health-economic quantity appears; no daily coefficient is reported; the two literature magnitudes are never set against ours; the sleep and blood-pressure clause was deleted from the Discussion; 2019 appears only as a one-cold-day exposure fact; 2024 does not appear. |
| Results only from `HA_APPROVED_AGGREGATE` / `REAL` / cited papers | **PASS** | Section 4 audit table. |
| Allowed number set respected | **PASS with one flagged correction** | All numerals are from the brief's allowed set, with the Ljung–Box threshold corrected from 10^−8^ to 10^−7^ (Section 5, item 1). No number outside the set entered the prose; the verified cold-day-month count is recorded in the prose file's "Notes for the parent session" instead. |
| Archive influenza numeral moved out of the Discussion | **PASS** | Discussion states direction and points to the accompanying release; 1.673 (1.249–2.243) does not appear in any drop-in section. |
| Figure 3 replaced by the trend-depletion sensitivity figure; autocorrelation demoted | **PASS** | Figure 3 is `outputs/release_chd_hf/figures/figure4_trend_depletion_sensitivity.png`; the autocorrelation values are one Results sentence with "(see Supplement)". |
| Citation fixes: [9] alone in sentence 1; [6] on 2023 exposure counts; [10] in Statistical analysis | **PASS** | Checked in place. |
| Do not edit the live file or Stage 3 outputs | **PASS** | Only `manuscript/cns_team/` files were written; `git status` shows no modification to the live draft or to `reports/laidlaw_stage3/`. |

## 4. Number audit

Two layers were used. First, a machine check parsed every estimate-with-interval statement out of the seven prose sections and required each one to match an `rr`, `rr_low`, `rr_high` triple in a governed output table at the precision printed: 33 statements checked, 0 unmatched. The same check compared all twelve Table 2 markdown rows against `table2_core_models.csv` cell by cell (0 mismatches), confirmed the Ljung–Box thresholds, confirmed that the weather paragraph is identical to the live file, and confirmed that 2.63 appears only in the Introduction and that 1.673 appears nowhere. Second, the remaining claims — counts, prevalences, percentages, and cited-paper values — were read against source by hand, as listed below. All CSV paths are relative to the repository root.

| Claim as written | Source | Verified |
|---|---|---|
| CHD 156,156 events; mean 1,183.0 per month | `outputs/release_chd_hf/tables/table1_outcome_summary.csv` | Yes (1183 stored; 1,183.0 as displayed) |
| HF 29,681 events; mean 224.9 per month | same | Yes |
| CHD annual 23,830 → 12,323; HF 4,336 → 2,296; 2020 dip CHD 10,237, HF 1,964 | `outputs/tables/cvd_descriptive_annual_totals.csv` | Yes |
| Population aged 35+ rose 17% | same table, `mean_population` 4,430,186 → 5,188,660 (ratio 1.171) | Yes |
| CHD January 1,386 and September 1,097; HF January 287 and September 196 | `outputs/tables/cvd_descriptive_seasonality_by_month.csv` (1386.27, 1097.09, 286.91, 196.36) | Yes |
| Hot nights 10 (2013), 61 (2021), 56 (2023) | `outputs/live_identification/cold_days_by_month_year.csv`, summed by year | Yes |
| Very hot days 17 → 54, and 54 in 2023 | same | Yes |
| Cold days 14 (2013), 1 (2019), 13 (2021), 14 (2023) | same | Yes |
| 2013 hot nights about seven days below the 1981–2010 normal | REAL HKO Year's Weather 2013 [2], via `claim_ledger.md` | Yes (cited claim) |
| 2021 the highest annual hot-night count in the Observatory record at that time | HKO 2021 yearbook [4], corroborated in `knowledge/2026-08-13_pi_hko_yearbook_check.md` and `knowledge/2026-08-13_kimi_web_weather_lit_harvest.md` | Yes; wording weakened from the live draft (Section 5, item 3) |
| 145 cold days; 141 in December–February (December 40, January 54, February 47); 4 in March | `outputs/live_identification/cold_days_by_month_year.csv`, recomputed | Yes |
| NO₂ 53.7 → 32.1; PM2.5 30.8 → 14.6; O₃ 42.6 → 58.3 µg m^−3^ | `outputs/tables/pollution_annual_means_general_2013_2023.csv` (53.72/32.08; 30.83/14.56; 42.61/58.31) | Yes |
| Table 2, all twelve count ratios, *p*, and *q* | `outputs/release_chd_hf/tables/table2_core_models.csv` | Yes, row by row |
| Minimum *q* = 0.192; all twelve > 0.19 | same, `q_value_core_bh` (min 0.19224) | Yes |
| HF mean-minimum-temperature unrounded upper bound 1.00005 | same, `rr_high` = 1.00004966 | Yes |
| Table 3 ladder, CHD hot nights: 0.995–1.049, 0.997–1.047, 1.0003–1.0439, 1.002–1.042 | `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` | Yes |
| Table 3 ladder, HF cold days: 1.023–1.125, 1.011–1.138, 1.007–1.143, 1.006–1.144 | same | Yes |
| NW3 CHD hot nights unrounded 1.000253–1.043860 | same (1.0002531783659, 1.04386043738117) | Yes |
| VIF 4.66 for maximum and minimum temperature; near 1.96 for hot nights and very hot days | `outputs/tables/cvd_exposure_vif.csv` (4.6585; 1.9581 and 1.9579) | Yes |
| Joint CHD hot nights 1.045 (1.015–1.075) | `outputs/tables/cvd_single_vs_joint_estimates.csv`, Newey–West lag 6 (1.0447, 1.0154–1.0748) | Yes |
| Joint HF cold days 1.073 | same (1.0728) | Yes |
| Lag-1 autocorrelation 0.508 (CHD hot nights) and 0.146 (HF cold days) | `outputs/tables/chd_pathway_residual_acf.csv`, `outputs/tables/hf_pathway_residual_acf.csv`, lag 1 | Yes (0.50780, 0.14554) |
| Ljung–Box lag 6: *p* < 10^−7^ for every CHD core model; *p* > 0.3 for every HF core model | `outputs/tables/chd_pathway_core_diagnostics.csv` (max 1.17 × 10^−8^), `outputs/tables/hf_pathway_core_diagnostics.csv` (min 0.319) | Yes; threshold corrected (Section 5, item 1) |
| CHD hot-night range 1.011–1.025; HF cold-day range 1.043–1.113 | `outputs/tables/cvd_trend_depletion_sensitivity.csv`, nine specifications | Yes (1.0110–1.0246; 1.0429–1.1128) |
| "Offset choice changed the core count ratios only trivially" (no numeral) | `outputs/tables/cvd_offset_sensitivity.csv` (CHD hot nights 1.0215–1.0218; HF cold days 1.0728–1.0751 across the three offsets) | Yes |
| HF cold days pre-2020: 1.113 (1.053–1.176) | same, `pre_covid` (1.11283, 1.05304–1.17602) | Yes |
| CHD hot nights pre-2020: 1.011 (0.991–1.032) | same, `pre_covid` (1.01098, 0.99076–1.03162) | Yes |
| CHD hot nights COVID-phase adjusted: 1.013 (0.994–1.033) | same, `covid_phase_adjusted` (1.01322, 0.99416–1.03264) | Yes |
| CHD hot nights lag 1: 1.010 (0.979–1.042) | `outputs/tables/cvd_lag_sensitivity.csv` (1.00993, 0.97912–1.04170) | Yes |
| HF cold days lag 1: 1.073 (1.014–1.135); lag 2: 1.053 (0.985–1.127) | same (1.07305, 1.01449–1.13500; 1.05349, 0.98488–1.12687) | Yes |
| Largest Cook's distance months: February 2020 (CHD), February 2022 (HF cold days) | `outputs/tables/cvd_influence_sensitivity.csv`, `excluded_month` | Yes |
| After excluding the most influential month: CHD 1.021 (1.001–1.040); HF 1.088 (1.034–1.144) | same (1.02067, 1.00147–1.04024; 1.08756, 1.03425–1.14361) | Yes |
| Daily-recovery criteria: Type I 0.048–0.150; minimum coverage 0.840; maximum relative bias 32.8; maximum false-sign rate 0.808 | `outputs/calibration_md/md_calibration_gate_summary.csv` (0.0480–0.1500; 0.84; 32.7742; 0.808) | Yes |
| Influenza coverage 121 of 132 months | `outputs/tables/combined_pathway_panel_estimates.csv`, P14 `n_months` = 121 | Yes |
| Goggins et al. 2013: 3.7% per 1 °C below about 24 °C; no significant heat association in three cities | [1] via `claim_ledger.md` | Yes (cited) |
| Goggins and Chan 2017: cumulative RR 2.63 (2.43–2.84), 11 °C versus 25 °C, lags to 23 days, 2002–2011 | [21] via `claim_ledger.md`; Introduction only | Yes (cited) |
| Guo et al. 2024: official hot-night flag −0.2% (−1.2% to 0.7%) over lags 0–4; hourly excess heat +3.1% (1.5–4.8%) | [17] via `claim_ledger.md` | Yes (cited) |
| Liu et al. 2020: 4.72% cold versus 0.16% heat; 4.25% moderate versus 0.63% extreme | [12] via `claim_ledger.md` | Yes (cited) |
| Liu et al. 2026: 1,455–3,238 modelled excess heat deaths, 2014–2023 | [13] via `claim_ledger.md` | Yes (cited) |
| Software: R 4.3.3, MASS 7.3-60.0.1, sandwich 3.1.3 | `claim_ledger.md`, session 12 August 2026 | Yes |

## 5. Findings that changed the prose

1. **Ljung–Box threshold was wrong by a hair in the live draft.** The live Results state *p* < 10^−8^ at lag 6 for CHD. The largest CHD core lag-6 *p*-value is 1.17 × 10^−8^ (`chd_pathway_core_diagnostics.csv`, P04A, the hot-night model), which is above 10^−8^. The drop-in states *p* < 10^−7^, which holds for all six CHD core models, and *p* > 0.3 for all six HF core models (minimum 0.319). This is a weakening of an allowed number rather than a new one.
2. **The 13 August critique's "roughly 33–37 months" estimate is too high.** Recomputed from `outputs/live_identification/cold_days_by_month_year.csv`, 29 of 132 months carry at least one official cold day. The figure is outside the allowed number set for this pass, so it is recorded in the prose file's notes rather than written into the manuscript. If the team wants the effective-information point, 29 is the number, and it strengthens the between-winters argument.
3. **The 2021 hot-night record claim was uncited and slightly over-stated.** "Highest annual number of hot nights in the Observatory record through the study window" mixed a full-record claim with a window claim. The drop-in reads "the highest annual number of hot nights in the Observatory record at that time [4]", which is what the 2021 yearbook supports and what the PI yearbook check records.
4. **Uncited references remain.** [3] (2017 yearbook) and [5] (2024 yearbook) are still uncited in the body. They are the weather co-investigator's block and are flagged, not deleted.

## 6. Overall verdict

**PASS.** The drop-ins are paste-ready for the live collaborative file. Three items need a human decision before or at merge: the uncited references [3] and [5]; whether to keep the archive influenza numeral in the release only, as written here, or restore it to the Discussion; and whether the 29-month cold-day exposure count enters the paper. None of the three blocks the paste.
