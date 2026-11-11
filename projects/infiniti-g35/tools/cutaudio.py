"""Measure every hard cut of a delivered reel against the kick in its own decoded audio.

Cuts come from frame differences (30 fps, 108x192 grey). For each cut, the kick is the strongest broadband hit within
+-150 ms; its time is the half-rise of a 1 ms RMS envelope (first sample reaching half the hit's peak, after the local
floor). A low-passed envelope reads 40-70 ms late (WRX VA lesson), so the envelope is NOT filtered.
    python projects/infiniti-g35/tools/cutaudio.py video.mp4 [--expect 161,321,...]"""
import argparse, subprocess
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--thr", type=float, default=12.0)
ap.add_argument("--expect", default="")
a = ap.parse_args()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
d = np.abs(np.diff(f, axis=0)).mean((1, 2))
cuts = [i + 1 for i in range(len(d)) if d[i] > a.thr and d[i] > 3 * np.median(d[max(0, i - 5):i + 6])]
SR = 48000
au = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                    capture_output=True, check=True).stdout
x = np.frombuffer(au, np.float32)
hop = SR // 1000  # 1 ms RMS
env = np.sqrt(np.convolve(x.astype(float) ** 2, np.ones(hop) / hop, "same"))[::hop]  # one value per ms
print(f"video {len(f)} frames = {len(f)/30:.3f} s; audio {len(x)/SR:.3f} s; cuts {len(cuts)}")
exp = [int(v) for v in a.expect.split(",") if v]
if exp:
    print("expected cut frames", exp, "found", cuts, "MATCH" if cuts == exp else "MISMATCH")
errs = []
for c in cuts:
    tc = c / 30; ms = int(round(tc * 1000))
    lo, hi = max(0, ms - 150), min(len(env) - 1, ms + 150)
    w = env[lo:hi]
    pk = lo + int(np.argmax(w))  # strongest hit near the cut
    floor = np.percentile(env[max(0, pk - 120):pk - 20], 20) if pk > 140 else 0.0
    half = floor + 0.5 * (env[pk] - floor)
    k = pk
    while k > lo and env[k - 1] >= half:
        k -= 1
    tk = k / 1000; e = tc - tk; errs.append(e)
    dup = d[c] < 0.3 if c < len(d) else False
    print(f"cut frame {c:4d} t={tc:7.3f}  kick {tk:7.3f}  err {1000*e:+6.1f} ms ({e*30:+.2f} fr)  next-dup {dup}"
          f"  luma {f[c].mean():.0f}")
if errs:
    print(f"max |err| {1000*max(map(abs, errs)):.1f} ms  (target <= 16.7 ms = 1/2 frame)")
