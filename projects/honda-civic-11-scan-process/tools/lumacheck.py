"""Lighting-dropout check: mean luma of every frame in PNG sequence dirs (or a video); flags frames that jump
more than --thresh (fraction) from the median of their neighbours (a flickering/missing light or a black frame).
usage: lumacheck.py dir_or_video [...] [--thresh 0.12]"""
import sys, glob, os, subprocess, numpy as np
from PIL import Image
args = [a for a in sys.argv[1:] if not a.startswith('--')]
th = float(sys.argv[sys.argv.index('--thresh') + 1]) if '--thresh' in sys.argv else 0.12
for src in args:
    if os.path.isdir(src):
        L = np.array([np.asarray(Image.open(f).convert('L').resize((135, 240))).mean() for f in sorted(glob.glob(src + '/*.png'))])
    else:
        raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', src, '-vf', 'scale=135:240', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
        L = np.frombuffer(raw, np.uint8).reshape(-1, 240 * 135).mean(1)
    bad = []
    for i in range(len(L)):
        nb = np.r_[L[max(0, i - 3):i], L[i + 1:i + 4]]
        if len(nb) and abs(L[i] - np.median(nb)) > th * max(np.median(nb), 8): bad.append((i, round(L[i], 1), round(float(np.median(nb)), 1)))
    print(f"{src}: {len(L)} frames, luma {L.min():.1f}-{L.max():.1f}, dropouts: {bad if bad else 'none'}")
