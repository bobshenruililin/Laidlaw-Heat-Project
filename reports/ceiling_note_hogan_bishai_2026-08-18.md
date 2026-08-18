# What this intern can finish, and what only you can open

**A working note for Professor David Bishai and Hogan**
**From:** Shen Ruililin (Bob), Laidlaw intern, Bishai Lab
**Date:** 18 August 2026
**Use:** a file you can print. Not a paste into the live manuscript. Not an Outlook dump.
**Provenance:** the CHD/HF series is `HA_APPROVED_AGGREGATE`. Public-web checks are labelled below. I have not invented a stroke coefficient, a daily coefficient, or a person-time series.

---

## 1. Why I am writing this

I have taken the monthly panel as far as an intern can take it without pretending the file is something else. I am asking you to see that ceiling clearly, not to bless a larger claim.

The live paper is an identification article. It shows where a 132-month first-hospitalisation series gets its information, and where it does not. That is the honest peak of this extract. Further intern hours on the same file have diminishing returns. Raising the scientific ceiling requires objects I cannot obtain by searching harder: a stroke file, still-at-risk person-time, ICD and inpatient semantics, a written weather lock, and PI-level governance.

I checked whether I had simply failed to find a public substitute. I downloaded the files. They are the wrong grain. The routes that could change the grain exist, and they run through you.

---

## 2. What the monthly panel can support

Zhenyuan Liu (Roro) delivered territory-month counts of first recorded CHD and HF hospitalisation after first diagnosis, among people with type 2 diabetes and/or hypertension, January 2013–December 2023. Admission cause is absent. Stroke was named and not attached. I have not filled that gap.

On that file I can defend the following, and not more.

The estimand is an ecological monthly count ratio from separate negative-binomial models, with calendar-month indicators, a 4-df time spline, and a days-in-month offset. It is not cohort incidence. It is not a principal-diagnosis claim. It is not a daily triggering analysis. It is not an attributable mortality fraction.

The analysis of record is twelve contrasts: CHD and HF each against mean temperature, mean Tmax, mean Tmin, official hot nights, official cold days, and official very hot days. All twelve Benjamini–Hochberg *q*-values exceed 0.19. HF cold days are directionally stable across standard-error constructions but are not multiplicity-protected. CHD hot nights exclude 1 under Newey–West lag 6 (count ratio 1.022, 1.002–1.042) and do not exclude 1 before 2020 (1.011, 0.991–1.032). Nine of the twelve pre-2020 intervals with Newey–West lag 6 include 1. That sentence is a sensitivity, not a primary.

Official cold days in 2013–2023 total 145; 141 fall in December–February. After calendar-month indicators, remaining cold-day variation is between-year winter, not summer versus winter. First-event CHD counts fell from 23,830 in 2013 to 12,323 in 2023 while the interpolated Census population aged 35 or older rose about 17%. That decline is compatible with depletion of a 2013–2023 diagnosis window and with pandemic changes in care-seeking. Without monthly still-at-risk person-time I cannot apportion those two, and I cannot convert a count ratio into incidence.

Hogan’s weather paragraph is already the authority: meteorological data were obtained from the Hong Kong Observatory. Official flags (hot night Tmin ≥ 28°C; very hot day Tmax ≥ 33°C; cold day Tmin ≤ 12°C) are aggregated to months. I have not overwritten that paragraph.

Jingwen Liu et al. (2020) and Roro’s excess-mortality work answer different questions (daily mortality attributable fractions; modelled heatwave excess deaths). I have used them as family context. I have not transported their relative risks onto this CHD/HF series.

That is a complete, honest paper of a particular kind. It is not a confirmatory thermal discovery. I am not asking you to freeze a confirmatory primary on this extract.

---

## 3. Why this is the intern-owned peak

Three constraints coincide. None of them yields to diligence on my side.

**Information.** One hundred and thirty-two months, twelve predeclared contrasts, a declining first-event series, winter-concentrated cold days, and no admission cause. Residual CHD autocorrelation remains after the core specification. A clean-room attempt to recover daily effects from monthly outcomes against daily exposures failed a 500-replicate calibration. I therefore have no real daily coefficient to report. Re-fitting the same twelve contrasts with extra splines, extra encodings, or a different HAC lag cannot mint a protected primary. It can only move intervals around a *q* floor that already sits above 0.19.

