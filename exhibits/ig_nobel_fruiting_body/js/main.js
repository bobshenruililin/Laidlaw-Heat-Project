import * as THREE from "three";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import {
  COUNTS,
  DAILY_REPLICATES,
  EQUATION_TERMS,
  POOL_SPRITES,
  PROVENANCE,
  RESIDUALS,
  SPELL_2018,
  SPRITE_PER_EVENTS,
} from "./data.js";
import { createMycelium } from "./mycelium.js";
import { createAirplanes } from "./airplanes.js";
import { createClock, DURATION } from "./ceremony.js";

const CHD = new THREE.Color("#c56a42");
const HF = new THREE.Color("#4e8f92");
const HOT = new THREE.Color("#e08a4a");
const COLD = new THREE.Color("#8ec8d0");

function $(id) {
  return document.getElementById(id);
}

function createPoints(n, color, size) {
  const pos = new Float32Array(n * 3);
  const seed = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2;
    const r = Math.sqrt(Math.random()) * 3.4;
    pos[i * 3] = Math.cos(a) * r;
    pos[i * 3 + 1] = 0.04 + Math.random() * 0.2;
    pos[i * 3 + 2] = Math.sin(a) * r;
    seed[i] = Math.random();
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aSeed", new THREE.BufferAttribute(seed, 1));
  const mat = new THREE.PointsMaterial({
    color,
    size,
    transparent: true,
    opacity: 0.75,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  });
  return new THREE.Points(geo, mat);
}

function createDailyEngine(n) {
  const pos = new Float32Array(n * 3);
  const vel = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    pos[i * 3] = (i % 25) * 0.09 - 1.1;
    pos[i * 3 + 1] = Math.floor(i / 25) * 0.09 + 0.4;
    pos[i * 3 + 2] = 2.6;
    vel[i * 3] = 0;
    vel[i * 3 + 1] = 0;
    vel[i * 3 + 2] = 0;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(
    geo,
    new THREE.PointsMaterial({
      color: "#f0d9a0",
      size: 0.045,
      transparent: true,
      opacity: 0.9,
      depthWrite: false,
    })
  );
  const frame = new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.BoxGeometry(2.5, 1.8, 0.4)),
    new THREE.LineBasicMaterial({ color: "#6a5840" })
  );
  frame.position.set(0, 1.1, 2.6);
  const group = new THREE.Group();
  group.add(pts, frame);
  group.visible = false;
  return { group, pos, vel, pts, failed: false };
}

