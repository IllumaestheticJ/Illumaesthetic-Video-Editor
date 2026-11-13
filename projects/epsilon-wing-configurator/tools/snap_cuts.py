"""Snap planned cut frames to the measured kick attack on the music stem (track from MUSIC_IN): 40-120 Hz 2 ms envelope,
half-rise before the strongest peak within +-120 ms. Prints planned -> snapped frames and the residual.
  python snap_cuts.py 123 258 ..."""
import subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt
sr = 48000
m = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", "13.5", "-i", "/home/user/media/epsilon-wing-configurator/music/ewc_track.mp3",
                                  "-t", "60", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
def att(t, w0=0.12):
    lo = sosfiltfilt(butter(4, [40, 120], 'bandpass', fs=sr, output='sos'), m[int((t - w0) * sr):int((t + w0) * sr)])
    e = np.sqrt(np.convolve(lo ** 2, np.ones(96) / 96, 'same')); p = np.argmax(e)
    seg = e[max(0, p - 3840):p]; j = np.flatnonzero(seg < 0.5 * e[p])
    return t - w0 + (max(0, p - 3840) + (j[-1] if len(j) else 0)) / sr
out = []
for f in map(int, sys.argv[1:]):
    a = att(f / 30); g = round(a * 30)
    if abs(g - f) > 3: g = f      # no kick near (fill): keep the plan
    out.append(g); print(f, '->', g, f'kick {a:.3f} err {1000 * (g / 30 - a):+.1f} ms')
print(out)
