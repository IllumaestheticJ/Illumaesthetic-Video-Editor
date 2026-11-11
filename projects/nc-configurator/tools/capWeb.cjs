// Shots A (home), B (product page), C (embedded configurator + add to cart) on the live site, frame-stepped at 30 fps.
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = '/home/user/media/work/nc/frames', ONLY = process.argv[2] || 'ABC', STEP = +process.argv[3] || 1;
const ease = (x) => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1' });
  const p = await ctx.newPage();
  const prep = async (url) => {
    await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(5000);
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 600) { await p.evaluate((y) => window.scrollTo(0, y), y); await p.waitForTimeout(300); }
    await p.waitForTimeout(2500); await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(800);
    await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}#__tap{position:fixed;z-index:2147483647;width:64px;height:64px;margin:-32px 0 0 -32px;border-radius:50%;background:rgba(40,40,40,.28);border:2px solid rgba(255,255,255,.85);box-shadow:0 0 0 1px rgba(0,0,0,.25);pointer-events:none;opacity:0}' });
    await p.evaluate(() => { const d = document.createElement('div'); d.id = '__tap'; document.body.append(d); window.__anim = new Map();
      window.__step = (ms) => { for (const a of document.getAnimations()) { try { if (!window.__anim.has(a)) { a.pause(); window.__anim.set(a, a.currentTime || 0); } const t = window.__anim.get(a) + ms; window.__anim.set(a, t); a.currentTime = t; } catch (e) {} } };
      window.__tap = (x, y, k) => { d.style.left = x + 'px'; d.style.top = y + 'px'; d.style.opacity = k <= 0 ? 0 : Math.min(1, k * 3) * (k > 0.7 ? (1 - k) / 0.3 : 1); d.style.transform = `scale(${0.6 + 0.5 * k})`; }; });
  };
  // run a shot: acts = {frame: async fn}; scroll(i) -> y or null; taps = [[frame, x, y]] (indicator shows for 9 frames from frame-3)
  const shot = async (name, N, { scroll, acts = {}, taps = [] }) => {
    fs.mkdirSync(`${OUT}/${name}`, { recursive: true });
    for (let i = 0; i < N; i++) {
      if (acts[i]) await acts[i]();
      const y = scroll ? scroll(i) : null; if (y != null) await p.evaluate((y) => window.scrollTo(0, y), y);
      let tp = [0, 0, 0]; for (const [f, x, yy] of taps) if (i >= f - 4 && i < f + 7) tp = [x, yy, (i - (f - 4) + 1) / 11];
      await p.evaluate(([tp]) => new Promise((r) => { window.__tap(...tp); window.__step(1000 / 30); requestAnimationFrame(() => requestAnimationFrame(r)); }), [tp]);
      if (i % STEP === 0) await p.screenshot({ path: `${OUT}/${name}/${String(i).padStart(4, '0')}.png` });
    }
    console.log(name, 'done');
  };
  const center = async (loc) => { const r = await loc.boundingBox(); return [r.x + r.width / 2, r.y + r.height / 2]; };

  if (ONLY.includes('A')) { // home: scroll to the wing configurator, pick Mazda > MX-5 Miata NC
    await prep('https://epsilon.plus/');
    const root = p.locator('[data-epsilon-wing-configurator]'); const sels = root.locator('select');
    await p.evaluate(() => window.scrollTo(0, 800)); await p.waitForTimeout(600);
    const m = await center(sels.nth(1)); await p.evaluate(() => window.scrollTo(0, 0));
    await shot('A', 83, { scroll: (i) => 800 * ease((i - 2) / 34), taps: [[46, m[0], m[1]]],
      acts: { 47: async () => { await sels.nth(1).selectOption({ label: 'MX-5 Miata NC (2006–2015) · 3D Scan' }); await p.waitForTimeout(3500); } } });
  }
  if (ONLY.includes('B') || ONLY.includes('C')) {
    await prep('https://epsilon.plus/products/tc-wing-mazda-miata-nc-bases-uprights');
    if (ONLY.includes('B')) await shot('B', 63, { scroll: (i) => 560 * ease((i - 14) / 26) });
    if (ONLY.includes('C')) {
      const root = p.locator('[data-epsilon-wing-configurator]');
      await p.evaluate(() => window.scrollTo(0, 2230)); await p.waitForTimeout(3500);
      const cfg = await center(root.getByText('CONFIGURE').first()); const atc = await center(p.locator('button:has-text("Add to cart"):visible').last());
      await p.evaluate(() => window.scrollTo(0, 560)); await p.waitForTimeout(300);
      let co = [300, 715];
      await shot('C', 105, { scroll: (i) => i < 60 ? 560 + (2230 - 560) * ease(i / 16) : null, taps: [[28, cfg[0], cfg[1]], [62, atc[0], atc[1]], [92, 105, 715]],
        acts: { 29: async () => { await root.getByText('CONFIGURE').first().click(); await p.waitForTimeout(300); },
          44: async () => { await root.locator('.ewc-drawer-body').evaluate((e) => { e.__y = 0; }); },
          63: async () => { await p.locator('button:has-text("Add to cart"):visible').last().click(); await p.waitForTimeout(3000); } } });
    }
  }
  await b.close();
})();
