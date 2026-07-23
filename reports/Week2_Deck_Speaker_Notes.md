# Week 2 Progress — Speaker Notes

### Slide 1 — Week 2 Progress
- **Say (keypoints):**
  - Welcome the Bishai Lab; let the identity slide breathe.
  - Introduce yourself simply: Bob, Laidlaw Scholar, Bishai Lab.
  - Frame this as a team progress update, not a results announcement.
- **On-slide jargon:** Laidlaw Scholars Programme → the research and leadership programme supporting this project.

### Slide 2 — This is a team project
- **Say (keypoints):**
  - Credit Hogan for weather framing, the Goggins challenge, age bands, and hot-month idea.
  - Credit Roro for stroke timing and aggregates; Dr Bishai for the multi-method plan, teamwork, and Jasmine question.
  - Acknowledge room-wide lessons: write early, consider equity, and connect to Hong Kong’s heat work.
- **On-slide jargon:** HA → Hong Kong’s Hospital Authority; stroke aggregates → grouped monthly counts, not patient records; Goggins baseline challenge → earlier Hong Kong studies found cold–cardiovascular links, so this is a later-period comparison, not a first discovery; Marmot equity → who bears risk and has least capacity to adapt.

### Slide 3 — What the July meeting changed
- **Say (keypoints):**
  - Without admission reasons, the general HA file cannot support principal-diagnosis AMI; the outcome becomes stroke aggregates.
  - We moved to a panel: Ren/Wang-style spells, 2D3N, and hot-month options aligned with Hogan.
  - For Roro, first GOPC mention marks an earlier stroke and hospitalisation; recover the true event month and ignore later mentions.
- **On-slide jargon:** AMI → acute myocardial infarction, or heart attack; GOPC marker → a General Out-patient Clinic stroke mention that points to an earlier event but is not the event date; spell → consecutive days or nights meeting a rule; 2D3N → two very hot days combined with three hot nights.

### Slide 4 — The question we are preparing
- **Say (keypoints):**
  - Are monthly thermal exposures during 2013–2023 associated with monthly stroke-event counts?
  - Is the picture stable across continuous temperature, official extremes, spells, cold, and sensitivities?
  - “Associate” is deliberate: this design cannot prove causation and complements daily heatwave–mortality work.
- **On-slide jargon:** daily DLNM → a distributed lag non-linear model using daily outcomes to estimate curved temperature risk and delayed effects; monthly stroke aggregates cannot recover that acute day-by-day pattern.

### Slide 5 — From January: Hogan’s intellectual lead
- **Say (keypoints):**
  - Hogan brought the Goggins stroke and AMI papers in as the historical Hong Kong baseline.
  - Cold effects are documented; ask how a later period compares without declaring a regime shift.
  - He highlighted ages 65–69 and 70–74, if Roro’s aggregate grain supports them.
  - His later proposal: define heatwaves, count monthly starts, and flag upper-tail months; lock the Atmospheric Research choices with him.
- **On-slide jargon:** upper-tail hot month → unusually many events against a pre-fixed reference; DOI → publication identifier, here `10.1016/j.atmosres.2024.107845`.

### Slide 6 — Climate: shared ground truth (descriptive)
- **Say (keypoints):**
  - Hot nights and very hot days are generally higher after 2018, with yearly variation.
  - Hot nights peak in 2021 at 61, and very hot days are elevated in 2020–2023.
  - Cold days fluctuate and persist through 2023; none of these lines is a stroke finding.
- **On-slide jargon:** HKO official extremes → Hong Kong Observatory thresholds: a hot night has minimum temperature at least 28°C, a very hot day has maximum temperature at least 33°C, and a cold day has minimum temperature at most 12°C.

### Slide 7 — Pollution layer (EPD EPIC)
- **Say (keypoints):**
  - These are annual averages from official monthly general-station data.
  - Say the visible trend plainly: NO₂, PM₂.₅, and PM₁₀ decline substantially across 2013–2023, while ozone rises overall despite year-to-year variation.
  - The changing mix justifies staged adjustment, with ozone last because it can track hot, sunny conditions; it proves no stroke effect.
