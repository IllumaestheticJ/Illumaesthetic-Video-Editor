"""Remove an isolated floating part from the top of a render: if the first run of bright rows ends > --gap px above the
next run (the car), paint rows [0, end+pad] with the background colour. Used for the parked wing peeking into S6.
    python mask_top.py src_dir dst_dir [--gap 60] [--max-top 260]"""
import glob, os, sys, shutil
import numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
gap = int(sys.argv[sys.argv.index("--gap") + 1]) if "--gap" in sys.argv else 60
max_top = int(sys.argv[sys.argv.index("--max-top") + 1]) if "--max-top" in sys.argv else 260
os.makedirs(dst, exist_ok=True)
n = 0
for f in sorted(glob.glob(os.path.join(src, "f_*.png"))):
    im = Image.open(f).convert("RGB"); a = np.asarray(im).copy(); L = a.mean(2)
    rows = np.where((L > 14).sum(1) > 3)[0]
    runs = np.split(rows, np.where(np.diff(rows) > 8)[0] + 1) if len(rows) else []
    if len(runs) >= 2 and runs[0][0] < max_top and runs[1][0] - runs[0][-1] > gap:
        a[: runs[0][-1] + 30] = (7, 7, 9); n += 1
        Image.fromarray(a).save(os.path.join(dst, os.path.basename(f)))
    else:
        shutil.copy(f, dst)
print("masked", n, "frames ->", dst)
