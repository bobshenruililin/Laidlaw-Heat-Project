# Stage 3 report and poster freeze — 12 August 2026

Bob locked two GPT-5.6 Sol outputs as the Laidlaw Stage 3 submission copies:

| File | SHA-256 prefix | Bytes |
|---|---|---|
| `reports/laidlaw_stage3/Laidlaw_Research_Report_2026.pdf` (same bytes as `outputs/Laidlaw_Stage3_Research_Report_Shen.pdf`) | `6136e85a654502a0` | 715,033 |
| `reports/poster/Laidlaw_Stage3_A0_portrait.pdf` (same bytes as `outputs/Laidlaw_Stage3_Poster_Shen.pdf`) | `4f7c1e408ae2d31f` | 92,744 |

These match the files Bob uploaded on 12 August 2026. They are already on `main` (merged PR #39).

## What later draft PRs would have changed

| PR | Would have changed the Sol PDFs? | Decision |
|---|---|---|
| #40 external-review-reconciliation | **Yes — report only.** Rewrote NW3 as 1.0003–1.0439, added ACF, F1.2 wording, `ns(time,4)`. Poster unchanged. | **Do not take.** Honesty belongs in the live manuscript, not a second Stage 3 report. |
| #41 Hogan/Roro handoff | No | Dictionary for the Roro temperature share is kept. Methods paste is superseded by `manuscript/live_collaborative/`. |
| #42 Sol publish-pattern trim | **Yes — report only.** Cut ≈300 words (3,551 → 3,245 tokens) for a 3,000-word cap. Poster unchanged. | **Do not take.** Bob prefers the untrimmed Sol report. |
| #43 Hogan tonight / Bishai | No | Already inside the single remaining PR. |
| #44 live manuscript | No | **Keep.** Collaborative manuscript only. |

## Rule

Do not rebuild `Laidlaw_Research_Report_2026.pdf` or `Laidlaw_Stage3_A0_portrait.pdf` unless Bob supplies a new locked copy. Journal and live-manuscript surfaces may still be edited.
