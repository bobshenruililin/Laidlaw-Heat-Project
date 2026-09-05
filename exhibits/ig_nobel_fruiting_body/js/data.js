/** Locked REAL constants only. Do not invent q-values for the other ten fits. */
export const PROVENANCE = "REAL";

export const TITLE_B =
  "Hot nights rose. Cold days stayed. The first heart admission did not settle the argument.";

export const AWARD =
  "for demonstrating, with 156,156 first heart admissions and twelve mycelial fits, that a confirmatory mushroom still will not fruit when every q exceeds 0.19.";

export const COUNTS = {
  chd: 156156,
  hf: 29681,
  months: 132,
  chdLabel: "156,156",
  hfLabel: "29,681",
};

export const Q_FENCE = 0.19;
export const Q_MIN_DISPLAY = "0.192";

export const RESIDUALS = {
  chd_hot_nights: {
    id: "CHD·Hot nights",
    rr: "1.022",
    ci: "1.002–1.042",
    q: "0.192",
    note: "SE-fragile. Pre-2020 includes 1.",
  },
  hf_cold_days: {
    id: "HF·Cold days",
    rr: "1.073",
    ci: "1.006–1.144",
    q: "0.192",
    pre2020: "1.113 (1.053–1.176)",
    note: "More coherent. Pre-2020 excludes 1.",
  },
};

export const SPELL_2018 = {
  year: 2018,
  officialHotNights: 26,
  daysInFiveNightSpells: 0,
};

export const DAILY_REPLICATES = 500;

export const EXPOSURES = [
  "Tmean",
  "Tmax",
  "Tmin",
  "Hot nights",
  "Very hot days",
  "Cold days",
];

export const OUTCOMES = ["CHD", "HF"];

export const NODES = OUTCOMES.flatMap((outcome, oi) =>
  EXPOSURES.map((exposure, ei) => {
    const id = `${outcome}·${exposure}`;
    const residual =
      id === RESIDUALS.chd_hot_nights.id || id === RESIDUALS.hf_cold_days.id;
    return {
      id,
      outcome,
      exposure,
      oi,
      ei,
      residual,
      qDisplay: residual ? "0.192" : "> 0.19",
      provenance: PROVENANCE,
    };
  })
);

export const EQUATION_LATEX =
  "\\log \\mathrm{E}(Y_t) = \\log(d_t) + \\alpha + \\beta X_t + \\sum_{m=2}^{12} \\gamma_m I(\\mathrm{month}_t = m) + s(t; 4~\\mathrm{df})";

export const EQUATION_TERMS = [
  { id: "offset", label: "offset log(d_t)", spoken: "days in the month, not person-time" },
  { id: "month", label: "month dummies", spoken: "season, not weather" },
  { id: "spline", label: "s(t; 4 df)", spoken: "slow drift, not a heatwave" },
  { id: "x", label: "one X_t", spoken: "one weather variable per fit" },
];

export const SPRITE_PER_EVENTS = 100;
export const POOL_SPRITES = {
  chd: Math.round(COUNTS.chd / SPRITE_PER_EVENTS),
  hf: Math.round(COUNTS.hf / SPRITE_PER_EVENTS),
};

export const NOT_A_SUBMISSION =
  "Ceremony chrome. Not an Ig Nobel submission. Not a win. Identification theatre.";
