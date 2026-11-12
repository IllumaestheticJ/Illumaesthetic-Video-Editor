"""Contact sheet of preview stills: one row per shot (first | mid | last).
    python projects/porsche-gt3rs-992/tools/sheet.py <preview_dir> out.jpg [shot ...]"""
import glob, os, sys
from PIL import Image, ImageDraw
d, out, names = sys.argv[1], sys.argv[2], sys.argv[3:] or sorted(os.listdir(sys.argv[1]))
rows = []
for n in names:
    fs = sorted(glob.glob(f"{d}/{n}/f_*.png"))
    if fs: rows.append((n, [Image.open(f) for f in fs]))
w, h = rows[0][1][0].size; cols = max(len(r[1]) for r in rows)
s = Image.new("RGB", (w * cols, h * len(rows)))
for i, (n, ims) in enumerate(rows):
    for j, im in enumerate(ims): s.paste(im.resize((w, h)), (j * w, i * h))
    ImageDraw.Draw(s).text((6, i * h + 6), n, fill=(255, 255, 0))
s.save(out, quality=88); print(out)
