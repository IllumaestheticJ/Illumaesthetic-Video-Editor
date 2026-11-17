"""bf-integra-stock-to-kitted v0 builder: frame-exact concat of the 5 sections + card text + logo + music.

    python3 projects/bf-integra-stock-to-kitted/tools/build_v0.py

Timeline (30 fps, cuts = round(beat_time * 30) on the kick grid of "140" - Lil Texas, drop 6.991 s, beat 0.43073 s):
  S1   0-209  stock scan pass (Blender 15 fps, each frame doubled; ends on the solved 0371 crop camera)
  S3 210-260  REAL 0371 from the solved frame (1:1 hard cut on the drop)
  S4 261-312  REAL 0370 rear 3/4
  S5 313-468  GLB kit parts drop in (beats 9-12) + card text (beat 13). v0.1: Del & Eps removed (owner). v0.2: site palette
  S7 469-527  Epsilon+ wordmark, music fades out
No text on S3/S4 (IRL). Card text = sourced wording only (see draft_v0_notes.md).
"""
import glob
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

M = "/home/user/media/bf-integra-stock-to-kitted"
OUT = os.environ.get("OUT", "/home/user/media/work/out/bf-integra-stock-to-kitted_v0.7.mp4")
FR = os.path.join(M, "v0_frames")
W, H = 1080, 1920
CUTS = [0, 210, 261, 313, 469, 528]
CARD_ON = 378 - 313       # beat 13 (12.590 s), local frame in S5
# v0.2: epsilon.plus site palette + type (theme tokens read from the live homepage 2026-11-17)
CHARCOAL = (26, 26, 26)   # --background / --button-background-primary / --accent: 26 26 26
SALE_RED = (248, 58, 58)  # --on-sale-badge-background / announcement bar: 248 58 58
GREY = (178, 178, 178)    # #B2B2B2 secondary text
FONT_B = os.path.join(M, "fonts/barlow_n7.woff")   # --heading-font-family: Barlow 700 (site's own file)
FONT_R = os.path.join(M, "fonts/barlow_n4.woff")   # --text-font-family: Barlow 400


def load(p):
    """RGBA renders are composited onto the site charcoal; footage/RGB frames pass through."""
    im = Image.open(p)
    if im.mode == "RGBA":
        bg = Image.new("RGBA", im.size, CHARCOAL + (255,))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    return im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)


KIT_SCALE, KIT_DX, KIT_DY = 0.6, 139, 424   # v0.4 safe zones: kit content lands in x ~220-760, y ~700-1440


HIT0, BEAT = 0.215, 0.43073   # intro hits of "140" (hi-band onsets, measured), every beat until the drop
WHITE = (255, 255, 255)


FONT_BF = os.path.join(M, "fonts/Anton.ttf")   # v0.7: Anton (Google Fonts, OFL), condensed poster face for the BF wall
TILT, PULSE, DECAY = 12, 0.13, 0.22   # degrees CCW; peak extra scale on a hit; seconds back to rest
SAFE = (48, 285, 920, 1440)           # owner safe zone; the pulse PEAK must fit inside it
_BF = {}


def _bf_block():
    """A wall of BLACK (white) / FRIDAY (sale red) x2, each line set in Anton and scaled to one width (justified
    block), tilted. Four lines so the words read above AND below the car once it fills the frame."""
    if "img" in _BF:
        return _BF["img"]
    f = ImageFont.truetype(FONT_BF, 400)
    lines = []
    for txt, col in (("BLACK", WHITE), ("FRIDAY", SALE_RED)) * 2:
        x0, y0, x1, y1 = f.getbbox(txt)
        im = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((-x0, -y0), txt, font=f, fill=col + (255,))
        lines.append(im)
    bw = 1000
    lines = [im.resize((bw, round(im.height * bw / im.width)), Image.LANCZOS) for im in lines]
    gap = 36
    blk = Image.new("RGBA", (bw, sum(im.height for im in lines) + gap * (len(lines) - 1)), (0, 0, 0, 0))
    y = 0
    for im in lines:
        blk.alpha_composite(im, (0, y)); y += im.height + gap
    blk = blk.rotate(TILT, resample=Image.BICUBIC, expand=True)
    sw, sh = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
    _BF["base"] = min(sw / blk.width, sh / blk.height) / (1 + PULSE)  # peak fills the safe zone, rest is ~88 %
    _BF["img"] = blk
    return blk


