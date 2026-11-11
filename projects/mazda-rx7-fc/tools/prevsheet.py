"""Contact sheet of preview renders: one row per shot (first/mid/last). prevsheet.py out.jpg dir1 [dir2 ...]"""
import sys, glob
from PIL import Image
rows = [sorted(glob.glob(f"{d}/*.png"))[:3] for d in sys.argv[2:]]
im0 = Image.open(rows[0][0]); W, H = im0.width // 2, im0.height // 2
o = Image.new("RGB", (W * 3 + 8, (H + 4) * len(rows)), (60, 0, 0))
for r, fs in enumerate(rows):
    for c, f in enumerate(fs):
        o.paste(Image.open(f).convert("RGB").resize((W, H)), (c * (W + 4), r * (H + 4)))
o.save(sys.argv[1]); print(sys.argv[1])
