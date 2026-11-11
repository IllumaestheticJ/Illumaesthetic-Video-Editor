"""Side-by-side contact strip of images (scaled to a common height). hstack.py out.jpg a.png b.png ... [--h 640]"""
import sys
from PIL import Image
a = sys.argv[1:]; out = a.pop(0); H = 640
if "--h" in a: i = a.index("--h"); H = int(a[i + 1]); del a[i:i + 2]
ims = [Image.open(p).convert("RGB") for p in a]
ims = [im.resize((int(im.width * H / im.height), H)) for im in ims]
s = Image.new("RGB", (sum(i.width for i in ims) + 6 * (len(ims) - 1), H), (60, 0, 0)); x = 0
for im in ims: s.paste(im, (x, 0)); x += im.width + 6
s.save(out, quality=88); print(out, s.size)
