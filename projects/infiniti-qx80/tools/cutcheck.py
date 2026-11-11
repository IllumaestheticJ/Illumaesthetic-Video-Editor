"""Cut timing vs the delivered audio: frame-diff cuts, and for each the nearest broadband onset in the decoded
audio (1 ms RMS envelope, half-rise between the 30 ms floor before and the 60 ms peak after a flux peak).
  python cutcheck.py out.mp4"""
import subprocess, sys, numpy as np
O = sys.argv[1]; SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", O, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
cuts = (np.where(np.abs(np.diff(f, axis=0)).mean((1, 2)) > 12)[0] + 1) / 30.0
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "quiet", "-i", O, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
w = SR // 1000; env = np.sqrt((a[: len(a) // w * w].reshape(-1, w) ** 2).mean(1))  # 1 ms RMS
lenv = np.log(env + 1e-6); flux = np.maximum(0, lenv[5:] - lenv[:-5]); flux = np.concatenate([np.zeros(5), flux])
for c in cuts:
    i0 = int(c * 1000); lo, hi = max(0, i0 - 120), i0 + 120
    k = lo + int(np.argmax(np.convolve(flux[lo:hi], np.ones(10), "same")))
    base = env[max(0, k - 40):k - 10].mean(); peak = env[k:k + 60].max(); half = base + (peak - base) / 2
    j = k - 10 + int(np.argmax(env[k - 10:k + 60] >= half))
    print(f"cut {c:7.3f}s  onset {j/1000:7.3f}s  err {1000*(c - j/1000):+5.0f} ms  (rise x{peak/max(base,1e-6):.1f})")
