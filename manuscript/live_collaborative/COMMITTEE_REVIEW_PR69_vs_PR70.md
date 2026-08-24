# Committee brief — PR 69 vs PR 70 (Hogan 24 August Methods)

**For:** editor of [PR 70](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/70) and the review committee.  
**Subject of review:** [PR 69](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/69) (this branch).  
**Date:** 24 August 2026.  
**Question:** which live-manuscript pack should Bob paste into Hogan’s shared file?

PR 69 and PR 70 were parallel attempts at the same Hogan request. They were **not** merged. PR 69 is the merge-by-hand: it took PR 70’s numbering and then kept or rejected other PR 70 choices against Hogan’s 24 August PDF + email, Fable’s locked forks, and the scientific contract (do not invent HA coefficients or an IRB number).

| | PR 69 (this pack) | PR 70 (parallel) |
|---|---|---|
| URL | https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/69 | https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/70 |
| Branch | `cursor/hogan-methods-rewrite-1754` | `cursor/hogan-methods-rewrite-b75b` |
| Base | `main` | `main` |
| Status | Open, ready for review | Open, draft |
| Hogan-facing file | Full manuscript **Word + PDF** | Methods-only Word paste |
| Paths | `manuscript/live_collaborative/Heat_CVD_Manuscript_20260824_hogan.docx` and `.pdf` | `manuscript/live_collaborative/Heat_CVD_Methods_20260824_paste.docx` |

Bob’s instruction after comparing the two was: produce a final Word then PDF that would satisfy Hogan, using Fable as the human for remaining forks. That file is on PR 69. Paste it into the shared live document; do not email a competing copy unless Hogan asks.

---

## 1. What PR 69 took from PR 70 (kept)

These were PR 70 wins. PR 69 adopted them because they fix Hogan’s email and Table 2 honesty.

| Item | Why PR 70 was right | Where it now lives in PR 69 |
|---|---|---|
| Nested **Model 1 / Model 2 / Model 3** | Hogan asked for numbered models a high-school reader can follow. Naming the twelve thermal fits “Models 1–12” (early PR 69) made Table 2 disagree with Methods once RH/rain were added to every model. | Abstract Methods; Methods statistical analysis; Results heading **Model 1** |
| **Table 2 = Model 1** | The numbers already in Table 2 were fitted **without** RH/rain. They must stay Model 1 until a governed-panel refit. | Table 2 caption; Word comment on Table 2 |
| **KW15 = rescaling, not new fits** | If the per-5-day count ratio is *R*, per 3 days is *R*^(3/5) and per 1 day is *R*^(1/5). Same coefficient. | Sensitivity analysis |
| **[21] for humidity only** | Goggins and Chan 2017 entered temperature, humidity, and wind speed — not rainfall. Citing [21] for rainfall is an error Hogan can catch. | Model 2 paragraph |
| Contract tests | PR 70’s `tests/test_hogan_methods_rewrite.py` is the right idea. | Same path on PR 69, adapted to the locks below |
| Shorter Methods with the equation in words | Hogan: Methods too complex. | Model 1 equation, then a plain-language definition of every symbol |

---

## 2. What PR 69 rejected from PR 70 (and why)

These would reopen balloons Hogan already closed, or put WIP / Results where he forbade them.

| PR 70 choice | PR 69 choice | Why |
|---|---|---|
| Ethics sentence **without** `UW XX-XXX`, and ethics at the **end** of Methods | Keep Hogan’s `UW XX-XXX` at the **start** of Methods | He typed the placeholder and put the one-sentence approval there (KW10/KW11). Deleting it erases his edit. Inventing the number is forbidden. |
| Health data names “outcome co-investigator”, `chd_inpatient` / `hf_inpatient`, and “stroke named in correspondence” | Strip those. Body describes the delivered CHD/HF series only. Stroke limitation: “A corresponding stroke series was not available for this analysis.” | Hogan: no WIP in the body. File labels and correspondence are comments, not manuscript sentences. |
| Italic author-order sentence in the body | Placeholders stay; order is a **Word comment** | Same WIP rule (H2). |
| Abstract Methods still contains the daily-recovery **calibration failure** | Failure stays in **Results** only. Abstract Methods says “Reported estimates are from Model 1.” | Hogan: no Results in Methods, including the Abstract. |
| Software **without** version numbers | Keep R 4.3.3 / MASS / sandwich versions | KW18: “Good.” Unrequested cuts create new review. |
| Body sentence that **corrects** Hogan’s averaging sentence (rainfall is a total, not an average) | Averaging sentence **verbatim**. Precision is a Word comment only. | Do not overwrite his HKO paragraph. His list already says “total rainfall.” |
| Acknowledgements `None.` | Same (kept) | KW19. |
| Model 3 as warmer/cooler vs same-date mean, without splitting mean vs max/min | **Primary Model 3 = daily mean** warmer/cooler. Max/min counts are **sensitivities**. | Hogan asked mean/max/min. Six counts as one model is collinear and harder to read. Fable locked this split. |
| No [22] | Add Chan, Goggins et al. 2013, *Bull World Health Organ* 91:576–584, doi:10.2471/BLT.12.113035 as **[22]** | Hogan’s rainfall–attendance memory is that paper (rainfall entered because heavy rain may deter attendance). It is **not** Goggins and Chan 2017. PR 69 does **not** claim [22] found a CVD–rainfall effect; it states the hypothesis they used to enter rainfall. |
| Methods-only `.docx` | Full manuscript Word + PDF, Hogan weather paragraph copied, figures 1–3 in | Bob asked for a final file Hogan can read tonight. |
| `LIVE_DOC_EDITS.md` still carrying the **15 August** paste list | 24 August is the only controlling paste path | Re-pasting 15 August would restore DJF under Weather and daily-recovery in Abstract Methods. |

