# Round A — independent evidence, data, and collaboration audit (15 August 2026)

**Auditor:** Fable-5 Max, independent Round A. No favored thesis received. Primary sources re-fetched this session where public: HKO Year's Weather 2013 and 2021 pages, ORA abstracts for Goggins 2013 and Goggins 2012, the IJC record for Goggins and Chan 2017, the Guo 2024 full text (ORA copy, Table 3), the Liu 2020 abstract record, and Springer/Crossmark for Yang Z 2025. Liu 2026 was checked against the repo's deep-read of the medRxiv v1 / private revised PDF only. Project CSVs re-read: `outputs/tables/pollution_annual_means_general_2013_2023.csv`.

**Headline.** No numeric mismatch was found between any quoted literature or exposure number and its primary source. The defects are attachment and pointer defects: two uncited references, two numeric claims resting on portal-landing-page citations, figures cited out of numerical order, and one word of looseness in the Liu 2020 sentence. The comment dispositions are scientifically adequate; on comment 4 this audit recommends flipping the D3 default from (a) omit-everywhere to (b) one Limitations clause.

---

## 1. Comment-by-comment audit (Hogan / Bishai / reviewer / reader)

### Comment 0 — running title provisional until Results

Disposition: title renamed to the delivered estimand; strikeable italic note; short running head left to Hogan (D1).

- **As Hogan:** He asked for amendment once results exist. Results exist; the title now names what was actually analysed, and the running-head decision stays his. Responsive.
- **As Bishai:** The title no longer promises AMI/stroke or an effect; it names outcome, population window, and city. Governance-safe.
- **As reviewer:** Accurate, non-claiming title. Long, but honest length is not a defect. The italic working-title note must not survive into a submitted file.
- **As reader:** Immediately knows the outcome is first hospitalisation after diagnosis, not cause-coded admission.
- **Verdict: adequate.** Remaining half (short head) is genuinely a human decision; keep D1 open.

### Comment 1 — Authors 2–4

Disposition: placeholders retained; roles in Acknowledgements only.

- **As Hogan / as Bishai:** Correct order of operations; no order asserted that the team has not made.
- **As reviewer:** Irrelevant until submission, at which point placeholders are a desk-reject.
- **As reader:** Neutral.
- **Verdict: adequate as interim; submission-blocking by design** (D2).

### Comment 3 — remove "Acute myocardial infarction and" (scope changed)

Disposition: removed as endpoint; Goggins 2013 kept as daily AMI history; Goggins and Chan 2017 added as the nearer daily HF anchor; full-file sweep confirmed no AMI/stroke coefficient anywhere.

- **As Hogan:** His question was answered with an action plus an inspection, not just a deletion. The added 2017 HF anchor is the right upgrade — it is closer to the present outcome than AMI or stroke history.
- **As Bishai:** Consistent with the 17 July recalibration; no AMI claims restored anywhere. Verified this session.
- **As reviewer:** Introduction and endpoints are now aligned. The stroke history sentence [11] survives although stroke is not studied; it is defensible as part of "local evidence is daily, diagnosis-specific, earlier decades," and the Limitations disclose that stroke was named but not delivered. Acceptable; trimming it is a taste call, not a correctness call.
- **As reader:** The history/estimand distinction is stated explicitly ("their coefficients do not transfer to monthly counts of first hospitalisation").
- **Verdict: adequate.** Nothing to restore.

### Comment 4 — cite the factors; drop housing/behaviour if unmeasured; consider medication

Disposition: housing, behaviour, AC dropped; medication **also** dropped, with evidence (no ATC/prescription field in the variable dictionary or release outputs); appendix listing rejected; mechanism reviews [9,10] kept as general citations.

