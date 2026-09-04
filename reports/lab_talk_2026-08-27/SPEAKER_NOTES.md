# Speaker notes — lab talk, Thursday 27 August 2026

**Audience:** Professor Bishai plus the lab.  
**Job:** walk the summer honestly; show the Stage 3 paper; manage novelty; report Hogan’s comments; leave a clean path to form 2a.  
**Length:** 25 minutes tight / 35–40 minutes full + questions.  
**File to share:** `reports/lab_talk_2026-08-27/slides.html` in Chrome, full screen (F11). Arrows or click to advance. Keep `ShenRuililin_Laidlaw_Stage3Report.pdf` in chat, not as the talk. 17 slides.

If you are sharing the **24 August** PDF (nested Model 1 / 2 / 3), say “Model 1” wherever these notes say “twelve-comparison panel.” The numbers are the same. If you are sharing the **22 August** PDF, stay with “twelve comparisons.”

Do not say we found a heat or cold effect. All twelve *q* > 0.19.

---

## Format (read this once)

Screenshare the **paper PDF page by page** only if someone asks to see a specific table. On Zoom, an 11-page article is too small, too slow, and looks like you are reading. A short deck with four snippets is the right object:

1. title page of the essay (say it exists; optional),
2. the forest (slide 9),
3. the two leading estimates with the *q* line (slide 10),
4. the conclusion sentence (slide 11).

The poster is a Laidlaw artefact, due 15 September. No signature on it today.

**Open in 90 seconds, before the science:**

> I have two jobs in this meeting. First, to introduce the intern project to the lab: what we asked, what file arrived, what we can and cannot claim. Second, this is the Laidlaw Stage 3 research report, due 31 August. At the end I will ask Professor Bishai for the supervisor block on form 2a. The journal file with Hogan is a separate document. I am not asking anyone to sign that today.

Then stop. Let Bishai nod. Then start slide 3.

---

## Part A — Where this sits in the lab (slides 3–4, ~5 min)

The lab already has two complementary objects. Do not mix their numbers into ours.

| Lab object | Estimand | What it is not |
|---|---|---|
| Jingwen Liu et al., 2020 (Jasmine) | Daily mortality attributable fraction, Hong Kong, 2006–2016 | Not hospitalisation; not our CHD/HF counts |
| Zhenyuan Liu et al., 2026 (Roro) | Modelled heatwave excess deaths, 2014–2023 | Not our first-event counts; do not quote 1,455–3,238 as this paper |
| This intern project | Monthly CHD and HF **first hospitalisation after first diagnosis**, T2D/HTN, 2013–2023 | Not AMI; not principal-dx; not daily DLNM; not stroke |

Say: *A mortality attributable fraction, a modelled excess-death total, and a monthly count ratio cannot be substituted for one another.* That sentence is in the essay. It is the lab-introduction sentence.

Bishai’s direction (name him): complete heat **and** cold in one panel; report every comparison; do not hunt a single confirmatory association.

---

## Part B — How the summer actually ran (slides 5–6, ~6 min)

Walk process, not heroics.

1. **July.** Recalibration: general HA extract has no admission cause. No AMI / principal-dx panel from that file. Stroke was named as the intended morbidity layer.
2. **Weather with Hogan.** Official HKO thresholds; hot-night / cold-day counts; his live weather paragraph is primary. Do not overwrite it in this talk.
3. **6–7 August.** Roro delivered CHD and HF first-event monthly aggregates. Stroke was not attached. No stroke coefficient exists. Say that once, clearly, to the room.
4. **After the file.** Twelve separate-exposure negative-binomial fits (CHD/HF × six thermal measures), days-in-month offset, four uncertainty constructions, Benjamini–Hochberg across twelve. Provisional hot-month / cold-month catalogue exists; Hogan’s reference-period lock is still open.
5. **Daily extension.** We tried a monthly-outcome / daily-exposure recovery. Calibration failed. No real daily coefficient was applied. That is a result: a refusal, not a missing appendix.

Events, if asked: CHD **156,156**; HF **29,681**; **132** months. Monthly means 1,183.0 and 224.9.

---

## Part C — Walk the Stage 3 paper (slides 7–11, ~12 min)

Slide 7 estimand; slide 8 twelve comparisons (say “Model 1” if the 24 August PDF is open); slide 9 forest; slide 10 the two estimates; slide 11 the *q* line.

Follow IMRD. Do not read Methods aloud. Point.

**Question.** Are monthly thermal contrasts associated with monthly first-hospitalisation counts in this cohort?

**Estimand.** Ecological **count ratio**, not incidence. No person-time. No admission cause. First hospitalisation after first CHD/HF diagnosis — not “a heat-caused AMI.”

