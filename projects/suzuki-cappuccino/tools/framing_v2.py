"""Framing check at given shot fractions (30 % res, 8 spp) -> one contact sheet per shot.
  framing_v2.py shot.json 0,0.5,0.9,1 out.jpg"""
import json, os, subprocess, sys, glob, tempfile
from PIL import Image
spec, fr, out = sys.argv[1], [float(v) for v in sys.argv[2].split(",")], sys.argv[3]
d = json.load(open(spec)); n = max(1, round(d["seconds"] * d["fps"]))
frames = sorted({min(n, max(1, round(f * (n - 1)) + 1)) for f in fr})
td = tempfile.mkdtemp()
subprocess.run(["blender", "-b", "-P", os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot.py"), "--", spec,
                "--res-pct", "30", "--samples", "8", "--frames", ",".join(map(str, frames)), "--out", td],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
ims = [Image.open(f"{td}/f_{f:04d}.png") for f in frames]
c = Image.new("RGB", (sum(i.width + 6 for i in ims), ims[0].height), (60, 0, 0)); x = 0
for i in ims: c.paste(i, (x, 0)); x += i.width + 6
c.save(out); print(out, frames)
