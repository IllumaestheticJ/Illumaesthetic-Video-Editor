"""Lighting-dropout check: mean luma of every PNG in each render folder; flags step drops (> 35 % frame-to-frame) and dark frames.
    lumacheck.py dir [dir ...]"""
import os, sys, numpy as np
from PIL import Image
for d in sys.argv[1:]:
    fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    L = np.array([np.asarray(Image.open(f"{d}/{f}").convert("L").reduce(8), np.float32).mean() for f in fs])
    r = L[1:] / np.maximum(L[:-1], 1e-3)
    bad = [i + 1 for i in np.where((r < 0.65) | (r > 1.55))[0]]
    dark = [i for i in range(len(L)) if L[i] < 0.5 * np.median(L)]
    print(f"{'OK ' if not bad and not dark else 'BAD'} {d.split('/')[-1]:14s} n={len(L)} luma {L.min():.1f}-{L.max():.1f} median {np.median(L):.1f}"
          + (f" steps@{bad[:6]}" if bad else "") + (f" dark@{dark[:6]}..({len(dark)})" if dark else ""))
