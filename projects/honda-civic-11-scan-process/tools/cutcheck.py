"""Measure cut frames (frame-diff spikes) and kick peaks (40-120 Hz) in a delivered mp4; print the error per cut.
usage: cutcheck.py video.mp4 t1,t2,...   (expected cut times in s)"""
import sys, subprocess, numpy as np
v = sys.argv[1]; exp = [float(x) for x in sys.argv[2].split(',')]
raw = subprocess.run(['ffmpeg', '-v', 'quiet', '-i', v, '-vf', 'scale=135:240', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 240, 135).astype(float); d = np.abs(np.diff(fr, axis=0)).mean((1, 2))
sr = 22050; y = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'quiet', '-i', v, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
n, h = 1024, 128; F = np.lib.stride_tricks.sliding_window_view(y, n)[::h] * np.hanning(n)
S = np.abs(np.fft.rfft(F, axis=1)); f = np.fft.rfftfreq(n, 1 / sr); low = S[:, (f > 40) & (f < 120)].sum(1); t = (np.arange(len(S)) * h + n / 2) / sr
for e in exp:
    k = int(round(e * 30)); w = d[max(0, k - 4):k + 3]; cf = max(0, k - 4) + int(np.argmax(w)) + 1   # first frame of new shot
    m = (t > e - 0.15) & (t < e + 0.15); kt = t[m][np.argmax(low[m])] if m.any() else float('nan')
    print(f"expected {e:7.3f}  cut frame {cf:4d} ({cf/30:7.3f})  kick {kt:7.3f}  cut-kick {1000*(cf/30-kt):+6.0f} ms")
