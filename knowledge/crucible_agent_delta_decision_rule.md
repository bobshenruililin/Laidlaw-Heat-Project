# Crucible Agent Delta — residual-signal decision rule

**Post-audit (14 Aug):** SURVIVES-IN-REDUCED-FORM. BH arithmetic and “q > 0.19 ≠ absence” stand. The 77%-of-detectable power inversion is *p* restated and is struck. Option B-lite is not a rival freeze (Option A already requires the full panel). See `knowledge/crucible_adversarial_audit.md` and `reports/identification_crucible_2026-08-14.md`.


**Date:** 2026-08-14  
**Mode:** Explore (proof memo; no new models; no HA microdata)  
**Agent:** Delta (requested GLM-5.3 Max; slot filled by Grok 4.5 High)  
**Branch:** `cursor/identification-crucible-1fd0`  
**Thesis (extreme):** Option A is a correct *reporting rule* (“no confirmatory primary”) and an incorrect *scientific reading* (“the panel found nothing”). The more honest freeze is Option B-lite: report the two outstanding residuals with multiplicity and SE-ladder attached, not as a null.

**Accepted estimand:** month FE + `ns(time,4)` residual association. This memo does not attack daily kernels, person-time bias, or the month-FE choice.

**Forbidden promotions:** calling RR 1.073 a discovery; calling either contrast a mechanism; inventing HA counts or new coefficients; reading `q>0.19` as absence of association.

---

## 1. Provenance

| Object | Status | Source |
|---|---|---|
| Core 12 RRs, NW6 p/q | `HA_APPROVED_AGGREGATE` | `outputs/release_chd_hf/tables/table2_core_models.csv`; `outputs/identification_crucible/bh_detectability.csv` |
| SE ladder exclude-1 flags | `HA_APPROVED_AGGREGATE` | `outputs/identification_crucible/se_method_discordance.csv`; `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv` |
| BH thresholds / min-p ratio | recomputed from paid p-values | `outputs/identification_crucible/identification_summary.json` |
| Detectability | paid NW6 SE inversion | `bh_detectability.csv` |
| Trend/depletion, pre-COVID, lag, influence | `HA_APPROVED_AGGREGATE` | `cvd_trend_depletion_sensitivity.csv`; `cvd_lag_sensitivity.csv`; `cvd_influence_sensitivity.csv`; `table3_robustness_summary.csv` |
| Residual ACF | `HA_APPROVED_AGGREGATE` | `cvd_core_model_fit.csv` (days-only NB) |
| Climate leftover after month+ns4 | `REAL` HKO monthly | `exposure_residual_variation.csv`; `identification_summary.json` |
| Option A / B wording | prior lead recommendation | `reports/bishai_integrated_report/integrated_project_report.md` §10 |

No governed CHD/HF microdata were read. No web search. Hogan weather prose, Stage 3 PDFs, and live paste files were not touched.

---

## 2. BH reconstruction — `q=0.192` is arithmetic

Twelve amended-core NW6 p-values, ascending:

| Rank | Contrast | p | Naive `p·m/rank` | BH step-up q |
|---:|---|---:|---:|---:|
| 1 | HF P04B cold days /5 | 0.03096467 | 0.3716 | **0.1922** |
| 2 | CHD P04A hot nights /5 | 0.03203984 | 0.1922 | **0.1922** |
| 3 | HF P02B mean tmin | 0.05041364 | 0.2017 | 0.2017 |
| 4 | HF P01A mean temp | 0.06915482 | 0.2075 | 0.2075 |
| 5–12 | remaining eight | ≥0.113 | ≥0.272 | ≥0.272 |

BH step-up: from the largest rank down, \(q_{(i)}=\min\!\big(q_{(i+1)},\,p_{(i)}\cdot m/i\big)\).  
Rank-2 naive already equals 0.1922; rank-1 is therefore *pulled down* to the same 0.1922, not “discovered weak.”  
Rank-1 `q<0.05` would need \(p\le 0.05/12=0.004167\). Observed min p is **7.43×** that threshold (`identification_summary.json`).  
**Decision rule piece:** `all q>0.19` is the 12-test Benjamini–Hochberg tax on two unadjusted ~0.031 signals. It is not a scientific demonstration that the residual associations are absent.

---

## 3. Power inversion — underpowered for the size it estimates

HF cold days /5: NW6 SE of log RR ≈ **0.03257** (`bh_detectability.csv`).  
Two-sided α=0.05 at ~80% power needs \(|\beta|\approx 2.8\cdot\mathrm{SE}=0.0912\) → RR≈**1.095**.  
Observed \(|\log\mathrm{RR}|=0.0703\) → RR **1.073**; observed/detectable = **0.771**.  
CHD hot nights /5: observed/detectable = **0.766** (RR 1.022 vs detectable ~1.029).

Under a true residual effect of this magnitude, failing BH at 0.05 after twelve tests is the **expected** outcome, not a surprise.  
**Decision rule piece:** `q>0.19 ≠ null`. The design cannot protect an effect it is only ~77% of the way to detecting at 80% power after the BH tax.