- **As Hogan:** The reply applies his own stated rule (do not dangle uncontrolled factors) to his own suggestion (medication), with a checkable evidence trail. That is the right way to decline a mentor's suggestion. The ledger correctly leaves him the option of a Limitations mention (D3 option b).
- **As Bishai:** Medication/BMI were his July ambition; the disposition documents that they were not delivered rather than quietly pretending they never existed. Correct.
- **As reviewer:** Here this audit departs from the ledger's default. The dangling-factor rule protects the *Introduction*; the *Limitations* section exists precisely to name what was not controlled. Any competent referee of a 2013–2023 T2D/HTN cohort will raise secular treatment change unprompted. Silence in Limitations will read as an oversight, not as discipline — especially since Limitations already names other undelivered items (age, sex, subtype strata). One factual clause ("medication and treatment-pattern data were not included in the aggregates; slow secular change in therapy is absorbed by, and not separable from, the trend spline") answers the question before it is asked, adds no number, and controls the framing.
- **As reader:** Currently cannot tell whether medication was forgotten or unavailable.
- **Verdict: scientifically adequate as stands; recommend flipping the D3 default from (a) to (b)** — Introduction stays clean either way. Hogan owns the call.

### Comment 8 — "environmental context has also evolved" reads as post-2009 pollutant change

Disposition: rewritten to 2013–2023 general-station means (NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 µg m⁻³) with an explicit "not a reconstruction of 2000–2009" sentence; "pathway variable" language removed; direction cross-checked against the GIA annex integers.

- **As Hogan:** He said "Research." The research was done, primary-sourced, and the sentence no longer implies the comparison he objected to. His literal question (did pollutants change *after* 2009?) was made moot by reframing rather than answered; if he wants the 2009→2013 bridge, EPD public series reach back to 2000 and the GIA annex covers 2011–2023, so it is buildable — but it is not needed for the present claim.
- **As Bishai:** The within-window claim is the one the design can carry; the ozone-coupling justification for staged adjustment is stated without over-claiming confounding resolution.
- **As reviewer:** The numbers verify against the project CSV exactly (53.72→32.08; 30.83→14.56; 42.61→58.31) and against the GIA integers in direction and rounded magnitude. Two hygiene items: reference [7] is a query portal, not a document — add an access date or cite the GIA annex PDF; and the 2023 GIA figures were marked preliminary in February 2024, so a final-figures re-check before submission is cheap insurance.
- **As reader:** Clear, and the "not interchangeable covariates" sentence prevents the usual misreading.
- **Verdict: adequate.** Best-handled comment in the set.

### Comment 9 — combine the thesis into one sentence; amend after Results

Disposition: one closing estimand sentence; alternatives parked in the approach registry; freeze deferred to team Gate 3.

- **As Hogan:** Exactly what he asked, in the order he asked it (one sentence now, amend after the team locks emphasis).
- **As Bishai:** Nothing is pre-frozen; Gate 3 stays a team decision (D4). Option A remains the lead recommendation.
- **As reviewer:** The aims sentence describes the estimand and the parallel heat/cold carry without smuggling a result. It matches what Results deliver.
- **As reader:** Knows what question the paper answers before Methods begin.
- **Verdict: adequate.**

### Comment 54 — Yang CY, not Yang C-Y

Disposition: kept as `Yang CY`.

- **All four lenses:** Correct. The author is Chun-Yuh Yang; NLM style is `Yang CY`. Verified against the ORA/Semantic Scholar author records this session.
- **Verdict: adequate; closed.**

---

## 2. Citation verification table (claim, source, supports?, residual risk)

