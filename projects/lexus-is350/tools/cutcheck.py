"""Cut timing vs the delivered file's own audio. Cuts = frame-diff peaks (luma, 1/4 res); kicks = broadband onsets:
half-rise of a 1 ms RMS envelope (rule from lessons 2026-11-11). Reports each expected cut frame, the detected cut,
the nearest kick and the error in frames.   cutcheck.py video.mp4 f1 f2 ...   (expected cut frames)"""
import subprocess, sys, numpy as np
v = sys.argv[1]; exp = [int(x) for x in sys.argv[2:]]
W, H = 135, 240
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
sr = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
n = sr // 1000
env = np.sqrt(np.convolve(a ** 2, np.ones(n) / n, "same"))
def kick_near(t, win=0.07):
    """strongest 1 ms-RMS peak within +-win of t, then the half-rise of its attack within 60 ms before the peak
    (a wider pre-window catches the sustained synth before each kick on generated tracks and reads 100+ ms early)"""
    i0, i1 = int((t - win) * sr), int((t + win) * sr)
    pk = i0 + int(np.argmax(env[i0:i1]))
    a0 = pk - int(0.06 * sr); seg = env[a0:pk + 1]; lo = seg.min(); half = lo + (env[pk] - lo) / 2
    return (a0 + int(np.where(seg >= half)[0][0])) / sr
print(" exp  det   t_cut   kick    err(frames)")
errs = []
for e in exp:
    lo, hi = e - 3, e + 4
    det = lo + int(np.argmax(d[lo:hi]))
    tc = det / 30; k = kick_near(tc)
    err = (tc - k) * 30 if k is not None else float("nan"); errs.append(err)
    print(f"{e:4d} {det:4d}  {tc:6.3f}  {k:6.3f}  {err:+5.2f}  {'OK' if abs(err) <= 0.5 and det == e else '<<'}")
print("max |err|", np.nanmax(np.abs(errs)).round(2), "frames")
