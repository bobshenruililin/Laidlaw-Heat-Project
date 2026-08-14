# Aggregation is the estimand

## 1. Thesis

This design identifies only a negative-binomial projection of a depleting first-event monthly count onto year-to-year weather deviations within the same calendar month after a smooth time control; it does not identify daily thermal triggering, individual causality, or heat- or cold-caused hospitalisation, so Gate 3 Option A is the only logically licensed freeze.

## 2. Provenance and data contract

1. `[HA_APPROVED_AGGREGATE]` The outcome is the territory-month count of the first recorded hospitalisation after the first CHD or HF diagnosis in a T2D/HTN cohort. Admission cause is absent. It is neither incidence nor a principal-diagnosis endpoint. The stroke file is missing.
2. `[REAL + HA_APPROVED_AGGREGATE DESIGN]` The panel contains \(n=132\) territory-months from January 2013 through December 2023. The model of record is fitted separately by outcome and exposure: negative binomial, calendar-month fixed effects, \(ns(time,4)\), a days-in-month offset, and Newey-West lag \(6\) for the main display. The control matrix has rank approximately \(16\), leaving approximately \(116\) residual degrees of freedom before adding the exposure.
3. `[BACKGROUND: HA_APPROVED_AGGREGATE + REAL C&SD]` First-event totals roughly halved over the study window while the broad population aged \(35+\) rose. This establishes depletion of the counted event pool; it is background to the outcome's meaning, not the principal argument here.
4. Numerical labels below are local: `[REAL]` means public HKO climate, `[HA_APPROVED_AGGREGATE]` means paid release tables, `[SYNTHETIC_CALIBRATION]` means no real health coefficient, and `[DESIGN_DERIVED]` means algebra or a calculation from those labelled artifacts.

## 3. The identified estimand

1. Let \(Y_{ot}\) be the observed first-event count for outcome \(o\) in month \(t\), \(D_t\) the number of days in that month, and \(Z_t=X_t/5\) for either the hot-night or cold-day count. `[DESIGN_DERIVED]` The divisor \(5\) is the paid model's reporting contrast, not a daily lag.

2. Let \(C_t\) contain the intercept, calendar-month indicators, and the \(4\)-df time-spline basis. `[DESIGN_DERIVED]` For each outcome and one exposure at a time, the fitted NB2 mean is

   \[
   Y_{ot}\sim NB2(\mu_{ot},\theta_o),\qquad
   \operatorname{Var}(Y_{ot})=\mu_{ot}+\mu_{ot}^2/\theta_o,
   \]

   \[
   \log\mu_{ot}=\log D_t+C_t^\top\gamma_o+\beta_o Z_t.
   \]

3. `[DESIGN_DERIVED]` With \(A_{ot}=\theta_o/(\theta_o+\mu_{ot})\), the maximum-likelihood score equations are

   \[
   U_{\beta_o}=\sum_t Z_tA_{ot}(Y_{ot}-\mu_{ot})=0,\qquad
   U_{\gamma_o}=\sum_t C_tA_{ot}(Y_{ot}-\mu_{ot})=0.
   \]

   These equations, not a comparison of hot months with cold months, define the coefficient.

4. `[DESIGN_DERIVED]` Define the Fisher weight
   \(Q_{ot}=\theta_o\mu_{ot}/(\theta_o+\mu_{ot})\), the weighted control
   projection

   \[
   \pi_o=(C^\top Q_oC)^{-1}C^\top Q_oZ,
   \]

   and the residual exposure \(\widetilde Z_o=Z-C\pi_o\). Because the nuisance
   score is zero, the exposure score is equivalently

   \[
   \sum_t \widetilde Z_{ot}A_{ot}(Y_{ot}-\mu_{ot})=0.
   \]

   Around the control-only fit, write its fitted mean and weights as
   \(\mu^{(0)}\), \(A^{(0)}\), \(Q^{(0)}\), and
   \(\widetilde Z^{(0)}\). Its first nuisance-adjusted Newton step is

   \[
   \widehat\beta_o\approx
   \frac{\sum_t\widetilde Z_{ot}^{(0)}A_{ot}^{(0)}
                     (Y_{ot}-\mu_{ot}^{(0)})}
        {\sum_tQ_{ot}^{(0)}(\widetilde Z_{ot}^{(0)})^2}.
   \]

   Thus the slope is a model-weighted association between residual first-event
   monthly counts and residual monthly weather burden.

