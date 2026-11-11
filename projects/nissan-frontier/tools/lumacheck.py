"""Per-frame mean luma of every PNG in render folders - catches Cycles persistent-data lighting dropouts (WRX VA,
Cappuccino: lights lost mid-shot, no log error). Flags frames < --ratio x the folder median and big frame-to-frame steps.
  lumacheck.py dir [dir ...]"""
import sys, os, argparse
import numpy as np
from PIL import Image
ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+"); ap.add_argument("--ratio", type=float, default=0.5)
a = ap.parse_args()
bad_all = 0
for d in a.dirs:
    fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
    L = np.array([np.asarray(Image.open(os.path.join(d, f)).convert("L").reduce(8), np.float32).mean() for f in fs])
    med = np.median(L); bad = [fs[i] for i in np.where(L < med * a.ratio)[0]]
    step = np.abs(np.diff(L)) / (med + 1e-6); jumps = [fs[i + 1] for i in np.where(step > 0.25)[0]]
    bad_all += len(bad)
    print(f"{os.path.basename(d):14s} n={len(fs):4d} median={med:5.1f} min={L.min():5.1f} max={L.max():5.1f} dark={bad[:6]}{'...' if len(bad) > 6 else ''} jumps={jumps[:6]}")
sys.exit(1 if bad_all else 0)
