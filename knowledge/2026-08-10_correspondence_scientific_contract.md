# Correspondence-grounded scientific contract — Laidlaw thermal-health project

**Source:** Nine-page Outlook thread supplied by Bob on 10 August 2026.  
**Coverage:** 21 April–6 August 2026.  
**Privacy:** This note omits email addresses, phone numbers, student identifiers,
and routine meeting logistics. The source PDF is not committed.

## What the correspondence establishes

### 10–12 July: initial analysis request

Bob reported a validated HKO pipeline and explicitly stated that synthetic
health outcomes had only tested the code. He asked for the diagnosis coding
system, principal-diagnosis availability, episode rules, age bands,
suppression rules, and secure output-vetting arrangements.

Professor Bishai then proposed merging monthly maximum, minimum, and lagged
temperature with monthly AMI and stroke admission risk. He requested a Table 1
containing sample sizes, means, and standard deviations for temperature and
available covariates. His desired patient-level adjustment list included age,
sex, diuretics, beta blockers, metformin, SGLT2 inhibitors, and BMI.

Roro confirmed:

- ICD-9 coding and inclusion of DAE records;
- complete admission outcomes at patient level;
- no ED-to-inpatient episodes in that extract;
- the ability to distinguish ages 65–69 and 70–74; and
- a controlled HPC access process requiring wet-ink signatures.

Roro also asked whether the additional HA work required an IRB protocol
update. No PI answer to that question appears in the supplied thread.

### 17–22 July: monthly outcome and exposure-definition pivot

The project moved away from principal-diagnosis AMI claims when the general HA
file was found not to contain admission causes. Bob's correspondence to Hogan
described the revised near-term focus as monthly stroke aggregates.

Roro relayed a contribution plan for monthly stroke and MI hospitalisations
under several heatwave scenarios. The plan mentioned a distributed-lag
non-linear model but immediately noted that an exposure in the previous month
was not biologically compelling when the anticipated heat effect window was
5–21 days. The binding interpretation is therefore:

- retain daily weather morphology inside each monthly exposure;
- do not describe an ordinary monthly lag model as a daily DLNM; and
- treat lag-one-month temperature as a labelled sensitivity, not a recovered
  daily lag curve.

The proposed exposure families were:

1. upper-tail monthly mean temperature;
2. prolonged hot-day events;
3. prolonged hot-night events;
4. humidity-augmented versions; and
5. a hot month containing at least one heatwave day.

Hogan proposed a distinct atmospheric construction:

1. source-lock a heatwave definition;
2. count heatwave events in each month over a long HKO record; and
3. define a hot month by the upper tail of that count distribution, with an
   absolute event-count threshold as an alternative.

These were proposals, not a completed weather lock.

### 22–28 July: team roles and live manuscript

Bob apologised to Hogan for building the HKO files without consultation and
asked him to remain a co-author and guide environmental methods. Hogan offered
to guide both weather methods and academic writing, specifically asking for
less flowery and more digestible prose. Roro agreed to that arrangement and
retained responsibility for regression oversight and outcome construction.

After meeting Bob, Hogan:

- created and shared a live manuscript;
- commented on the Introduction;
- wrote the weather component of Methods;
- asked Bob to complete the remaining Methods; and
- asked Roro to provide cleaned monthly stroke data and the health-data
  Methods.

The live file remains the collaborative manuscript authority. Repository
writing must not overwrite Hogan's weather text.

### 6 August: governed CHD/HF delivery

Roro's covering correspondence stated that the HA patient-level source was
limited to people diagnosed with T2D and/or HTN during 2013–2023. Because
admission cause was absent, the team defined the relevant event as the first
hospitalisation after the patient's first diagnosis record for the
cardiovascular condition. Dr Jingjing Zhou assisted in constructing
first-diagnosis records.

The correspondence said that CHD, HF, and stroke counts were included, but
only two attachments were present:

- coronary heart disease; and
- heart failure.

Stroke was not delivered and cannot be analysed or described as a result.
Roro asked Bob to share the completed temperature panel.

### 12 August: Hogan’s two asks

Hogan thanked Roro and asked Bob, by 12 August, where Methods writing stood, and whether Bob would send Roro the temperature panel or Hogan should send it. That is the round to answer. A later programme-report note to Professor Bishai is a different message.

Working culture of the thread: [`correspondence_working_culture.md`](correspondence_working_culture.md). Message ledger: [`correspondence_ledger.yml`](correspondence_ledger.yml).

## Binding scientific rules

1. Current CHD/HF outcomes are first hospitalisations after first diagnosis
   records among a T2D/HTN cohort.
2. Admission cause is not observed. Do not claim principal-diagnosis CHD, HF,
   AMI, or stroke admissions.
3. Current files are territory-month aggregates. The correspondence's
   patient-level covariate ambition is not supported by those files.
4. Age/sex capability does not imply age/sex fields were delivered.
5. Daily HKO data may define monthly exposure morphology. Monthly health data
   do not automatically identify daily lag-specific effects.
6. Stroke remains blocked.
7. Synthetic outcomes are plumbing or calibration only.
8. HA extracts and unvetted outputs stay inside approved governance.

## Human-owned decisions

- Whether the IRB protocol needs amendment.
- Exact CHD/HF ICD lists and the meaning of `*_inpatient`.
- Whether to obtain the T2D/HTN cohort still at risk of a first event.
- Which Hogan/Roro heatwave construction is primary.
- Whether lag-one-month temperature stays in the reported panel.
- Stroke delivery and role.
- Author order and the proposed Bob/Roro co-first designation.
- External dissemination of aggregate results.

## Contribution record

- **Professor David Bishai:** supervision, initial model/Table 1 direction,
  multi-method concept, PI/governance decisions.
- **Hogan:** weather definitions, atmospheric heatwave adaptation, live weather
  Methods, academic-writing mentorship.
- **Zhenyuan Liu (Roro):** governed HA outcome construction and delivery,
  regression mentorship, health-data Methods.
- **Dr Jingjing Zhou:** first-diagnosis record construction.
- **Bob Shen Ruililin:** HKO/exposure pipeline, integration, statistical
  implementation, and writing.

These descriptions record work and proposals. They do not establish final
author order, co-first status, Gate 3 approval, or publication permission.
