"""Cut timing vs the DECODED audio of the delivered file: kick peaks (40-120 Hz onset) from the mp4's own audio,
cuts from frame differences; reports each cut's error to the nearest kick (target |err| <= 1/2 frame = 16.7 ms).
    python projects/honda-s2000/tools/kickcheck.py video.mp4 [--cuts 106,158,...]"""
import argparse, subprocess
import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--cuts"); ap.add_argument("--thr", type=float, default=10)
a = ap.parse_args()
sr = 22050
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                                 capture_output=True, check=True).stdout, np.int16).astype(float)
hop = 64; fr = sr / hop
low = sosfiltfilt(butter(4, [40, 120], "band", fs=sr, output="sos"), x)
n = len(low) // hop; e = np.sqrt((low[:n * hop].reshape(n, hop) ** 2).mean(1))
d = np.maximum(0, np.diff(e, prepend=e[0])); pk, _ = find_peaks(d, height=d.max() * 0.2, distance=int(fr * 0.15))
kicks = pk / fr
if a.cuts:
    cuts = [int(c) for c in a.cuts.split(",")]
else:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float); dv = np.abs(np.diff(f, axis=0)).mean((1, 2))
    cuts = [i + 1 for i in range(len(dv)) if dv[i] > a.thr and dv[i] > 3 * np.median(dv[max(0, i - 5):i + 6])]
errs = []
for c in cuts:
    t = c / 30; k = kicks[np.argmin(np.abs(kicks - t))]; errs.append(t - k)
    print(f"cut frame {c:4d} t={t:7.3f}  nearest kick {k:7.3f}  err {1000 * (t - k):+6.1f} ms")
errs = np.array(errs)
print(f"{len(kicks)} kicks decoded; |err| max {1000 * np.abs(errs).max():.1f} ms, within 1/2 frame: {np.mean(np.abs(errs) <= 1 / 60) * 100:.0f} %")
