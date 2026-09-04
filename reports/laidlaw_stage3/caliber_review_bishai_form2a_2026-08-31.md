# Caliber review — Laidlaw Stage 3 outputs vs Bishai form 2a

**Date:** 31 August 2026  
**Mode:** Decide. Independent triangulation of the three files Bob uploaded for review.  
**Not:** a Gate 3 freeze, a journal referee report, or permission to quote a confirmatory thermal effect.

**Files examined (Bob’s uploads, not the later repo lock):**

| Object | Bytes | SHA-256 prefix | Created |
|---|---:|---|---|
| `ShenRuililin_Laidlaw_Stage3Report.pdf` | 407,146 | `c083d4096a0924b1` | 22 Aug 2026 17:39 (LaTeX via pandoc) |
| `ShenRuililin_Laidlaw_Stage3Poster.pdf` | 93,978 | `0ef58e0951bb2ffd` | 22 Aug 2026 17:34 (pdfTeX) |
| `2a. Laidlaw - Report Form (HKU).pdf` | 335,946 | `722ba1f70f246c2d` | Word → macOS Quartz; modified 31 Aug 2026 08:49 |

These hashes are the **22 August night foldback** ([`knowledge/2026-08-22_stage3_foldback.md`](../../knowledge/2026-08-22_stage3_foldback.md)). They are **not** the 24 August Hogan-aligned rebuild in `outputs/` (`605cd8db43072cb5` / `a972206e61932650`). Science (the twelve count ratios) is the same. The signed essay still says “core panel”; the 24 August files name nested Model 1 / 2 / 3.

Form date of submission: **23 August 2026**. Supervisor date: **31 August 2026**. That order is consistent with Email A going out on the foldback PDFs, then Hogan’s 24 August comments prompting a repo rebuild that Bishai did not re-sign.

---

## Verdict

The Stage 3 essay and poster are **high-calibre for the Laidlaw research-summer requirement** and **unusually honest for undergraduate epidemiology**. They meet the programme’s length, IMRD, and “academic rigour” bar. They sit slightly above the “accessible to a wide, non-subject-specific audience” brief (the “How to read the estimates” gloss is the concession). They do **not** support a confirmatory heat–CVD finding.

Professor Bishai’s **satisfactory** rating and his judgement of technical level, help-seeking, and partnership are **fair**. His scientific sentence is **not**. It names the weaker residual, generalises the outcome, and drops every hedge the scholar put in the Abstract and Conclusion.

**Agree with the performance assessment. Do not agree that the report “shows an association between 5 days of very hot nights and cardiovascular disease.”** Keep his wording on the form. Do not quote that sentence anywhere else.

---

## 1. What Laidlaw asked for

Printed on page 2 of form 2a:

- a **ca. 2,000–3,000-word** research essay, “accessible to a wide, non-subject specific audience”;
- a research poster;
- academic rigour; supervisor review;
- optional later journal paper with the supervisor.

Report due **31 August 2026**; poster file **15 September 2026**.

The signed packet is complete for the report deadline. The poster is optional for today and is already built.

---

## 2. Essay caliber (the object Bishai examined)

**Length.** Introduction–Conclusion is about **2,560 words** (foldback lock said 2,575). Abstract excluded, as specified. Inside the band.

**Estimand.** Territory-month count ratios of first hospitalisation after first CHD or HF diagnosis in a T2D/HTN cohort, 132 months, admission cause not recorded. Daily triggering, principal-diagnosis CHD/HF, AMI, stroke, mortality attributable fractions, and Roro’s modelled heat deaths are kept distinct. That boundary is the project’s scientific contract, and the essay holds it.

**Numbers.** CHD 156,156 events; HF 29,681; hot nights 1.022 (1.002–1.042), *q* = 0.192; cold days 1.073 (1.006–1.144), *q* = 0.192; all twelve *q* > 0.19. These match the 7 August amended panel, the independent re-fit, and Table 2 of the signed PDF. Provenance is `HA_APPROVED_AGGREGATE`. No invented stroke rows.

**Honesty that is better than typical undergraduate (and many MSc) papers.**