| # | Live-file claim | Cited source | Primary check this session | Supports? | Residual risk |
|---|---|---|---|---|---|
| 1 | 1 °C below ~24 °C → +3.7% AMI admissions, Hong Kong, 2000–2009 | Goggins 2013 [1] | ORA abstract: "3.7% (average lag 0–13 temperature) in Hong Kong… threshold temperature of 24°C," p<.0001 | **Yes, exact** | None material; lag detail lives in the ledger, not the sentence |
| 2 | No significant heat association in HK/Taipei/Kaohsiung; same-day NO₂ strongest pollutant | Goggins 2013 [1] | ORA abstract: "No significant heat effects were observed"; "same day NO2 levels were the strongest predictors in all three cities" | **Yes, exact** | None |
| 3 | Author string `Yang CY` (comment 54) | Goggins 2013 [1] | Author is Chun-Yuh Yang | **Yes** | None |
| 4 | Cumulative RR 2.63 (2.43–2.84), 11 °C vs 25 °C, lags to 23 days, daily public-hospital HF admissions 2002–2011 | Goggins & Chan 2017 [21] | IJC abstract: identical values, window, lag span; public hospitals ≈83% of admissions | **Yes, exact** | Unused ally: the paper found the cold association stronger for **new** hospitalisations than recurrent — directly relevant to a first-event outcome; optional half-sentence if Hogan wants it |
| 5 | Official hot-night flag: excess RR −0.2% (−1.2% to 0.7%), lags 0–4, after mean-temperature adjustment | Guo 2024 [17] | Full-text Table 3, All NCNE row: −0.2 (−1.2, 0.7); models adjust for mean temperature averaged over lags 0–3 | **Yes, exact** | None |
| 6 | Hourly excess-heat metric, 20:00–07:59; +3.1% (1.5–4.8%) at its extreme value | Guo 2024 [17] | HNe window is 20:00 (D(t−1)) to 07:59 (D(t)); 99th pct 28.9 °C·h vs 0: 3.1 (1.5, 4.8) | **Yes, exact** | None |
| 7 | "Daily unplanned emergency hospitalisations… hot seasons of 2000–2019"; did not study first CHD/HF in a T2D/HTN cohort | Guo 2024 [17] | "Only emergency admissions without a plan were included"; May–October 2000–19; outcomes are NCNE and cause groups | **Yes** | None |
| 8 | Cold AF 4.72% vs heat 0.16%, 2006–2016 | Liu 2020 [12] | Abstract: AF 4.72% and 0.16% | **Yes** | Wording: those AFs are **total-mortality** figures inside a cause-specific study; "cold-dominant attributable fraction for cause-specific mortality" is one word loose — say "for mortality" |
| 9 | Moderate 4.25% vs extreme 0.63% | Liu 2020 [12] | Abstract: "Moderate temperatures played a major role in all-cause mortality with AF of 4.25%, and 0.63% for extreme" | **Yes** | Same all-cause nuance; full PDF still not in repo — abstract-level verification only |
| 10 | 1,455–3,238 model-based excess heat deaths 2014–2023, range from heatwave definition | Liu 2026 [13] | Repo deep-read: 1,455 (1,098–1,812) under `HWD_Tavg`; 3,238 (3,234–3,242) under `HWD_Tcombined`; four definitions | **Yes, as complementary mortality** | Preprint (v1) with a private revised PDF; numbers may move on revision; DOI not independently resolvable in this session; team self-citation (Bishai on both) — keep "model-based" and definition-dependence wording, which the live sentence already has |
| 11 | 2013: 10 hot nights, "about seven days below the 1981–2010 normal"; 17 very hot days; 14 cold days | HKO Year's Weather 2013 [2] | Live page fetched: prose "only ten Hot Nights… about seven days below normal"; Table 3 totals 17/10/14; normal 17.8 | **Yes, exact** | None |
| 12 | 2021: 61 hot nights and 54 very hot days, both records; 13 cold days; "highest… through the study window" | HKO Year's Weather 2021 [4] | Live page fetched: record items 36–37 (54 VHD, 61 HN highest annual on record); Table 2c totals 54/61/13 | **Yes, exact** | None; claim stays true even past the window (2024: 50) |
| 13 | 2023: 56 hot nights, 54 very hot days, 14 cold days | cited to [6] HKO Open Data | PI check 13 Aug matched ywx2023 Table 3 (56/54/14, EHD 4); numbers correct | **Numbers yes; pointer weak** | **Mismatch of attachment, not of fact:** [6] is a generic landing page; a referee cannot find "56" behind it. Add *The Year's Weather — 2023* to the reference list |
| 14 | July 2013 = 1 hot night; July 2022 = 25 (largest monthly count in window) | project tables + [6] | July 2013 = 1 verified on the 2013 yearbook monthly table this session; July 2022 = 25 from `hot_nights_by_month_year.csv` (ledger-verified), consistent with the HKO monthly record | **Yes** | July 2022 not re-fetched from a public page this session; low risk |
| 15 | EPD general stations: NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 µg m⁻³ | project CSV + [7] | CSV re-read: 53.72→32.08; 30.83→14.56; 42.61→58.31; GIA annex integers 54→32, 31→15, 43→58 | **Yes, exact** | [7] is a query portal — add access date or cite the GIA annex; 2023 GIA figures were "preliminary" (Feb 2024) — re-check finals before submission; keep "general stations" qualifier (present; roadside must never substitute) |
| 16 | Stroke history: 1999–2006 public hospitals; HS inverse with temperature; IS weaker below ~22 °C | Goggins 2012 [11] | ORA abstract: 1999–2006, 35+; HS strong negative linear; IS only below 22 °C | **Yes** | History-only; no percentages quoted in the live file — correct restraint |
| 17 | Influenza scientifically motivated in this setting | Yang Z 2025 [18] | Springer/Crossmark: real paper, Int J Biometeorol 69(5):963–973; HK stroke admissions 1998–2019; ILI+ association | **Yes, as covariate-class motivation** | It is a stroke-outcome paper motivating a covariate in a CHD/HF paper; fine as motivation, must never drift toward an outcome claim (ledger already fences this) |