function boot() {
  const canvas = $("c");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
  renderer.setClearColor(0x070b10, 1);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x070b10, 0.055);
  const camera = new THREE.PerspectiveCamera(42, 16 / 9, 0.1, 80);
  camera.position.set(0, 4.8, 9.2);

  const hemi = new THREE.HemisphereLight(0xb7c4c8, 0x1a120c, 0.55);
  const key = new THREE.DirectionalLight(0xffe6c8, 0.55);
  key.position.set(4, 8, 3);
  scene.add(hemi, key);

  const spores = createPoints(900, 0xcbb892, 0.035);
  spores.position.y = 0.8;
  scene.add(spores);

  const hotField = createPoints(520, HOT, 0.055);
  const coldField = createPoints(520, COLD, 0.055);
  hotField.visible = false;
  coldField.visible = false;
  scene.add(hotField, coldField);

  const poolChd = createPoints(POOL_SPRITES.chd, CHD, 0.05);
  const poolHf = createPoints(POOL_SPRITES.hf, HF, 0.06);
  poolChd.visible = false;
  poolHf.visible = false;
  scene.add(poolChd, poolHf);

  const mycelium = createMycelium(scene);
  const planes = createAirplanes(scene);
  const daily = createDailyEngine(DAILY_REPLICATES);
  scene.add(daily.group);

  const pointer = new THREE.Vector3(0, 0.2, 0);
  const ray = new THREE.Raycaster();
  const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  const hit = new THREE.Vector3();
  const ndc = new THREE.Vector2();

  function onPointer(e) {
    const r = canvas.getBoundingClientRect();
    ndc.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((e.clientY - r.top) / r.height) * 2 + 1;
    ray.setFromCamera(ndc, camera);
    ray.ray.intersectPlane(plane, hit);
    if (hit) pointer.lerp(hit, 0.35);
  }
  window.addEventListener("pointermove", onPointer);

  let composer = null;
  function layout() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    if (!composer) {
      composer = new EffectComposer(renderer);
      composer.addPass(new RenderPass(scene, camera));
      const bloom = new UnrealBloomPass(new THREE.Vector2(w, h), 0.72, 0.55, 0.18);
      composer.addPass(bloom);
      composer.addPass(new OutputPass());
    }
    composer.setSize(w, h);
  }
  window.addEventListener("resize", layout);
  layout();

  const clock = createClock();
  const hud = {
    kicker: $("kicker"),
    caption: $("caption"),
    title: $("title-b"),
    award: $("award"),
    clock: $("clock-read"),
    ring: $("clock-ring"),
    act: $("act-num"),
    glm: $("glm-panel"),
    board: $("board-panel"),
    ruler: $("ruler-panel"),
    weather: $("weather-line"),
    pool: $("pool-line"),
    daily: $("daily-line"),
    shepherd: $("shepherd"),
    provenance: $("provenance"),
    termNote: $("term-note"),
    rulerInput: $("ruler"),
    rulerOut: $("ruler-out"),
    startBtn: $("start"),
  };

  hud.provenance.textContent = PROVENANCE;
  $("chd-count").textContent = COUNTS.chdLabel;
  $("hf-count").textContent = COUNTS.hfLabel;
  $("month-count").textContent = String(COUNTS.months);
  $("sprite-note").textContent = `each sprite = ${SPRITE_PER_EVENTS} events · ${PROVENANCE}`;
  $("rr-chd").textContent = RESIDUALS.chd_hot_nights.rr;
  $("ci-chd").textContent = `(${RESIDUALS.chd_hot_nights.ci}) · q = ${RESIDUALS.chd_hot_nights.q}`;
  $("note-chd").textContent = RESIDUALS.chd_hot_nights.note;
  $("rr-hf").textContent = RESIDUALS.hf_cold_days.rr;
  $("ci-hf").textContent = `(${RESIDUALS.hf_cold_days.ci}) · q = ${RESIDUALS.hf_cold_days.q}`;
  $("note-hf").textContent = `${RESIDUALS.hf_cold_days.note} Pre-2020: ${RESIDUALS.hf_cold_days.pre2020}.`;
  $("q-fence").textContent = `All twelve q-values exceeded 0.19 · minimum shown q = ${RESIDUALS.chd_hot_nights.q}`;

  const ACT_INDEX = {
    title: 1,
    weather: 2,
    pool: 3,
    glm: 4,
    daily: 5,
    board: 6,
    ruler: 7,
    close: 8,
  };

  function setAct(act) {
    document.body.dataset.act = act.id;
    hud.kicker.textContent = act.kicker;
    hud.caption.textContent = act.caption;
    hud.act.textContent = ACT_INDEX[act.id] + "/8";
    hud.glm.hidden = act.id !== "glm";
    hud.board.hidden = act.id !== "board" && act.id !== "close";
    hud.ruler.hidden = act.id !== "ruler";
    hud.weather.hidden = act.id !== "weather";
    hud.pool.hidden = act.id !== "pool";
    hud.daily.hidden = act.id !== "daily";
    hud.shepherd.hidden = act.id !== "close";
    hud.award.hidden = act.id !== "title";
    hud.title.classList.toggle("quiet", act.id !== "title" && act.id !== "close");
    hotField.visible = act.id === "weather" || act.id === "title";
    coldField.visible = act.id === "weather" || act.id === "title";
    poolChd.visible = act.id === "pool";
    poolHf.visible = act.id === "pool";
    daily.group.visible = act.id === "daily";
    if (act.id === "daily") daily.failed = false;
    if (act.id === "glm") lightTerm(0);
  }

  let lastAct = "";
  function lightTerm(i) {
    document.querySelectorAll("[data-term]").forEach((el, idx) => {
      el.classList.toggle("on", idx === i);
    });
    hud.termNote.textContent = EQUATION_TERMS[i].spoken;
  }
  document.querySelectorAll("[data-term]").forEach((el, idx) => {
    el.addEventListener("click", () => lightTerm(idx));
  });

  function publish(which) {
    mycelium.tryFruit(which);
    const targets = {
      chd: which === "chd" ? mycelium.fruitWorldPos("chd") : null,
      hf: which === "hf" ? mycelium.fruitWorldPos("hf") : null,
    };
    planes.launchAt(targets);
    hud.board.hidden = false;
    hud.caption.textContent = "both q = 0.192. they are not twins.";
  }
  $("publish-chd").addEventListener("click", () => publish("chd"));
  $("publish-hf").addEventListener("click", () => publish("hf"));

  function snapRuler() {
    const v = Number(hud.rulerInput.value);
    const five = v >= 5;
    hud.ruler.hidden = !five && document.body.dataset.act !== "ruler";
    hud.rulerOut.innerHTML = five
      ? `<strong>${SPELL_2018.year}</strong>: ${SPELL_2018.officialHotNights} official hot nights. <strong>${SPELL_2018.daysInFiveNightSpells}</strong> days in spells of five or more consecutive hot nights. I(count/5) is a reporting scale.`
      : `I(count/5) is a reporting scale, not ${v} consecutive night${v === 1 ? "" : "s"}. Drag to 5.`;
    hud.rulerInput.classList.toggle("snap", five);
  }
  hud.rulerInput.addEventListener("input", snapRuler);

  const demo = new URLSearchParams(location.search);
  if (demo.get("nights")) {
    hud.rulerInput.value = demo.get("nights");
  }
  snapRuler();
  if (demo.get("publish") === "chd") setTimeout(() => publish("chd"), 700);
  if (demo.get("publish") === "hf") setTimeout(() => publish("hf"), 700);

  hud.startBtn.addEventListener("click", () => {
    if (clock.done) clock.seek(0);
    clock.toggle();
    hud.startBtn.textContent = clock.running ? "Pause" : "Start 60s";
  });
  window.addEventListener("keydown", (e) => {
    if (e.key === " " && e.target.tagName !== "INPUT") {
      e.preventDefault();
      hud.startBtn.click();
    } else if (e.key >= "1" && e.key <= "8") {
      const t0 = [0, 8, 16, 24, 32, 40, 50, 56][Number(e.key) - 1];
      clock.seek(t0);
    }
  });

  const t0 = performance.now();
  let last = t0;
  let glmStep = 0;
  let glmAcc = 0;

  function driftPoints(obj, mode, t, dt) {
    const arr = obj.geometry.attributes.position.array;
    const seeds = obj.geometry.attributes.aSeed.array;
    for (let i = 0; i < seeds.length; i++) {
      const o = i * 3;
      if (mode === "hot") {
        arr[o + 1] += (0.35 + seeds[i]) * dt;
        if (arr[o + 1] > 4.2) arr[o + 1] = 0.05;
      } else if (mode === "cold") {
        arr[o + 1] -= (0.25 + seeds[i] * 0.4) * dt;
        if (arr[o + 1] < 0.02) arr[o + 1] = 3.6;
      } else if (mode === "pool") {
        arr[o] *= 1 + 0.12 * dt;
        arr[o + 2] *= 1 + 0.12 * dt;
        arr[o + 1] += 0.05 * dt;
        if (Math.hypot(arr[o], arr[o + 2]) > 5.5) {
          const a = seeds[i] * Math.PI * 2;
          arr[o] = Math.cos(a) * 0.2;
          arr[o + 2] = Math.sin(a) * 0.2;
          arr[o + 1] = 0.05;
        }
      } else if (mode === "spore") {
        arr[o] += Math.sin(t * 0.3 + seeds[i] * 10) * 0.15 * dt;
        arr[o + 1] += Math.cos(t * 0.2 + seeds[i] * 8) * 0.1 * dt;
        arr[o + 2] += Math.sin(t * 0.25 + seeds[i] * 6) * 0.15 * dt;
      }
    }
    obj.geometry.attributes.position.needsUpdate = true;
  }

  function stepDaily(dt) {
    const { pos, vel } = daily;
    for (let i = 0; i < DAILY_REPLICATES; i++) {
      const o = i * 3;
      if (!daily.failed) {
        const tx = ((i % 25) / 24) * 2 - 1;
        const ty = tx * 0.6 + 1.1;
        pos[o] += (tx - pos[o]) * 0.8 * dt;
        pos[o + 1] += (ty - pos[o + 1]) * 0.8 * dt;
      } else {
        vel[o + 1] -= 4.5 * dt;
        pos[o] += vel[o] * dt;
        pos[o + 1] += vel[o + 1] * dt;
        pos[o + 2] += vel[o + 2] * dt;
        if (pos[o + 1] < 0.05) {
          pos[o + 1] = 0.05;
          vel[o] *= 0.4;
          vel[o + 1] *= -0.15;
        }
      }
    }
    daily.pts.geometry.attributes.position.needsUpdate = true;
  }

  function frame(now) {
    requestAnimationFrame(frame);
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    const t = (now - t0) / 1000;
    const act = clock.tick(now);
    if (act.id !== lastAct) {
      lastAct = act.id;
      setAct(act);
    }
    const remain = clock.remaining;
    hud.clock.textContent = remain.toFixed(1) + "s";
    const frac = 1 - remain / DURATION;
    hud.ring.style.strokeDashoffset = String((1 - frac) * 113.1);

    if (act.id === "glm") {
      glmAcc += dt;
      if (glmAcc > 2) {
        glmAcc = 0;
        glmStep = (glmStep + 1) % 4;
        lightTerm(glmStep);
      }
    }
    if (act.id === "daily" && clock.elapsed > 35.5) {
      if (!daily.failed) {
        daily.failed = true;
        for (let i = 0; i < DAILY_REPLICATES; i++) {
          daily.vel[i * 3] = (Math.random() - 0.5) * 2.5;
          daily.vel[i * 3 + 1] = Math.random() * 1.2;
          daily.vel[i * 3 + 2] = (Math.random() - 0.5) * 1.2;
        }
      }
    }

    driftPoints(spores, "spore", t, dt);
    if (hotField.visible) driftPoints(hotField, "hot", t, dt);
    if (coldField.visible) driftPoints(coldField, "cold", t, dt);
    if (poolChd.visible) {
      driftPoints(poolChd, "pool", t, dt);
      driftPoints(poolHf, "pool", t, dt);
    }
    if (daily.group.visible) stepDaily(dt);

    const attract = act.id === "board" || act.id === "title" || !clock.running ? 0.95 : 0.35;
    mycelium.update(t, pointer, attract);
    const hits = planes.update(dt);
    if ((hits.chd > 6 || hits.hf > 6) && !mycelium.fruiting.knocked) {
      mycelium.knock();
    }

    const look = act.id === "daily" ? new THREE.Vector3(0, 1.0, 2.2) : new THREE.Vector3(0, 0.3, 0);
    const camHome =
      act.id === "glm"
        ? new THREE.Vector3(0, 3.4, 7.2)
        : act.id === "daily"
          ? new THREE.Vector3(0, 2.6, 6.4)
          : act.id === "pool"
            ? new THREE.Vector3(0, 6.2, 5.5)
            : new THREE.Vector3(0, 4.8, 9.2);
    camera.position.lerp(camHome, 0.04);
    camera.lookAt(look);
    camera.position.x += Math.sin(t * 0.12) * 0.002;

    composer.render();
    hud.startBtn.textContent = clock.done ? "Replay" : clock.running ? "Pause" : "Start 60s";
  }

  setAct(clock.act);
  if (clock.auto) {
    clock.start();
    hud.startBtn.textContent = "Pause";
  }
  requestAnimationFrame(frame);
}

boot();