---

## 4. Separate HF cold from CHD hot nights

### HF P04B cold days /5 = 1.073 — outstanding residual (headline of the exploratory panel)

- **SE-concordant:** Model / HC1 / NW3 / NW6 **all** exclude 1 — the only core-12 contrast with `se_concordant_exclude_1=True`.
- **Trend/depletion range:** 1.043–1.113 (baseline 1.073); pre-COVID **1.113**, p=1.5×10⁻⁴; drop max-Cooks month 2022-02 → **1.088**, p=0.001; lag-1 **1.073** (1.014–1.135), p=0.014.
- **Residual ACF1:** ~0.15 (days-only NB). Serial correlation is modest; NW does not rescue a fragile Model CI.
- **Climate leftover:** after month+ns4, cold days retain **~46%** of variation (`variation_share_remaining_after_full_controls=0.458`). The residual estimand is not empty.

### CHD P04A hot nights /5 = 1.022 — demote to SE-sensitive

- **SE-fragile:** Model and HC1 **include** 1; only NW3/NW6 exclude 1.
- **Trend/depletion range:** 1.011–1.025; **pre-COVID 1.011 (0.991–1.032), p=0.289** — fails the pre-COVID cut.
- **Residual ACF1:** ~0.51. NW6 **narrows** relative to Model (0.995–1.049 → 1.002–1.042). That narrowing is a diagnostic that serial correlation is not inflating CHD precision in the usual “Model too tight” story; it is a reason to distrust SE-selected exclusion of 1.
- July hot nights still vary 1–25 within calendar month (`identification_summary.json`); identification leftover exists, but the *association* does not survive the SE/pre-COVID ladder that HF cold does.

**Extreme separation:** headline HF cold as the exploratory panel’s outstanding residual; demote CHD hot nights to an SE-sensitive companion contrast. Do not sell them as equal “two signals.”

---

## 5. Option A vs Option B-lite

| Reading | Licensed? | Why |
|---|---|---|
| Option A as reporting rule: “do not freeze a confirmatory primary” | **Yes** | All q>0.19; no contrast clears BH; Gate 3 must not crown a primary. |
| Option A as scientific null: “the panel found nothing” / “no association” | **No — forbidden promotion** | Converts a multiplicity/power tax into absence. Contradicts SE-concordant HF cold, pre-COVID strengthening, influence/lag robustness, and non-empty residual climate variation. |
| Option B-lite | **Preferred freeze language** | Report HF cold (outstanding) and CHD hot nights (SE-sensitive) as exploratory residuals with BH q and full SE ladder attached; refuse discovery and mechanism language. |

### Audit-surviving sentence

> Under the month-FE + ns(time,4) residual estimand, this twelve-contrast panel does not license a confirmatory primary; it does retain an SE-concordant exploratory residual for HF cold days per five days (RR 1.073; Model/HC1/NW3/NW6 all exclude 1; BH q=0.192) and an SE-fragile companion for CHD hot nights per five days (RR 1.022; Model/HC1 include 1; q=0.192), where q>0.19 is the expected Benjamini–Hochberg outcome for effects at ~77% of the 80%-power detectable size, not a demonstration of absence.

---

## 6. Self-falsification — when Delta would accept a true null

Delta’s residual-signal claim dies, and a true-null reading becomes honest, only if **all** of the following hold on the same paid panel (or a governed re-fit that replaces it):

1. **No SE-concordant exclude-1 contrast** in the core 12 (HF P04B loses Model or HC1 or both NW intervals that currently exclude 1).
2. **Min unadjusted p ≥ 0.20** (or BH rank-1 q ≥ 0.50 with no second p near the first), so the “BH tax on a real ~0.03 signal” story cannot be told.
3. **observed/detectable ≤ 0.35** for every near-null contrast *or* NW6 SE tight enough that 80%-power detectable |β| is below the paid |log RR| while CIs still include 1 under Model and HC1.
4. **HF cold robustness collapse:** pre-COVID RR CI includes 1, lag-1 fails, and influence drop moves the point estimate through 1 — i.e. the 1.043–1.113 band no longer sits above 1.
5. **Climate leftover near zero** for cold days after month+ns4 (residual share ≪ current 46%), so the residual estimand itself empties.

Any one of (1)–(4) alone weakens the extreme thesis; the conjunction of (1)+(2)+(4) is enough for Delta to concede Option A-as-null for HF cold. CHD hot nights already fail (1) and the pre-COVID cut; they are not carrying the thesis.

---

## 7. What this memo is not

- Not Alpha (daily-kernel failure).  
- Not Beta (person-time bias as cause).  
- Not Gamma (month FE as wrong estimand).  
- Not a Gate 3 freeze; humans own Option A / B / C.  
- Not a discovery claim, mechanism claim, or stroke claim.

**Keep:** Option B-lite wording + HF/CHD separation + BH/power arithmetic.  
**Drop:** reading `q>0.19` as “no association.”  
**Park:** any promotion of 1.073 to primary until a human Gate 3 and, if sought, a design that can clear BH at the observed effect size.
