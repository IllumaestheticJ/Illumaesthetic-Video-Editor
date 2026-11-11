"""Voice stats for matching a preset voice to a reference delivery (no cloning): median F0, F0 spread, speaking-rate
proxy (voiced-segment onsets/s), pause ratio, spectral tilt. usage: voicestats.py file [start end] ..."""
import subprocess, sys, numpy as np
def load(p, a=None, b=None, sr=16000):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(a), "-to", str(b)] if a is not None else []) + ["-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32), sr
def f0_track(x, sr, fmin=70, fmax=400, hop=160, win=640):
    f0 = []
    for i in range(0, len(x) - win, hop):
        w = x[i:i + win] * np.hanning(win)
        if np.sqrt(np.mean(w ** 2)) < 0.01: f0.append(0); continue
        ac = np.correlate(w, w, "full")[win - 1:]; ac /= ac[0] + 1e-9
        lo, hi = int(sr / fmax), int(sr / fmin); k = lo + np.argmax(ac[lo:hi])
        f0.append(sr / k if ac[k] > 0.45 else 0)
    return np.array(f0)
def stats(p, a=None, b=None):
    x, sr = load(p, a, b); f = f0_track(x, sr); v = f[f > 0]
    voiced = f > 0; on = np.flatnonzero(np.diff(voiced.astype(int)) == 1)
    S = np.abs(np.fft.rfft(x[: len(x) // 1024 * 1024].reshape(-1, 1024) * np.hanning(1024), axis=1)).mean(0)
    fr = np.fft.rfftfreq(1024, 1 / sr); tilt = 10 * np.log10(S[(fr > 2000) & (fr < 5000)].mean() / S[(fr > 200) & (fr < 1000)].mean())
    dur = len(x) / sr
    return dict(f0_med=round(float(np.median(v)), 1), f0_iqr=round(float(np.subtract(*np.percentile(v, [75, 25]))), 1),
                voiced_frac=round(float(voiced.mean()), 2), syll_per_s=round(len(on) / dur, 2), tilt_db=round(float(tilt), 1), dur=round(dur, 1))
if __name__ == "__main__":
    a = sys.argv[1:]; p = a[0]
    print(p.split("/")[-1], stats(p, float(a[1]), float(a[2])) if len(a) > 2 else stats(p))