5. **Precise name.** The estimand is the outcome-specific, separate-exposure,
   nuisance-adjusted NB2 pseudo-true log count-ratio parameter for a
   year-to-year within-calendar-month change in monthly extreme-day burden,
   conditional on the fitted \(4\)-df secular trend and normalized by days in
   month. `[DESIGN_DERIVED]` The reported \(\exp(\beta_o)\) is the expected
   monthly count ratio for \(5\) additional hot nights or cold days. It is an
   ecological conditional association parameter, not a daily effect, an
   individual causal contrast, an incidence-rate ratio, or an admission-cause
   effect.

6. Month fixed effects remove the average January–December thermal cycle; they
   do not erase all exposure variation. `[REAL]` Mean temperature has
   \(R^2=0.958\) under month effects and \(R^2=0.964\) after the time spline,
   leaving an SD of \(0.90^\circ C\). Its coefficient is therefore driven by
   roughly \(1^\circ C\) anomalies within calendar month, not summer versus
   winter.

7. `[REAL]` Hot nights have month-effect \(R^2=0.712\), full-control
   \(R^2=0.749\), residual SD \(2.70\) nights, and \(57/132\) nonzero months.
   July ranges from \(1\) to \(25\) hot nights, with mean \(13.5\).
   `[REAL]` Cold days have month-effect \(R^2=0.531\), full-control
   \(R^2=0.542\), residual SD \(1.73\) days, \(46\%\) of variation remaining,
   and \(29/132\) nonzero months. There are \(145\) cold days in total,
   \(97.2\%\) in DJF; January ranges from \(0\) to \(11\). These are sparse,
   season-specific year-to-year anomalies, but they are not zero variation.

## 4. Why a daily lag kernel is not recovered

1. Let daily latent means be \(\lambda_d(k)\), where \(k\) is a daily lag
   kernel, and let \(A\) be the calendar aggregation operator. The observed
   monthly mean is

   \[
   \Lambda_m(k)=\sum_{d\in m}\lambda_d(k)=(A\lambda(k))_m.
   \]

   `[DESIGN_DERIVED]` Any daily perturbation \(v\) satisfying
   \(\sum_{d\in m}v_d=0\) for every month lies in the null space of \(A\):
   \(A(\lambda+v)=A\lambda\). More people observed inside the same monthly
   cells could estimate \(\Lambda_m\) more precisely, but could not reveal
   which days generated it. Daily allocation and lag timing require either
   daily outcomes or additional structural restrictions.

2. A constrained M\(|\)D likelihood supplies such restrictions. Its local
   information for lag parameter \(k_\ell\) comes through

   \[
   \frac{\partial\Lambda_m}{\partial k_\ell}
   =\sum_{d\in m}\lambda_d(k)x_{d-\ell}.
   \]

   `[DESIGN_DERIVED]` The observed data contribute one aggregated score per
   month, not one health score per day. A low-dimensional kernel can therefore
   be admitted only if its restrictions recover truth with calibrated error
   under the actual weather sequence, count scale, seasonality, depletion,
   shocks, and serial dependence. Algebraic convergence alone is not
   identification.

