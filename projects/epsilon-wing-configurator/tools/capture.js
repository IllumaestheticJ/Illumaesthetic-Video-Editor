// Frame-stepped screen capture of the Epsilon+ wing configurator (live site) for the 9:16 reel.
// Playwright fake clock: every output frame = clock.runFor(1000/30) + one screenshot, so app animations play at true speed
// however slow the screenshot is. A drawn cursor (DOM overlay, pointer-events none) shows every click/drag.
//   node capture.js <shot> [--dry]      (needs require('playwright'); run from a dir where it resolves)
// Output: /home/user/media/epsilon-wing-configurator/cap/<shot>/f_00000.jpg + meta.json (clip + panes for compose.py)
// Never clicks "Send quote request" / "Send report" (outward-facing). "Save spec" only stores in localStorage.
const { chromium } = require('playwright');
const fs = require('fs');
const ROOT = '/home/user/media/epsilon-wing-configurator/cap/';
const URL = 'https://epsilon.plus/pages/wing-configurator';
const FPS = 30;
const DRY = process.argv.includes('--dry');
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

class Cap {
  constructor(name, layout) { this.name = name; this.layout = layout; this.n = 0; this.cur = null; this.dir = ROOT + name + '/'; }
  async open() {
    const vp = this.layout === 'portrait' ? { width: 540, height: 960 } : { width: 1600, height: 1000 };
    this.dpr = this.layout === 'portrait' ? 2.5 : 3;
    this.b = await chromium.launch();
    this.ctx = await this.b.newContext({ viewport: vp, deviceScaleFactor: this.dpr });
    this.p = await this.ctx.newPage();
    await this.p.goto(URL, { waitUntil: 'networkidle', timeout: 120000 });
    await this.p.waitForTimeout(3000);
    await this.p.addStyleTag({ content: `.announcement-bar, header, .shopify-section-group-header-group{display:none!important}
      /* Model select full width so the '· 3D Scan' label is not truncated (layout only) */ .ewc-carpick{grid-template-columns:1fr!important}
      #capcur{position:fixed;left:0;top:0;width:22px;height:22px;z-index:2147483647;pointer-events:none;transform:translate(-3px,-2px)}
      #capring{position:fixed;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;border:3px solid #7c3aed;z-index:2147483646;pointer-events:none;opacity:0}` });
    await this.p.evaluate(() => {
      window.scrollTo(0, document.querySelector('.ewc-bleed').getBoundingClientRect().top + scrollY);
      const c = document.createElement('div'); c.id = 'capcur';
      c.innerHTML = '<svg viewBox="0 0 22 22" width="22" height="22"><path d="M2 1 L2 18 L6.5 13.8 L9.6 20.6 L12.6 19.3 L9.6 12.6 L15.6 12.4 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
      const r = document.createElement('div'); r.id = 'capring';
      document.body.append(c, r); c.style.display = 'none';
    });
    await this.p.clock.install();
    await this.settle(1500);
    fs.mkdirSync(this.dir, { recursive: true });
    for (const f of fs.readdirSync(this.dir)) if (f.endsWith('.jpg')) fs.unlinkSync(this.dir + f);
  }
  async settle(ms) { for (let t = 0; t < ms; t += 100) { await this.p.clock.runFor(100); await this.p.waitForTimeout(40); } }
  async waitIdle(ms = 2500) { await this.p.waitForLoadState('networkidle').catch(() => {}); await this.settle(ms); }
  rect(sel) { return this.p.evaluate(s => { const e = typeof s === 'string' ? document.querySelector(s) : null; if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, cx: r.x + r.width / 2, cy: r.y + r.height / 2 }; }, sel); }
  async rectText(sel, re) {
    return this.p.evaluate(([s, re]) => { const e = [...document.querySelectorAll(s)].find(x => new RegExp(re, 'i').test(x.textContent.trim())); if (!e) return null; const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height, cx: r.x + r.width / 2, cy: r.y + r.height / 2 }; }, [sel, re]);
  }
  setMeta(clip, panes, extra = {}) { this.meta = { clip, panes, dpr: this.dpr, fps: FPS, ...extra }; }
  async snap() {
    const want = !DRY || this.dryFrames.has(this.n);
    if (want) await this.p.screenshot({ path: this.dir + `f_${String(this.n).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92, clip: this.meta.clip });
    this.n++;
  }
  async tick(k = 1) { for (let i = 0; i < k; i++) { await this.p.clock.runFor(1000 / FPS); await this.snap(); } }
  async curShow(x, y) {
    this.cur = { x, y };
    await this.p.evaluate(([x, y]) => { const c = document.getElementById('capcur'); c.style.display = 'block'; c.style.left = x + 'px'; c.style.top = y + 'px'; }, [x, y]);
    await this.p.mouse.move(x, y);
  }
  async move(x, y, k = 12) {
    const a = this.cur || { x, y };
    for (let i = 1; i <= k; i++) {
      const t = ease(i / k); const px = a.x + (x - a.x) * t, py = a.y + (y - a.y) * t;
      await this.p.evaluate(([x, y]) => { const c = document.getElementById('capcur'); c.style.left = x + 'px'; c.style.top = y + 'px'; }, [px, py]);
      await this.p.mouse.move(px, py); await this.tick();
    }
    this.cur = { x, y };
  }
  async ring(i, k) {  // expanding click ring, frame i of k
    await this.p.evaluate(([x, y, t]) => { const r = document.getElementById('capring'); r.style.left = x + 'px'; r.style.top = y + 'px'; r.style.opacity = t >= 1 ? 0 : (1 - t) * 0.9; r.style.transform = `scale(${0.5 + t * 0.9})`; }, [this.cur.x, this.cur.y, i / k]);
  }
  async click(x, y, k = 12, after = null) {  // move, press ring, real click (or custom action), ring fades
    await this.move(x, y, k);
    await this.ring(0, 8); await this.tick(2);
    if (after) await after(); else await this.p.mouse.click(x, y);
    for (let i = 1; i <= 8; i++) { await this.ring(i, 8); await this.tick(); }
  }
  async clickSel(sel, re, k = 12) { const r = re ? await this.rectText(sel, re) : await this.rect(sel); if (!r) throw new Error('no ' + sel + ' ' + re); await this.click(r.cx, r.cy, k); }
  async choose(sel, label, k = 10) {  // native <select>: cursor clicks the box, value changes (no OS popup in headless)
    const r = await this.rect(sel); await this.click(r.x + r.w * 0.75, r.cy, k, async () => { await this.p.selectOption(sel, { label }); });
  }
  async drag(x1, y1, x2, y2, k, pre = 10) {
    await this.move(x1, y1, pre); await this.ring(0, 8); await this.p.mouse.down(); await this.tick(2);
    for (let i = 1; i <= k; i++) {
      const t = ease(i / k); const px = x1 + (x2 - x1) * t, py = y1 + (y2 - y1) * t;
      await this.p.evaluate(([x, y]) => { const c = document.getElementById('capcur'); c.style.left = x + 'px'; c.style.top = y + 'px'; }, [px, py]);
      await this.ring(Math.min(i, 8), 8);
      await this.p.mouse.move(px, py); await this.tick();
    }
    await this.p.mouse.up(); this.cur = { x: x2, y: y2 }; await this.tick(2);
  }
  async linearDrag(x1, y1, dx, dy, k) {  // constant-speed drag (orbits): no easing, cursor hidden
    await this.p.mouse.move(x1, y1); await this.p.mouse.down();
    for (let i = 1; i <= k; i++) { await this.p.mouse.move(x1 + dx * i / k, y1 + dy * i / k); await this.tick(); }
    await this.p.mouse.up();
  }
  async scrollPanel(top, k) {
    const s0 = await this.p.evaluate(() => document.querySelector('.ewc-drawer-body').scrollTop);
    for (let i = 1; i <= k; i++) { const v = s0 + (top - s0) * ease(i / k); await this.p.evaluate(v => { document.querySelector('.ewc-drawer-body').scrollTop = v; }, v); await this.tick(); }
  }
  async panelTo(sel, re, offset = 0) {  // scrollTop that puts the element at `offset` px below the body top (no frames)
    return this.p.evaluate(([s, re, off]) => {
      const b = document.querySelector('.ewc-drawer-body');
      const e = re ? [...b.querySelectorAll(s)].find(x => new RegExp(re, 'i').test(x.textContent.trim())) : b.querySelector(s);
      return b.scrollTop + e.getBoundingClientRect().top - b.getBoundingClientRect().top - off;
    }, [sel, re, offset]);
  }
  async setPanelScroll(v) { await this.p.evaluate(v => { document.querySelector('.ewc-drawer-body').scrollTop = v; }, v); }
  async pick(make, model) {  // setup-time car change (no frames)
    await this.p.selectOption('select[aria-label=Make]', { label: make }, { force: true }); await this.settle(300);
    const lab = await this.p.$$eval('select[aria-label=Model] option', (o, m) => o.find(x => x.textContent.startsWith(m)).textContent, model);
    await this.p.selectOption('select[aria-label=Model]', { label: lab }, { force: true }); await this.waitIdle(3000);
    return lab;
  }
  async pan(dx, dy) { const v = await this.rect('.ewc-viewport'); await this.p.mouse.move(v.cx, v.cy); await this.p.mouse.down({ button: 'right' });
    await this.p.mouse.move(v.cx + dx, v.cy + dy, { steps: 8 }); await this.p.mouse.up({ button: 'right' }); await this.settle(600); }
  async orbit(dx, dy) { const v = await this.rect('.ewc-viewport'); await this.p.mouse.move(v.cx, v.cy); await this.p.mouse.down();
    await this.p.mouse.move(v.cx + dx, v.cy + dy, { steps: 8 }); await this.p.mouse.up(); await this.settle(600); }
  async zoom(ticks) { const v = await this.rect('.ewc-viewport'); await this.p.mouse.move(v.cx, v.cy); for (let i = 0; i < Math.abs(ticks); i++) { await this.p.mouse.wheel(0, ticks > 0 ? 120 : -120); await this.settle(150); } await this.settle(600); }
  async center(fx = 0.5, fy = 0.5, iters = 2) {  // pan so the car+wing edge bbox centre sits at (fx, fy) of the viewport
    const { execFileSync } = require('child_process');
    for (let k = 0; k < iters; k++) {
      const v = await this.rect('.ewc-viewport'); const f = '/tmp/claude-0/ewc_center.png';
      await this.p.screenshot({ path: f, clip: { x: v.x, y: v.y, width: v.w, height: v.h } });
      const [x0, y0, x1, y1] = execFileSync('python3', ['/home/user/illumaesthetic-video-editor/projects/epsilon-wing-configurator/tools/bbox.py', f]).toString().trim().split(' ').map(Number).map(n => n / this.dpr);
      const dx = v.w * fx - (x0 + x1) / 2, dy = v.h * fy - (y0 + y1) / 2;
      if (Math.abs(dx) < 6 && Math.abs(dy) < 6) break;
      await this.pan(dx, dy);
    }
  }
  async view(name) { await this.p.click(`.ewc-stage button:has-text("${name}")`); await this.settle(1200); }
  async openAdjust() { await this.p.evaluate(() => { document.querySelector('.ewc-more-setup').open = true; }); await this.settle(300); }
  async finish() {
    fs.writeFileSync(this.dir + 'meta.json', JSON.stringify({ ...this.meta, frames: this.n }, null, 1));
    console.log(this.name, 'frames', this.n); await this.b.close();
  }
}

// ---- layouts: clip = absolute css rect captured; panes = [{src:[x,y,w,h] clip-relative css, dst:[x,y,w,h] px of 1080x1920}]
function portraitStage(c, st) {  // 9:16 window of the portrait app: full bleed width, height = width*16/9 from the bleed top
  const w = st.w, h = w * 16 / 9;
  const clip = { x: st.x, y: st.y, width: w, height: h };
  c.setMeta(clip, [{ src: [0, 0, w, h], dst: [0, 0, 1080, 1920] }]);
}
function stack(c, top, bot, split = 1100) {  // top: stage rect (aspect 1080:split), bot: panel rect (aspect 1080:(1900-split))
  const x0 = Math.min(top.x, bot.x), y0 = Math.min(top.y, bot.y), x1 = Math.max(top.x + top.w, bot.x + bot.w), y1 = Math.max(top.y + top.h, bot.y + bot.h);
  const clip = { x: x0, y: y0, width: x1 - x0, height: y1 - y0 };
  c.setMeta(clip, [{ src: [top.x - x0, top.y - y0, top.w, top.h], dst: [0, 0, 1080, split] },
                   { src: [bot.x - x0, bot.y - y0, bot.w, bot.h], dst: [0, split + 20, 1080, 1900 - split] }]);
}
function topRect(cx, cy, h) { const w = h * 1080 / 1100; return { x: cx - w / 2, y: cy - h / 2, w, h }; }
async function panelRect(c, yTop, h = 284) { const d = await c.rect('.ewc-drawer'); return { x: d.x, y: yTop, w: d.w, h }; }
function panelFull(c, d, y, h) {  // whole drawer column, 9:16
  const w = d.w, hh = w * 16 / 9; const clip = { x: d.x, y, width: w, height: hh };
  c.setMeta(clip, [{ src: [0, 0, w, hh], dst: [0, 0, 1080, 1920] }]);
}

const SHOTS = {
  // 0.00-4.07: hook, GR86 scan with its recommended wing, slow orbit
  async hero_a(c, N) {
    await c.pick('Toyota', 'GR86');
    portraitStage(c, await c.rect('.ewc-bleed'));
    await c.pan(-80, 0); await c.orbit(-12, 0); await c.zoom(-3);
    const v = await c.rect('.ewc-viewport');
    await c.linearDrag(v.cx, v.cy, 62, 0, N - 1);
  },


  // 4.07-8.57: closer on the wing, continuing the orbit
  async hero_b(c, N) {  // phone layout: the CONFIGURE sheet opens and scrolls through steps 1-4, back to Vehicle
    await c.pick('Toyota', 'GR86');
    portraitStage(c, await c.rect('.ewc-bleed'));
    await c.pan(-80, 0); await c.orbit(40, 0); await c.zoom(-3);
    const t = await c.rect('.ewc-drawer-toggle');
    await c.curShow(t.cx - 120, t.cy - 160); await c.tick(4);
    await c.click(t.cx, t.cy, 12); await c.settle(0); await c.tick(10);
    const end = await c.p.evaluate(() => { const b = document.querySelector('.ewc-drawer-body'); return b.scrollHeight - b.clientHeight; });
    const pq = await c.panelTo('.ewc-step-checkout', null, 10);
    await c.scrollPanel(Math.min(end, pq), 54); await c.tick(10);
    await c.scrollPanel(0, 30);
    await c.tick(Math.max(0, N - c.n));
  },


  // 8.57-14.07: make/model pickers swap the car in the 3D view, ends on the NA Miata
  async cars(c, N) {
    await c.pick('Toyota', 'GR86');
    const v = await c.rect('.ewc-viewport'); const mk = await c.rect('select[aria-label=Make]');
    stack(c, topRect(v.cx, v.cy, 694), await panelRect(c, mk.y - 150));
    await c.curShow(v.cx + 300, v.cy);
    const go = async (make, model, hold) => {
      await c.choose('select[aria-label=Make]', make, 9); await c.settle(200);
      const lab = await c.p.$$eval('select[aria-label=Model] option', (o, m) => o.find(x => x.textContent.startsWith(m)).textContent, model);
      await c.choose('select[aria-label=Model]', lab, 9);
      await c.p.waitForLoadState('networkidle').catch(() => {}); await c.p.waitForTimeout(1500);
      await c.tick(hold);
    };
    await c.tick(6);
    await go('Honda', 'Civic Type R FL5', 22);
    await go('Chevrolet', 'Corvette C8', 22);
    await go('Mazda', 'MX-5 Miata NA', 1);
    await c.tick(N - c.n);
  },
  // 14.07-18.07: wing element on the NA Miata, rear view (TC 47.5 -> TC 66.5 -> GT -> custom width)
  async wing(c, N) {
    await c.pick('Mazda', 'MX-5 Miata NA'); await c.view('Rear');
    const v = await c.rect('.ewc-viewport'); const ws = await c.rect('select[aria-label="Wing element"][data-where="panel"]');
    const tw = 1050, th = tw * 760 / 1080;   // wide pane: the whole 66.5" wing + car fit
    stack(c, { x: v.cx - tw / 2, y: v.y + 4, w: tw, h: th }, await panelRect(c, ws.y - 110, 384 * 1140 / 1080), 760);
    await c.curShow(ws.x + 200, ws.y + 120); await c.tick(2);
    const sel = 'select[aria-label="Wing element"][data-where="panel"]';
    for (const [lab, hold] of [['TC 47.5" (1206 mm)', 12], ['TC 66.5" (1689 mm)', 8], ['GT Wing (66 Inch, Dry Carbon)', 10], ['Custom TC width…', 1]]) {
      await c.choose(sel, lab, 6); await c.p.waitForTimeout(800); await c.tick(hold);
    }
    await c.tick(N - c.n);
  },

  // 18.07-24.07: tested setups + mount types on the NA Miata (fender -> bottom card -> swan neck -> fender)
  async mounts(c, N) {  // P7 tested setups 0.1-1.5 s, P8 'bottom mount' ~2.3 s, P9 'swan neck' ~3.7 s, 'fender mount' ~4.6 s
    await c.pick('Mazda', 'MX-5 Miata NA'); await c.openAdjust();
    const v = await c.rect('.ewc-viewport');
    const top = await c.panelTo('.ewc-step-setup', null, 10); await c.setPanelScroll(top); await c.settle(300);
    const sh = await c.rect('.ewc-step-setup');
    stack(c, topRect(v.cx + 70, v.cy + 10, 600), await panelRect(c, sh.y - 4));
    const card = await c.rectText('.ewc-presets button', '^Bottom mount');
    await c.curShow(card.cx + 160, card.cy + 160); await c.move(card.cx + 120, card.cy + 10, 30); await c.tick(Math.max(0, 52 - c.n));
    await c.clickSel('.ewc-presets button', '^Bottom mount', 10); await c.p.waitForTimeout(800);
    const to = await c.panelTo('.ewc-seg', null, 150); await c.scrollPanel(to, 14);
    await c.tick(Math.max(0, 98 - c.n));
    await c.clickSel('.ewc-seg button', '^Swan neck', 10); await c.p.waitForTimeout(800);
    await c.tick(Math.max(0, 128 - c.n));
    await c.clickSel('.ewc-seg button', '^Fender mount', 8); await c.p.waitForTimeout(800);
    await c.tick(Math.max(0, N - c.n));
  },

  // 24.07-26.07: base style on the GR86 (CNC <-> sheet metal)
  async bases(c, N) {
    await c.pick('Toyota', 'GR86'); await c.openAdjust();
    const v = await c.rect('.ewc-viewport');
    await c.p.mouse.move(v.cx, v.cy); for (let i = 0; i < 2; i++) { await c.p.mouse.wheel(0, -120); await c.settle(150); }
    await c.p.click('.ewc-step-setup button:has-text("Change")').catch(() => {}); await c.settle(500);
    const to = await c.panelTo('.ewc-step-setup button', '^5 axis CNC', 110); await c.setPanelScroll(to); await c.settle(300);
    const cnc = await c.rectText('.ewc-step-setup button', '^5 axis CNC');
    stack(c, topRect(v.cx, v.cy + 40, 560), await panelRect(c, cnc.y - 110));
    await c.curShow(cnc.cx + 60, cnc.cy + 90); await c.tick(2);
    await c.clickSel('.ewc-step-setup button', '^5 axis CNC', 8); await c.p.waitForTimeout(800); await c.tick(4);
    const t2 = await c.panelTo('.ewc-step-setup button', '^Sheet metal', 110); await c.scrollPanel(t2, 6); await c.tick(4);
    await c.clickSel('.ewc-step-setup button', '^Sheet metal', 8); await c.p.waitForTimeout(800);
    await c.tick(Math.max(0, N - c.n));
  },
  // 26.07-29.07: AoA holes, side view (trunk zoom), GR86
  async aoa(c, N) {  // 3D close-up of the wing from the side; AoA hole 0 -> 15 below
    await c.pick('Toyota', 'GR86'); await c.openAdjust();
    await c.orbit(-210, -10); await c.zoom(-4);
    const sel = 'select[aria-label="AoA hole"]';
    const to = await c.panelTo(sel, null, 140); await c.setPanelScroll(to); await c.settle(300);
    const v = await c.rect('.ewc-viewport'); const s = await c.rect(sel);
    stack(c, topRect(v.cx, v.cy, 600), await panelRect(c, s.y - 140));
    const opts = await c.p.$$eval(sel + ' option', o => o.map(x => x.textContent));
    await c.curShow(s.x + 250, s.cy + 40); await c.tick(2);
    await c.click(s.x + s.w * 0.75, s.cy, 8, async () => { await c.p.focus(sel); });
    for (let i = 1; i < opts.length && c.n < N - 8; i++) { await c.p.selectOption(sel, { label: opts[i] }); await c.tick(i < 3 ? 6 : 4); }
    await c.tick(Math.max(0, N - c.n));
  },

  // 29.07-30.57: turn and zoom the 3D view
  async turn3d(c, N) {  // the cursor turns the car to a front 3/4 (no other shot uses it) and zooms in
    await c.pick('Toyota', 'GR86');
    portraitStage(c, await c.rect('.ewc-bleed'));
    await c.pan(-80, 0); await c.orbit(-150, 0); await c.zoom(-1);
    const v = await c.rect('.ewc-viewport');
    await c.curShow(v.cx + 110, v.cy + 90);
    await c.drag(v.cx + 110, v.cy + 90, v.cx - 40, v.cy + 80, 24, 3);
    for (let i = 0; i < 4; i++) { await c.p.mouse.wheel(0, -30); await c.tick(2); }
    await c.tick(Math.max(0, N - c.n));
  },


  // 30.57-35.57: side view: drag the wing (overhang/height), then the round handle to tilt
  async side(c, N) {
    await c.pick('Toyota', 'GR86'); await c.view('Side');
    const st = await c.rect('.ewc-bleed'); portraitStage(c, st);
    const w = await c.rect('svg .ewc-wing');
    const gx = w.x + w.w * 0.5, gy = w.y + w.h * 0.3;
    await c.curShow(gx + 80, gy + 160); await c.tick(8);
    await c.drag(gx, gy, gx + 12, gy - 40, 34, 12); await c.tick(10);
    const h = await c.rect('svg .ewc-handle-rotate');
    await c.drag(h.cx, h.cy, h.cx + 6, h.cy - 34, 28, 12); await c.tick(Math.max(0, N - c.n));
  },
  // 35.57-38.57: rear view: drag an endplate to change the width
  async rear(c, N) {
    await c.pick('Toyota', 'GR86'); await c.view('Rear');
    portraitStage(c, await c.rect('.ewc-bleed'));
    const hs = await c.p.evaluate(() => [...document.querySelectorAll('svg .ewc-handle-width')].map(e => { const r = e.getBoundingClientRect(); return { cx: r.x + r.width / 2, cy: r.y + r.height / 2 }; }));
    const rgt = hs.sort((a, b) => b.cx - a.cx)[0];
    await c.curShow(rgt.cx - 90, rgt.cy + 120); await c.tick(5);
    await c.drag(rgt.cx, rgt.cy, rgt.cx - 45, rgt.cy, 36, 10); await c.tick(Math.max(0, N - c.n));
  },

  // 38.57-41.57: number controls + a lock, side view on top
  async sliders(c, N) {  // rear view on top (height + spacing dims, MM/IN toggle); number controls + locks below
    await c.pick('Toyota', 'GR86'); await c.openAdjust(); await c.view('Rear');
    const to = await c.panelTo('.ewc-numctl[data-num="overhang"]', null, 10); await c.setPanelScroll(to); await c.settle(300);
    const v = await c.rect('.ewc-viewport'); const foot = await c.rect('.ewc-stagefoot'); const oc = await c.rect('.ewc-numctl[data-num="overhang"]');
    const st = await c.rect('.ewc-stage'); const tw = st.w - 4, th = tw * 800 / 1080;   // whole rear view + MM/IN foot
    stack(c, { x: st.x + 2, y: foot.y + foot.h - 6 - th, w: tw, h: th }, await panelRect(c, oc.y - 8, 384 * 1100 / 1080), 800);
    const sl = await c.rect('.ewc-numctl[data-num="height"] .ewc-num-slider');
    const val = await c.p.$eval('.ewc-numctl[data-num="height"] .ewc-num-slider', e => [+e.min, +e.max, +e.value]);
    const fx = x => sl.x + 8 + (sl.w - 16) * (x - val[0]) / (val[1] - val[0]);
    await c.curShow(sl.cx, sl.cy + 60); await c.tick(2);
    await c.drag(fx(val[2]), sl.cy, fx(Math.min(val[1], val[2] + 76)), sl.cy, 24, 6); await c.tick(3);
    await c.clickSel('.ewc-numctl[data-num="overhang"] .ewc-num-btn[data-dir="more"]', null, 8);
    await c.clickSel('.ewc-numctl[data-num="overhang"] .ewc-num-btn[data-dir="more"]', null, 2);
    const tl = await c.panelTo('.ewc-locks', null, 120); await c.scrollPanel(tl, 12);
    await c.clickSel('.ewc-lock', '^Width', 8); await c.tick(Math.max(0, 88 - c.n));
    const mm = await c.rect('button[aria-label=Millimetres]');
    await c.click(mm.cx, mm.cy, 10); await c.tick(Math.max(0, N - c.n));
  },

  async units_unused(c, N) {
    await c.pick('Toyota', 'GR86'); await c.view('Side');
    const st = await c.rect('.ewc-bleed'); portraitStage(c, st);
    const mm = await c.rect('button[aria-label=Millimetres]');
    await c.curShow(mm.cx + 90, mm.cy - 120); await c.tick(4);
    await c.click(mm.cx, mm.cy, 10); await c.tick(Math.max(0, N - c.n));
  },
  // 43.07-48.57: live estimate, save spec, request a quote (locks; never sends)
  async price(c, N) {  // header estimate updates live (+ custom upright), then Save spec, then Request a quote (never sent)
    await c.pick('Toyota', 'GR86'); await c.openAdjust();
    const d = await c.rect('.ewc-drawer');
    const top = await c.panelTo('.ewc-numctl[data-num="height"]', null, 200); await c.setPanelScroll(top); await c.settle(300);
    panelFull(c, d, d.y, 0);
    const plus = await c.rect('.ewc-numctl[data-num="height"] .ewc-num-btn[data-dir="more"]');
    await c.curShow(plus.cx - 120, plus.cy + 120); await c.tick(3);
    await c.clickSel('.ewc-numctl[data-num="height"] .ewc-num-btn[data-dir="more"]', null, 10); await c.p.waitForTimeout(600); await c.tick(8);
    await c.clickSel('.ewc-numctl[data-num="height"] .ewc-num-btn[data-dir="more"]', null, 2); await c.p.waitForTimeout(600); await c.tick(8);
    const to = await c.panelTo('.ewc-step-checkout', null, 20); await c.scrollPanel(to, 16); await c.tick(10);
    await c.clickSel('.ewc-step-checkout button', '^Save spec', 10); await c.p.waitForTimeout(500); await c.tick(26);
    await c.clickSel('.ewc-step-checkout button', '^Request a quote', 10); await c.p.waitForTimeout(800); await c.tick(8);
    const to2 = await c.panelTo('.ewc-step-checkout .ewc-actions', null, 160); await c.scrollPanel(to2, 14);
    await c.tick(Math.max(0, N - c.n));
  },

  // 48.57-52.57: more options: blueprint / own photos (no upload)
  async more(c, N) {
    await c.pick('Toyota', 'GR86');
    const d = await c.rect('.ewc-drawer');
    const top = await c.panelTo('.ewc-step-checkout .ewc-pricebox', null, 20); await c.setPanelScroll(top); await c.settle(300);
    panelFull(c, d, d.y, 0);
    await c.curShow(d.cx, d.y + 200); await c.tick(3);
    const to = await c.panelTo('.ewc-more-panel', null, 60); await c.scrollPanel(to, 12);
    await c.clickSel('.ewc-more-panel > summary', null, 8); await c.tick(8);
    await c.clickSel('.ewc-more-panel details summary', 'blueprint', 8); await c.tick(14);
    await c.clickSel('.ewc-more-panel details summary', 'own photos', 10); await c.tick(6);
    const to2 = await c.panelTo('.ewc-more-panel', null, 20); await c.scrollPanel(to2, 12);
    await c.tick(Math.max(0, N - c.n));
  },
  // 52.57-55.57: conclusion, wide slow orbit
  async outro(c, N) {  // finished build, high rear 3/4 from the RIGHT (hero_a is rear-left), centred, slow push-in, no orbit
    await c.pick('Toyota', 'GR86');
    portraitStage(c, await c.rect('.ewc-bleed'));
    await c.orbit(150, -30); await c.zoom(-4); await c.center(0.5, 0.46, 3);
    const v = await c.rect('.ewc-viewport'); await c.p.mouse.move(v.cx, v.cy);
    for (let i = 0; i < N; i++) { if (i % 5 === 0 && i < N - 10) await c.p.mouse.wheel(0, -45); await c.tick(); }
  },



};
const LAYOUT = { hero_a: 'portrait', hero_b: 'portrait', turn3d: 'portrait', side: 'portrait', rear: 'portrait', outro: 'portrait' };
const FRAMES = { hero_a: 125, hero_b: 138, cars: 168, wing: 123, mounts: 183, bases: 63, aoa: 93, turn3d: 48, side: 153, rear: 93, sliders: 138, price: 168, more: 123, outro: 93 };

(async () => {
  const name = process.argv[2]; const N = FRAMES[name];
  const c = new Cap(name, LAYOUT[name] || 'desk');
  c.dryFrames = new Set([0, Math.floor(N / 3), Math.floor(N * 2 / 3), N - 1]);
  await c.open();
  await SHOTS[name](c, N);
  if (c.n < N) await c.tick(N - c.n);
  await c.finish();
})().catch(e => { console.error(e); process.exit(1); });
