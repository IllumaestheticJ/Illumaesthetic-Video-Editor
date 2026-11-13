"""Final assembly with the cloned-voice narration and a continuous music bed.
usage: final.py <media_dir> <out_name.mp4> [--captions]
Timing comes from the generated audio (vo/NN.wav), not word counts: cards hold for their line, IRL shots keep their length
and a line that runs past its shot carries into the next card. After 3:04 the clips' own audio is dropped (it carries
pieces of the same music) and replaced by one levelled bed (musicbed.py) under the narration."""
import sys, os, wave, subprocess, importlib.util, numpy as np
M, OUTN = sys.argv[1], sys.argv[2]; HERE = os.path.dirname(os.path.abspath(__file__)); a0 = sys.argv[:]
sys.argv = [a0[0], M, '--script-only']; sp = importlib.util.spec_from_file_location('b', f'{HERE}/build.py'); b = importlib.util.module_from_spec(sp); sp.loader.exec_module(b); sys.argv = a0
SR = 48000; VO_RMS = -19.0; BED_DB = -11.0; LEAD, GAP, TAIL = 0.30, 0.25, 0.55
def wav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768; x = x.reshape(-1, w.getnchannels()).mean(1); assert w.getframerate() == SR, p; return x
def trim(x, th=10**(-45/20)):
    k = np.nonzero(np.abs(x) > th)[0]; return x[max(k[0]-int(.03*SR), 0):k[-1]+int(.12*SR)]
def level(x):
    n = len(x)//4800; e = np.sqrt((x[:n*4800].reshape(n, 4800)**2).mean(1)); act = e[e > e.max()*.1]; return x*10**(VO_RMS/20)/np.sqrt((act**2).mean())
# ---- fit the generated lines: one splice, then slow down the lines the voice model rushed (no pitch change)
FIT = f'{M}/vo_fit'; os.makedirs(FIT, exist_ok=True); MAXRATE = 3.7
def save(p, x):
    w = wave.open(p, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1)*32767).astype(np.int16).tobytes())
def fade(x, n=720): x = x.copy(); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n); return x
# line 03 came out with a garbled first word ("Mill bracing"): take "With no bracing," from line 06 and join it to the rest of 03
l3, l6 = wav(f'{M}/vo/03.wav'), wav(f'{M}/vo/06.wav'); h = fade(l6[int(1.30*SR):int(2.08*SR)]); r = fade(l3[int(1.08*SR):]); h *= np.sqrt((r[:SR*3]**2).mean())/np.sqrt((h**2).mean())*1.0
save(f'{FIT}/03_spliced.wav', np.concatenate([h, np.zeros(int(.10*SR), np.float32), r]))
def fitted(i, nar):
    src = f'{FIT}/03_spliced.wav' if i == 3 else f'{M}/vo/{i:02d}.wav'; x = trim(wav(src)); rate = b.nwords(nar)/(len(x)/SR)
    if rate <= MAXRATE: return x, rate, 1.0
    f = max(MAXRATE/rate, 0.72); out = f'{FIT}/{i:02d}_t{f:.3f}.wav'
    if not os.path.exists(out): b.run(['-i', src, '-af', f'atempo={f:.4f}', '-ar', str(SR), '-ac', '1', out])
    return trim(wav(out)), rate, f
# ---- schedule from audio
rows = []; t = 0.0; cur = 0.0; vi = 0; vo = []
for it in b.TL:
    k, a, c, sec, pic, nar = it
    if nar:
        x, rate, f = fitted(vi, nar); print('  line %02d  %.1f s  %.2f words/s%s' % (vi, len(x)/SR, b.nwords(nar)/(len(x)/SR), '' if f == 1 else '  (slowed x%.2f from %.2f)' % (f, rate))); x = level(x); s = max(t + LEAD, cur + GAP); e = s + len(x)/SR; vo.append((s, x, nar, vi)); vi += 1; cur = e
        d = (c - a) if k in ('src', 'gfx', 'fx') else max(float(c), e + TAIL - t)
    else: d = b.dur(it)
    rows.append((t, d, it)); t += d
total = t; t_new = next(tt for tt, d, it in rows if it[5]); print('total %s, narration from %s, %d lines, last line ends %s' % (b.tc(total), b.tc(t_new), len(vo), b.tc(cur)))
for (tt, d, it), nxt in zip(rows, rows[1:] + [None]):
    if it[5] and it[0] == 'src':
        s, x, _, i = next(v for v in vo if v[2] == it[5]); over = s + len(x)/SR - (tt + d)
        if over > 0.1: print('  line %02d runs %.1f s past its shot at %s (carries into the next card)' % (i, over, b.tc(tt)))
