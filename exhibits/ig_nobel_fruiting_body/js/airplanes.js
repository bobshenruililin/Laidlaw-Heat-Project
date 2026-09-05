import * as THREE from "three";

export function createDartGeometry() {
  const geo = new THREE.BufferGeometry();
  const p = new Float32Array([
    0.55, 0.0, 0.0, -0.32, 0.02, 0.34, -0.12, 0.0, 0.0, 0.55, 0.0, 0.0, -0.12, 0.0, 0.0, -0.32,
    0.02, -0.34, 0.55, 0.0, 0.0, -0.18, -0.07, 0.0, -0.12, 0.0, 0.0,
  ]);
  geo.setAttribute("position", new THREE.BufferAttribute(p, 3));
  geo.computeVertexNormals();
  return geo;
}

export function createAirplanes(scene, maxCount = 160) {
  const geo = createDartGeometry();
  const mat = new THREE.MeshStandardMaterial({
    color: "#f4f0e6",
    emissive: "#9aa7b0",
    emissiveIntensity: 0.35,
    roughness: 0.55,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.InstancedMesh(geo, mat, maxCount);
  mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  mesh.count = 0;
  scene.add(mesh);

  const dummy = new THREE.Object3D();
  const planes = [];

  function spawn(origin, target, n = 36, kind = "chd") {
    for (let i = 0; i < n && planes.length < maxCount; i++) {
      const pos = origin.clone().add(
        new THREE.Vector3((Math.random() - 0.5) * 2.5, 1.2 + Math.random() * 2.2, (Math.random() - 0.5) * 2.5)
      );
      const vel = target.clone().sub(pos).normalize().multiplyScalar(3.2 + Math.random() * 2.4);
      vel.y += 0.4;
      planes.push({
        pos,
        vel,
        alive: true,
        hit: false,
        spin: (Math.random() - 0.5) * 8,
        target: target.clone(),
        kind,
      });
    }
  }

  const hits = { chd: 0, hf: 0 };

  return {
    mesh,
    hits,
    spawn,
    launchAt(targets) {
      hits.chd = 0;
      hits.hf = 0;
      const cam = new THREE.Vector3(0, 4.2, 6.5);
      if (targets.chd) spawn(cam, targets.chd, 48, "chd");
      if (targets.hf) spawn(cam, targets.hf, 48, "hf");
    },
    update(dt) {
      let live = 0;
      const g = 2.8;
      for (const p of planes) {
        if (!p.alive) continue;
        p.vel.y -= g * dt * 0.35;
        const lift = p.vel.length() * 0.12;
        p.vel.y += lift * dt;
        p.vel.multiplyScalar(1 - 0.35 * dt);
        p.pos.addScaledVector(p.vel, dt);
        const d = p.pos.distanceTo(p.target);
        if (d < 0.55 && !p.hit) {
          p.hit = true;
          hits[p.kind] += 1;
          p.vel.add(new THREE.Vector3((Math.random() - 0.5) * 4, 2, (Math.random() - 0.5) * 4));
        }
        if (p.pos.y < -1.5 || p.pos.length() > 18) p.alive = false;
        dummy.position.copy(p.pos);
        dummy.lookAt(p.pos.clone().add(p.vel));
        dummy.rotateZ(p.spin * 0.2);
        dummy.scale.setScalar(0.85);
        dummy.updateMatrix();
        mesh.setMatrixAt(live, dummy.matrix);
        live += 1;
      }
      mesh.count = live;
      mesh.instanceMatrix.needsUpdate = true;
      return hits;
    },
    clear() {
      planes.length = 0;
      mesh.count = 0;
      hits.chd = 0;
      hits.hf = 0;
    },
  };
}
