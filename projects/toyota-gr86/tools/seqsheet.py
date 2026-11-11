"""Contact sheet of a PNG sequence: n evenly spaced frames in one row.  seqsheet.py dir out.jpg [n]"""
import glob, sys
from PIL import Image
fs = sorted(glob.glob(sys.argv[1] + "/f_*.png")); n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
ims = [Image.open(f).resize((270, 480)) for f in pick]
o = Image.new("RGB", (len(ims) * 276, 480), (60, 60, 60))
for i, im in enumerate(ims): o.paste(im, (i * 276, 0))
o.save(sys.argv[2]); print(sys.argv[2], len(fs), "frames")
