"""Measure cuts (frame diffs) against the decoded audio of the delivered file: nearest broadband onset =
half-rise of a 1 ms RMS envelope.   python projects/porsche-gt3rs-992/tools/cutcheck.py out.mp4 [--thr 6]"""
import subprocess, sys
import numpy as np
O = sys.argv[1]; thr = float(sys.argv[3]) if len(sys.argv) > 3 else 6.0
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", O, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
d = np.abs(np.diff(f, axis=0)).mean((1, 2))
cuts = [i + 1 for i in range(len(d)) if d[i] > thr and d[i] > 3 * np.median(d[max(0, i - 5):i + 6])]
sr = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", O, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
w = sr // 1000; env = np.sqrt(np.convolve(a ** 2, np.ones(w) / w, mode="same"))
for c in cuts:
    t = c / 30; i0, i1 = int((t - 0.25) * sr), int((t + 0.25) * sr)
    seg = env[i0:i1]; pk = np.argmax(seg); base = np.percentile(seg[:max(1, pk)], 10) if pk else 0
    half = base + 0.5 * (seg[pk] - base); j = np.argmax(seg[:pk + 1] >= half)
    on = (i0 + j) / sr
    print(f"cut frame {c:4d} t={t:7.3f}  onset {on:7.3f}  err {1000*(t-on):+6.0f} ms ({(t-on)*30:+.2f} fr)")
