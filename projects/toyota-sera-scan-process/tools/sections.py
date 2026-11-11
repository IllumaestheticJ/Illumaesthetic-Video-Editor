"""Per-beat band energies on the kick grid -> find section changes (drop) and accented beats.
    python tools/sections.py track.mp3 t0 period
"""
import subprocess, sys
import numpy as np
sr = 22050
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, dtype=np.float32)
t0, per = float(sys.argv[2]), float(sys.argv[3])
bands = [(30, 120), (120, 500), (500, 2000), (2000, 6000), (6000, 11000)]
rows = []
k = 0
while t0 + (k + 1) * per <= len(x) / sr:
    a = int((t0 + k * per) * sr); seg = x[a:a + int(per * sr)]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))); f = np.fft.rfftfreq(len(seg), 1 / sr)
    e = [np.log10(S[(f >= lo) & (f < hi)].sum() + 1e-9) for lo, hi in bands]
    # transient strength at the beat (first 60 ms vs previous 60 ms), full band
    w = int(0.06 * sr); pre = x[max(0, a - w):a]; post = x[a:a + w]
    tr = float(np.sqrt(np.mean(post ** 2)) / (np.sqrt(np.mean(pre ** 2)) + 1e-6))
    rows.append((k, t0 + k * per, *e, tr)); k += 1
R = np.array(rows)
print("beat  time   sub   lowmid  mid   hi    air   transient")
for r in R:
    print(f"{int(r[0]):3d} {r[1]:6.3f} " + " ".join(f"{v:5.2f}" for v in r[2:7]) + f"  {r[7]:5.2f}")
# novelty between consecutive 4-beat blocks
B = R[:, 2:7]
print("\nblock novelty (4-beat blocks, L2 of mean band diff):")
for i in range(4, len(B) - 3, 4):
    print(f" beat {i:3d} t={R[i,1]:6.3f}  {np.linalg.norm(B[i:i+4].mean(0) - B[i-4:i].mean(0)):.3f}")
