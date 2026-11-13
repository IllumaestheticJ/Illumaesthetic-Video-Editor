"""finalize.py shot_dir fps_src fps_out WxH : luma scan of png/ + previews.
Writes <shot>/luma.txt, <shot>/<shot>_src.mov (ProRes 422 HQ at source fps, scaled to WxH),
<shot>/<shot>_preview.mp4 (H.264, minterpolated to fps_out, WxH)."""
import sys, glob, os, subprocess
import numpy as np
from PIL import Image
d, fs, fo, wh = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
n = os.path.basename(d.rstrip("/"))
fr = sorted(glob.glob(f"{d}/png/f_*.png"))
L = []
for f in fr:
    a = np.asarray(Image.open(f).convert("L"), dtype=np.float32)
    L.append((os.path.basename(f), a.mean(), np.percentile(a, 99.5)))
m = np.array([x[1] for x in L])
jumps = np.abs(np.diff(m)) if len(m) > 1 else np.array([0])
bad = [L[i][0] for i in range(len(L)) if L[i][2] < 60]
with open(f"{d}/luma.txt", "w") as o:
    for x in L: o.write("%s mean %.2f p99.5 %.1f\n" % x)
    o.write(f"frames {len(L)} mean {m.min():.2f}..{m.max():.2f} max_step {jumps.max():.2f} dark_frames {bad}\n")
print(n, f"frames {len(L)} mean {m.min():.2f}..{m.max():.2f} max_step {jumps.max():.2f} dark {bad}")
W, H = wh.split("x")
sc = f"scale={W}:{H}:flags=lanczos"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fs), "-i", f"{d}/png/f_%04d.png", "-vf", sc,
                "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", f"{d}/{n}_src.mov"], check=True)
vf = sc if abs(fs - fo) < 1e-3 else f"minterpolate=fps={fo}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,{sc}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fs), "-i", f"{d}/png/f_%04d.png", "-vf", vf + ",format=yuv420p",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-r", str(fo), f"{d}/{n}_preview.mp4"], check=True)
print("encoded", n)
