"""BF 9 v1.0 compositor: road scene 1 (drive_road.py) -> offer card (road still) -> road scene 3 (product car,
part falls off) -> end card. Nothing is pushed or scaled per frame (user 2026-11-18: the stock card "wiggling" must be still).

python compose_v10.py --s1 <frames> --card <still png> --s3 <frames> --logo "<Epsilon+ Logo.png>" --out <frames dir>

Timing (30 fps), cuts on measured hits of "BREAKING NEWS"; readability rule (lessons.md, revised 2026-11-18):
>= 1.8 s for 1-3 words + 0.3 s per extra word, >= 2.2 s for prices/offers.
  f0-153    scene 1: BLACK FRIDAY SALE -> car's nose on the text on the 2.48 s hit -> 3 DAYS LEFT clear ~3.1 s (2.0 s)
  f154-228  5.14 s hit: UP TO 60% OFF road still (2.5 s)
  f229-377  7.62 s hit: scene 3: COROLLA SKIRTS (1.8 s) -> car on the text on the 9.40 s hit, skirts fall off ->
            ONLY 2 LEFT clear ~10.0 s (2.6 s)
  f378-455  12.6 s hit: end card (Unbounded beside the logo), fade 14.7-15.2 s
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--s1", required=True)
ap.add_argument("--card", required=True)
ap.add_argument("--s3", required=True)
ap.add_argument("--logo", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
W, H = 1080, 1920
C_CARD, C_S3, C_END, END = 154, 229, 378, 456
CX = 540
UNB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../assets/fonts/unbounded/Unbounded-{}.ttf")
os.makedirs(args.out, exist_ok=True)


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


def up(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)


card = up(args.card)
logo = Image.open(args.logo).convert("RGBA")
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)
bf_lay = text_layer("BLACK FRIDAY", 54, tracking=10, weight=500)
url_lay = text_layer("WWW.EPSILON.PLUS", 36, (200, 200, 200, 255), tracking=6, weight=400)

for f in range(END):
    if f < C_CARD:
        fr = up(f"{args.s1}/f_{f:04d}.png")
    elif f < C_S3:
        fr = card  # held still: no push, no resampling per frame
    elif f < C_END:
        fr = up(f"{args.s3}/f_{f - C_S3:04d}.png")
    else:
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        t = 0.35 + 0.65 * (f - C_END) / 6
        paste_center(fr, bf_lay, CX, 850, alpha=ease_out(t))
        paste_center(fr, logo, CX, 960, scale=1.06 - 0.06 * ease_out(t), alpha=ease_out(t))
        paste_center(fr, url_lay, CX, 1070, alpha=ease_out((f - C_END - 4) / 6))
        fade = min(1, (END - 1 - f) / 15)
        if fade < 1:
            fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, round(255 * (1 - fade)))))
    fr.convert("RGB").save(f"{args.out}/c_{f:04d}.png")
print("frames", END)
