"""BF civic-parts-rain v0 - composite every output frame (1080x1920, 30 fps) from the renders + footage + overlays, then
encode with the music. Text only over scan/CGI/black (never over the IRL flash).

    python comp.py [--check]   -> /home/user/media/work/out/bf-civic-parts-rain_v0.mp4
Timeline (frames @30, music from the song start; cut times = measured onset peaks of the decoded track, see editlog):
  0-487   take (scan + rain + Ron's parts seating: lip 329, skirts 371, rear lip 435, wing 466)
  (v0.2: the IRL badge flash is cut - owner)
  488-593 Ron's render 7, hard 1:1 cut, gentle zoom OUT (no push-in)
  594-646 4a lookbook FE (Rallye Red), 647-693 4b lookbook FL (Boost Blue); offer text over both
  694-794 Epsilon+ wordmark (720 px) + 'SHOP DEALS NOW · WWW.EPSILON.PLUS' ; fade 780-794 (owner 2026-11-17: no Del & Eps - typical Epsilon+ branding only)
"""
import os, subprocess, sys, glob, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = "/home/user/media/bf-civic-parts-rain"; OUTD = f"{M}/comp"; os.makedirs(OUTD, exist_ok=True)
FINAL = "/home/user/media/work/out/bf-civic-parts-rain_v0.4.mp4"
W, H = 1080, 1920
# v0.4: music from MUSIC_START (owner: first scene too long); frames = (song time - MUSIC_START) * 30 on measured hits:
# lip 11.320, skirts 12.365, rear lip 13.436, wing 14.495, render-7 cut 15.534, FE 17.459, FL 19.792, end card 21.554, CTA 21.905, end 24.9
MUSIC_START = 9.25
F_LIP, F_SKIRT, F_REAR, F_WING, F_FLASH, F_R7, F_4A, F_4B, F_END, F_CTA, N = 62, 93, 126, 157, 189, 189, 246, 316, 369, 380, 470
BLUR = 5.0   # px at 1080 wide on the rain layer (owner: falling parts a bit blurred)
F_CH_IN, F_CH_OUT = 169, 300
OFF = (232, 236, 242)
ID_B = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"; ID_M = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
def font(p, s): return ImageFont.truetype(p, s)

SAFE_CX = 484
BOXES = {}   # text/logo boxes for scripts/safezone_check.py --text-boxes
def text(img, s, size, y, fpath=ID_B, track=6, alpha=1.0, fill=OFF, x=None):
    """centred (or left at x) text with letter tracking; alpha 0..1"""
    f = font(fpath, size); d = ImageDraw.Draw(img)
    widths = [d.textlength(c, font=f) for c in s]; tw = sum(widths) + track * (len(s) - 1)
    cx = SAFE_CX - tw / 2 if x is None else x   # v0.3: centred on the safe area x 48-920 (knowledge/safe-zones.md)
    x0 = cx; lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    for c, w in zip(s, widths):
        dl.text((cx, y), c, font=f, fill=fill + (int(255 * alpha),)); cx += w + track
    img.alpha_composite(lay)
    if alpha > 0:
        BOXES[(s, round(y))] = {"text": s, "x": int(x0), "y": int(y), "w": int(tw + 1), "h": int(size * 1.25),
                             "key": s in ("30% OFF", "THE FULL KIT", "SHOP DEALS NOW", "WWW.EPSILON.PLUS", "BLACK FRIDAY")}
    return tw

def env(f, a, b, fade=6):
    """0..1 envelope: in at a, out at b"""
    if f < a or f > b: return 0.0
    return min(1.0, (f - a + 1) / fade, (b - f + 1) / fade)

