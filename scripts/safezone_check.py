#!/usr/bin/env python3
"""Check a 9:16 reel against the social-app safe zones (Reels / TikTok / Shorts).

Usage:
    python scripts/safezone_check.py OUT.mp4 [--every 0.5] [--sheet sheet.jpg] [--text-boxes boxes.json]

What it does
1. Samples frames every --every seconds and draws the danger zones over them, making a contact
   sheet you must LOOK at. Red = app UI covers it; amber = cropped in the home-feed 4:5 preview.
2. If --text-boxes is given (a JSON list of {"t0","t1","x","y","w","h","label"} in 1080x1920
   pixels, i.e. every caption/price/logo box the edit draws), it reports each box that touches a
   zone. Exit code 1 if any text box is in a red zone, or if a box flagged "key": true sits in
   the amber feed-crop zone.

Zones (1080x1920; scaled for other sizes): see knowledge/safe-zones.md.
"""
import argparse, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

W, H = 1080, 1920
# red: covered by app UI on at least one of Reels / TikTok / Shorts
RED = {
    "top (status bar, Reels/Following tabs)": (0, 0, 1080, 220),
    "bottom (caption, comments, audio, CTA)": (0, 1920 - 480, 1080, 1920),
    "right rail (like / comment / share)": (1080 - 160, 900, 1080, 1920 - 480),
    "left edge": (0, 220, 48, 1920 - 480),
}
# amber: outside the centred 4:5 (1080x1350) home-feed / grid preview crop
AMBER = {
    "feed crop top": (0, 0, 1080, 285),
    "feed crop bottom": (0, 1920 - 285, 1080, 1920),
}


def scale(box, w, h):
    sx, sy = w / W, h / H
    x0, y0, x1, y1 = box
    return (int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy))


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height:format=duration", "-of", "json", path])
    j = json.loads(out)
    return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"]["duration"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--every", type=float, default=0.5)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--text-boxes", default=None)
    a = ap.parse_args()
    w, h, dur = probe(a.video)
    if abs(w / h - 9 / 16) > 0.01:
        print(f"WARNING: {w}x{h} is not 9:16; zones are defined for 9:16 reels")
    sheet = a.sheet or os.path.splitext(a.video)[0] + "_safezones.jpg"
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps=1/{a.every},scale=270:-2",
                    os.path.join(tmp, "f_%04d.png")], check=True)
    frames = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
    tiles = []
    for f in frames:
        im = Image.open(os.path.join(tmp, f)).convert("RGBA")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for b in AMBER.values():
            d.rectangle(scale(b, im.width, im.height), fill=(255, 170, 0, 70))
        for b in RED.values():
            d.rectangle(scale(b, im.width, im.height), fill=(255, 0, 0, 90))
        tiles.append(Image.alpha_composite(im, ov).convert("RGB"))
    if tiles:
        cols = 8
        tw, th = tiles[0].size
        rows = (len(tiles) + cols - 1) // cols
        S = Image.new("RGB", (cols * tw, rows * th), "black")
        for i, t in enumerate(tiles):
            S.paste(t, ((i % cols) * tw, (i // cols) * th))
        S.save(sheet, quality=85)
        print(f"sheet: {sheet}  ({len(tiles)} frames, every {a.every}s) - LOOK at it: nothing that matters may sit in red; key text not in amber")
    bad = 0
    if a.text_boxes:
        for bx in json.load(open(a.text_boxes)):
            r = (bx["x"], bx["y"], bx["x"] + bx["w"], bx["y"] + bx["h"])
            for name, z in RED.items():
                if overlap(r, z):
                    print(f"RED  {bx.get('label','box')} {bx['t0']}-{bx['t1']}s hits {name}")
                    bad += 1
            for name, z in AMBER.items():
                if overlap(r, z):
                    lvl = "AMBER-KEY" if bx.get("key") else "amber"
                    print(f"{lvl} {bx.get('label','box')} {bx['t0']}-{bx['t1']}s is in {name}")
                    bad += 1 if bx.get("key") else 0
        print("text boxes: " + ("OK" if not bad else f"{bad} problem(s)"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
