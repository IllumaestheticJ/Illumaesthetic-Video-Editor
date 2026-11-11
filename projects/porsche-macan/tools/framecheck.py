"""Per-frame luma check + contact sheet for a rendered PNG sequence (lesson: scan every frame's max luma before
assembling - persistent-data renders can go unlit mid-shot).
    python projects/porsche-macan/tools/framecheck.py render_dir sheet.jpg [cols]"""
import os, sys
import numpy as np
from PIL import Image
d, out = sys.argv[1], sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 8
fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
mx, mean = [], []
for f in fs:
    a = np.asarray(Image.open(os.path.join(d, f)).convert("L").reduce(4))
    mx.append(int(a.max())); mean.append(float(a.mean()))
mean = np.array(mean); med = np.median(mean)
bad = [fs[i] for i in range(len(fs)) if mx[i] < 60 or mean[i] < 0.5 * med]
print(f"{d}: {len(fs)} frames, max luma {min(mx)}-{max(mx)}, mean {mean.min():.1f}-{mean.max():.1f}; suspicious: {bad or 'none'}")
pick = [fs[int(round(i))] for i in np.linspace(0, len(fs) - 1, min(cols * 2, len(fs)))]
ims = [Image.open(os.path.join(d, f)).convert("RGB").reduce(4) for f in pick]
w, h = ims[0].size; r = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (w * cols, h * r))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * w, (i // cols) * h))
sh.save(out, quality=85)
