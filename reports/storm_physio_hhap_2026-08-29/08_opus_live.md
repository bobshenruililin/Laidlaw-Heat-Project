# Opus physiology-register (live) — 29 August 2026

**Seat:** physiology register. Not Opus 5 Max (quota-blocked). Hogan spare academic English.  
**Surfaces:** say-map §§7–8; crown physiology §6; `writing_standards_hogan.md`; live Discussion paragraphs that open “Candidate mechanisms”, “A corresponding hypothesis”, and “The World Health Organization”; `04_article.md`; `literature/references.bib` keys `chevance2024sleep`, `ioannou2024heatwave`, `oconnor2025bedroom`, `ashe2025ehe`, `ikaheimo2018cold`, `li2026cold`. Builder Discussion string checked in lockstep.

**Locked and not read as editable:** Table 2; Abstract; Hogan’s HKO weather paragraph.

## Verdict

**GO after two clause-level rewrites** in the cold/HF paragraph. Night/CHD and WHO mapping paragraphs did not require a live-text change.

Applied in lockstep to `Heat_CVD_Manuscript_live_update.md`, `scripts/64_hogan_20260824_manuscript_docx.py`, and `04_article.md`. Hogan PDF not rebuilt. Table 2, Abstract, and the HKO weather paragraph untouched.

## Applied old → new (only where wrong)

### 1. Phenotype overspecification (scientific)

Ikäheimo (2018) writes that a **failing heart** has little reserve against cold-induced afterload. Li et al. (2026) write of an already compromised heart and afterload, not of left-ventricular systolic failure as a required phenotype. This cohort is first hospitalisation after first HF diagnosis, without recorded phenotype (HFrEF vs HFpEF). “Failing left ventricle” was not in either cited review’s claim sentence and is not identified here.

**Old:** `a failing left ventricle has little reserve against that load [27,28].`

**New:** `a failing heart has little reserve against that load [27,28].`

### 2. Lab jargon in a journal Discussion (Hogan voice)

The surrounding live Discussion says “this analysis”, “these data”, and “the present counts”. “This file” is internal archive language.

**Old:** `A heat-only reading of this file would miss the more coherent residual.`

**New:** `A heat-only reading of this analysis would miss the more coherent residual.`

No other sentence in the three assigned paragraphs was wrong enough to rewrite.

## Night / CHD (hypothesis) — source check

All of the following are labelled hypothesis. The paragraph states that the studies do not measure first CHD hospitalisation in Hong Kong, do not measure indoor temperature in this series, and that “This panel does not identify that pathway.”

| Claim in live text | Source | Register |
|:--|:--|:--|
| Ambient heat associated with shorter and more fragmented sleep [23] | Chevance et al., *Sleep Med Rev* 2024;75:101915. Published finding: higher outdoor or indoor temperature associated with degraded sleep **quality and quantity**. Fragmentation is among the quality indicators in that literature. Sleep review, not hospitalisation. | Pass. Optional tighter Chevance-own-words phrasing not applied (not false). |
| Ten-day confinement; seven young men; three nights at 26.3 °C; nocturnal core temperature **0.2 °C higher during and after** those nights than before them; total sleep time fell with overnight core temperature [24] | Ioannou et al., *Appl Physiol Nutr Metab* 2024;49:1394–1408, DOI 10.1139/apnm-2024-0105. Nights 4–6: 26.3 °C; nights 1–3 and 7–10: 22.3 °C. Mean nocturnal core temperature 0.2 °C higher during **and after** the heatwave vs pre; +0.3 °C in the first two hours of sleep; TST −14 min per 0.1 °C overnight core temperature. Not T2D/HTN; not Hong Kong; not hospitalisation. | Pass. The required during-and-after clause is present. |
| 47 adults ≥65 years; bedroom temperatures above 24 °C associated with lower heart-rate variability [25] | O’Connor et al., *BMC Med* 2025;23:703. vs nights <24 °C, bins 24–26 / 26–28 / 28–32 °C: OR 1.4, 2.0, 2.9 for a clinically relevant drop in lnRMSSD. The paper’s own conclusion uses “above 24 °C”. Bedroom, southeast Queensland, observational. Not HKO Tmin ≥ 28 °C. | Pass. Outdoor official count is not treated as bedroom temperature. |
| Three studies; blood-pressure findings mixed; none demonstrated sleep as a mediator of hospitalisation [26] | Ashe et al., *Syst Rev* 2025;14:19. Three eligible studies; no CVD outcomes; no formal mediation. Two studies: SBP and DBP fell in the heat; Kim et al.: DBP fell, SBP positive but not significant. | Pass. “Mixed” is the mandated register (say-map §8; crown §6). No nocturnal-dipping theorem. No claim that hot nights raised blood pressure here. |
| Official hot-night flag can be null after mean temperature while hourly nighttime excess heat is not [17] | Guo et al., *Lancet Reg Health West Pac* 2024;51:101168. `HNday28` overall null after multi-day mean temperature; hourly `HNe` associated. Daily hot-season emergency hospitalisation, not monthly first-event CHD. | Pass. Neighbour encoding, not a replication. Monthly official counts are not `HNe`. |

