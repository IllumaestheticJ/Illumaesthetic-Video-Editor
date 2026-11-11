"""Kick-anchored beat grid + per-beat accent strength + end-of-music for the MR2 track (lessons: anchor on kick peaks,
cut on accents, measure where generated tracks really end).  music_grid.py track.mp3"""
import sys, numpy as np, librosa
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=256))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)
low = S[(f >= 40) & (f <= 120)].sum(0); t = librosa.frames_to_time(np.arange(len(low)), sr=sr, hop_length=256)
lown = low / low.max()
pk = librosa.util.peak_pick(lown, pre_max=8, post_max=8, pre_avg=20, post_avg=20, delta=0.08, wait=20)
kt = t[pk]
P0 = 0.534
# least squares grid on kicks that sit near a beat of the rough grid
n = np.round((kt - kt[0]) / P0); A = np.vstack([np.ones_like(n), n]).T
for _ in range(3):
    c, per = np.linalg.lstsq(A, kt, rcond=None)[0]
    res = kt - (c + per * n); keep = np.abs(res) < 0.06; A, kt, n = A[keep], kt[keep], n[keep]
print(f"grid: t = {c:.4f} + {per:.5f} n  ({60/per:.2f} BPM), rms {np.sqrt(np.mean((kt-(c+per*n))**2))*1000:.1f} ms on {len(kt)} kicks")
rms = librosa.feature.rms(y=y, hop_length=256)[0]; rt = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=256)
db = 20 * np.log10(rms / rms.max() + 1e-9)
flux = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
first = int(np.ceil((0 - c) / per)); beats = c + per * np.arange(first, int((len(y) / sr - c) / per) + 1)
print(" n     t     kick   flux   rmsdB")
for i, b in enumerate(beats):
    j = np.argmin(np.abs(t - b)); w = slice(max(0, j - 4), j + 5)
    print(f"{i:3d} {b:6.3f}  {lown[w].max():.2f}  {flux[w].max():5.1f}  {db[j]:6.1f}")
# end: last time the level is within 30 dB of peak (smoothed)
sm = np.convolve(db, np.ones(20) / 20, "same")
print("last above -30 dB:", rt[np.where(sm > -30)[0][-1]].round(2), " last above -45 dB:", rt[np.where(sm > -45)[0][-1]].round(2))
