"""bf-paint-match-roulette v0.2: retro "car dealership menu" version (owner reference: PS1-era racing game showroom).

Original UI drawn here (own icons, type and branding) in that genre's layout: lineup grid -> car screen with turntable,
colour name, CHANGE COLOR, price where the credits sit, BUY. Colours/prices: live store lists + BF liquidation sheet.
python3 compose_v02.py [--still t]  -> /home/user/media/work/out/bf-paint-match-roulette_v0.2.mp4
"""
import json, math, subprocess, os, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = '/home/user/media/bf-paint-match-roulette'
OUT = '/home/user/media/work/out/bf-paint-match-roulette_v0.4.mp4'
W, H, FPS = 1080, 1920, 30
B0, BP = 0.0903, 60 / 140.0
def bt(b): return B0 + BP * b
END_T = bt(53) + 0.5

ORANGE = (247, 160, 20); RED = (240, 84, 28); GREY = (150, 150, 150); WHITE = (240, 240, 240); DARK = (30, 22, 4)
FI = '/usr/share/fonts/opentype/inter/'
def F(name, size): return ImageFont.truetype(FI + name, size)
SERIF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', s)
f_tab = F('InterDisplay-Bold.otf', 36); f_stat = F('InterDisplay-Bold.otf', 44); f_small = F('InterDisplay-Bold.otf', 34)
f_price = F('InterDisplay-Black.otf', 104); f_was = F('InterDisplay-Bold.otf', 50); f_btn = F('InterDisplay-Black.otf', 30)
f_buy = F('InterDisplay-Black.otf', 58); f_tile = F('InterDisplay-Black.otf', 76); f_tile2 = F('InterDisplay-Black.otf', 44)
f_col = F('InterDisplay-Bold.otf', 46); f_code = F('InterDisplay-Medium.otf', 34)

col = json.load(open(f'{M}/renders/colours.json'))
BLACK = ['Gloss Black', '', '#0b0b0d', 'base']
CARS = {
 'fl': dict(make='Honda', title='Civic Hatch', sub='FL2 / FL5', base=(450, 315), paint=(850, 715), special={},
            colours=[['Championship White', 'NH0', '#f6f5ee', 'gloss'], ['Boost Blue Pearl', 'B637P', '#0a7ee8', 'pearl'],
                     ['Sonic Gray Pearl', 'NH877P', '#6e7886', 'pearl'], ['Rallye Red', 'R513', '#c8102e', 'gloss']] +
                    [c for c in col['FL'] if c[1] != 'NH877P']),
 'fe': dict(make='Honda', title='Civic Sedan', sub='FE', base=(450, 315), paint=(850, 715), special={'NH883P': (900, 765)},
            colours=[c for c in col['FE'][:1]] + [['Sonic Gray Pearl', 'NH877P', '#6e7886', 'pearl']] + col['FE'][1:5] +
                    [col['FE'][5], ['Rallye Red', 'R513', '#c8102e', 'gloss']] + col['FE'][6:]),
 'de5': dict(make='Acura', title='Integra', sub='DE4 / DE5', base=(500, 350), paint=(950, 800), special={'NH883P': (1000, 850)},
             colours=col['DE']),
}
assert len(CARS['fl']['colours']) == 12 and len(CARS['fe']['colours']) == 11 and len(CARS['de5']['colours']) == 10
ORDER = ['fl', 'fe', 'de5']

# ---------- turntable frames + tint ----------
_yy, _xx = np.mgrid[0:420, 0:720].astype(np.float32)
VIG = (np.clip((420 - _yy) / 70, 0, 1) * np.clip(_xx / 60, 0, 1) * np.clip((720 - _xx) / 60, 0, 1))[..., None]
_tt = {}
def tt(car, k):
    key = (car, k)
    if key not in _tt:
        d = f'{M}/tt/{car}/'
        _tt[key] = [np.asarray(Image.open(d + f'{t}_{k:02d}.png').convert('RGB')).astype(np.float32) / 255 for t in 'bwm']
    return _tt[key]
def lin(h): return np.array([(int(h[i:i + 2], 16) / 255) ** 2.2 for i in (1, 3, 5)], np.float32)
def car_img(car, k, hexc, base_wing):
    b, w, m = tt(car, k)
    lb, lw = b ** 2.2, w ** 2.2
    c = lin(hexc); wc = np.array([0.004] * 3, np.float32) if base_wing else c
    kk = m[..., 0:1] * c + m[..., 1:2] * wc
    out = (lb + (lw - lb) * kk / 0.95).clip(0, 1) ** (1 / 2.2)
    return Image.fromarray((out * VIG * 255).astype(np.uint8))

