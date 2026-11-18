"""bf-paint-match-roulette v0.2: retro "car dealership menu" version (owner reference: PS1-era racing game showroom).

Original UI drawn here (own icons, type and branding) in that genre's layout: lineup grid -> car screen with turntable,
colour name, CHANGE COLOR, price where the credits sit, BUY. Colours/prices: live store lists + BF liquidation sheet.
python3 compose_v02.py [--still t]  -> /home/user/media/work/out/bf-paint-match-roulette_v0.2.mp4
"""
import json, math, subprocess, os, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = '/home/user/media/bf-paint-match-roulette'
OUT = '/home/user/media/work/out/bf-paint-match-roulette_v0.11.mp4'
W, H, FPS = 1080, 1920, 30
B0, BP = 0.0903, 60 / 140.0
def bt(b): return B0 + BP * b
BASE_B, LINE0_B, LINE_B, OFFER_B, LOGO_B = 7, 8, 4, 10, 6   # v0.11 owner rule: hold text for slow readers (prices >= 3 s)
END_T = None

ORANGE = (247, 160, 20); RED = (240, 84, 28); GREY = (150, 150, 150); WHITE = (240, 240, 240); DARK = (30, 22, 4)
FI = '/usr/share/fonts/opentype/inter/'
def F(name, size): return ImageFont.truetype(FI + name, size)
UB = '/home/user/Illumaesthetic-Video-Editor/assets/fonts/unbounded/Unbounded-%d.ttf'
AKIRA = '/home/user/Illumaesthetic-Video-Editor/assets/fonts/akira/AkiraExpanded-SuperBold.otf'   # licensed, gitignored (knowledge/fonts.md)
def U(wt, size):
    """Akira Expanded for headlines / offers / big prices (weight >= 800, size >= 30); Unbounded for small labels and logo-adjacent text."""
    if wt >= 800 and size >= 30:
        f = ImageFont.truetype(AKIRA, int(round(size * 0.95))); f._akira_dy = int(round(size * 0.10)); return f   # 0.95: same line width as Unbounded 900
    return ImageFont.truetype(UB % wt, size)
_text0 = ImageDraw.ImageDraw.text
def _text(self, xy, text, *a, **k):
    f = k.get('font'); dy = getattr(f, '_akira_dy', 0)
    if dy: assert text.isascii(), text    # Akira has no non-ASCII glyphs
    return _text0(self, (xy[0], xy[1] + dy), text, *a, **k)
ImageDraw.ImageDraw.text = _text
SERIF = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', s)
f_tab = F('InterDisplay-Bold.otf', 36); f_stat = F('InterDisplay-Bold.otf', 44); f_small = F('InterDisplay-Bold.otf', 34)
f_price = F('InterDisplay-Black.otf', 104); f_was = F('InterDisplay-Bold.otf', 50); f_btn = F('InterDisplay-Black.otf', 30)
f_buy = F('InterDisplay-Black.otf', 58); f_tile = F('InterDisplay-Black.otf', 76); f_tile2 = F('InterDisplay-Black.otf', 44)
f_col = F('InterDisplay-Bold.otf', 46); f_code = F('InterDisplay-Medium.otf', 34)

