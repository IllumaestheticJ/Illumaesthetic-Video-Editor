"""Review images from the delivered file: contact sheet (every 24th frame) and +-2 frame strips around every cut.
usage: strips.py [delivered.mp4] [outdir]"""
import subprocess, sys, os
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, SM
f = sys.argv[1] if len(sys.argv) > 1 else f"{SM}/out/smart450_v3.mp4"
od = Path(sys.argv[2] if len(sys.argv) > 2 else f"{SM}/out"); od.mkdir(exist_ok=True, parents=True)
TW, TH = 216, 384
r = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"scale={TW}:{TH}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(r, np.uint8).reshape(-1, TH, TW, 3)
n = len(fr)
# contact sheet: every 24th frame, 9 per row
idx = list(range(0, n, 24))
cols = 9; rows = (len(idx) + cols - 1) // cols
sheet = Image.new("RGB", (cols * TW, rows * (TH + 14)), (15, 15, 15)); d = ImageDraw.Draw(sheet)
for k, i in enumerate(idx):
    x, y = (k % cols) * TW, (k // cols) * (TH + 14)
    sheet.paste(Image.fromarray(fr[i]), (x, y + 14)); d.text((x + 3, y + 1), f"f{i} {i/30:.2f}s", fill=(255, 255, 255))
sheet.save(od / "contact_sheet.jpg", quality=88)
# cut strips: 5 cuts per image
cuts = [s for s in SHOTS[1:]]
for part in range(0, len(cuts), 5):
    g = cuts[part:part + 5]
    img = Image.new("RGB", (5 * TW, len(g) * (TH + 14)), (15, 15, 15)); d = ImageDraw.Draw(img)
    for k, s in enumerate(g):
        for j, o in enumerate(range(-2, 3)):
            i = min(max(s["start"] + o, 0), n - 1)
            img.paste(Image.fromarray(fr[i]), (j * TW, k * (TH + 14) + 14))
            d.text((j * TW + 3, k * (TH + 14) + 1), f"{s['id']} cut f{s['start']} {o:+d} (f{i})", fill=(255, 255, 0) if o == 0 else (255, 255, 255))
    img.save(od / f"cut_strips_{part // 5 + 1}.jpg", quality=88)
print("frames", n, "->", od)
