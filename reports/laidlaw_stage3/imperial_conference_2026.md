# Imperial conference + Horizons spreadsheet — action board

**Email:** Audrey Chung, Horizons Office, 14 August 2026 (not committed; gist in the knowledge note).  
**Conference:** European / Annual Laidlaw Scholars Conference, Imperial College London, **16–18 October 2026**.  
**Ingest:** [`knowledge/2026-08-14_audrey_imperial_conference.md`](../../knowledge/2026-08-14_audrey_imperial_conference.md).  
**Not sent.** Bob submits on LSN / the Google sheet / the conference form. Agents do not.

If one hour exists before 31 August, it is still **form 2a + locked essay**. The overdue spreadsheet is the only conference-adjacent task that should jump the queue, because it is late and short.

## Calendar (do not mix surfaces)

| When | What | Surface | Status in repo |
|---|---|---|---|
| Overdue 20 Jun | Spreadsheet **J–O** | Horizons Google sheet + LSN summary | Paste pack below. Bob maps to the actual headers. |
| Sun 23 Aug | Opening performance (Ambition) | Conference form | Default **skip**. |
| Sun 31 Aug | Essay + endorsed 2a + Network University-room post | `laidlaw@hku.hk` + LSN | Locked PDF ready. 2a and Network post are human. |
| Sun 6 Sep, midnight HKT | Panel abstract **and** Annual Laidlaw Scholars Conference 2026 Abstract Submission form | Conference form | Draft below. 6-minute oral + slides + Q&A. Research panel, not LiA. |
| Mon 15 Sep | Poster **file** | Horizons + LSN | Locked A0. Do not rebuild. |
| Thu 24 Sep | Taylor & Francis: upload poster PDF to LSN + consent | LSN | Optional. If selected: print **A1**, may miss one session. |
| Week of 5 Oct | Chi Wah showcase | HKU, A0 portrait | Locked A0 + logo overlay. |
| 16–18 Oct | Imperial | A1 portrait even for the walk-in showcase | Scale the locked PDF. Six HKU posters shortlisted for panels. |

LiA panel: **no.** LiA is a 2027 placement.

## 1. Spreadsheet columns J–O (overdue) — paste pack

Audrey: on the Laidlaw Scholars Network, provide a summary that includes research topic, objectives, and anticipated outcomes; complete columns J, K, L, M, N, O.

The sheet itself is not in this repo. Paste in **header order**. If the headers are not Topic / Objectives / Methods / Anticipated outcomes / LSN link / Notes, rearrange; do not invent a sixth scientific claim to fill a blank.

**Topic (likely J)**  
Heat, cold, and first hospitalisation after coronary heart disease or heart failure diagnosis in Hong Kong, 2013–2023.

**Objectives (likely K)**  
Estimate monthly associations between official thermal encodings (mean temperature, mean Tmax, mean Tmin, hot nights, very hot days, cold days) and first recorded CHD and HF hospitalisations among people with type 2 diabetes and/or hypertension. Hold heat and cold in one design. Report the full twelve-contrast panel rather than a single headline.

**Methods / approach (likely L)**  
Ecological territory-month time series, 132 months. Governed Hospital Authority aggregates (admission cause not recorded; stroke named and not attached). Hong Kong Observatory Headquarters exposures. Separate negative-binomial models with calendar-month indicators, a smooth function of time, and a days-in-month offset. Exploratory: the model set was specified after the outcome series were available.

**Anticipated outcomes (likely M)**  
A methods-honest account of what monthly first-event counts can and cannot settle. No protected confirmatory thermal claim is expected from twelve contrasts with multiplicity control. Complementary to daily mortality work in the same city, not a rescaling of it.

**LSN / Network (likely N)**  
Not yet posted. Draft: `reports/lsn/research_project_summary.md`. The URL Horizons reports to the Foundation is the HKU University-room post, not GitHub Pages. Leave this cell as “to be posted with the 31 August essay” until Bob actually posts.

**Notes / supervisor (likely O)**  
Supervisor: Professor David Bishai. Weather co-investigator: Hogan. Outcome co-investigator: Zhenyuan Liu. Do not list coefficients here.

## 2. Spreadsheet columns Q and R — research output (due with the files)

Audrey: complete Q and R. Essay 31 August; poster 15 September.

Until the files are on the Network, do not invent URLs.

**Q (essay)**  
`Laidlaw_Research_Report_2026.pdf` (SHA-256 prefix `6136e85a654502a0`). Network URL: blank until posted in the HKU University room.

**R (poster)**  
`Laidlaw_Stage3_A0_portrait.pdf` (SHA-256 prefix `4f7c1e408ae2d31f`). Network URL: blank until posted. Imperial print size is A1 (see below); the file Horizons wants on 15 September remains the locked A0.

