# Comment-resolution ledger — Hogan 28 July 2026 threads

Statuses allowed: `implemented` · `answered with evidence` · `requires analysis` · `requires author decision` · `blocked by unavailable data` · `deferred until Results` · `rejected` (with scientific reason).

Do not resolve these silently in Hogan’s shared file. Paste replies from the last column. Weather paragraph is not a comment thread; it is copied verbatim.

| ID | Original concern | Action taken (15 Aug re-audit) | Evidence | Resulting live-file text | Status | Author decision remaining? |
|---|---|---|---|---|---|---|
| 0 | Running title provisional until Results exist | Title already names the delivered estimand (CHD/HF first hospitalisation, 2013–2023), not AMI/stroke. Added a strikeable working-title note. A shorter running head is still Hogan’s to set. | Results tables exist (`table2_core_models.csv`); Gate 3 still open, so emphasis is not frozen. | Title + italic working-title note under affiliations. | `implemented` (estimand title) + `requires author decision` (short running head) | Yes — shorter running head |
| 1 | Authors 2–4 with Bishai | Placeholders retained. Roles only in Acknowledgements. | No authorship decision in repo. | `Author 2–4` placeholders. | `requires author decision` | Yes — order / co-first |
| 3 | Remove “Acute myocardial infarction and” because scope changed? | Removed as **this study’s endpoint**. Goggins 2013 AMI remains local daily history. Inspected Abstract, Methods, Tables, Discussion, Conclusion, References: no AMI/stroke coefficient is reported. Goggins and Chan 2017 added as closer daily HF history [21]. | Roro delivered CHD/HF first-event aggregates; stroke named and not attached. | Intro no longer claims AMI/stroke as endpoints. | `implemented` | No, unless Hogan wants AMI wording restored as history only (already present via [1]) |
| 4 | Cite listed factors; if no housing/behaviour data, do not mention them; consider **medication** instead | Housing, behavioural adaptation, and air-conditioning **omitted** from the paper body (Hogan’s rule: do not dangle uncontrolled factors). Medication **also omitted**: it is not in the monthly aggregates, so naming it would create the same dangling-factor problem. Physiological reviews [9,10] stay as general citations, not as measured covariates. Appendix listing of unmeasured factors **rejected** for the same reason. | `data_processed/variable_dictionary.csv` has no medication/ATC/prescription field. Release tables and `outputs/release_chd_hf/` likewise. Bishai July Table 1 listed medications/BMI as ambition; they were not delivered. | Intro does not name housing, behaviour, AC, or medication. | `implemented` + `answered with evidence` | Yes — Hogan may still prefer a Limitations mention of medication. **Recommended default: keep omitted.** |
| 8 | “Environmental context has also evolved” reads as pollutant change after Goggins 2000–2009 | Rewritten to **2013–2023** general-station means. No reconstruction of 2000–2009 EPD concentrations. Direction independently consistent with HKSAR GIA annex integers (NO₂ 54→32; PM2.5 31→15; O₃ 43→58). | `outputs/tables/pollution_annual_means_general_2013_2023.csv`; GIA 7 Feb 2024 annex (see `knowledge/2026-08-13_pi_hko_yearbook_check.md`). | Intro pollution paragraph: NO₂ 53.7→32.1; PM2.5 30.8→14.6; O₃ 42.6→58.3 µg m⁻³. Ozone wording further tightened this pass (associational, not “pathway variable”). | `implemented` + `answered with evidence` | No, unless Hogan wants a 2000–2009 vs 2013 reconstruction (would need a new primary EPD source) |
| 9 | Combine thesis into one sentence; leave until Results, then amend | Last Introduction paragraph is one estimand sentence. Results exist, but the team has not frozen a headline. Sentence remains **provisional**. Alternative formulations live in [`approach_registry.md`](approach_registry.md), not in the paper. | Gate 3 open; all twelve *q* > 0.19. | One closing Intro sentence. | `implemented` (one sentence) + `deferred until Results` freeze | Yes — freeze wording after team Gate 3 |
| 54 | Yang CY, not Yang C-Y | Kept in reference 1. | Goggins et al. *Int J Cardiol* 2013 author line. | `Yang CY` | `implemented` | No |

## Weather Methods (not a numbered comment)

Hogan’s paragraph is copied **verbatim**, including “Meteorological data was obtained from the HKO.” A processing paragraph follows and does not edit his sentences.

## Paste-ready replies (unchanged scientific content; 15 Aug medication/pollution audit explicit)

**0.** Amended the title to the delivered CHD/HF first-hospitalisation estimand. I left a working-title note so a shorter running head can still be set after the team freezes Results emphasis.

**1.** Left Author 2–4 as placeholders pending discussion with Professor Bishai.

**3.** Removed AMI/stroke as our endpoints. Goggins 2013 stays as local daily AMI history. Goggins and Chan 2017 is the closer daily HF admissions paper; those coefficients are not transferred to our monthly first-event counts.

**4.** Agreed on housing and behavioural adaptation: we do not have those data, so they are not named. I also omitted medication. It is not in the released monthly aggregates (no ATC/prescription field), and naming it would raise an uncontrolled factor in the same way housing would. Citations now attach to factors the design actually handles, or to general mechanism reviews.

**8.** Rewritten with 2013–2023 EPD general-station means (NO₂ and PM2.5 down; ozone up). I did not reconstruct 2000–2009 concentrations, so this is not a claim about change immediately after Goggins’ window.

**9.** Combined into one closing sentence now that the CHD/HF panel exists. Happy to amend the sentence after a team freeze of Results emphasis.

**54.** Kept as Yang CY.
