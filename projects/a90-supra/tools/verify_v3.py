"""Checks on the DELIVERED v3 mp4 (no librosa needed): where each cut really is (largest frame jump near each bar line),
how far the 35-120 Hz kick attack is from it, frozen / black frames, bright pixels touching the frame edge.
    python projects/a90-supra/tools/verify_v3.py out.mp4"""
import json, os, subprocess, sys
import numpy as np, scipy.signal as ss
D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
O = sys.argv[1]; tl = json.load(open(D + "/timeline_v3.json")); bars = tl["bars"]
v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", O, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout, np.uint8).reshape(-1, 192, 108).astype(float)
d = np.r_[0, np.abs(np.diff(v, axis=0)).mean((1, 2))]
sr = 48000; a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", O, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
e = np.sqrt(np.convolve(ss.sosfiltfilt(ss.butter(4, [35, 120], btype="band", fs=sr, output="sos"), a) ** 2, np.ones(480) / 480, "same"))[::48]
print("frames", len(v), "duration %.2f" % (len(a) / sr))
names = [s["shot"] for s in tl["shots"] if s["shot"] != "s12a_shell"]
worst = 0
for k in range(1, 20):
    c = bars[k]; j = c - 4 + int(np.argmax(d[c - 4:c + 5]))
    T = j / 30; i0 = int((T - 0.12) * 1000); w = e[i0:int((T + 0.12) * 1000)]; pk = w.argmax(); q = pk
    while q > 0 and w[q] > w[pk] * 0.5: q -= 1
    off = (i0 + q) / 1000 - T; worst = max(worst, abs(off))
    print(f"bar {k + 1:2d} {names[k]:16s} planned {c:4d} cut at {j:4d} ({j - c:+d} f)  jump {d[j]:5.1f} (before {d[j - 1]:.2f}, after {d[j + 1]:.2f})  kick attack {off * 1000:+4.0f} ms")
print("worst kick offset %.0f ms" % (worst * 1000))
last = bars[19] + 60
print("frozen frames (diff < 0.003) before the fade:", [i for i in range(1, last - 25) if d[i] < 0.003][:30])
print("black frames before the fade:", [i for i in range(0, last - 25) if v[i].mean() < 1.0][:20])
big = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", O, "-vf", "scale=270:480,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout, np.uint8).reshape(-1, 480, 270)
for k, n in enumerate(names):
    seg = big[bars[k] + 1:(bars[k + 1] if k < 19 else last) - 1]; br = seg > 60
    print(f"edge touch {n:16s} left {br[:, :, :2].any((1, 2)).mean():.2f} right {br[:, :, -2:].any((1, 2)).mean():.2f} top {br[:, :2].any((1, 2)).mean():.2f} bottom {br[:, -2:].any((1, 2)).mean():.2f}  (share of frames with scan pixels on that edge)")
