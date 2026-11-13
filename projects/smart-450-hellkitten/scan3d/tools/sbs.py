"""sbs.py frame.png render.png out.jpg : side by side + 50% onion, both at render size"""
import sys
from PIL import Image
a = Image.open(sys.argv[1]).convert("RGB"); b = Image.open(sys.argv[2]).convert("RGB").resize(a.size)
w = 960; h = int(a.height * w / a.width)
a2, b2 = a.resize((w, h)), b.resize((w, h))
on = Image.blend(a2, b2, 0.5)
c = Image.new("RGB", (w * 3 + 20, h)); c.paste(a2, (0, 0)); c.paste(b2, (w + 10, 0)); c.paste(on, (2 * w + 20, 0)); c.save(sys.argv[3])
