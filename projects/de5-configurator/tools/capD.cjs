// Shot D: configurator 3D view (DE5 + GT wing) full-frame, orbit from the default view to the solved camera of the GT listing photo (v2: Drive photo _DSF3972, 7145x4763; v1 used the listing's rear-quarter-white)
const { chromium } = require('playwright'); const fs = require('fs');
const cam = JSON.parse(fs.readFileSync('/home/user/media/work/de5/match/cam_v2.json'));
const N = +process.argv[2] || 131, OUT = process.argv[3] || '/home/user/media/work/de5/frames/D', STEP = +process.argv[4] || 1;
// photo window (cx, cy, height in photo px; 9:16) at time t (s) relative to the cut; same linear push as shot E
const WIN = { c0: [3320, 2381.5, 4763], c1: [2193, 2381.5, 4763], dur: 82 / 30 };   // v4: sideways slide at constant scale (user hated the zoom); 13.74 photo px/frame at the cut, same as layers.py E
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 });
  await p.goto('http://localhost:8123/product.html'); await p.waitForTimeout(9000);
  await p.addStyleTag({ content: 'canvas{position:fixed!important;left:0;top:0;width:100vw!important;height:100vh!important;z-index:99999}body{overflow:hidden}' });
  await p.evaluate(({ cam, WIN }) => {
    const { THREE, camera, controls, renderer } = window.__ewc3d;
    controls.enabled = false; controls.update = () => {}; renderer.setPixelRatio(2.5); renderer.setSize(432, 768, false);
    camera.matrixAutoUpdate = false; const W = 1080, H = 1920, near = 0.05, far = 100;
    // solved camera (OpenCV) -> world rotation of a three camera
    const th = Math.hypot(...cam.rvec), ax = new THREE.Vector3(...cam.rvec).normalize();
    const Rcv = new THREE.Matrix4().makeRotationAxis(ax, th); const e = Rcv.elements; // column-major; row i = (e[i], e[i+4], e[i+8])
    const row = (i) => new THREE.Vector3(e[i], e[i + 4], e[i + 8]);
    const t = new THREE.Vector3(...cam.tvec); const eyeS = new THREE.Vector3(-row(0).dot(t), -row(1).dot(t), -row(2).dot(t)).set(0,0,0);
    const Rt = new THREE.Matrix3().setFromMatrix4(Rcv).transpose(); eyeS.copy(t).applyMatrix3(Rt).multiplyScalar(-1);
    const qS = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().makeBasis(row(0), row(1).multiplyScalar(-1), row(2).multiplyScalar(-1)));
    const fwdS = row(2); const PWc = 7145, PHc = 4763, f0c = cam.f * PWc / cam.w;
    // look-at point = where the 9:16 window's centre ray meets the car's distance (the window is off the lens axis, so aiming along the axis slid the car off-frame mid-orbit)
    const dirW = row(0).multiplyScalar((WIN.c0[0] - PWc / 2) / f0c).add(row(1).multiplyScalar((WIN.c0[1] - PHc / 2) / f0c)).add(row(2)).normalize();
    const tgtS = eyeS.clone().addScaledVector(dirW, eyeS.distanceTo(new THREE.Vector3(0.6, 0.85, 0)));
    const PW = 7145, PH = 4763, f0 = cam.f * PW / cam.w;
    const qOff = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(eyeS, tgtS, new THREE.Vector3(0, 1, 0))).invert().multiply(qS);
    const pivot = new THREE.Vector3(0.6, 0.85, 0);
    const sph = (v) => { const d = v.clone().sub(pivot); const r = d.length(); return [r, Math.atan2(d.z, d.x), Math.asin(d.y / r)]; };
    const eye0 = new THREE.Vector3(1.2 - 7.85 * 0.82, 0.75 + 2.26 * 0.82, -7.735 * 0.82)   /* v2: default view mirrored to the driver side, so the orbit sweeps ~75 deg round the rear to the photo's passenger-side camera */, tgt0 = new THREE.Vector3(1.2, 0.75, 0);
    const s0 = sph(eye0), s1 = sph(eyeS); if (s0[1] < 0) s0[1] += 2 * Math.PI; if (s1[1] < 0) s1[1] += 2 * Math.PI;
    const K0 = [960 / Math.tan(17.5 * Math.PI / 180), 540, 960];
    const sm = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
    window.__pose = (u, tRel) => {
      const k = Math.max(-1, tRel / WIN.dur), w = WIN.c0.map((a, i) => a + (WIN.c1[i] - a) * k), sc = H / w[2];
      const K1 = [f0 * sc, (PW / 2 - w[0]) * sc + W / 2, (PH / 2 - w[1]) * sc + H / 2];
      const us = sm(u), r = s0[0] * Math.pow(s1[0] / s0[0], us), az = s0[1] + (s1[1] - s0[1]) * us, el = s0[2] + (s1[2] - s0[2]) * us;
      const eye = u >= 1 ? eyeS.clone() : new THREE.Vector3(pivot.x + r * Math.cos(el) * Math.cos(az), pivot.y + r * Math.sin(el), pivot.z + r * Math.cos(el) * Math.sin(az));
      const tg = tgt0.clone().lerp(tgtS, us); const ql = new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(eye, tg, new THREE.Vector3(0, 1, 0)));
      const q = ql.multiply(new THREE.Quaternion().slerp(qOff, sm((u - 0.45) / 0.55)));   // blend in the solved camera's offset from a plain look-at, not its absolute orientation (that pointed away from the car while the eye was still orbiting)
      const kk = sm((u - 0.45) / 0.55),   /* principal point blends with the SAME weight as the slerp to the solved rotation, or the car drifts off-frame mid-orbit */ K = K0.map((a, i) => i === 0 ? a * Math.pow(K1[0] / a, us) : a + (K1[i] - a) * kk);
      camera.matrix.compose(eye, q, new THREE.Vector3(1, 1, 1)); camera.matrixWorld.copy(camera.matrix); camera.matrixWorldInverse.copy(camera.matrix).invert();
      camera.projectionMatrix.set(2 * K[0] / W, 0, 1 - 2 * K[1] / W, 0, 0, 2 * K[0] / H, 2 * K[2] / H - 1, 0, 0, 0, -(far + near) / (far - near), -2 * far * near / (far - near), 0, 0, -1, 0);
      camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
    };
  }, { cam, WIN });
  const HOLD = 12; // frames at the end fully on the solved camera (push only)
  for (let i = 0; i < N; i += STEP) {
    const u = Math.min(1, i / (N - 1 - HOLD)), tRel = (i - N) / 30;
    await p.evaluate(([u, t]) => new Promise((r) => { window.__pose(u, t); requestAnimationFrame(() => requestAnimationFrame(r)); }), [u, tRel]);
    await p.screenshot({ path: `${OUT}/${String(i).padStart(4, '0')}.png` });
  }
  // frame N = the cut frame itself (for the onion check)
  await p.evaluate(([u, t]) => new Promise((r) => { window.__pose(u, t); requestAnimationFrame(() => requestAnimationFrame(r)); }), [1, 0]);
  await p.screenshot({ path: `${OUT}/cut.png` });
  await b.close(); console.log('done');
})();
