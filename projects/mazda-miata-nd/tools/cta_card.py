"""Mobile call-to-action transition (user v3 feedback): the reassembled scan shrinks into a phone showing the car's
illumaesthetic.com listing (mobile screenshot, 360-degree viewer of this same scan), then the CTA text settles.

    python cta_card.py last_frame.png phone_screenshot.png out.mp4 [--secs 2.6]

Timeline (s): 0-0.55 car scales/moves into the phone's viewer area while the phone fades/slides up behind it;
0.40-0.75 car dissolves into the listing (same scan in the 360 viewer); 0.55-1.0 title + URL fade in; hold.
Text is factual: the listing exists (illumaesthetic.com/products/mazda-miata-nd-3d-scan-2016). No prices/specs on screen
beyond what the page itself shows.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (7, 7, 9)
INK = (232, 236, 242)
FONT_T = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_S = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def ramp(t, a, b):
    return ease((t - a) / (b - a))


def tracked(text, font, track, fill):
    w = int(sum(font.getlength(c) for c in text) + track * (len(text) - 1)) + 4
    h = int(font.size * 1.3)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = 0
    for c in text:
        d.text((x, 0), c, font=font, fill=fill)
        x += font.getlength(c) + track
    return im


def with_alpha(im, a):
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("last_frame")
    ap.add_argument("screenshot")
    ap.add_argument("out")
    ap.add_argument("--secs", type=float, default=2.6)
    ap.add_argument("--crop-h", type=int, default=1760, help="screenshot rows kept (below: a broken widget image)")
    ap.add_argument("--map", help="json {k, ox, oy}: the render frame (1080x1920) scaled by k with its top-left at (ox, oy)"
                    " in screenshot px lands 1:1 on the listing car (tools/solve_listing.py + the reassembly's last frame)")
    ap.add_argument("--fps", type=int, default=30, help="output frame rate (60 for the true-60 cut)")
    a = ap.parse_args()
    global FPS
    FPS = a.fps

    car = Image.open(a.last_frame).convert("RGB").resize((W, H), Image.LANCZOS)
    shot = Image.open(a.screenshot).convert("RGB")
    shot = shot.crop((0, 0, shot.width, min(shot.height, a.crop_h)))
    # phone: screen 700 px wide, 14 px bezel, rounded
    sw = 700
    sh = round(shot.height * sw / shot.width)
    screen = shot.resize((sw, sh), Image.LANCZOS)
    bez, rad = 16, 64
    pw, ph = sw + 2 * bez, sh + 2 * bez
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(phone)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), rad, fill=(22, 23, 26, 255), outline=(70, 72, 78, 255), width=3)
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), rad - bez, fill=255)
    scr = screen.convert("RGBA")
    scr.putalpha(mask)
    phone.alpha_composite(scr, (bez, bez))
    glow = Image.new("RGBA", (pw + 120, ph + 120), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((60, 60, pw + 59, ph + 59), rad, fill=(200, 210, 230, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(30))

    px, py = (W - pw) // 2, int(H * 0.51) - ph // 2  # phone top-left at rest
    # the listing's 360 viewer area (screenshot px 200..980 x 330..760) -> where the car lands
    vx0, vy0, vx1, vy1 = [v * sw / shot.width for v in (200, 330, 980, 760)]
    vcx, vcy = px + bez + (vx0 + vx1) / 2, py + bez + (vy0 + vy1) / 2
    vscale = (vx1 - vx0) / W * 1.35  # car frame (whole 1080 width) scaled so the car ~ fills the viewer
    sp = sw / shot.width  # screenshot px -> phone screen px
    if a.map:
        mp = json.load(open(a.map))
        s_end = mp["k"] * sp
        tl_end = (px + bez + mp["ox"] * sp, py + bez + mp["oy"] * sp)
        # tone the scan toward the listing's grey render as it lands (per-channel median gain on car pixels)
        sh_np = np.asarray(shot).astype(np.float32)
        lst = sh_np[int(330):int(700), 200:980].reshape(-1, 3); lst = lst[lst.mean(1) > 62]
        car_np = np.asarray(car).astype(np.float32).reshape(-1, 3); car_np = car_np[car_np.mean(1) > 40]
        gain = np.median(lst, 0) / np.maximum(1, np.median(car_np, 0))
    else:
        mp = None

    title = tracked("MIATA ND 3D SCAN", ImageFont.truetype(FONT_T, 70), 7, INK + (255,))
    sub = tracked("SCAN DATA AVAILABLE", ImageFont.truetype(FONT_S, 40), 9, INK + (210,))
    url = tracked("ILLUMAESTHETIC.COM", ImageFont.truetype(FONT_T, 50), 6, INK + (255,))

    n = int(round(a.secs * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                          "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        fr = Image.new("RGBA", (W, H), BG + (255,))
        # phone slides up 120 px and fades in
        ap_ = ramp(t, 0.05, 0.5)
        oy = int(120 * (1 - ap_))
        fr.alpha_composite(with_alpha(glow, ap_), (px - 60, py - 60 + oy))
        fr.alpha_composite(with_alpha(phone, ap_), (px, py + oy))
        # car: full frame -> into the viewer, then dissolves into the listing's own render of the scan
        m = ramp(t, 0.0, 0.55)
        if mp:
            s = float(np.exp(np.log(s_end) * m))  # log-scale zoom reads as a constant-speed pull-out
            x0, y0 = tl_end[0] * m, (tl_end[1] + oy) * m
            ac = 1.0 - ramp(t, 0.58, 0.88)
        else:
            s = 1.0 + (vscale - 1.0) * m
            x0 = W / 2 + (vcx - W / 2) * m - W * s / 2
            y0 = H / 2 + (vcy + oy - H / 2) * m - H * s / 2
            ac = 1.0 - ramp(t, 0.40, 0.75)
        if ac > 0:
            cw, chh = max(2, int(W * s)), max(2, int(H * s))
            c = car.resize((cw, chh), Image.LANCZOS)
            if mp:
                g = 1 + (gain - 1) * m
                c = Image.fromarray(np.clip(np.asarray(c).astype(np.float32) * g, 0, 255).astype(np.uint8))
            c = c.convert("RGBA")
            # black of the render -> transparent so it sits on the phone screen
            lum = np.asarray(c.convert("L")).astype(np.float32)
            al = np.clip((lum - 12) / 30, 0, 1) * ac
            c.putalpha(Image.fromarray((al * 255).astype(np.uint8)))
            fr.alpha_composite(c, (int(round(x0)), int(round(y0))))
        # text
        at = ramp(t, 0.55, 1.0)
        ty = py - 250 + int(30 * (1 - at))
        fr.alpha_composite(with_alpha(title, at), ((W - title.width) // 2, ty))
        fr.alpha_composite(with_alpha(sub, ramp(t, 0.7, 1.15)), ((W - sub.width) // 2, ty + 100))
        au = ramp(t, 0.85, 1.3)
        fr.alpha_composite(with_alpha(url, au), ((W - url.width) // 2, py + ph + 70))
        p.stdin.write(np.asarray(fr.convert("RGB")).tobytes())
    p.stdin.close()
    p.wait()
    print(a.out, n, "frames")


if __name__ == "__main__":
    main()
