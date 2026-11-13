// Capture the mobile listing page for the CTA (lessons: iPhone 14 Pro UA, viewport 393x699 @3x = 1179x2097,
// hide only the 360 viewer's "Drag to rotate" hint, span.ia-spin__hint).
//   NODE_PATH=$(npm root -g) node capture_listing.js <url> <out.png> [info.json] [extra,css,selectors,to,hide]
// The extra selectors are for a SOLVE-ONLY capture (view buttons cover the car's roof); the CTA uses the plain capture.
const { chromium } = require('playwright');
const fs = require('fs');
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) ' +
  'Version/16.0 Mobile/15E148 Safari/604.1';
(async () => {
  const [url, out, infoPath, extra] = process.argv.slice(2);
  const b = await chromium.launch();
  const ctx = await b.newContext({ userAgent: UA, viewport: { width: 393, height: 699 }, deviceScaleFactor: 3,
    isMobile: true, hasTouch: true });
  const pg = await ctx.newPage();
  await pg.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
  try { await pg.waitForLoadState('networkidle', { timeout: 45000 }); } catch (e) { console.log('networkidle timeout'); }
  await pg.waitForTimeout(4000);
  const n = await pg.evaluate(() => { const h = document.querySelectorAll('span.ia-spin__hint');
    h.forEach(e => { e.style.visibility = 'hidden'; }); return h.length; });
  const info = await pg.evaluate(() => { const q = s => [...document.querySelectorAll(s)].map(e => {
      const r = e.getBoundingClientRect();
      return { cls: String(e.className), tag: e.tagName, x: r.x, y: r.y, w: r.width, h: r.height, src: e.currentSrc || e.src || null }; });
    return { title: document.title, h1: (document.querySelector('h1') || {}).innerText, url: location.href, spin: q('[class*="ia-spin"]') }; });
  info.hint_hidden = n;
  if (extra) await pg.evaluate(sel => document.querySelectorAll(sel).forEach(e => { e.style.visibility = 'hidden'; }), extra);
  await pg.screenshot({ path: out });
  if (infoPath) fs.writeFileSync(infoPath, JSON.stringify(info, null, 1));
  console.log(JSON.stringify(info, null, 1).slice(0, 5000));
  await b.close();
})();
