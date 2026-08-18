# Independent Round B — readability pass on the applied revisions

**Reviewer.** Opus-5 Max, manuscript architect. Round B reads the current `Heat_CVD_Manuscript_live_update.md` after the parent applied selected Round A replacements. Round A's memo is `independent_round_a_opus5_20260815.md` and is not restated here.

**Question for this round.** The applied revisions are technically correct. Do they still read as Hogan spare English, and did any of them create throat-clearing, doubled sentences, or claim-and-order problems?

**Constraint.** No numbers added. Paste-ready fixes only where a defect is real. Every quotation below was checked to appear exactly once in the current file.

---

## Verdict

The seven applied changes hold. The Abstract now leads with the null; figures are cited in the order 1, 2, 3, 4; Strengths and limitations precedes the Conclusion; the mean-temperature adjustment asymmetry with Guo et al. is stated; the comparative claims are gone; the 2023 exposure counts have a source; and the prescription limitation is recorded where Hogan asked for it.

Nine readability defects follow, and seven of them are side effects of the fixes rather than pre-existing problems. Two are worth doing first: a clause that now appears verbatim in two sections, and a Methods paragraph that says the same thing three times.

One substitution is a genuine scientific improvement and should not be reverted: replacing "It is not produced by entering correlated heat metrics jointly" with a statement about the joint diagnostic. The old sentence made a causal-sounding claim about what did not produce the association; the new one reports what the diagnostic showed.

---

## 1. A caveat clause now appears verbatim in two sections

"differences between exposure encodings were not formally tested" appears in both the Discussion opening and the Conclusion. It belongs where the comparison is made. In the Conclusion the next sentence already carries the caveat, so the repetition also produces two consecutive hedges.

Current (Conclusion): `In governed monthly aggregates for people with type 2 diabetes and/or hypertension, the largest count ratios were for hot nights in CHD and for cold days in HF; differences between exposure encodings were not formally tested.`

Replacement: `In governed monthly aggregates for people with type 2 diabetes and/or hypertension, the largest count ratios were for hot nights in CHD and for cold days in HF.`

The following sentence, "Neither association survived correction across the twelve comparisons", is left untouched and does the caveat work.

## 2. The Discussion opening sentence is now 49 words

The same clause makes the Discussion's second sentence the longest in the section. Split it at the semicolon; keep the clause here, since this is where the comparison is made.

Current: `Under Newey–West lag-6 reporting for the core panel, the largest CHD count ratio was for official hot-night burden rather than for mean temperature or cold days, and the largest HF count ratio was for cold-day burden rather than for hot nights; differences between exposure encodings were not formally tested.`

Replacement: `Under Newey–West lag-6 reporting for the core panel, the largest CHD count ratio was for official hot-night burden rather than for mean temperature or cold days, and the largest HF count ratio was for cold-day burden rather than for hot nights. Differences between exposure encodings were not formally tested.`

## 3. The new pollution paragraph states its point three times, and one "because" does not earn its conclusion

The added sentences rename the same models twice and then assert that they are alternative associational specifications *because* the role of ozone is not established. The ozone rationale is already given one sentence earlier in the same paragraph, so the clause reads as doubling, and the inference it announces is a definition rather than a consequence.

Current: `Pollution covariates were examined only in staged archive models. Because the role of ozone relative to temperature is not established from these aggregates, those models are alternative associational specifications. They do not identify mediation or show that confounding is resolved.`

Replacement: `Pollution covariates were examined only in staged models outside the core panel. Those models are alternative associational specifications: they do not identify mediation, and they do not show that confounding is resolved.`

## 4. Two Methods sentences are now redundant with the paragraph above

With item 3 in place, the Statistical analysis subsection repeats commitments already made in the Weather and pollutants subsection, and "confounding is resolved" appears twice in Methods. Humidity and influenza are each already excluded from the core panel in their own paragraphs, so nothing is lost by deleting the pair.

Current: `Archive models that entered pollution, humidity, or influenza are not adjusted versions of the separate core panel. They were not used to claim that confounding is resolved.`

Replacement: delete both sentences. The Discussion retains "Archive models in which they enter are not adjusted versions of the core panel", and Limitations retains "Confounding by pollution, humidity, and influenza is unresolved in the core panel".

## 5. A trailing clause negates what its own noun already says

"Joint coefficients are diagnostics, not preferred estimates" is already in Results, and the noun in this sentence is "diagnostic". The relative clause adds no information.

Current: `Its point estimate was similar in the joint extreme-day diagnostic, which was not designated as a preferred model.`

Replacement: `Its point estimate was similar in the joint extreme-day diagnostic.`

## 6. Two consecutive sentences open with "It does not"

Splitting the Guo sentence left three short sentences in a row, the last two with the same pronoun subject and the same opening. The fix keeps one claim per sentence and removes the echo.

Current: `A *q*-unprotected hot-night count ratio is what that design can support. It does not conflict with the official-flag result in Guo et al. [17]. It does not show that hourly nighttime intensity is absent.`

Replacement: `A *q*-unprotected hot-night count ratio is what that design can support. It does not conflict with the official-flag result in Guo et al. [17]. Nor does it show that hourly nighttime intensity is absent.`