col = json.load(open(f'{M}/renders/colours.json'))
BLACK = ['Gloss Black', '', '#0b0b0d', 'base']
CARS = {
 'fl': dict(make='Honda', logo='civic', title='Civic Hatch', sub='HATCHBACK · FL2 / FL5', base=(450, 315), paint=(850, 715), special={},
            colours=[['Championship White', 'NH0', '#f6f5ee', 'gloss'], ['Boost Blue Pearl', 'B637P', '#0a7ee8', 'pearl'],
                     ['Sonic Gray Pearl', 'NH877P', '#6e7886', 'pearl'], ['Rallye Red', 'R513', '#c8102e', 'gloss']] +
                    [c for c in col['FL'] if c[1] != 'NH877P']),
 'fe': dict(make='Honda', logo='civic', title='Civic Sedan', sub='SEDAN · FE', base=(450, 315), paint=(850, 715), special={'NH883P': (900, 765)},
            colours=[c for c in col['FE'][:1]] + [['Sonic Gray Pearl', 'NH877P', '#6e7886', 'pearl']] + col['FE'][1:5] +
                    [col['FE'][5], ['Rallye Red', 'R513', '#c8102e', 'gloss']] + col['FE'][6:]),
 'de5': dict(make='Acura', logo='integra', title='Integra Type S', sub='TYPE S · DE5', base=(500, 350), paint=(950, 800),
             special={'NH883P': (1000, 850)}, colours=col['DE'], third=None),   # owner: 3rd entry is the Type S (lookbook DE5 v19; no lip kit parts)
 'wb': dict(make='Acura', logo='integra', title='Integra Widebody', sub='WIDEBODY · DE4', base=(500, 350), paint=(950, 800), special={'NH883P': (1000, 850)},
            colours=[c for c in col['DE'] if c[1] != 'YR651P'], third='WIDEBODY FLARES 50% OFF'),   # owner: DE4 never came in Tiger Eye Pearl (Type S only)
           #     # sheet: Fender Flare Widebody DE4 $800 -> $400
}
assert len(CARS['fl']['colours']) == 12 and len(CARS['fe']['colours']) == 11 and len(CARS['de5']['colours']) == 10
ORDER = ['fl', 'fe', 'de5', 'wb']

# ---------- turntable frames + tint ----------
_yy, _xx = np.mgrid[0:420, 0:720].astype(np.float32)
VIG = (np.clip((420 - _yy) / 70, 0, 1) * np.clip(_xx / 60, 0, 1) * np.clip((720 - _xx) / 60, 0, 1))[..., None]
_tt = {}
def tt(car, k):
    key = (car, k)
    if key not in _tt:
        d = f'{M}/ttp/' + car + '/'   # v0.5: turntables with the Epsilon lip kits fitted
        _tt[key] = [np.asarray(Image.open(d + f'{t}_{k:02d}.png').convert('RGB')).astype(np.float32) / 255 for t in 'bwm']
        _tt[key].append(np.asarray(Image.open(d + f'p_{k:02d}.png').convert('RGBA')).astype(np.float32) / 255)   # v0.10: Epsilon+ rear plate layer (render_plate.py)
    return _tt[key]
def lin(h): return np.array([(int(h[i:i + 2], 16) / 255) ** 2.2 for i in (1, 3, 5)], np.float32)
def car_img(car, k, hexc, base_wing):
    b, w, m, pl = tt(car, k)
    lb, lw = b ** 2.2, w ** 2.2
    c = lin(hexc); wc = np.array([0.004] * 3, np.float32) if base_wing else c
    kk = m[..., 0:1] * c + (m[..., 1:2] + m[..., 2:3]) * wc   # wing and lip kit / flares: black on the base screen, paint-matched otherwise
    out = (lb + (lw - lb) * kk / 0.95).clip(0, 1) ** (1 / 2.2)
    out = out * (1 - pl[..., 3:4]) + pl[..., :3] * pl[..., 3:4]   # plate over the tinted car (straight alpha)
    return Image.fromarray((out * VIG * 255).astype(np.uint8))

# ---------- UI pieces (v0.3: everything inside the safe area x 48-920, y 285-1440; knowledge/safe-zones.md) ----------
X0, X1, Y0, Y1 = 48, 920, 285, 1440
CX = (X0 + X1) // 2
f_tab = F('InterDisplay-Bold.otf', 27); f_small = F('InterDisplay-Bold.otf', 30); f_col = F('InterDisplay-Bold.otf', 42)
f_code = F('InterDisplay-Medium.otf', 30); f_price = U(900, 74); f_was = U(700, 32)
f_btn = U(800, 20); f_buy = U(900, 34); f_tile = F('InterDisplay-Black.otf', 66)
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
    d.text((X0 + 148, BAR_Y + 12), 'www.epsilon.plus', font=U(400, 22), fill=WHITE)
    rr(d, (X1 - 280, BAR_Y, X1, Y1), 28, fill=ORANGE); t = 'BLACK FRIDAY'; f = U(800, 21)
    d.text((X1 - 140 - d.textlength(t, font=f) / 2, BAR_Y + 14), t, font=f, fill=DARK)
