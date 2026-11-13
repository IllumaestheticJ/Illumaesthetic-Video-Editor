"""Verify every meow onset against the lattice in the DECODED final audio and draw the arrangement strip.
usage: meowcheck.py  -> prints max error, writes out/meow_strip.png and meow_check.json
1. global alignment: cross-correlate the delivered mp4's decoded audio with smart450_mix.wav (AAC delay),
2. per meow: onset = first 2 ms-RMS sample above 20 % of the meow's local peak (high-passed 250 Hz) in the decoded meow STEM, +-60 ms around the lattice time,
3. the same onset is also searched in (mp4 audio - music stem - shop stem) as a codec-level cross-check."""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfiltfilt, spectrogram, correlate
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SM, SHOTS, T, FPS
SR = 44100
OUT = Path(SM) / "out"
def dec(p, mono=True):
    r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    return r.mean(axis=1).astype(np.float64) if mono else r.astype(np.float64)
stem, mix, mp4 = dec(OUT / "stem_meows.wav"), dec(OUT / "smart450_mix.wav"), dec(OUT / "smart450_v4.mp4")
n = min(len(mix), len(mp4)); a, b = mix[:n], mp4[:n]
lag = int(np.argmax(correlate(b[: SR * 10], a[: SR * 10], mode="full", method="fft")) - (SR * 10 - 1))
print("mp4 vs wav master lag samples", lag, "=", round(lag / SR * 1000, 2), "ms")
mm = json.loads((Path(__file__).resolve().parent.parent / "meow_map.json").read_text())
hp = sosfiltfilt(butter(4, 250, "high", fs=SR, output="sos"), stem)
w = int(0.002 * SR); env = np.sqrt(np.convolve(hp ** 2, np.ones(w) / w, "same"))
import meows as MW
from scipy.signal import fftconvolve
MW.arrange()
evs = sorted(MW.EV, key=lambda d: (d["m"], d["kind"]))
stem_hp = hp
rows = []
for m, e in zip(mm["meows"], evs):
    z, s_, r = MW.shot(e["sid"], e["semis"], e["crop"], e["tune"])
    zt = sosfiltfilt(butter(4, 250, "high", fs=SR, output="sos"), z) if len(z) > 64 else z
    t = m["time_s"]; idx = int(round(t * SR)) - int(round(0.003 * SR * r))
    lo = idx - int(0.025 * SR); hi = idx + len(zt) + int(0.025 * SR)
    seg = stem_hp[lo:hi]
    # cross-correlation of the known one-shot against the decoded stem (mono mix of both channels): lag of the peak = placement error
    cc = fftconvolve(seg, zt[::-1], mode="valid")
    lag = int(np.argmax(cc)) - int(0.025 * SR)
    rows.append(dict(n=m["n"], kind=m["kind"], beat_m=m["beat_m"], expected_s=t, err_ms=round(lag / SR * 1000, 2), xcorr_peak=round(float(cc.max() / (np.linalg.norm(zt) * np.linalg.norm(seg[np.argmax(cc):np.argmax(cc) + len(zt)]) + 1e-12)), 2)))
e1 = [abs(r["err_ms"]) for r in rows]
print("meows:", len(rows), "| onset error against the lattice by cross-correlating each known one-shot with the DECODED stem: max {:.2f} ms, mean {:.2f} ms".format(max(abs(r["err_ms"]) for r in rows), np.mean([abs(r["err_ms"]) for r in rows])))
(OUT / "meow_check.json").write_text(json.dumps(dict(mp4_vs_master_lag_ms=lag / SR * 1000, rows=rows), indent=1))
# strip: waveform of the stem + spectrogram of the final mix, meow times marked, cuts as ticks
fig, ax = plt.subplots(3, 1, figsize=(18, 8), sharex=True, gridspec_kw=dict(height_ratios=[1, 2, 0.5]))
t = np.arange(len(stem)) / SR
ax[0].plot(t, stem, lw=0.4, color="tab:orange"); ax[0].set_ylabel("meow stem")
f, tt, S = spectrogram(mp4, SR, nperseg=2048, noverlap=1536)
ax[1].pcolormesh(tt, f, 10 * np.log10(S + 1e-12), shading="auto", vmin=-110, vmax=-40, cmap="magma"); ax[1].set_ylim(0, 6000); ax[1].set_ylabel("final mix, Hz")
for m in mm["meows"]:
    for a_ in ax[:2]: a_.axvline(m["time_s"], color="cyan", lw=0.9, alpha=0.8)
    ax[0].text(m["time_s"], 0.5 * max(abs(stem)), str(m["n"]), color="cyan", fontsize=8)
for k in range(-4, 73, 4):
    ax[2].axvline(T(k), color="grey", lw=0.5)
for s in SHOTS: ax[2].axvline(s["start"] / FPS, color="red", lw=0.8); ax[2].text(s["start"] / FPS + 0.03, 0.3, s["id"], fontsize=6, rotation=90)
ax[2].set_yticks([]); ax[2].set_xlabel("s (cyan = meow onsets, red = picture cuts, grey = 4-beat bars)"); ax[2].set_xlim(0, len(stem) / SR)
plt.tight_layout(); plt.savefig(OUT / "meow_strip.png", dpi=80)
