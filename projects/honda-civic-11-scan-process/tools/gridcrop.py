"""Crop a region of an image and draw a labelled pixel grid (full-res coords) for landmark picking.
usage: gridcrop.py img x0 y0 x1 y1 out.jpg [step] [scale]"""
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('RGB'); x0, y0, x1, y1 = map(int, sys.argv[2:6]); out = sys.argv[6]
step = int(sys.argv[7]) if len(sys.argv) > 7 else 50; sc = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
c = im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * sc), int((y1 - y0) * sc)), Image.LANCZOS); d = ImageDraw.Draw(c)
for x in range((x0 // step + 1) * step, x1, step):
    X = (x - x0) * sc; d.line([(X, 0), (X, c.height)], fill=(255, 0, 255) if x % (step * 2) == 0 else (0, 200, 255), width=1); d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // step + 1) * step, y1, step):
    Y = (y - y0) * sc; d.line([(0, Y), (c.width, Y)], fill=(255, 0, 255) if y % (step * 2) == 0 else (0, 200, 255), width=1); d.text((2, Y + 2), str(y), fill=(255, 255, 0))
c.save(out, quality=92)
