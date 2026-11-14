"""Contact sheet of PNG frames with labels. sheet.py out.jpg cols thumbw img1 [img2 ...]  (label = filename)"""
import sys, os
from PIL import Image, ImageDraw
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); fs = sys.argv[4:]
ims = [Image.open(f).convert("RGB") for f in fs]
th = int(ims[0].height * tw / ims[0].width)
rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (cols * tw, rows * th), (40, 40, 40)); d = ImageDraw.Draw(c)
for i, (im, f) in enumerate(zip(ims, fs)):
    x, y = (i % cols) * tw, (i // cols) * th
    c.paste(im.resize((tw, th)), (x, y)); d.text((x + 4, y + 4), os.path.basename(f), fill=(255, 255, 0))
    d.rectangle([x, y, x + tw - 1, y + th - 1], outline=(90, 90, 90))
c.save(out, quality=88); print(out, c.size)