**Methods, one breath.** Separate negative binomial for each outcome × each exposure. Calendar month + smooth trend + days offset. Intervals: model-based, HC1, Newey–West lag 3 and lag 6. Main display is lag 6. Multiplicity: twelve comparisons.

**Results.** Most intervals include 1. Two largest:

- CHD hot nights / 5 days: **1.022 (1.002–1.042)**, *q* = **0.192**. Two of four SE methods include 1. Pre-2020: **1.011 (0.991–1.032)**. Lag-1 residual ACF **0.508**. Treat as SE-sensitive, pandemic-period-sensitive.
- HF cold days / 5 days: **1.073 (1.006–1.144)**, *q* = **0.192**. Concordant across four SE methods. Pre-2020 stronger: **1.113 (1.053–1.176)**. Official cold days: **141 of 145** in December–February. Identified between winters, not summer vs winter.

Then the line that must be said in full:

> After correction, every *q*-value exceeded 0.19. The panel provides no confirmed association.

**Conclusion of the paper.** Hypotheses, not proof. What remains is a defined first-event outcome, a complete twelve-comparison panel, four uncertainty methods, and a documented refusal of daily coefficients.

If Bishai asks “so what did you find?”: *We found the limits of this extract, and two residual signals that do not survive correction. That is the finding.*

---

## Part D — Novelty and expectation (slides 12–13, ~5 min)

Worthy of a Laidlaw signature **because it is an honest programme paper**, not because it discovers a new thermal effect.

What is new *for this extract* (do not call it a statistical theorem):

- a governed monthly first-event CHD/HF construction in a T2D/HTN cohort, with heat and cold carried together;
- a complete panel rather than a selected headline;
- an explicit grain → estimand map: monthly counts cannot support daily triggering claims, and we showed that with a failed calibration rather than by assertion.

Hogan’s line on aggregation-identifiability and calibrated refusal is a **contribution type** for the journal file. It is not Gate 3. It is not “we invented a method that proves heat.” Basagaña and Ballester already treat aggregated outcomes. Name the debt.

What would be fake novelty: promoting 1.022 or 1.073 to a confirmatory result; importing Roro’s excess deaths; talking as if stroke had arrived.

---

## Part E — Beyond Stage 3: Hogan (slides 14–16, ~8 min)

Slide 14 two documents; slide 15 comments; slide 16 still human.

Separate document: Hogan’s **live shared manuscript**. He writes weather Methods. Bob pastes; do not email a competing Word copy.

**Comments already answered in the paste pack (28 July threads):** running title; AMI/stroke not our endpoint; housing / behaviour / AC out; pollution is 2013–2023 EPD, not Goggins 2000–2009; Introduction closes in one sentence.

**Later writing/identification comments (24 August email, if you have it):** numbered Model 1 ⊂ 2 ⊂ 3 rather than “core panel”; Methods a reader can follow, no Results in Methods; add monthly humidity and rainfall (specified, **not fitted** on the governed panel — no invented coefficients); do not count temperature-variability days; count days versus leave-one-year-out same-calendar-day mean; one ethics sentence; keep editing the shared file. If Model 2/3 health fits are not on a governed machine, say **specified, not fitted**.

**Still human, not this signature:** paste into the live file; Hogan weather lock (HM23 reference period); Roro IRB number; authorship 2–4; Gate 3 freeze; stroke file.

One sentence to the room: *Hogan’s review improves the journal paper. It does not decide form 2a.*

---

## Part F — Why the signature, then ask (slide 17, ~3 min)

Form 2a is a programme endorsement of a sole-author ~2,000–3,000 word report. It is not journal acceptance.

The report:

- matches the direction you set (complete panel, every comparison, no confirmatory hunt);
- states the missing stroke file and the missing admission cause;
- does not overclaim (*q* > 0.19);
- exists as a PDF a programme reader can follow, with an A0 poster behind it.

Ask:

> I would be grateful if you would complete the supervisor block — rating, comments, signature — on the Laidlaw form. I have left those fields blank. Optional wording is on the one-pager if it saves time. The poster is 15 September and does not need a signature today.

Then stop talking.

If he wants to take it away: Friday 28 August. Report due 31 August.

---

## Do not say

- “We found that hot nights cause CHD” / “cold days cause HF.”
- AMI, principal-diagnosis CHD/HF, or a stroke result.
- Roro’s 1,455–3,238 excess deaths as this study.
- Daily DLNM triggering from monthly counts.
- Model 2/3 health coefficients if they have not been fitted.
- That Gate 3 is closed.
- An invented IRB number.

## If questions run long

Park weather lock, stroke, person-time, authorship, and Gate 3 **after** the form, or for a later slot. They are real. They are not the Laidlaw bar.
