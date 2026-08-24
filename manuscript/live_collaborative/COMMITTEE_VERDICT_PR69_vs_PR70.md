# Committee verdict — PR 69 vs PR 70 (Hogan 24 August pack)

**Date:** 24 August 2026.  
**Committee:** Fable 5, Opus 5, Grok 4.6, Sol 5.6.  
**Question:** which live-manuscript pack should Bob paste into Hogan’s shared file?  
**Answer:** neither pack as-is. **PR 69 is the base. Six PR 70 locks are grafted in.** The Hogan-facing files on this branch are that merge.

Do not email a competing copy. Paste `Heat_CVD_Manuscript_20260824_hogan.docx` into Hogan’s live file.

---

## Votes

| Member | Base | Mandatory grafts from the other pack | Dissent (rejected) |
|---|---|---|---|
| **Fable 5** | PR 69 | Present-tense Model 2/3; no invented “data-sharing agreement”; keep `UW XX-XXX` at the start of Methods | — |
| **Opus 5** | PR 69 | Same present-tense graft; humidity wording must be both tails and modest; both cites are daily vs our monthly mean/total; Abstract Methods must not mention calibration failure | — |
| **Grok 4.6** | PR 69 | Number the Model 1 equation as (1); keep ethics placeholder in the body | — |
| **Sol 5.6** | Fail both until equation numbered **and** `UW XX-XXX` moved to a Word comment | Equation (1) adopted | Moving ethics out of the body — **rejected 3–1**. It orphans KW11. |

**Locked recipe:** PR 69 body + PDF pipeline; present-tense Model 2/3; equation (1); [21] both-tails modest humidity; [22] Chan 2013 attendance hypothesis + daily-vs-monthly grain; Table 2 = Model 1; Model 3 daily-mean primary with 15 July 2018 example; `UW XX-XXX` stays; Hogan weather verbatim; no invented HA coefficients.

---

## What this merge keeps from PR 69

- Full Hogan-facing Word + PDF, not a Methods-only paste.
- Ethics: one sentence at the **start** of Methods with Hogan/Jingjing’s `UW XX-XXX` (Roro fills the number).
- Hogan HKO paragraph **verbatim**, including the averaging sentence. Rainfall-is-total lives in a **Word comment** only.
- No WIP (`outcome co-investigator`, `chd_inpatient`, “named in correspondence”).
- Abstract Methods names Model 1/2/3 and does **not** mention daily-recovery calibration failure.
- Software version numbers kept. Acknowledgements `None.`
- Model 3 = days above/below leave-one-year-out same-calendar-day **mean**. Max/min counts are sensitivities.
- [22] Chan, Goggins et al. 2013, *Bull World Health Organ* (doi:10.2471/BLT.12.113035) for rainfall as a hypothesized attendance deterrent, not as a CVD–rainfall finding.

## What this merge keeps from PR 70

- Nested **Model 1 / 2 / 3** (not “Models 1–12”).
- Table 2 = Model 1. No invented Model 2/3 health coefficients.
- KW15 = rescaling \(R^{3/5}\) / \(R^{1/5}\), not new fits.
- Goggins 2017 [21] for **humidity only**.
- Contract tests.
- Equation with every symbol named, now numbered **(1)**.
- Present tense for unfitted Model 2/3.
- Data availability: GitHub URL; counts not posted; sharing depends on ethics approval. No invented data-sharing agreement.

## Shared must-nots (both PRs; still binding)

1. Invented Model 2/3 health coefficients.
2. Invented IRB number.
3. Overwrite of Hogan’s HKO paragraph, including the averaging sentence.
4. “core panel” / “twelve core contrasts”.
5. Results in Methods (141 of 145 cold days; VIF; calibration failure).
6. Jingjing TV-day counts.
7. Using this Methods paste as the Laidlaw Stage 3 programme essay. Stage 3 is a separate 24 August programme rebuild.
8. Citing Goggins and Chan 2017 [21] as the rainfall paper.

---

## Human items this merge cannot close

- Roro: replace `UW XX-XXX`; confirm ICD/timing if they differ.
- Governed-panel machine: fit Model 2 with `scripts/53_hogan_models_rh_rain.R`. Do not type coefficients by hand.
- Bob: paste the Word file into Hogan’s shared live document. Do not email a parallel copy unless Hogan asks.
- Gate 3 remains open.