# ---------- UI pieces (v0.3: everything inside the safe area x 48-920, y 285-1440; knowledge/safe-zones.md) ----------
X0, X1, Y0, Y1 = 48, 920, 285, 1440
CX = (X0 + X1) // 2
f_tab = F('InterDisplay-Bold.otf', 27); f_small = F('InterDisplay-Bold.otf', 30); f_col = F('InterDisplay-Bold.otf', 42)
f_code = F('InterDisplay-Medium.otf', 30); f_price = F('InterDisplay-Black.otf', 92); f_was = F('InterDisplay-Bold.otf', 44)
f_btn = F('InterDisplay-Black.otf', 26); f_buy = F('InterDisplay-Black.otf', 44); f_tile = F('InterDisplay-Black.otf', 66)
f_tile2 = F('InterDisplay-Black.otf', 38); f_bar = F('InterDisplay-Bold.otf', 30)
def rr(d, box, r, fill=None, outline=None, width=0): d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
def icon_row(d):
    x = X0; y = Y0 + 4; s = 54
    for i in range(4):
        rr(d, (x, y, x + s, y + s), 8, fill=ORANGE)
        if i == 0:
            for a in range(2):
                for b in range(2): d.rectangle((x + 11 + a * 18, y + 11 + b * 18, x + 25 + a * 18, y + 25 + b * 18), fill=DARK)
        elif i == 1:
            d.polygon([(x + 8, y + 20), (x + 46, y + 14), (x + 46, y + 22), (x + 8, y + 28)], fill=DARK)
            d.rectangle((x + 14, y + 28, x + 18, y + 44), fill=DARK); d.rectangle((x + 36, y + 24, x + 40, y + 44), fill=DARK)
        elif i == 2:
            d.polygon([(x + 27, y + 9), (x + 39, y + 31), (x + 15, y + 31)], fill=DARK); d.ellipse((x + 15, y + 20, x + 39, y + 44), fill=DARK)
        else:
            d.polygon([(x + 9, y + 17), (x + 33, y + 17), (x + 46, y + 27), (x + 33, y + 37), (x + 9, y + 37)], fill=DARK)
            d.ellipse((x + 14, y + 23, x + 22, y + 31), fill=ORANGE)
        x += s + 10
def tabs(d, labels, active):
    y = Y0 + 6; widths = [d.textlength(t, font=f_tab) + 34 for t in labels]; x = X1 - sum(widths) - 12
    for i, (t, w) in enumerate(zip(labels, widths)):
        rr(d, (x, y, x + w + 12, y + 48), 24, fill=RED if i == active else GREY)
        d.text((x + 18, y + 8), t, font=f_tab, fill=WHITE); x += w
BAR_Y = 1384
def bottom_bar(d, back_hot=False):
    rr(d, (X0, BAR_Y, X0 + 130, Y1), 12, fill=(255, 200, 60) if back_hot else ORANGE)
    m = BAR_Y + 28
    d.polygon([(X0 + 24, m), (X0 + 52, m - 16), (X0 + 52, m - 6), (X0 + 104, m - 6), (X0 + 104, m + 6), (X0 + 52, m + 6), (X0 + 52, m + 16)], fill=DARK)
    d.text((X0 + 150, BAR_Y + 8), 'www.epsilon.plus', font=f_bar, fill=WHITE)
    rr(d, (X1 - 280, BAR_Y, X1, Y1), 28, fill=ORANGE); t = 'BLACK FRIDAY'; f = F('InterDisplay-Black.otf', 28)
    d.text((X1 - 140 - d.textlength(t, font=f) / 2, BAR_Y + 10), t, font=f, fill=DARK)
def cursor(im, x, y):
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (0, 54), (14, 42), (26, 68), (38, 61), (26, 37), (45, 37)]
    d.polygon([(x + a + 4, y + b + 4) for a, b in pts], fill=(0, 0, 0))
    d.polygon([(x + a, y + b) for a, b in pts], fill=(255, 226, 40), outline=(60, 40, 0))
