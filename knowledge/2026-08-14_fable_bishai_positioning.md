# Fable pass — positioning the maps for Bishai — 14 August 2026

**Role:** senior-scientist read of what a doctoral supervisor actually wants to receive.
**Mode:** Decide. Residue only — no email sent, no analysis run, no number created. Every numeral below already exists in a repo file (`2026-08-14_threshold_does_not_travel.md`, `2026-08-14_opus_professor_pass.md`, `2026-08-14_yc_board_synthesis.md`, the live manuscript, the Bishai status draft).
**Charter:** [`2026-08-14_bishai_positioning_charter.md`](2026-08-14_bishai_positioning_charter.md).
**Rails:** no health on maps; no transported CHD/HF ratios; live paper stays on HKO Headquarters; frozen PDFs stay frozen; Gate 3 open; all core *q* > 0.19. Bishai is a supervisor, not a YC partner.

---

## The one sentence Bishai should remember

> **"We measured our own largest limitation before a reviewer could, and the measurement defends the design."**

The limitation is the paper's own sentence: all exposures from one Observatory station, applied territory-wide. The measurement is the calibration: −1.47 °C night bias, agreement 0.031 at the official 28 °C threshold, never above 0.47 at any threshold. The defence is that no recalibrated reanalysis reproduces the station's nights, so staying on Headquarters is a supported decision. That is a supervisor line — it reports moved work, an honest limitation, and a design he can stand behind. The Demo Day version ("449, 17, or 1,453 hot depending on the thermometer") stays in the demo file.

## How the maps earn their keep

Bishai asked in July for multi-method work and a Table 1 of temperature. The panel
delivered the methods side: twelve contrasts, a four-construction uncertainty ladder,
every *q* reported. The maps are the exposure side of the same panel — the Table 1 of
temperature made spatial. They characterise the instrument before anyone trusts a
coefficient. The live paper concedes that exposures come from a single station; the
maps price that concession. At the same coordinate on the same 4,017 nights, the
station flags 449 hot nights and the reanalysis 17; adding back the bias recovers the
count but not the nights (maximum Jaccard 0.47 at 26.3 °C). That is the identification
result: the station cannot be replaced by a gridded product, so keeping Headquarters
is a defended choice, not a habit. EOF1 at 92 % adds the second defence — the basin's
daily anomaly field has about one degree of freedom, so a single well-sited station
loses less than it appears to. They are not a second health paper: no health series
touches a cell, no ratio travels, no map claims a finding. Their whole job is to turn
one Limitations sentence into a measured quantity.

## What to send him (and what not)

| Object | Disposition | Why |
|---|---|---|
| Frozen Stage 3 essay PDF | **Send now** | Attached to the 2a email. Frozen bytes; it is the programme object, not a results source. |
| Form 2a | **Send now** | His endorsement is the named likeliest miss before 31 August. One ask, one date, nothing else in the email. |
| Live-paper status | **Never as a separate memo** | He is copied on the Hogan/Roro thread and reads it. Status travels there; a parallel note duplicates the thread. |
| One methods figure (`exceedance_and_agreement`, static) | **Send later** | Inside the science note, after Hogan has seen the card — the limitation sentence lands in Hogan's weather section first. |
| URLs (LSN University-room post) | **Send later** | Once posted. That URL is what HKU reports to the Foundation; GitHub Pages is not a substitute. |
| Gate 3 packet | **Send later** | When he convenes the team freeze. It is his decision object, not a progress update; offer it, do not push it. |
| Six map links | **One link later; never six** | The hallway index only, inside the science note, labelled exposure-only. Six links reads as a portfolio, and the four rooms are one claim. |

Not on any list: HA source files, release CSVs, unrequested model tables, the poster
(unless he asks), or any `.md` attachment. The thread culture is explicit — show the
thing asked for, in a form the person can open.

## Two emails, not one

**Email one — the endorsement.** Form 2a plus the frozen essay. One ask (his
endorsement), one date (the 31 August deadline), no maps, no demo link, no new
science, no Gate 3 language. Mixing a signature request with new science invites him
to review the science before signing, and the signature is on the critical path to
`laidlaw@hku.hk`. The board already ruled the demo out of this email.

**Email two — the science note, later.** The three-decision status draft
(`analysis_plan/bishai_stage3_status_report.md`) already carries the panel honestly:
twelve contrasts, all *q* > 0.19, no headline requested. Fold in one paragraph on the
exposure calibration, the one static figure, and the one hallway link — framed as the
single-station limitation measured, not as a new project. Because he reads the
thread, if the same content serves Hogan and Roro it belongs on the thread and no
private note is needed that day. The rule either way: if he answers only one email
this month, it must be the 2a.

