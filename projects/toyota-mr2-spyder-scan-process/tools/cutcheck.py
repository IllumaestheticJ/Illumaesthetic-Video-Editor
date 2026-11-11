"""Cut timing vs the DECODED audio of a delivered file.
Cuts: frame-to-frame mean abs diff peaks (hard cuts). Hits: broadband onsets = half-rise point of a 1 ms RMS envelope
(lesson subaru-wrx-va: a low-passed envelope reads 40-70 ms late). Reports each cut's error to the nearest hit.
usage: cutcheck.py video.mp4 [--expect 96,193,...] [--thr 25]"""
import argparse, subprocess, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--expect', default=''); ap.add_argument('--thr', type=float, default=25)
a = ap.parse_args()
W, H, fps = 108, 192, 30
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
cuts = [i + 1 for i in range(len(d)) if d[i] > a.thr and d[i] >= d[max(0, i - 1)] and d[i] >= d[min(len(d) - 1, i + 1)]]
sr = 48000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                                 capture_output=True).stdout, np.float32)
w = sr // 1000
env = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
hop = w
e = env[::hop]  # 1 ms resolution
base = np.minimum.accumulate(e[::-1])[::-1]
hits = []
i = 0
look = 60  # ms window
while i < len(e) - look:
    pre = e[max(0, i - 30):i].mean() if i > 30 else e[:i + 1].mean()
    pk = i + int(np.argmax(e[i:i + look]))
    if e[pk] > 2.2 * pre + 1e-4 and e[pk] > 0.08 * e.max():
        half = pre + 0.5 * (e[pk] - pre)
        j = i
        while j < pk and e[j] < half: j += 1
        hits.append(j / 1000.0); i = pk + 150; continue
    i += 2
hits = np.array(hits)
print(f'{len(cuts)} cuts detected, {len(hits)} onsets')
exp = [int(v) for v in a.expect.split(',')] if a.expect else []
for c in cuts:
    t = c / fps
    k = np.argmin(np.abs(hits - t)) if len(hits) else 0
    err = (t - hits[k]) * 1000 if len(hits) else float('nan')
    tag = '' if not exp else ('expected' if c in exp else f'(nearest expected {min(exp, key=lambda e_: abs(e_ - c))})')
    print(f'cut @ frame {c:4d} = {t:7.3f} s  nearest onset {hits[k]:7.3f} s  err {err:+6.1f} ms  ({err / (1000 / fps):+.2f} fr) {tag}')