def scanlines(im):
    a = np.asarray(im).astype(np.float32); a[1::4] *= 0.86; a[2::4] *= 0.93
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def price_block(d, x, y, was, now):
    d.ellipse((x, y + 6, x + 92, y + 98), fill=ORANGE); d.text((x + 25, y + 11), '$', font=F('InterDisplay-Black.otf', 68), fill=DARK)
    t = f'{now:,}'; d.text((x + 116, y - 8), t, font=f_price, fill=WHITE)
    wx = x + 124 + d.textlength(t, font=f_price) + 16; ws = f'${was:,}'
    d.text((wx, y + 36), ws, font=f_was, fill=GREY); tw = d.textlength(ws, font=f_was)
    d.line((wx - 6, y + 64, wx + tw + 6, y + 64), fill=RED, width=6)

CAR_Y = 520; CAR_W = X1 - X0; CAR_H = int(CAR_W * 420 / 720)          # 872 x 508
CC_BOX = (X1 - 290, 1128, X1, 1222)
def car_screen(car, k, colour, flash=0.0, cc_hot=False):
    c = CARS[car]; base = colour[3] == 'base'
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    icon_row(d); tabs(d, [c['make'], 'SPORT WING', 'PAINT MATCH'], 2)
    tw = d.textlength(c['title'], font=SERIF(104)); d.text((CX - tw / 2, 356), c['title'], font=SERIF(104), fill=WHITE)
    sw = d.textlength(c['sub'], font=f_code); d.text((CX - sw / 2, 482), c['sub'], font=f_code, fill=GREY)
    ci = car_img(car, k, '#8a8f96' if base else colour[2], base).resize((CAR_W, CAR_H), Image.LANCZOS)
    im.paste(ci, (X0, CAR_Y)); d = ImageDraw.Draw(im)
    y = 1040
    for t in ('BASE WING 30% OFF', 'PAINT MATCH AVAILABLE'):
        d.ellipse((X0, y + 6, X0 + 28, y + 34), fill=ORANGE); d.text((X0 + 42, y), t, font=f_small, fill=WHITE); y += 44
    name = colour[0]; f = f_col
    while d.textlength(name, font=f) > 440: f = f.font_variant(size=f.size - 2)
    d.text((X1 - d.textlength(name, font=f), 1034), name, font=f, fill=WHITE)
    if colour[1]: d.text((X1 - d.textlength(colour[1], font=f_code), 1084), colour[1], font=f_code, fill=GREY)
    allc = [BLACK] + c['colours']; n = len(allc); sw_ = 36
    for i, cc in enumerate(allc):
        x0 = X0 + i * (sw_ + 4); sel = cc[0] == colour[0]
        d.rectangle((x0, 1158 - (8 if sel else 0), x0 + sw_, 1194 + (8 if sel else 0)), fill=cc[2], outline=WHITE if sel else (70, 70, 70), width=3 if sel else 1)
    rr(d, CC_BOX, 46, fill=(255, 200, 60) if (cc_hot or flash > 0) else ORANGE)
    d.text((CC_BOX[0] + 44, CC_BOX[1] + 14), 'CHANGE', font=f_btn, fill=DARK); d.text((CC_BOX[0] + 56, CC_BOX[1] + 48), 'COLOR', font=f_btn, fill=DARK)
    d.ellipse((CC_BOX[0] + 200, CC_BOX[1] + 22, CC_BOX[0] + 250, CC_BOX[1] + 72), fill=colour[2], outline=DARK, width=4)
    was, now = c['base'] if base else c['special'].get(colour[1], c['paint'])
    price_block(d, X0, 1246, was, now)
    d.text((X0 + 118, 1340), 'GLOSS BLACK BASE WING' if base else 'PAINT-MATCHED WING', font=F('InterDisplay-Medium.otf', 26), fill=ORANGE)
    d.ellipse((X1 - 136, 1236, X1, 1372), outline=ORANGE, width=13); bw = d.textlength('BUY', font=f_buy)
    d.text((X1 - 68 - bw / 2, 1278), 'BUY', font=f_buy, fill=WHITE)
    bottom_bar(d)
    return im

