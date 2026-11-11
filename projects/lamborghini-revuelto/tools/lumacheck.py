"""Lighting-dropout check (lessons: Cycles can drop every light mid-animation). Per-frame mean luma of each render dir;
flags frames whose luma falls >35 % below the median of their 7 neighbours.   lumacheck.py dir [dir ...]"""
import sys, glob, numpy as np
from PIL import Image
for d in sys.argv[1:]:
    fs = sorted(glob.glob(d + "/f_*.png"))
    L = np.array([np.asarray(Image.open(f).convert("L").reduce(8), float).mean() for f in fs])
    bad = [i + 1 for i in range(len(L)) if L[i] < 0.65 * np.median(L[max(0, i - 3):i + 4])]
    print(f"{d.split('/')[-1]:16s} n={len(L):3d} luma min {L.min():5.1f} med {np.median(L):5.1f} max {L.max():5.1f}  dropouts: {bad or 'none'}")
