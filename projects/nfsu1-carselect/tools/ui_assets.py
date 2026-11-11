"""Build the menu artwork for the Epsilon cars: logo-strip sprites and name plates, as premultiplied RGBA.

Lifted from the capture where the game has the make (Toyota, Mazda, Honda: 8th-percentile images per menu state,
minus the same without any logo); real artwork otherwise (Scion and Lotus emblems from Wikimedia, the GR COROLLA
badge texture from the GLB). Model names the game has no artwork for (del Sol, FR-S) are typeset in Inter.
    python ui_assets.py <work>/ui <work>/logos
"""
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ui, logos = sys.argv[1:3]
ST = ["honda", "peugeot", "mazda", "dodge", "mitsu", "toyota"]
p8 = {k: np.load(f"{ui}/p8_{k}.npy").astype(np.float32) for k in ST}
bg = np.min([p8[k] for k in ST], 0)
SLOT = {"L": 750, "C": 1086, "R": 1392}; SW = 322; Y0, Y1 = 20, 205
PL = (230, 410, 1150, 1850)                      # plate canvas rows, cols
P_WHITE = 220.0                                   # plate ink level (lerp alpha ~0.5 at pre ~110)


def strip_sprite(state, slot):
    x = SLOT[slot]
    pre = np.clip(p8[state][Y0:Y1, x - SW // 2:x + SW // 2] - bg[Y0:Y1, x - SW // 2:x + SW // 2], 0, 255)
    lum = pre.mean(2)
    keep = (cv2.dilate((lum > 42).astype(np.uint8), np.ones((11, 11), np.uint8)) > 0) & (lum > 12)
    pre[~keep] = 0
    a = np.clip(lum / 125.0, 0, 1) * keep
    return np.dstack([pre, a * 255]).astype(np.float32)


def art_sprite(path, h, cy, gain, canvas=(Y1 - Y0, SW)):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED).astype(np.float32)
    g = cv2.cvtColor(im[..., :3].astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    w = int(round(im.shape[1] * h / im.shape[0]))
    g = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA); al = cv2.resize(im[..., 3], (w, h), interpolation=cv2.INTER_AREA) / 255
    out = np.zeros(canvas + (4,), np.float32)
    y = int(cy - h / 2); x = (canvas[1] - w) // 2
    v = g * gain * al                               # premultiplied grey (the strip's logos are silver)
    out[y:y + h, x:x + w, :3] = v[..., None]; out[y:y + h, x:x + w, 3] = np.clip(al * (0.35 + 0.65 * g / 255), 0, 1) * 255
    return out


def text_img(txt, font, px, tracking=0):
    f = ImageFont.truetype(font, px)
    w = int(sum(f.getlength(c) + tracking for c in txt)) + 20
    im = Image.new("L", (w, int(px * 1.5)), 0); d = ImageDraw.Draw(im); x = 6
    for c in txt:
        d.text((x, int(px * 0.15)), c, 255, font=f); x += f.getlength(c) + tracking
    a = np.array(im); ys, xs = np.nonzero(a > 10)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32) / 255


def plate_from(state):
    r0, r1, c0, c1 = PL
    pre = np.clip(p8[state][r0:r1, c0:c1] - bg[r0:r1, c0:c1], 0, 255).mean(2)
    keep = cv2.dilate((pre > 32).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    pre[~keep | (pre < 7)] = 0
    return pre


def rows_split(pre):
    ink = (pre > 25).sum(1); ys = np.nonzero(ink > 3)[0]
    gaps = np.nonzero(np.diff(ys) > 3)[0]
    cut = (ys[gaps[0]] + ys[gaps[0] + 1]) // 2 if len(gaps) else (ys[0] + ys[-1]) // 2
    return ys[0], cut, ys[-1]


def put(canvas, ink, x, y, level=110.0):
    h, w = ink.shape
    canvas[y:y + h, x:x + w] = np.maximum(canvas[y:y + h, x:x + w], ink * level)


def save(name, pre_gray_or_rgba):
    a = pre_gray_or_rgba
    if a.ndim == 2:
        a = np.dstack([a, a, a, np.clip(a / P_WHITE, 0, 1) * 255])
    np.save(f"{ui}/assets/{name}.npy", a.astype(np.float32))
    v = np.clip(a[..., :3] * 2, 0, 255).astype(np.uint8)
    cv2.imwrite(f"{ui}/assets/{name}.png", v)


INTER = "/usr/share/fonts/opentype/inter/"
# ---- logo strip
save("strip_toyota_C", strip_sprite("toyota", "C")); save("strip_toyota_S", strip_sprite("mitsu", "R"))
save("strip_mazda_C", strip_sprite("mazda", "C")); save("strip_mazda_S", strip_sprite("dodge", "L"))
save("strip_honda_C", strip_sprite("honda", "C")); save("strip_honda_S", strip_sprite("peugeot", "L"))
save("strip_scion_C", art_sprite(f"{logos}/commons_Scion_logo.png", 104, 82, 0.62)); save("strip_scion_S", art_sprite(f"{logos}/commons_Scion_logo.png", 66, 106, 0.30))
save("strip_lotus_C", art_sprite(f"{logos}/en_Lotus_Cars_logo.png", 118, 84, 0.62)); save("strip_lotus_S", art_sprite(f"{logos}/en_Lotus_Cars_logo.png", 74, 106, 0.30))
# ---- plates
toy, hon, maz = plate_from("toyota"), plate_from("honda"), plate_from("mazda")
save("plate_mazda", maz)
for car, src, make_txt in (("corolla", toy, None), ("delsol", hon, None), ("frs", None, "Scion")):
    c = np.zeros_like(maz)
    if src is not None:
        y0, cut, y1 = rows_split(src); c[:cut] = src[:cut]
        xs = np.nonzero((src[cut:] > 25).sum(0))[0]; bx0, bx1 = xs.min(), xs.max(); by0 = cut + np.nonzero((src[cut:] > 25).sum(1))[0].min(); bh = y1 - by0
    else:
        y0, cut, y1 = rows_split(hon); xs = np.nonzero((hon > 25).sum(0))[0]; bx0, bx1 = xs.min(), xs.max(); by0 = cut + np.nonzero((hon[cut:] > 25).sum(1))[0].min(); bh = y1 - by0
        t = text_img(make_txt, INTER + "Inter-Medium.otf", 60); put(c, t, bx0, y0 + 2)
    if car == "corolla":
        b = cv2.imread(f"{logos}/decal_badge_grcorolla.png", cv2.IMREAD_UNCHANGED).astype(np.float32)
        g = cv2.cvtColor(b[..., :3].astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32) / 255 * (b[..., 3] / 255)
        w = bx1 - bx0 + 30; h = int(round(g.shape[0] * w / g.shape[1])); g = cv2.resize(g, (w, h), interpolation=cv2.INTER_AREA)
        g = np.clip((g - 0.12) * 1.5, 0, 1); put(c, g, bx0 - 10, by0 + (bh - h) // 2 + 4)
    else:
        txt = {"delsol": "del Sol", "frs": "FR-S"}[car]
        t = text_img(txt, INTER + "Inter-ExtraBoldItalic.otf", 200)
        h = bh + 6; w = int(round(t.shape[1] * h / t.shape[0])); t = cv2.resize(t, (w, h), interpolation=cv2.INTER_AREA); put(c, t, bx0, by0 - 3)
    save(f"plate_{car}", c)
save("plate_dodge_native", plate_from("dodge"))
print("ok")
