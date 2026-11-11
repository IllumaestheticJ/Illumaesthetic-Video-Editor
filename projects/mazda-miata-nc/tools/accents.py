"""Per-beat accent map of a track (numpy only): kick-band (40-120 Hz) energy peaks -> least-squares beat grid,
then per-beat RMS / kick / high-band flux, so cuts can go on the strong accents (lessons: anchor on the kick, not
the first spectral onset). Prints the grid fit, a per-beat table and where the music ends.
    accents.py track.mp3 [--bpm 103.4]"""
import subprocess, sys
import numpy as np
SR = 22050
path = sys.argv[1]
bpm = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else None
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
hop, win = 256, 2048
n = 1 + (len(x) - win) // hop
fr = np.lib.stride_tricks.as_strided(x, (n, win), (x.strides[0] * hop, x.strides[0])) * np.hanning(win)
S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(win, 1 / SR); t = (np.arange(n) * hop + win / 2) / SR
kick = S[:, (f >= 40) & (f <= 120)].sum(1); hi = S[:, f > 2000]
flux = np.maximum(0, np.diff(np.log1p(hi), axis=0)).sum(1); flux = np.r_[0, flux]
rms = np.sqrt((fr ** 2).mean(1))
# kick peaks
k = kick / (kick.max() + 1e-9); dk = np.r_[0, np.diff(k)]
pk = [i for i in range(2, n - 2) if k[i] == k[i - 2:i + 3].max() and k[i] > 0.25 and dk[i - 1] > 0]
pt = t[pk]
period = 60 / bpm if bpm else np.median(np.diff(pt))
# strongest kicks only (> 0.7), phase from the strongest one, then least squares on kicks near the grid
strong = pt[k[pk] > 0.7]
ref = pt[np.argmax(k[pk])]
idx = np.round((strong - ref) / period)
res = strong - (ref + period * idx)
ok = np.abs(res) < 0.06
A = np.c_[np.ones(ok.sum()), idx[ok]]
(t0, per), *_ = np.linalg.lstsq(A, strong[ok], rcond=None)
t0 = t0 - per * np.ceil(t0 / per); idx = np.round((strong - t0) / per); ok = np.abs(strong - (t0 + per * idx)) < 0.06
print(f"kick grid: t = {t0:.4f} + {per:.5f} n  ({60/per:.2f} BPM), {ok.sum()} kicks, rms {np.sqrt(np.mean((strong[ok]-(t0+per*idx[ok]))**2))*1000:.1f} ms")
nb0 = -int(t0 // per)
end_rms = rms.max() * 0.03
last = t[np.where(rms > end_rms)[0][-1]]
print(f"duration {len(x)/SR:.2f} s; last audio above 3% peak RMS at {last:.2f} s")
print(" n     t      rms   kick  flux   bar")
for b in range(nb0, int((len(x) / SR - t0) / per) + 1):
    tb = t0 + per * b
    m = (t >= tb - 0.08) & (t < tb + 0.12)
    if not m.any(): continue
    print(f"{b:3d} {tb:7.3f}  {rms[m].max()/rms.max():.2f}  {k[m].max():.2f}  {flux[m].max()/flux.max():.2f}  {'|' if b % 4 == 0 else ' '}"
          + "#" * int(20 * rms[m].max() / rms.max()))