- **On-slide jargon:** EPD EPIC → the Environmental Protection Department’s public air-quality data platform; NO₂, PM₂.₅, PM₁₀, O₃ → nitrogen dioxide, fine particles, larger inhalable particles, and ozone.

### Slide 8 — Why heatwave definitions stay plural
- **Say (keypoints):**
  - Definitions select different shares of 132 months: p90/p95/p97.5 flag 14/7/5; VHD-spell and 2D3N flag 39/38.
  - p90/p95/p97.5 means the monthly mean reaches the 90th/95th/97.5th percentile—roughly the hottest 10%/5%/2.5% under a frozen reference. VHD spell ≥3 touches three consecutive very hot days; 2D3N combines days and nights.
  - Plural rules measure level, rarity, persistence, and day–night stress—not whichever answer looks favourable.
- **On-slide jargon:** Ren/Wang-style spells → published Hong Kong rules for consecutive hot days, nights, or both; hot-month options → pre-labelled monthly translations of daily heat.

### Slide 9 — A labelled panel — not seventeen discoveries
- **Say (keypoints):**
  - Named families stop every coefficient or small p-value becoming a separate discovery.
  - Gate 3 proposes P02, same-month maximum/minimum temperature, plus P04, official extreme counts; the team must freeze these.
  - Yang/Chong motivates cold–flu co-exposure: without CHP surveillance, a flu-heavy winter could look like pure cold.
- **On-slide jargon:** Gate 3 → the decision locking the primary model; CHP flu → Centre for Health Protection influenza surveillance for overlapping cold and flu.

### Slide 10 — What each person still unlocks
- **Say (keypoints):**
  - Public climate, population, pollution, most influenza data, and dry-run code are ready.
  - Hogan unlocks final weather, heatwave, hot-month, and cold-month operational definitions.
  - Roro unlocks the real stroke aggregates, dictionary, transfer path, and true event-month construction.
  - Dr Bishai unlocks Jasmine’s identity and table; the graphic shows dependencies, not performance.
- **On-slide jargon:** synthetic dry-run → invented test data used only to check that code joins and models run; synthetic ≠ findings because those numbers contain no real stroke evidence.

### Slide 11 — Honesty line
- **Say (keypoints):**
  - Ready: environmental descriptives, outcome logic for confirmation, exposure review, and early writing.
  - Not ready: stroke coefficients, a claim that heat has replaced cold, or AMI findings from a file without admission reasons.
  - Environmental trends are context; inference waits for stroke aggregates, locked definitions, and quality checks.
- **On-slide jargon:** coefficient → a model’s numerical estimate of an association; it is not available for stroke yet.

### Slide 12 — Literature anchors (selected)
- **Say (keypoints):**
  - Goggins supplies earlier cold-dominant stroke/AMI context and the comparability challenge.
  - Guo/Gasparrini supports multiple heatwave definitions; Wang/Ren supplies VHD, hot-night, spell, and 2D3N structures.
  - Yang/Chong motivates cold–influenza analysis; later Guo work motivates staged pollution.
  - These papers anchor methods, not stroke results.
- **On-slide jargon:** literature anchor → a prior study that justifies a definition or analysis choice, not proof that the same result holds in our data.

### Slide 13 — A signal from Dr Bishai — still to verify
- **Say (keypoints):**
  - Dr Bishai recalls more non-significant p-values for heat and fewer for cold in “Jasmine’s paper.”
  - Treat that memory as a research prompt, not a citable finding or stroke result.
  - Identify the source, definitions, models, and complete test set; compare estimates and intervals first, with null-counting secondary.
- **On-slide jargon:** Jasmine → an unresolved paper/person/project label; null p-value → usually p ≥ 0.05, meaning a significance threshold was not met, not that effect is zero.

### Slide 14 — First: identify “Jasmine’s paper”
- **Say (keypoints):**
  - Wang/Ren 2019 covers Hong Kong 5VHD, 5HN, and 2D3N events, but remains unconfirmed.
  - The meeting-note Liu 2020 lead is unverified; Sida Liu’s verified Hong Kong mortality paper is nearby evidence, not assumed to be Jasmine’s.
  - Ask Dr Bishai for a PDF, DOI, citation, or screenshot and exact figure or table.