def flash_layer(t):
    """v0.7: a tilted BLACK / FRIDAY wall fills the background BEHIND the stock scan (CGI only) and punches bigger and
    brighter on every beat of "140" (first hit 0.215 s, then every 0.43073 s), easing back between hits. At its peak
    it fills the owner safe zone x 48-920 / y 285-1440 and never leaves it."""
    blk = _bf_block()
    k = int((t - HIT0) // BEAT) if t >= HIT0 else -1
    e = max(0.0, 1 - (t - (HIT0 + k * BEAT)) / DECAY) ** 2 if k >= 0 else 0.0
    sc = _BF["base"] * (1 + PULSE * e)
    im = blk.resize((round(blk.width * sc), round(blk.height * sc)), Image.BILINEAR)
    a = 0.55 + 0.45 * e
    im.putalpha(Image.fromarray((np.array(im.split()[3]) * a).astype(np.uint8)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx, cy = (SAFE[0] + SAFE[2]) // 2, (SAFE[1] + SAFE[3]) // 2
    layer.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
    return layer


def load_flash(p, i):
    """Stock pass frame i (30 fps): charcoal, then the flash text, then the RGBA scan car on top."""
    car = Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    fl = flash_layer(i / 30.0)
    if fl is not None:
        bg.alpha_composite(fl)
    bg.alpha_composite(car)
    return bg.convert("RGB")


def load_kit(p):
    """v0.4: the RGBA kit render scaled to 60 % and placed inside the safe zone (x 48-920, y 285-1440) on charcoal."""
    im = Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)
    sm = im.resize((int(W * KIT_SCALE), int(H * KIT_SCALE)), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    bg.alpha_composite(sm, (KIT_DX, KIT_DY))
    return bg.convert("RGB")


def doubled(pattern, n):
    src = sorted(glob.glob(pattern))
    out = [s for s in src for _ in (0, 1)]
    while len(out) < n:  # hold the last (solved) pose
        out.append(out[-1])
    return out[:n]


def video_frames(mp4, n, tag):
    d = os.path.join(M, "tmp_" + tag)
    os.makedirs(d, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-frames:v", str(n), os.path.join(d, "f_%04d.png")], check=True)
    return sorted(glob.glob(os.path.join(d, "f_*.png")))[:n]


def text_center(d, y, s, font, fill=(255, 255, 255)):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill)


def card(im, k):
    """Card over the CGI kit shot (never over IRL), styled like the site: Barlow 700 caps in white, the offer in a
    sale-red badge (the site's on-sale badge colour), secondary lines in grey. Fades in over 4 frames."""
    a = min(1.0, (k - CARD_ON + 1) / 4.0)
    if a <= 0:
        return im
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    text_center(d, 300, "FULL KIT", ImageFont.truetype(FONT_B, 104))
    f = ImageFont.truetype(FONT_B, 150)
    t = "30%+ OFF"
    tw = d.textlength(t, font=f)
    x0, y0 = (W - tw) / 2 - 40, 410
    d.rounded_rectangle((x0, y0, x0 + tw + 80, y0 + 180), radius=26, fill=SALE_RED + (255,))
    d.text(((W - tw) / 2, y0 + 4), t, font=f, fill=(255, 255, 255))
    text_center(d, 610, "LIP  ·  SKIRTS  ·  SPATS  ·  SPORT WING", ImageFont.truetype(FONT_B, 44), (255, 255, 255))
    text_center(d, 664, "ACURA INTEGRA (DE4)", ImageFont.truetype(FONT_R, 40), GREY)
    layer.putalpha(Image.fromarray((np.array(layer.split()[3]) * a).astype(np.uint8)))
    base = im.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


LOGO = Image.open(os.path.join(M, "assets/Epsilon+ Logo.png")).convert("RGBA")


def logo_frame(k, n):
    lw = 720
    lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    a = min(1.0, (k + 1) / 5.0) * min(1.0, (n - k) / 8.0)
    im = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    l2 = lg.copy()
    l2.putalpha(Image.fromarray((np.array(lg.split()[3]) * a).astype(np.uint8)))
    im.alpha_composite(l2, ((W - lw) // 2, (H - lg.height) // 2))
    # v0.6 (owner, via parent): the only on-screen web address is WWW.EPSILON.PLUS, under the wordmark, in the safe zone
    tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    text_center(ImageDraw.Draw(tl), (H + lg.height) // 2 + 70, "WWW.EPSILON.PLUS", ImageFont.truetype(FONT_B, 60), GREY)
    tl.putalpha(Image.fromarray((np.array(tl.split()[3]) * a).astype(np.uint8)))
    im.alpha_composite(tl)
    return im.convert("RGB")


def main():
    os.makedirs(FR, exist_ok=True)
    for f in glob.glob(os.path.join(FR, "*.png")):
        os.remove(f)
    n = [CUTS[i + 1] - CUTS[i] for i in range(len(CUTS) - 1)]
    s1 = doubled(os.path.join(M, "render/s1_stockpass_wide/f_*.png"), n[0])
    s3 = video_frames(os.path.join(M, "clips/s3_0371_wide.mp4"), n[1], "s3")
    s4 = video_frames(os.path.join(M, "clips/s4_0370_wide.mp4"), n[2], "s4")
    s5 = doubled(os.path.join(M, "render/s5_kit_rgba/f_*.png"), n[3])
    i = 0
    for p in s1:
        load_flash(p, i).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for p in s3 + s4:
        load(p).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for k, p in enumerate(s5):
        card(load_kit(p), k).save(  # v0.1: no Del & Eps (owner: typical branding only)
            os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for k in range(n[4]):
        logo_frame(k, n[4]).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    assert i == CUTS[-1], i
    dur = CUTS[-1] / 30
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    music = os.path.join(M, "music/lil_texas_140.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", os.path.join(FR, "f_%04d.png"),
                    "-i", music, "-t", f"{dur:.4f}",
                    "-af", f"afade=t=out:st={dur - 0.45:.3f}:d=0.45,volume={os.environ.get('GAIN', '1.0')}",
                    "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", OUT], check=True)
    print("OUT", OUT, i, "frames")


if __name__ == "__main__":
    main()
