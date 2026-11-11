"""Per-frame mean luma of every render folder; flags frames < 50 % of the folder median (lighting dropout).
    luma.py renders/final"""
import glob, os, sys, numpy as np
from PIL import Image
for d in sorted(glob.glob(sys.argv[1] + "/*/")):
    fs = sorted(glob.glob(d + "f_*.png"))
    if not fs: continue
    L = np.array([np.asarray(Image.open(f).convert("L").reduce(4)).mean() for f in fs])
    med = np.median(L); bad = [os.path.basename(f) for f, l in zip(fs, L) if l < 0.5 * med]
    steps = np.abs(np.diff(L)); jump = steps.max() if len(steps) else 0
    print(f"{os.path.basename(d.rstrip('/')):14s} n={len(fs):3d} luma min {L.min():5.1f} med {med:5.1f} max {L.max():5.1f}  "
          f"max frame-to-frame step {jump:4.1f}  dark={bad[:6]}{'...' if len(bad) > 6 else ''}")
