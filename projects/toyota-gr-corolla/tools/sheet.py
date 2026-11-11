"""Labelled contact sheet of still PNGs: sheet.py out.jpg a.png b.png ... [--cols 6] [--h 480]"""
import sys
from PIL import Image, ImageDraw
args = sys.argv[1:]
cols = int(args[args.index("--cols") + 1]) if "--cols" in args else 6
H = int(args[args.index("--h") + 1]) if "--h" in args else 480
files = [a for a in args[1:] if a.endswith((".png", ".jpg")) and a != args[0]]
ims = []
for f in files:
    im = Image.open(f).convert("RGB")
    im = im.resize((int(im.width * H / im.height), H))
    ImageDraw.Draw(im).text((6, 6), f.rsplit("/", 1)[-1][:40], fill=(255, 200, 0))
    ims.append(im)
w = ims[0].width
rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (w * cols, H * rows), (40, 40, 40))
for i, im in enumerate(ims):
    c.paste(im, ((i % cols) * w, (i // cols) * H))
c.save(args[0], quality=88)
print(args[0], c.size)
