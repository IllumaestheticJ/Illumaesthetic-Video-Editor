"""Contact sheet of a PNG frame dir: framesheet.py dir out.jpg [n=8]  (n evenly spaced frames incl. first/last, 270 px wide)"""
import glob, sys
from PIL import Image, ImageDraw
fs = sorted(glob.glob(sys.argv[1] + "/f_*.png")); n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
pick = [fs[round(i * (len(fs) - 1) / (n - 1))] for i in range(n)]
ims = [Image.open(f) for f in pick]; w = 270; h = int(ims[0].height * w / ims[0].width)
s = Image.new("RGB", (w * n, h))
for i, (f, im) in enumerate(zip(pick, ims)):
    s.paste(im.resize((w, h)), (i * w, 0)); ImageDraw.Draw(s).text((i * w + 4, 4), f.split("/")[-1][2:6], fill=(255, 255, 0))
s.save(sys.argv[2]); print(sys.argv[2], len(fs), "frames")
