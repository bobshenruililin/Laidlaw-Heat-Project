# Health-economics identification laboratory

Explore-mode layer. **Not a paper. Not a costing. Not a Gate 3 input.**

| File | Role |
|---|---|
| `paradigm_registry.yml` | Anti-convergence registry (Cycle 1) |
| `cycle1_hypotheses.md` | Opus 5 divergent portfolio HE-01–HE-12 |
| `cycle1_structural_equations.md` | GPT-5.6 implementable DGPs |
| `cycle1_adversarial_audit.md` | GPT-5.6 hostile referee |
| `cycle2_mutations.md` | Time-inconsistency + HA rationing mutations |
| `failed_hypotheses.md` | Do-not-repeat list |
| `dags.json` | DAG adjacency for the UI |
| `engine_state.md` | Checkpoint log |

Runnable:

```bash
python3 scripts/48b_health_econ_theory_helpers.py
HE_MC_SCENARIOS=smoke HE_MC_REPS=8 python3 scripts/48_health_econ_monte_carlo.py
HE_MC_SCENARIOS=all HE_MC_REPS=200 python3 scripts/48_health_econ_monte_carlo.py
python3 scripts/48_health_econ_mc_checks.py
# Optional MASS::glm.nb twin if Rscript is available:
HE_MC_SCENARIOS=smoke HE_MC_REPS=8 Rscript scripts/48_health_econ_monte_carlo.R
```

UI: [`docs/health_econ/index.html`](../../docs/health_econ/index.html)

Kimi K3 was requested for the UI and is **not** in the allowed subagent model list; the dashboard is implemented in-repo with React + D3 from CDN.
