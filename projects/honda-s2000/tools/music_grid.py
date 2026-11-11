"""Measure the S2000 track: kick onsets (40-120 Hz energy peaks), tempo by least-squares fit of kicks to a grid,
per-beat accent strength (RMS + low-band), and where the music ends. numpy/scipy only.
    python projects/honda-s2000/tools/music_grid.py track.wav [--bpm-range 60,180]"""
import sys, json
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt, find_peaks
sr, x = wavfile.read(sys.argv[1]); x = x.astype(float); x /= np.abs(x).max()
hop = 256; fr = sr / hop
def env(sig):
    n = len(sig) // hop; e = np.sqrt((sig[:n * hop].reshape(n, hop) ** 2).mean(1)); return e
low = env(sosfiltfilt(butter(4, [40, 120], "band", fs=sr, output="sos"), x))
full = env(x)
db = 20 * np.log10(full + 1e-9)
t = np.arange(len(full)) / fr
# end of music: last time the 0.5 s RMS is within 30 dB of the track's peak
k = int(fr * 0.5); sm = np.convolve(full, np.ones(k) / k, "same"); sdb = 20 * np.log10(sm + 1e-9)
alive = np.where(sdb > sdb.max() - 30)[0]; end30 = t[alive[-1]]
alive20 = np.where(sdb > sdb.max() - 20)[0]; end20 = t[alive20[-1]]
# kick peaks: onset of low-band energy
d = np.maximum(0, np.diff(low, prepend=low[0]))
pk, pr = find_peaks(d, height=d.max() * 0.25, distance=int(fr * 0.15))
kt = t[pk]
# tempo: search beat period that best fits kicks (phase via circular mean)
best = None
for bpm in np.arange(60, 181, 0.05):
    P = 60 / bpm; ph = np.angle(np.mean(np.exp(2j * np.pi * kt / P)))
    off = ((kt - ph / (2 * np.pi) * P) / P); err = np.abs(off - np.round(off)) * P
    sc = np.mean(err < 0.03)
    if best is None or sc > best[0] + 1e-9: best = (sc, bpm, P, ph)
sc, bpm, P, ph = best
t0 = (ph / (2 * np.pi) * P) % P
print(f"duration {t[-1]:.2f}s  end(-20dB) {end20:.2f}  end(-30dB) {end30:.2f}")
print(f"kicks {len(kt)}  best grid {bpm:.2f} BPM (P={P:.4f}s) phase t0={t0:.3f}  fit {sc*100:.0f}% within 30 ms")
print("first kicks", np.round(kt[:24], 3).tolist())
# per-beat accent table on the fitted grid
beats = np.arange(t0, end30 + P, P)
rows = []
for i, b in enumerate(beats):
    a, z = int(b * fr), int(min(len(full), (b + P) * fr))
    if z <= a: continue
    hit = d[max(0, a - 3):a + 4].max() / d.max()
    rows.append((i, round(b, 3), round(float(20 * np.log10(full[a:z].mean() + 1e-9)), 1), round(float(low[a:z].mean() / low.max()), 3), round(float(hit), 2)))
for r in rows: print(*r)
json.dump({"bpm": bpm, "beat": P, "t0": t0, "end20": end20, "end30": end30, "kicks": kt.tolist(), "beats": [r[1] for r in rows]},
          open(sys.argv[1] + ".grid.json", "w"), indent=0)
