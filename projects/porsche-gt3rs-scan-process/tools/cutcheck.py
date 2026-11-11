"""Cut timing vs the decoded audio of a delivered reel: broadband onset = half-rise of a 1 ms RMS envelope (rule 2026-11-11).
   python cutcheck.py video.mp4 frame1,frame2,...  [fps]"""
import subprocess, sys, numpy as np
v, frames = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]; fps = float(sys.argv[3]) if len(sys.argv) > 3 else 30
sr = 48000
a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', v, '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
w = sr // 1000; env = np.sqrt(np.convolve(a.astype(float) ** 2, np.ones(w) / w, 'same'))
for f in frames:
    t = f / fps; i0, i1 = int((t - 0.12) * sr), int((t + 0.12) * sr)
    seg = env[i0:i1]; pk = np.argmax(seg); base = np.percentile(env[max(0, i0 - sr // 10):i0], 20)
    half = base + (seg[pk] - base) / 2; j = pk
    while j > 0 and seg[j] > half: j -= 1
    on = (i0 + j) / sr
    print(f'cut f{f} {t:.3f}s  onset {on:.3f}s  err {1000*(t-on):+5.0f} ms')
