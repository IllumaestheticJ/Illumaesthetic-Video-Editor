"""Verify the delivered file: find cuts from frame differences (decoded at 30 fps, 108x192 grey) and report each
cut's error vs the nearest beat of the refined grid (t0 + n*B). Also reports duration, black/dup frames at cuts.
    python projects/honda-s2000/tools/cutcheck.py video.mp4 [--t0 0.0565 --beat 0.43463]"""
import argparse, subprocess
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("video")
ap.add_argument("--t0", type=float, default=0.0565); ap.add_argument("--beat", type=float, default=0.43463)
ap.add_argument("--thr", type=float, default=18.0)
a = ap.parse_args()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
d = np.abs(np.diff(f, axis=0)).mean((1, 2))
print(f"frames {len(f)} = {len(f)/30:.3f} s; mean luma first/last {f[0].mean():.1f}/{f[-1].mean():.1f}")
cuts = [i + 1 for i in range(len(d)) if d[i] > a.thr and d[i] > 3 * np.median(d[max(0, i - 5):i + 6])]
for c in cuts:
    t = c / 30; n = round((t - a.t0) / a.beat); bt = a.t0 + n * a.beat
    dup = d[c] < 0.5 if c < len(d) else False
    print(f"cut @ frame {c:4d} t={t:7.3f}  beat {n:3d} ({bt:.3f})  err {1000*(t-bt):+6.1f} ms ({(t-bt)*30:+.2f} fr)"
          f"  diff {d[c-1]:.1f}  next-frame-dup {d[c] < 0.3 if c < len(d) else '-'}  luma {f[c].mean():.0f}")
