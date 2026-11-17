"""BF 9 drive/drift variant compositor: Blender frames (drive_over.py) for f0-207, then the end card, -> PNG frames.

python compose_drive.py --render <dir with f_0000.png..> --logo "<Epsilon+ Logo.png>" --out <frames dir>
Same cut grid as v0.x (BREAKING NEWS): wordmark card on f208 (6.92 s hit), end f282 (9.4 s).
Safe zones (knowledge/safe-zones.md): the end card sits inside x 48-920 / y 285-1440, centred on x 484.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True)
ap.add_argument("--logo", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
W, H = 1080, 1920
C3, END = 208, 282
SAFE_CX = (48 + 920) / 2
UNB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../assets/fonts/unbounded/Unbounded-{}.ttf")
# knowledge/fonts.md: text next to the logo uses Unbounded (not Akira): 500 for the label, 400 for the URL
os.makedirs(args.out, exist_ok=True)

logo = Image.open(args.logo).convert("RGBA")
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)


def ease_out(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3


def text_layer(txt, size, fill=(255, 255, 255, 255), tracking=0, weight=500):
    f = ImageFont.truetype(UNB.format(weight), size)
    widths = [f.getlength(c) for c in txt]
    lay = Image.new("RGBA", (int(sum(widths) + tracking * (len(txt) - 1)) + 40, int(size * 1.4)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay); x = 20
    for c, w_ in zip(txt, widths):
        d.text((x, size * 0.15), c, font=f, fill=fill); x += w_ + tracking
    return lay


def paste_center(base, lay, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        lay = lay.resize((max(1, round(lay.width * scale)), max(1, round(lay.height * scale))), Image.LANCZOS)
    if alpha < 1.0:
        lay = lay.copy(); lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    base.alpha_composite(lay, (round(cx - lay.width / 2), round(cy - lay.height / 2)))


bf_lay = text_layer("BLACK FRIDAY", 54, tracking=10, weight=500)
url_lay = text_layer("WWW.EPSILON.PLUS", 36, (200, 200, 200, 255), tracking=6, weight=400)

for f in range(END):
    if f < C3:
        fr = Image.open(f"{args.render}/f_{f:04d}.png").convert("RGB").resize((W, H), Image.LANCZOS)
    else:
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        t = 0.35 + 0.65 * (f - C3) / 6
        paste_center(fr, bf_lay, SAFE_CX, 790, alpha=ease_out(t))
        paste_center(fr, logo, SAFE_CX, 900, scale=1.06 - 0.06 * ease_out(t), alpha=ease_out(t))
        paste_center(fr, url_lay, SAFE_CX, 1010, alpha=ease_out((f - C3 - 4) / 6))
        fade = min(1, (END - 1 - f) / 14)
        if fade < 1:
            fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, round(255 * (1 - fade)))))
    fr.convert("RGB").save(f"{args.out}/c_{f:04d}.png")
print("frames", END)
