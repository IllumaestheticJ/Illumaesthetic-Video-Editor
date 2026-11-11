"""C_final = x-ray frames, crossfading into the clay pass (listing grey on listing background) over frames A..B, clay after.
   python morph_end.py C_dir C_clay_dir out_dir A B"""
import sys, os, shutil
from PIL import Image
src, clay, out, a, b = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
os.makedirs(out, exist_ok=True)
for f in sorted(os.listdir(src)):
    n = int(f[2:6]); p = os.path.join(out, f)
    if n < a:
        shutil.copy(os.path.join(src, f), p); continue
    t = min(1.0, (n - a) / (b - a)); t = t * t * (3 - 2 * t)
    Image.blend(Image.open(os.path.join(src, f)).convert("RGB"), Image.open(os.path.join(clay, f)).convert("RGB"), t).save(p)
print(out)