**No quoted number failed verification.** All flagged risks are pointer, wording, or versioning risks.

---

## 3. Unused references 3 and 5

**Ref 3 — Year's Weather 2017.** No body sentence uses a 2017 exposure number. Uncited references fail journal production checks and read, in an hour-long referee scan, as carelessness. **Recommendation: drop at submission — and use the freed slot for *The Year's Weather — 2023*, which the body actually needs** (the 56/54/14 sentence currently hangs on the generic [6]). Keep 2017 in the working bibliography file in case Hogan attaches a sentence.

**Ref 5 — Year's Weather 2024.** 2024 is after the 132-month health window and must not become a health year. Two clean states exist: (a) Hogan adopts the one-sentence post-sample climate note in `optional_2024_climate_sentence.md`, in which case [5] becomes cited and stays; (b) he does not, in which case [5] is dropped at submission. **Recommendation: (b) unless Hogan actively wants the sentence.** Never attach 2024 to a model or a health claim.

Both were Hogan's original bibliography entries, so the drop is his call — hence decision D-C below rather than a silent edit.

---

## 4. External-data compatibility

**Contextual — may be used or kept without changing the estimand:**

- HKO yearbooks and annual extreme-day counts (validation and exposure natural history; the PI check already reconciles 2013/2019/2021/2023).
- The optional 2024 climate sentence (post-sample exposure only; explicitly not a health year).
- EPD 2013–2023 general-station means as description, plus staged archive sensitivities — provided they are never presented as an adjusted Table 2 (the live file already states this twice).
- C&SD population 35+ (Figure 1 context; offset sensitivity clearly labelled as not cohort person-time).
- ERA5-Land at the Observatory coordinate (limitation/corroboration of monthly means only; already one Limitations sentence).
- CHP Flu Express (archive covariate and unresolved-confounding statement; 121/132 months; never zero-filled).
- King's Park / Waglan official flags (exposure-definition sensitivity, Hogan-first; not in the live body).

**Estimand-changing if merged — each requires a protocol change and author approval before any model touches it:**

- **Still-at-risk cohort person-time** (D10): converts every count ratio into an incidence-rate ratio; changes the interpretation of all twelve contrasts and the Abstract.
- **Person-level or stratified HA fields** (medication, BMI, age–sex strata): changes the cohort definition and the adjustment set; opens conditional estimands the current aggregates cannot support.
- **Daily health outcomes, or any coefficient from daily-recovery methods:** moves from monthly association to daily triggering; currently refused by the failed 500-replicate calibration, and that refusal is part of the paper.
- **Pollution, influenza, or humidity entered into the core single-exposure models:** a temperature coefficient conditional on ozone answers a different question; the staged posture exists precisely to prevent this silent estimand shift.
- **ERA5 or other-station substitution for hot-night counts:** the 28 °C threshold does not travel (slope 0.045; 57 vs 9 hot-night months); swapping sources redefines the exposure contrast itself.
- **Extending the window to 2024:** changes the study period, the trend spline's support, and the seasonal-adjustment basis.
- **Any spatial overlay of health counts on exposure cells** (WorldPop, spatial fields): implies within-territory contrasts the territory-month aggregates cannot identify.

---

## 5. Collaborator decision list

Concise decision requests (owner; options; recommended default). Not an email; not sent.

