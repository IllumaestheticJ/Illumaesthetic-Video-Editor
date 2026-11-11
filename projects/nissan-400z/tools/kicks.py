"""Kick times (40-120 Hz onset peaks, refined to the band-energy peak) + per-kick strength, and a robust grid fit
by phase search (period fixed from autocorrelation of the kick envelope).  kicks.py track.mp3"""
import subprocess, sys, numpy as np
sr = 22050
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
hop, n = 128, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); t = np.arange(len(S)) * hop / sr
kb = S[:, (f > 40) & (f < 120)].sum(1)
kf = np.maximum(0, np.diff(kb, prepend=kb[0]))
w = int(0.08 * sr / hop)
pk = [i for i in range(w, len(kf) - w) if kf[i] == kf[i - w:i + w + 1].max() and kf[i] > 0.08 * kf.max()]
kt = t[pk]; ks = kf[pk] / kf.max()
# period: autocorrelation of onset envelope in 0.35-0.6 s
ac = np.correlate(kf - kf.mean(), kf - kf.mean(), "full")[len(kf) - 1:]
lags = np.arange(len(ac)) * hop / sr; m = (lags > 0.35) & (lags < 0.6)
P = lags[m][np.argmax(ac[m])]
# refine period+phase on strong kicks by least squares
strong = kt[ks > 0.3]
best = None
for Pp in np.arange(P - 0.006, P + 0.006, 0.0002):
    ph = np.angle(np.exp(2j * np.pi * strong / Pp).sum()) / (2 * np.pi) * Pp
    r = (strong - ph + Pp / 2) % Pp - Pp / 2
    sc = np.abs(r).mean()
    if best is None or sc < best[0]: best = (sc, Pp, ph % Pp)
sc, P, ph = best
print(f"period {P:.4f} s = {60 / P:.2f} BPM, phase {ph:.3f} s, mean |resid| strong kicks {sc * 1000:.1f} ms")
print("kicks (t strength):", " ".join(f"{a:.3f}:{b:.2f}" for a, b in zip(kt, ks)))