**Governance.** I am not the principal investigator. I cannot sign an HA Undertaking, name a Hong Kong storage location, or commit the lab to destroy data within twelve months of study completion. The Hospital Authority’s own portal is explicit: the PI must be employed by a local university, government bureau, or section 88 charity; applications go to the Central Panel on Administrative Assessment of External Data Requests; charges recover staff time. Guo et al. (2024, *Lancet Reg. Health West. Pac.*) analysed daily emergency hospitalisations in Hong Kong and stated that those admission data were used under licence and are not publicly available. That is the same wall I am on, in print.

**File contract.** Roro’s extract is first hospitalisation after first CHD/HF diagnosis in a T2D/HTN cohort, without admission reason. Public DH and HA tables are episode discharges, usually annual or financial-year, in the whole hospital population. They cannot be recoded into our estimand by an intern with a spreadsheet.

I treated the third constraint as a hypothesis I might be wrong about. Section 5 is the test.

---

## 4. Diminishing returns, briefly

Once every defensible claim has a referee-citable object — table, figure, interval, refusal — extra intern hours are grooming.

Further encodings of the same 132 months, without a predeclared descriptive atlas and without a new data contract, are a hunt. Cover letters, highlight bullets, and journal-word-count trimming do not change identification. Rebuilding the Laidlaw Stage 3 PDF does not change identification. Inserting health-economics language does not change identification. Reconstructing hourly nighttime excess heat and dropping it into my processing paragraph would overwrite Hogan’s Methods and still would not create a daily first-event series.

I will keep the live file consistent, the supplement cited, and the claim ledger green. That is maintenance. It is not a new result.

---

## 5. What I actually opened (so this is not a shrug)

I wrote a script, `scripts/52_public_outcome_ceiling_search.py`, and fetched the public objects on 18 August 2026 (UTC). Machine log: `outputs/auto_research/public_outcome_ceiling_search.json`. Human table: `reports/public_data_ceiling_search_2026-08-18.md`. I did not stop at search snippets.

### 5.1 Hospital Authority open data — throughput, not diagnosis

`https://www.ha.org.hk/opendata/ipdpdd-en.json` returns 809 rows. Keys: Financial Year, Cluster, Hospital, IP / DP / IP+DP discharges and deaths. First row: Cheshire Home, Chung Hom Kok, 2008–09, 246 inpatient discharges and deaths. Seventeen financial years, 2008–09 through 2024–25. There is no month field. There is no ICD field.

The age–gender companion file is financial year × age band × sex. Still no ICD, no month, no T2D/HTN cohort, no first-event rule.

The DATA.GOV.HK specification for this family is beds, discharges, patient days, occupancy, and average length of stay. “Monthly/daily archives” on that portal are file-version history, not monthly disease counts.

HA Major Statistics lists “Number of Inpatient and Day Inpatient Discharges and Deaths in Hospitals under the Hospital Authority by Disease Group.” I guessed three JSON filenames under `ha.org.hk/opendata/`. Each returned HTTP 200 wrapping an HTML 404 page. CKAN search for “disease group hospital authority” returned **zero** packages.

### 5.2 Department of Health — one year, one chapter, episodes

I downloaded

`Inpatient Discharges and Deaths in All Hospitals Classified by Disease, 2023 (EN).csv`

from the DH DATA.GOV.HK series. Twenty-eight rows. Circulatory chapter I00–I99: **162,691** episode discharges and deaths, 7.20% of 2,266,303. The file’s own note: figures are on an **episode basis including day inpatients**. There is no month. There is no T2D/HTN restriction. There is no first-hospitalisation-after-first-diagnosis rule. This is not our series at a coarser grain. It is a different object.

CHP’s Heart Diseases page (updated 31 March 2026) reports **about 88,900** inpatient discharges and inpatient deaths with heart diseases as principal diagnosis in 2024, and 6,594 registered deaths. Annual. Territory. Principal diagnosis in that episode. Still not a monthly first-event T2D/HTN panel.

