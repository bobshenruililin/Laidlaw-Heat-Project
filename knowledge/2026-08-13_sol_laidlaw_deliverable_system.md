# Laidlaw deliverable system after the live-paper handoff

**Date:** 13 August 2026
**Owner:** Bob Shen Ruililin
**Purpose:** Keep programme outputs, public communication, and the journal collaboration separate.

## Decision

Keep the Stage 3 report and A0 poster frozen.

The overnight live-document work does not make either programme PDF obsolete. It
clarifies their role: they are fixed Laidlaw submission artefacts, while Hogan's
shared file is the only journal manuscript. Later scientific wording belongs in
the live paper. Rebuilding a programme PDF would create two submission versions
without improving the collaborative manuscript.

Lift the freeze only if Bob authorises a replacement because Laidlaw requires a
format or factual correction, or because a material governance or safety issue
requires withdrawal. A replacement would need a new full-file hash and a new
written lock. The live-paper end-game alone is not a reason to lift it.

## What each artefact does

| Artefact | Function now | Authority and edit rule |
|---|---|---|
| Stage 3 research report | Fixed programme essay and submission record. It explains the project to a broad or academic Laidlaw audience. | Byte-locked at SHA-256 prefix `6136e85a654502a0`. Do not edit, rebuild, trim, or use it as the journal manuscript. |
| A0 portrait poster | Fixed programme poster for the Laidlaw submission and later display, including the November showcase. | Byte-locked at SHA-256 prefix `4f7c1e408ae2d31f`. Do not edit or rebuild it. Check the existing file at actual size; do not generate a replacement. |
| LSN research-project summary | Draft public introduction for cross-disciplinary Laidlaw Scholars Network peers, with an exposure-only interactive companion. | It is a dated paste pack, not a manuscript or submitted finding. Its 5 August stroke-and-waiting frame is now stale. Do not post it unchanged. Any revision should describe the current project without reporting health estimates and should replace the branch preview link with a stable public link when available. Bob makes the final voice, privacy, and posting decision. |
| Laidlaw website blogs | First-person accounts of process, revision, teamwork, and uncertainty. | Drafts only. They may explain how the research question changed, but must not convert plans, weather descriptives, or analysis work into health findings. Bob edits and publishes them. |
| Hogan live paper | Sole journal-track manuscript and shared record of co-author revisions. | Edit the shared file through `manuscript/live_collaborative/LIVE_DOC_EDITS.md`. Preserve Hogan's weather text. Roro owns expansion of health-data Methods. Do not circulate a parallel Word manuscript. |
| Repository `chd_hf_*` draft | Methods-heavy repository record and reproducibility surface for the CHD/HF analysis package. | It is not the live paper and should not be pasted wholesale into it. Edit it only for an explicit repository-methods or release task, then reconcile any proposed journal wording through the live-file workflow. Label divergence rather than implying that it controls the manuscript. |

## What remains owed

### Laidlaw programme

The repository does not prove that the administrative submission is complete.
The report and poster files are ready and locked; remaining actions are human:

1. obtain and complete the official HKU report form without inventing comments
   or signatures;
2. obtain Professor Bishai's endorsement and comments, and confirm authority to
   include the disclosure-minimised CHD/HF material;
3. submit the endorsed form and fixed report through the stated HKU route;
4. complete spreadsheet columns Q and R;
5. compare the existing poster with the official sample when accessible and
   inspect or print the locked file at actual size before the showcase.

The LSN summary and website blogs are communication drafts. The repository does
not establish that either is a mandatory Stage 3 submission. If Bob chooses or
is required to post them, he still owes the final voice, privacy, link, and
site-format pass.

### Hogan, Roro, and Bishai

Bob's immediate journal duty is to paste the end-game pack into Hogan's shared
file, answer the recorded comment threads, and make the agreed temperature-file
handoff without attaching a competing manuscript. He should preserve Hogan's
weather section and mark health-data text for Roro rather than filling unknown
ICD, timing, or inpatient semantics.

Bob also owes the team explicit requests and durable records for dissemination
authority, the PI's ethics/IRB determination, outcome semantics, authorship and
order, cohort risk-set decisions, and any further governed data request. The
underlying approvals and specialist text remain owned by the relevant people:
Hogan for weather, Roro for health-data construction and Methods, and Bishai
with the team for supervision, governance, and authorship decisions.

Professor Bishai's Laidlaw endorsement and the team's journal decisions are
related human checks, but they are not interchangeable. Programme endorsement
does not make the Stage 3 PDF the journal authority, and manuscript approval
does not complete the HKU form.

## Surface-selection rule for future agents

Use the audience and requested action, not the newest file date.

1. If the request concerns HKU submission, word limits, forms, or a programme
   showcase, use the locked Stage 3 artefacts and the administrative checklist.
   Record status around them; do not rebuild them.
2. If the request concerns journal prose, co-author comments, Results,
   Discussion, or Methods, work through the Hogan live-file paste workflow.
3. If the request concerns reproducibility, release tables, model
   documentation, or repository methods, use the `chd_hf_*` surface and state
   that it is not manuscript authority.
4. If the request concerns the peer-network project page, revise the LSN paste
   pack and exposure-only companion. Recheck its date, project framing, and
   public link before posting.
5. If the request concerns a reflective Laidlaw story, use the blog canon and
   leave a draft for Bob's creative and privacy pass.
6. If the request names more than one audience, split the outputs. Do not make
   one file serve programme administration, public reflection, and journal
   authorship.

When the target is unclear, stop before editing and ask which audience will
receive the artefact. Never resolve ambiguity by changing a locked PDF.

## Process improvement written with this memo

`reports/laidlaw_stage3/ARTEFACT_MAP.md` is the living routing index. It records
which surface is fixed, draft, live, or repository-only and gives a short
pre-edit checklist. Future agents should update the index when status or public
links change; they should not revise locked scientific content to reflect those
status changes.

## Scientific boundary

No stroke result is available. The LSN and blog surfaces must not imply one.
This memo adds no health estimate and does not promote a headline claim.
