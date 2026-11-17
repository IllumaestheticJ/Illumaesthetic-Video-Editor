"""BF 9 v0.1 compositor (no characters, owner 2026-11-17): plate + numeral frames + text -> PNG frames (30 fps, 1080x1920).

python compose_v0.py --media /home/user/media/bf-days-left-countdown --days 3 --out frames_dir
Cut frames come from the measured hits of "BREAKING NEWS" (see editlog): 1.96 s, drop 4.62 s, 6.92 s.
"""
import argparse, os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("--media", required=True)
ap.add_argument("--days", type=int, required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()
M = args.media
W, H, FPS = 1080, 1920, 30
C1, DROP, C3, END = 59, 139, 208, 282  # frames: shot 2 starts, drop, wordmark, end (9.4 s)
SLAM = 154      # 5.13 s hit: "DAYS LEFT"
SALE_IN = 180   # 6.01 s hit: "BLACK FRIDAY SALE" line
# safe zones (knowledge/safe-zones.md): text/logos/key subject inside x 48-920, y 285-1440
SAFE = (48, 285, 920, 1440)
SAFE_CX = (SAFE[0] + SAFE[2]) / 2  # 484
NUM_S = 0.72  # numeral render scale; content 780x956 px in the render -> 562x688
NUM_OFF = (round(SAFE_CX - 468 * NUM_S), round(330 - 270 * NUM_S))  # render content centre x 468, top y 270
BLACK_I = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
BOLD_I = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
os.makedirs(args.out, exist_ok=True)

plate = Image.open(f"{M}/work/plate_integra.png").convert("RGB")
logo = Image.open(f"{M}/src/Epsilon+ Logo.png").convert("RGBA")
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)

line = "LAST DAY" if args.days == 0 else ("DAY LEFT" if args.days == 1 else "DAYS LEFT")


def scaled(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def ease_out(t):
    t = min(max(t, 0), 1)
    return 1 - (1 - t) ** 3


def text_layer(txt, size, font=BLACK_I, fill=(255, 255, 255, 255), tracking=0, halo=True):
    f = ImageFont.truetype(font, size)
    chars = list(txt)
    widths = [f.getlength(c) for c in chars]
    tw = int(sum(widths) + tracking * (len(chars) - 1)) + 40
    th = int(size * 1.4)
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 20
    for c, w_ in zip(chars, widths):
        d.text((x, size * 0.15), c, font=f, fill=fill)
        x += w_ + tracking
    if halo:
        sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
        sh.putalpha(lay.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: min(255, v * 2)))
        out = Image.alpha_composite(sh, lay)
        return out
    return lay


def paste_center(base, lay, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        lay = lay.resize((max(1, round(lay.width * scale)), max(1, round(lay.height * scale))), Image.LANCZOS)
    if alpha < 1.0:
        a = lay.getchannel("A").point(lambda v: int(v * alpha)); lay = lay.copy(); lay.putalpha(a)
    base.alpha_composite(lay, (round(cx - lay.width / 2), round(cy - lay.height / 2)))


days_lay = text_layer(line, 118, tracking=5)
bf_lay = text_layer("BLACK FRIDAY", 64, BOLD_I, tracking=14, halo=False)
url_lay = text_layer("EPSILON.PLUS", 46, BOLD_I, (200, 200, 200, 255), tracking=10, halo=False)
sale_lay = text_layer("BLACK FRIDAY SALE", 52, BOLD_I, (215, 215, 215, 255), tracking=10)

for f in range(END):
    if f < C1:  # ---- shot 1: plate, crop-in + push
        s = 1.04 + 0.05 * f / (C1 - 1)  # push; car kept inside the safe box (knowledge/safe-zones.md)
        pl = plate.resize((round(W * s), round(H * s)), Image.LANCZOS)
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        fr.paste(pl, (round(SAFE_CX - 540 * s), round(960 - 960 * s)))
    elif f < C3:  # ---- shots 2-3: numeral render, text slam, sale line
        num = Image.open(f"{M}/work/num{args.days}/f_{f - C1:04d}.png").convert("RGBA")
        num = num.resize((round(W * NUM_S), round(H * NUM_S)), Image.LANCZOS)
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        fr.alpha_composite(num, NUM_OFF)
        # clip everything from the render (incl. the scan beam) to the safe box
        clip = Image.new("RGBA", (W, H), (0, 0, 0, 255)); clip.paste(fr.crop(SAFE), SAFE[:2]); fr = clip
        if f >= SLAM:
            t = (f - SLAM) / 4
            paste_center(fr, days_lay, SAFE_CX, 1110, scale=1.0 + 0.3 * (1 - ease_out(t)), alpha=ease_out(t * 1.5))
        if f >= SALE_IN:
            paste_center(fr, sale_lay, SAFE_CX, 1235, alpha=ease_out((f - SALE_IN) / 5))
    else:  # ---- shot 4: wordmark card, fades out with the music
        fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        t = 0.35 + 0.65 * (f - C3) / 6
        paste_center(fr, bf_lay, SAFE_CX, 790, alpha=ease_out(t))
        paste_center(fr, logo, SAFE_CX, 900, scale=1.06 - 0.06 * ease_out(t), alpha=ease_out(t))
        paste_center(fr, url_lay, SAFE_CX, 1010, alpha=ease_out((f - C3 - 4) / 6))
        fade = min(1, (END - 1 - f) / 14)
        if fade < 1:
            blk = Image.new("RGBA", (W, H), (0, 0, 0, round(255 * (1 - fade))))
            fr.alpha_composite(blk)
    fr.convert("RGB").save(f"{args.out}/c_{f:04d}.png")
print("frames", END)
