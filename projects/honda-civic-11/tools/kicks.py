"""Kick grid + energy map for a track (numpy only). Lesson: anchor cuts on 40-120 Hz kick peaks, not spectral onsets.

    python kicks.py track.mp3 [--bpm 143.6]
Prints per-second RMS (dB), per-beat low-band strength on the fitted grid, the grid (t0, period) and where audio ends.
"""
import argparse, subprocess
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("track"); ap.add_argument("--bpm", type=float, default=143.6)
a = ap.parse_args()
sr = 22050
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.track, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
y = np.frombuffer(raw, np.float32)
hop, n = 128, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); t = np.arange(len(S)) * hop / sr
low = S[:, (f > 40) & (f < 120)].sum(1)
rms = np.sqrt((fr ** 2).mean(1)); db = 20 * np.log10(rms + 1e-9); db -= db.max()
print("RMS dB/s:", " ".join(f"{s}:{db[(t >= s) & (t < s + 1)].mean():.0f}" for s in range(int(t[-1]) + 1)))
fl = np.diff(low, prepend=low[0]); fl[fl < 0] = 0
# local peaks of the low-band flux
w = 12
pk = [i for i in range(w, len(fl) - w) if fl[i] == fl[i - w:i + w].max() and fl[i] > np.percentile(fl, 92)]
kt = t[pk]; ks = fl[pk]
P = 60 / a.bpm
st = kt[ks > np.percentile(ks, 50)]
st = st[st > 7]
nn = np.round((st - st[0]) / P); A = np.vstack([np.ones_like(nn), nn]).T
c = np.linalg.lstsq(A, st, rcond=None)[0]
for _ in range(3):
    e = st - A @ c; g = np.abs(e) < 0.04
    c = np.linalg.lstsq(A[g], st[g], rcond=None)[0]
e = st[g] - A[g] @ c
t0, per = c
t0 = t0 - per * np.floor(t0 / per)
print("grid t0 %.4f period %.5f (%.2f BPM), kick rms err %.1f ms, n=%d" % (t0, per, 60 / per, 1000 * np.sqrt((e ** 2).mean()), g.sum()))
# strength per grid beat: low-band flux max within +-40 ms, and broadband flux
bb = np.diff(rms, prepend=rms[0]); bb[bb < 0] = 0
print("beat  time   kick  broad  dB")
k = 0
while t0 + k * per < t[-1]:
    bt = t0 + k * per; m = np.abs(t - bt) < 0.04
    print("%3d %7.3f %6.1f %6.3f %4.0f" % (k, bt, fl[m].max() / np.median(fl[fl > 0]) if m.any() else 0, bb[m].max() * 100 if m.any() else 0, db[m].max() if m.any() else -99))
    k += 1
for lv in (-30, -40, -50):
    print("last frame above %d dB: %.2f s" % (lv, t[np.nonzero(db > lv)[0][-1]]))