3. `[SYNTHETIC_CALIBRATION]` F1.2 tested \(500\) replicates across \(36\) core
   cells. Minimum convergence was \(1.000\), the maximum median Hessian
   condition number was \(1.82\times10^3\) against a \(10^8\) ceiling, and the
   divergent-fit rate was \(0\). The method nevertheless had null Type I error
   as high as \(0.150\) against the required \(0.03\)–\(0.08\), minimum
   coverage \(0.840\) against at least \(0.90\), maximum absolute relative bias
   \(32.77\) against at most \(0.20\), and maximum moderate-effect false-sign
   probability \(0.808\) against at most \(0.10\).

4. Those failures are not the signature of a merely underpowered but valid
   estimator. `[SYNTHETIC_CALIBRATION]` A pure power problem would permit
   calibrated Type I error and coverage with wide intervals; F1.2 instead
   produced false positives, undercoverage, severe bias, and wrong signs while
   fitting cleanly. The recorded decision is
   `FAIL_METHODS_FEASIBILITY_ONLY`, and no real daily coefficient was admitted.

5. “Retune M\(|\)D” is not an inferential answer. Retuning after seeing a failed
   gate changes the structural restrictions that manufacture daily
   information from monthly sums. A replacement becomes admissible only after
   a new, prespecified, independently audited calibration passes every gate.
   Until then, the daily kernel is an unvalidated extrapolation through the
   aggregation null space.

## 5. Why “CHD heat / HF cold” is a forbidden promotion

1. `[HA_APPROVED_AGGREGATE]` The separate monthly models report CHD hot nights
   per \(5\) days at \(1.022\). Its Model interval includes \(1\), whereas its
   Newey-West lag-\(6\) interval excludes \(1\). `[HA_APPROVED_AGGREGATE]` HF
   cold days per \(5\) days is \(1.073\); all \(4\) displayed SE methods exclude
   \(1\), but its BH value is \(q=0.192\).

2. These are two roots of two different score systems. Neither estimates the
   cross-outcome contrast. `[DESIGN_DERIVED; A58]` The frozen test is

   \[
   \Delta=
   (\beta_{H,CHD}-\beta_{C,CHD})
   -
   (\beta_{H,HF}-\beta_{C,HF}).
   \]

   Separate nominal tests do not estimate \(\operatorname{Var}(\widehat\Delta)\)
   and cannot establish \(\Delta\ne0\).

3. The registry names `M06_STACKED_HEAT_COLD_INTERACTION`, but the public
   release contains no `HA_APPROVED_AGGREGATE` result from that model.
   Therefore “CHD heat / HF cold mechanism” is not a tested result. It is a
   post-outcome narrative assembled by selecting different exposures from
   different outcome models.

## 6. Concrete counterexamples to rival theses

1. **“Month fixed effects kill all thermal variation.”** False. `[REAL]` After
   full controls, hot nights retain SD \(2.70\) and cold days SD \(1.73\);
   \(46\%\) of cold-day variation remains. The design identifies anomaly
   association, not zero.

2. **“The daily problem is just \(n=132\).”** False as a description of the
   present failure. `[DESIGN_DERIVED]` Aggregation has a within-month null space
   even with perfectly measured monthly totals. `[SYNTHETIC_CALIBRATION]` At
   \(500\) replications, F1.2 converged in every core cell yet failed Type I,
   coverage, bias, and sign gates. The defect is unvalidated recovery from the
   available grain, not merely a wide confidence interval.

3. **“\(q>0.19\) hides a discovery.”** False. `[HA_APPROVED_AGGREGATE]` All
   \(12\) core BH values exceed \(0.19\); the smallest nominal
   \(p=0.03096\). `[DESIGN_DERIVED]` Rank \(1\) in a \(12\)-test family requires
   \(p\le0.00417\) for \(q<0.05\), so the minimum is \(7.43\) times too large.
   More importantly, even a multiplicity-protected monthly coefficient would
   still be the anomaly-association estimand in Section 3, not daily
   triggering or a biological mechanism. BH does not conceal a causal object;
   that object was never estimated.

