"""Contact sheet, one row per dir: python projects/subaru-wrx-vb/tools/sheet.py out.jpg dir1 dir2 ...
Env N=8 samples at most N evenly spaced frames per dir (final renders), W=200 thumbnail width."""
import glob, os, sys
from PIL import Image, ImageDraw
N, W = int(os.environ.get("N", 8)), int(os.environ.get("W", 200))
rows = []
for d in sys.argv[2:]:
    fs = sorted(glob.glob(f"{d}/*.png"))
    if len(fs) > N:
        fs = [fs[round(i * (len(fs) - 1) / (N - 1))] for i in range(N)]
    rows.append((os.path.basename(d.rstrip("/")), [Image.open(f).convert("RGB") for f in fs]))
w0, h0 = rows[0][1][0].size
w, h = W, round(W * h0 / w0)
n = max(len(r[1]) for r in rows)
S = Image.new("RGB", (w * n, h * len(rows)), (40, 40, 40))
for j, (name, ims) in enumerate(rows):
    for i, im in enumerate(ims):
        S.paste(im.resize((w, h)), (i * w, j * h))
    ImageDraw.Draw(S).text((4, j * h + 4), name, fill=(255, 255, 0))
S.save(sys.argv[1]); print(sys.argv[1], S.size)
