# Open questions log

**Purpose:** living list of questions that must remain visible until a person, governed file or primary source closes them.

**Last reviewed:** 23 July 2026.

Update a row by recording the decision, date and evidence link. Do not erase the old question or convert a working assumption into a fact without provenance.

## Weather and literature

| ID | Open question | Current state | Owner | What closes it |
|---|---|---|---|---|
| W01 | What are Jasmine’s exact MMT, moderate/extreme cutoffs, temperature/lag basis and attributable-risk procedure? | Paper identity, model family and headline AFs are locked; exact methods are unavailable in the workspace | Bob / source holder; consult Jingwen if needed | Full paper and supplement ingested and transcribed into a versioned source manifest |
| W02 | What changed between Roro’s revised manuscript and medRxiv v1? | `revised manuscript_clean.pdf` has not been ingested; v1 includes operator ambiguities | Roro / Bob | Versioned PDF comparison covering definitions, equations, tables and claims |
| W03 | What is the executable Li-HW / `HM23` rule? | Event family and Hogan’s count-to-tail adaptation are known; reference period, percentile/tie method, gaps, missingness and month mapping remain open | Hogan with Bob implementing | Hogan’s wording recorded on the Tuesday decision sheet and reflected in the registry |
| W04 | Which hot and cold definitions should enter Gate 3 as the proposed co-primary pair? | Core starters exist; no pair is locked | Hogan / Bishai / team | Written pair and rationale, selected before substantive coefficient interpretation |
| W05 | Should Roro’s four `HWD_*` definitions become four named monthly exposure siblings? | Proposed as siblings, not replacements; exact source operators still need the revised manuscript | Hogan for weather role; Roro for source truth | Written family role plus final executable source manifest |
| W06 | Which threshold reference period and percentile implementation should all relative definitions use? | Options include 2013–2019, full 2013–2023 or a defensible pre-study/external climatology | Hogan / team | One primary reference, percentile algorithm and tie rule frozen before outcomes |
| W07 | Is HKO Headquarters the primary exposure station, and what spatial sensitivity is feasible? | Headquarters is the working choice; multi-station sensitivity remains proposed | Hogan | Written station choice and any fixed sensitivity specification |
| W08 | Does Hogan still endorse the “evolutionary comparison” framing after Goggins? | It is the current intellectual prompt, not a settled claim | Hogan | Tuesday wording on whether to retain, revise or drop “evolutionary” |
| W09 | Should `CM05` remain in the first-wave panel? | Proposed as an any-day `Tmin ≤10°C` severe-cold sensitivity only | Hogan / Bishai | Written role; it must not be called a biological or genetic threshold |

## Outcome data and governance

| ID | Open question | Current state | Owner | What closes it |
|---|---|---|---|---|
| D01 | When and through what approved route will the HA stroke aggregates transfer? | Files are not in the workspace; no row counts may be assumed | Roro / PI / Bob | Governed receipt note with file hash, transfer authority and coverage |
| D02 | What exactly does a row/cell represent? | Month-only versus month × age × sex, outcome definition and subtype fields are unknown | Roro / Bob on receipt | Data dictionary plus schema/QC note |
| D03 | How is the true stroke event month recovered from the first GOPC marker? | Working rule says the first mention is a marker for an earlier event; field-level algorithm is not locked | Roro | Written executable timing rule tested on the delivered schema |
| D04 | Are ischaemic and haemorrhagic stroke separable? | Unknown; pooled stroke remains the near-term default | Roro / file inspection | Confirmed subtype field and coding, or written pooled-only decision |
| D05 | Can ages 65–69 and 70–74 be reported separately under disclosure controls? | HA can support stratification in principle; the delivered aggregate grain and suppression rules remain unknown | Roro | Schema and release rules confirm reportable cells |
| D06 | What do suppression and missing-value codes mean? | Unknown; suppressed values must never be treated as zero | Roro | Written code list and release rule |
| D07 | What ethics/governance determination applies to the current aggregate use? | PI decision remains open | Bishai | Written PI/governance determination and any required protocol update |
| D08 | What population universe matches the HA outcome denominator? | C&SD age–sex denominators are ready, but resident/eligibility alignment is unconfirmed | Roro / Bob | Outcome eligibility definition matched to a documented denominator construction |
| D09 | Is any valid AMI series available outside the general HA file? | General HA data lack reasons for admission; AMI is out of scope unless a separate series exists | Bishai / Roro | Separate governed AMI outcome definition and file, or explicit closure as out of scope |

## Analysis and reporting

| ID | Open question | Current state | Owner | What closes it |
|---|---|---|---|---|
| A01 | When does Gate 3 freeze, and exactly what does it freeze? | Tuesday should nominate the weather pair; the headline model still requires real-data QC/descriptives and team sign-off | Bishai / Hogan / team | Dated freeze note naming outcome, hot/cold pair, trend/seasonality, offsets and sensitivity roles |
| A02 | Which multi-method specifications remain in the reportable panel? | P01–P18 and HM/CM families are a structured catalogue, not independent discoveries | Team | Pre-specified panel/registry version and reporting plan frozen before substantive interpretation |
| A03 | How should the 11 missing CHP influenza months be handled? | Flu coverage is 121/132 months; `CM30` is a sensitivity | Bob / team | Frozen complete-case/imputation decision with a missingness audit; no silent zero fill |
| A04 | Should 2024 be added? | Optional extension; must not delay the 2013–2023 core | Roro / team | Availability and governance confirmed, then a written core-versus-extension decision |
| A05 | Can historical change be tested rather than discussed qualitatively? | Goggins used daily outcomes and different exposures/lags; direct coefficient comparison is currently invalid | Team | A genuinely harmonized design, otherwise retain qualitative comparison only |
| A06 | How will COVID-era care-seeking be handled? | Sensitivity phases exist; final role is not frozen | Team | Gate 3 sensitivity specification recorded before interpreting results |
| A07 | Are pollution, humidity and influenza confounders, mediators or effect modifiers in each pathway? | Staged models are proposed; causal roles differ and 132 months limit interactions | Team | Pathway-specific adjustment rationale and model ladder frozen in the SAP |
| A08 | What result, if any, would justify an adaptation discussion? | No stroke result exists; the design cannot identify genes or ancestry effects | Team | At most a carefully bounded discussion after real results, with non-genetic alternatives; no genetic inference from this study |

## Hard stop rules while questions remain open

- No invented HA schema, row counts, coefficients or subgroup availability.
- No source-faithful Jasmine reproduction before W01 closes.
- No final Roro operator before W02 closes.
- No primary-result language before D01–D08, outcome QC and A01 close.
- No selection of a weather definition because it later produces the largest or most significant association.
- Daily mortality AFs/RRs, modeled excess deaths and monthly stroke associations remain separate estimands.