### 5.3 Census population and survey prevalence — not person-time

C&SD Table 110-01001 (population by sex and age group) updates **half-yearly**. I already use an interpolated 35+ series as an ecological sensitivity. It is not person-time among members of the HA T2D/HTN cohort who have not yet had a first CHD or HF hospitalisation.

The Health Behaviour Survey 2023 reports doctor-diagnosed hypertension with ongoing care in **21.3%** of persons aged 15 or above, and diabetes mellitus in **9.2%**. Population Health Survey 2020–22 gives related point prevalences, including 1.6% self-reported doctor-diagnosed coronary heart disease among persons aged 15 or above. A survey prevalence is a snapshot of a sampled population. It cannot be divided into 132 monthly still-at-risk counts for our cohort.

Published papers that do have those denominators use HA Clinical Management System extracts under collaboration. The Hong Kong Diabetes Surveillance Database is described in *IJE* (Wu et al., 2022) as a curated HA EMR resource, not a download. The BMJ Open GOPC protocol for HT/DM trajectories states that the HA statistics team extracts anonymised CMS data for the collaborating team. That is Roro’s world, not DATA.GOV.HK.

### 5.4 DATA.GOV.HK catalogue search

CKAN `package_search` for inpatient / hospitalisation / hospitalization returned **one** package: C&SD Table 930-92087, “Hospital Authority – inpatient services,” update frequency **quarterly**. Throughput, not ICD first-events.

### 5.5 Weather is not the missing object

I can download HKO daily mean temperature at Headquarters. For 2013 the public API returned 365 complete days; 1 January 2013 was 13.9°C. The live climate file is already built from that family of official series.

The HKO Open Data API’s `HHOT` datatype is hourly **astronomical tides**, not hourly air temperature. I confirmed that a naive hourly-temperature call fails. Guo et al. used hourly temperature to build hot-night excess. Substituting that metric into the live paper would be a weather rewrite, which is Hogan’s paragraph, and it would still leave the outcome monthly.

So: I am not blocked on temperature access. I am blocked on outcome grain, outcome semantics, and the right to request a different extract.

### 5.6 Papers that look like a shortcut are licensed extracts

Guo, Chan, Qiu, Wong, and Ho (2024): “The data of hospital admissions are available from Hong Kong Hospital Authority… restrictions apply to the availability of these data, which were used under license for the current study, and so are not publicly available.”

That sentence is the ceiling, written by a group that already had daily emergency admissions. I cannot recreate their outcome. I also cannot honestly treat their HNe finding as our CHD/HF result. Different outcome, different grain, different licence.

---

## 6. Official paths that exist, and that I cannot walk alone

I did not only search open data. I read the research-request rules.

### 6.1 HA Central Panel (off-site extract)

Portal: `https://www3.ha.org.hk/data/Provision/Index/`

- Applications: Central Panel on Administrative Assessment of External Data Requests.
- **Form A**, expedited aggregates, catalogue of IP / A&E / SOP / FMC / births. Charge **normally HK$15,000 or above**. Data often ready within two weeks of payment if no further clarification.
- **Form B**, customised aggregates or patient-based records. Charge **normally HK$60,000 or above**, varying with complexity.
- PI must be employed by a local university, government bureau, or section 88 organisation.
- Patient-based requests need ethics approval.
- HA cautions that a time series may be refused if completeness or comparability across years or institutions is in doubt.
- Cells with fewer than five underlying units are shown as `<5`.
- Form A inpatient dimensions include admission/discharge date, age, sex, district, specialty, admission via A&E, and **ICD-9-CM diagnosis group**. That could, in principle, yield monthly diagnosis-group episode counts for **all inpatients**. It would still not be first CHD/HF events among a T2D/HTN cohort unless Form B (or a custom specification) says so.
- Undertaking: data stored at a named physical location **in Hong Kong**, accessible only to named users, **permanently destroyed within 12 months** of study completion.

