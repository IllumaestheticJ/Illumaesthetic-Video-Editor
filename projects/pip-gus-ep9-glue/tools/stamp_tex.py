"""Ep 9 cartoon stamp texture: sage rubber-stamp mark reading "ASA / ABS" (approved script v4, line 12; cartoon only).

Usage: python stamp_tex.py OUT_DIR   -> OUT_DIR/stamp_asa_abs.png
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
FONT = REPO / "remotion/public/fonts/fjalla-one-latin-400-normal.woff2"
SAGE = (0x61, 0x9f, 0x73, 255)

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
W, H = 900, 420
im = Image.new("RGBA", (W, H), (0xec, 0xef, 0xec, 255))
d = ImageDraw.Draw(im)
d.rounded_rectangle((18, 18, W - 18, H - 18), radius=40, outline=SAGE, width=26)
f = ImageFont.truetype(str(FONT), 230)
t = "ASA / ABS"
bb = d.textbbox((0, 0), t, font=f)
d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), t, font=f, fill=SAGE)
im.save(out / "stamp_asa_abs.png")
print(out / "stamp_asa_abs.png")
