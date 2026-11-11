"""Lighting-dropout check: per-frame mean luma of PNG sequences; flags frames whose luma drops > 25 % vs the running median.
    python lumacheck.py dir [dir ...]"""
import sys, glob, os, numpy as np
from PIL import Image
for d in sys.argv[1:]:
    fs = sorted(glob.glob(os.path.join(d, "f_*.png")))
    L = np.array([np.asarray(Image.open(f).convert("L").reduce(4), float).mean() for f in fs])
    med = np.array([np.median(L[max(0, i - 6):i + 7]) for i in range(len(L))])
    bad = np.where(L < 0.75 * med)[0]
    print(f"{os.path.basename(d):14s} n={len(L):3d} luma {L.min():5.1f}-{L.max():5.1f}  min/neighbour-median {np.min(L / med):.2f}  "
          + ("OK" if len(bad) == 0 else f"DROPOUT frames {[int(b) + 1 for b in bad]}"))
