/* Health-economics identification laboratory. SYNTHETIC_THEORY. Not findings. */
(function () {
  const html = htm.bind(React.createElement);
  const e = React.createElement;

  const TABS = [
    ["overview", "Overview"],
    ["HE-01", "HE-01 stock"],
    ["HE-07", "HE-07 SEW"],
    ["HE-08", "HE-08 RTE"],
    ["HE-10", "HE-10 ADR"],
    ["HE-C2-10", "C2 CATD"],
    ["HE-C2-02", "C2 queue"],
    ["HE-C2-PORT", "C2 portfolio"],
    ["failed", "Failed"],
  ];

  const COPY = {
    overview: {
      title: "What this laboratory is",
      body: "A monthly ecological count ratio for first CHD/HF hospitalisation cannot be multiplied into a welfare or hospital-cost object without four silent equalities: renewable stock, pure need, no displacement, constant visibility. Cycle 1 named those equalities, an adversarial audit killed most of them, and three objects survived only as escalation statistics (SEW, RTE, ADR). Cycle 2 mutates the survivors under present bias and daily rationing. Nothing here is a Gate 3 input, a stroke result, or a currency figure.",
    },
    "HE-01": {
      title: "Depleting first-event stock",
      verdict: "KILL (level) / costing caveat (size)",
      body: "Y_t draws down S_t. ns(time,4) may absorb log S_t, in which case θ is a hazard modulation and the objection is bookkeeping. The liability level remains unidentified because S_t is unobserved. Slider: replacement ratio ρ. A 2020 inflow freeze is the adversarial kink.",
    },
    "HE-07": {
      title: "Visibility of the welfare loss",
      verdict: "SURVIVE-TO-ESCALATION",
      body: "Observed elasticity = morbidity elasticity + d log ω / dX. If the admission threshold moves with heat, even a lower-bound reading fails. Statistic: selection-envelope width over a SYNTHETIC grid of threshold movement, plus MNAR and macro-shock stresses.",
    },
    "HE-08": {
      title: "Regime-weighted elasticity",
      verdict: "SURVIVE-TO-ESCALATION",
      body: "Pooled θ is an identifying-variation weighted average. 2020-02 and 2022-02 are both Februaries; 141/145 cold days sit in DJF. Cycle 2 adds decaying household caution versus ratcheted protocol. Slider: true pandemic delta.",
    },
    "HE-10": {
      title: "Monthly mean as a unit-value index",
      verdict: "SURVIVE-TO-ESCALATION",
      body: "Daily g(T) is imposed, never recovered (this is not the failed M|D). ADR = |β_month − β_target| / (0.5 × existing CI width). Cosmetic only if the 95th percentile ADR < 1 under escalation.",
    },
    "HE-C2-10": {
      title: "Truncation composed with aggregation",
      verdict: "Cycle 2 candidate — highest sim priority",
      body: "Daily min(D,K) removes the tail that generates Jensen curvature. The two biases oppose on curvature and agree on slope. Signed CATD can differ by contrast. A small |CATD| inside the cancellation region is a calibration coincidence, not validity.",
    },
    "HE-C2-02": {
      title: "Queue-clearing vs demand (second moment)",
      verdict: "Cycle 2 candidate",
      body: "HE-03 died on the monthly mean. Mild daily truncation barely moves the mean and compresses variance. Detection target: slope of squared Pearson residuals on fitted mean, demand family versus queue family. No bed shadow price is recovered.",
    },
    "HE-C2-PORT": {
      title: "One request, not three",
      verdict: "Analytic ledger — does not ask",
      body: "HE-03, HE-06, and HE-11 died of the same missing cross-section. The unit of request is a bundle priced in integer human asks. This matrix does not assert that cluster files exist.",
    },
    failed: {
      title: "Do not re-walk",
      body: "Simple cost-of-illness, nudges, DLNM AF costing, M|D retune, VSL, QALY-from-counts, DiD warnings, synthetic control, AMI costing, stroke economics, gazetted fees as opportunity cost, Lerner-index cartel, real-options wait with invented volatility.",
    },
  };

  function pill(kind, text) {
    return html`<span className=${"pill " + kind}>${text}</span>`;
  }

  function Dag({ graphId, graphs }) {
    const ref = React.useRef(null);
    React.useEffect(() => {
      const el = ref.current;
      if (!el || !window.d3) return;
      const links = (graphs && graphs[graphId]) || [];
      el.innerHTML = "";
      const width = el.clientWidth || 520;
      const height = 340;
      const svg = d3.select(el).append("svg").attr("viewBox", [0, 0, width, height]);
      const nodesMap = new Map();
      links.forEach((l) => {
        if (!nodesMap.has(l.source)) nodesMap.set(l.source, { id: l.source });
        if (!nodesMap.has(l.target)) nodesMap.set(l.target, { id: l.target });
      });
      const nodes = Array.from(nodesMap.values());
      const simLinks = links.map((d) => ({ source: d.source, target: d.target }));
      const sim = d3
        .forceSimulation(nodes)
        .force("link", d3.forceLink(simLinks).id((d) => d.id).distance(90))
        .force("charge", d3.forceManyBody().strength(-180))
        .force("center", d3.forceCenter(width / 2, height / 2));
      const link = svg
        .append("g")
        .attr("stroke", "rgba(232,239,232,.35)")
        .selectAll("line")
        .data(simLinks)
        .join("line");
      const node = svg
        .append("g")
        .selectAll("g")
        .data(nodes)
        .join("g")
        .call(
          d3
            .drag()
            .on("start", (ev, d) => {
              if (!ev.active) sim.alphaTarget(0.2).restart();
              d.fx = d.x;
              d.fy = d.y;
            })
            .on("drag", (ev, d) => {
              d.fx = ev.x;
              d.fy = ev.y;
            })
            .on("end", (ev, d) => {
              if (!ev.active) sim.alphaTarget(0);
              d.fx = null;
              d.fy = null;
            })
        );
      node.append("circle").attr("r", 8).attr("fill", "#4aa3c7");
      node
        .append("text")
        .text((d) => d.id)
        .attr("x", 12)
        .attr("y", 4)
        .attr("fill", "#e8efe8")
        .attr("font-size", 11)
        .attr("font-family", "Sora, sans-serif");
      sim.on("tick", () => {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);
        node.attr("transform", (d) => `translate(${d.x},${d.y})`);
      });
      return () => sim.stop();
    }, [graphId, graphs]);
    return html`<div className="dag" ref=${ref}></div>`;
  }

  function toyCOI(rho, phi, omega, theta) {
    // Naive COI scale factor if the four equalities fail. Dimensionless.
    const stock = rho;
    const displace = 1 - phi;
    const vis = omega;
    const rr = Math.exp(theta);
    return {
      naive: rr,
      adjusted: rr * stock * displace * vis,
      warning: "Dimensionless illustration only. Not HKD. Not a finding.",
    };
  }

  function App() {
    const [tab, setTab] = React.useState("overview");
    const [dags, setDags] = React.useState(null);
    const [gates, setGates] = React.useState(null);
    const [summary, setSummary] = React.useState(null);
    const [port, setPort] = React.useState(null);
    const [varsigma, setVarsigma] = React.useState(null);
    const [rho, setRho] = React.useState(0.7);
    const [phi, setPhi] = React.useState(0.3);
    const [omega, setOmega] = React.useState(0.2);
    const [theta, setTheta] = React.useState(Math.log(1.07));
    const [u, setU] = React.useState(0.95);
    const [delta, setDelta] = React.useState(Math.log(1.03));

    React.useEffect(() => {
      Promise.all([
        fetch("./dags.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
        fetch("./results.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
        fetch("./port.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
        fetch("./varsigma.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
      ]).then(([dg, res, p, v]) => {
        if (dg) setDags(dg.graphs || dg);
        if (res) {
          setGates(res.gates || res);
          setSummary(res.summary || null);
        }
        if (p) setPort(p);
        if (v) setVarsigma(v);
      });
    }, []);

    const graphId =
      tab === "HE-C2-10" ? "HE-C2-cartel" : tab === "failed" ? null : tab === "overview" ? "HE-10" : tab;
    const copy = COPY[tab] || COPY.overview;
    const toy = toyCOI(rho, phi, omega, theta);

    return html`<div>
      <header className="hero">
        ${pill("synth", "SYNTHETIC_THEORY")}
        ${pill("kill", "not a finding")}
        ${pill("park", "Gate 3 not an input")}
        <h1>Health-economics identification laboratory</h1>
        <p className="sub">
          Laidlaw Heat Project · monthly CHD/HF first-hospitalisation panel, Hong Kong 2013–2023.
          This page visualises <em>what cannot be identified</em> from 132 territory-months.
          Stroke remains undelivered. Daily coefficients remain unadmitted after failed M|D calibration.
          Kimi K3 was not available in the allowed model list; the UI is React + D3 in-repo.
        </p>
      </header>
      <nav className="tabs">
        ${TABS.map(
          ([id, label]) =>
            html`<button className=${tab === id ? "active" : ""} onClick=${() => setTab(id)}>${label}</button>`
        )}
      </nav>
      <main id="main">
        <div className="grid">
          <section className="card">
            <h2>${copy.title}</h2>
            ${copy.verdict ? html`<p>${pill("survive", copy.verdict)}</p>` : null}
            <p className="sub">${copy.body}</p>
            ${graphId && dags ? html`<${Dag} graphId=${graphId} graphs=${dags} />` : html`<p className="muted">DAG loads from dags.json.</p>`}
          </section>
          <aside className="card">
            <h3>Parameter sliders</h3>
            <p className="muted">Client-side illustration of the naive-COI trap. Not the Monte Carlo.</p>
            <label className="slider">Replacement ratio ρ = ${rho.toFixed(2)}
              <input type="range" min="0.4" max="1.2" step="0.01" value=${rho} onInput=${(ev) => setRho(+ev.target.value)} />
            </label>
            <label className="slider">Displacement φ = ${phi.toFixed(2)}
              <input type="range" min="0" max="0.9" step="0.01" value=${phi} onInput=${(ev) => setPhi(+ev.target.value)} />
            </label>
            <label className="slider">Visibility ω = ${omega.toFixed(2)}
              <input type="range" min="0.05" max="1" step="0.01" value=${omega} onInput=${(ev) => setOmega(+ev.target.value)} />
            </label>
            <label className="slider">True log count ratio θ = ${theta.toFixed(3)} (RR ${Math.exp(theta).toFixed(3)})
              <input type="range" min="0" max="0.15" step="0.001" value=${theta} onInput=${(ev) => setTheta(+ev.target.value)} />
            </label>
            <label className="slider">Capacity utilisation u = ${u.toFixed(2)}
              <input type="range" min="0.7" max="1.1" step="0.01" value=${u} onInput=${(ev) => setU(+ev.target.value)} />
            </label>
            <label className="slider">Regime Δ = ${delta.toFixed(3)}
              <input type="range" min="-0.08" max="0.08" step="0.001" value=${delta} onInput=${(ev) => setDelta(+ev.target.value)} />
            </label>
            <p className="stat">${toy.adjusted.toFixed(3)}</p>
            <p className="mono muted">naive RR ${toy.naive.toFixed(3)} × ρ × (1−φ) × ω → adjusted scale. ${toy.warning}</p>
          </aside>
        </div>
        <section className="card">
          <h3>Monte Carlo gates</h3>
          ${gates ? html`<pre className="mono">${JSON.stringify(gates, null, 2)}</pre>` : html`<p className="muted">results.json not present yet. Run <span class="mono">Rscript scripts/48_health_econ_monte_carlo.R</span> then copy gates into docs/health_econ/results.json.</p>`}
          ${varsigma ? html`<p>HKO variance gradient ς = <span class="mono">${Number(varsigma.varsigma).toFixed(4)}</span> (R² ${Number(varsigma.r2).toFixed(2)}; <span class="mono">${varsigma.data_status}</span> climate only).</p>` : null}
        </section>
        ${tab === "HE-C2-PORT" && port ? html`<section className="card">
          <h3>Identification-status matrix</h3>
          <p className="muted">${port.supermodularity}</p>
          <p className="mono">asserts_data_exist: ${String(port.asserts_data_exist)}</p>
        </section>` : null}
        ${summary ? html`<section className="card">
          <h3>Scenario summaries</h3>
          <table>
            <thead><tr><th>Scenario</th><th>H</th><th>n_ok</th><th>stat p50</th><th>stat p95</th><th>size/power</th></tr></thead>
            <tbody>
              ${summary.slice(0, 40).map((row) => html`<tr>
                <td className="mono">${row.scenario}</td>
                <td>${row.hypothesis}</td>
                <td>${row.n_ok}</td>
                <td className="mono">${row.stat_p50}</td>
                <td className="mono">${row.stat_p95}</td>
                <td className="mono">${row.empirical_size_or_power}</td>
              </tr>`)}
            </tbody>
          </table>
        </section>` : null}
      </main>
      <footer>
        Explore mode · monetisation_permitted: false · no stroke coefficients · no daily coefficients ·
        <a href="../../analysis_plan/health_econ/README.md">lab README</a>
      </footer>
    </div>`;
  }

  const root = ReactDOM.createRoot(document.getElementById("root"));
  root.render(e(App));
})();