TILE_Y = [444, 750, 1056]; TILE_H = 290
def tile_center(i): return (640, TILE_Y[i] + 170)
_tile = {}
def lineup_screen(hot=-1):
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    icon_row(d); tabs(d, ['Epsilon+', 'SPORT WING'], 1)
    rr(d, (CX - 150, 362, CX + 150, 426), 32, fill=RED); f = F('InterDisplay-Black.otf', 42); lw = d.textlength('LINEUP', font=f)
    d.text((CX - lw / 2, 370), 'LINEUP', font=f, fill=DARK)
    for i, car in enumerate(ORDER):
        c = CARS[car]; y = TILE_Y[i]
        if car not in _tile:
            g = car_img(car, 4, '#d8d8d8', False).convert('L').resize((650, 379), Image.LANCZOS).crop((60, 50, 590, 340))
            a = np.asarray(g).astype(np.float32) / 255
            t = np.stack([247 * (0.72 + 0.5 * a), 160 * (0.72 + 0.62 * a), 20 + 190 * a], -1).clip(0, 255).astype(np.uint8)
            _tile[car] = Image.fromarray(t)
        d.rectangle((X0, y, X1, y + TILE_H), fill=(255, 196, 70) if hot == i else ORANGE)
        im.paste(_tile[car], (X1 - 530, y)); d = ImageDraw.Draw(im)
        if hot == i: d.rectangle((X0, y, X1, y + TILE_H), outline=WHITE, width=6)
        d.text((X0 + 24, y + 16), c['title'], font=f_tile, fill=DARK)
        d.text((X0 + 28, y + 96), c['sub'], font=f_tile2, fill=DARK)
        d.ellipse((X0 + 24, y + 196, X0 + 88, y + 260), fill=DARK); d.text((X0 + 41, y + 199), '$', font=F('InterDisplay-Black.otf', 48), fill=ORANGE)
        d.text((X0 + 106, y + 186), str(c['base'][1]), font=f_tile, fill=DARK)
        ws = f"${c['base'][0]}"; wx = X0 + 106 + d.textlength(str(c['base'][1]), font=f_tile) + 20
        d.text((wx, y + 212), ws, font=f_tile2, fill=(110, 70, 0)); d.line((wx - 4, y + 236, wx + d.textlength(ws, font=f_tile2) + 4, y + 236), fill=(160, 30, 0), width=5)
    bottom_bar(d)
    return im

logo = Image.open(f'{M}/logo/banner_black.png').convert('RGBA'); la = logo.split()[3]
def logo_at(width, colr):
    l = Image.merge('RGBA', tuple(la.point(lambda v, c=c: c) for c in colr) + (la,))
    return l.resize((width, int(logo.height * width / logo.width)), Image.LANCZOS)
def offer_screen():
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    icon_row(d); tabs(d, ['Epsilon+', 'BLACK FRIDAY'], 1)
    t = 'Sport Wing'; tw = d.textlength(t, font=SERIF(124)); d.text((CX - tw / 2, 380), t, font=SERIF(124), fill=WHITE)
    rr(d, (X0 + 20, 580, X1 - 20, 720), 70, fill=ORANGE); t = 'BASE WING 30% OFF'; f = F('InterDisplay-Black.otf', 62)
    d.text((CX - d.textlength(t, font=f) / 2, 612), t, font=f, fill=DARK)
    rr(d, (X0 + 20, 750, X1 - 20, 890), 70, fill=RED); t = 'PAINT MATCH AVAILABLE'; f = F('InterDisplay-Black.otf', 52)
    d.text((CX - d.textlength(t, font=f) / 2, 788), t, font=f, fill=WHITE)
    y = 980
    for name, (was, now) in (('Civic Hatch / Sedan', (450, 315)), ('Integra', (500, 350))):
        d.text((X0 + 20, y + 26), name, font=f_small, fill=WHITE); price_block(d, 400, y - 10, was, now); y += 150
    bottom_bar(d)
    return im

# ---------- timeline ----------
ev = []      # (time, kind) for SFX
segs = []    # (b0, b1, fn(t, dur))
def lineup_seg(b0, b1, target, start_xy):
    tx, ty = tile_center(target)
    def fn(t, dur):
        p = min(1, t / (dur * 0.6)); p = p * p * (3 - 2 * p)
        x = start_xy[0] + (tx - start_xy[0]) * p; y = start_xy[1] + (ty - start_xy[1]) * p
        im = lineup_screen(target if p >= 1 else -1); cursor(im, x, y); return im
    segs.append((b0, b1, fn)); ev.append((bt(b0) + (bt(b1) - bt(b0)) * 0.6, 'tick')); ev.append((bt(b1), 'select'))