## 7. The adjustment asymmetry is buried at the end of a four-item list

The added item is the substantive one, and it is a statement about the models rather than about the data. Ending a list of three data descriptors with it flattens it. Give it its own sentence.

Current: `The present analysis uses monthly official counts, a first-event CHD series, a later decade, and models that carry hot nights without adjustment for monthly mean temperature.`

Replacement: `The present analysis uses monthly official counts, a first-event CHD series, and a later decade. Its hot-night models carry no adjustment for monthly mean temperature.`

## 8. The prescription sentence doubles its own clause and overstates what the spline absorbs

"Absorbed by" already implies inseparable, so the second clause repeats the first. The larger issue is a claim one: a four-degree-of-freedom spline of month index absorbs gradual change, while calendar-month indicators absorb seasonal change; an abrupt formulary or guideline shift would be absorbed by neither.

Current: `Monthly prescription fields were not in the released aggregates, so changes in therapy are absorbed by the time spline and are not separable from it.`

Replacement: `Monthly prescription fields were not in the released aggregates. Changes in therapy were therefore not examined, and any gradual change of that kind is not separable from the time spline.`

## 9. The same 2023 counts now carry two different sources

The Results paragraph attributes the 2023 exposure counts to the new yearbook reference, while the Introduction still attributes the 2023 cold-day count to the open-data reference. The numbers agree; the sourcing does not.

Current (Introduction): `Cold days persisted across the period (14 in 2013, 13 in 2021, and 14 in 2023) [2,4,6].`

Replacement: `Cold days persisted across the period (14 in 2013, 13 in 2021, and 14 in 2023) [2,4,22].`

**Consequence to settle in the same pass.** That change leaves reference 6 cited nowhere, joining references 3 and 5. The open-data reference is the natural citation for the daily Headquarters series in the Weather processing paragraph, which currently carries no citation. Cite it there, or remove 3, 5, and 6 together as one list-hygiene decision. Do not add a reference that has not been checked.

---

## Abstract wording, lower priority

The reordered Results paragraph works. Two small things came with it.

**"twelve" three times, "Benjamini–Hochberg" twice.** The Methods paragraph already establishes the twelve core contrasts one paragraph earlier, so the opening clause can drop its count.

Current: `No contrast in the twelve-model panel reached a multiplicity-protected threshold: all twelve Benjamini–Hochberg *q*-values exceeded 0.19. The two largest associations, under Newey–West lag-6 reporting, were 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF, both with *q* = 0.192.`

Replacement: `No contrast reached a multiplicity-protected threshold: all twelve Benjamini–Hochberg *q*-values exceeded 0.19. Under Newey–West lag-6 reporting, the two largest count ratios were 1.022 (1.002–1.042) per five hot nights for CHD and 1.073 (1.006–1.144) per five cold days for HF, both with *q* = 0.192.`

Two gains beyond rhythm. Fronting the reporting choice removes a mid-sentence appositive. More importantly, "largest count ratios" is exactly true of the printed values, whereas "largest associations" invites a magnitude reading that the HF mean-minimum-temperature row would contest: on the log scale that ratio sits slightly further from 1 than the CHD hot-night ratio does.

**"multiplicity-protected" twice in the Abstract.** The Conclusions sentence now nearly repeats the new Results opener, and the only word carrying new content is "differential". Optional replacement, which keeps the hedge and reuses the Conclusion's own vocabulary:

Current: `The data do not support a multiplicity-protected differential thermal claim.`

Optional replacement: `The differential pattern of heat for CHD and cold for HF does not survive correction across the twelve comparisons.`

Do not adopt this if the team prefers the hedge stated as an adjective; the repetition is tolerable, and weakening or strengthening the hedge for rhythm would be the wrong trade.

---

## Pre-existing, not from this round

- **Mixed tense in Results §Core panel.** `All twelve *q*-values exceeded 0.19. No contrast meets a multiplicity-protected confirmatory threshold in this exploratory panel.` Past then present, in adjacent sentences. Set both in the past.
- **Figure 3 caption repeats the in-text sentence.** The text gives July 2022 and its count, and the caption then gives the colour-scale maximum as the same month and count. One of the two can go, and the caption is the better place to lose it.
- **Four labels for one pair of contrasts.** The Abstract, Table 3 caption, the residual paragraph, and the Discussion each name the pair differently. If one label is wanted, "the two largest count ratios" is the only one that is literally true of the values; "the two remaining associations" in the Discussion means something different and should stay.
- **References 3 and 5 remain uncited**, as reported in Round A.

## Checked and sound, no change proposed

Figure renumbering is complete and internally consistent: the hot-night display is Figure 3 in text, caption, and image line; the residual display is Figure 4; the Discussion's hot-night call points to Figure 3; and the caption sentence "The layout matches Figure 2" is still correct. Moving Strengths and limitations above the Conclusion did not orphan any reference or create a repetition with the Discussion's closing paragraph. The lengthened title is at the upper end of what a journal will take, but each element in it is load-bearing and the author note already reserves a shorter running head.
