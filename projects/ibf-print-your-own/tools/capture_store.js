// Real screen capture of the live store page at phone size. Hides the chat bubble + sticky add-to-cart bar,
// saves one full-page screenshot per gallery slide (the reel composes scroll/slide motion from these).
// node capture_store.js <url> <outdir>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[3] || '.';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await p.goto(process.argv[2], { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(2000);
  const dots = await p.evaluate(() => {
    const sel = ['.flickity-page-dots .dot', '.slick-dots button', 'button[aria-label*="lide"]', '[class*="dot"]'];
    for (const s of sel) { const n = document.querySelectorAll(s); if (n.length >= 2) return [s, n.length]; }
    return null; });
  console.log('dots', JSON.stringify(dots));
  const hide = '#shopify-chat, shopify-chat, inbox-online-store-chat, .sticky-atc, .product-sticky-atc, [class*="sticky-atc"], [class*="StickyAtc"] { display: none !important; }';
  await p.addStyleTag({ content: hide });
  await p.waitForTimeout(500);
  for (let i = 0; i < 4; i++) {
    if (dots && i > 0) { const n = await p.$$(dots[0]); if (n[i]) { await n[i].click({ force: true }); await p.waitForTimeout(1200); } }
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.screenshot({ path: path.join(out, `store_g${i}.png`), fullPage: true });
  }
  await b.close();
})();