ROT = 10.0  # turntable angles per second (48 per turn)
def car_seg(car, b0):
    c = CARS[car]; seq = [BLACK] + c['colours']; t0 = bt(b0)
    cx, cy = CC_BOX[0] + 120, CC_BOX[1] + 52
    for i, colr in enumerate(seq):
        s0 = b0 if i == 0 else b0 + 1 + i; s1 = b0 + 2 if i == 0 else s0 + 1
        def fn(t, dur, colr=colr, i=i, s0=s0):
            tt_ = bt(s0) + t - t0; k = int(tt_ * ROT) % 48
            im = car_screen(car, k, colr, flash=1.0 if (i > 0 and t < 0.1) else 0, cc_hot=(i == 0 and t > dur * 0.7))
            if i == 0:
                p = min(1, t / (dur * 0.7)); p = p * p * (3 - 2 * p)
                sx, sy = tile_center(ORDER.index(car)); cursor(im, sx + (cx - sx) * p, sy + (cy - sy) * p)
            else: cursor(im, cx, cy + (6 if t < 0.08 else 0))
            return im
        segs.append((s0, s1, fn))
        if i > 0: ev.append((bt(s0), 'color'))
    return b0 + 2 + len(c['colours'])
lineup_seg(0, 3, 0, (200, 480))
e = car_seg('fl', 3)                                   # 3..17
lineup_seg(e, e + 2, 1, tile_center(0)); e = car_seg('fe', e + 2)    # 19..32
lineup_seg(e, e + 2, 2, tile_center(1)); e = car_seg('de5', e + 2)   # 34..46
segs.append((e, 50, lambda t, dur: offer_screen())); ev.append((bt(e), 'select'))
wl = logo_at(720, (255, 255, 255))
def logo_seg(t, dur):
    im = Image.new('RGB', (W, H), (0, 0, 0)); fade = min(1, t / 0.2, max(0, (dur - t) / 0.5))
    l = wl.copy(); l.putalpha(l.split()[3].point(lambda v: int(v * fade))); im.paste(l, (CX - 360, 860 - l.height // 2), l)
    d = ImageDraw.Draw(im); t_ = 'WWW.EPSILON.PLUS'; f = F('InterDisplay-Bold.otf', 44); g = int(200 * fade)
    d.text((CX - d.textlength(t_, font=f) / 2, 860 + l.height // 2 + 44), t_, font=f, fill=(g, g, g)); return im
segs.append((50, None, logo_seg))
print('end beat of car screens', e)

def frame_at(tsec):
    for b0, b1, fn in segs:
        s = 0.0 if b0 == 0 else bt(b0); en = END_T if b1 is None else bt(b1)
        fs, fe = int(round(s * FPS)), int(round(en * FPS))
        f = int(round(tsec * FPS))
        if fs <= f < fe: return scanlines(fn((f - fs) / FPS, (fe - fs) / FPS))
    return Image.new('RGB', (W, H))

if '--still' in sys.argv:
    for t in sys.argv[sys.argv.index('--still') + 1:]:
        frame_at(float(t)).save(f'{M}/still4_{t}.png')
    sys.exit()

# ---------- SFX (synthesised menu blips) ----------
SR = 48000
def tone(f0, f1, dur, vol, sq=0.35):
    n = int(SR * dur); t = np.arange(n) / SR; f = f0 + (f1 - f0) * t / dur; ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + sq * np.sign(np.sin(ph)); env = np.minimum(1, t / 0.003) * np.exp(-t / (dur * 0.35)); return vol * y * env
sfx = np.zeros(int(SR * (END_T + 1)), np.float32)
def put(t, y):
    i = int(t * SR); sfx[i:i + len(y)] += y[:max(0, len(sfx) - i)]
for t, kind in ev:
    if kind == 'tick': put(t, tone(1500, 1500, 0.04, 0.10))
    elif kind == 'select': put(t, tone(880, 880, 0.07, 0.22)); put(t + 0.07, tone(1320, 1320, 0.12, 0.22))
    elif kind == 'color': put(t, tone(1175, 1568, 0.09, 0.20))
w = wave.open(f'{M}/music/sfx_v03.wav', 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((sfx.clip(-1, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump({'events': [(round(t, 4), k) for t, k in ev]}, open(f'{M}/events_v03.json', 'w'))

nfr = int(round(END_T * FPS)); silent = OUT.replace('.mp4', '_silent.mp4')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
for f in range(nfr): p.stdin.write(frame_at(f / FPS).tobytes())
p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', f'{M}/music/music_v0.wav', '-i', f'{M}/music/sfx_v03.wav',
                '-filter_complex', '[1:a]volume=-5dB[m];[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0[s];[m][s]amix=inputs=2:normalize=0,volume=4.2dB[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(END_T), OUT], check=True)
print('wrote', OUT, nfr)