## Directions that make the maps more relevant

Nothing below is another map. The 90-cell cache has been read; the eighth spatial
method told us what the first did, and a fifth Leaflet is killed on sight. Ranked by
whether a sentence in the CHD/HF paper changes because of it.

1. **Monthly-grain attenuation slope (HKO vs ERA5 hot-night counts, 132 months).**
   The paper's exposure is a monthly count, so this is the agreement statistic at the
   estimand's own grain. Regress the grid's monthly count on the station's; a slope
   below one says, without touching an outcome, roughly how far a grid-based
   coefficient would be pulled toward the null. It converts the Limitations hedge
   into a number. *Constraints:* one coordinate, one product; it bounds a
   hypothetical grid analysis, not our HKO estimates; state that the failed
   daily-recovery calibration is why no daily version exists.
2. **Effective identifying months per contrast.** With calendar-month indicators and
   the trend spline, each contrast is identified between years within month; cold
   days are 141/145 December–February. Print, for all twelve contrasts, the months
   actually carrying exposure variation. It reframes *q* > 0.19 as a design fact
   rather than a multiplicity accident — the identification honesty his multi-method
   ask deserves. *Constraints:* counts read off the exposure files, not asserted; the
   DJF exploration figure stays EXPLORE-ONLY until verified.
3. **Population-weighted hot nights (the Marmot direction, exposure only).** The
   hotspot mass sits on water and the highland cells record none; weighting the HK
   lattice and PRD mosaic by public gridded population moves the map from pixels to
   people — who is exposed, not just where it is warm. This is the only Marmot-shaped
   step available without health data. *Constraints:* public population grids only;
   weighting does not repair the −1.47 °C bias; the result stays a grid object; no
   health counts on cells, no transported ratios; do not invoke Marmot in text until
   this layer exists.
4. **Effective dimension of the HM/CM definition space (exposure only).** Ninety-eight
   definitions is a menu. The correlation structure and effective rank of the 98
   monthly series tells Hogan which definitions genuinely differ from `HM23` and makes
   the multiplicity discussion honest. Direct input to his lock. *Constraints:* run
   before outcomes reopen; an effective-rank statement is not a licence to fit more
   definitions.
5. **Station replicates for the calibration.** Add one or two further HKO open-data
   stations as public replicates, reporting sensitivity and PPV beside Jaccard. This
   answers the n = 1 coordinate objection from public data and states the
   Headquarters pixel as a mixed land–sea cell — a declared worst case, not a hidden
   one. *Constraints:* public stations only; never framed as "validation of ERA5."
6. **Year-shifted negative-control exposure (last, gated).** Re-fit the twelve
   contrasts with exposure displaced by whole years. It directly tests whether the
   CHD hot-night residual is a trend artefact — the only item here that touches
   outcomes. *Constraints:* needs a human nod and a Gate-3-open label; generates new
   numbers; a pass upgrades no *q* and creates no headline.

## What would embarrass us in front of him

- The pitch register: the Demo Day sentence, "AI ran eight spatial methods
  overnight," product language of any kind. He supervised a scholar, not a startup.
- Bundling the 2a with science, maps, or the demo — delaying his signature is the
  named likeliest miss of the whole programme.
- Any map with health colour on it; any transported CHD/HF ratio; ERA5 counts pasted
  as HKO flags; apparent-temperature counts quoted as hot nights.
- Promoting HF cold days (1.073) or CHD hot nights (1.022) to a finding before the
  team Gate 3 he owns. All twelve *q*-values exceed 0.19 and he knows it.
- "+0.29 °C/decade" or "23 of 90" as a trend claim (0/90 survive BH); EOF1 92 %
  quoted as a discovery instead of a design statement; SAR ρ as spillover science;
  the *r* > 0.90 network as an object.
- "Validation of ERA5" from one coordinate.
- Name-dropping Marmot before a population-weighted layer exists to stand on.
- Six links as a portfolio, `.md` attachments, decision lists on the thread, or a
  parallel Word manuscript.
- Reopening the frozen essay or poster to reconcile them with later prose.
- Calling count ratios incidence, or letting "first hospitalisation after first
  diagnosis" drift toward "cardiac admission."

---

*Residue: this memo. No email was sent, no analysis was run, no number was created.
Companions: [`2026-08-14_yc_board_synthesis.md`](2026-08-14_yc_board_synthesis.md),
[`2026-08-14_opus_professor_pass.md`](2026-08-14_opus_professor_pass.md),
[`2026-08-14_threshold_does_not_travel.md`](2026-08-14_threshold_does_not_travel.md).*
