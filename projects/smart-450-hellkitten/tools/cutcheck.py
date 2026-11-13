"""Cut sync on the DELIVERED file (lessons: zero-phase kick band 35-110 Hz, 1 ms RMS, half-rise before the envelope peak).

    python projects/smart-450-hellkitten/tools/cutcheck.py [delivered.mp4]

1. decode the audio of the delivered mp4 (the mix, which is what the viewer hears; the music dominates the kick band),
2. find the picture cut frames in the decoded video (largest frame-to-frame luma/difference jumps, matched to the shot table),
3. for each cut: kick onset = first half-rise of the 1 ms RMS of the 35-110 Hz band within +-90 ms of the cut time, taken in the
   ~60 ms before the local envelope peak; report cut time - onset (ms) and the shot-table frame (measured frame vs expected).
Cuts that fall in a section with no kick (breaks, riser) are reported as 'no kick' and judged against the music grid instead.
"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfiltfilt

sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, FPS, SM

SR = 44100
f = sys.argv[1] if len(sys.argv) > 1 else f"{SM}/out/smart450_v4.mp4"

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).astype(np.float64)
sos = butter(4, [35, 110], btype="band", fs=SR, output="sos")
k = sosfiltfilt(sos, x)
w = SR // 1000
env = np.sqrt(np.convolve(k ** 2, np.ones(w) / w, mode="same"))

# measured cut frames: mean abs difference between consecutive frames at low res
vid = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=72:128,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
fr = np.frombuffer(vid, np.uint8).reshape(-1, 128, 72).astype(np.int16)
d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))   # d[i] = change into frame i+1
nfr = len(fr)

hp = np.sqrt(np.convolve(sosfiltfilt(butter(4, 2500, btype="high", fs=SR, output="sos"), x) ** 2, np.ones(w) / w, mode="same"))
rows = []
glob_peak = env.max()
for s in SHOTS[1:]:
    exp = s["start"]
    lo, hi = max(1, exp - 3), min(nfr - 1, exp + 3)
    cand = np.arange(lo, hi + 1)
    meas = int(cand[np.argmax(d[cand - 1])])               # frame index of the first frame of the new shot
    t_cut = exp / FPS                                       # direction's cut time convention: first frame of the shot
    t_meas = meas / FPS
    a, b = int(max(0, t_cut - 0.09) * SR), int((t_cut + 0.09) * SR)
    seg = env[a:b]
    pk = a + int(np.argmax(seg))
    onset = None
    if seg.max() > 0.12 * glob_peak:
        # half-rise within the 60 ms before the peak: last sample below 30 % of the local peak, then +1 ms
        pre = env[max(a, pk - int(0.06 * SR)):pk + 1]
        lowp = np.where(pre < 0.30 * env[pk])[0]
        onset = (max(a, pk - int(0.06 * SR)) + (lowp[-1] if len(lowp) else 0)) / SR
    # kick click (hi band > 2.5 kHz): half-rise within 20 ms before the nearest strong peak in +-70 ms
    a2, b2 = int(max(0, t_cut - 0.07) * SR), int((t_cut + 0.07) * SR)
    pk2 = a2 + int(np.argmax(hp[a2:b2])); lo2 = max(a2, pk2 - int(0.02 * SR)); lw = np.where(hp[lo2:pk2 + 1] < 0.3 * hp[pk2])[0]
    click = (lo2 + (lw[-1] + 1 if len(lw) else 0)) / SR if hp[pk2] > 0.5 * hp.max() else None
    rows.append(dict(shot=s["id"], expected_frame=exp, measured_frame=meas, cut_s=round(t_meas, 4),
                     click_s=None if click is None else round(click, 4),
                     click_err_ms=None if click is None else round((t_meas - click) * 1000, 1),
                     kickband_s=None if onset is None else round(onset, 4),
                     kickband_lag_ms=None if onset is None else round((onset - t_meas) * 1000, 1), peak_rel=round(float(seg.max() / glob_peak), 2)))
print(f"video frames {nfr} audio {len(x)/SR:.3f}s")
for r in rows:
    print(r)
errs = [r["click_err_ms"] for r in rows if r["click_err_ms"] is not None]
print("cuts on a kick click:", len(errs), "mean", round(float(np.mean(errs)), 1), "max abs", round(float(np.max(np.abs(errs))), 1), "ms (half frame = 16.7)")
lag = [r["kickband_lag_ms"] for r in rows if r["kickband_lag_ms"] is not None]
print("kick-band (35-110 Hz) 30 % half-rise lags the cut by", round(float(np.mean(lag)), 1), "ms on average (bass swell after the click)")
Path(f.replace(".mp4", "_cutcheck.json")).write_text(json.dumps(rows, indent=1))