---

## 3. What neither PR may do (shared must-nots)

Committee should fail the pack if any of these appear.

1. Invented Table 2 / Model 2 / Model 3 **health** coefficients. Governed panels are absent. PR 69 flags Model 2 with `scripts/53_hogan_models_rh_rain.R` and a Word comment.
2. Invented IRB number.
3. Overwrite of Hogan’s HKO paragraph, including “All monthly data were derived by taking the average of daily data in each calendar month.”
4. “core panel” / “twelve core contrast.”
5. Results in Methods (141 of 145 cold days; VIF; Type I / calibration failure).
6. Jingjing TV-day counts. TV has no threshold.
7. Rebuild of Stage 3 PDFs (byte-lock `c083d4096a0924b1` / `0ef58e0951bb2ffd`).
8. Citing Goggins and Chan 2017 [21] as the rainfall paper.

---

## 4. How to read Model 1 / 2 / 3 in PR 69

| Name | What it is | In Table 2? |
|---|---|---|
| **Model 1** | Twelve separate negative-binomial fits: six thermal variables × CHD/HF. Offset = number of days in the month. No RH, no rainfall in the equation. | **Yes.** These are the existing numbers. |
| **Model 2** | Model 1 + monthly mean RH + monthly total rainfall. | **No.** Specified. Not fitted. |
| **Model 3** | Same structure as Model 1, but official extreme-day counts replaced by days above/below the leave-one-year-out same-calendar-day **mean** of daily mean temperature. Max/min versions are sensitivities. | **No.** Specified. Weather counts exist (`data_processed/hogan_abnormal_day_counts_2013_2023.csv`, 132 months). Health coefficients not invented. |

KW15 is not Model 4. It is a scale change of Model 1 extreme-day coefficients.

---

## 5. Suggested committee checklist

Work from PR 69’s PDF (`Heat_CVD_Manuscript_20260824_hogan.pdf`) plus PR 70’s Methods markdown if you want the parallel draft.

1. Open PR 69 PDF page 1. Cover line present? Abstract names Model 1/2/3 and does **not** mention calibration failure?
2. Methods page: Hogan weather paragraph verbatim, including the averaging sentence?
3. Ethics: one sentence at the **start**, `UW XX-XXX` kept?
4. Health data: no co-investigator / `chd_inpatient` / correspondence?
5. Model 1 equation has **no** RH or rainfall terms?
6. Model 2 cites [21] humidity and [22] rainfall-as-attendance-hypothesis, and does **not** say Goggins 2017 used rainfall?
7. Model 3 primary = daily mean; max/min in Sensitivity?
8. Acknowledgements = `None.` Author-order italic **absent** from the body?
9. Table 2 caption = Model 1, and numbers match the old thermal-only table (CHD hot nights 1.022; HF cold days 1.073; all twelve *q* > 0.19)?
10. Software still has version numbers?
11. `python3 tests/test_hogan_methods_rewrite.py` on the PR 69 tree.

If the PR 70 editor prefers a different lock (ethics at end; no [22]; six-count Model 3 as primary; no cover line), write the dissent against this brief rather than against an undocumented chat.

---

## 6. Human items the committee cannot close from either PR

- Roro: replace `UW XX-XXX`; confirm ICD/timing if they differ.
- Governed-panel machine: `Rscript scripts/53_hogan_models_rh_rain.R` to produce Model 2 numbers. Do not type them by hand.
- Bob: paste the PR 69 Word file into Hogan’s shared live document.

Gate 3 remains open. No AMI / principal-dx / stroke result.
