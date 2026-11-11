"""Build a 30 fps PNG sequence from a 15 fps render plus real 30 fps in-between renders.

    python merge30.py <15fps dir> <30fps evens dir> <out dir>

30 fps frame j (1-based, t = (j-1)/30): odd j = 15 fps frame (j+1)/2 (same time); even j = the rendered in-between
if it exists (rendered where parts move fast: minterpolate smeared them), else a 50/50 blend of its two neighbours
(only on slow camera-only stretches, where it is invisible). Odd/rendered frames are symlinked.
"""
import os
import sys

import numpy as np
from PIL import Image

src15, src30, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
n15 = len([f for f in os.listdir(src15) if f.endswith(".png")])
rendered = blended = 0
for j in range(1, 2 * n15):
    dst = os.path.join(out, f"f_{j:04d}.png")
    if os.path.lexists(dst):
        os.remove(dst)
    if j % 2:
        os.symlink(os.path.join(src15, f"f_{(j + 1) // 2:04d}.png"), dst)
        continue
    r = os.path.join(src30, f"f_{j:04d}.png")
    if os.path.exists(r):
        os.symlink(r, dst)
        rendered += 1
        continue
    a = np.asarray(Image.open(os.path.join(src15, f"f_{j // 2:04d}.png")).convert("RGB"), np.float32)
    b = np.asarray(Image.open(os.path.join(src15, f"f_{j // 2 + 1:04d}.png")).convert("RGB"), np.float32)
    Image.fromarray(((a + b) / 2).round().astype(np.uint8)).save(dst)
    blended += 1
print(out, "frames", 2 * n15 - 1, "rendered in-betweens", rendered, "blended", blended)
