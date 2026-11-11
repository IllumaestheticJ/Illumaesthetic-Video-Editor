"""Contact strip of a rendered shot: sheet.py <frames dir> out.png [n]"""
import sys, os
from PIL import Image
d, out = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
c = Image.new("RGB", (270 * n, 480))
for i, f in enumerate(pick): c.paste(Image.open(os.path.join(d, f)).convert("RGB").resize((270, 480)), (i * 270, 0))
c.save(out); print(out, pick)
