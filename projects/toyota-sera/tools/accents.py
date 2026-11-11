"""Music analysis for the Sera reel: kick grid (40-120 Hz peaks, least squares - FG2 lesson), per-beat RMS / low-band
energy / onset strength to find phrase accents, and where the music actually ends (generated tracks end early).
    accents.py track.mp3"""
import sys
import librosa
import numpy as np

y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f > 40) & (f < 120)].sum(0)
t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=hop)
lowd = np.maximum(0, np.diff(low, prepend=low[0]))
pk = librosa.util.peak_pick(lowd, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=np.percentile(lowd, 90) * 0.3, wait=15)
kt = t[pk]; strength = lowd[pk]
kt = kt[strength > np.percentile(strength, 40)]
# fit grid t = t0 + n*T with T near the tempo estimate
tempo = librosa.beat.beat_track(y=y, sr=sr)[0]
T0 = 60 / float(np.atleast_1d(tempo)[0])
best = None
for T in np.linspace(T0 * 0.98, T0 * 1.02, 81):
    for ph in np.linspace(0, T, 60, endpoint=False):
        n = np.round((kt - ph) / T); r = kt - (ph + n * T)
        sc = np.mean(np.abs(r) < 0.03)
        if best is None or sc > best[0]: best = (sc, T, ph)
_, T, ph = best
n = np.round((kt - ph) / T); r = kt - (ph + n * T); m = np.abs(r) < 0.04
A = np.c_[np.ones(m.sum()), n[m]]; (t0, T), *_ = np.linalg.lstsq(A, kt[m], rcond=None)
print(f"kick grid: t = {t0:.4f} + {T:.5f} n  ({60/T:.2f} BPM), {m.sum()} kicks on grid, rms {np.std(kt[m]-(t0+n[m]*T))*1000:.1f} ms")
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
on = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
dur = len(y) / sr
k0 = int(np.ceil(-t0 / T))
print(" beat    t     rms   low   onset  kick")
for k in range(k0, int((dur - t0) / T) + 1):
    b = t0 + k * T
    i = (t >= b - 0.05) & (t < b + 0.10)
    w = (t >= b) & (t < b + T)
    if not i.any(): continue
    kick = np.any(np.abs(kt - b) < 0.04)
    print(f"{k:4d} {b:6.3f}  {rms[w].mean()*100:5.1f} {low[w].mean()/low.max()*100:5.1f} {on[i].max():6.2f}  {'K' if kick else ''}")
# end of music
env = librosa.amplitude_to_db(rms, ref=np.max)
loud = t[env > -30]
print(f"duration {dur:.3f}; last frame above -30 dB: {loud.max():.2f}; above -45 dB: {t[env > -45].max():.2f}")
