"""Part A animatic + look-dev contact sheet from the per-shot stills rendered by partA_scene.py.

Stills are held for their storyboard durations (version A, 465 frames at 30 fps). Burned in, for timing review only:
  - the script A dialogue lines as subtitles, in their script.md time windows (speaker-prefixed, small, lower safe area);
  - the planned on-screen titles as grey placeholder plates (the real text is a Remotion overlay later);
  - a shot tag in the top-left corner.
Silent stereo audio track. Nothing in the top 220 px or bottom 420 px except the shot tag.

Revised ending (S10-S12): the phone screen renders as key colour; the real IS350 frame (a clean graded source frame, P2's
first frame) is corner-pinned into it from screen_corners.json and keyed by the magenta so hands/heads stay in front. S12's
push is shown as a 2D zoom of its start still driven by the same corner data (exact for the screen, which is on the camera
axis; background parallax is not shown), ending full-frame at 17.3 s. A 1 s tail of the P2 frame follows so the hand-off
can be judged.

Usage: python partA_animatic.py --stills DIR --out DIR --footage P2_FIRST.png [--keep-frames]
Writes OUT/partA_animatic.mp4 and OUT/partA_lookdev.jpg.
"""
import argparse, json, math, os, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS = 30
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 220, 1920 - 420
SHOTS = [("S1", 0, 57), ("S2", 57, 110), ("S3", 110, 162), ("S4", 162, 200), ("S5", 200, 237),
         ("S6", 237, 283), ("S7", 283, 330), ("S8", 330, 375), ("S9", 375, 423), ("S10", 423, 459),
         ("S11", 459, 498), ("S12", 498, 519)]
TAIL = ("P2", 519, 549)   # real footage still after the cut (animatic only)
# script.md version A: (speaker, start s, end s, line)
LINES = [("PIP", 0.2, 1.9, "So... how do you scan a whole car?"),
         ("GUS", 1.9, 3.6, "The usual way? Dots. Lots of dots."),
         ("GUS", 3.7, 5.3, "One every few inches. Never in a row."),
         ("PIP", 5.5, 6.6, "Then you scan it?"),
         ("GUS", 6.7, 7.9, "In pieces."),
         ("GUS", 7.9, 9.4, "Front. Side. Roof. Back."),
         ("GUS", 9.5, 11.0, "Then I line them all up."),
         ("PIP", 11.1, 12.1, "Is it done yet?"),
         ("GUS", 12.1, 12.5, "No."),
         ("GUS", 12.6, 14.1, "Now we peel the dots off."),
         ("PIP", 14.1, 15.3, "Wait. I saw an Illumaesthetic video..."),
         ("PIP", 15.3, 16.6, "...they did a whole car way faster."),
         ("GUS", 16.6, 17.3, "...Show me.")]
# planned on-screen text per shot (script.md version A; only the sourced numbers ~8 CM, 4+, 3+)
TITLES = {"S1": ["HOW DO YOU 3D-SCAN", "A WHOLE CAR?"], "S2": ["THE USUAL WAY"],
          "S3": ["A DOT EVERY ~8 CM"], "S5": ["SCANNER NEEDS", "4+ DOTS IN VIEW"],
          "S6": ["OVERLAPPING SECTIONS"], "S7": ["MATCH 3+ POINTS", "PER PIECE"], "S9": ["THEN PEEL", "EVERY ONE OFF"]}
