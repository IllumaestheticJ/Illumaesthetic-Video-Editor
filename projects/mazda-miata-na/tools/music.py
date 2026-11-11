"""Measure the reel's track: kick grid (40-120 Hz peaks, least-squares line - lessons: anchor on kicks, not flux),
per-beat RMS / low-end / flux so accents and section changes show, and where the music actually ends.
    python music.py track.mp3"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f >= 40) & (f <= 120)].sum(0); lowd = np.maximum(0, np.diff(low, prepend=low[0]))
t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=hop)
pk = librosa.util.peak_pick(lowd, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=np.percentile(lowd, 90) * 0.5, wait=10)
kt = t[pk]
_, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop, units="time")
period = np.median(np.diff(beats))
# phase of the kicks against the beat period (circular histogram), then least squares on the on-phase kicks
ph = np.angle(np.exp(2j * np.pi * kt / period)); hist, e = np.histogram(ph, bins=36, range=(-np.pi, np.pi))
phi = (e[np.argmax(hist)] + e[np.argmax(hist) + 1]) / 2
t0 = (phi / (2 * np.pi)) * period
n = np.round((kt - t0) / period); r = kt - (t0 + n * period); k = np.abs(r) < 0.05
A = np.c_[np.ones(len(kt)), n]
c = np.linalg.lstsq(A[k], kt[k], rcond=None)[0]
t0, P = c; t0 = t0 - np.floor(t0 / P) * P
print(f"kick grid: t = {t0:.4f} + {P:.5f} n  ({60 / P:.2f} BPM), kicks {len(kt)}, on-grid rms {np.sqrt(np.mean((kt[k] - A[k] @ c) ** 2)) * 1000:.1f} ms")
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
dur = len(y) / sr
print(" n     t     rms   low  flux  kick")
for i in range(int(dur / P) + 1):
    a = t0 + i * P; m = (t >= a - 0.04) & (t < a + P - 0.04)
    if not m.any(): break
    kick = np.any(np.abs(kt - a) < 0.05)
    print(f"{i:3d} {a:6.3f} {rms[m].mean()*100:5.1f} {low[m].mean()/low.max()*100:5.1f} {flux[(t >= a - 0.03) & (t < a + 0.06)].max():5.2f} {'K' if kick else ''}")
db = librosa.amplitude_to_db(rms, ref=rms.max())
loud = t[db > -30]; print(f"last frame above -30 dB: {loud[-1]:.2f} s; above -45 dB: {t[db > -45][-1]:.2f} s; file {dur:.2f} s")
