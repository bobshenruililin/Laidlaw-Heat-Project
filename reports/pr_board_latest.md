# Open PR board — 2026-08-30

**Living science PR:** #82 (`origin/cursor/model23-gate3-b75b`).
**Rule:** do not merge. Close only `CLOSE_SUPERSEDED` rows with zero unique files versus the living tip.
**Gate 3:** remains open. Playbook: `analysis_plan/playbooks/07_pr_board.md`.

| PR | Draft | Mergeable | Action | Unique vs living tip | Note |
|---|---|---|---|---|---|
| [#82](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/82) Objective audit of physiology/HHAP; Model 2/3 plumbing; Gate 3 stays open | yes | MERGEABLE | `KEEP_LIVING_SCIENCE` | 0 | Living journal-track tip (audit cut, Model 2/3 plumbing, Cursor workflow). Update this PR; do not open a parallel science PR. |
| [#81](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/81) Physiology hypotheses and WHO–HK HHAP mapping in manuscript and Laidlaw report | no | MERGEABLE | `CLOSE_SUPERSEDED` | 0 | Long STORM insert; unique files vs living tip = 0. WORSE audit cut lives on #82. |
| [#80](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/80) Fukuda brief scoped to what this Laidlaw repo actually holds | no | MERGEABLE | `KEEP_UNIQUE` | 6 | Fukuda pitch pack. MERGEABLE. Not science-stack. Do not fold into #82. |
| [#79](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/79) Crown 6-df as robustness among 5, 6, and 8 | no | MERGEABLE | `CLOSE_SUPERSEDED` | 0 | Crown 6-df robustness; unique files vs living tip = 0. |
| [#78](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/78) Rebuild live Figure 3 so spline df cannot be read as heatwave duration | no | MERGEABLE | `CLOSE_SUPERSEDED` | 0 | Live Figure 3 rebuild; unique files vs living tip = 0. |
| [#77](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/77) Map Bishai Figure 3 comments: pre-COVID, spline df, 5-day rule, HHAP | no | MERGEABLE | `CLOSE_SUPERSEDED` | 0 | Bishai forest/HHAP mapping; unique files vs living tip = 0. |
| [#75](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/75) 27 August lab talk slides for the Bishai meeting | no | CONFLICTING | `KEEP_UNIQUE` | 7 | 27 Aug lab-talk slides. CONFLICTING. Event passed; unique HTML/notes remain on the branch. Port before close. |
| [#74](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/74) Thursday form 2a pack: Hogan is not the signer | no | CONFLICTING | `KEEP_UNIQUE` | 18 | Thursday form 2a print pack. CONFLICTING. Unique send_pack_2026-08-25. Supersedes the meeting overlay of #73 but does not contain #73's four unique files. |
| [#73](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/73) Bishai can sign form 2a without another Hogan review | no | CONFLICTING | `KEEP_UNIQUE` | 4 | Form 2a signature memo. CONFLICTING. Four unique files not in #74. Do not close as a duplicate of #74. |
| [#69](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/69) Hogan Methods: Model 1/2/3 Word manuscript and PDF | no | CONFLICTING | `CLOSE_SUPERSEDED` | 0 | Hogan Methods Word/PDF. Already merged via PR 71 (2026-08-27). Close as duplicate of merged work. |
| [#68](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/68) Add compounding scientific-search system (Playbook 06) | no | CONFLICTING | `KEEP_UNIQUE` | 22 | Playbook 06 scientific-search harness. CONFLICTING. Unique analysis_plan/scientific_search/. Do not reuse number 06 in this branch. |
| [#67](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/67) Name aggregation-identifiability and calibrated refusal as the contribution | yes | CONFLICTING | `KEEP_UNIQUE` | 3 | Aggregation-identifiability contribution. DRAFT + CONFLICTING. Three unique memos. |
| [#66](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/66) Email A: change form 2a research topic off AMI/stroke | yes | CONFLICTING | `KEEP_UNIQUE` | 1 | Email A form 2a topic off AMI/stroke. DRAFT + CONFLICTING. One unique knowledge file. |
| [#62](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/62) UK conference airfare: ask Horizons if the named CX itinerary is okay | yes | CONFLICTING | `KEEP_ADMIN` | 10 | UK conference airfare / Horizons. Not science. CONFLICTING. Unique reports/horizons_uk_conference_2026/. |
| [#61](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/61) Add Guo 2016 temperature variability to the climate panel | yes | CONFLICTING | `KEEP_DEAD_PENDING_HUMAN` | 10 | Guo 2016 TV climate panel. Hogan refused TV-day counts in the live weather Methods. Unique scripts/CSV remain. Do not merge until Hogan accepts; do not delete the climate work. |
| [#58](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/58) Record 18 Aug roundtable on the 15 Aug collab draft | yes | CONFLICTING | `KEEP_UNIQUE` | 5 | 18 Aug collab-draft roundtable. DRAFT + CONFLICTING. Unique knowledge + goal prompt. |
| [#53](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/53) Identification crucible: what the monthly panel can actually license | yes | CONFLICTING | `KEEP_UNIQUE` | 32 | Identification crucible. DRAFT + CONFLICTING. Unique outputs/identification_crucible/. Still the licensed-paragraph record. |
| [#46](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/46) Week 4–6 Laidlaw blogs and Week 6 compute menu | yes | CONFLICTING | `KEEP_UNIQUE` | 4 | Week 4–6 Laidlaw blogs. DRAFT + CONFLICTING. Unique reports/blog/week4–6. |

## Close-ready (zero unique files)

#81, #79, #78, #77, #69

## Keep open

#82, #80, #75, #74, #73, #68, #67, #66, #62, #61, #58, #53, #46

## Unique paths (close-ready should be empty)

### #81
None.

### #79
None.

### #78
None.

### #77
None.

### #69
None.

## Policy

Do not merge. Do not freeze Gate 3. Playbook 06 lives on PR #68; this branch uses Playbooks 07 and 08 so the numbers do not collide.