FONT_T = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
FONT_S = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FONT_TAG = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
OFF_WHITE, NEAR_BLACK, SAGE = (236, 239, 236), (11, 12, 11), (119, 172, 135)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def clock_inset(s8, s4):
    """S4's 'clock turning fast in a wall inset': a round crop of the S8 clock, pasted top-right inside the safe area."""
    meta = json.loads((s8.parent / "clock_px.json").read_text()) if (s8.parent / "clock_px.json").exists() else None
    im8 = Image.open(s8).convert("RGB")
    cx, cy, r = (meta["cx"], meta["cy"], meta["r"]) if meta else (510, 545, 175)
    crop = im8.crop((cx - r, cy - r, cx + r, cy + r)).resize((300, 300), Image.LANCZOS)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 299, 299), fill=255)
    base = Image.open(s4).convert("RGB")
    x0, y0 = 60, SAFE_TOP + 40   # top-left: empty floor in S4 (top-right had GUS)
    d = ImageDraw.Draw(base)
    d.ellipse((x0 - 10, y0 - 10, x0 + 310, y0 + 310), fill=NEAR_BLACK)
    base.paste(crop, (x0, y0), mask)
    return base


def perspective_coeffs(dst, src):
    """PIL PERSPECTIVE coefficients mapping output (dst) pixels to input (src) pixels."""
    import numpy as np
    A, b = [], []
    for (x, y), (X, Y) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -X * x, -X * y], [0, 0, 0, x, y, 1, -Y * x, -Y * y]]
        b += [X, Y]
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def key_mask(im):
    """Soft matte from the magenta key: 1 on the screen, 0 elsewhere (hands, bezel and heads in front stay)."""
    import numpy as np
    a = np.asarray(im, dtype=np.float32)
    m = np.clip((np.minimum(a[..., 0], a[..., 2]) - a[..., 1] - 40) / 80.0, 0, 1)
    return Image.fromarray((m * 255).astype("uint8"), "L")


def pin(still, footage, corners):
    fw, fh = footage.size
    warped = footage.transform((W, H), Image.PERSPECTIVE, perspective_coeffs(corners, [(0, 0), (fw, 0), (fw, fh), (0, fh)]),
                               Image.BICUBIC)
    out = still.copy()
    out.paste(warped, (0, 0), key_mask(still))
    return out


def zoom_about(im, cx, cy, k):
    """2D push: scale by k about (cx, cy), which stays put."""
    w, h = W / k, H / k
    x0, y0 = cx - cx / k, cy - cy / k
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + w, y0 + h), Image.BICUBIC)


