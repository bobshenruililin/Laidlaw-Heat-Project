# Governed data request — DRAFT UNSENT

**2 October 2026.** Prepared for Bob's review; no request or collaborator message has been sent. These are proposed fields, not evidence of availability or access approval. The first task is a feasibility/schema response, not transfer of clinical records.

## Priority 1: definitions and smallest discriminating extension

Please assess whether the approved project scope can support:

- A non-sensitive event/eligibility specification or query-version attestation: T2D/HTN entry, CHD/HF codes and diagnosis setting, look-back, first-observed versus incident event, same-day rules, admission/ED/day-case inclusion, linkage, deduplication and coding changes.
- Outcome-specific monthly eligible population and person-time, including new entries and removal at first event/death/loss of observation; observable-history coverage. Confirm whether the cohort refreshes and whether later diagnoses determine earlier inclusion.
- Separately defined validated cardiovascular events, death ascertainment and care contacts (outpatient, primary care and ED/inpatient as available). Clarify recurrent versus first events, cause-specific versus all-cause events, suppression and missingness.

An aggregate-only extension can address denominator/recording questions but does not by itself identify physiology. If the source cannot validate an admission cause, preserve the present first-recorded construction and state the limitation.

## Priority 2: measurement needed to distinguish clinical and care pathways

Subject to scope, availability and governance, the analyst would use longitudinal HbA1c/glucose, blood pressure, lipid measures and creatinine/eGFR, with measurement dates, units, reference/assay changes, clinical setting, measurement indication where available and frequency. Include treatment histories and attendance/testing opportunity to evaluate changes in selected attenders. Blood pressure is a clinical measurement rather than a laboratory assay. Medication recording needs prescribing/dispensing and adherence limits distinguished.

BNP/NT-proBNP or troponin is optional and strongly indication-selected; it must not be treated as population surveillance. Infection/test records, vaccination dates and doses, and follow-up coverage would help distinguish viral exposure and pandemic phases. Infection testing is selective and changes over time; an unrecorded positive is not verified absence of infection. No specific laboratory or infection field is assumed to exist.

## What may enter this repository

A non-sensitive schema/field dictionary, semantic decision record, availability/missingness summaries authorised for export, approved estimates and disclosure-reviewed figure source data. No patient identifier, encounter-level row, precise patient date or laboratory record enters GitHub or an external research agent. A secure analyst can run versioned scripts locally and return a reviewed aggregate packet with source/query versions and a run manifest.

## Draft message for Bob to review

Subject: Feasibility check for interpreting the change in recorded cardiovascular hospitalisations

Dear Hogan and colleagues,

We have separated the recorded hospitalisation pattern from the claim that health improved. The current monthly CHD and HF counts cannot distinguish physiological change from care use or changes in the eligible population and recording process. Relevant Hong Kong studies already examine care continuity, cardiovascular outcomes and clinical measurements, so a stronger paper needs a specific additional test rather than simply a longer time series.

Could we first confirm the event-construction and cohort-eligibility specification, including first-event rules, look-back, entry and exit, death linkage, and inpatient versus other care settings? If within the approved scope, outcome-specific monthly eligible person-time and care-contact/death summaries would be the smallest useful extension.

Could you also advise whether a governed analyst could assess the availability of repeated HbA1c, blood pressure, lipids and renal measurements, with treatment and testing/attendance information? Infection and vaccination history would be helpful where available. A schema or feasibility response is sufficient initially; we are not requesting patient records by email or proposing that they be transferred to GitHub.

We would agree the question and analysis plan after verifying these definitions and before inspecting new associations. Analyses would remain in the approved environment, with only disclosure-reviewed outputs used in the manuscript.

Best wishes,
Bob

**Review before sending:** confirm recipients, appropriate scope/access process and whether a new request is appropriate. The scientific packet neither asserts availability nor grants transfer/dissemination permission.
