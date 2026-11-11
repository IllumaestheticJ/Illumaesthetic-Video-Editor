"""Check a delivered reel's cuts against its own DECODED audio.
  cutcheck.py video.mp4 cuts.json
Cuts: frame-diff peaks near each planned cut (cuts.json "cuts"[1:]). Kicks: broadband onset = half-rise of a 1 ms RMS
envelope (a low-passed envelope reads 40-70 ms late - WRX VA lesson), searched within +-120 ms of the planned beat.
Also flags duplicate frames (diff ~0) and black frames in the scan part."""
import json, subprocess, sys
import numpy as np

V, C = sys.argv[1], json.load(open(sys.argv[2]))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
sr = 48000
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                     capture_output=True).stdout
y = np.frombuffer(pcm, np.float32)
w = sr // 1000
env = np.sqrt(np.convolve(y ** 2, np.ones(w) / w, mode="same"))
print(f"video {len(fr)} frames ({len(fr)/30:.3f} s), audio {len(y)/sr:.3f} s")
errs = []
for c in C["cuts"][1:]:
    F = round(c * 30)
    k = max(range(F - 3, F + 4), key=lambda i: d[i - 1])
    a, b = int((c - 0.12) * sr), int((c + 0.12) * sr)
    seg = env[a:b]
    pk = int(np.argmax(seg)); base = np.percentile(seg[:max(1, pk)], 10) if pk > 0 else seg.min()
    half = base + (seg[pk] - base) / 2
    i = pk
    while i > 0 and seg[i] > half:
        i -= 1
    onset = (a + i) / sr
    e = k / 30 - onset; errs.append(e)
    print(f"planned {c:7.3f}  cut frame {k:4d} = {k/30:7.3f} s  kick onset {onset:7.3f}  err {e*1000:+6.1f} ms  "
          f"{'OK' if abs(e) <= 1/60 + 1e-6 else 'OFF'}")
print(f"max |err| {max(abs(e) for e in errs)*1000:.1f} ms (target <= 16.7 ms = 1/2 frame)")
dups = [i for i in range(1, len(d)) if d[i - 1] < 0.05 and fr[i].mean() > 8]
print("near-duplicate frames:", dups)
print("black frames:", [i for i in range(len(fr)) if fr[i].mean() < 3][:40])
