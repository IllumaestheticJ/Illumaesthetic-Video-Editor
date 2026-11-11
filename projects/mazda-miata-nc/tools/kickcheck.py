"""Cuts of a delivered reel vs the KICK in its decoded audio (brief v2: cuts on kick peaks, +-1/2 frame).

    python projects/mazda-miata-nc/tools/kickcheck.py out.mp4 --cuts 89,142,...   (cut frames; or auto-detect)

Kick = 40-120 Hz band (FFT brick-wall), 2 ms RMS envelope. For each cut, the kick attack nearest the cut
(within +-200 ms) is where the envelope first reaches 50 % of that kick's peak. Also prints the peak time.
"""
import subprocess, sys
import numpy as np

path = sys.argv[1]
fps = 30.0
if "--cuts" in sys.argv:
    cuts = [int(v) / fps for v in sys.argv[sys.argv.index("--cuts") + 1].split(",")]
else:
    W, H = 135, 240
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    d = np.r_[0, np.abs(np.diff(fr, axis=0)).mean((1, 2))]
    cuts = [i / fps for i in range(1, len(d)) if d[i] > 6 * (np.median(d[max(1, i-15):i+15]) + .05) and d[i] > 1
            and d[i] == d[max(1, i-15):i+15].max()]
sr = 8000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).astype(np.float64)
F = np.fft.rfft(a); f = np.fft.rfftfreq(len(a), 1 / sr); F[(f < 40) | (f > 120)] = 0
k = np.fft.irfft(F, len(a))
w = int(0.002 * sr); env = np.sqrt(np.convolve(k * k, np.ones(w) / w, mode="same"))
print(" cut fr   cut s  kick-attack s  peak s   err ms  err fr")
errs = []
for c in cuts:
    s0, s1 = int((c - 0.2) * sr), int((c + 0.2) * sr)
    seg = env[s0:s1]; pk = int(np.argmax(seg)); pv = seg[pk]
    # walk back from the peak to the 50 % point
    j = pk
    while j > 0 and seg[j] > 0.5 * pv: j -= 1
    att = (s0 + j) / sr; e = (c - att) * 1000; errs.append(e)
    print(f"  {round(c*fps):5d}  {c:7.3f}  {att:9.3f}  {(s0+pk)/sr:7.3f}  {e:+7.1f}  {e/1000*fps:+5.2f}")
print(f"max |err| {max(abs(e) for e in errs):.1f} ms (half frame {500/fps:.1f} ms)")
