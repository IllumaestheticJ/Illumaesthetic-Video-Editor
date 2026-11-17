"""v0 delivery checks: cut frames (frame diff) vs kick attacks in the DECODED audio, loudness/true peak, frame count.
usage: python verify.py OUT.mp4"""
import subprocess, sys, json, numpy as np, scipy.signal as ss
out = sys.argv[1]
W, H = 108, 192
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', out, '-vf', f'scale={W}:{H},format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)
diff = np.abs(np.diff(v, axis=0)).mean((1, 2))
cuts = [i + 1 for i in range(1, len(diff) - 1) if diff[i] > 4 and diff[i] > 3 * np.median(diff[max(0, i - 6):i + 6])]
print('frames', len(v), 'duration', len(v) / 30)
print('cut frames (diff)', cuts)
a = subprocess.run(['ffmpeg', '-v', 'error', '-i', out, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
y = np.frombuffer(a, np.float32); sr = 48000
sos = ss.butter(4, [40, 120], 'band', fs=sr, output='sos'); lo = ss.sosfiltfilt(sos, y)
env = np.abs(ss.hilbert(lo)); hop = 48; e = np.convolve(env[::hop], np.ones(5) / 5, 'same')
pk, _ = ss.find_peaks(e, height=e.max() * 0.3, distance=int(0.3 * sr / hop))
att = []
for p in pk:  # half-rise attack before the low-pass peak
    j = p
    while j > 0 and e[j] > e[p] * 0.5: j -= 1
    att.append(j * hop / sr)
att = np.array(att)
print('kick attacks', np.round(att, 3).tolist())
for c in cuts:
    t = c / 30; k = att[np.argmin(np.abs(att - t))]
    print(f'cut {c:4d} ({t:6.3f}s)  nearest kick {k:6.3f}s  err {1000 * (t - k):+6.0f} ms')
ln = subprocess.run(['ffmpeg', '-nostats', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
tail = ln[ln.rfind('Summary'):]
print(tail)