- Full twelve-contrast panel; no significance-count narrative.
- Four-construction uncertainty ladder; CHD Newey–West intervals **narrower** than model-based, with ACF(1) = 0.508 named as a reason for caution.
- Pre-2020 split shown in full: CHD 1.011 (0.991–1.032) includes 1; HF 1.113 (1.053–1.176) excludes 1.
- Daily-from-monthly recovery reported as a **failed 500-replicate calibration**, not as a coefficient.
- Nine numbered limitations, including missing person-time, unresolved pollution/humidity/influenza, HQ weather as a territory proxy, and stroke not delivered.
- Conclusion: “hypotheses, not proof of thermal effects.”

**Craft against Hogan’s writing bar.** Spare, one claim per sentence in Methods and Results. Formal author–date/numbered citations. Collaborators credited by role. Internal gate language is out of the scientific body. A few production nicks: `Xiaofang Y e` line-break in reference 3; full given names rather than Vancouver initials; Hogan cited by given name only.

**Where it is weaker than a journal Methods paper (and the essay says so).**

- The twelve models were specified after the outcome series was available (disclosed).
- Pollution, humidity, and influenza are assembled but not in the reported fits.
- Model 2 (RH + rainfall) and Model 3 (climatology-day counts) are **absent from this signed version**. They exist only in the later 24 August files, still unfitted.
- Accessibility: Newey–West, HC1, Benjamini–Hochberg, and ecological bias are specialist. A non-epidemiology Dean can follow the Abstract and the “How to read” box; they will not follow the SE ladder without effort. That is a programme-brief tension, not a scientific defect.

**Relative standing.** For a Year 2 BASc Laidlaw scholar this is well above the usual summer-research essay. It is an identification article, not a discovery article. That is the correct genre for these data.

---

## 3. Poster caliber

One ISO A0 portrait page (841 × 1189 mm). Required sections are present, plus Interpretation/Limitations and a six-item REFERENCES strip.

**What is strong.** The visual argument is the whole twelve-contrast forest plus the four-SE ladder for the two residuals. Pre-2020 callouts are unequal on purpose (CHD includes 1; HF excludes 1). The conclusion box repeats “exploratory, not confirmatory.” Footer names Hogan, Zhenyuan Liu, and Bishai.

**What is compressed.** Official hot-night rise 10 → 61 is an environmental descriptor, correctly captioned. “Hospital burden complements mortality” is a short-hand that the essay handles more carefully. Density is high for a non-specialist showcase; it would compete for a methods-honest prize, not a splashy-finding prize.

Poster file deadline is 15 September. Today’s Horizons packet does not require it.

---

## 4. Form 2a as an administrative object

| Field | Content | Note |
|---|---|---|
| Name / curriculum / year | Shen Ruililin; BASc(Global Health and Development); Year 2 | Year 2 on the form |
| Supervisor | Prof. Bishai, David Makram | |
| Topic | Exploratory monthly CHD/HF first-hospitalisation study, 2013–2023 | No AMI/stroke/confirmatory headline |
| Attachment period | 4 July – 14 August 2026 | Work continued after 14 Aug; normal form lag |
| Student signature | Handwritten “Bob Shen”; 23 August 2026 | |
| Rating | **satisfactory** circled (Preview circle around the left word) | Binary; comments carry the real judgement |
| Supervisor comments | Typed paragraph (verbatim below) | |
| Supervisor name / signature / date | Prof David Makram Bishai; blue-ink signature; 31 August 2026 | |

The signed file should stay local. Do not put the signature image in git.

---

## 5. Bishai’s comments, sentence by sentence

Verbatim:

> Bob has done some highly technical original research that shows an association between 5 days of very hot nights and cardiovascular disease. He has performed at a level not typically seen for first year undergraduates, but I am not surprised. He has asked for help when needed and formed an effective partnership with other researchers.

The pack offered him a more accurate paste ([`analysis_plan/send_pack_2026-08-24/suggested_supervisor_comments.md`](../../analysis_plan/send_pack_2026-08-24/suggested_supervisor_comments.md)). He wrote his own, as that file said he might.

| Claim | Independent reading |
|---|---|
| **Satisfactory** | **Agree.** It is the only positive box. The comments then elevate. |
| **Highly technical** | **Agree.** Separate-exposure NB panel, days offset, four SE constructions, BH *q*, pre-2020 split, failed daily-recovery gate. That is unusual undergraduate technique. |
| **Original research** | **Partly agree.** Original governed analysis and an original *identification* contribution (what monthly first-event counts cannot support). Not original as a new heat–CVD effect. |
| **“shows an association between 5 days of very hot nights and cardiovascular disease”** | **Disagree as science.** See below. |
| **Level not typically seen for first-year undergraduates** | **Agree on caliber; mild year mismatch.** The form says Year 2. The compliment still holds for early undergraduate work. |
| **Not surprised** | Interpersonal, not a finding. Leave it. |
| **Asked for help / effective partnership** | **Strongly agree.** Weather co-investigator (Hogan), outcome co-investigator (Zhenyuan Liu), diagnosis-record assistance (Jingjing Zhou), concept supervision (Bishai). This is the most accurate sentence in the box. |

