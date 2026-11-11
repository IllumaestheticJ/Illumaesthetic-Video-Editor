"""Lighting-dropout check: per-frame mean luma of every PNG render folder; flags frames < 60 % of the folder median
and steps > 25 % between neighbours.   python projects/porsche-gt3rs-992/tools/luma.py <dir> [<dir> ...]"""
import glob, sys
import numpy as np
from PIL import Image
for d in sys.argv[1:]:
    fs = sorted(glob.glob(f"{d}/*.png"))
    L = np.array([np.asarray(Image.open(f).convert("L").reduce(8), dtype=np.float32).mean() for f in fs])
    med = np.median(L); dark = [i + 1 for i in np.where(L < 0.6 * med)[0]]
    step = [i + 2 for i in np.where(np.abs(np.diff(L)) > 0.25 * med)[0]]
    print(f"{d.split('/')[-1]:14s} n={len(L):3d} median={med:5.1f} min={L.min():5.1f} max={L.max():5.1f} dark={dark[:10]} steps={step[:10]}")
