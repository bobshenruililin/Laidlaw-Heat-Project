/** 60-second Ig Nobel conductor. Space starts/stops. ?ceremony autoplays. */

export const DURATION = 60;

export const ACTS = [
  {
    id: "title",
    t0: 0,
    t1: 8,
    kicker: "Award sentence",
    caption: "",
  },
  {
    id: "weather",
    t0: 8,
    t1: 16,
    kicker: "Weather, then the file",
    caption: "weather.",
  },
  {
    id: "pool",
    t0: 16,
    t1: 24,
    kicker: "First hospitalisation after first diagnosis",
    caption: "people leave the pool. this is not incidence.",
  },
  {
    id: "glm",
    t0: 24,
    t1: 32,
    kicker: "Equation (1)",
    caption: "one weather variable per fit.",
  },
  {
    id: "daily",
    t0: 32,
    t1: 40,
    kicker: "The extension that did not ship",
    caption: "the clever extension did not earn a number.",
  },
  {
    id: "board",
    t0: 40,
    t1: 50,
    kicker: "Twelve fits · the fence",
    caption: "both q = 0.192. they are not twins.",
  },
  {
    id: "ruler",
    t0: 50,
    t1: 56,
    kicker: "Five is a ruler",
    caption: "a ruler, not a trigger.",
  },
  {
    id: "close",
    t0: 56,
    t1: 60,
    kicker: "Shepherd",
    caption: "please stop, I'm bored.",
  },
];

export function actAt(t) {
  const x = Math.min(Math.max(t, 0), DURATION - 0.001);
  return ACTS.find((a) => x >= a.t0 && x < a.t1) || ACTS[ACTS.length - 1];
}

export function createClock() {
  let running = false;
  let elapsed = 0;
  let last = 0;
  const auto = /[?&]ceremony\b/.test(location.search);
  const actParam = new URLSearchParams(location.search).get("act");
  const jump = ACTS.find((a) => a.id === actParam);
  if (jump) elapsed = jump.t0;

  return {
    get running() {
      return running;
    },
    get elapsed() {
      return elapsed;
    },
    get remaining() {
      return Math.max(0, DURATION - elapsed);
    },
    get act() {
      return actAt(elapsed);
    },
    get done() {
      return elapsed >= DURATION;
    },
    get auto() {
      return auto;
    },
    start() {
      running = true;
      last = performance.now();
    },
    stop() {
      running = false;
    },
    toggle() {
      if (running) this.stop();
      else this.start();
    },
    seek(t) {
      elapsed = Math.min(Math.max(t, 0), DURATION);
    },
    tick(now) {
      if (running && elapsed < DURATION) {
        elapsed = Math.min(DURATION, elapsed + (now - last) / 1000);
      }
      last = now;
      return this.act;
    },
  };
}
