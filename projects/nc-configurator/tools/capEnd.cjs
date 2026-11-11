// End card: Epsilon+ logo (site header asset) on the configurator's grey, 90 frames with a slow 4 % push
const { chromium } = require('playwright'); const fs = require('fs'); const OUT = '/home/user/media/work/nc/frames/H';
(async () => { fs.mkdirSync(OUT, { recursive: true }); const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 }); await p.goto('http://localhost:8123/endcard.html'); await p.waitForTimeout(800);
  for (let i = 0; i < 90; i++) { await p.evaluate((i) => { const k = Math.min(1, i / 8); document.getElementById('c').style.transform = `translateY(-6%) scale(${0.97 + 0.04 * i / 89 + 0.03 * (1 - (1 - k) ** 3) - 0.03})`; document.getElementById('c').style.opacity = k; }, i);
    await p.screenshot({ path: `${OUT}/${String(i).padStart(4, '0')}.png` }); }
  await b.close(); })();