4. **“Four excluding intervals prove an HF cold mechanism.”** False.
   `[HA_APPROVED_AGGREGATE]` The \(4\)-method concordance belongs to one
   separate monthly association. `[DESIGN_DERIVED; A58]` It neither supplies
   the stacked \(\Delta\) nor changes outcome semantics.

5. **“The missing stroke file will repair identification.”** False for a
   monthly stroke aggregate. It would add another monthly outcome, not daily
   timing, admission cause, an individual risk set, or the cross-outcome test
   already required for CHD and HF.

## 7. What would falsify this thesis

1. **Daily triggering:** a governed HA file with exact event dates for the
   defined first-event outcome, a verified construction dictionary, and enough
   timing detail to fit a daily health model would remove the monthly
   aggregation barrier. A monthly stroke file would not.
2. **M\(|\)D recovery from current grain:** a new method frozen before real
   fitting and shown in an independent synthetic calibration to pass every
   F1.2 gate—Type I, coverage, relative bias, false sign, stress coverage,
   convergence, Hessian, and divergence—would falsify the current
   methods-feasibility conclusion. Partial improvement would not.
3. **Individual or admission-cause causality:** a governed person-level file
   containing event dates, explicit admission cause or principal diagnosis,
   cohort entry and exit, the time-varying at-risk set, and an analysis design
   that closes the relevant causal exchangeability assumptions would replace
   the present ecological estimand. A larger monthly count alone would not.
4. **CHD-hot/HF-cold heterogeneity:** restoration of the governed CHD/HF panels
   matching receipt hashes, followed by the frozen stacked interaction with a
   released `HA_APPROVED_AGGREGATE` estimate of \(\Delta\) and calibrated
   uncertainty, would test A58. It would not by itself establish an individual
   mechanism.
5. **A confirmatory primary:** prospectively frozen exposure, outcome,
   contrast, model, and multiplicity rule tested in new governed outcome data
   could support a confirmatory primary. Re-labelling the already-viewed
   contrasts cannot.

## 8. Gate 3 conclusion

1. Option A—explicitly no confirmatory primary—is not conservative taste. It is
   the direct consequence of the identified object: a post-outcome,
   separate-model monthly anomaly association with first-event depletion.
2. Option B, if used to headline the two nominal contrasts, would silently
   promote that object into daily thermal triggering and differential
   CHD-versus-HF mechanism. Neither the outcome grain, the score equations, the
   failed daily-recovery gate, nor A58 supports that promotion.
3. Deferral can await better data, but it does not license a primary claim from
   the current data. For a current freeze, only Option A states exactly what is
   identified and exactly what is not.

## 9. What must not be claimed

The project must not claim that heat or cold caused a hospitalisation; that an
individual's exposure triggered an event on a particular day or lag; that the
counts are incidence, attack rates, principal-diagnosis CHD/HF, AMI, or stroke;
that CHD has a heat mechanism while HF has a cold mechanism; that a selected SE
method or nominal contrast establishes a discovery; or that the failed M\(|\)D
fit yielded a real daily coefficient. No HA row count, ICD list, admission
meaning, stroke result, or health-model coefficient may be supplied beyond the
governed release.

## 10. In-repo proof sources

1. `outputs/identification_crucible/exposure_residual_variation.csv`
2. `outputs/identification_crucible/calendar_month_support.csv`
3. `outputs/identification_crucible/identification_summary.json`
4. `outputs/identification_crucible/bh_detectability.csv`
5. `outputs/identification_crucible/se_method_discordance.csv`
6. `outputs/release_chd_hf/tables/table2_core_models.csv`
7. `outputs/release_chd_hf/tables/table4_uncertainty_ladder.csv`
8. `outputs/calibration_md/md_calibration_f1_2_decision_report.md`
9. `analysis_plan/final_reanalysis_protocol_2026-08-10.md`
10. `analysis_plan/assumption_ledger.md` (A58)