- **On-slide jargon:** unconfirmed lead → a plausible source that must not be cited as the intended paper until its identity is verified.

### Slide 15 — Definition-harmonised extension to 2023
- **Say (keypoints):**
  - Transcribe the source outcome, time unit, thresholds, reference, lag, and model.
  - Validate the exposure coding in overlapping years, then carry the unchanged definitions through December 2023.
  - Join monthly exposure measures only to Roro’s true stroke-event month.
  - If the source used daily mortality, this monthly stroke work is definition transport, not exact replication; report uncertainty and never select by significance.
- **On-slide jargon:** definition-harmonised extension → preserving an earlier exposure rule in a later period while acknowledging that another outcome or time scale changes the question.

### Slide 16 — Next week: spin out hot and cold months
- **Say (keypoints):**
  - Build symmetric hot/cold families before inspecting stroke associations.
  - Hot and cold families cover official counts, percentile tails, spells, event counts, intensity, anomalies, warnings, and compound exposure.
  - The 50 hot and 48 cold definitions are a catalogue of choices organised into families, not 98 independent claims.
- **On-slide jargon:** degree-day intensity → the accumulated amount by which daily temperature exceeds a hot threshold or falls below a cold threshold.

### Slide 17 — Starter set — small enough to run first
- **Say (keypoints):**
  - Start with Hogan’s event-count tail, a simple p90 monthly-mean rule, 5-VHD and 5-hot-night spells, and 2D3N.
  - Cold starters: five days at or below 12°C, lower-5% monthly mean, and three-day spell.
  - Add night-heat intensity, hot plus ozone, any day at or below 10°C, and cold plus CHP flu; Yang/Chong warns that a flu-heavy winter is not a pure cold effect.
- **On-slide jargon:** starter set → a small, pre-labelled first batch chosen for interpretability and coverage before wider sensitivity analyses.

### Slide 18 — Hogan’s atmospheric recipe is one family
- **Say (keypoints):**
  - Li et al. define May–September heatwaves as at least three consecutive days above a calendar-day p90 maximum-temperature threshold, using a moving 15-day window.
  - Hogan’s adaptation: identify events, count monthly starts, then flag pre-fixed upper-tail counts.
  - Freeze reference years, percentile method, gap rule, cross-month assignment, and monthly tail before outcomes; keep this credited family beside other definitions.
- **On-slide jargon:** calendar-day p90 → an unusually high temperature for that time of year, rather than one fixed threshold for every date.

### Slide 19 — Hypothesis, not mechanism
- **Say (keypoints):**
  - South China populations may appear heat-adapted while temperatures near 10°C remain consequential.
  - Our monthly ecological study cannot identify genes, ancestry effects, or a causal adaptation mechanism.
  - Housing, air conditioning, behaviour, occupation, age, health care, and acclimatisation are alternatives; 10°C is a candidate cutoff, not a biological threshold or stroke finding.
- **On-slide jargon:** mechanism → the causal process producing an association; this study may describe patterns but cannot establish a genetic or biological pathway.

### Slide 20 — Laidlaw Stage 3 is on the horizon
- **Say (keypoints):**
  - Stage 3 requires a 2,000–3,000-word essay, A0 portrait poster, and endorsed HKU report.
  - Early literature and methods writing exposes assumptions and missing decisions.
  - Until outcomes arrive, poster results remain environmental and process-focused; November is a horizon, not a reason to overstate readiness.
- **On-slide jargon:** A0 portrait → a large vertical poster measuring 841 × 1189 mm.

### Slide 21 — Thank you
- **Say (keypoints):**
  - Thank the lab and make three concrete asks.
  - Dr Bishai: please identify Jasmine’s paper and the exact hotter-null/colder-signal table.
  - Hogan: please lock the heatwave, hot-month, and cold-month rules together, including the count-to-upper-tail idea.
  - Roro: confirm GOPC-to-true-stroke timing, dictionary, and transfer path.
  - End team-first: going far means going together—and keep the “:)”.
- **On-slide jargon:** count-to-upper-tail → count heatwave starts by month, then label only unusually high-count months using a threshold fixed in advance.