Closing sentence: “nights may matter for CHD because…” sits inside “the physiological claim is therefore a hypothesis” and is closed by “This panel does not identify that pathway.” That is motivation, not a causal chain from this 132-month series (say-map §8).

Indoor temperature is not inferred from outdoor official counts.

## Cold / HF (hypothesis) — source check

| Claim in live text (after rewrite) | Source | Register |
|:--|:--|:--|
| Cold exposure can raise sympathetic outflow, peripheral resistance, and afterload [27,28] | Ikäheimo, *Temperature* 2018;5:123–146: sympathetic vasoconstriction, peripheral resistance, blood pressure, cardiac workload, afterload. Li et al., *Front Physiol* 2026;16:1740919: cold as sympathomimetic stimulus; afterload augmentation; limited reserve in CVD including HF. Capability language (“can”), not a claim that this panel measured the pathway. | Pass. |
| A failing heart has little reserve against that load | Ikäheimo: “A heart failure patient has little physiological reserve… a failing heart may not be able to compensate.” Li: compromised heart / decompensation risk. | Pass after rewrite. |
| Goggins and Chan’s daily Hong Kong HF series is the local epidemiological neighbour, not a magnitude to import [21] | Goggins and Chan, *Int J Cardiol* 2017;228:537–542. Daily HF admissions; cumulative RR 2.63 comparing 11 °C with 25 °C. | Pass. **2.63 is absent** from this paragraph. Questions compared, not magnitudes. |
| Present counts do not measure afterload, blood pressure, or infection | Say-map §7: physiology as interpretation, not a result. | Pass. |
| Official cold-day burden **marks** winters in which those loads are more frequent | Ecological monthly grain. “Marks”, not “causes”. | Pass. No causal verb for the 132-month association. |

Influenza, indoor conditions, and care-seeking remain unseparated [18]. That is a limit, not a mechanism claim.

## 5 / 6 / 8-day myocardial cliff

Absent from the three assigned paragraphs. The preceding Discussion already states that spline degrees of freedom do not describe a physiological duration. The consecutive-days paragraph (test-locked, not rewritten here) states that five additional official days is a reporting scale rather than a consecutive-day trigger. The WHO paragraph states that the estimates do not set a five-day trigger. Crown §6: no myocardial threshold at 5 vs 6 vs 8 days. Pass.

## WHO paragraph (mapping, not physiology identification)

Checked only for causal verbs, indoor-T inference, and duration cliff. “Sits with”, “can inform”, “cannot evaluate”, “mapping, not a test”, “was not measured here”, “do not set a five-day trigger”, “do not count admissions averted”, “do not say whether existing warnings work.” Indoor night temperature is named as an unmeasured exposure-reduction **hypothesis**. Pass. No evaluation of VHWW or of a municipal HHAP.

## Causal verbs for ecological monthly associations

None of the three paragraphs says that official hot nights or cold days caused, produced, or mediated CHD or HF hospitalisation in this cohort. Association language is reserved for the cited sleep, laboratory, bedroom-HRV, and Guo studies. The present panel is closed with “does not identify”, “do not measure”, “marks”, and “sits with”.

## Optional (not applied; not required for GO)

1. Chevance [23]: replace “shorter and more fragmented sleep” with “shorter and poorer-quality sleep” to track that review’s own abstract. Fragmentation is not false; it is a quality indicator. Hogan one-claim-per-sentence is already met.
2. Ioannou [24]: the protocol also used hot days (35.4 °C) during nights 4–6. The live sentence attributes the 0.2 °C nocturnal elevation to three nights at 26.3 °C. The **after** period (nights 7–10 at 22.3 °C) is the non-recovery fact the sentence needs, and it is stated. Adding daytime heat would stack a second exposure into the same clause.
3. Ashe [26]: “mixed” could be expanded to “two of three reported lower blood pressure; one had a non-significant systolic rise.” That would be longer, not safer. The kill list forbids a raised-BP / dipping theorem. “Mixed” stays.

Do not apply (1)–(3) unless a human asks.

## What this seat does not do

Does not freeze Gate 3. Does not paste into Hogan’s shared file. Does not rebuild the Hogan PDF or Stage 3 hashes. Does not touch Table 2, the Abstract, or Hogan’s HKO weather paragraph. Does not import Goggins 2.63 or Guo’s hourly `HNe` as this panel’s coefficient.
