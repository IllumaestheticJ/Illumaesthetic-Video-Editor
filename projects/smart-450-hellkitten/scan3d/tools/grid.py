"""grid.py img out.jpg x0 y0 x1 y1 : crop with a labelled 50 px grid (pixel coords of the source image), scaled to 1000 wide"""
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert("RGB"); x0, y0, x1, y1 = map(int, sys.argv[3:7])
c = im.crop((x0, y0, x1, y1)); s = 1000 / c.width; c = c.resize((1000, int(c.height * s))); d = ImageDraw.Draw(c)
for x in range((x0 // 50 + 1) * 50, x1, 50):
    X = (x - x0) * s; d.line([(X, 0), (X, c.height)], fill=(255, 0, 255) if x % 100 == 0 else (0, 160, 255), width=1)
    if x % 100 == 0: d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // 50 + 1) * 50, y1, 50):
    Y = (y - y0) * s; d.line([(0, Y), (c.width, Y)], fill=(255, 0, 255) if y % 100 == 0 else (0, 160, 255), width=1)
    if y % 100 == 0: d.text((2, Y + 2), str(y), fill=(255, 255, 0))
c.save(sys.argv[2])