1. **Running head** (Hogan). (a) Keep full estimand title until Gate 3 — **default**; (b) set a short head now. Cost of waiting: none.
2. **Medication in Limitations** (Hogan, comment 4 / D3). (a) Omit everywhere — current ledger default; (b) one factual Limitations clause: not in the aggregates; slow secular therapy change is absorbed by, and not separable from, the trend spline. **Round A recommends (b):** referees will raise it unprompted; Limitations is the correct home for named unmeasured factors; the Introduction stays clean either way.
3. **References 3 and 5** (Hogan). (a) Drop both at submission and add *The Year's Weather — 2023* to anchor the 2023 exposure counts — **recommended default**; (b) keep [5] only if adopting the optional 2024 climate sentence; (c) leave uncited — not journal-safe.
4. **Figure renumbering** (Hogan). Figures are cited in the order 1, 2, 4, 3. (a) Renumber the hot-night heatmap to Figure 3 and the residual ACF to Figure 4 — **recommended default**; (b) demote the ACF figure to a supplement (numbers already in text), which resolves the order automatically. His call because Figure 4 was offered as strikeable.
5. **Health-data paragraph** (Roro / D6). (a) Deliver ICD lists, executable timing rule, inpatient-vs-DAE semantics — required before submission; (b) confirm the bridge paragraph's inferences in writing. Default until then: bridge stays visibly provisional; the paper is not submittable.
6. **Stroke series** (Roro / D9). (a) Attach; (b) confirm it is not coming for this paper. Default: no stroke analysis, no invented rows.
7. **Still-at-risk person-time** (Roro–HA / D10). (a) Deliver monthly cohort person-time — upgrades the estimand; (b) confirm unavailable. Default: days-in-month offset; estimates remain count ratios and the paper says so.
8. **Gate 3 thesis freeze** (team / D4). Option A — no confirmatory primary, panel reported in full — **recommended default**; alternatives are in the Gate 3 packet. The one-sentence thesis is amended only after this freeze.
9. **Dissemination authority and IRB decision** (Bishai + Roro / D8). Written confirmation for the governed aggregates, and the IRB-amendment decision, before any submission. Default: do not submit.
10. **Author order and Authors 2–4** (Bishai + Hogan / D2). Placeholders until decided. Blocks submission by design.

---

## 6. Defects that would make a referee reject the paper in an hour

Ordered by how fast an hour-referee finds them:

1. **Figures cited out of numerical order** (Figure 4 appears in the text before Figure 3). Mechanical, and the first thing a production check or an irritated referee catches. Fix: decision 4.
2. **Uncited references [3] and [5]** sitting in the list. Reads as carelessness and invites the question "what else wasn't checked?" Fix: decision 3.
3. **Numeric claims on portal citations.** The 2023 exposure counts (56/54/14) cite a generic open-data landing page [6], and the EPD means cite a query portal [7] with no access date. A referee who tries to verify and cannot will not try twice. Fix: add the 2023 yearbook reference; add access dates or the GIA annex for [7].
4. **Outcome definition not executable.** Methods say ICD lists and the timing rule "remain with the outcome co-investigator" and inpatient semantics are "inferred from labels." Honest in a live draft; fatal in a submission. Fix: decision 5 — this is the single largest submission blocker.
5. **Author placeholders and the italic working-title note** if left in a submitted file. Desk-level.
6. **Ethics paragraph states the IRB-amendment decision is pending.** Cannot be pending at submission. Fix: decision 9.
7. **Positioning risk, not integrity risk:** an exploratory panel in which all twelve q-values exceed 0.19 and the leading CHD interval excludes 1 only under Newey–West. The manuscript's own framing (complete panel, four-construction ladder, refusals, identification account) is the defence — an hour-referee at a methods-friendly venue reads it as discipline; at an effect-hungry clinical venue it reads as "no finding." Journal choice and an intact Gate 3 freeze carry this; any post-hoc promotion of the NW-only exclusion to a headline would convert the defence into the indictment.
8. **One word in the Liu 2020 sentence:** the 4.72%/0.16% and 4.25%/0.63% figures are total-mortality attributable fractions inside a cause-specific study; "cold-dominant attributable fraction for cause-specific mortality" should read "for mortality." Thirty-second fix; the kind of imprecision a burden-literature referee notices immediately.

**Constraints honored:** no new health numbers were computed or introduced anywhere in this audit; no AMI or stroke endpoint is restored or recommended for restoration.
