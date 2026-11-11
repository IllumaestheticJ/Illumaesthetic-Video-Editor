"""Snap planned cut times to the onset of the strongest kick near each one (dense mixes where the broadband
half-rise of cutcheck.py triggers on guitar/pads). Zero-phase 40-150 Hz band (no filter latency), 8 ms RMS envelope,
onset = first sample before the peak where the envelope reaches half way from the pre-hit floor to the peak.

    python projects/c5-corvette/tools/kickcut.py track_or_reel.mp3|mp4 9.393,13.839,... [--win 0.15] [--fps 30]
Prints planned time, kick onset, kick peak, strength and the onset frame (round(onset*fps)).
"""
import subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt

path, ts = sys.argv[1], [float(v) for v in sys.argv[2].split(",")]
opt = dict(zip(sys.argv[3::2], sys.argv[4::2]))
W, fps, sr = float(opt.get("--win", 0.15)), float(opt.get("--fps", 30)), 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).astype(np.float64)
lo = sosfiltfilt(butter(4, [40, 150], "band", fs=sr, output="sos"), a)
w = int(sr * 0.008)
env = np.sqrt(np.convolve(lo ** 2, np.ones(w) / w, mode="same"))
print(" planned   onset    peak    strength  frame")
for t in ts:
    s0, s1 = int((t - W) * sr), int((t + W) * sr)
    seg = env[s0:s1]; p = int(np.argmax(seg)); pk = seg[p]
    floor = env[max(0, s0 + p - int(0.12 * sr)):s0 + p].min()
    i = p
    while i > 0 and seg[i] > floor + 0.5 * (pk - floor):
        i -= 1
    on = (s0 + i) / sr
    print(f"{t:8.3f} {on:8.3f} {(s0 + p) / sr:8.3f}  {pk:6.3f}  {round(on * fps):5d}")
