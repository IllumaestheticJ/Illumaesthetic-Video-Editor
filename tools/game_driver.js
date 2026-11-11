// Long-running headless Chromium session for a browser-playable game, driven over a local HTTP API.
// An agent cannot hold a browser open between tool calls; this process does, and the agent sends it
// one step at a time (press a key, look at a screenshot, press the next).
//
//   node tools/game_driver.js --url https://nfsu2.xyz/ --size 1280x720 --port 8765 --profile /home/user/media/work/<p>/game/profile &
//   curl -s 'localhost:8765/shot?path=/abs/out.png'            screenshot of the page (PNG; .jpg = JPEG)
//   curl -s 'localhost:8765/key?k=Enter'                       tap a key (Playwright key names)
//   curl -s 'localhost:8765/key?k=ArrowUp&ms=1500'             hold a key for ms
//   curl -s 'localhost:8765/keys?down=ArrowUp,ArrowLeft&ms=800' hold several keys together
//   curl -s 'localhost:8765/click?x=640&y=360'                 mouse click
//   curl -s 'localhost:8765/text'                              visible page text (first 1500 chars)
//   curl -s -X POST localhost:8765/eval --data 'document.title' evaluate JS in the page, JSON result
//   curl -s 'localhost:8765/log'                               recent console lines
//   curl -s 'localhost:8765/down?k=ArrowUp'  /up?k=ArrowUp     press / release without waiting (autopilots)
//   curl -s 'localhost:8765/resize?w=1920&h=1080'              change the viewport live
//   curl -s 'localhost:8765/rec?start=/abs/out.webm&fps=60&mbps=40'   record the game canvas + its audio (real time)
//   curl -s 'localhost:8765/rec?stop=1'                        stop; returns bytes written
//   curl -s 'localhost:8765/quit'
// Recording uses canvas.captureStream + MediaRecorder in the page; --init tools/game_audio_tap.js (loaded before
// the site's own scripts) mirrors everything the page sends to its speakers into the recording.
// The profile directory keeps the site's storage (game data cache, saves) between runs.
const { chromium } = require('playwright');
const http = require('http');
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d; };
const [W, H] = arg('size', '1280x720').split('x').map(Number);
const PORT = +arg('port', '8765');
const log = [];
(async () => {
  const ctx = await chromium.launchPersistentContext(arg('profile', '/tmp/game_profile'), {
    headless: true, viewport: { width: W, height: H },
    args: ['--enable-unsafe-webgpu', '--enable-features=Vulkan,WebGPU', '--use-vulkan=swiftshader', '--use-angle=swiftshader',
      '--use-webgpu-adapter=swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required',
      ...(arg('audio', 'off') === 'on' ? [] : ['--mute-audio'])],
  });
  const init = arg('init');
  if (init) await ctx.addInitScript({ path: init });
  const page = ctx.pages()[0] || await ctx.newPage();
  const fs = require('fs'); let recFd = null, recBytes = 0;
  await ctx.exposeBinding('__recChunk', (_src, b64) => { if (recFd !== null) { const b = Buffer.from(b64, 'base64'); fs.writeSync(recFd, b); recBytes += b.length; } });
  page.on('console', m => { log.push(`[${m.type()}] ${m.text().slice(0, 400)}`); if (log.length > 400) log.shift(); });
  page.on('pageerror', e => log.push('[pageerror] ' + String(e).slice(0, 400)));
  await page.goto(arg('url'), { waitUntil: 'domcontentloaded', timeout: 120000 });
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  http.createServer(async (req, res) => {
    const u = new URL(req.url, 'http://x'); const q = Object.fromEntries(u.searchParams);
    const done = (o) => { res.setHeader('content-type', 'application/json'); res.end(JSON.stringify(o) + '\n'); };
    try {
      if (u.pathname === '/shot') {
        const jpg = /\.jpe?g$/.test(q.path);
        await page.screenshot({ path: q.path, type: jpg ? 'jpeg' : 'png', ...(jpg ? { quality: +(q.q || 80) } : {}) }); done({ ok: q.path });
      } else if (u.pathname === '/key') {
        await page.keyboard.down(q.k); await sleep(+(q.ms || 80)); await page.keyboard.up(q.k); done({ ok: q.k });
      } else if (u.pathname === '/keys') {
        const ks = q.down.split(','); for (const k of ks) await page.keyboard.down(k);
        await sleep(+(q.ms || 80)); for (const k of ks.reverse()) await page.keyboard.up(k); done({ ok: ks });
      } else if (u.pathname === '/down') { await page.keyboard.down(q.k); done({ ok: q.k });
      } else if (u.pathname === '/up') { await page.keyboard.up(q.k); done({ ok: q.k });
      } else if (u.pathname === '/resize') { await page.setViewportSize({ width: +q.w, height: +q.h }); done({ ok: [q.w, q.h] });
      } else if (u.pathname === '/rec' && q.start) {
        recFd = fs.openSync(q.start, 'w'); recBytes = 0;
        const r = await page.evaluate(({ fps, mbps, codec, sel }) => {
          const cs = [...document.querySelectorAll('canvas')].filter(c => c.offsetParent !== null).sort((a, b) => b.width * b.height - a.width * a.height);
          const c = sel ? document.querySelector(sel) : cs[0];
          if (!c) return { error: 'no canvas' };
          const stream = c.captureStream(fps);
          const taps = (window.__audioTaps || []).filter(t => t.ctx.state !== 'closed');
          for (const t of taps) for (const tr of t.dest.stream.getAudioTracks()) stream.addTrack(tr);
          const mime = `video/webm;codecs=${codec}${taps.length ? ',opus' : ''}`;
          const mr = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: mbps * 1e6, audioBitsPerSecond: 256000 });
          mr.ondataavailable = async e => { if (!e.data.size) return; const buf = new Uint8Array(await e.data.arrayBuffer()); let s = ''; for (let i = 0; i < buf.length; i += 32768) s += String.fromCharCode.apply(null, buf.subarray(i, i + 32768)); window.__recChunk(btoa(s)); };
          window.__rec = mr; mr.start(500);
          return { mime, canvas: [c.width, c.height], audioTaps: taps.length };
        }, { fps: +(q.fps || 60), mbps: +(q.mbps || 30), codec: q.codec || 'vp8', sel: q.sel || '' });
        done(r);
      } else if (u.pathname === '/rec' && q.stop) {
        await page.evaluate(() => new Promise(res => { const m = window.__rec; if (!m || m.state === 'inactive') return res(); m.onstop = () => setTimeout(res, 700); m.stop(); }));
        if (recFd !== null) { fs.closeSync(recFd); recFd = null; } done({ bytes: recBytes });
      } else if (u.pathname === '/click') { await page.mouse.click(+q.x, +q.y); done({ ok: [q.x, q.y] });
      } else if (u.pathname === '/text') { done({ text: (await page.evaluate(() => document.body.innerText)).slice(0, +(q.n || 1500)) });
      } else if (u.pathname === '/eval') {
        let b = ''; for await (const c of req) b += c; done({ result: await page.evaluate(b) });
      } else if (u.pathname === '/log') { done({ log: log.slice(-(+(q.n || 30))) });
      } else if (u.pathname === '/quit') { done({ ok: 'bye' }); await ctx.close(); process.exit(0);
      } else done({ error: 'unknown ' + u.pathname });
    } catch (e) { done({ error: String(e).slice(0, 500) }); }
  }).listen(PORT, '127.0.0.1', () => console.log('driver on ' + PORT));
})();