b.script_md(rows, total)
# ---- picture: frame-exact segments (cached by index + frame count) so cards cannot drift against the sound
SEG = f'{M}/work/segf'; os.makedirs(SEG, exist_ok=True); lst = []; FPS = 24000/1001; done_fr = 0
for i, (tt, d, (k, a, c, sec, pic, nar)) in enumerate(rows):
    n = int(round((tt + d)*FPS)) - done_fr
    if k == 'fx': n = int(round((c - a)*FPS))
    done_fr += n; f = f'{SEG}/s{i:02d}_{k}_{n}f.mp4'; lst.append(f); FR = ['-frames:v', str(n)]
    if os.path.exists(f): continue
    if k == 'src': b.run(['-ss', str(a), '-i', b.SRC, '-vf', 'scale=1920:1080', '-an', *FR, *[v for v in b.V if v not in ('-c:a', 'aac', '-b:a', '160k', '-ar', '48000', '-ac', '2')], f + '.tmp.mp4'])
    elif k == 'fx':
        subprocess.run([sys.executable, f'{HERE}/callout.py', b.SRC, str(a), str(c), f + '.fx.mp4'], check=True); b.run(['-i', f + '.fx.mp4', '-an', '-c:v', 'copy', f + '.tmp.mp4']); os.remove(f + '.fx.mp4')
    elif k == 'gfx': b.run(['-i', f'{M}/work/flex.mp4', '-an', *FR, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '24000/1001', '-video_track_timescale', '24000', f + '.tmp.mp4'])
    else: b.run(['-loop', '1', '-framerate', '24000/1001', '-i', f'{b.CARDS}/{a}.png', *FR, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '24000/1001', '-video_track_timescale', '24000', f + '.tmp.mp4'])
    os.rename(f + '.tmp.mp4', f)
open(f'{SEG}/list.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst)); b.run(['-f', 'concat', '-safe', '0', '-i', f'{SEG}/list.txt', '-c', 'copy', f'{SEG}/picture.mp4'])
print('picture frames', done_fr, '= %.3f s; schedule %.3f s' % (done_fr/FPS, total))
# ---- sound: rough-cut audio up to 3:04, then bed + narration
w = wave.open(f'{M}/work/audio48.wav')   # the cut is 1:1 with the rough cut up to 3:04
o = np.frombuffer(w.readframes(int(200*SR)), np.int16).reshape(-1, 2).astype(np.float32)/32768        # FIRST 200 s only (v6 bug: a second read replaced this with 200 s onward)
N = int(total*SR) + SR; mix = np.zeros((N, 2), np.float32); n0 = int(t_new*SR); xf = int(.25*SR); mix[:n0+xf] = o[:n0+xf]; mix[n0:n0+xf] *= np.linspace(1, 0, xf)[:, None]
# music after 3:04 from the real tracks (Dropbox "Media for Miata Brace Vid"), following the rough cut's own choices, found by
# fingerprint matching: 2AM under the control section, Time Stand Still under fender / both-braces shop footage, Cosmic
# Countdown under the strut-brace footage, Dark Summer Night under the data cards. One level, crossfades, no gaps.
MUS = f'{M}/music'; XF = 1.2
def track(name):
    w = wave.open(f'{MUS}/{name}_48.wav'); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32)/32768
    hop = SR//2; n = len(x)//hop; e = 10*np.log10((x[:n*hop].reshape(n, hop, 2)**2).mean((1, 2)) + 1e-12)
    env = np.convolve(np.pad(e, 8, mode='edge'), np.ones(17)/17, 'valid'); g = np.clip(-20.0 - env, -12, 9)            # slow levelling to -20 dB RMS
    return x*(10**(np.interp(np.arange(len(x)), (np.arange(n)+.5)*hop, g)/20))[:, None]
TR = {k: track(k) for k in ('2am', 'time_stand_still', 'cosmic_countdown', 'dark_summer_night')}; LEN = {k: len(v)/SR for k, v in TR.items()}
def want(k, a, sec):
    if sec.startswith('1.'): return '2am', 92.3 + (184.27 - 180.0)          # carries the whole control section, as in the rough cut
    if k != 'src': return 'dark_summer_night', None
    if 240 <= a < 275: return 'cosmic_countdown', 87.9 + (a - 240.0)
    return 'time_stand_still', 137.0 + (a - 300.0) if a < 335 else 137.0
