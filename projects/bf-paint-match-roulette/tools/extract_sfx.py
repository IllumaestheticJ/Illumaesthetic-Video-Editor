"""Recover a menu SFX from a gameplay capture that has music underneath.

The same sample plays at every menu action over different music. Align every instance (band-passed cross-correlation
against an iteratively refined template) and take the median: the sound adds coherently, the music does not.
python3 extract_sfx.py <audio.wav> <events.json> <kind> <out.wav> [offset_s] [f_lo] [f_hi]
"""
import sys, json, wave, numpy as np
from scipy.signal import butter, sosfiltfilt, fftconvolve
wav, evf, kind, out = sys.argv[1:5]
OFF = float(sys.argv[5]) if len(sys.argv) > 5 else 0.18
FLO = float(sys.argv[6]) if len(sys.argv) > 6 else 450
FHI = float(sys.argv[7]) if len(sys.argv) > 7 else 2500
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
ts = [t for t, k in json.load(open(evf)) if k == kind]
bp = sosfiltfilt(butter(4, [FLO, FHI], 'bp', fs=sr, output='sos'), x)
L = int(1.0 * sr); PRE = int(0.06 * sr); SR = int(0.12 * sr)      # window, pre-roll, search radius
starts0 = [int((t + OFF) * sr) - PRE for t in ts]
starts0 = [a for a in starts0 if a - SR >= 0 and a + L + SR < len(x)]
# seed template: the instance whose band energy jumps the most at the expected onset
def jump(a): return (bp[a + PRE:a + PRE + 4000] ** 2).sum() / ((bp[a:a + PRE] ** 2).sum() + 1e-6)
tmpl = bp[max(starts0, key=jump):][:L].copy()
for it in range(4):
    k = tmpl[:int(0.35 * sr)]; kn = k / (np.linalg.norm(k) + 1e-9)
    al, sc = [], []
    for a in starts0:
        seg = bp[a - SR:a + SR + len(k)]
        c = fftconvolve(seg, kn[::-1], 'valid'); e = np.sqrt(fftconvolve(seg ** 2, np.ones(len(k)), 'valid') + 1e-9)
        nc = c / e; j = int(np.argmax(nc)); al.append(a - SR + j); sc.append(float(nc[j]))
    sc = np.array(sc); thr = max(0.25, np.percentile(sc, 40))
    good = [a for a, s in zip(al, sc) if s >= thr]
    tmpl = np.median(np.array([bp[a:a + L] for a in good]), 0)
    print(kind, 'iter', it, 'events', len(al), 'kept', len(good), 'median ncc', round(float(np.median(sc)), 3), 'thr', round(float(thr), 3), flush=True)
full = np.array([x[a:a + L] for a in good]); med = np.median(full, 0)
# level: scale so the band RMS matches the typical single instance (median shrinks nothing coherent)
env = np.sqrt(np.convolve(med ** 2, np.ones(1024) / 1024, 'same')); pk = env.max()
on = max(0, int(np.argmax(env > pk * 0.05)) - 200)
end = len(med) - 1 - int(np.argmax(env[::-1] > pk * 0.04)); end = min(len(med), end + int(0.04 * sr))
y = med[on:end].copy(); n = int(0.03 * sr); y[-n:] *= np.linspace(1, 0, n); y[:100] *= np.linspace(0, 1, 100)
noise = float(np.sqrt((med[:int(0.03 * sr)] ** 2).mean())); sig = float(np.sqrt((y ** 2).mean()))
print(kind, 'instances used', len(good), 'length s', round(len(y) / sr, 3), 'peak', round(float(np.abs(y).max()), 3),
      'residual music vs sfx dB', round(20 * np.log10(noise / sig + 1e-9), 1))
o = wave.open(out, 'w'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
o.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); o.close()
