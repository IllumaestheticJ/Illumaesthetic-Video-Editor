"""Delivery checks for the v0 mp4: cut frames vs onsets measured on the DECODED audio of the delivered file, loudness/true
peak, picture-cut detection, edge contact sheet (first/middle/last frame of every shot).
    python check_v0.py /home/user/media/work/out/bf-civic-parts-rain_v0.mp4
"""
import json, subprocess, sys
import numpy as np, librosa
from PIL import Image
V = sys.argv[1]; M = "/home/user/media/bf-civic-parts-rain"
CUTS = {"render7 (1:1)": 189, "FE offer": 246, "FL offer": 316, "end card": 369}
SEATS = {"lip": 62, "skirts": 93, "rear lip": 126, "wing": 157}
a = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-ac", "1", "-ar", "22050", "-f", "f32le", "-"], capture_output=True).stdout
y = np.frombuffer(a, np.float32); sr = 22050; hop = 64
on = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop); t = librosa.frames_to_time(np.arange(len(on)), sr=sr, hop_length=hop)
def nearest_onset(ts, win=0.12):
    m = (t > ts - win) & (t < ts + win); i = np.argmax(np.where(m, on, -1)); return t[i], on[i] / on.max()
print("event          frame  t_frame   onset   err_ms  strength")
for d in (CUTS, SEATS):
    for k, f in d.items():
        tf = f / 30; to, s = nearest_onset(tf); print(f"{k:14s} {f:5d}  {tf:7.3f}  {to:7.3f}  {1000*(tf-to):+6.0f}   {s:.2f}")
r = subprocess.run(["ffmpeg", "-v", "info", "-i", V, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
summ = r[r.rfind("Summary:"):]
print("\n".join(l.strip() for l in summ.splitlines() if any(k in l for k in ("I:", "Peak:", "LRA:"))))
# picture cuts (frame-difference peaks)
fr = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(fr, np.uint8).reshape(-1, 96, 54).astype(float); d = np.abs(np.diff(F, axis=0)).mean((1, 2))
print("frames", len(F), "| largest frame diffs at:", sorted(np.argsort(d)[-6:] + 1))
# contact sheet: first/middle/last of each shot
shots = [(0, 188), (189, 245), (246, 315), (316, 368), (369, 469), (62, 62)]
pick = [f for a_, b in shots for f in (a_, (a_ + b) // 2, b)]
sel = "+".join(f"eq(n\\,{f})" for f in pick)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", V, "-vf", f"select='{sel}',scale=180:320,tile=9x2", "-frames:v", "1", f"{M}/comp/v0_sheet.jpg"])
print("sheet", f"{M}/comp/v0_sheet.jpg")
