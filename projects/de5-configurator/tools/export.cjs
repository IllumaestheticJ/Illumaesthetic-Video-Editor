const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 432, height: 768 } });
  await p.goto('http://localhost:8123/product.html'); await p.waitForTimeout(9000); await p.screenshot({ path: '/home/user/media/work/de5/match/default.png' });
  const d = await p.evaluate(() => {
    const { carGroup, kitGroup, camera, controls } = window.__ewc3d; const out = {};
    for (const [n, g] of [['car', carGroup], ['kit', kitGroup]]) {
      const parts = []; g.updateMatrixWorld(true);
      g.traverse(o => { if (!o.isMesh) return; const geo = o.geometry.clone().applyMatrix4(o.matrixWorld); const pos = Array.from(geo.attributes.position.array).map(v => +v.toFixed(5)); const idx = geo.index ? Array.from(geo.index.array) : null; parts.push({ pos, idx, color: o.material.color ? o.material.color.getHex() : 0 }); });
      out[n] = parts;
    }
    out.cam = { pos: camera.position.toArray(), target: controls.target.toArray(), fov: camera.fov, aspect: camera.aspect };
    return out;
  });
  fs.writeFileSync('/home/user/media/work/de5/match/scene.json', JSON.stringify(d)); console.log(d.car.length, d.kit.length, d.cam);
  await b.close();
})();
