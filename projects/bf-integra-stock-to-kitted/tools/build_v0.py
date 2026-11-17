"""bf-integra-stock-to-kitted v0 builder: frame-exact concat of the 5 sections + card text + logo + music.

    python3 projects/bf-integra-stock-to-kitted/tools/build_v0.py

Timeline (30 fps, cuts = round(beat_time * 30) on the kick grid of "140" - Lil Texas, drop 6.991 s, beat 0.43073 s):
  S1   0-209  stock scan pass (Blender 15 fps, each frame doubled; ends on the solved 0371 crop camera)
  S3 210-260  REAL 0371 from the solved frame (1:1 hard cut on the drop)
  S4 261-312  REAL 0370 rear 3/4
  S5 313-468  GLB kit parts drop in (beats 9-12) + card text (beat 13). v0.1: Del & Eps removed (owner)
  S7 469-527  Epsilon+ wordmark, music fades out
No text on S3/S4 (IRL). Card text = sourced wording only (see draft_v0_notes.md).
"""
import glob
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

M = "/home/user/media/bf-integra-stock-to-kitted"
OUT = os.environ.get("OUT", "/home/user/media/work/out/bf-integra-stock-to-kitted_v0.1.mp4")
FR = os.path.join(M, "v0_frames")
W, H = 1080, 1920
CUTS = [0, 210, 261, 313, 469, 528]
CARD_ON = 378 - 313       # beat 13 (12.590 s), local frame in S5
CHAR_ON = 391 - 313       # beat 14 (13.021 s)
FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FONT_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


def load(p):
    im = Image.open(p).convert("RGB")
    return im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)


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
    """Card text over the black CGI kit shot (never over IRL). Fades in over 4 frames."""
    a = min(1.0, (k - CARD_ON + 1) / 4.0)
    if a <= 0:
        return im
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    text_center(d, 140, "FULL KIT", ImageFont.truetype(FONT_B, 92))
    text_center(d, 245, "30%+ OFF", ImageFont.truetype(FONT_XB, 168))
    text_center(d, 465, "LIP  ·  SKIRTS  ·  SPATS  ·  SPORT WING", ImageFont.truetype(FONT_B, 40), (210, 210, 210))
    text_center(d, 525, "ACURA INTEGRA (DE4)", ImageFont.truetype(FONT_B, 40), (150, 150, 150))
    layer.putalpha(Image.fromarray((np.array(layer.split()[3]) * a).astype(np.uint8)))
    base = im.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


DEL = Image.open(os.path.join(M, "assets/del_placeholder.png")).convert("RGBA")
EPS = Image.open(os.path.join(M, "assets/eps_placeholder.png")).convert("RGBA")


def chars(im, k):
    """v0 PLACEHOLDER: model-sheet cut-outs (no Higgsfield generation yet), popped in on beat 14."""
    if k < CHAR_ON:
        return im
    s = min(1.0, 0.7 + 0.1 * (k - CHAR_ON))  # quick 3-frame pop
    base = im.convert("RGBA")
    for src, h, x, y in ((DEL, 420, 30, 1880), (EPS, 340, 720, 1880)):
        hh = int(h * s)
        c = src.resize((int(src.width * hh / src.height), hh), Image.LANCZOS)
        base.alpha_composite(c, (x, y - hh))
    d = ImageDraw.Draw(base)
    tag = ImageFont.truetype(FONT_B, 22)
    d.rectangle((30, 1418, 312, 1450), fill=(255, 40, 40, 255))
    d.text((40, 1420), "PLACEHOLDER: Del & Eps", font=tag, fill=(255, 255, 255))
    return base.convert("RGB")


LOGO = Image.open(os.path.join(M, "assets/Epsilon+ Logo.png")).convert("RGBA")


def logo_frame(k, n):
    lw = 720
    lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    a = min(1.0, (k + 1) / 5.0) * min(1.0, (n - k) / 8.0)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    l2 = lg.copy()
    l2.putalpha(Image.fromarray((np.array(lg.split()[3]) * a).astype(np.uint8)))
    im.alpha_composite(l2, ((W - lw) // 2, (H - lg.height) // 2))
    return im.convert("RGB")


def main():
    os.makedirs(FR, exist_ok=True)
    for f in glob.glob(os.path.join(FR, "*.png")):
        os.remove(f)
    n = [CUTS[i + 1] - CUTS[i] for i in range(len(CUTS) - 1)]
    s1 = doubled(os.path.join(M, "render/s1_stockpass/f_*.png"), n[0])
    s3 = video_frames(os.path.join(M, "clips/s3_0371.mp4"), n[1], "s3")
    s4 = video_frames(os.path.join(M, "clips/s4_0370.mp4"), n[2], "s4")
    s5 = doubled(os.path.join(M, "render/s5_kit/f_*.png"), n[3])
    i = 0
    for p in s1 + s3 + s4:
        load(p).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for k, p in enumerate(s5):
        card(load(p), k).save(  # v0.1: no Del & Eps (owner: typical branding only)
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
