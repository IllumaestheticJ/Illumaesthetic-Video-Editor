"""Cut timing vs the decoded audio of the OUTPUT (lessons: broadband onset, half-rise of a 1 ms RMS envelope).
    python projects/subaru-wrx-vb/tools/cutcheck.py out.mp4 [n_cuts]
Cuts = the n largest frame differences. Onset = for the strongest envelope rise within +-120 ms of the cut, the first
1 ms bin where the envelope reaches half way from the preceding 30 ms floor to that peak."""
import subprocess, sys
import numpy as np
f, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 7
sr = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
env = np.sqrt((a[: len(a) // 48 * 48].reshape(-1, 48) ** 2).mean(1))  # 1 ms RMS
v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=135:240", "-f", "rawvideo", "-pix_fmt",
                                  "gray", "-"], capture_output=True, check=True).stdout, np.uint8).reshape(-1, 240, 135)
d = np.abs(np.diff(v.astype(float), axis=0)).mean((1, 2))
cuts = sorted(int(i) + 1 for i in np.argsort(d)[::-1][:n])
errs = []
for c in cuts:
    t = c / 30; i0 = int(t * 1000)
    w = env[i0 - 120: i0 + 120]
    rise = np.array([w[k:k + 15].max() - w[max(0, k - 30):k].mean() for k in range(30, len(w) - 15)])
    k = int(np.argmax(rise)) + 30
    floor = w[k - 30:k].mean(); peak = w[k:k + 15].max()
    j = k - 5 + int(np.argmax(w[k - 5:k + 15] >= floor + 0.5 * (peak - floor)))
    on = (i0 - 120 + j) / 1000
    errs.append((t - on) * 1000)
    print(f"cut frame {c:5d} {t:7.3f}s  onset {on:7.3f}s  cut-onset {(t - on) * 1000:+6.1f} ms")
print("max |err| ms %.1f (half frame 16.7)" % np.abs(errs).max())
