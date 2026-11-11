"""Broadband onset (1 ms RMS half-rise) of every grid beat in the source track -> JSON {beat_index: onset_s}.
v1 cut on the kick-band grid and landed 40-60 ms late on some beats (cutcheck.py); v2 cuts go on these onsets.
  onsets.py track.mp3 out.json [--period 0.6035 --phase 0.024]"""
import argparse, json, subprocess
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("track"); ap.add_argument("out")
ap.add_argument("--period", type=float, default=0.6035); ap.add_argument("--phase", type=float, default=0.024)
a = ap.parse_args(); sr = 48000
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.track, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
w = sr // 1000; env = np.sqrt(np.convolve(pcm ** 2, np.ones(w) / w, mode="same"))
res = {}
for b in range(int((len(pcm) / sr - a.phase) / a.period)):
    tb = a.phase + b * a.period; i0, i1 = int((tb - 0.08) * sr), int((tb + 0.06) * sr)
    if i0 < int(0.05 * sr): continue
    seg = env[i0:i1]; pk = int(np.argmax(seg)); floor = np.percentile(env[i0 - int(0.05 * sr):i0], 20)
    if seg[pk] < 2 * floor: continue
    half = floor + (seg[pk] - floor) / 2; k = pk
    while k > 0 and seg[k] > half: k -= 1
    res[b] = round((i0 + k) / sr, 4)
json.dump(res, open(a.out, "w"), indent=0)
print(" ".join(f"b{b}:{t:.3f}({(t-(a.phase+b*a.period))*1000:+.0f})" for b, t in res.items()))
