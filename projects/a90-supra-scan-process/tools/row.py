"""Side-by-side row of images (framing checks). usage: python row.py out.jpg img1 img2 ... [--h 640]"""
import sys
from PIL import Image
args = [a for a in sys.argv[2:] if not a.startswith("--")]
h = 640
ims = [Image.open(a).convert("RGB") for a in args]
ims = [i.resize((int(i.width * h / i.height), h)) for i in ims]
out = Image.new("RGB", (sum(i.width for i in ims) + 6 * (len(ims) - 1), h), (40, 40, 40))
x = 0
for i in ims:
    out.paste(i, (x, 0)); x += i.width + 6
out.save(sys.argv[1], quality=90)
