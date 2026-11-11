"""Measure the Cappuccino track: true end, kick-peak-anchored beat grid (FG2 lesson), per-beat accent strength.
  music.py track.mp3"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop)); f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f > 40) & (f < 120)].sum(0); t = librosa.frames_to_time(np.arange(len(low)), sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]; db = 20 * np.log10(rms + 1e-9); top = db.max()
print("file dur", round(len(y) / sr, 3), " last frame > -25 dB:", t[np.where(db > top - 25)[0][-1]].round(3),
      " > -40 dB:", t[np.where(db > top - 40)[0][-1]].round(3))
on = np.diff(low, prepend=low[0]); on[on < 0] = 0
pk = librosa.util.peak_pick(on, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=on.max() * 0.08, wait=40)
kt = t[pk]; print("kick peaks", len(kt), np.round(kt, 3).tolist())
best = None
for per in np.linspace(0.468, 0.484, 161):
    ph = np.angle(np.mean(np.exp(2j * np.pi * kt / per))); t0 = (ph / (2 * np.pi)) * per % per
    e = ((kt - t0 + per / 2) % per) - per / 2; s = np.median(np.abs(e))
    if best is None or s < best[0]: best = (s, per, t0)
s, per, t0 = best; print(f"grid: period {per:.4f} s ({60/per:.2f} BPM) t0 {t0:.3f} median |kick err| {s*1000:.1f} ms")
g = t0 + np.arange(int(len(y) / sr / per) + 1) * per
for i, gi in enumerate(g):
    m = (t > gi - 0.04) & (t < gi + 0.08)
    if m.any():
        print(f"{i:3d} {gi:7.3f}  kick {low[m].max():7.1f}  rms {db[m].max() - top:6.1f} dB", "#" * int(low[m].max() / low.max() * 40))
