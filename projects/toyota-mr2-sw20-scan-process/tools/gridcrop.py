"""Zoomed crop with a labelled pixel grid (full-res coords) for landmark picking.
usage: gridcrop.py img.png out.jpg x0 y0 x1 y1 [step=20] [scale=3] [img_scale=1 (if img is a 50% render use 2)]"""
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert("RGB"); x0, y0, x1, y1 = map(int, sys.argv[3:7])
step = int(sys.argv[7]) if len(sys.argv) > 7 else 20; sc = float(sys.argv[8]) if len(sys.argv) > 8 else 3
k = float(sys.argv[9]) if len(sys.argv) > 9 else 1
c = im.crop((int(x0 / k), int(y0 / k), int(x1 / k), int(y1 / k))).resize((int((x1 - x0) * sc), int((y1 - y0) * sc)), Image.LANCZOS)
d = ImageDraw.Draw(c)
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * sc; d.line([(X, 0), (X, c.height)], fill=(0, 255, 255) if x % 100 == 0 else (255, 0, 255), width=1)
    if x % 100 == 0 or step >= 50: d.text((X + 2, 2), str(x), fill=(0, 255, 0))
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * sc; d.line([(0, Y), (c.width, Y)], fill=(0, 255, 255) if y % 100 == 0 else (255, 0, 255), width=1)
    if y % 100 == 0 or step >= 50: d.text((2, Y + 2), str(y), fill=(0, 255, 0))
c.save(sys.argv[2])