def compose(still, shot, title, sub):
    im = still.copy()
    d = ImageDraw.Draw(im, "RGBA")
    # shot tag (review only)
    d.text((40, 40), f"{shot}  ANIMATIC", font=font(FONT_TAG, 30), fill=(236, 239, 236, 200), stroke_width=2,
           stroke_fill=(11, 12, 11, 200))
    if title:
        ft = font(FONT_T, 74)
        y = SAFE_TOP + 40
        for line in title:
            bw = d.textlength(line, font=ft)
            pad = 22
            d.rounded_rectangle((W / 2 - bw / 2 - pad, y - 8, W / 2 + bw / 2 + pad, y + 86), 14, fill=(11, 12, 11, 215))
            d.text((W / 2 - bw / 2, y), line, font=ft, fill=OFF_WHITE)
            y += 104
    if sub:
        spk, text = sub
        fs = font(FONT_S, 46)
        words = f"{spk}: {text}"
        # wrap to 2 lines max within 900 px
        lines, cur = [], ""
        for w in words.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=fs) > 900 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        y = SAFE_BOTTOM - 40 - 62 * len(lines)
        for i, line in enumerate(lines):
            bw = d.textlength(line, font=fs)
            d.rectangle((W / 2 - bw / 2 - 16, y - 6, W / 2 + bw / 2 + 16, y + 58), fill=(11, 12, 11, 170))
            x = W / 2 - bw / 2
            if i == 0:   # speaker name in sage
                name = f"{spk}:"
                d.text((x, y), name, font=fs, fill=SAGE)
                x += d.textlength(name + " ", font=fs)
                line = line[len(name):].lstrip()
            d.text((x, y), line, font=fs, fill=OFF_WHITE)
            y += 62
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--footage", required=True, help="clean 1080x1920 frame of the real footage for the phone screen")
    ap.add_argument("--keep-frames", action="store_true")
    a = ap.parse_args()
    st, out = Path(a.stills), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    seg_dir = out / "_segments"
    frm_dir = out / "_frames"
    for p in (seg_dir, frm_dir):
        shutil.rmtree(p, ignore_errors=True)
        p.mkdir()
    stills = {s: Image.open(st / f"{s}.png").convert("RGB") for s, _, _ in SHOTS}
    stills["S4"] = clock_inset(st / "S8.png", st / "S4.png")
    foot = Image.open(a.footage).convert("RGB")
    assert foot.size == (W, H), foot.size
    cj = json.loads((st / "screen_corners.json").read_text())
    stills["S11"] = pin(stills["S11"], foot, cj["shots"]["S11"]["corners"])
    stills["P2"] = foot
    s12 = cj["shots"]["S12"]
    a12, b12 = s12["frames"]
    c0 = s12["per_frame"][str(a12)]
    w0 = c0[1][0] - c0[0][0]
    cx0, cy0 = sum(p[0] for p in c0) / 4, sum(p[1] for p in c0) / 4
    total = TAIL[2]
    cache = {}
    for f in range(total):
        t = f / FPS
        shot = next((s for s, a0, b0 in SHOTS if a0 <= f < b0), TAIL[0])
        sub = next(((spk, txt) for spk, t0, t1, txt in LINES if t0 <= t < t1), None)
        title = TITLES.get(shot)
        key = (shot, sub) if shot != "S12" else (shot, sub, f)
        if key not in cache:
            p = seg_dir / f"seg{len(cache):03d}.png"
            if shot == "S12":
                cf = s12["per_frame"][str(f)]
                k = (cf[1][0] - cf[0][0]) / w0
                # the push keeps the screen centre fixed (camera on the screen axis); check against the 3D corners
                cxf, cyf = sum(q[0] for q in cf) / 4, sum(q[1] for q in cf) / 4
                assert abs(cxf - cx0) < 1.0 and abs(cyf - cy0) < 1.0, (f, cxf, cyf)
                img = foot.copy() if f == b12 - 1 else pin(zoom_about(stills["S12"], cx0, cy0, k), foot, cf)
            else:
                img = stills[shot]
            compose(img, shot, title, sub).save(p, compress_level=1)
            cache[key] = p
        os.symlink(cache[key], frm_dir / f"f{f:04d}.png")
    mp4 = out / "partA_animatic.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frm_dir / "f%04d.png"),
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                    "-map", "0:v", "-map", "1:a", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
                    "-frames:v", str(total), str(mp4)], check=True)
    # look-dev contact sheet: clean stills (no text), 5 x 2, labelled
    tw, th = 360, 640
    cols, rows = 6, 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 16, rows * th + (rows + 1) * 16 + rows * 44), (24, 26, 24))
    d = ImageDraw.Draw(sheet)
    for i, (s, a0, b0) in enumerate(SHOTS):
        r, c = divmod(i, cols)
        x, y = 16 + c * (tw + 16), 16 + r * (th + 16 + 44)
        # S11/S12 shown with the real frame pinned into the key-colour screen (as the compositor will)
        img = stills["S11"] if s == "S11" else pin(stills["S12"], foot, c0) if s == "S12" else Image.open(st / f"{s}.png").convert("RGB")
        sheet.paste(img.resize((tw, th), Image.LANCZOS), (x, y + 44))
        d.text((x, y + 6), f"{s}  {a0 / FPS:.1f}-{b0 / FPS:.1f} s", font=font(FONT_TAG, 26), fill=OFF_WHITE)
    sheet.save(out / "partA_lookdev.jpg", quality=90)
    if not a.keep_frames:
        shutil.rmtree(seg_dir)
        shutil.rmtree(frm_dir)
    print(mp4, out / "partA_lookdev.jpg", f"{len(cache)} segments, {total} frames")


if __name__ == "__main__":
    main()
