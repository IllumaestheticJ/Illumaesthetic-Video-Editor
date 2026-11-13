"""s12 interior x-ray: crossfade the shell layer (s12a_shell, first 8 frames) into the interior-alone layer (s12_int_xray),
same camera, 15 fps source frames. The shell never lifts and nothing opens; it fades like an x-ray.
    python projects/a90-supra/tools/xray_v3.py  -> /home/user/media/work/a90/renders_v3/s12_comp/f_####.png"""
import glob, os, shutil
import numpy as np
from PIL import Image
R = "/home/user/media/work/a90/renders_v3/"
os.makedirs(R + "s12_comp", exist_ok=True)
for f in sorted(glob.glob(R + "s12_int_xray/f_*.png")):
    n = int(f[-8:-4]); a = R + f"s12a_shell/f_{n:04d}.png"; out = R + f"s12_comp/f_{n:04d}.png"
    k = min(1.0, max(0.0, (n - 3) / 4.0))       # frames 1-3 shell, 4-7 fade, 7+ interior (ends ~0.4 s in, before half-beat 2)
    if k >= 1 or not os.path.exists(a):
        shutil.copy(f, out); continue
    A = np.asarray(Image.open(a).convert("RGB"), float); B = np.asarray(Image.open(f).convert("RGB"), float)
    Image.fromarray(np.clip(A * (1 - k) + B * k, 0, 255).astype(np.uint8)).save(out)
print("composited", len(glob.glob(R + "s12_comp/*.png")))
