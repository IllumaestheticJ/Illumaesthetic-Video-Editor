"""Fit the Ep 8 music bed (job 2fd1e9e8, 50 s, ~99 BPM, bar 2.415 s) to the cut after the cartoon grew 1.6 s (new L08).

Repeats one bar starting on a strong onset in the middle of the track (the bed is ducked under dialogue there), with a
20 ms crossfade at the joint. With the build's --music-in 0.6 the track's lift (~42 s) lands on the IRL cut (43.9 s) and
its natural ending finishes before the video does. No time-stretch.
Usage: python ep8_music_fit.py IN OUT
"""
import subprocess, sys
import numpy as np

SR, BAR, A = 48000, 2.415, 26.076          # bar length from `ive beats` (period 0.302 s x 8); A = strong onset


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


x = load(sys.argv[1])
a, b, xf = int(A * SR), int((A + BAR) * SR), int(0.02 * SR)
head, tail = x[:b + xf].copy(), x[a:].copy()        # head runs xf past the bar so the crossfade keeps the bar length
r = np.linspace(0, 1, xf)[:, None]
joint = head[-xf:] * (1 - r) + tail[:xf] * r
y = np.vstack([head[:-xf], joint, tail[xf:]])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", sys.argv[2]],
               input=y.astype(np.float32).tobytes(), check=True)
print(f"{len(x) / SR:.2f} s -> {len(y) / SR:.2f} s")
