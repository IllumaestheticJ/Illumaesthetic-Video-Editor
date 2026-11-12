"""Kick-attack grid for a music file (numpy + scipy): 40-120 Hz zero-phase envelope, attacks = half-rise before each
peak; least-squares tempo fit; per-second RMS map. Usage: python kicks.py track.mp3 [out.json]"""
import json, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks

def load(p, sr=48000):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    return x, sr

def main(p, out=None):
    x, sr = load(p)
    lo = sosfiltfilt(butter(4, [40, 120], "bandpass", fs=sr, output="sos"), x)
    w = int(0.004 * sr); env = np.sqrt(np.convolve(lo ** 2, np.ones(w) / w, "same"))
    pk, _ = find_peaks(env, height=0.25 * np.percentile(env, 99.5), distance=int(0.25 * sr))
    att = []
    for i in pk:
        a = i - int(0.08 * sr); seg = env[a:i]
        j = np.flatnonzero(seg < 0.5 * env[i]); att.append((a + (j[-1] if len(j) else 0)) / sr)
    att = np.array(att)
    d = np.diff(att); per = np.median(d[(d > 0.3) & (d < 0.9)])
    k = np.round((att - att[0]) / per); A = np.vstack([np.ones_like(k), k]).T
    t0, per = np.linalg.lstsq(A, att, rcond=None)[0]
    res = att - (t0 + per * k)
    rms = [float(20 * np.log10(np.sqrt(np.mean(x[i * sr:(i + 1) * sr] ** 2)) + 1e-9)) for i in range(len(x) // sr)]
    r = dict(bpm=60 / per, period=per, t0=t0, n=len(att), resid_ms=float(np.sqrt(np.mean(res ** 2)) * 1000),
             attacks=[round(float(a), 4) for a in att], rms_db=[round(v, 1) for v in rms])
    print(json.dumps({k_: v for k_, v in r.items() if k_ not in ("attacks",)}, indent=0)[:1500])
    print("attacks", " ".join(f"{a:.3f}" for a in att))
    if out: json.dump(r, open(out, "w"), indent=1)

if __name__ == "__main__":
    main(*sys.argv[1:])
