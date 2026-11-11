"""Measure every hard cut of a delivered mp4 against the kick onsets in ITS OWN decoded audio.
Cuts: frame-difference peaks. Onset: half-rise of a 1 ms broadband RMS envelope (a low-passed envelope reads 40-70 ms
late - WRX VA lesson), searched -60..+80 ms around each cut.
  cutcheck.py out.mp4 [--min-diff 15]"""
import argparse, subprocess
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("--min-diff", type=float, default=15)
a = ap.parse_args()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.mp4, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(np.float32)
d = np.abs(np.diff(v, axis=0)).mean((1, 2))
cuts = [i + 1 for i in range(1, len(d) - 1) if d[i] > a.min_diff and d[i] >= d[i - 1] and d[i] >= d[i + 1]]
sr = 48000
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.mp4, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
w = sr // 1000
env = np.sqrt(np.convolve(pcm ** 2, np.ones(w) / w, mode="same"))
errs = []
for c in cuts:
    tc = c / 30
    i0, i1 = int((tc - 0.06) * sr), int((tc + 0.08) * sr)
    seg = env[i0:i1]; pk = int(np.argmax(seg)); floor = np.percentile(env[i0 - int(0.05 * sr):i0], 20)
    half = floor + (seg[pk] - floor) / 2
    k = pk
    while k > 0 and seg[k] > half: k -= 1
    to = (i0 + k) / sr
    errs.append((tc - to) * 1000)
    print(f"cut frame {c:5d} t={tc:7.3f}  onset {to:7.3f}  cut-onset {errs[-1]:+6.1f} ms  (frame diff {d[c - 1]:.0f})")
print(f"|err| max {max(map(abs, errs)):.1f} ms, mean {np.mean(errs):+.1f} ms; half frame = 16.7 ms")
