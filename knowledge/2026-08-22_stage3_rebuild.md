# Stage 3 report and poster — Bob-authorised rebuild (22 August 2026)

**Mode:** Ship. Not a Gate 3 freeze. Not a journal rewrite.

Bob lifted the 12 August Sol byte-lock. He asked to delete the poster’s self-referential footer, take the 2,000–3,000-word HKU requirement seriously, change the report typeface, format the essay as a formal academic paper, and name the submission files `ShenRuililin_Laidlaw_Stage3Report.pdf` and `ShenRuililin_Laidlaw_Stage3Poster.pdf`. Fable and Sol reviewed the live manuscript against the previous essay, then signed off the rebuilt PDFs (GO / GO).

## New lock

| File | Bytes | SHA-256 |
|---|---:|---|
| `outputs/ShenRuililin_Laidlaw_Stage3Report.pdf` | 708,248 | `b8b4c63ca9d32dd37e5ba240cf2212071953b4d815c6b24ca957fa5414fdfd6b` |
| `outputs/ShenRuililin_Laidlaw_Stage3Poster.pdf` | 92,186 | `b3f16ff27f76ea9b244d27919a8319c676326ba47c31a92344892e43701443ac` |

Identical copies: `reports/laidlaw_stage3/ShenRuililin_Laidlaw_Stage3Report.pdf`, `reports/poster/ShenRuililin_Laidlaw_Stage3Poster.pdf`, and the legacy names `Laidlaw_Research_Report_2026.pdf` / `Laidlaw_Stage3_A0_portrait.pdf` / `outputs/Laidlaw_Stage3_*_Shen.pdf`.

## What changed

**Poster.** Only the footer. The AI metadata block (ISO A0, collaborators, “machine-validated”) is gone. `\vfill` is retained so the bands do not shift. Contact line only: `shenrll@connect.hku.hk`. One page, 841 × 1189 mm. Required sections unchanged. Conclusion wording left as in the 12 August layout (an alternative sentence was considered and not applied).

**Report.** TeX Gyre Termes, no contents list, running header, 11 pt, 1.15 spacing. Author line is Shen Ruililin. Main text (Summary through Conclusion) is about 2,900 words. Honesty aligned with the live manuscript without turning the essay into the journal paper:

- Newey–West lag 3 printed as 1.0003–1.0439
- pre-2020 CHD hot nights 1.011 (0.991–1.032)
- CHD lag-1 residual autocorrelation 0.508
- cold days 141 of 145 in December–February; 29 of 132 months
- Conclusion uses “more closely associated … than the other thermal measures,” not “most elevated”
- “continuity” jargon removed

## Superseded lock

12 August Sol copies (SHA prefixes `6136e85a654502a0` / `4f7c1e408ae2d31f`) remain in git history. See [`2026-08-12_sol_stage3_outputs_lock.md`](2026-08-12_sol_stage3_outputs_lock.md).

## Still true

Gate 3 is open. No stroke result. No CHD/HF model was refit. Hogan’s weather paragraph was not rewritten. Form 2a is still a new message to Bishai only. Rebuild again only if Bob or Bishai requires a further correction.
