# Post-meeting next steps — 17 July 2026 lab meeting

**Purpose:** Capture decisions and actions after the meeting so the project can move without relying on informal memory.  
**Status:** Filled from meeting debrief (17 Jul 2026). Full narrative: `reports/meeting_debrief_2026-07-17.md`.  
**Data status:** Outcome / aggregate files **not yet received** (user will send next).

---

## 1. Decisions made (from meeting feedback)

| Topic | Decision | Source | Notes |
|---|---|---|---|
| General HA admission reasons | **Not available** for this extract — reasons for admission not specified | Meeting 17 Jul | Demotes general-file AMI / principal-dx CVD endpoints |
| Stroke outcomes | **Stroke admission data exist**; analysis will use **aggregates** | Meeting 17 Jul | Primary near-term outcome family |
| Exposure resolution for analysis | **Monthly temperature** (and monthly summaries from daily HKO) | Meeting 17 Jul | Do not claim daily admissions DLNM |
| Analytic strategy | Explore **~10 different methods** for insight breadth | Meeting 17 Jul | Multi-specification panel; see debrief §4 |
| Heatwave definitions | Align with **Chao Ren**–team defined heatwaves (Wang/Ren EHWE tradition) and lab multi-definition practice | Meeting 17 Jul (“Chao Ran”) | Use spell / 2D3N / official extremes already in climate file |
| Lab daily-scale context | Prof. Bishai / collaborators have **daily-scale heatwave work through 2023** (mortality / multi-definition) | Meeting 17 Jul | Complementary to this monthly stroke-aggregate project; not a substitute |

---

## 2. Decisions still open (await data / PI)

| Topic | Why still open | Blocker | Owner | Target |
|---|---|---|---|---|
| Exact stroke aggregate grain | Files not yet received | Incoming data + dictionary | Bob / Roro | On data arrival |
| IS vs HS split in stroke file | Unknown until schema seen | Stroke extract codebook | Roro / Bob | On data arrival |
| AMI series availability | General HA lacks reasons; separate AMI file not confirmed | Confirmation | Roro / Bishai | After data review |
| Medication / BMI for aggregates | Aggregates often lack patient covariates | Schema | Roro | On data arrival |
| IRB / governance for stroke aggregate use | PI determination | Meeting follow-up | **Bishai** | ASAP |
| Small-cell suppression | Needed before releasing tables | HPC / HA policy | Roro | Before shared tables |
| Headline method among ~10 | Freeze after QC | Gate 3 | Bishai / Bob | After descriptives |
| Full meaning of DAE (if still relevant) | May be less central if working only from stroke aggregates | Dictionary | Roro | If patient-level still used |

---

## 3. Action register

| Action | Owner | Deadline | Depends on | Done? |
|---|---|---|---|---|
| Receive and securely store stroke / HA aggregate files | Bob | When sent | User transfer | |
| QC aggregates; write short data receipt note | Bob | Immediately after receipt | Files | |
| Merge aggregates to monthly HKO climate + denominators (if strata match) | Bob | After QC | Files + climate | |
| Adapt merge / descriptive scripts for aggregate stroke (not diagnosis panel) | Bob | After schema known | Files | |
| Run multi-method ladder M1–M10 (labelled; no over-claim) | Bob | After Gate 2 | Merge ready | |
| Extend weather build to December 2012 (lag-1 Jan 2013) | Bob | Near-term | — | |
| Update assumption ledger + decision gates from meeting | Bob | This commit | Meeting notes | Yes (this update) |
| Wet-ink / HPC onboarding if patient-level still needed beyond aggregates | Bob, Hogan, Roro | Parallel | Signatures | |
| IRB determination for current use | Bishai | ASAP | Governance note | |

---

## 4. What can proceed before / without full HPC patient-level access

- Ingest and analyse **stroke aggregates** once files are sent (if they arrive outside HPC, follow whatever transfer/governance rule the PI sets).
- Keep HKO monthly climate, extremes, spell / 2D3N metrics ready.
- Build Table 1 environment panel (already largely done).
- Draft blank outcome Table 1 / rate figures for stroke aggregates.
- Do **not** invent AMI or subtype results from general admissions lacking reasons.

---

## 5. Branching paths after data arrival

### If stroke aggregates are territory-month only

- Monthly time-series / count models with population offset (or crude counts with care).
- Multi-method exposure panel still applies; age interactions limited.

### If stroke aggregates are month × age (± sex)

- Prefer rate models with C&SD person-time aligned to bands.
- Prioritise older-age contrasts if 65–69 / 70–74 present.

### If stroke file includes subtype codes

- Reinstate separate IS / HS models as primary within the stroke family.
- Still do not invent AMI from the general “no reason” HA file.

### If only undifferentiated hospital aggregates arrive (no stroke)

- Stop endpoint claims; request stroke series clarification before modelling associations.

---

## 6. First deliverables after data arrive

1. Data receipt + QC note.  
2. Merged monthly panel (climate + stroke aggregates).  
3. Descriptive figures (stroke over time vs temperature / extremes).  
4. Multi-method association table (M1–M10), clearly labelled.  
5. Short methods note stating what was **not** possible (no general admission reasons; monthly not daily).

---

## Related documents

- `reports/meeting_debrief_2026-07-17.md` — full recalibration narrative  
- `analysis_plan/assumption_ledger.md`  
- `analysis_plan/decision_gates.md`
