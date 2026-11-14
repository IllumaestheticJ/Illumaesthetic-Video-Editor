"""Promo reels (1080x1920, 30 fps) cut from the long-form: usage  python reels.py <media_dir> [1|2|3 ...]
Shop footage is cropped from the 4K rough cut (the burned-in subtitle band and corner titles are cropped out, and no text is
put over it); text sits only on the scan / graphic shots; every number is a rounded width difference from Strut Spread.xlsx.
Music: the owner-supplied Gran Turismo compilation (music/gt_48.wav), as in the long-form from v11. Voice: the owner's on-camera audio rebuilt from the raw clips, and the approved narration takes (vo10). Ends on a YouTube card."""
import sys, os, math, wave, subprocess, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont
M = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); SRC = f'{M}/dl/MiataScan_RoughCut_1.mp4'
W, H, FPS, SR = 1080, 1920, 30, 48000; OUT = f'{M}/out/reels'; WK = f'{M}/work/reels'; os.makedirs(OUT, exist_ok=True); os.makedirs(WK, exist_ok=True)
sp = importlib.util.spec_from_file_location('h', f'{HERE}/heat3d.py'); h = importlib.util.module_from_spec(sp); sp.loader.exec_module(h)
BG = tuple(h.BGC) if not isinstance(h.BGC, str) else (22, 22, 24); GOLD, FG, RED, GREEN, BLUE = (214, 164, 25), (232, 236, 242), (229, 72, 77), (63, 185, 80), (76, 154, 255)
_f = {}
def F(sz, wt='Bold'):
    if (sz, wt) not in _f: _f[(sz, wt)] = ImageFont.truetype(subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout, sz)
    return _f[(sz, wt)]