I can draft specifications. I cannot be the PI, pay the charge, or sign the Undertaking.

### 6.2 EHPDCL / HKU-EHPDCL (secure lab, not a public CSV)

The former HA Data Collaboration Lab now sits with EH Plus Digital. HKUMed hosts HKU-EHPDCL on Sassoon Road for HKU researchers and postgraduate students.

- **CRADLE:** sample of about 200,000 patients from 2007 and 2017. Free. **Output is not allowed.** Familiarisation only.
- **DARE:** >30 years of structured HA data, quarterly refresh, named-user licence, fee, institutional agreement, confidentiality undertaking. Aggregated exports require ethics and office review.
- **EXPERT:** customised datasets, including chronic-disease products; ethics; quotation.

Enquiry office: EHPDCL, 11/F Harbourside HQ, Kowloon Bay. This is a PI-and-faculty path. A Laidlaw intern cannot open DARE by filling a web form.

### 6.3 Code on Access to Information and Data Access Requests

An AccessInfo request already on the public record shows how HA answers: research extracts go through the Central Panel, not through ATI as a back door to patient-based files. Data Access Requests under the Personal Data (Privacy) Ordinance are for a living individual’s own records. Neither route is a monthly T2D/HTN first-event panel.

---

## 7. How to break the ceiling

I group these by what would actually change, then by who can open the door. Several of these are independent. None of them is a promise that a protected heat effect exists. They change the **question** the paper is allowed to ask.

### 7.1 A true still-at-risk denominator (changes the estimand)

If Roro can supply monthly counts of people in the T2D/HTN cohort who have not yet had a first CHD (or HF) hospitalisation, the offset can become person-time. The paper could then speak of rates, with the usual caveats. C&SD 35+ and survey prevalence cannot substitute. This is the single change that would stop me having to write “a count ratio remains a count ratio.”

### 7.2 ICD lists, inpatient versus DAE, and event timing (changes what the count *is*)

Roro still owns the health-data paragraph. I need, in his words: which ICD or ICPC codes define CHD and HF; whether the event is inpatient, day inpatient, or includes HA attendance that is not an admission; how “first recorded hospitalisation after first diagnosis” is dated; and how suppression works. Without that, referees will infer inpatient semantics I cannot defend. Form A’s ICD-9-CM dimension does not answer our cohort rule.

### 7.3 The stroke file (adds a morbidity layer, does not repair CHD/HF)

Stroke was named for this project and not delivered. I will not invent rows. If the file arrives, the first hour is hash, grain, dictionary, and suppression — not a coefficient. Subtype (ischaemic versus haemorrhage) is unknown until the file says so. A stroke series would sit beside CHD/HF. It would not convert the present twelve *q*-values into a primary.

### 7.4 Age 65–69 and 70–74 (visibility, if disclosure allows)

Hogan asked for those bands. The delivered CHD/HF file is territory-month. If Roro can release those strata under HA cell rules, we can show who carries the counts. We still would not have individual-level confounding control.

### 7.5 A daily outcome that actually calibrates (different paper)

Guo et al. needed licensed daily emergency admissions. Our clean-room monthly-outcome/daily-exposure recovery failed. The way to a daily DLNM is a new governed daily series, not another intern method. I would not start that analysis until a file passes the same QC bar we used for CHD/HF.

### 7.6 Admission cause / principal diagnosis (reopens AMI only if a new extract exists)

The 17 July meeting closed principal-diagnosis AMI from the general HA file. Only a separate extract with reasons for admission would reopen it. I will not rebuild the Week-1 AMI frame on the present file.

### 7.7 Weather lock (changes exposure definition, not outcome grain)

Hogan’s remaining decisions are written down in the readiness sheet: Li-HW / HM23 season; percentile reference period; ties; gap rule; missing-day tolerance; whether a heatwave that crosses months is assigned by start, touch, or burden; whether official monthly hot-night **counts** remain the live encoding given Guo’s HNe result; whether Roro’s four `HWD_*` definitions are named monthly siblings. I can implement whatever he writes. I must not fill the blanks from registry defaults.

