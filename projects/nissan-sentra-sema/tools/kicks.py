"""Kick attacks (35-120 Hz envelope, zero-phase, half-rise before each peak) and broadband hits of a track window.
  kicks.py track t0 t1  -> prints onset times (s) and writes nothing; numpy + scipy + ffmpeg only."""
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks
trk, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); sr = 22050
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', trk, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).astype(float)
lo = sosfiltfilt(butter(4, [35, 120], 'bandpass', fs=sr, output='sos'), x)
w = int(sr * 0.008); env = np.sqrt(np.convolve(lo ** 2, np.ones(w) / w, 'same'))
pk, pr = find_peaks(env, height=env.max() * 0.35, distance=int(sr * 0.15))
on = []
for p in pk:
    a = max(0, p - int(sr * 0.06)); seg = env[a:p]; lowi = a + int(np.argmin(seg)); half = (env[lowi] + env[p]) / 2
    k = lowi + int(np.argmax(env[lowi:p] >= half)); on.append((t0 + k / sr, env[p] / env.max()))
print(' '.join(f'{t:.3f}({s:.1f})' for t, s in on))
d = np.diff([t for t, _ in on]); print('median gap', np.median(d).round(4), 'n', len(on))
