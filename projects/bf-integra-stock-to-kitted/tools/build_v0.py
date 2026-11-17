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
import sys
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

M = "/home/user/media/bf-integra-stock-to-kitted"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # tools/track.py
OUT = os.environ.get("OUT", "/home/user/media/work/out/bf-integra-stock-to-kitted_v0.9.mp4")
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


ROW_SIZE, ROW_GAP, SCROLL = 300, 10, 150   # Anton px; px between rows; scroll speed px/s (rows alternate direction)
_ROWS = {}


def _row_strip(col):
    """One long, seamlessly tileable strip of 'BLACK FRIDAY ' in Anton, in one colour; returns (strip, period)."""
    if col in _ROWS:
        return _ROWS[col]
    f = ImageFont.truetype(FONT_BF, ROW_SIZE)
    unit = "BLACK FRIDAY  "
    per = round(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(unit, font=f))
    asc, desc = f.getmetrics()
    n = 2600 // per + 3
    im = Image.new("RGBA", (per * n, asc + desc), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for j in range(n):
        d.text((j * per, 0), unit, font=f, fill=col + (255,))
    top = f.getbbox("BLACK FRIDAY")[1]
    _ROWS[col] = (im.crop((0, top, im.width, asc)), per)  # trim to cap height so rows pack tight
    return _ROWS[col]


def flash_layer(t):
    """v0.8 (user: 'text takes up the whole background, ok if cut off, scrolling, colours alternating to the beat'):
    full-bleed wall of BLACK FRIDAY rows behind the stock scan (CGI only), tilted 12 deg, each row scrolling sideways
    (alternate rows opposite ways). On every beat of "140" the row colours swap white <-> sale red and the wall punches
    +6 % bigger and to full brightness, easing back over 0.22 s. The user allowed it to bleed off-frame: it is a
    background pattern, so it deliberately leaves the safe zone (logged as a user-approved exception)."""
    k = int((t - HIT0) // BEAT) if t >= HIT0 else -1
    e = max(0.0, 1 - (t - (HIT0 + k * BEAT)) / DECAY) ** 2 if k >= 0 else 0.0
    S = 2400  # square canvas, big enough to cover 1080x1920 after the tilt and the pulse
    cv = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    strip_h = _row_strip(WHITE)[0].height
    pitch = strip_h + ROW_GAP
    for r in range(S // pitch + 1):
        col = WHITE if (r + max(k, 0)) % 2 == 0 else SALE_RED
        strip, per = _row_strip(col)
        off = (t * SCROLL * (1 if r % 2 else -1) + r * per * 0.37) % per
        cv.alpha_composite(strip.crop((int(off), 0, int(off) + S, strip_h)), (0, r * pitch))
    cv = cv.rotate(TILT, resample=Image.BILINEAR)
    sc = 1 + 0.06 * e
    if sc > 1.001:
        cv = cv.resize((round(S * sc), round(S * sc)), Image.BILINEAR)
    cx, cy = cv.width // 2, cv.height // 2
    layer = cv.crop((cx - W // 2, cy - H // 2, cx - W // 2 + W, cy - H // 2 + H))
    a = 0.6 + 0.4 * e
    layer.putalpha(Image.fromarray((np.array(layer.split()[3]) * a).astype(np.uint8)))
    return layer


def load_flash(p, i):
    """Stock pass frame i (30 fps): charcoal, then the flash text, then the RGBA scan car on top."""
    car = Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    fl = flash_layer(i / 30.0)
    if fl is not None:
        bg.alpha_composite(fl)
    # v0.8: soft charcoal halo under the car so the silver scan separates from the white rows
    from PIL import ImageFilter
    halo = car.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(28))
    sh = Image.new("RGBA", (W, H), CHARCOAL + (0,)); sh.putalpha(halo.point(lambda v: min(255, int(v * 1.6))))
    bg.alpha_composite(sh)
    bg.alpha_composite(car)
    return bg.convert("RGB")


def load_kit(p):
    """v0.4: the RGBA kit render scaled to 60 % and placed inside the safe zone (x 48-920, y 285-1440) on charcoal."""
    im = Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)
    sm = im.resize((int(W * KIT_SCALE), int(H * KIT_SCALE)), Image.LANCZOS)
    bg = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    bg.alpha_composite(sm, (KIT_DX, KIT_DY))
    return bg.convert("RGB")


# v0.8 (user: "have the actual PU parts on the car highlighted (or the car blurred)" -> both shots): on the real
# footage the kit parts stay sharp with a sale-red edge glow while the rest of the frame is blurred, desaturated and
# dimmed. Part outlines were placed by hand on one key frame (edges read from brightness profiles / zoomed crops) and
# carried through the clip by tools/track.py. (key frame, polygon, tracking): "roi" = homography on features around the
# part; ("anchor", poly) = similarity on a rigid textured region (the 0370 wing stands proud of the trunk, so the
# trunk's motion carries it).
HL_PARTS = {
    "s3": [  # 0371 side pass, window pans nose -> tail
        (0, [(950, 1040), (990, 1036), (1015, 1030), (1030, 1030), (1038, 1045), (1032, 1053), (985, 1053), (952, 1050)], "roi"),  # lip
        (0, [(25, 1062), (150, 1074), (300, 1076), (450, 1071), (600, 1060), (712, 1055), (712, 1080), (600, 1084),
             (450, 1094), (300, 1101), (150, 1110), (25, 1117)], "roi"),  # skirt (edges from column profiles)
        (50, [(0, 683), (33, 686), (100, 690), (150, 702), (187, 712), (213, 728), (220, 750), (217, 777), (200, 781),
              (100, 789), (70, 790), (20, 786), (15, 775), (25, 765), (55, 768), (40, 745), (0, 716)], "roi"),  # wing
        (50, [(0, 1087), (10, 1080), (50, 1098), (100, 1120), (150, 1140), (183, 1153), (247, 1162), (247, 1197),
              (167, 1187), (100, 1173), (67, 1167), (50, 1150), (20, 1113)], "roi"),  # rear spat
    ],
    "s4": [  # 0370 rear 3/4, car closing on the camera
        (51, [(25, 630), (100, 611), (420, 613), (470, 626), (560, 679), (645, 722), (635, 738), (560, 735), (470, 690),
              (400, 650), (300, 640), (165, 640), (160, 720), (120, 720), (60, 700), (25, 650)],
         ("anchor", [(40, 760), (560, 760), (720, 800), (700, 880), (560, 960), (300, 1010), (60, 960), (30, 860)])),  # wing
        (0, [(118, 1088), (150, 1092), (205, 1100), (215, 1125), (190, 1145), (150, 1140), (125, 1130)], "roi"),  # L spat
        (0, [(640, 1160), (720, 1160), (752, 1150), (752, 1200), (700, 1225), (650, 1222), (625, 1190)], "roi"),  # R spat
        (0, [(840, 1072), (900, 1050), (950, 1018), (985, 994), (988, 1006), (950, 1033), (900, 1068), (845, 1090)], "roi"),  # skirt
    ],
}
HL_IN = {"s3": 13, "s4": 0}   # s3: the 1:1 cut plays clean for one beat (local frame 13 = 7.42 s), then the parts light up


def part_tracks(paths, clip):
    import cv2
    import track
    G = [cv2.imread(p, 0) for p in paths]
    out = []
    for key, poly, how in HL_PARTS[clip]:
        if how == "roi":
            out.append(track.track_poly(G, key, poly))
        else:
            out.append(track.track_anchor(G, key, poly, how[1], "sim"))
    return out


def highlight(path, polys, amt):
    """Real frame with the kit parts sharp + red edge glow, everything else blurred, half-desaturated, dimmed."""
    import cv2
    img = cv2.imread(path)
    if amt <= 0:
        return Image.fromarray(img[..., ::-1])
    m = np.zeros(img.shape[:2], np.uint8)
    for p in polys:
        cv2.fillPoly(m, [p.astype(np.int32)], 255)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    mf = cv2.GaussianBlur(m, (0, 0), 3).astype(np.float32) / 255
    ring = cv2.GaussianBlur(cv2.dilate(m, np.ones((9, 9), np.uint8)), (0, 0), 4).astype(np.float32) / 255
    ring = np.clip((ring - mf) * 1.5, 0, 1) * 0.35   # v0.9 (user: "too much, more subtle"): was 0.8
    bl = cv2.GaussianBlur(img, (0, 0), 3.5).astype(np.float32)  # was sigma 9
    bl = (0.8 * bl + 0.2 * bl.mean(2, keepdims=True)) * 0.8     # was 50 % desat, 55 % brightness
    out = img.astype(np.float32) * mf[..., None] + bl * (1 - mf[..., None])
    out = out * (1 - ring[..., None]) + np.array(SALE_RED[::-1], np.float32) * ring[..., None]
    out = img.astype(np.float32) * (1 - amt) + out * amt
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)[..., ::-1])


KIT2 = {}  # v0.8 kit shot placement, fitted once from the body pass (see fit_kit2)


def fit_kit2(body_paths, box=(60, 820, 910, 1400)):
    """Scale + offset so the car (union of the body pass alpha over the whole orbit) sits inside `box`
    (under the card, inside the owner safe zone x 48-920 / y 285-1440)."""
    acc = None
    for p in body_paths[::6] + body_paths[-1:]:
        a = np.array(Image.open(p).convert("RGBA").resize((W, H)).split()[3]) > 10
        acc = a if acc is None else (acc | a)
    ys, xs = np.nonzero(acc)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    sc = min((box[2] - box[0]) / (x1 - x0), (box[3] - box[1]) / (y1 - y0))
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    KIT2.update(sc=sc, dx=cx - sc * (x0 + x1) / 2, dy=cy - sc * (y0 + y1) / 2)


def load_kit2(parts_p, body_p):
    """v0.8 (user: parts highlighted on the car / car blurred): the website-model car body blurred and dimmed, the
    four kit parts sharp on top (body held out, so hidden faces stay hidden) with a sale-red edge glow."""
    from PIL import ImageFilter
    sc, dx, dy = KIT2["sc"], KIT2["dx"], KIT2["dy"]
    def place(p):
        im = Image.open(p).convert("RGBA").resize((W, H), Image.LANCZOS)
        im = im.resize((round(W * sc), round(H * sc)), Image.LANCZOS)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(im, (round(dx), round(dy)))
        return lay
    body, parts = place(body_p), place(parts_p)
    b = np.array(body.filter(ImageFilter.GaussianBlur(3.5))).astype(np.float32)  # v0.9: was blur 9 / 42 %
    b[..., :3] *= 0.7
    bg = Image.new("RGBA", (W, H), CHARCOAL + (255,))
    bg.alpha_composite(Image.fromarray(b.astype(np.uint8)))
    a = parts.split()[3]
    glow = a.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(4)).point(lambda v: min(255, int(v * 0.6)))
    g = Image.new("RGBA", (W, H), SALE_RED + (0,)); g.putalpha(glow)
    bg.alpha_composite(g)
    bg.alpha_composite(parts)
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
    s1 = doubled(os.path.join(M, "render/s1_stockpass_wheels/f_*.png"), n[0])
    s3 = video_frames(os.path.join(M, "clips/s3_0371_wide.mp4"), n[1], "s3")
    s4 = video_frames(os.path.join(M, "clips/s4_0370_wide.mp4"), n[2], "s4")
    s5 = doubled(os.path.join(M, "render/s5_parts_held/f_*.png"), n[3])      # v0.8: parts, body held out
    s5b = doubled(os.path.join(M, "render/s5_body/f_*.png"), n[3])           # v0.8: car body (blurred in post)
    fit_kit2(sorted(set(s5b)))
    i = 0
    for p in s1:
        load_flash(p, i).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for clip, paths in (("s3", s3), ("s4", s4)):
        tr = part_tracks(paths, clip)
        for k, p in enumerate(paths):
            amt = min(1.0, max(0.0, (k - HL_IN[clip] + 1) / 3.0))
            highlight(p, [t[k] for t in tr], amt).save(os.path.join(FR, f"f_{i:04d}.png")); i += 1
    for k, (p, pb) in enumerate(zip(s5, s5b)):
        card(load_kit2(p, pb), k).save(  # v0.1: no Del & Eps (owner: typical branding only)
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
