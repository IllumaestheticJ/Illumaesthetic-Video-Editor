"""Minimum distance (px) between any bright pixel and each frame edge, over ALL frames of each rendered shot.
A moving part that reaches 0 px has left the screen.  Keep >= 20 px unless the shot is a deliberate close-up.
  python edge_margins.py /home/user/media/work/renders/<car>/<shot> [more shot dirs ...]"""
import glob, sys
import numpy as np
from PIL import Image
for s in sys.argv[1:]:
    m = [10 ** 9] * 4
    for f in sorted(glob.glob(s.rstrip('/') + '/*.png')):
        a = np.asarray(Image.open(f).convert('L')); ys, xs = np.where(a > np.median(a) + 25)
        if len(xs) == 0: continue
        h, w = a.shape; m = [int(min(p, q)) for p, q in zip(m, [xs.min(), w - 1 - xs.max(), ys.min(), h - 1 - ys.max()])]
    print(f"{s.rstrip('/').split('/')[-1]:18s} min margin px  L {m[0]:4d}  R {m[1]:4d}  T {m[2]:4d}  B {m[3]:4d}" + ("   <-- under 20 px: check" if min(m) < 20 else ""))
