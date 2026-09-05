import * as THREE from "three";
import { NODES, RESIDUALS } from "./data.js";

const CHD = new THREE.Color("#c56a42");
const HF = new THREE.Color("#4e8f92");
const SPORE = new THREE.Color("#d7c4a3");

function nodePosition(node, spacing = 1.55) {
  const x = (node.ei - 2.5) * spacing;
  const z = (node.oi - 0.5) * 2.15;
  return new THREE.Vector3(x, 0.12, z);
}

function mushroomGeometry() {
  const g = new THREE.Group();
  const stem = new THREE.Mesh(
    new THREE.CylinderGeometry(0.05, 0.08, 0.42, 10),
    new THREE.MeshStandardMaterial({
      color: "#e8d9c4",
      emissive: "#3a2a18",
      roughness: 0.7,
    })
  );
  stem.position.y = 0.21;
  const cap = new THREE.Mesh(
    new THREE.SphereGeometry(0.28, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2),
    new THREE.MeshStandardMaterial({
      color: "#8b3d2a",
      emissive: "#4a1810",
      emissiveIntensity: 0.65,
      roughness: 0.45,
    })
  );
  cap.position.y = 0.42;
  cap.scale.set(1, 0.55, 1);
  g.add(stem, cap);
  g.scale.setScalar(0.001);
  g.userData.fruit = 0;
  return g;
}

function buildHyphae(nodes) {
  const positions = [];
  const seeds = [];
  const colors = [];
  const tmp = new THREE.Color();

  function strand(a, b, k, color) {
    const mid = a.clone().lerp(b, 0.5);
    mid.x += Math.sin(k * 12.1) * 0.35;
    mid.z += Math.cos(k * 9.7) * 0.35;
    mid.y += 0.15 + 0.2 * Math.abs(Math.sin(k * 4.0));
    const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
    const pts = curve.getPoints(10);
    for (let i = 0; i < pts.length - 1; i++) {
      positions.push(pts[i].x, pts[i].y, pts[i].z, pts[i + 1].x, pts[i + 1].y, pts[i + 1].z);
      seeds.push(k + i * 0.01, k + i * 0.01 + 0.5);
      colors.push(color.r, color.g, color.b, color.r, color.g, color.b);
    }
  }

  nodes.forEach((n, i) => {
    const p = n.position;
    const col = n.outcome === "CHD" ? CHD : HF;
    for (let k = 0; k < 18; k++) {
      const end = p.clone();
      const ang = (k / 18) * Math.PI * 2 + i * 0.2;
      end.x += Math.cos(ang) * (0.35 + (k % 5) * 0.12);
      end.z += Math.sin(ang) * (0.35 + (k % 5) * 0.12);
      end.y = -0.02;
      strand(p, end, i + k * 0.17, col);
    }
    const right = nodes[i + 1];
    if (right && right.oi === n.oi) strand(p, right.position, i * 1.3, tmp.copy(col).lerp(SPORE, 0.35));
    const down = nodes[i + 6];
    if (down) strand(p, down.position, i * 2.1, SPORE);
  });

  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute("aSeed", new THREE.Float32BufferAttribute(seeds, 1));
  geo.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
  return geo;
}

const HYPHA_VERT = /* glsl */ `
uniform float uTime;
uniform vec3 uPointer;
uniform float uAttract;
attribute float aSeed;
attribute vec3 color;
varying vec3 vColor;
varying float vGlow;
void main() {
  vColor = color;
  vec3 p = position;
  vec3 ptr = uPointer;
  float d = length(p.xz - ptr.xz);
  float fall = exp(-d * d * 0.12);
  vec3 dir = normalize(ptr - p + vec3(0.0001, 0.0, 0.0001));
  p += dir * uAttract * fall * (0.35 + 0.65 * sin(uTime * 2.2 + aSeed * 6.283));
  p.y += 0.07 * sin(uTime * 1.6 + aSeed * 9.1) * (0.3 + fall);
  vGlow = 0.25 + 0.75 * fall;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}
`;