## 3. LSN Network summary (same content, public register)

Use [`../lsn/research_project_summary.md`](../lsn/research_project_summary.md) after a voice/privacy pass. Do not post the 5 August stroke pack. Do not put CHD/HF coefficients on LSN. The conference abstract below is a different register (panel reviewers); the LSN post is for peers.

## 4. Conference panel — recommended, after 2a

Six HKU posters are shortlisted for panels. A 6-minute slot is the right length for this internship if the talk is identification plus an exploratory panel, not a heat-kills-CHD story.

**Decision Bob still owns:** submit / not submit. Default recommendation: **submit the research panel abstract** once Email A to Bishai is out. Skip the opening performance. Skip LiA. Taylor & Francis is optional after the poster is on LSN.

### Abstract (paste into the conference form)

**Title.** Measuring the thermometer: official hot nights, cold days, and first cardiac hospitalisations in Hong Kong, 2013–2023.

**Abstract (~220 words).**  
Hong Kong’s official “hot night” is a minimum temperature of 28 °C at the Observatory. This Laidlaw project asked what monthly counts of those nights, and of official cold days, can say about first hospitalisation after coronary heart disease (CHD) or heart failure (HF) diagnosis among people with type 2 diabetes and/or hypertension.

The governed file that arrived was not the stroke series named in the original plan. It is 132 territory-months (January 2013–December 2023) of first-event counts without recorded admission cause. Each thermal encoding entered a separate negative-binomial model with calendar-month indicators, a smooth function of time, and a days-in-month offset. All twelve core contrasts had Benjamini–Hochberg *q*-values above 0.19. No protected confirmatory claim is reported.

The result that travels is identification. After calendar-month indicators, June–September always had at least one official hot night; the remaining contrast is intensity (July 2013, 1 night; July 2022, 25). Official cold days fall almost entirely in December–February. Monthly mean temperature at Headquarters is corroborated by reanalysis; monthly 28 °C-night *counts* are not. The paper therefore stays on the Observatory garden, and the garden has been priced.

This is complementary to daily mortality work in the same city, not a rescaling of it. Stroke remains unattached. Better-denominated data are required before a thermal effect on cardiac hospitalisation in this cohort can be estimated.

**Keywords.** Hong Kong; hot nights; cold days; coronary heart disease; heart failure; monthly time series; exposure identification.

**Do not paste into the form:** 1.022 or 1.073 as a finding; daily Jaccard 0.031; 449 vs 17 vs 1,453; Gate 3; “AI-discovered”; a stroke coefficient; LiA language.

### Six-minute slide outline (one minute each)

1. **The file that arrived.** Named stroke; received CHD/HF first hospitalisation after first diagnosis; no admission cause; 132 months.
2. **The encodings.** Mean T / Tmax / Tmin vs official hot nights, very hot days, cold days. One city, two seasons.
3. **The panel, honestly.** Twelve contrasts; all *q* > 0.19; HF–cold more concordant; CHD–hot nights depend on the standard error. No headline.
4. **Figure 2.** Cold days live in December–February (141/145). The coefficient is between winters.
5. **Figure 4.** June–September always on; July 1 vs 25. A hot-night coefficient is summer intensity.
6. **The garden.** Means travel; the official flag does not. Stay on Headquarters. Credit Hogan, Roro, Bishai. Stop.

Slides can reuse `figures/live_identification/` Figures 2 and 4 (exposure only) and the locked poster’s forest only if disclosure is already cleared for Laidlaw. If unsure, use the heatmaps alone.

## 5. Taylor & Francis (optional)

Upload the **locked** poster PDF to LSN and tick consent by **24 September**. If selected: print **A1 portrait**, bring it, miss one other session. Do not rebuild the A0 file for commissioning editors. Do not add coefficients that the locked poster does not already carry.

## 6. What to print

| Event | Size | File | Rebuild? |
|---|---|---|---|
| Chi Wah, week of 5 Oct | **A0** portrait | Locked `Laidlaw_Stage3_A0_portrait.pdf` | **No.** Logos as overlay. |
| Imperial showcase and T&F | **A1** portrait | Same PDF, print-shop scale to 594 × 841 mm | **No.** Expect ~0.7× type. |

## 7. Human sequence (this week)

1. Open Audrey’s spreadsheet. Paste J–O from §1. Do not invent a Network URL.
2. Fill local 2a HUMAN blanks. Send Email A + locked essay to Bishai.
3. Voice/privacy pass on the LSN summary. Post essay to the University room by 31 August.
4. After Email A is out: submit the §4 abstract on the conference form by 6 September if you want a panel.
5. Poster file 15 September (locked A0). A1 print can wait until travel is booked.
