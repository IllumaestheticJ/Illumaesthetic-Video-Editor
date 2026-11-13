"""Copy a rendered frame folder, optionally holding the first frame, and dim a frame range so a centred title reads.
    python tools/dim.py SRC_DIR OUT_DIR [--hold N] --dim A:B[:LEVEL[:RAMP]]
Frames A..B (0-based, after the hold) are multiplied by LEVEL (default 0.38) with RAMP-frame ramps (default 4) at both ends."""
import argparse, glob, os, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--hold", type=int, default=0); ap.add_argument("--dim", required=True)
a = ap.parse_args(); d = a.dim.split(":"); A, B = int(d[0]), int(d[1]); lv = float(d[2]) if len(d) > 2 else 0.38; rp = int(d[3]) if len(d) > 3 else 4
fs = sorted(glob.glob(a.src + "/*.png")); seq = [fs[0]] * a.hold + fs; os.makedirs(a.out, exist_ok=True)
for o in glob.glob(a.out + "/*.png"): os.remove(o)
for i, f in enumerate(seq):
    k = float(np.clip(min(i - A, B - i) / rp, 0, 1)); g = 1 - (1 - lv) * k
    im = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    cv2.imwrite(f"{a.out}/f_{i+1:04d}.png", np.clip(im.astype(np.float32) * g, 0, 65535 if im.dtype == np.uint16 else 255).astype(im.dtype))
print(len(seq), "frames ->", a.out)
