// Capture QX80 R-Spec press articles as phone-width screenshots for "press coverage" shots.
// usage: node capture.js <out_dir> [key ...]   (public articles only; blocked/challenge pages are skipped, never bypassed)
// Writes <out>/<key>_page.png (first screen) and <out>/<key>_headline.png (masthead + H1 + hero), plus <out>/<key>.json.
const { chromium } = require('playwright');
const fs = require('fs');
const out = process.argv[2];
const only = process.argv.slice(3);
const urls = {
  motor1: 'https://www.motor1.com/news/777089/infiniti-qx80-r-spec-1000-hp-sema/',
  thedrive: 'https://www.thedrive.com/news/infiniti-imagined-a-1000-hp-nissan-gt-r-suv-with-midnight-purple-paint-for-sema',
  carscoops: 'https://www.carscoops.com/?p=3308224',
  motorillustrated: 'https://motorillustrated.com/infiniti-qx80-r-spec-1000-hp-gt-r-engine-sema-2025/166518/',
  gearjunkie: 'https://gearjunkie.com/motors/infiniti-qx80-r-spec-reveal',
  drifted: 'https://www.drifted.com/infiniti-unveils-1000-hp-qx80-r-spec-as-a-gigantic-tribute-to-the-gt-r/',
  infinitinews: 'https://usa.infinitinews.com/en-US/releases/luxury-and-adrenaline-infiniti-qx80-r-spec-build-commands-respect-with-gt-r-engine-capable-of-1000-horsepower',
  dupontregistry: 'https://news.dupontregistry.com/blogs/infiniti/infiniti-1000hp-qx80-r-spec',
  gentlemanracer: 'https://thegentlemanracer.com/2025/10/qx80-r-spec/',
  autoguide: 'https://cdn-fastly.autoguide.com/auto/manufacturers/infiniti/infiniti-gives-the-qx80-an-engine-from-the-nissan-gt-r-44626747',
};
const extra = process.env.EXTRA_URLS ? JSON.parse(process.env.EXTRA_URLS) : {};
Object.assign(urls, extra);
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1';
const CHALLENGE = /just a moment|attention required|verify you are human|are you a robot|access denied|captcha|checking your browser|request blocked|forbidden/i;

async function dismiss(p) {
  // click obvious consent / close buttons (harmless DOM interaction)
  for (const f of p.frames()) {
    try {
      await f.evaluate(() => {
        const rx = /^(accept( all)?( cookies)?|i accept|agree|i agree|got it|ok|okay|allow all|continue|close|no thanks|×|✕|x)$/i;
        for (const el of document.querySelectorAll('button, a[role=button], [role=button], .close, [aria-label*="lose"]')) {
          const t = (el.innerText || el.getAttribute('aria-label') || '').trim();
          if (rx.test(t) || /^close/i.test(el.getAttribute('aria-label') || '')) { try { el.click(); } catch (e) {} }
        }
      });
    } catch (e) {}
  }
  await p.waitForTimeout(800);
  // hide remaining fixed/sticky overlays that are not the site header, plus common ad/consent containers
  await p.evaluate(() => {
    const css = document.createElement('style');
    css.textContent = `#onetrust-banner-sdk,#onetrust-consent-sdk,.fc-consent-root,#didomi-host,.qc-cmp2-container,#sp_message_container,
      [id^="sp_message"],.cookie-banner,#cookie-banner,.cc-window,#CybotCookiebotDialog,.truste_overlay,#truste-consent-track,
      iframe[id^="google_ads"],.adhesion,.ad-sticky,[class*="sticky-ad"],[id*="sticky-ad"],[class*="StickyAd"],.bottom-ad,
      [class*="newsletter-modal"],[class*="Modal"][class*="overlay"] {display:none!important}
      html,body{overflow:auto!important}`;
    document.head.appendChild(css);
    for (const el of document.querySelectorAll('body *')) {
      const s = getComputedStyle(el);
      if (s.position !== 'fixed') continue;
      const r = el.getBoundingClientRect();
      const isHeader = r.top <= 2 && r.height < 140 && el.querySelector('img, svg, a');
      if (isHeader) continue;
      if (r.height > 40 || r.width > 200) el.style.setProperty('display', 'none', 'important');
    }
  });
  await p.waitForTimeout(400);
}

async function one(ctx, k, u) {
  const rec = { key: k, url: u };
  const p = await ctx.newPage();
  try {
    const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await p.waitForTimeout(4000);
    rec.final_url = p.url();
    rec.http = r && r.status();
    rec.title = await p.title();
    const bodyText = (await p.evaluate(() => (document.body && document.body.innerText || '').slice(0, 3000))).trim();
    if ((rec.http && rec.http >= 400) || CHALLENGE.test(rec.title) || (bodyText.length < 1500 && CHALLENGE.test(bodyText))) {
      rec.status = 'blocked';
      rec.note = `http ${rec.http}; title "${rec.title.slice(0, 80)}"`;
      await p.screenshot({ path: `${out}/${k}_BLOCKED.png` });
      return rec;
    }
    await dismiss(p);
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.waitForTimeout(500);
    await p.screenshot({ path: `${out}/${k}_page.png` });
    // headline region
    const box = await p.evaluate(() => {
      const hs = [...document.querySelectorAll('h1')].filter(h => {
        const r = h.getBoundingClientRect(); return r.width > 50 && r.height > 10 && (h.innerText || '').trim().length > 15;
      });
      if (!hs.length) return null;
      const h = hs[0];
      const hr = h.getBoundingClientRect();
      const absTop = hr.top + window.scrollY;
      return { absTop, text: h.innerText.trim().replace(/\s+/g, ' ') };
    });
    if (!box) { rec.status = 'rejected'; rec.note = 'no h1 found'; return rec; }
    rec.headline = box.text;
    const scrollY = Math.max(0, box.absTop - 120);
    await p.evaluate(y => window.scrollTo(0, y), scrollY);
    await p.waitForTimeout(1800);
    await dismiss(p);
    const clip = await p.evaluate(() => {
      const h = [...document.querySelectorAll('h1')].find(h => (h.innerText || '').trim().length > 15 && h.getBoundingClientRect().width > 50);
      const hr = h.getBoundingClientRect();
      const top = Math.max(0, hr.top - 120);
      let bottom = hr.bottom + 260;
      const imgs = [...document.querySelectorAll('img, picture, video')].map(i => i.getBoundingClientRect())
        .filter(r => r.width > 300 && r.height > 150 && r.top >= hr.top - 5 && r.top < hr.bottom + 600);
      if (imgs.length) bottom = imgs[0].bottom + 8;
      bottom = Math.min(bottom, top + 900, window.innerHeight);
      return { x: 0, y: top, width: window.innerWidth, height: Math.max(100, bottom - top) };
    });
    await p.screenshot({ path: `${out}/${k}_headline.png`, clip });
    rec.page_png = `${out}/${k}_page.png`;
    rec.headline_png = `${out}/${k}_headline.png`;
    rec.status = 'ok';
  } catch (e) {
    rec.status = 'blocked'; rec.note = 'load failed: ' + String(e).slice(0, 140);
  } finally {
    await p.close();
  }
  return rec;
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: UA });
  for (const [k, u] of Object.entries(urls)) {
    if (only.length && !only.includes(k)) continue;
    const rec = await one(ctx, k, u);
    fs.writeFileSync(`${out}/${k}.json`, JSON.stringify(rec, null, 2));
    console.log(k, rec.status, rec.http, (rec.headline || rec.note || '').slice(0, 100));
  }
  await b.close();
})();
