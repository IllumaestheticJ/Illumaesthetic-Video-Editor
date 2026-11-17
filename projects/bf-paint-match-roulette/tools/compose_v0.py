"""Assemble bf-paint-match-roulette v0 (preview) from stills.

python3 compose_v0.py  -> /home/user/media/work/out/bf-paint-match-roulette_v0.mp4
Grid: GT2 "Arcade Mode Theme", 140 BPM, first beat 0.0703 s (measured flux grid; every 8th has a transient).
Text only on render frames, never on photos. Prices: projects/_blackfriday/PRICES.md (liquidation sheet rev 25).
"""
import json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = '/home/user/media/bf-paint-match-roulette'
R = f'{M}/renders/v0'
OUT = '/home/user/media/work/out/bf-paint-match-roulette_v0.mp4'
W, H, FPS = 1080, 1920, 30
B0, BP = 0.0703, 60 / 140.0
def bt(b): return B0 + BP * b
END_T = bt(53) + 0.5

FD = '/usr/share/fonts/opentype/inter/'
F_HEAD = ImageFont.truetype(FD + 'InterDisplay-Black.otf', 86)
F_SUB = ImageFont.truetype(FD + 'InterDisplay-Bold.otf', 52)
F_CHIP = ImageFont.truetype(FD + 'InterDisplay-Bold.otf', 46)
F_CODE = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 34)
F_TAG = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 24)
OFF = (232, 236, 242)
GREY = (140, 146, 156)

col = json.load(open(f'{M}/renders/colours.json'))
FL, FE, DE = col['FL'], col['FE'], col['DE']

_cache = {}
def img(path, cover=False, cx=0.5):
    k = (path, cover, cx)
    if k not in _cache:
        im = Image.open(path).convert('RGB')
        if cover:
            sw, sh = im.size; tw = sh * W / H
            if tw <= sw:
                x0 = (sw - tw) * cx; im = im.crop((int(x0), 0, int(x0 + tw), sh))
            else:
                th = sw * H / W; y0 = (sh - th) / 2; im = im.crop((0, int(y0), sw, int(y0 + th)))
        _cache[k] = im.resize((W, H), Image.LANCZOS)
    return _cache[k]

def zoom(im, z, fx=0.5, fy=0.5):
    if z <= 1.0001: return im.copy()
    w, h = W / z, H / z; x0 = (W - w) * fx; y0 = (H - h) * fy
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)

def ctext(d, y, s, f, fill=OFF, spacing=6):
    # tracked, centred
    widths = [d.textlength(c, font=f) for c in s]; tw = sum(widths) + spacing * (len(s) - 1)
    x = (W - tw) / 2
    for c, cw in zip(s, widths):
        d.text((x, y), c, font=f, fill=fill); x += cw + spacing
    return tw

def price(d, y, label, was, now, f=F_SUB):
    # "LABEL  $was  $now" centred, was struck through
    parts = [(label + '  ', OFF, False), (was, GREY, True), ('  ' + now, OFF, False)]
    ws = [d.textlength(p, font=f) for p, _, _ in parts]; x = (W - sum(ws)) / 2
    for (p, c, strike), w in zip(parts, ws):
        d.text((x, y), p, font=f, fill=c)
        if strike:
            bb = d.textbbox((x, y), p, font=f); ym = (bb[1] + bb[3]) / 2
            d.line((bb[0] - 4, ym, bb[2] + 4, ym), fill=(220, 60, 60), width=6)
        x += w

def chip(d, name, code, hexc, y=1400):
    s = name.upper(); f = F_CHIP
    tw = d.textlength(s, font=f); cw = d.textlength(code, font=F_CODE)
    total = 70 + tw + 24 + cw; x = (W - total) / 2
    d.rounded_rectangle((x - 24, y - 18, x + total + 24, y + 70), radius=18, fill=(10, 10, 12))
    d.ellipse((x, y + 2, x + 50, y + 52), fill=hexc, outline=OFF, width=3)
    d.text((x + 70, y), s, font=f, fill=OFF)
    d.text((x + 70 + tw + 24, y + 10), code, font=F_CODE, fill=GREY)

def shade_top(im, h=560, a=170):
    g = Image.new('L', (1, h)); g.putdata([int(a * (1 - i / h)) for i in range(h)])
    black = Image.new('RGB', (W, h), (0, 0, 0)); im.paste(black, (0, 0), g.resize((W, h)))

def tag(d, s):
    d.text((40, 1840), s, font=F_TAG, fill=(255, 200, 60))