### 7.8 A new HA extract or EHPDCL project (PI-owned)

If the lab wants monthly ICD-restricted counts, person-time, or daily emergency admissions, the honest routes are Form B (or a carefully specified Form A that we then admit is still not our cohort) and/or DARE/EXPERT. That needs Professor Bishai (or another eligible PI), ethics paper, protocol, charge, Hong Kong storage, and a destruction date. I can prepare the specification and the relevance paragraph. I cannot submit.

### 7.9 What would still not break the ceiling

A 133rd month does not exist in the delivered window. A Nature-scale venue does not follow from 132 ecological months and *q* > 0.19. Dual public manuscripts of the same paper do not add information. Monetising hospitalisations on synthetic prices does not belong in this article.

---

## 8. What each of you could provide

I am not packing these into one email. They are a meeting list. The same human hour still runs Hogan’s live file, then Roro, then Professor Bishai.

### Hogan

You already wrote the weather Methods. Please keep that paragraph.

What I cannot finish without you:

1. The HM23 / cold-tail reference period, percentile and tie rule, gap rule, missingness, and cross-month assignment, in your words.
2. Whether the live paper keeps official monthly hot-night counts, or whether you want a written intensity encoding. If the latter, it is your rewrite, not a silent substitution in my processing paragraph.
3. Endorsement (or correction) of the identification article in the live file, so Professor Bishai is not asked to bless a draft you have not accepted.

What I do not need from you: another temperature CSV. I can pull HKO daily myself. The lock is the definition, not the download.

### Roro

You already delivered the CHD/HF aggregates (6–7 August) and you own the health-data Methods. Dr Zhou’s first-diagnosis work should remain visible in that paragraph.

What would raise the ceiling:

1. The stroke aggregate, if it exists, with dictionary.
2. ICD / ICPC lists, inpatient versus DAE, and the executable first-event dating rule.
3. Monthly still-at-risk person-time for the T2D/HTN cohort, or a written statement that it cannot be constructed from this collaboration.
4. Age 65–69 and 70–74 cells, if disclosure allows.

I know your attention is split. A one-sentence “not available” is more useful than silence. I will not chase a file you do not have by scraping DH chapters.

### Professor Bishai

These are PI decisions. I can recommend; I cannot take them.

1. **Headline.** I recommend we do not freeze a confirmatory primary on this extract. The paper’s contribution is identification and honest refusal. That is still a paper. It is the paper this file can support.
2. **Dissemination.** Written authority to send the live article to a journal after Hogan has endorsed it. First venue that fits the identification article is *Environmental Research*, not a Lancet-family “added value” slot.
3. **Ethics / protocol.** Whether the current approved-aggregate use needs a protocol note or IRB action.
4. **Authorship and order.**
5. **Stroke wait.** Submit CHD/HF as identification now, or wait for a stroke file that may not arrive on a Laidlaw clock.
6. **New extract.** Whether you, as local PI, will open Form A/B or HKU-EHPDCL. The published charges start around HK$15,000 (expedited aggregates) and HK$60,000 (customised). Form A still will not, by catalogue, recreate our T2D/HTN first-event rule. Form B or DARE might. I will draft the specification if you want that door opened.
7. **Person-time ask.** A PI-level request to Roro for the still-at-risk denominator, if you judge it in-scope for the existing collaboration rather than a new HA charge.

I am not asking you to invent a thermal discovery for a funder. I am asking you to see that the intern-owned work has reached the reporting standard this extract deserves, and that the next scientific inch is a human door.

---

## 9. What I will keep doing

- Work in Hogan’s live file, not a parallel Word manuscript.
- Keep every claim tied to a table that already exists.
- QC any new governed file in the first hour (hash, grain, dictionary, suppression) before any model.
- Leave health-economics and daily coefficients out of this paper.
- Credit Hogan, Roro, Dr Zhou, Jingwen Liu, and you by role, in spare English.

I wanted to be wrong about the public-data wall. I downloaded the wall. The way through it is not another intern night. It is a sentence from Hogan, a file or a refusal from Roro, and a PI decision from you.

Shen Ruililin
18 August 2026