def ease(x): x = min(max(x, 0), 1); return x*x*(3 - 2*x)
def run(c): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + c, check=True)
ENC = ['-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-video_track_timescale', '30000']
# ---------------------------------------------------------------- segments
def track(a, d):
    """where the host's face is, 4 times a second (skin tone in the top 55 % of the frame), smoothed: the 9:16 window follows him"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(d + .3), '-i', SRC, '-vf', 'fps=4,scale=480:270', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 270, 480, 3).astype(int); xs = []
    for g in f:
        r, gg, b = g[:150, :, 0], g[:150, :, 1], g[:150, :, 2]; skin = (r > 110) & (gg > 60) & (r > gg*1.15) & (r < gg*1.7) & (gg > b*1.05) & (r - b > 30) & (r < 245)
        xs.append(np.argmax(np.convolve(skin.sum(0).astype(float), np.ones(50), 'same'))/480)
    xs = np.array(xs); xs = np.array([np.median(xs[max(i - 1, 0):i + 2]) for i in range(len(xs))]); xs = np.convolve(np.pad(xs, 1, mode='edge'), np.ones(3)/3, 'valid')
    return [(i/4, float(x)) for i, x in enumerate(xs)]
def irl(out, a, d, cx, n):
    hh = 1840 if a < 184.27 else 2160; ww = int(hh*9/16)//2*2; px = lambda c: int(min(max(c*3840 - ww/2, 0), 3840 - ww))      # front section: crop above the burned-in subtitle band
    if cx == 'host':
        K = track(a, d); e = str(px(K[-1][1]))
        for (t0, c0), (t1, c1) in reversed(list(zip(K, K[1:]))): e = f'if(lt(t,{t1}),{px(c0)}+({px(c1) - px(c0)})*(t-{t0})/{t1 - t0},{e})'
        x = f"'{e}'"
    else: x = px(cx)
    run(['-ss', f'{a:.3f}', '-i', SRC, '-vf', f'crop={ww}:{hh}:{x}:0,scale={W}:{H}:flags=lanczos,fps={FPS}', '-an', '-frames:v', str(n), *ENC, out])
def pipe(out, n, draw):
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *ENC, out], stdin=subprocess.PIPE)
    for i in range(n): ff.stdin.write(draw(i/FPS, n/FPS).convert('RGB').tobytes())
    ff.stdin.close(); ff.wait()
def car(state, yaw, pitch, w, hh, scale): return Image.fromarray(h.render(f'{M}/heat3d', state, math.radians(yaw), math.radians(pitch), w, hh, scale, splat=4))
def ctext(d, y, s, font, fill, a=1.0):
    if a <= 0: return
    c = tuple(int(BG[i] + (fill[i] - BG[i])*min(a, 1)) for i in range(3)); d.text((W/2, y), s, font=font, fill=c, anchor='mm')
def ramp(im, d, y):
    v = np.linspace(-h.SC, h.SC, 600); im.paste(Image.fromarray(np.repeat(h.cmap(v)[None].astype(np.uint8), 22, 0)), (240, y))
    d.text((226, y + 11), 'IN', font=F(30), fill=FG, anchor='rm'); d.text((854, y + 11), 'OUT', font=F(30), fill=FG, anchor='lm')
def heat_single(state, y0, y1, head, big, sub):
    def draw(t, D):
        im = Image.new('RGB', (W, H), BG); u = t/D; im.paste(car(state, y0 + (y1 - y0)*ease(u), 15, W, 900, 0.29), (0, 560)); d = ImageDraw.Draw(im)
        ctext(d, 300, head, F(64), FG, t/.3)
        if big:
            k = ease((t - .5)/1.2); ctext(d, 430, f'+{big*k:.1f} mm', F(170, 'Black'), GOLD, (t - .4)/.3); ctext(d, 555, sub, F(46, 'SemiBold'), FG, (t - .9)/.3)
        else: ctext(d, 400, sub, F(50, 'SemiBold'), GOLD, (t - .4)/.3)
        ramp(im, d, 1470); return im
    return draw
def heat_pair(a, b, la, lb, y0, y1, head=None):
    def draw(t, D):
        im = Image.new('RGB', (W, H), BG); u = t/D; yaw = y0 + (y1 - y0)*ease(u); d = ImageDraw.Draw(im)
        for st, lab, col, yy, t0 in ((a, la, RED, 250, .1), (b, lb, GREEN, 890, .7)):
            im.paste(car(st, yaw, 15, W, 560, 0.235), (0, yy + 70)); d = ImageDraw.Draw(im)
            al = min(max((t - t0)/.3, 0), 1); c = tuple(int(BG[i] + (col[i] - BG[i])*al) for i in range(3)); w = d.textlength(lab, font=F(50))
            d.rounded_rectangle([W/2 - w/2 - 34, yy, W/2 + w/2 + 34, yy + 80], 40, fill=c); d.text((W/2, yy + 40), lab, font=F(50), fill=(14, 14, 14) if al > .5 else c, anchor='mm')
        if head: ctext(d, 160, head, F(56), FG, t/.3)
        ramp(im, d, 1500); return im
    return draw
def bars(rows):
    def draw(t, D):
        im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im); ctext(d, 330, 'STRUT TOWER SPREAD', F(60), FG, t/.3); ctext(d, 405, 'one corner jacked, vs the car on the ground', F(36, 'Medium'), (150, 156, 164), (t - .2)/.3)
        y = 640
        for lab, v, col, t0 in rows:
            k = ease((t - t0)/.8); al = (t - t0)/.25
            if al > 0:
                d.text((110, y), lab, font=F(48), fill=FG); d.rounded_rectangle([110, y + 76, 110 + max(860*v/1.7*k, 18), y + 166], 14, fill=col)
                d.text((110 + 860*v/1.7*k + 26, y + 121), f'+{v*k:.1f} mm', font=F(76, 'Black'), fill=FG, anchor='lm')
            y += 340
        return im
    return draw
_logo = None
def endcard(q):
    def draw(t, D):
        global _logo
        if _logo is None:
            lg = Image.open(f'{M}/logos/IllumaestheticLogoColor-01.png').convert('RGBA'); _logo = lg.resize((760, int(lg.height*760/lg.width)), Image.LANCZOS)
        im = Image.new('RGB', (W, H), (10, 10, 12)); d = ImageDraw.Draw(im)
        for j, line in enumerate(q): ctext(d, 560 + 96*j, line, F(84, 'Black'), FG if j < len(q) - 1 else GOLD, (t - .05 - .12*j)/.25)
        k = ease((t - .5)/.4); w = d.textlength('FULL TEST ON YOUTUBE', font=F(54))
        if k > 0:
            d.rounded_rectangle([W/2 - w/2 - 44, 930, W/2 + w/2 + 44, 1030], 50, fill=tuple(int(10 + (RED[i] - 10)*k) for i in range(3))); d.text((W/2, 980), 'FULL TEST ON YOUTUBE', font=F(54), fill=(255, 255, 255), anchor='mm')
        k = ease((t - .8)/.4)
        if k > 0: lg = _logo.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v*k))); im.paste(lg, (W//2 - lg.width//2, 1180), lg)
        return im
    return draw
# ---------------------------------------------------------------- sound
def wav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768; x = x.reshape(-1, w.getnchannels()).mean(1); r = w.getframerate()
    return x if r == SR else np.interp(np.arange(0, len(x), r/SR), np.arange(len(x)), x).astype(np.float32)
def act_rms(x):
    n = len(x)//4800; e = np.sqrt((x[:n*4800].reshape(n, 4800)**2).mean(1)); return np.sqrt((e[e > e.max()*.1]**2).mean())
_o = None
def own(a, d):
    global _o
    if _o is None: w = wave.open(f'{M}/work/front_clean48.wav'); _o = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768      # v2: dialogue rebuilt from the raw clips (cleanfront.py), no rough-cut music in it
    x = _o[int(a*SR):int((a + d)*SR)].copy(); e = 480; x[:e] *= np.linspace(0, 1, e); x[-e:] *= np.linspace(1, 0, e); return x
REF = None
def vo(i):
    global REF
    if REF is None: REF = act_rms(own(48, 45))
    x = wav(f'{M}/vo10/{i:02d}.wav'); k = np.nonzero(np.abs(x) > 10**(-45/20))[0]; x = x[max(k[0] - 1440, 0):k[-1] + 5760]; return x*REF/act_rms(x)
def music(name, pos, n):
    w = wave.open(f'{M}/music/{name}_48.wav'); w.setpos(int(pos*SR)); x = np.frombuffer(w.readframes(n), np.int16).reshape(-1, 2).mean(1).astype(np.float32)/32768
    return x*(10**(-20/20)/np.sqrt((x**2).mean() + 1e-12))
# ---------------------------------------------------------------- the reels: (kind, args..., seconds or None = length of its voice, voice)
# voice: ('own', a) rough-cut audio from a for the segment | ('vo', i) narration take i | None
REELS = {
 1: dict(name='Reel1_1p7mm', music=('gt', 600.0), seg=[
    ('irl', 191.6, 0.36, 1.25, None),
    ('irl', 194.1, 0.50, 2.4, ('vo', 3)),
    ('draw', heat_single('jacked', 255, 325, 'ONE CORNER JACKED UP', 1.7, 'wider between the strut towers'), 8.9, None),      # the rest of narration take 3, which starts under the tape-measure shot
    ('draw', heat_pair('jacked', 'fender', 'NO BRACING  +1.7 mm', 'FENDER BRACES  +0.3 mm', 210, 320), None, ('vo', 10)),
    ('draw', endcard(['DOES BRACING', 'ACTUALLY WORK?']), 2.8, None)]),
 2: dict(name='Reel2_the_surprise', music=('gt', 1290.0), seg=[
    ('irl', 64.62, 'host', 4.45, ('own', 64.62)),
    ('irl', 257.75, 0.62, 2.0, None),
    ('draw', bars([('Strut tower brace', 0.8, BLUE, .3), ('Fender braces', 0.3, GREEN, 2.3)]), None, ('vo', 16)),
    ('irl', 313.8, 0.55, None, ('vo', 11)),
    ('draw', heat_pair('strut', 'fender', 'STRUT TOWER BRACE  +0.8 mm', 'FENDER BRACES  +0.3 mm', 210, 300, 'BODY MOVEMENT, SAME SCALE'), 3.4, None),
    ('draw', endcard(['WHICH BRACE', 'WOULD YOU PICK?']), 2.8, None)]),
 3: dict(name='Reel3_the_question', music=('gt', 860.0), seg=[
    ('irl', 0.0, 'host', 8.25, ('own', 0.0)),
    ('irl', 185.5, 0.55, 1.2, None), ('irl', 191.6, 0.36, 1.2, None), ('irl', 194.2, 0.50, 1.2, None), ('irl', 207.7, 0.50, 1.2, None), ('irl', 209.27, 0.68, 0.9, None),
    ('draw', heat_single('jacked', 255, 315, 'WHERE DOES A MIATA FLEX?', 0, 'one corner jacked, 3D scanned'), 3.0, None),
    ('draw', heat_pair('jacked', 'strut', 'NO BRACING', 'STRUT TOWER BRACE', 215, 305), 3.0, None),
    ('draw', endcard(['DOES BRACING', 'ACTUALLY WORK?']), 2.8, None)]),
}
def build(k):
    R = REELS[k]; t = 0.0; fr = 0; files = []; voice = []; tl = []
    for i, (kind, *a) in enumerate(R['seg']):
        d, v = a[-2], a[-1]; x = None
        if v: x = own(v[1], d) if v[0] == 'own' else vo(v[1])
        if d is None: d = len(x)/SR + 0.45
        n = int(round((t + d)*FPS)) - fr; f = f'{WK}/r{k}_s{i}_{n}.mp4'; files.append(f); tl.append((t, d, kind))
        if not os.path.exists(f):
            if kind == 'irl': irl(f + '.tmp.mp4', a[0], d, a[1], n)
            else: pipe(f + '.tmp.mp4', n, a[0])
            os.rename(f + '.tmp.mp4', f)
        if x is not None: voice.append((t + (0 if v[0] == 'own' else 0.2), x, v[0]))
        t += d; fr += n
    open(f'{WK}/r{k}.txt', 'w').write(''.join(f"file '{f}'\n" for f in files)); N = int(fr/FPS*SR); mix = np.zeros(N, np.float32); duck = np.zeros(N, np.float32)
    for s, x, kind in voice:
        p = int(s*SR); x = x[:N - p]; mix[p:p + len(x)] += x; duck[max(p - 4800, 0):p + len(x) + 4800] = 1 if kind == 'vo' else 0.75
    kk = int(.35*SR); duck = np.convolve(duck, np.ones(kk)/kk, 'same'); m = music(*R['music'], N); g = 10**((-1.5 - 11.5*duck)/20)          # -21.5 dB RMS open, -33 under the voice
    m = m*g; r = int(1.2*SR); m[-r:] *= np.linspace(1, 0.25, r); mix = np.tanh((mix + m)*1.15)*0.8          # peaks stay under -1.5 dBFS after AAC
    w = wave.open(f'{WK}/r{k}.wav', 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.repeat(mix[:, None], 2, 1)*32767).astype(np.int16).tobytes())
    out = f"{OUT}/Miata_{R['name']}.mp4"
    run(['-f', 'concat', '-safe', '0', '-i', f'{WK}/r{k}.txt', '-i', f'{WK}/r{k}.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', out])
    print(out, '%.1f s' % (fr/FPS), ' | '.join('%.1f %s' % (a, c) for a, b, c in tl))
if __name__ == '__main__':
    for k in ([int(x) for x in sys.argv[2:]] or [1, 2, 3]): build(k)
