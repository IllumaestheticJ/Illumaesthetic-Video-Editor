"""Contact sheet of preview frames: python projects/subaru-wrx-vb/tools/sheet.py out.jpg dir1 dir2 ... (one row per dir)"""
import glob, os, sys
from PIL import Image, ImageDraw
rows = []
for d in sys.argv[2:]:
    fs = sorted(glob.glob(f"{d}/*.png"))
    rows.append((os.path.basename(d.rstrip("/")), [Image.open(f).convert("RGB") for f in fs]))
w, h = rows[0][1][0].size
n = max(len(r[1]) for r in rows)
S = Image.new("RGB", (w * n, h * len(rows)), (40, 40, 40))
for j, (name, ims) in enumerate(rows):
    for i, im in enumerate(ims):
        im = im.resize((w, h)); S.paste(im, (i * w, j * h))
    ImageDraw.Draw(S).text((4, j * h + 4), name, fill=(255, 255, 0))
S.save(sys.argv[1]); print(sys.argv[1], S.size)