const HYPHA_FRAG = /* glsl */ `
varying vec3 vColor;
varying float vGlow;
void main() {
  gl_FragColor = vec4(vColor * (0.55 + 0.9 * vGlow), 0.22 + 0.55 * vGlow);
}
`;

export function createMycelium(scene) {
  const group = new THREE.Group();
  group.name = "mycelium";

  const nodes = NODES.map((n) => {
    const position = nodePosition(n);
    const color = n.outcome === "CHD" ? CHD : HF;
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(n.residual ? 0.16 : 0.11, 18, 18),
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: n.residual ? 1.1 : 0.55,
        roughness: 0.35,
        metalness: 0.05,
      })
    );
    mesh.position.copy(position);
    mesh.userData = { ...n, position };
    group.add(mesh);
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(n.residual ? 0.22 : 0.16, 0.008, 8, 24),
      new THREE.MeshBasicMaterial({ color: "#e8d9c4", transparent: true, opacity: 0.35 })
    );
    ring.rotation.x = Math.PI / 2;
    ring.position.copy(position);
    group.add(ring);
    return { ...n, position, mesh, fruit: n.residual ? mushroomGeometry() : null };
  });

  nodes.forEach((n) => {
    if (n.fruit) {
      n.fruit.position.copy(n.position);
      group.add(n.fruit);
    }
  });

  const hyphaGeo = buildHyphae(nodes);
  const hyphaMat = new THREE.ShaderMaterial({
    uniforms: {
      uTime: { value: 0 },
      uPointer: { value: new THREE.Vector3(0, 0.2, 0) },
      uAttract: { value: 0.85 },
    },
    vertexShader: HYPHA_VERT,
    fragmentShader: HYPHA_FRAG,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexColors: true,
  });
  const hyphae = new THREE.LineSegments(hyphaGeo, hyphaMat);
  group.add(hyphae);
  const hyphaLit = new THREE.LineSegments(
    hyphaGeo.clone(),
    new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.45,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    })
  );
  group.add(hyphaLit);

  const substrate = new THREE.Mesh(
    new THREE.CircleGeometry(7.2, 64),
    new THREE.MeshStandardMaterial({
      color: "#0c1412",
      roughness: 0.95,
      metalness: 0,
      emissive: "#08110e",
    })
  );
  substrate.rotation.x = -Math.PI / 2;
  substrate.position.y = -0.04;
  group.add(substrate);

  scene.add(group);

  const fruiting = { chd: 0, hf: 0, knocked: false };

  function fruitOf(which) {
    const id = which === "chd" ? RESIDUALS.chd_hot_nights.id : RESIDUALS.hf_cold_days.id;
    return nodes.find((n) => n.id === id);
  }

  return {
    group,
    nodes,
    uniforms: hyphaMat.uniforms,
    fruiting,
    fruitWorldPos(which) {
      const n = fruitOf(which);
      return n ? n.position.clone() : new THREE.Vector3();
    },
    tryFruit(which) {
      fruiting[which] = 1;
      fruiting.knocked = false;
      const n = fruitOf(which);
      if (n?.fruit) n.fruit.userData.fruit = 1;
    },
    knock() {
      fruiting.knocked = true;
      fruiting.chd = 0;
      fruiting.hf = 0;
    },
    update(t, pointer, attract) {
      hyphaMat.uniforms.uTime.value = t;
      hyphaMat.uniforms.uPointer.value.copy(pointer);
      hyphaMat.uniforms.uAttract.value = attract;
      nodes.forEach((n) => {
        const s = 1 + 0.06 * Math.sin(t * 2.4 + n.ei);
        n.mesh.scale.setScalar(s);
        if (n.fruit) {
          const want = n.fruit.userData.fruit || 0;
          if (fruiting.knocked) n.fruit.userData.fruit = Math.max(0, want - 0.08);
          const f = n.fruit.userData.fruit;
          const sc = THREE.MathUtils.lerp(0.001, 1.15, f);
          n.fruit.scale.setScalar(sc);
          n.fruit.rotation.y = t * 0.4;
        }
      });
    },
  };
}
