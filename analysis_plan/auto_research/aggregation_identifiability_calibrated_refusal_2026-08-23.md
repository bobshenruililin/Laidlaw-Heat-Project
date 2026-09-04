# Aggregation-identifiability and calibrated refusal

**Date:** 23 August 2026. **Mode:** Ship (Playbook 05). **Not a Gate 3 freeze. Not a new estimator.**

Hogan’s line, reported by Bob, on the Stage 3 draft: make the aggregation-identifiability and calibrated-refusal framework the original methodological contribution. This memo names that framework, maps it onto displays that already exist, and bounds originality. It does not rewrite programme Stage 3 PDFs (the 22 August lock on `main` remains the programme pair). Journal-track wording lives in the live collaborative file; paste remains a human step.

## Originality bound

This is an **operational framework for this extract**, not a statistical theorem.

Basagaña and Ballester already showed that temporally aggregated outcomes can be combined with disaggregated exposures under a derived likelihood, and that monthly recovery is not automatic ([15], [16] in the live file; `literature/final_methods_evidence_map.md`). Greenland and Morgenstern already warn that ecological monthly series do not identify individual-level effects. This project does **not** claim priority for the idea that monthly totals cannot recover daily lags.

What is intern-owned here is narrower:

1. a **grain → estimand map** for this governed monthly first-event extract;
2. a **pre-specified refusal** when a named check fails, displayed rather than buried in limitations;
3. a **string tripwire** (`estimand_policy` in `claim_ledger.yml`) that requires the contribution phrases and forbids a short list of smuggled-primary strings. It is not a semantic estimand parser.

Naming the framework raises the defensibility of the contribution type. It does not raise power. It does not freeze Gate 3. It does not create stroke, daily, AMI, or monetisation coefficients.

## Two objects

**Aggregation-identifiability.** At month grain, some estimands are recoverable from 132 territory-months of first CHD/HF hospitalisation counts among people with T2D and/or HTN. Some are not. The contribution is the map, not a new coefficient.

**Calibrated refusal.** When a pre-specified check fails, the paper does not estimate that object. Refusal is a result of the methods, not a late ethics paragraph.

```
monthly extract
        |
        v
 grain → estimand map
        |
        v
 F1.2 / q-bar / SE ladder / winter support
        |
   +----+----+
   v         v
recover    refuse
```

F1.2 is an internal protocol label. It must **not** appear in the live manuscript (`forbidden_in_manuscript`). The live file already reports the same refusal without that token: “No real daily coefficient is reported.”

## Grain → estimand map

| Estimand | Recoverable here? | Why | Where it already lives |
|---|---|---|---|
| Ecological monthly count ratio, first CHD or HF hospitalisation after first diagnosis, T2D/HTN cohort, days-in-month offset | Yes, exploratory | That is the delivered grain | Table 2; live Results |
| Winter identification of official cold days (between-winter, not summer-versus-winter) | Yes, descriptive | 141 of 145 official cold days fall in DJF; 29 of 132 months carry ≥1 | Figure 2; live Results |
| First-event decline vs C&SD 35+ population (depletion, not incidence) | Yes, descriptive | Still-at-risk person-time was not delivered | Figure 1 |
| Movement of each contrast across Model / HC1 / NW3 / NW6 | Yes, diagnostic | No SE method may be chosen because it excludes 1 | Table 3; assumption A54 |
| Specification dependence (trend df, pre-2020, COVID-phase, lag-1 month) | Yes, diagnostic | Window and spline entanglement are identified, not estimated away | Figure 3 |
| Twelve-contrast *q*-bar (min *q* = 0.192) | Yes, as a refusal of a protected primary | Multiplicity is reported, not used to promote a winner | Table 2 |
| Wald MDE from Table 4 SEs (intern-owned, not a primary) | Yes, as a power statement about the existing ladder | CHD hot nights NW6 MDE ≈ 2.86% per five nights at 80% power; observed 1.022 excludes 1 only under Newey–West and is *q*-unprotected | Derived from `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`; formula exp((1.96+0.84)×SE_log). Not pasted into the live file. |
| Daily DLNM / daily trigger coefficients from 132 monthly sums | **No** | Clean-room M\|D failed 500-replicate F1.2 worst-cell gates | Live Methods + Results refusal; protocol F1.2 |
| Heatwave excess-death mortality; Jasmine/Roro attributable fractions | **No** | Different estimand class | Live Discussion; evidence map |
| AMI / principal-diagnosis CHD or HF | **No** | Admission cause was not recorded | Live Methods; assumption A04 / A40 / A46 |
| Stroke coefficients | **No** | File named, not attached | Idle checklist; never invent |
| Cohort incidence (still-at-risk person-time) | **No** | Denominator not delivered; offset is days | Live Methods; assumption A48 |
| Health-econ / `SYNTHETIC_THEORY` | **No** | Out of the journal-track file | Playbook 05 failure modes |

## Existing displays (already instantiate the framework)

The live Discussion already said “identification rather than estimation” and listed four displays. Hogan’s line promotes that refusal from a limitations ethic into the **named contribution**. The displays do not change:

1. **Winter support** — Figure 2; 29 of 132 months; 141 of 145 cold days in DJF.
2. **Depletion** — Figure 1; first-event decline against rising 35+ population.
3. **SE ladder** — Table 3; CHD hot nights Model/HC1 include 1; NW3 unrounded 1.000253–1.043860; NW6 1.022 (1.002–1.042).
4. **Specification map** — Figure 3; pre-2020 CHD hot nights 1.011 (0.991–1.032) includes 1.

Plus two refusals that were already in the file:

5. **Daily-recovery refusal** after F1.2 (Type I 0.048–0.150; minimum coverage 0.840; relative bias 32.8; moderate false-sign 0.808). No real daily coefficient.
6. **Multiplicity refusal** — all twelve core *q* > 0.19. No confirmatory primary (lead Option A; Gate 3 still open).

Permutation and future-month negative-control checks remain unrun. They may illustrate calibrated refusal later. They are not a primary.

## What auto-research may and may not do

**May:** keep this memo; keep the live contribution paragraph in Hogan English; keep the machine estimand rule; audit originality bound; log residue.

**May not:** rebuild Stage 3 PDF/A0 poster; overwrite Hogan weather (“Meteorological data was obtained from the HKO.”); freeze Gate 3; invent stroke/daily/AMI/monetisation numbers; claim a theorem; treat MDE or permutation tests as a confirmatory primary; paste into Hogan’s shared file.

## Live-file contribution paragraph

Drafted in `manuscript/live_collaborative/Heat_CVD_Manuscript_live_update.md` (Discussion). Paste list: `LIVE_DOC_EDITS.md`. Stage 3 source markdown is **not** the journal authority and is not rebuilt as PDF.

## Auditor

`claim_ledger.yml` now carries `estimand_policy`. `scripts/50_audit_live_claim_ledger.py` fails if the contribution phrases are missing, if the daily-recovery refusal sentence is missing, or if a smuggled primary phrase appears. A green auditor is not a Gate 3 freeze.