def cursor(im, x, y):
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (0, 54), (14, 42), (26, 68), (38, 61), (26, 37), (45, 37)]
    d.polygon([(x + a + 4, y + b + 4) for a, b in pts], fill=(0, 0, 0))
    d.polygon([(x + a, y + b) for a, b in pts], fill=(255, 226, 40), outline=(60, 40, 0))
def scanlines(im):
    a = np.asarray(im).astype(np.float32); a[1::4] *= 0.86; a[2::4] *= 0.93
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def price_block(d, x, y, was, now):
    d.ellipse((x, y + 6, x + 92, y + 98), fill=ORANGE); d.text((x + 23, y + 16), '$', font=U(900, 54), fill=DARK)
    t = f'{now:,}'; d.text((x + 112, y + 4), t, font=f_price, fill=WHITE)
    wx = x + 112 + d.textlength(t, font=f_price) + 16; ws = f'${was:,}'
    d.text((wx, y + 44), ws, font=f_was, fill=GREY); tw = d.textlength(ws, font=f_was)
    d.line((wx - 6, y + 66, wx + tw + 6, y + 66), fill=RED, width=5)

CAR_Y = 585; CAR_W = X1 - X0; CAR_H = int(CAR_W * 420 / 720)          # 872 x 508
CC_BOX = (X1 - 290, 1178, X1, 1258)
_lg = {}
def model_logo(name, width, colr):
    """Owner-supplied Civic / Integra wordmarks (logo/<name>_alpha.png), tinted and scaled to a width."""
    key = (name, width, colr)
    if key not in _lg:
        a = Image.open(f'{M}/logo/{name}_alpha.png').filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
        a = a.resize((width, max(1, int(a.height * width / a.width))), Image.LANCZOS)
        _lg[key] = Image.merge('RGBA', tuple(Image.new('L', a.size, c) for c in colr) + (a,))
    return _lg[key]
