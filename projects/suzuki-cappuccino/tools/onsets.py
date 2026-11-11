"""Broadband kick onset (half-rise of a 1 ms RMS envelope) for every beat of the 126 BPM grid of the source track.
  onsets.py track.mp3 out.json    -> {"beat_onsets": [...], "frames": [round(onset*30)]}"""
import json, subprocess, sys
import numpy as np
sr = 48000
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
w = sr // 1000; env = np.sqrt(np.convolve(y ** 2, np.ones(w) / w, mode="same"))
T0, P = 0.033, 60 / 126.0
ons = []
for n in range(int((len(y) / sr - T0) / P) + 1):
    c = T0 + n * P; a, b = max(0, int((c - 0.12) * sr)), int((c + 0.12) * sr)
    seg = env[a:b]; pk = int(np.argmax(seg)); base = np.percentile(seg[:max(1, pk)], 10) if pk else seg.min()
    half = base + (seg[pk] - base) / 2; i = pk
    while i > 0 and seg[i] > half: i -= 1
    ons.append(round((a + i) / sr, 4))
json.dump({"beat_onsets": ons, "frames": [round(o * 30) for o in ons]}, open(sys.argv[2], "w"))
print([(n, o, round(o * 30)) for n, o in enumerate(ons) if n % 2 == 0])
