"""BF 9 v0.9 compositor: floor swap (drive_over.py, f0-180) -> offer card -> low-stock card -> end card.

python compose_v09.py --render <floor frames dir> --cardA <still png> --cardB <still png> --logo "<Epsilon+ Logo.png>" \
    --label "COROLLA HATCH SIDE SKIRTS" --out <frames dir>

Timing (30 fps), cuts on measured hits of "BREAKING NEWS" (20 ms RMS rises), sized by the readability rule
(knowledge/lessons.md: >= 2.5 s for 1-3 words + 0.4 s per extra word, >= 3 s for any price/offer):
  f0    BLACK FRIDAY SALE on the floor (readable until the car reaches it on the 2.48 s hit)
  ~f100 3 DAYS LEFT clear of the car                                  -> readable ~2.7 s
  f181  6.02 s hit  card A  "UP TO 60% OFF" (offer, 4 words)          -> 3.4 s
  f282  9.40 s hit  card B  "ONLY 2 LEFT" + product label (7 words)   -> 4.4 s (>= 4.1 s)
  f415  13.84 s hit end card BLACK FRIDAY / logo / WWW.EPSILON.PLUS    -> ~2.8 s readable, fade out to f519 (17.3 s)
Each card is a Blender still of the same floor (same camera as the floor render's last frame) with a slow digital push,
so the look continues across the cuts. Text next to the logo is Unbounded (knowledge/fonts.md).
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--render", required=True)
ap.add_argument("--cardA", required=True)
ap.add_argument("--cardB", required=True)
ap.add_argument("--logo", required=True)
ap.add_argument("--label", default="COROLLA HATCH SIDE SKIRTS")
ap.add_argument("--out", required=True)
args = ap.parse_args()
W, H = 1080, 1920
LAST_RENDER = 180
CA, CB, CE, END = 181, 282, 415, 519
CX, CY = 540, 960
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


def push(im, z):
    big = im.resize((round(W * z), round(H * z)), Image.LANCZOS)
    ox, oy = round(CX * z - CX), round(CY * z - CY)
    return big.crop((ox, oy, ox + W, oy + H))


def up(path):
    return Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)


cardA, cardB = up(args.cardA), up(args.cardB)
logo = Image.open(args.logo).convert("RGBA")
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)
bf_lay = text_layer("BLACK FRIDAY", 54, tracking=10, weight=500)
url_lay = text_layer("WWW.EPSILON.PLUS", 36, (200, 200, 200, 255), tracking=6, weight=400)
lab_lay = text_layer(args.label, 34, (215, 215, 215, 255), tracking=4, weight=500)
assert lab_lay.width - 40 <= 920 - 160, "label too wide for the safe box"

for f in range(END):
    if f < CA:  # floor swap render
        fr = up(f"{args.render}/f_{min(f, LAST_RENDER):04d}.png")
    elif f < CB:  # card A: offer; a light kick-in on the cut, then a slow push
        fr = push(cardA, 1.0 + 0.03 * (1 - ease_out((f - CA) / 6)) + 0.02 * (f - CA) / (CB - CA))
    elif f < CE:  # card B: low stock + the product it is about
        fr = push(cardB, 1.0 + 0.03 * (1 - ease_out((f - CB) / 6)) + 0.02 * (f - CB) / (CE - CB))
        fr = fr.convert("RGBA")
        paste_center(fr, lab_lay, CX, 1090, alpha=ease_out((f - CB - 3) / 6))
    else:  # end card (Unbounded beside the logo), fades out with the music
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        t = 0.35 + 0.65 * (f - CE) / 6
        paste_center(fr, bf_lay, CX, 850, alpha=ease_out(t))
        paste_center(fr, logo, CX, 960, scale=1.06 - 0.06 * ease_out(t), alpha=ease_out(t))
        paste_center(fr, url_lay, CX, 1070, alpha=ease_out((f - CE - 4) / 6))
        fade = min(1, (END - 1 - f) / 15)
        if fade < 1:
            fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, round(255 * (1 - fade)))))
    fr.convert("RGB").save(f"{args.out}/c_{f:04d}.png")
print("frames", END)