def layered(car_p, rain_p):
    """car layer + rain layer (transparent film, car held out), rain blurred with premultiplied alpha"""
    img = load(car_p)
    r = np.asarray(load(rain_p)).astype(np.float32) / 255.0
    a = r[..., 3:4]; pm = np.concatenate([r[..., :3] * a, a], 2)
    pm = np.stack([np.asarray(Image.fromarray((pm[..., k] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(BLUR))) for k in range(4)], 2).astype(np.float32) / 255.0
    al = pm[..., 3:4]; rgb = np.where(al > 1e-4, pm[..., :3] / np.maximum(al, 1e-4), 0)
    img.alpha_composite(Image.fromarray((np.concatenate([np.clip(rgb, 0, 1), al], 2) * 255).astype(np.uint8), "RGBA"))
    return img

def load(p, size=(W, H)):
    im = Image.open(p).convert("RGBA")
    return im if im.size == size else im.resize(size, Image.LANCZOS)

# --- assets
DEL = Image.open(f"{M}/chars/del_34_ph.png").convert("RGBA"); EPS = Image.open(f"{M}/chars/eps_34_ph.png").convert("RGBA")
def scaled(im, h): return im.resize((round(im.size[0] * h / im.size[1]), h), Image.LANCZOS)
DEL_L, EPS_L = scaled(DEL, 560), scaled(EPS, 560 * 562 * 588 // (516 * 634))
DEL_S, EPS_S = scaled(DEL, 470), scaled(EPS, 470 * 562 * 588 // (516 * 634))
EPS_SM = EPS_L.transpose(Image.FLIP_LEFT_RIGHT)
LOGO = Image.open(f"{M}/img/Epsilon+ Logo.png").convert("RGBA"); LOGO = LOGO.resize((720, round(LOGO.size[1] * 720 / LOGO.size[0])), Image.LANCZOS)
R7 = Image.open(f"{M}/img/7FinalSedanFL.jpg").convert("RGB")

def scan_reveal(img, ch, x, ybot, f, f_in, f_out, n=15):
    """paste a cut-out with a bottom->top scan-in (cyan edge) and a top->bottom scan-out"""
    if f < f_in or f > f_out + n: return
    h = ch.size[1]
    r = min(1.0, (f - f_in) / n) if f < f_out else max(0.0, 1 - (f - f_out) / n)
    if r <= 0: return
    vis = int(h * r); y0 = ybot - h
    part = ch.crop((0, h - vis, ch.size[0], h)); img.alpha_composite(part, (x, y0 + h - vis))
    if r < 1:
        a = np.asarray(ch)[max(0, h - vis - 3):h - vis + 3, :, 3] > 40
        line = Image.new("RGBA", (ch.size[0], a.shape[0]), (111, 195, 214, 0)); la = np.zeros(a.shape + (4,), np.uint8)
        la[a] = (111, 195, 214, 255); img.alpha_composite(Image.fromarray(la), (x, y0 + h - vis - 3))

def socket(img, cx, cy, ang):
    s = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.ellipse((25, 25, 125, 125), fill=(196, 199, 204, 255), outline=(240, 242, 245, 255), width=4)
    hexpts = [(75 + 26 * math.cos(math.radians(60 * k)), 75 + 26 * math.sin(math.radians(60 * k))) for k in range(6)]
    d.polygon(hexpts, fill=(20, 20, 22, 255))
    s = s.rotate(ang, resample=Image.BICUBIC); img.alpha_composite(s, (int(cx - 75), int(cy - 75)))

def frame(f):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    if f < F_FLASH:
        img = layered(f"{M}/renders/take_car/f_{f:04d}.png", f"{M}/renders/take_rain/f_{f:04d}.png")
        e = env(f, 3, 56, 6)
        if e: text(img, "BLACK FRIDAY", 96, 330, ID_B, 8, e)
        for a, b, s in ((F_LIP, F_SKIRT - 3, "FRONT LIP"), (F_SKIRT, F_REAR - 3, "SIDE SKIRTS"), (F_REAR, F_WING - 3, "REAR LIP"), (F_WING, F_R7 - 1, "SPORT WING")):
            e = env(f, a, b, 4)
            if e: text(img, s, 40, 1370, MONO, 8, e)
    elif f < F_R7:
        img = load(f"{M}/footage/flash/f_{f - F_FLASH + 1:04d}.png")
    elif f < F_4A:
        k = 1.0 - 0.03 * (f - F_R7) / (F_4A - F_R7)        # gentle zoom out (owner disliked push-ins on the end photo)
        s = 860 / 1180 * k; R = R7.resize((round(1920 * s),) * 2, Image.LANCZOS)   # v0.3: 860 px, inside the right rail
        img.paste(R, (round(SAFE_CX - 1020 * s), round(1000 - 942.5 * s)))
    elif f < F_END:
        car = "fe" if f < F_4B else "fl"; i = f - (F_4A if car == "fe" else F_4B)
        img = layered(f"{M}/renders/cgi_{car}_car/f_{i:04d}.png", f"{M}/renders/cgi_{car}_rain/f_{i:04d}.png")
        e = env(f, F_4A, F_END - 1, 5)
        text(img, "BLACK FRIDAY", 60, 300, ID_M, 14, e)
        text(img, "30% OFF", 176, 372, ID_B, 6, e)
        text(img, "THE FULL KIT", 88, 575, ID_B, 10, e)
        sub = "CIVIC FE · LIP · SKIRTS · REAR LIP · WING" if car == "fe" else "CIVIC FL · LIP · SKIRTS · WING"
        text(img, sub, 29, 1310, MONO, 3, e)
        text(img, "PAINT-MATCH AT FULL PRICE", 27, 1365, MONO, 4, e * 0.8)
    else:
        e = env(f, F_END, N + 20, 6)
        lg = LOGO.copy(); lg.putalpha(lg.getchannel("A").point(lambda v: int(v * e)))
        img.alpha_composite(lg, (SAFE_CX - LOGO.size[0] // 2, 840))
        BOXES[('logo', 840)] = {"text": "Epsilon+ wordmark", "x": SAFE_CX - LOGO.size[0] // 2, "y": 840, "w": LOGO.size[0], "h": LOGO.size[1], "key": True}
        e2 = env(f, F_CTA, N + 20, 6)
        if e2:
            text(img, "SHOP DEALS NOW", 58, 1010, ID_B, 10, e2)
            text(img, "WWW.EPSILON.PLUS", 46, 1090, ID_M, 12, e2)
    if f >= N - 15:  # picture fade to black
        k = max(0.0, 1 - (f - (N - 16)) / 15); blk = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - k)))); img.alpha_composite(blk)
    return img.convert("RGB")

if __name__ == "__main__":
    only = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and sys.argv[1] == "--frames" else None
    for f in (only or range(N)):
        frame(f).save(f"{OUTD}/c_{f:04d}.png" if not only else f"{OUTD}/check_{f:04d}.png")
    import json
    json.dump(list(BOXES.values()), open(f"{M}/comp/text_boxes.json", "w"), indent=1)
    if only: sys.exit()
    os.makedirs(os.path.dirname(FINAL), exist_ok=True)
    mus = f"{M}/music/freaked_out.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{OUTD}/c_%04d.png", "-ss", f"{MUSIC_START}", "-t", f"{N/30:.3f}", "-i", mus,
                    "-filter_complex", f"[1:a]afade=t=out:st={N/30-0.6:.3f}:d=0.6,volume={sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('dB') else '0dB'},alimiter=limit=0.82:level=disabled[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", FINAL], check=True)
    print("WROTE", FINAL)
