"""Contact sheet of a rendered frame folder: N evenly spaced frames.  sheet.py dir out.jpg [N]"""
import os, sys
from PIL import Image
d, out = sys.argv[1:3]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
W, H = 270, 480
im = Image.new("RGB", (W * n, H))
for i, f in enumerate(pick): im.paste(Image.open(f"{d}/{f}").convert("RGB").resize((W, H)), (i * W, 0))
im.save(out, quality=85); print(out, len(fs), "frames")
