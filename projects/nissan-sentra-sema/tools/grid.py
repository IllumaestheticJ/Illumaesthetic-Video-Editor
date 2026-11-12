"""Zoomed crop with a labelled pixel grid, for picking landmarks. grid.py img x0 y0 x1 y1 out.jpg [scale] [step]"""
import sys
from PIL import Image, ImageDraw
img, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
sc = float(sys.argv[7]) if len(sys.argv) > 7 else 2; st = int(sys.argv[8]) if len(sys.argv) > 8 else 50
im = Image.open(img).convert("RGB").crop((x0, y0, x1, y1)); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range((x0 // st + 1) * st, x1, st):
    X = (x - x0) * sc; d.line([(X, 0), (X, im.height)], fill=(0, 255, 255), width=1); d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // st + 1) * st, y1, st):
    Y = (y - y0) * sc; d.line([(0, Y), (im.width, Y)], fill=(0, 255, 255), width=1); d.text((2, Y + 2), str(y), fill=(255, 255, 0))
im.save(out, quality=88); print(out, im.size)
