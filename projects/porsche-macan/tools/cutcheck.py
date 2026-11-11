"""Measure every cut in a delivered reel against the decoded audio (user rule 2026-11-11, from subaru-wrx-va).

    python projects/porsche-macan/tools/cutcheck.py out.mp4 [--expect 4.109,8.176,...]

Cuts: frame-difference peaks of the decoded video (mean abs diff of 1/8-scale greyscale frames; a cut is a frame
whose diff is > 6x the local median). Audio: broadband 1 ms RMS envelope; onset = local half-rise before the strongest
(5 ms smoothed) peak within +-60 ms of the cut (a low-passed envelope reads 40-70 ms late).
Prints cut time, nearest onset, error (ms) and frames; target |err| <= half a frame (16.7 ms at 30 fps).
"""
import subprocess, sys
import numpy as np

path = sys.argv[1]
expect = [float(v) for v in sys.argv[sys.argv.index("--expect") + 1].split(",")] if "--expect" in sys.argv else None
W, H = 135, 240
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
fps = 30.0
d = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
cuts = []
for i in range(1, len(d)):
    loc = d[max(1, i - 15):i + 15]
    if d[i] > 6 * (np.median(loc) + 0.05) and d[i] > 1.0 and d[i] == loc.max():
        cuts.append(i / fps)
sr = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
win = sr // 1000
env = np.sqrt(np.convolve(a.astype(np.float64) ** 2, np.ones(win) / win, mode="same"))
e5 = np.convolve(env, np.ones(5 * win) / (5 * win), mode="same")  # 5 ms smoothing to locate the peak
print(f"{len(fr)} frames ({len(fr)/fps:.3f} s), audio {len(a)/sr:.3f} s; detected cuts: {len(cuts)}")
print("   cut s   onset s   err ms  err frames")
errs = []
for c in cuts:
    s0, s1 = int((c - 0.06) * sr), int((c + 0.06) * sr)
    seg = e5[max(0, s0):s1]
    if len(seg) == 0:
        continue
    # strongest transient within +-60 ms, onset = local half-rise walking back from its peak (a first-crossing rule
    # over +-120 ms latched onto earlier, weaker transients in the intro and read 110 ms early)
    ip = int(seg.argmax()); base = np.percentile(e5[max(0, s0 - sr // 4):max(1, s0)], 20) if s0 > 0 else 0
    half = base + 0.5 * (seg[ip] - base); i = ip
    while i > 0 and seg[i] > half:
        i -= 1
    on = i + max(0, s0)
    t = on / sr; e = (c - t) * 1000; errs.append(e)
    print(f"  {c:7.3f}  {t:7.3f}  {e:+7.1f}  {e/1000*fps:+5.2f}")
if expect:
    print("expected cuts:", expect)
    print("missing:", [x for x in expect if not any(abs(x - c) < 0.05 for c in cuts)])
if errs:
    print(f"max |err| {max(abs(e) for e in errs):.1f} ms (half frame = {500/fps:.1f} ms)")
