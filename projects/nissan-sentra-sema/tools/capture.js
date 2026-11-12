// Capture article pages as phone-width screenshots for the media barrage.
// usage: node capture.js <out_dir>   (public articles only; social posts come from the user's screen recordings)
const { chromium } = require('playwright');
const out = process.argv[2];
const urls = {
  topgear_ph: 'https://www.topgear.com.ph/news/car-news/nissan-sentra-spec-v-concept-sema-2026-a6941-20261029',
  carscoops: 'https://www.carscoops.com/2299297/nissan-sentra-spec-v-sema-concept/',
  autopian: 'https://www.theautopian.com/it-sure-seems-like-nissan-released-ai-generated-slop-of-its-latest-concept-car/',
  topspeed: 'https://www.topspeed.com/nissan-full-beast-mode-three-concepts/',
  motorweek: 'https://motorweek.org/this-just-in/nissan-sentra-spec-v-is-a-super-cool-sema-concept/',
  tflcar: 'https://tflcar.com/2026/10/nissan-sentra-spec-v-concept-sema-2026/',
  yahoo: 'https://autos.yahoo.com/new-vehicles-and-reviews/articles/garbled-nissan-badge-raises-ai-185100374.html',
  motoringresearch: 'https://www.motoringresearch.com/america-news/sema-show-nissan-sentra-v-spec-concept/',
  auto123: 'https://www.auto123.com/en/news/nissan-sentra-spec-v-concept-sema-2026/74330/',
  motorillustrated: 'https://motorillustrated.com/nissan-sentra-spec-v-concept-sema-2026/200447/',
  autonewsline: 'https://www.autonewsline.com/2026/10/nissan-sentra-spec-v-concept-sema-2026.html',
  pakwheels: 'https://www.pakwheels.com/blog/nissan-sentra-spec-v-300hp-sema-2026/',
};
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  for (const [k, u] of Object.entries(urls)) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await p.waitForTimeout(4000);
      await p.screenshot({ path: `${out}/${k}.png` });
      console.log(k, r && r.status(), (await p.title()).slice(0, 90));
    } catch (e) { console.log(k, 'FAIL', String(e).slice(0, 120)); }
    await p.close();
  }
  await b.close();
})();
