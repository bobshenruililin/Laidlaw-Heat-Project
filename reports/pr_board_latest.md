# Open PR board — 2026-09-04

**Living science tip:** `origin/main` (PR #82 merged).
**Rule:** do not merge. Close only `CLOSE_SUPERSEDED` rows with zero unique files versus the living tip.
**Gate 3:** remains open. Playbook: `analysis_plan/playbooks/07_pr_board.md`.

| PR | Draft | Mergeable | Action | Unique vs living tip | Note |
|---|---|---|---|---|---|
| [#94](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/94) Add Playbook 06 scientific-search harness without live-manuscript hunks | no | MERGEABLE | `KEEP_UNIQUE` | 22 | CL train: Playbook 06 harness onto main. No live-manuscript hunks. Successor of #68 unique tree. |
| [#93](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/93) Add the Fukuda pitch pack scoped to what this repo holds | no | MERGEABLE | `KEEP_UNIQUE` | 6 | CL train: Fukuda pack onto main. Successor of #80 unique files. |
| [#92](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/92) Add the Laidlaw Conference 2026 abstract and Hogan 4 Sep briefing | no | MERGEABLE | `KEEP_UNIQUE` | 19 | CL train: Laidlaw Conference 2026 + Hogan 4 Sep briefing onto main. Successor of #86 unique packs. |
| [#91](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/91) Put HKU and Laidlaw logos on the Stage 3 navy header | no | MERGEABLE | `KEEP_UNIQUE` | 2 | CL train: Stage 3 poster logos onto main. Fresh port from #87; does not carry #84. |
| [#90](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/90) Add the 31 August Horizons Stage 3 send pack | no | MERGEABLE | `KEEP_UNIQUE` | 8 | CL train: Horizons 31 Aug send pack onto main. Successor of #83 unique files. |
| [#89](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/89) Record that Bishai signed form 2a against the 22 Aug foldback | no | MERGEABLE | `KEEP_UNIQUE` | 2 | CL train: form 2a signed memos onto main. Hash table of record. Successor of #84 unique files. |
| [#88](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/88) Point the Playbook 07 board at origin/main after PR 82 | no | MERGEABLE | `KEEP_UNIQUE` | 1 | CL train car 0: Playbook 07 board. Living tip origin/main. Does not merge unique science. |
| [#87](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/87) Add HKU and Laidlaw logos to the Stage 3 poster header | no | MERGEABLE | `KEEP_UNIQUE` | 4 | Stage 3 poster logos (HKU + Laidlaw). Port as its own CL vs main. Do not merge the caliber-review head. Navy lockups; equal width; centred. |
| [#86](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/86) Laidlaw Conference 2026 abstract, Hogan bullets, and 9-slide talk | yes | MERGEABLE | `KEEP_UNIQUE` | 20 | Laidlaw Conference 2026 abstract/talk. MERGEABLE. Port as its own CL. Not journal-track. |
| [#85](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/85) WHO 2026 × Hong Kong HHAP companion; restore live S9 | yes | MERGEABLE | `KEEP_REVIEW` | 13 | WHO 2026 × HK HHAP companion plus Hogan Word/PDF rebuild. Park the Hogan binaries and S9 live-file rewrite. Not in the Stage 3 CL train. |
| [#84](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/84) Record Bishai form 2a signature and Stage 3 caliber review | no | CONFLICTING | `KEEP_UNIQUE` | 2 | Bishai form 2a signed (31 Aug) + caliber review. CONFLICTING vs main. Port memos only; do not swap Stage 3 essay PDFs. |
| [#83](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/83) Horizons Stage 3 send pack (31 August) | no | CONFLICTING | `KEEP_UNIQUE` | 8 | Horizons Stage 3 send pack 31 Aug. Port send_pack_2026-08-31/ as its own CL. Keep dated 30 Aug pack on main. |
| [#80](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/80) Fukuda brief scoped to what this Laidlaw repo actually holds | no | CONFLICTING | `KEEP_UNIQUE` | 6 | Fukuda pitch pack. MERGEABLE. Port as its own CL. Not journal-track. |
| [#75](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/75) 27 August lab talk slides for the Bishai meeting | no | CONFLICTING | `KEEP_UNIQUE` | 7 | 27 Aug lab-talk slides. CONFLICTING. Event passed; unique HTML/notes remain. Park; not in this CL train. |
| [#74](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/74) Thursday form 2a pack: Hogan is not the signer | no | CONFLICTING | `KEEP_UNIQUE` | 18 | Thursday form 2a print pack. CONFLICTING. Unique send_pack_2026-08-25. Do not merge: regresses Stage 3 essay PDF. Park. |
| [#73](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/73) Bishai can sign form 2a without another Hogan review | no | CONFLICTING | `KEEP_UNIQUE` | 4 | Form 2a signature memo (pre-sign). CONFLICTING. Four unique files not in #74. Park; #84 is the signed record. |
| [#68](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/68) Add compounding scientific-search system (Playbook 06) | no | CONFLICTING | `KEEP_UNIQUE` | 22 | Playbook 06 scientific-search harness. CONFLICTING. Port harness only as a later CL; do not take live-manuscript hunks. Do not reuse number 06. |
| [#67](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/67) Name aggregation-identifiability and calibrated refusal as the contribution | yes | CONFLICTING | `KEEP_UNIQUE` | 3 | Aggregation-identifiability memos also live on #68. Close only after a Playbook 06 CL lands those files on main. |
| [#66](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/66) Email A: change form 2a research topic off AMI/stroke | yes | CONFLICTING | `KEEP_UNIQUE` | 1 | Email A form 2a topic off AMI/stroke. Worksheet topic already on main. Park the leftover knowledge file. |
| [#62](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/62) UK conference airfare: ask Horizons if the named CX itinerary is okay | yes | CONFLICTING | `KEEP_ADMIN` | 10 | UK conference airfare / Horizons. Not science. CONFLICTING. Park; not in this CL train. |
| [#61](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/61) Add Guo 2016 temperature variability to the climate panel | yes | CONFLICTING | `KEEP_DEAD_PENDING_HUMAN` | 10 | Guo 2016 TV climate panel. Hogan refused TV-day counts in the live weather Methods. Unique scripts/CSV remain. Do not merge until Hogan accepts; do not delete the climate work. |
| [#58](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/58) Record 18 Aug roundtable on the 15 Aug collab draft | yes | CONFLICTING | `KEEP_UNIQUE` | 5 | 18 Aug collab-draft roundtable. DRAFT + CONFLICTING. Park; craft already folded via merged #65. |
| [#53](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/53) Identification crucible: what the monthly panel can actually license | yes | CONFLICTING | `KEEP_UNIQUE` | 32 | Identification crucible. DRAFT + CONFLICTING. Explore record. Not in the Stage 3 CL train. Do not treat as findings. |
| [#46](https://github.com/bobshenruililin/Laidlaw-Heat-Project/pull/46) Week 4–6 Laidlaw blogs and Week 6 compute menu | yes | CONFLICTING | `KEEP_UNIQUE` | 4 | Week 4–6 Laidlaw blogs. DRAFT + CONFLICTING. Park; not journal-track. |

## Close-ready (zero unique files)

_None._

## Keep open

#94, #93, #92, #91, #90, #89, #88, #87, #86, #85, #84, #83, #80, #75, #74, #73, #68, #67, #66, #62, #61, #58, #53, #46

## Unique paths (close-ready should be empty)

## Policy

Do not merge. Do not freeze Gate 3. Playbook 06 unique tree is on #94; leave #68/#67 open until unique-vs-main is empty.

