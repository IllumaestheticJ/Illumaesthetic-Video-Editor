"""Short factual section labels over the removed-state scan shots -> transparent ProRes 4444 overlay (full reel length).

    python projects/toyota-gr-corolla/tools/labels.py labels.json out.mov

labels.json: {"frames": 1146, "fps": 30, "items": [{"text": "CRASH BEAM", "in": 800, "out": 822, "y": 220}, ...]}
House style (style-guide): Inter Display, tracking +6, off-white #e8ecf2, 96 px from the left edge, a short rule under
the text; 6-frame fade in/out; enter on a beat, leave before the cut. Wording only names what the scan files show.
"""
import json
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
W, H, X, SIZE, TRACK, COL = 1080, 1920, 96, 46, 6, (232, 236, 242)


def draw_label(img, text, y, alpha):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, SIZE)
    x = X
    a = int(255 * alpha)
    for ch in text:
        d.text((x, y), ch, font=f, fill=COL + (a,))
        x += f.getlength(ch) + TRACK
    d.line([(X, y + SIZE + 18), (X + 64, y + SIZE + 18)], fill=COL + (a,), width=3)


def main():
    cfg = json.load(open(sys.argv[1]))
    n, fps = cfg["frames"], cfg.get("fps", 30)
    with tempfile.TemporaryDirectory() as td:
        blank = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for i in range(n):
            im = blank.copy()
            for it in cfg["items"]:
                if it["in"] <= i < it["out"]:
                    al = min(1.0, (i - it["in"] + 1) / 6, (it["out"] - i) / 6)
                    draw_label(im, it["text"], it["y"], al)
            im.save(f"{td}/f_{i:05d}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", f"{td}/f_%05d.png",
                        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", sys.argv[2]], check=True)
    print(sys.argv[2])


if __name__ == "__main__":
    main()
