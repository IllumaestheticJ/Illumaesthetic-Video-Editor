"""Check the DELIVERED mp4, not the plan: loudness, cut frames, frozen/black frames, kick sync.
  python verify_delivery.py out.mp4 --cuts 103,206,309 [--lock 1131]
Pass = integrated loudness about -14 LUFS, true peak < -1 dBFS, every cut one clean jump, low-band onset within ~35 ms."""
import argparse, glob, os, re, subprocess, tempfile
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('mp4'); ap.add_argument('--cuts', required=True); ap.add_argument('--lock', type=int)
a = ap.parse_args(); cuts = [int(c) for c in a.cuts.split(',')]
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', a.mp4, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1]); pk = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1])
print(f'loudness {I} LUFS, true peak {pk} dBFS', '' if (-16 <= I <= -12.5 and pk < -1) else '  <-- FIX (target about -14 LUFS, peak < -1 dBFS)')
with tempfile.TemporaryDirectory() as d:
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.mp4, '-vf', 'scale=270:480', d + '/f_%04d.png'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.mp4, '-ac', '1', '-ar', '22050', d + '/a.wav'], check=True)
    from PIL import Image
    A = [np.asarray(Image.open(f).convert('L'), float) for f in sorted(glob.glob(d + '/f_*.png'))]
    import librosa, scipy.signal as ss
    y, sr = librosa.load(d + '/a.wav', sr=22050)
dd = np.array([0] + [np.abs(A[i] - A[i - 1]).mean() for i in range(1, len(A))])
for c in cuts: print('cut', c, 'frame diffs around it', np.round(dd[c - 2:c + 3], 1), '' if dd[c] > 5 * max(dd[c - 1], dd[c + 1], 0.2) else '  <-- not a clean single jump')
print('frozen frames before the last cut:', [i for i in range(1, cuts[-1]) if dd[i] < 0.01][:20])
print('black frames:', [i for i, x in enumerate(A) if x.mean() < 1.0][:30])
b, a2 = ss.butter(4, [40, 120], btype='band', fs=sr); lo = ss.filtfilt(b, a2, y)
on = librosa.onset.onset_detect(y=lo, sr=sr, units='time', hop_length=128, backtrack=True)
for c in cuts + ([a.lock] if a.lock else []):
    t = c / 30; e = (on[np.argmin(abs(on - t))] - t) * 1000; print(f'frame {c} t={t:.3f}s nearest 40-120 Hz onset {e:+.0f} ms', '' if abs(e) <= 35 else '  <-- check by ear / grid')