### Why the association sentence is the wrong summary of this scholar’s own report

1. **Exposure name.** The essay and HKO series use **hot nights** (Tmin ≥ 28 °C). “Very hot days” are Tmax ≥ 33 °C. “Very hot nights” is the Wang/Ren–Roro heatwave dialect for the same 28 °C night threshold. Bishai is on that mortality paper. The slip is lab language, not a different exposure — but it is not the language of the signed essay.

2. **Outcome.** The event is **first hospitalisation after first CHD diagnosis** (and separately HF) in a T2D/HTN cohort, **without recorded admission cause**. It is not “cardiovascular disease,” not principal-diagnosis CHD, and not AMI.

3. **Which residual.** The essay treats **HF × cold days** as the more coherent leftover (all four SEs exclude 1; stronger before 2020). Bishai named only the **CHD × hot-night** residual, which is smaller, SE-sensitive (model-based 0.995–1.049 and HC1 include 1), and compatible with 1 in 2013–2019 (1.011, 0.991–1.032).

4. **Strength.** Both leading *q*-values are **0.192**. Every *q* exceeds 0.19. Abstract: “The data do not support a multiplicity-protected thermal claim.” Conclusion: “hypotheses, not proof.” The supervisor box asserts the claim the body refuses.

5. **Contrast per five days.** The “5 days” increment is correct. That is the only quantitative piece that matches Table 2.

This is the exact over-claim the project’s non-negotiable rules exist to block: monthly first-event count ratios must not be narrated as a CVD heat effect.

It is also a familiar supervisor pattern: the programme story is rising hot nights; the more coherent residual in these data is winter cold and heart failure (directionally aligned with Goggins and Chan 2017, not a magnitude replication).

---

## 6. Do the three documents agree with each other?

| Check | Essay | Poster | Form 2a comments |
|---|---|---|---|
| Exploratory / all *q* > 0.19 | Explicit | Explicit | Absent |
| CHD hot nights 1.022 per 5 days | Yes, with SE and window hedges | Yes, with the same hedges | “association” without hedges |
| HF cold days 1.073, more coherent | Yes | Yes | Omitted |
| First-event, no admission cause | Yes | Yes | Collapsed to “CVD” |
| Stroke / AMI | Not claimed | Not claimed | Not claimed (good) |
| Daily coefficient | Refused | Next-study only | Not mentioned |
| Partnership | Acknowledgements | Footer | Accurate |

Essay and poster are aligned. The supervisor box is the odd one out, and it is the odd one out in the **generous-PI** register, not in the **unsatisfactory** register.

---

## 7. What to do now (human)

1. **Submit today** to `laidlaw@hku.hk`: endorsed form 2a + the **22 August foldback essay** (`c083d4096a0924b1`). That is the file he examined. Do not attach the 24 August Hogan-aligned PDF (`605cd8db43072cb5`) unless he re-reads it.
2. **Keep his wording.** Do not tidy the comments box.
3. **Do not quote** the association sentence on LSN, the Laidlaw blog, the live manuscript, or any press-like summary. Quote the scholar’s Abstract if a one-liner is needed.
4. **Poster** can wait until 15 September. If the showcase file is updated to the 24 August Hogan-aligned poster, say so; it is not the signed object.
5. **Gate 3 remains open.** A satisfactory Stage 3 form is not a confirmatory primary and not journal authority. IRB, ICD/timing, authorship, and person-time are unchanged.

---

## Provenance of this review

Text extracted from the three uploads; pages rendered; SHA-256 compared to `knowledge/2026-08-22_stage3_foldback.md` and `analysis_plan/send_pack_2026-08-24/HASH_VERIFY.md`; coefficients checked against `reports/laidlaw_stage3/results_panel_chd_hf_2026-08-07.md` and `reports/chd_hf_independent_review_2026-08-07.md`. Signed form not copied into git.