blocks = []                                                               # merged (start, end, track, anchor)
for tt, d, (k, a, c, sec, pic, nar) in rows:
    if tt < t_new - 1e-6: continue
    name, pos = want(k, a, sec)
    if blocks and blocks[-1][2] == name: blocks[-1][1] = tt + d
    else: blocks.append([tt, tt + d, name, pos])
plan = []; DSN0 = 20.0; dsn = DSN0; END = lambda n: LEN[n] - XF - 6.0     # (cut time, track, track position)
def card_bed(t0, t1):
    global dsn
    while t0 < t1 - 0.01:
        if END('dark_summer_night') - dsn < 25: dsn = DSN0
        run = min(t1 - t0, END('dark_summer_night') - dsn); plan.append((t0, 'dark_summer_night', dsn)); dsn += run; t0 += run
for t0, t1, name, pos in blocks:
    if name == 'dark_summer_night': card_bed(t0, t1); continue
    run = min(t1 - t0, max(END(name) - pos, 0))
    if run > 3: plan.append((t0, name, pos))
    else: run = 0
    card_bed(t0 + run, t1)                                                # track ran out before the section did
bed = np.zeros((int((total - t_new + 1)*SR), 2), np.float32); xf = int(XF*SR)
for i, (t0, name, pos) in enumerate(plan):
    t1 = plan[i+1][0] if i+1 < len(plan) else total; n = int((t1 - t0)*SR) + xf; x = TR[name][int(pos*SR):int(pos*SR)+n].copy()
    if i > 0: x[:xf] *= np.sin(np.linspace(0, np.pi/2, xf))[:, None]
    if len(x) > xf: x[-xf:] *= np.cos(np.linspace(0, np.pi/2, xf))[:, None]
    p = int((t0 - t_new)*SR); x = x[:len(bed)-p]; bed[p:p+len(x)] += x
    print('  music %s  %-18s from %5.1f s' % (b.tc(t0), name, pos))
g = np.full(len(bed), 10**(BED_DB/20), np.float32); r = int(1.5*SR); g[:r] = 10**(np.linspace(0, BED_DB, r)/20); r2 = int(3*SR); g[-r2:] *= np.linspace(1, 0, r2)       # ease down from the rough cut's level
m = min(len(bed), N - n0); mix[n0:n0+m] += bed[:m]*g[:m, None]
for s, x, nar, i in vo: p = int(s*SR); mix[p:p+len(x)] += x[:, None]
mix = np.tanh(mix*1.0); ww = wave.open(f'{SEG}/mix.wav', 'w'); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((mix[:int(total*SR)]*32767).astype(np.int16).tobytes())
# ---- subtitles in the rough cut's style (white) for the new narration + the labels build.ass() already makes
L = ['[Script Info]', 'PlayResX: 1920', 'PlayResY: 1080', '[V4+ Styles]', 'Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV',
     'Style: old,Inter Display,54,&H00FFFFFF,&H00000000,&H00000000,1,1,4,0,2,60,60,40', 'Style: ig,Inter Display,46,&H00FFFFFF,&H00000000,&H00000000,1,1,4,0,7,60,60,50', '[Events]', 'Format: Layer, Start, End, Style, Text']
for u0, u1 in ((97.3, 103.0), (118.4, 122.4)): L.append(f'Dialogue: 0,{b.at(u0)},{b.at(u1)},ig,Miata Chop Shop\\NIG  @MCS_Parts')
import json
for tt, d, (k, a, c, sec, pic, nar) in rows:
    if k == 'gfx':
        for s in json.load(open(f'{M}/work/transcript.json')):
            if a - .1 <= s['start'] < c:
                cs = b.chunks(s['text'], 6); n = sum(len(q.split()) for q in cs); u = s['start'] - a + tt
                for q in cs: e = u + (min(s['end'], c) - s['start'])*len(q.split())/n; L.append(f'Dialogue: 0,{b.at(u)},{b.at(e)},old,{q}'); u = e
for s, x, nar, i in vo:
    cs = b.chunks(nar, 6); n = sum(b.nwords(q) for q in cs); u = s
    for q in cs: e = u + (len(x)/SR)*b.nwords(q)/n; L.append(f'Dialogue: 0,{b.at(u)},{b.at(e - .03)},old,{q}'); u = e
open(f'{SEG}/final.ass', 'w').write('\n'.join(L) + '\n')
os.makedirs(b.OUT, exist_ok=True)
b.run(['-i', f'{SEG}/picture.mp4', '-i', f'{SEG}/mix.wav', '-map', '0:v', '-map', '1:a', '-vf', f'ass={SEG}/final.ass', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', f'{b.OUT}/{OUTN}'])
print('done', f'{b.OUT}/{OUTN}')
