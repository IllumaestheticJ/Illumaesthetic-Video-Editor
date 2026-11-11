"""Measure every hard cut of a rendered reel against the decoded audio's kick onset.

    python projects/toyota-gr86/tools/cutcheck.py out.mp4 [--expect 7.395 13.246 ...]

Cuts: frames whose mean abs difference to the previous frame (64x114 grey) is a spike (> 6x the median and > 12).
Onset: broadband (no low-pass, which reads 40-70 ms late) 1 ms RMS envelope; within -120..+80 ms of the cut, find the
largest envelope rise and report where it first crosses half of that peak (half-rise). Offset = cut - onset.
"""
import argparse
import subprocess

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("--expect", type=float, nargs="*", default=[])
a = ap.parse_args()

W, H, SR = 64, 114, 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)
fps = 30.0
d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
med = np.median(d) + 1e-6
cuts = [i + 1 for i in range(len(d)) if d[i] > max(12, 6 * med) and d[i] >= d[max(0, i - 1)] and d[i] >= d[min(len(d) - 1, i + 1)]]

pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.float32).astype(float)
hop = SR // 1000
env = np.sqrt(np.convolve(x * x, np.ones(hop) / hop, "same"))[::hop]   # 1 ms RMS, 1 ms steps
print(f"frames {len(fr)} ({len(fr) / fps:.3f} s), audio {len(x) / SR:.3f} s, last >-30 dB "
      f"{np.nonzero(20 * np.log10(env + 1e-9) > -30)[0].max() / 1000:.3f} s")
print(" cut  frame   t_cut   onset   offset_ms  expect_ms")
for c in cuts:
    t = c / fps
    i0, i1 = int((t - 0.12) * 1000), int((t + 0.08) * 1000)
    seg = env[i0:i1]
    base = seg[:20].min()
    pk = seg.argmax()
    half = base + 0.5 * (seg[pk] - base)
    j = pk
    while j > 0 and seg[j - 1] >= half:
        j -= 1
    on = (i0 + j) / 1000
    ex = min(a.expect, key=lambda e: abs(e - t)) if a.expect else None
    print(f"{cuts.index(c) + 1:4d} {c:6d} {t:7.3f} {on:7.3f} {1000 * (t - on):9.0f}"
          + (f" {1000 * (t - ex):9.0f}" if ex is not None else ""))
