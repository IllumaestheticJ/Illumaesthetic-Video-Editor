"""Per-frame mean luma of rendered shots; flags any frame-to-frame step > thr (lighting dropout check, lessons.md).
    lumacheck.py shotdir [shotdir ...] [--thr 4]"""
import glob, sys
from PIL import Image, ImageStat
thr = float(sys.argv[sys.argv.index("--thr") + 1]) if "--thr" in sys.argv else 4.0
for d in [a for a in sys.argv[1:] if a.startswith("/")]:
    fs = sorted(glob.glob(d + "/f_*.png"))
    m = [ImageStat.Stat(Image.open(f).convert("L").reduce(4)).mean[0] for f in fs]
    bad = [(i + 1, round(m[i - 1], 1), round(m[i], 1)) for i in range(1, len(m)) if abs(m[i] - m[i - 1]) > thr]
    print(f"{d.split('/')[-1]:12s} {len(fs)} frames  luma {min(m):.1f}-{max(m):.1f}  steps>{thr}: {bad or 'none'}")
