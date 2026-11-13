// Phone-width screenshots of real Frontier Ronin coverage (hook + reveal headlines). After nissan-sentra-sema/tools/capture.js.
// usage: node capture.js <out_dir>     (hosts must be on the environment allow-list)
const { chromium } = require('playwright');
const out = process.argv[2];
const urls = {
  motorillustrated_art: 'https://motorillustrated.com/nissan-sema-concepts-frontier-ronin/200781/',
};
(async () => {
  const b = await chromium.launch(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {});
  const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, ignoreHTTPSErrors: false,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  for (const [k, u] of Object.entries(urls)) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
      await p.waitForTimeout(4000);
      await p.screenshot({ path: `${out}/${k}.png` });
      const links = await p.$$eval('a', as => as.map(a => a.href + ' | ' + (a.textContent || '').trim().slice(0, 90)).filter(t => /ronin/i.test(t)).slice(0, 6));
      console.log(k, r && r.status(), (await p.title()).slice(0, 90), JSON.stringify(links));
    } catch (e) { console.log(k, 'FAIL', String(e).slice(0, 160)); }
    await p.close();
  }
  await b.close();
})();