eps = Image.open(f'{M}/chars/eps.png'); dele = Image.open(f'{M}/chars/del.png')
def put_char(im, ch, h, x, yfoot, flip=False):
    c = ch.transpose(Image.FLIP_LEFT_RIGHT) if flip else ch
    s = h / c.height; c = c.resize((int(c.width * s), int(h)), Image.LANCZOS)
    # soft contact shadow
    sh = Image.new('L', (int(c.width * 1.3), 60), 0); ImageDraw.Draw(sh).ellipse((0, 0, sh.width, 60), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    im.paste((0, 0, 0), (int(x + c.width / 2 - sh.width / 2), int(yfoot - 30)), sh)
    im.paste(c, (int(x), int(yfoot - h)), c)

# ---------- shot list (beat index start, end, fn(t_local, dur) -> PIL image) ----------
shots = []
def add(b0, b1, fn): shots.append((bt(b0) if b0 > 0 else 0.0, bt(b1), fn))

def render_shot(path, z0=1.0, z1=1.03, text=None, fx=0.5, fy=0.45):
    def fn(t, dur):
        im = zoom(img(path), z0 + (z1 - z0) * t / dur, fx, fy)
        if text:
            d = ImageDraw.Draw(im); text(d, im, t, dur)
        return im
    return fn

def photo_shot(path, cx=0.5):
    def fn(t, dur):
        return zoom(img(path, cover=True, cx=cx), 1.0 + 0.03 * t / dur)
    return fn

# 1  silver scan + Eps placeholder
def s1_text(d, im, t, dur):
    put_char(im, eps, 760, 700, 1650)
    d = ImageDraw.Draw(im); tag(d, 'DRAFT v0 - Eps = model-sheet placeholder (no Higgsfield gen yet)')
add(0, 5, render_shot(f'{R}/fe_scan.png', text=s1_text))

# 2  base wing (gloss black) on Sonic Gray FE
def s2_text(d, im, t, dur):
    shade_top(im); d = ImageDraw.Draw(im)
    ctext(d, 230, 'BASE WING 30% OFF', F_HEAD)
    price(d, 360, 'CIVIC SPORT WING', '$450', '$315')
add(5, 9, render_shot(f'{R}/fe_base.png', 1.03, 1.06, s2_text))

# 3  paint wash: wing goes gloss black -> Sonic Gray Pearl
base = img(f'{R}/fe_base.png'); paint = img(f'{R}/fe_NH877P.png')
mask = np.asarray(img(f'{R}/fe_mask.png').convert('L')).astype(np.float32) / 255
ys, xs = np.nonzero(mask > 0.5); wx0, wx1 = xs.min(), xs.max()
xx = np.tile(np.arange(W, dtype=np.float32), (H, 1))
def s3(t, dur):
    p = min(1.0, max(0.0, t / 0.6)); p = p * p * (3 - 2 * p)
    front = wx1 - (wx1 - wx0 + 80) * p              # wash travels from the right end (where Eps' hand was)
    w = np.clip((xx - front) / 60, 0, 1) * mask
    a = np.asarray(base).astype(np.float32); b = np.asarray(paint).astype(np.float32)
    im = Image.fromarray((a * (1 - w[..., None]) + b * w[..., None]).astype(np.uint8))
    im = zoom(im, 1.06 + 0.03 * t / dur, 0.5, 0.45)
    shade_top(im); d = ImageDraw.Draw(im)
    ctext(d, 230, 'PAINT MATCH AVAILABLE', F_HEAD)
    price(d, 360, 'PAINT-MATCHED', '$850', '$715')
    if p >= 1: chip(d, 'Sonic Gray Pearl', 'NH877P', '#6e7886')
    return im
add(9, 13, s3)

# 4-6 real FL5 photos (no text)
P = f'{M}/photos'
add(13, 15, photo_shot(f'{P}/full_civic-fl5-sport-wing-blue-rear-quarter.jpg', 0.55))
add(15, 17, photo_shot(f'{P}/full_civic-type-r-fl5-sport-wing-white-rear-quarter.jpg', 0.5))
add(17, 19, photo_shot(f'{P}/full_civic-type-r-fl5-sport-wing-red-rear-quarter.jpg', 0.5))

def roulette(path, name, code, hexc, head, sub=None, extra=None, z=(1.0, 1.02)):
    def tx(d, im, t, dur):
        shade_top(im); d = ImageDraw.Draw(im)
        ctext(d, 230, head, F_HEAD if len(head) < 20 else F_SUB)
        if sub: sub(d)
        if name: chip(d, name, code, hexc)
        if extra: extra(d)
    return render_shot(path, z[0], z[1], tx)

# 7-15 FL hatch renders (locked camera)
def fl_sub(d): ctext(d, 350, 'CIVIC HATCH SPORT WING', F_SUB, GREY)
add(19, 21, roulette(f'{R}/fl_{FL[0][1]}.png', FL[0][0], FL[0][1], FL[0][2], 'PAINT MATCH AVAILABLE', fl_sub))
for i, c in enumerate(FL[1:]):
    add(21 + i, 22 + i, roulette(f'{R}/fl_{c[1]}.png', c[0], c[1], c[2], 'PAINT MATCH AVAILABLE', fl_sub))

# 16-26 FE spin (half-beats) + real Rallye Red FE landing
def fe_sub(d):
    ctext(d, 350, '11 HONDA COLOURS', F_SUB, GREY); price(d, 430, 'BASE', '$450', '$315')
for i, c in enumerate(FE):
    add(29 + 0.5 * i, 29.5 + 0.5 * i, roulette(f'{R}/fe_{c[1]}.png', None, None, None, 'CIVIC SEDAN SPORT WING', fe_sub))
add(33.5, 37, photo_shot(f'{P}/full_DILL7196.jpg', 0.5))

# 27-36 Integra spin + landing
def de_sub(d):
    ctext(d, 350, '10 ACURA COLOURS', F_SUB, GREY); price(d, 430, 'BASE', '$500', '$350')
for i, c in enumerate(DE[:8]):
    add(37 + 0.5 * i, 37.5 + 0.5 * i, roulette(f'{R}/de5_{c[1]}.png', None, None, None, 'INTEGRA SPORT WING', de_sub))
c = DE[8]; add(41, 42, roulette(f'{R}/de5_{c[1]}.png', c[0], c[1], c[2], 'INTEGRA SPORT WING', de_sub))
c = DE[9]
def de_land(d): price(d, 1520, 'PAINT-MATCHED', '$950', '$800', F_CHIP)
add(42, 45, roulette(f'{R}/de5_{c[1]}.png', c[0], c[1], c[2], 'INTEGRA SPORT WING', de_sub, de_land, (1.0, 1.04)))

# 37 end: silver scan + Del & Eps placeholders
def end_text(d, im, t, dur):
    put_char(im, dele, 820, 40, 1700)
    put_char(im, eps, 740, 760, 1690, flip=True)
    shade_top(im); d = ImageDraw.Draw(im)
    ctext(d, 200, 'BASE WING 30% OFF', F_HEAD)
    ctext(d, 320, 'PAINT MATCH AVAILABLE', F_SUB)
    ctext(d, 410, 'FROM $315', F_HEAD, (255, 255, 255))
    tag(d, 'DRAFT v0 - Del & Eps = model-sheet placeholders')
add(45, 49, render_shot(f'{R}/fe_scan_end.png', 1.0, 1.03, end_text))

# 38 logo
logo = Image.open(f'{M}/logo/banner_black.png').convert('RGBA')
a = logo.split()[3]; logo = Image.merge('RGBA', (a.point(lambda v: 255),) * 3 + (a,))
s = 720 / logo.width; logo = logo.resize((720, int(logo.height * s)), Image.LANCZOS)
def logo_shot(t, dur):
    im = Image.new('RGB', (W, H), (0, 0, 0))
    total = END_T - bt(49); fade = min(1, t / 0.25, max(0, (total - t) / 0.5))
    l = logo.copy(); l.putalpha(l.split()[3].point(lambda v: int(v * fade)))
    im.paste(l, ((W - 720) // 2, (H - l.height) // 2), l)
    d = ImageDraw.Draw(im); ctext(d, (H + l.height) // 2 + 60, 'EPSILON.PLUS', F_CODE, tuple(int(v * fade) for v in GREY))
    return im
shots.append((bt(49), END_T, logo_shot))

# ---------- render ----------
os.makedirs(os.path.dirname(OUT), exist_ok=True)
nfr = int(round(END_T * FPS))
cuts = []
starts = [int(round(s * FPS)) for s, _, _ in shots] + [nfr]
starts[0] = 0
for i in range(len(shots)): cuts.append(starts[i])
json.dump({'cuts_s': [round(c / FPS, 4) for c in cuts], 'cut_beats_s': [round(s, 4) for s, _, _ in shots]},
          open(f'{M}/cuts_v0.json', 'w'))
silent = OUT.replace('.mp4', '_silent.mp4')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                      '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', silent],
                     stdin=subprocess.PIPE)
for i, (s0, s1, fn) in enumerate(shots):
    f0, f1 = starts[i], starts[i + 1]; dur = max(1e-3, (f1 - f0) / FPS)
    for f in range(f0, f1):
        p.stdin.write(fn((f - f0) / FPS, dur).convert('RGB').tobytes())
p.stdin.close(); p.wait()
print('frames', nfr, 'shots', len(shots), 'silent', silent)