def car_screen(car, k, colour, flash=0.0, cc_hot=False):
    c = CARS[car]; base = colour[3] == 'base'
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    icon_row(d); tabs(d, [c['make'], 'SPORT WING', 'PAINT MATCH'], 2)
    lg = model_logo(c['logo'], 640 if c['logo'] == 'civic' else 700, (240, 240, 240))   # v0.8: Integra wordmark without the Acura badge (owner)
    im.paste(lg, (CX - lg.width // 2, 420 - lg.height // 2), lg); d = ImageDraw.Draw(im)
    fsub = U(600, 26); sw = d.textlength(c['sub'], font=fsub); d.text((CX - sw / 2, 488), c['sub'], font=fsub, fill=GREY)
    ci = car_img(car, k, BLACK[2] if base else colour[2], base).resize((CAR_W, CAR_H), Image.LANCZOS)   # owner: gloss black base wing only on a black car
    im.paste(ci, (X0, CAR_Y)); d = ImageDraw.Draw(im)
    y = 1092; fb = F('InterDisplay-Bold.otf', 24)
    for t in [x for x in ('BASE WING 30% OFF', 'PAINT MATCH AVAILABLE', c.get('third', 'FRONT LIP + SKIRTS 30% OFF')) if x]:   # sheet: lips/skirts 30 %
        d.ellipse((X0, y + 4, X0 + 22, y + 26), fill=ORANGE); d.text((X0 + 34, y), t, font=fb, fill=WHITE); y += 31
    name = colour[0]; f = f_col
    while d.textlength(name, font=f) > 400: f = f.font_variant(size=f.size - 2)
    d.text((X1 - d.textlength(name, font=f), 1086), name, font=f, fill=WHITE)
    if colour[1]: d.text((X1 - d.textlength(colour[1], font=f_code), 1134), colour[1], font=f_code, fill=GREY)
    allc = [BLACK] + c['colours']; n = len(allc); sw_ = 36
    for i, cc in enumerate(allc):
        x0 = X0 + i * (sw_ + 4); sel = cc[0] == colour[0]
        d.rectangle((x0, 1200 - (8 if sel else 0), x0 + sw_, 1236 + (8 if sel else 0)), fill=cc[2], outline=WHITE if sel else (70, 70, 70), width=3 if sel else 1)
    rr(d, CC_BOX, 46, fill=(255, 200, 60) if (cc_hot or flash > 0) else ORANGE)
    d.text((CC_BOX[0] + 40, CC_BOX[1] + 13), 'CHANGE', font=f_btn, fill=DARK); d.text((CC_BOX[0] + 50, CC_BOX[1] + 41), 'COLOR', font=f_btn, fill=DARK)
    d.ellipse((CC_BOX[0] + 200, CC_BOX[1] + 15, CC_BOX[0] + 250, CC_BOX[1] + 65), fill=colour[2], outline=DARK, width=4)
    was, now = c['base'] if base else c['special'].get(colour[1], c['paint'])
    if car == 'wb':      # owner: show both prices (wing + flares). Flares: sheet has only the PU price, $800 -> $400
        for yy, lab, (w_, n_) in ((1264, 'WING', (was, now)), (1322, 'FLARES', (800, 400))):
            d.ellipse((X0, yy + 4, X0 + 56, yy + 60), fill=ORANGE); d.text((X0 + 15, yy + 11), '$', font=U(900, 32), fill=DARK)
            t = f'{n_:,}'; fpp = U(900, 46); d.text((X0 + 70, yy + 4), t, font=fpp, fill=WHITE)
            wx = X0 + 70 + d.textlength(t, font=fpp) + 12; ws = f'${w_:,}'; fw = U(700, 22)
            d.text((wx, yy + 33), ws, font=fw, fill=GREY); d.line((wx - 4, yy + 48, wx + d.textlength(ws, font=fw) + 4, yy + 48), fill=RED, width=4)
            d.text((wx, yy + 4), lab, font=U(700, 18), fill=ORANGE)
    else:
        price_block(d, X0, 1272, was, now)
        wx = X0 + 112 + d.textlength(f'{now:,}', font=f_price) + 16
        d.text((wx, 1272 + 12), 'BASE WING' if base else 'PAINT-MATCHED', font=U(700, 19), fill=ORANGE)
    d.ellipse((X1 - 118, 1262, X1, 1380), outline=ORANGE, width=12); bw = d.textlength('BUY', font=U(900, 30))
    d.text((X1 - 59 - bw / 2, 1303), 'BUY', font=U(900, 30), fill=WHITE)
    bottom_bar(d)
    return im

TILE_Y = [440, 674, 908, 1142]; TILE_H = 222
def tile_center(i): return (640, TILE_Y[i] + 130)
_tile = {}
def lineup_screen(hot=-1):
    im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    icon_row(d); tabs(d, ['Epsilon+', 'SPORT WING'], 1)
    rr(d, (CX - 150, 362, CX + 150, 426), 32, fill=RED); f = U(900, 32); lw = d.textlength('LINEUP', font=f)
    d.text((CX - lw / 2, 376), 'LINEUP', font=f, fill=DARK)
    for i, car in enumerate(ORDER):
        c = CARS[car]; y = TILE_Y[i]
        if car not in _tile:
            g = car_img(car, 16, '#d8d8d8', False).convert('L').resize((560, 327), Image.LANCZOS).crop((40, 60, 520, 60 + TILE_H))
            a = np.asarray(g).astype(np.float32) / 255
            t = np.stack([247 * (0.72 + 0.5 * a), 160 * (0.72 + 0.62 * a), 20 + 190 * a], -1).clip(0, 255).astype(np.uint8)
            _tile[car] = Image.fromarray(t)
        d.rectangle((X0, y, X1, y + TILE_H), fill=(255, 196, 70) if hot == i else ORANGE)
        im.paste(_tile[car], (X1 - 480, y)); d = ImageDraw.Draw(im)
        if hot == i: d.rectangle((X0, y, X1, y + TILE_H), outline=WHITE, width=6)
        ft = U(900, 38); f2 = U(700, 22); fp = U(900, 46)
        lg = model_logo(c['logo'], 300 if c['logo'] == 'civic' else 340, DARK)
        im.paste(lg, (X0 + 22, y + 44 - lg.height // 2), lg); d = ImageDraw.Draw(im)
        d.text((X0 + 24, y + 82), c['sub'], font=f2, fill=DARK)
        d.ellipse((X0 + 22, y + 140, X0 + 78, y + 196), fill=DARK); d.text((X0 + 36, y + 147), '$', font=U(900, 34), fill=ORANGE)
        d.text((X0 + 94, y + 138), str(c['base'][1]), font=fp, fill=DARK)
        ws = f"${c['base'][0]}"; wx = X0 + 94 + d.textlength(str(c['base'][1]), font=fp) + 16
        d.text((wx, y + 160), ws, font=f2, fill=(110, 70, 0)); d.line((wx - 4, y + 175, wx + d.textlength(ws, font=f2) + 4, y + 175), fill=(160, 30, 0), width=4)
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
    rr(d, (X0 + 20, 580, X1 - 20, 720), 70, fill=ORANGE); t = 'BASE WING 30% OFF'; f = U(900, 44)
    d.text((CX - d.textlength(t, font=f) / 2, 620), t, font=f, fill=DARK)
    rr(d, (X0 + 20, 750, X1 - 20, 890), 70, fill=RED); t = 'PAINT MATCH AVAILABLE'; f = U(900, 36)
    d.text((CX - d.textlength(t, font=f) / 2, 796), t, font=f, fill=WHITE)
    y = 980
    for name, (was, now) in (('Civic Hatch / Sedan', (450, 315)), ('Integra', (500, 350))):
        d.text((X0 + 20, y + 26), name, font=f_small, fill=WHITE); price_block(d, 430, y - 10, was, now); y += 150
    bottom_bar(d)
    return im

# ---------- timeline ----------
ev = []      # (time, kind) for SFX
segs = []    # (b0, b1, fn(t, dur))
def lineup_seg(b0, b1, target, start_xy):
    tx, ty = tile_center(target)
    def fn(t, dur):
        p = min(1, t / min(dur * 0.6, 0.6)); p = p * p * (3 - 2 * p)
        x = start_xy[0] + (tx - start_xy[0]) * p; y = start_xy[1] + (ty - start_xy[1]) * p
        im = lineup_screen(target if p >= 1 else -1); cursor(im, x, y); return im
    segs.append((b0, b1, fn)); ev.append((bt(b1), 'select'))
    if b0 > 0: ev.append((bt(b0), 'back'))
ROT = 10.0  # turntable angles per second (48 per turn)
def car_seg(car, b0, step=1):
    c = CARS[car]; seq = [BLACK] + c['colours']; t0 = bt(b0)
    cx, cy = CC_BOX[0] + 120, CC_BOX[1] + 52
    for i, colr in enumerate(seq):
        s0 = b0 if i == 0 else b0 + BASE_B + (i - 1) * step; s1 = b0 + BASE_B if i == 0 else s0 + step
        def fn(t, dur, colr=colr, i=i, s0=s0):
            tt_ = bt(s0) + t - t0; k = int(tt_ * ROT) % 48
            im = car_screen(car, k, colr, flash=1.0 if (i > 0 and t < 0.1) else 0, cc_hot=(i == 0 and t > dur - 0.25))
            if i == 0:
                p = min(1, t / 0.6); p = p * p * (3 - 2 * p)
                sx, sy = tile_center(ORDER.index(car)); cursor(im, sx + (cx - sx) * p, sy + (cy - sy) * p)
            else: cursor(im, cx, cy + (6 if t < 0.08 else 0))
            return im
        segs.append((s0, s1, fn))
        if i > 0: ev.append((bt(s0), 'color'))
    return b0 + BASE_B + len(c['colours']) * step
lineup_seg(0, LINE0_B, 0, (200, 480))
e = car_seg('fl', LINE0_B)                                   # 3..17
lineup_seg(e, e + LINE_B, 1, tile_center(0)); e = car_seg('fe', e + LINE_B)    # 19..32
lineup_seg(e, e + LINE_B, 2, tile_center(1)); e = car_seg('de5', e + LINE_B)   # 34..46
lineup_seg(e, e + LINE_B, 3, tile_center(2)); e = car_seg('wb', e + LINE_B)       # 48..60; owner: even colour-change speed -> one colour per beat on every car
LOGO_S = e + OFFER_B; END_T = bt(LOGO_S + LOGO_B) + 0.5
segs.append((e, LOGO_S, lambda t, dur: offer_screen())); ev.append((bt(e), 'select'))
wl = logo_at(720, (255, 255, 255))
def logo_seg(t, dur):
    im = Image.new('RGB', (W, H), (0, 0, 0)); fade = min(1, t / 0.2, max(0, (dur - t) / 0.5))
    l = wl.copy(); l.putalpha(l.split()[3].point(lambda v: int(v * fade))); im.paste(l, (W // 2 - 360, 880 - l.height // 2), l)
    d = ImageDraw.Draw(im); t_ = 'WWW.EPSILON.PLUS'; f = U(300, 34); g = int(200 * fade)
    d.text((W // 2 - d.textlength(t_, font=f) / 2, 880 + l.height // 2 + 44), t_, font=f, fill=(g, g, g)); return im
segs.append((LOGO_S, None, logo_seg))
print('end beat of car screens', e)

# v0.6 (owner: "video needs to be centered"): the menu is drawn in the 872x1155 box, then scaled to 760 wide and centred on
# x = 540 (x 160-920, clear of the right rail), y 433-1440 (bottom edge on the safe line).
SCALE = 760 / (X1 - X0); BOX_W, BOX_H = 760, int(round((Y1 - Y0) * 760 / (X1 - X0))); BOX_X, BOX_Y = (W - 760) // 2, Y1 - int(round((Y1 - Y0) * 760 / (X1 - X0)))
def centre(im):
    out = Image.new('RGB', (W, H), (0, 0, 0))
    out.paste(im.crop((X0, Y0, X1, Y1)).resize((BOX_W, BOX_H), Image.LANCZOS), (BOX_X, BOX_Y)); return out
def frame_at(tsec):
    for b0, b1, fn in segs:
        s = 0.0 if b0 == 0 else bt(b0); en = END_T if b1 is None else bt(b1)
        fs, fe = int(round(s * FPS)), int(round(en * FPS))
        f = int(round(tsec * FPS))
        if fs <= f < fe:
            im = fn((f - fs) / FPS, (fe - fs) / FPS)
            return scanlines(im if fn is logo_seg else centre(im))
    return Image.new('RGB', (W, H))

if '--still' in sys.argv:
    for t in sys.argv[sys.argv.index('--still') + 1:]:
        frame_at(float(t)).save(f'{M}/still11_{t}.png')
    sys.exit()

# ---------- SFX (synthesised menu blips) ----------
SR = 48000
def sample(name, dur, lo, hi, gain):
    """Original menu sound recovered from the owner's reference capture (tools/extract_sfx.py), band-limited and trimmed."""
    from scipy.signal import butter, sosfiltfilt
    w_ = wave.open(f'{M}/sfx/{name}.wav'); r = w_.getframerate()
    y = np.frombuffer(w_.readframes(w_.getnframes()), np.int16).astype(np.float32) / 32768
    y = sosfiltfilt(butter(4, [lo, hi], 'bp', fs=r, output='sos'), y)[:int(dur * r)]
    n = int(0.12 * r); y[-n:] *= np.linspace(1, 0, n) ** 2
    y = np.interp(np.arange(int(len(y) * SR / r)) * r / SR, np.arange(len(y)), y)
    return (gain * y / np.abs(y).max()).astype(np.float32)
CONFIRM = sample('confirm', 0.62, 250, 6000, 0.50); BACK = sample('back', 0.50, 250, 3500, 0.42)
sfx = np.zeros(int(SR * (END_T + 1)), np.float32)
def put(t, y):
    i = int(t * SR); n = min(len(y), len(sfx) - i); sfx[i:i + n] += y[:n]
for t, kind in ev:
    put(t - 0.006, BACK if kind == 'back' else CONFIRM)     # sample attack starts ~6 ms into the clip
w = wave.open(f'{M}/music/sfx_v11.wav', 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((sfx.clip(-1, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump({'events': [(round(t, 4), k) for t, k in ev]}, open(f'{M}/events_v11.json', 'w'))

nfr = int(round(END_T * FPS)); silent = OUT.replace('.mp4', '_silent.mp4')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', silent], stdin=subprocess.PIPE)
for f in range(nfr): p.stdin.write(frame_at(f / FPS).tobytes())
p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', f'{M}/music/music_v11.wav', '-i', f'{M}/music/sfx_v11.wav',
                '-filter_complex', '[1:a]volume=-5dB[m];[2:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=-5dB[s];[m][s]amix=inputs=2:normalize=0,volume=4.2dB[a]',
                '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', str(END_T), OUT], check=True)
print('wrote', OUT, nfr)
