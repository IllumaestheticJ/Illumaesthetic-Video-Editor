"""(copied from porsche-gt3-992) Measure a track (numpy only, no librosa here): loudness per second, kick-band (40-120 Hz) onsets,
least-squares beat grid anchored on kicks (lesson: anchor on the kick peak, not spectral flux), per-beat accent strength.
    python music_grid.py track.mp3"""
import subprocess, sys, numpy as np
sr = 22050
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
y = np.frombuffer(raw, np.float32)
hop, n = 256, 2048
fr = np.lib.stride_tricks.sliding_window_view(np.pad(y, (n // 2, n // 2)), n)[::hop] * np.hanning(n)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); t = np.arange(len(S)) * hop / sr
rms = np.sqrt((fr ** 2).mean(1)); db = 20 * np.log10(rms + 1e-9)
print("dB per s:", " ".join(f"{s}:{db[(t >= s) & (t < s + 1)].mean():.0f}" for s in range(int(t[-1]) + 1)))
kb = S[:, (f > 40) & (f < 120)].sum(1); kf = np.maximum(0, np.diff(kb, prepend=kb[0]))
# peaks: local max in +-60 ms and above 10 % of max
w = int(0.06 * sr / hop)
pk = [i for i in range(w, len(kf) - w) if kf[i] == kf[i - w:i + w + 1].max() and kf[i] > 0.1 * kf.max()]
# refine each kick to the kick-band energy peak just after the onset
kt = np.array([t[i] for i in pk]); ks = kf[pk]
P0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.557  # RX-7 track (ive beats)
nidx = np.round((kt - kt[0]) / P0); A = np.vstack([nidx, np.ones_like(nidx)]).T
(P, t0), *_ = np.linalg.lstsq(A, kt, rcond=None)
res = kt - (nidx * P + t0)
print(f"grid: period {P:.4f} s ({60 / P:.2f} BPM), t0 {t0:.3f}, |resid| mean {np.abs(res).mean() * 1000:.1f} ms, kicks {len(kt)}")
# per-beat accent: broadband onset strength + kick strength at each grid beat
flux = np.maximum(0, np.diff(S, axis=0, prepend=S[:1])).sum(1)
nb = int((t[-1] - t0) / P) + 1
print("beat  time   kick  flux  dB")
for b in range(nb):
    tb = t0 + b * P; m = (t > tb - 0.04) & (t < tb + 0.06)
    if not m.any(): continue
    k = kf[m].max() / kf.max(); fx = flux[m].max() / flux.max(); d = db[m].max()
    print(f"{b:3d} {tb:7.3f} {k:5.2f} {fx:5.2f} {d:5.1f}" + ("  <==" if k > 0.5 else ""))
