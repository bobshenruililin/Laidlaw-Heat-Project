# Opus 5 verdict — PR 69 vs PR 70 (Hogan 24 August Methods pack)

**Role:** CNS-register scientific critic on the review committee. Remit: estimands, citations, and the prohibition on inventing coefficients.
**Reviewed against:** `Commented_Heat_CVD_Manuscript_20260824.pdf` (re-extracted here, not taken on trust from either PR's summary), the two live manuscripts, `COMMITTEE_REVIEW_PR69_vs_PR70.md`, `hogan_20260824_comment_inventory.md`, `knowledge/2026-08-24_hogan_pdf_comments.md`, `supplement_inventory.md`, and the primary sources for references [21] and [22].
**Date:** 24 August 2026.

---

## 1. Merge decision

**Ship PR 69 as the base. Graft six PR 70 items into it. Do not ship PR 70 as the base.**

This is not a close call on the base, and it is not a clean win for PR 69 either.

PR 70 fails three of Hogan's and Jingjing's explicit 24 August instructions in ways a supervisor will catch on one read:

1. it deletes `UW XX-XXX`, which is in the body text of the circulated PDF and is the anchor for KW11;
2. it puts work-in-progress and internal file labels in Health data and in Limitations;
3. its Abstract Methods states a simulation *result* ("failed simulation calibration") in the section Hogan told us to keep result-free.

PR 69 clears all three. But PR 69 has one genuine honesty defect that PR 70 does not — it describes unfitted models in the past tense — plus a mis-attributed comment ID and a mischaracterisation of PR 70 in its own committee brief. Those must be fixed before the pack goes to Hogan, and the fix is to import PR 70's wording.

Overall: PR 69 is right about *what the file may contain*; PR 70 is right about *how to describe a model that has not been fitted*.

---

## 2. Answers to the six questions I was asked

### 2.1 Is Model 2/3 specified without fake health coefficients?

**Both PRs: yes on coefficients. PR 69 only: no on grammar.**

Neither manuscript contains a Model 2 or Model 3 health estimate anywhere. Table 2 in both is the pre-existing thermal-only Model 1 panel, unchanged, and the twelve rows are numerically identical across the two PRs. Neither invents an IRB number. Both clear must-nots 1 and 2 of the committee brief.

The defect is tense, and it is in PR 69:

> PR 69 Abstract: "Model 2 **added** relative humidity and rainfall. Model 3 **used** counts of days warmer or cooler than the day-of-year historical average."
> PR 69 Methods: "Model 2 additionally **included** monthly mean relative humidity [21] and monthly total rainfall [22]…"

Past tense asserts that the fits happened. A reader who then finds no Model 2 estimate in Table 2 or the supplement concludes that we fitted it and did not report it — which is a worse accusation than not having fitted it.

The rule needs one distinction, because it is not "avoid the past tense". The climatology **weather series** was in fact built: `data_processed/…day_counts_2013_2023.csv` is 132 real HKO months. Past tense is correct for that construction, which is why PR 69's Methods sentence "Model 3 **counted**, for each month, the days whose daily mean temperature was above or below…" is honest, and is anchored by "Model 3 is specified and is not reported in Table 2." The past tense is only a lie about the **health fits**. So the two sentences that must change are PR 69's Abstract "Model 2 added" and "Model 3 used", and PR 69's Methods "Model 2 additionally included" — the last of which is the worst of the three, because Model 2 never receives the "is specified and is not reported" protection that Model 3 gets. Its unfitted status rests entirely on "Table 2 reports Model 1."

PR 70 gets this right in both sections: Abstract "Model 2 **adds** monthly total rainfall and monthly mean relative humidity… Model 3 **replaces** official extreme-day counts with…"; Methods "Model 2 **adds**… Model 3 **uses**… but **replaces**…". Present tense reads as specification. Import it.

PR 70 has a separate arithmetic error in the same paragraph: "Model 3 uses **the same twelve fits** as Model 1". Replacing three official extreme-day counts with two climatology counts gives five exposures × two outcomes = ten fits. Twelve is also the number the Benjamini–Hochberg correction is defined over, so reusing it for a different exposure set corrupts the multiplicity story. PR 69 is safer by declining to state a fit count for Model 3. Keep PR 69's silence.

### 2.2 Is Goggins 2017 correctly used (humidity vs rainfall)?

**Both PRs avoid the error Hogan's own email invited. PR 69 slightly overstates the humidity result. Neither states the estimand mismatch.**

Verified against the published abstract (`doi:10.1016/j.ijcard.2016.11.106`): the predictors were "daily mean temperature, humidity, and wind speed", and the reported humidity finding was that "**both high and low** relative humidity were **modestly** associated with more admissions." There is no rainfall variable in that paper.

Hogan's email attributed *both* rainfall and relative humidity to Goggins and Chan 2017. Citing [21] for rainfall would have been an error he could catch in his own suggestion. Both PRs avoid it: PR 69 cites [21] for humidity and [22] for rainfall; PR 70 cites [21] for humidity and gives rainfall no citation at all.

Two problems remain, one in each PR.

PR 69 writes "Humidity was associated with daily heart-failure admissions [21]." That flattens a **U-shaped** finding into a linear-sounding one, and it drops "modestly". It matters here specifically: Model 2 enters a *linear monthly mean* relative-humidity term, which cannot represent a both-tails relation. Left as written, the citation implies our specification tests what they found. It does not.

PR 70's rainfall term is uncited and therefore unmotivated, which is worse in front of a supervisor who asked for those two variables and named a source.

Neither PR states the sharper point: both cited papers fitted **daily** meteorological terms, and we are fitting a **monthly mean** and a **monthly total**. Rewrite R1 below fixes all of this in five plain sentences.

### 2.3 Is Chan 2013 BLT [22] an appropriate rainfall-attendance cite, or an overclaim?

**Appropriate. Better supported than PR 69 itself claims. Not an overclaim.**

The archived Bulletin text (`doi:10.2471/BLT.12.113035`) states it directly:

> "Same-day rainfall (square-root-transformed) was also included in all models **based on the hypothesis that heavy rain would deter people from going to hospital**."

PR 69's sentence — "Chan et al. entered daily rainfall on the hypothesis that heavy rain deters hospital attendance [22]" — is a near-verbatim paraphrase of the paper's own stated rationale. PR 69 also explicitly declines to claim that [22] found a CVD–rainfall effect. That is the correct discipline, and the citation is in fact a closer match than PR 69 argues: [22] is a Hong Kong Hospital Authority admissions time series (1998–2009, 7,869,661 admissions) with circulatory disease as an analysed cause. Same data family, same city, same outcome type.

Three precision fixes:

- Rainfall in [22] was a **control term**, not a predictor of interest. PR 69's "both previously used as meteorological predictors of hospital admissions" is loose. Say "entered in", not "predictors of".
- It was **same-day, square-root-transformed** rainfall. Our monthly total is a coarser and differently-shaped construct. State it.
- Do not correct Hogan's attribution in the body. Listing what [21] actually entered (temperature, humidity, wind speed) makes the omission of rainfall self-evident without a sentence that reads as a correction of the supervisor. Put the explicit note — "Goggins and Chan 2017 did not enter rainfall; the rainfall precedent is Chan et al. 2013" — in the Word comment, per the committee brief's own principle that precision goes in comments.

### 2.4 Model 3: daily-mean primary vs six collinear counts

**PR 69's labelling is correct. The committee brief's characterisation of PR 70 is a strawman and should be withdrawn.**

The brief rejects "Model 3 as warmer/cooler vs same-date mean, without splitting mean vs max/min" and argues "Six counts as one model is collinear." Neither manuscript proposes six counts in one model. PR 70's statistical section replaces the official counts with exactly two — days warmer and days cooler than the same-date mean of daily *mean* temperature — and its data file carries four columns, not six. The brief is arguing against a model neither PR wrote.

The real difference is narrower and still favours PR 69. PR 69 states the analytic role: "The same counts based on daily maximum and minimum temperature were examined in **sensitivity analyses**." PR 70 describes building the max/min versions and never says what they are for, which leaves a reader unable to tell whether they are primary. Keep PR 69's explicit split.

Two data-layer observations that cut the other way:

- PR 69's series is **symmetric and complete** (above/below for each of tmean, tmax, tmin — six columns). PR 70's is **asymmetric** (tmax-above and tmin-below only), which is a defensible warm-tail/cold-tail design but is unjustified in the text. PR 69's file is the better sensitivity substrate. Keep it.
- PR 70's file carries provenance columns PR 69's lacks: `n_clim_years_min`, `climatology_rule = leave_one_year_out_same_calendar_day_2012_2023`, `data_status = REAL_PUBLIC_HKO`. Under the repo's own provenance rule these are not optional. Graft them.

PR 69 also earns a point neither the brief nor PR 70 mentions: "Equal values were counted as neither." I checked, and this is material — 12 days across 10 of the 132 months tie the climatology exactly, so warmer + cooler does not sum to the days in the month. Without that sentence the definition is incomplete. Keep it, but do **not** print the tie count in Methods: a count of days is an observation, and KW16 already established that observations go to Results.

### 2.5 Ethics placement vs Hogan's "no WIP"

**PR 69 is right. PR 70 is wrong, and its test suite enforces the error.**

I extracted the circulated PDF rather than trusting either PR's summary, because the two flatly contradict each other. PR 69's inventory says Hogan typed `UW XX-XXX`; PR 70's knowledge note says "No `UW XX-XXX` in the body." The PDF settles it. At page-lines 78–81, inside the study-design paragraph and **immediately before the `Health data` heading**:

> "…We refer to the twelve separate single-exposure models as the core panel. In line with ethical requirements, the study was approved by the Institutional Review Board (IRB) of the HKU/Hospital Authority HK West Cluster (IRB reference number: **UW XX-XXX**)."

And the two balloons anchored there:

> KW10: "@Bob: You only need one sentence here to indicate that this study has ethics approval. All the other stuff is not required (**I deleted it already**)."
> KW11: "@Roro: Can you input the IRB reference number **here** for this study?"

The reading is unambiguous. The surrounding process text was already deleted by Jingjing; the one approval sentence with the placeholder is what she deliberately left; and "here" in KW11 refers to that placeholder at the start of Methods. `UW XX-XXX` is not our work-in-progress — it is a live query addressed to a named person. Deleting it orphans KW11, so Roro would be answering a comment attached to text that no longer exists.

PR 70 deletes the placeholder and moves the ethics sentence to the **end** of Methods, after the software paragraph. That is wrong twice over: it erases a collaborator's retained edit, and it lands the sentence in a structurally odd position that Hogan's requested order (data sources → equation → sensitivity) does not have a slot for.

Worse, PR 70's contract test hard-codes the error:

```python
assert "UW XX-XXX" not in methods
```

The test is green while the requirement is violated. PR 69 inverts the assertion with the reason in a comment, which is correct.

One qualification against PR 69's brief: KW10 and KW11 are **KW = Jingjing**, not Hogan. The brief's "He typed the placeholder … Deleting it erases his edit" mis-attributes the edit. The lock is right; the attribution should read "Jingjing retained this sentence and Roro owns the number."

### 2.6 Abstract Methods must not smuggle Results

**PR 69 is right. PR 70 violates it, and its test cannot see the violation.**

PR 70's Abstract Methods closes: "A method for recovering daily exposure coefficients from monthly sums **failed simulation calibration** and was not applied to the health series." "Failed simulation calibration" is the outcome of the calibration study — Supplementary Table S8 — stated in Methods. Hogan's instruction was no Results in Methods, and the committee brief's own must-not list names the calibration failure specifically.

PR 70's test defines `_methods()` as the slice between `## Methods` and `## Results`, so the Abstract is outside its scope entirely and the assertion set never looks for calibration language. Green, uncovered. PR 69 adds `test_abstract_methods_names_models_without_calibration_failure`, which is the assertion that was missing.

PR 69's architecture is correct: Methods says only what was done — "Separately, we tested a published method for estimating daily temperature effects from monthly outcomes using simulated Hong Kong weather [15,16]. We did not apply that method to the hospital counts." — and the failure appears in Results and Discussion.

I considered whether PR 69 should add a neutral Abstract clause ("evaluated by simulation but not applied to the health series") to preserve the honesty PR 70 was reaching for. **Recommend against.** It states a decision without room to give the reason, so it invites exactly the "why not?" that the Abstract cannot answer, and it adds a clause to the section Hogan just told us was too complex. Omission is the better call.

---

## 3. Ranked locks

Ranked by what a supervisor notices first and by what is hardest to undo once pasted.

| # | Lock | Source | Severity |
|---|---|---|---|
| **L1** | Ethics: one sentence, **verbatim**, including `(IRB reference number: UW XX-XXX)`, at the **start** of Methods before `Health data`. Do not reword a sentence a collaborator retained. Never substitute a real-looking number. | PR 69 | **Blocker.** PDF-verified; PR 70 fails. |
| **L2** | No Model 2 / Model 3 / Table 2 health coefficients. Table 2 caption names Model 1. | Both | **Blocker.** Both pass; keep the assertion. |
| **L3** | Abstract Methods contains no calibration verdict. Daily-recovery failure lives in Results and Discussion only. | PR 69 | **Blocker.** PR 70 fails. |
| **L4** | Describe unfitted models in the **present tense** — "Model 2 adds…", "Model 3 replaces…" — in both Abstract and Methods. | **PR 70** | **Blocker.** PR 69 fails; this is the one place PR 69 misleads. |
| **L5** | No WIP or internal file labels in the body: no "outcome co-investigator", no `chd_inpatient` / `hf_inpatient`, no "named in correspondence", no author-order italic, no "external dissemination requires confirmation". Stroke reads "A corresponding stroke series was not available for this analysis." | PR 69 | **Blocker.** PR 70 fails in Health data and Limitations. |
| **L6** | Hogan's HKO paragraph verbatim, including "All monthly data were derived by taking the average of daily data in each calendar month." Rainfall-is-a-total precision goes in a comment, never in the body. | Both | **Blocker.** Both pass. |
| **L7** | `[21]` for humidity only; `[22]` = Chan et al. 2013 *Bull World Health Organ* 91:576–584 for rainfall-as-attendance-hypothesis. No CVD–rainfall effect claim. Apply rewrite **R1**. | PR 69 base + primary-source corrections | High. |
| **L8** | Model 3 primary = daily **mean** warmer/cooler counts. Max/min counts labelled **sensitivities**. State no fit count for Model 3; drop PR 70's "same twelve fits". Keep "Equal values were counted as neither" and keep the tie count out of Methods. | PR 69 | High. |
| **L9** | No "core panel", "core count ratios", "twelve core contrast", or bare "the complete panel". PR 70 leaves three residues; PR 69 has none. | PR 69 | High — this is the exact phrase Hogan asked us to retire. |
| **L10** | Abstract must name Model 1's exposures precisely: three continuous temperature measures **and** the official counts of hot nights, very hot days, and cold days. "Each temperature measure" mislabels three day counts as temperatures. | **PR 70** | Medium. |
| **L11** | Every Results object has a Methods antecedent. PR 70's Methods never declares the joint max/min and joint extreme-day models that its Results section reports (VIF 4.66; joint hot-night 1.045). PR 69 declares them. | PR 69 | Medium. |
| **L12** | Keep the sentence explaining that extremely hot days (T<sub>max</sub> ≥ 35 °C) were obtained but not used as a Model 1 exposure. Hogan's weather list has four extreme-day counts; the model uses three. Answer it before he asks. | PR 69 | Medium. |
| **L13** | Discussion must say **why** the archive pollution models are not adjusted Model 1: they used a general-population offset and entered maximum and minimum temperature jointly. Verified against `supplement_inventory.md` S9. Apply rewrite **R5**. | **PR 70** | Medium. |
| **L14** | Keep software version numbers (R 4.3.3, MASS 7.3-60.0.1, sandwich 3.1.3). **Correct the stated reason:** KW18 "Good." anchors to **Table 1**, not Software. Keep them for reproducibility, not because Hogan blessed them. | PR 69 lock, corrected reason | Medium. |
| **L15** | Climatology series: keep PR 69's six symmetric columns; graft PR 70's provenance columns (`climatology_rule`, `n_clim_years_min`, `data_status = REAL_PUBLIC_HKO`). Rename to `hogan_climatology_day_counts_2013_2023.csv` — "abnormal" implies a health judgement these weather counts do not carry. | **PR 70** naming and provenance, PR 69 columns | Medium. |
| **L16** | Script numbers: use PR 70's **61/62/63**. `scripts/52_public_outcome_ceiling_search.py` and `scripts/53_mde_from_uncertainty_ladder.py` already exist on `main`, so PR 69's `52_hogan_abnormal_day_counts` / `53_hogan_models_rh_rain` collide. | **PR 70** | Medium. |
| **L17** | Ship the **full manuscript** Word + PDF, not a Methods-only paste. Bob asked for a file Hogan can read tonight, and Model 1/2/3 numbering changes the Abstract, the Results heading, and the Table 2 caption — a Methods-only paste leaves the file internally inconsistent. | PR 69 | Medium. |
| **L18** | Adopt PR 69's contract suite (11 tests), with the additions in §5. PR 70's 6-test suite is green while three Hogan asks are violated. | PR 69 | Medium. |
| **L19** | Data availability must not assert an unverified instrument. Apply rewrite **R4**. | Corrected | Low. |
| **L20** | Withdraw two claims from `COMMITTEE_REVIEW_PR69_vs_PR70.md`: the "six counts as one model" characterisation of PR 70 (§2.4), and "He typed the placeholder" (KW10/KW11 are Jingjing). Fix the KW18 row in `hogan_20260824_comment_inventory.md`. Roro may read these. | Corrected | Low, but it is a provenance record. |

---

## 4. Citation and prose rewrites

### R1 — Model 2 paragraph (replaces PR 69's four sentences)

> Model 2 adds monthly mean relative humidity and monthly total rainfall to Model 1. Goggins and Chan entered daily mean temperature, humidity, and wind speed as predictors of daily heart-failure admissions and deaths in Hong Kong, and reported that both high and low relative humidity were modestly associated with more admissions [21]. Chan et al. included same-day rainfall in Hong Kong hospital-admission models on the hypothesis that heavy rain deters people from going to hospital [22]. Both papers fitted daily values, so a monthly mean and a monthly total are coarser than the terms they used. Table 2 reports Model 1.

Every clause is checkable against the two abstracts. Present tense in sentence 1 (L4). `[21]` carries humidity only, with the both-tails shape intact. `[22]` carries the hypothesis, not a finding. Sentence 4 is the estimand caveat neither PR had. Listing what [21] entered makes the absence of rainfall self-evident without a sentence that corrects Hogan.

**Accompanying Word comment, not body text:**

> Rainfall precedent: Goggins and Chan 2017 [21] entered temperature, humidity, and wind speed, not rainfall. The rainfall-as-attendance-deterrent hypothesis is Chan, Goggins, Yue and Lee 2013, *Bull World Health Organ* 91:576–584, doi:10.2471/BLT.12.113035, where same-day square-root-transformed rainfall was a control term. Our Model 2 rainfall term is a monthly total, so it cannot represent same-day attendance deterrence; our relative-humidity term is a linear monthly mean, so it does not test the non-linear pattern [21] reported. Model 2 estimates are produced by the governed refit script; do not enter them by hand.

### R2 — Abstract Methods, models sentence

Replace PR 69's:

> Each temperature measure entered a separate negative-binomial model (Model 1), with calendar-month indicators, a 4-df time spline, and an offset for the number of days in the month. Model 2 added relative humidity and rainfall. Model 3 used counts of days warmer or cooler than the day-of-year historical average. Reported estimates are from Model 1.

with:

> Model 1 is a separate negative-binomial model for each of three continuous temperature measures and the official counts of hot nights, very hot days, and cold days, with calendar-month indicators, a 4-df time spline, and an offset for the number of days in the month. Model 2 adds monthly mean relative humidity and monthly total rainfall. Model 3 replaces the official extreme-day counts with counts of days warmer or cooler than the same-calendar-day historical mean. Reported estimates are from Model 1.

Fixes L4 and L10 together. No calibration language (L3).

### R3 — Model 3 paragraph

> Model 3 counts, for each month, the days whose daily mean temperature was above or below the historical average for that day of the year. For 15 July 2018, for example, that average is the mean of every other 15 July in the Hong Kong Observatory daily series for 2012–2023, leaving 2018 out. Days equal to that average were counted as neither. The same counts built from daily maximum and daily minimum temperature are sensitivity analyses. Table 2 reports Model 1.

Present tense (L4). PR 70's worked example, which is the high-school-readable form Hogan asked for. PR 69's tie rule and sensitivity labelling (L8). No fit count.

### R4 — Data and code availability

Replace PR 69's "Access to Hospital Authority data is governed by the data-sharing agreement and ethics approval." — which asserts a specific instrument I could not verify in this checkout — and PR 70's version, which names an unnamed collaborator and reads as work-in-progress:

> The code used to generate the findings is at https://github.com/bobshenruililin/Laidlaw-Heat-Project. The monthly Hospital Authority counts are not publicly posted; what may be shared is determined by Hospital Authority approval and by the study's ethics approval.

Matches KW20 without a "we still need to check" sentence in the body.

### R5 — Discussion, pollution sentence (import PR 70's precision)

> Supplementary models that entered nitrogen dioxide, fine particulate matter, or ozone used a general-population offset and entered maximum and minimum temperature jointly, so they are not adjusted versions of Model 1 (Supplementary Table S9). On a monthly grain they cannot separate confounding from mediation for ozone, and no such model was used to revise Table 2.

Verified against `supplement_inventory.md`, which records S9 as "Archive pollution-staged models (P11; joint Tmax/Tmin; population×days offset) … **not** core-adjusted". PR 69 compresses this to "are sensitivities, not replacements for Model 1", which states the conclusion without the reason. Drop "Archive" and "core" in favour of "Supplementary" (L9).

### R6 — Inpatient semantics: comment, not body

PR 70 puts "Inpatient-only semantics are inferred from the delivered column labels and are not yet confirmed" in Limitations. That is a real uncertainty about our own outcome definition, and PR 69 loses it by dropping the sentence entirely. But stating an unresolved internal question in Limitations is work-in-progress (L5), and the fix is not to restore the file labels. Move it to a comment:

> @Roro: please confirm whether the delivered CHD and HF monthly counts are inpatient admissions only. The Methods currently say "first recorded hospitalisation" without asserting an inpatient restriction. If they are inpatient-only, we add one clause; if not, the outcome wording stays as is.

Keep PR 69's Limitations sentence "Confounding by pollution, humidity, rainfall, and influenza is unresolved in Model 1." It already carries the consequence of Model 2 being unfitted, and PR 70 drops rainfall from that list.

### R7 — Health data provenance sentence

The circulated PDF contains "Governed monthly aggregates were constructed and released by the outcome co-investigator", and **no balloon was placed on it**. PR 69 deletes it; PR 70 expands it. Deletion is the right call — unnamed collaborator roles belong in author contributions, and Hogan's email asked for no work-in-progress in the body — but because it survived the review pass untouched, the removal is our editorial judgement rather than an instruction we were given. Surface it:

> Removed "constructed and released by the outcome co-investigator" and the delivered file labels from Health data, per the no-work-in-progress instruction. Contributor roles can go in author contributions once authorship is settled. Restore if you would rather keep the attribution in Methods.

---

## 5. Test assertions to add to PR 69's suite

PR 69's suite is the right base — it already covers the Abstract, the `[21]`/`[22]` split, the ethics placeholder, the WIP strings, the Results heading, the Table 2 caption, and the docx comments. Five gaps remain, four of them created by the rewrites above.

```python
def test_unfitted_models_are_present_tense():
    """L4. Past tense asserts fits that have not happened."""
    methods, am = _methods(), _abstract_methods()
    for blob in (methods, am):
        assert "Model 2 adds" in blob or "Model 2 additionally adds" in blob
        assert "Model 2 added" not in blob
        assert "Model 2 additionally included" not in blob
        assert "Model 3 used" not in blob
    assert "the same twelve fits" not in methods  # Model 3 is not twelve fits

def test_rainfall_citation_claims_hypothesis_not_effect():
    """L7. [22] supplies a rationale, never a rainfall effect."""
    methods = _methods()
    assert "deters people from going to hospital [22]" in methods
    for bad in ("rainfall was associated", "effect of rainfall",
                "rainfall predicted", "Goggins and Chan entered rainfall"):
        assert bad.lower() not in methods.lower()
    # Humidity must keep its both-tails shape.
    assert "both high and low relative humidity" in methods

def test_abstract_names_model1_exposures_precisely():
    """L10. Hot nights and cold days are day counts, not temperature measures."""
    am = _abstract_methods()
    assert "hot nights" in am and "cold days" in am
    assert "Each temperature measure entered" not in am

def test_methods_declare_every_reported_model():
    """L11. No Results object without a Methods antecedent."""
    methods = _methods()
    assert "in one model" in methods or "jointly" in methods   # joint VIF models
    assert "quasi-Poisson" in methods
    assert "Ljung" in methods or "autocorrelation" in methods

def test_climatology_series_carries_provenance():
    """L15. Provenance columns are not optional."""
    rows = list(csv.DictReader(CLIM.open(encoding="utf-8")))
    assert rows[0]["climatology_rule"] == "leave_one_year_out_same_calendar_day_2012_2023"
    assert rows[0]["data_status"] == "REAL_PUBLIC_HKO"
    assert int(rows[0]["n_clim_years_min"]) >= 10
```

Two edits to PR 69's existing tests:

- `test_numbered_models_and_equation_symbols` splits the equation block on the literal `"Model 2 additionally"`. Rewrite R1 changes that phrase to `"Model 2 adds"`, so the split anchor must change or the RH/rainfall check silently stops guarding the Model 1 equation. Anchor on `"Model 2 "` instead.
- `test_climatology_series_is_weather_only` points at `hogan_abnormal_day_counts_2013_2023.csv`. Repoint to `hogan_climatology_day_counts_2013_2023.csv` (L15).

---

## 6. What I did not verify, and what no committee can close

Verified from primary sources: the `[21]` predictor set and humidity finding; the `[22]` rainfall variable and the deterrence hypothesis, quoted from the archived Bulletin text; the `UW XX-XXX` placeholder and the KW10/KW11 anchors, by re-extracting the circulated PDF; the KW18 anchor (Table 1, not Software); the S1/S8/S9 supplementary mappings in `supplement_inventory.md`; the 12 tie days and the 132-month length of both climatology files; the script-number collision against `main`; and that PR 70's test suite passes while violating L1, L3 and L5.

Not verified, and not verifiable from this checkout: any Model 2 or Model 3 health coefficient. The governed CHD/HF panels are absent. **Neither PR invents them, and no committee decision in this memo licenses typing one.** Model 2 and Model 3 estimates come from the refit script on the machine that holds the panel, or they do not exist.

Human-owned, unchanged by this verdict: Roro replaces `UW XX-XXX` and confirms inpatient semantics and ICD/timing; Hogan and Bishai settle author order; Bob pastes the Word file into the shared live document rather than emailing a competing copy.

Gate 3 remains open. No AMI, principal-diagnosis, or stroke result.

---

## 7. One-line verdict

PR 69 ships, on PR 70's grammar: **PR 69's locks + PR 70's present tense (L4), Abstract exposure precision (L10), S9 pollution provenance (L13), climatology naming and provenance columns (L15), script numbers 61/62/63 (L16)** — with rewrites R1–R7 applied and the five test assertions in §5 added before the Word and PDF are rebuilt.
