# Hostile-referee read of the merged live manuscript — Fable (senior scientist / methods editor)

**Date:** 15 August 2026. **Mode:** Ship.
**Target:** `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` at commit `7d36f9f` (the 15 August merged paper, not the 13 August version).
**Checked against:** `claim_ledger.md`, `00_parent_synthesis.md`, my own `01_fable_architecture.md`, and `.cursor/skills/cns-writing/SKILL.md`.
**Rails observed:** no new numbers (every scientific numeral below is a ledger row or a recount of an existing CSV; word counts are file statistics); no Gate 3 freeze; Hogan's weather paragraph untouched; Stage 3 PDFs untouched; no health-econ. This file does not edit the live manuscript.
**Independent recounts performed:** from `outputs/live_identification/cold_days_by_month_year.csv` (`REAL`) I recounted 29 of 132 months with at least one official cold day; 145 total cold days with 141 in December–February (December 40, January 54, February 47) and 4 in March; annual hot nights 10 (2013), 61 (2021), 56 (2023); very hot days 17 (2013), 54 (2021), 54 (2023); cold days 14 (2013), 1 (2019), 13 (2021), 14 (2023). Every recount matches the merged text.

---

## 1. Verdict

Yes — this is now the strongest honest paper these data support, and the merge executed the architecture essentially in full: the pre-2020 CHD hot-night null is in the Abstract, Results, Discussion, and Limitations; the flu numeral is out of the body; Figure 3 does identification work and the ACF is demoted; the 2021 record claim is cited and bounded; the Ljung–Box threshold is corrected to a value that is actually true; the ladder-direction caution survived verbatim; and the twelve-contrast panel, the estimand boundary, and the M|D refusal all hold under hostile reading. What still fails a Nature referee is the evidence class itself, which no edit can change and which the paper honestly declares — that venue is closed and should stay closed. What a *good* EHP or Environmental Research referee will still hit is narrower: (i) the paper describes staged pollutant models but displays none of them, so "confounding is unresolved" reads as an assertion rather than a shown boundary, and a major-revision request for those existing archive estimates is near-certain; (ii) two deliberate governance placeholders (the outcome-paragraph instruction sentence and the Ethics section's process language) are correct for a live collaborative draft but are submission-blocking text; and (iii) a handful of register faults — internal provenance tags in figure captions, verbatim duplication of the cold-day accounting between Methods and Results, and one ambiguous rounding sentence. **No remaining item is desk-reject class. There is one referee-facing major (KL1) and one human-owned major (KL2); everything else is minor or nit.**

---

## 2. Kill list

### Architecture items — merge audit first

| Item (from `01_fable_architecture.md`) | Status in merged file |
|---|---|
| K1 flu numeral out of Discussion | **Already executed.** Direction-only sentence; 1.673 appears nowhere in the body. Pointer wording differs from my paste — see KL5. |
| K2 uncited [3]/[5] | **Open, human-owned.** Correctly flagged to the weather co-investigator, not deleted. Still uncited in the merged body ([2], [4], [6] carry the exposure claims). |
| K3 2021 record superlative | **Already executed.** Now "the highest annual number of hot nights in the Observatory record at that time [4]" — cited, bounded. |
| K4 pre-2020 null in Abstract | **Already executed.** "(1.011, 0.991–1.032)" in Abstract Results; window dependence in Abstract Conclusions. |
| K5 figure re-architecture | **Already executed.** Figure 3 = trend/depletion sensitivity; residual ACF referenced as Supplementary Figure S1; both PNG paths resolve in `figures/live_identification/`. |
| K6 post-2020 entanglement | **Already executed.** Discussion: "confined to specifications that include 2020–2023, which are the years in which hot nights peaked and in which care-seeking changed." |
| K7 Abstract ≤ 300 | **Executed for the ≤ 300 target** (273 words excluding structural labels; was 388). Over IJE's 250 — see §4. |
| Multiplicity-refusal consolidation (§5 item 5) | **Executed acceptably.** Five tellings remain, but the Table 3 telling ("concordance … does not create multiplicity protection") and the Conclusion telling ("neither association survived correction") each carry content the others do not. No further cut required. |
| Ljung–Box fidelity | **Already executed** (Opus catch, parent adopted): *p* < 10^−7^, true for all six CHD core models (max 1.17 × 10^−8^). |

### Remaining kills

**KL1. No pollutant-adjusted display anywhere in the paper's display set.** Severity: **major** (major-revision demand, not desk-reject). Location: Methods "Weather and pollutants data" processing paragraph ("Staged pollution models exist in the archive"); Discussion paragraph beginning "Pollution and influenza are scientifically motivated." Why: the Introduction motivates NO₂, PM2.5, and ozone with real trend numbers; the Methods declare staged models exist and a staging order; the Discussion declares confounding unresolved — and then the paper shows none of it. A referee at Environmental Research or EHP will ask for the staged pollutant sensitivities in the supplement, and the honest answer ("they exist, labelled, in the archive") makes withholding them look worse, not better. These are existing archive estimates, not new model runs, so surfacing them respects the no-new-numbers rail; the numerals must be transcribed from the archive tables into the supplement with ledger rows added — a team paste, not mine to invent here. **Remedy (two parts).** (a) Supplement map: add a Table S9 for the staged pollutant models to `03_sol_supplement_map.md`, labelled *not core-adjusted*, same boundary language as Table S7. (b) **PASTE-READY** (Discussion, replace "Archive models in which they enter are not adjusted versions of the core panel."):
> "Staged models that added nitrogen dioxide, fine particulate matter, and then ozone to single thermal exposures are reported in the supplement as labelled sensitivities; on a monthly grain they cannot separate confounding from mediation for ozone, and no staged estimate was used to revise Table 2."
Do not paste (b) before (a) exists, or the sentence points at nothing.

**KL2. Deliberate draft markers in the scientific body.** Severity: **major for submission; intentional and correct today; human-owned.** Locations: Methods "Health data" final sentence ("Field-level ICD lists and the executable timing rule remain with the outcome co-investigator and should replace this paragraph where they differ from it") and the Ethics section's two process sentences ("Written confirmation … remains required before journal submission"; "Whether the institutional review protocol requires amendment … remains a decision for the supervising investigator"). Why: these are editorial instructions and governance logistics inside the scientific body — exactly what the CNS skill forbids at submission. They are also exactly what this live collaborative draft *should* contain until the outcome co-investigator delivers the governed construction and the supervising investigator records the IRB decision. **No paste-ready fix exists** — writing replacement text would invent collaborator facts, which is the one thing worse than the marker. Resolution: the "Roro health-data paragraph" and "PI IRB decision" rows of the human-blocker table. Track; do not edit.

**KL3. Internal provenance vocabulary in figure captions.** Severity: **minor.** Locations: Figure 1 caption ("Provenance: HA_APPROVED_AGGREGATE annual totals; REAL Census…"), Figure 2 caption ("Provenance: REAL HKO official flags…"), Figure 3 caption ("Provenance: HA_APPROVED_AGGREGATE estimates…"). Why: `HA_APPROVED_AGGREGATE` and `REAL` are repository provenance tags, not journal language; a referee reads them as leaked internal tooling, and the CNS skill bars internal process vocabulary from the scientific body. The provenance discipline must survive — translate the tag, keep the trace. **PASTE-READY (three caption tails, replacing each "Provenance:" clause):**
> Figure 1: "Source: governed Hospital Authority aggregate annual totals; Census and Statistics Department mid-year population aged 35 years or older."
> Figure 2: "Source: Hong Kong Observatory official daily cold-day flags (T~min~ ≤ 12 °C), aggregated to calendar months."
> Figure 3: "Source: sensitivity estimates computed from the governed aggregate series (trend and depletion sensitivity table)."

**KL4. Verbatim duplication of the cold-day accounting between Methods and Results.** Severity: **minor.** Location: Methods weather-processing paragraph ("Official cold days were concentrated in December–February: 141 of 145 days across 2013–2023, with four days in March. Twenty-nine of 132 months carried at least one official cold day.") versus Results exposure context, which carries the identical numerals plus the month breakdown and Figure 2. Why: exposure descriptives are Results facts; Methods needs only the design consequence. Duplicating the full accounting violates the one-telling-plus-echo rule and pads Methods, which is already over its soft budget (1,319 words against my ≤ 1,200). **PASTE-READY (Methods, replace the two quoted sentences):**
> "Official cold days were concentrated in December–February (Results, Figure 2), so with calendar-month indicators in the model the remaining cold-day variation is a difference between years within winter months."
Keep the winter-only-restriction sentence that follows. Results, Discussion, and Limitations tellings stay as merged.

**KL5. Supplement items have no in-body anchors.** Severity: **minor** (deferred until the supplement is assembled). Location: Discussion flu sentence ("that estimate is reported in the accompanying release") and the absence of any body citation for Sol's Tables S1–S8 and Figures S2–S3; only Supplementary Figure S1 is cited. Why: most target journals require every supplementary item to be cited from the main text; "the accompanying release" is not a citable object in a journal PDF. **PASTE-READY (Discussion, flu sentence, once the supplement exists):**
> "On the 121 months with influenza data, an archive model associated higher influenza activity with higher CHD counts (Supplementary Table S7); that model is not an adjusted version of the core panel and does not adjust Table 2."
The remaining anchors (S1–S6, S8, and S9 if KL1(a) is taken) are a mechanical pass at supplement-assembly time, not now.

**KL6. Ambiguous rounding sentence after Table 2.** Severity: **nit.** Location: Results, "The HF mean-minimum-temperature interval included 1 at the fourth decimal place, with an unrounded upper bound of 1.00005." Why: "included 1 at the fourth decimal place" can be read as *excluded except at* the fourth decimal; the interval simply includes 1, narrowly. **PASTE-READY:**
> "The HF mean-minimum-temperature interval narrowly included 1, with an unrounded upper bound of 1.00005."

**KL7. Abstract undersells the M|D result.** Severity: **nit.** Location: Abstract Methods, "…was tested in simulation and was not applied to the health series." Why: read alone, this sounds like a scoping choice rather than a calibration failure; the Results say it failed. One word fixes it. **PASTE-READY:**
> "A method for recovering daily exposure coefficients from monthly sums failed simulation calibration and was not applied to the health series."
(The §4 shorter Abstract already incorporates this.)

**KL8. "Refusal" appears five times.** Severity: **nit; voice call, not an error.** Locations: Introduction close, Results (M|D paragraph), Discussion (M|D paragraph), Discussion (contribution paragraph: "the refusals"), Strengths. Why: it is the paper's identity word and each use is accurate, but five occurrences of a non-standard term invites a referee's marginalia. If trimmed, keep the Introduction and Discussion M|D uses and let Results and Strengths say the plain form ("no daily health coefficient is reported" / "reported without a coefficient"). Optional; I would not fight for it.

**KL9. Newey–West on a negative-binomial ML fit is unglossed.** Severity: **nit** (a statistics referee at IJE would raise it; ER/EHP likely will not). Location: Statistical analysis, the Newey–West sentence. Why: HAC covariances are defined for estimating equations; applying them to `glm.nb` output is defensible but one clause pre-empts the query. **PASTE-READY (append to "Core intervals used Newey–West standard errors with lag 6 [19]…"):**
> "…treating the fitted negative-binomial score equations as estimating equations."

No other kills. The estimand boundary, the between-winters identification, the depletion display and its refusal to quantify, the joint-model diagnostics framing, the Goggins/Guo questions-not-magnitudes comparisons, the M|D boundary sentence, and the "what a protected claim would have required" paragraph all survive hostile reading as merged. **Zero desk-reject items. One referee-facing major (KL1); one human-owned major (KL2). If KL1 and KL2 are closed, no majors remain.**

---

## 3. Remaining CNS-checklist failures

Against `.cursor/skills/cns-writing/SKILL.md`:

1. **"No draft markers, process gossip, internal gate language, or administrative logistics remain in the scientific body" — FAILS today**, on exactly the KL2 sentences (Health data instruction; Ethics process language) and the KL3 caption tags. KL2 is intentional and human-owned; KL3 has a paste above. Everything else on this rule passes: zero hits for "Gate 3", "continuity", "pipeline", "TBD", "placeholder", "novel", "remarkably", "it is important to note"; "significant" appears once, correctly, inside the Goggins et al. citation; "caused" appears once, inside the Limitations' *denial* of a cardiac-caused-admission reading.
2. **"Each sentence carries one claim; redundant clauses cut" — marginal fail** on the KL4 Methods/Results duplication. One paste fixes it.
3. All other checklist items **pass** on the merged file: the opening states problem and estimand without throat-clearing; every quantitative statement traces to the ledger (I re-verified the recountable ones independently); citations are attached and [3]/[5] are flagged rather than orphan-deleted silently; collaborators are credited by role; nulls and discordant sensitivities are displayed with equal prominence to the leading estimates; mortality, excess-death, and morbidity quantities are kept distinct; limitations match the design; no claim exceeds provenance; the register matches the Hogan standard.

---

## 4. Abstract length

Measured on the merged file: **273 words** excluding the four structural labels (277 including them; 293 including the Keywords line). That is **within Environmental Research's ~300** and **23 words over IJE's 250**. Since IJE holds rank 3, here is a 248-word version (labels excluded from the count) that keeps the pre-2020 null, the DJF identification, the *q* > 0.19 statement, and the M|D refusal, and loses only the ladder narrative detail and the HF pre-2020 strengthening (both remain in Results):

**PASTE-READY (IJE-format Abstract, 248 words):**

> **Background.** Hong Kong records more hot nights than a decade ago, while cold days persist. Whether the cold-dominant pattern of earlier daily cardiac-admission studies extends to monthly first-hospitalisation counts is untested.
>
> **Methods.** We analysed 132 territory-months (2013–2023) of first hospitalisations after first diagnosis of coronary heart disease (CHD; 156,156 events) or heart failure (HF; 29,681 events) among people with type 2 diabetes and/or hypertension; admission cause was not recorded. Three continuous temperature measures and official counts of hot nights, very hot days, and cold days each entered a separate negative-binomial model with calendar-month indicators, a 4-df time spline, and a days-in-month offset. Intervals used model-based, HC1, and Newey–West lag-3 and lag-6 constructions, with Benjamini–Hochberg q-values across the twelve exploratory contrasts. A method for recovering daily exposure coefficients from monthly sums failed simulation calibration and was not applied to the health series.
>
> **Results.** Under Newey–West lag-6 reporting, the count ratio was 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF; all twelve q-values exceeded 0.19. For CHD hot nights, model-based and HC1 intervals included 1, as did the pre-2020 estimate (1.011, 0.991–1.032). For HF cold days, all four constructions excluded 1. Official cold days fell almost entirely in December–February (141 of 145), identifying that contrast between winters.
>
> **Conclusions.** The data do not support a multiplicity-protected differential thermal claim. The HF cold-day association is concordant across standard-error methods; the CHD hot-night association depends on the construction and on including 2020–2023. Estimates are ecological monthly count ratios.

Every numeral is a ledger row. Do not swap this in for an Environmental Research submission — the current 273-word Abstract is richer and fits; hold this version for IJE only.

---

## 5. What the parent got wrong

1. **The 29-month count placement — half right.** Verifying the count before admitting it was exactly right (my architecture held it EXPLORE-ONLY pending verification; the parent recomputed 29 from the `REAL` CSV, and my independent recount agrees). But placing the full accounting in Methods *and* Results *and* Discussion *and* Limitations produced a verbatim numeral duplication between Methods and Results (KL4). The counts belong once, in Results with Figure 2; Methods needs only the identification consequence; the Discussion and Limitations echoes are earned because they decide interpretation. One paste fixes it.
2. **Venue ranking — not wrong.** Moving Environmental Research to rank 1 is a justified operational deviation from my tier-(c) ordering (I had named LPH/EHP/IJE as the class with EHP or IJE the expected outcome). Sol's reasoning — space for diagnostics, tolerance for a single-city panel whose contribution is inferential transparency — is sound, the demotion of LPH to rank 4 on editorial rather than thematic fit is correct, and no document claims or implies CNS suitability. I endorse the ranking as merged.
3. **The parent synthesis under-records the Abstract length.** "Opus 250-word structure + Fable's M|D refusal sentence" describes the input, but the merged Abstract is 273 words — fine for Environmental Research, over the IJE cap the parent's own rank-3 entry cites. Not a science error; §4 closes it.
4. **The flu pointer drifted from the K1 paste.** My K1 sentence pointed at Supplementary Table S7; the merged sentence points at "the accompanying release," which is not a citable journal object. Correct for today (the supplement does not exist yet), but the S7 pointer must be restored at supplement assembly (KL5).
5. **Everything else audited clean.** The Ljung–Box 10^−7^ correction, the "at that time" bounding of the 2021 record with [4], the [3]/[5] flag-don't-delete call, the byte-identical weather paragraph, the health-econ exclusion, and the Stage 3 locks were all executed as decided.

---

## 6. Explicit refusals

**Do not promote a primary.** All twelve core *q*-values exceed 0.19 (minimum 0.192); the model set was specified after the outcome series were available; concordance of the HF cold-day interval across four standard-error constructions is not multiplicity protection, and the paper says so in its own words. Any edit that elevates HF cold days (or CHD hot nights, or the joint-model 1.045) to a finding contradicts the paper's spine and should be reverted on sight. Gate 3 remains open and is team-owned.

**Do not claim CNS venue.** CNS *register* is the prose standard, applied; CNS *venue* is not honest on these data and no repo note, cover letter, slide, or reply to this file should say or imply otherwise. The honest submission path remains Environmental Research first, EHP as one deliberate reach, IJE only with the structural cut (§4 supplies its Abstract), and nothing above that.

---

*Residue: this file. Next executable steps in-repo: KL3 and KL4 pastes into the live file by whoever holds the pen next; KL1(a) into `03_sol_supplement_map.md` before KL1(b); KL2 and K2 stay with the humans named in the blocker table.*
