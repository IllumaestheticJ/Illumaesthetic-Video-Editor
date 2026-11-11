"""Registration check sheets: each part (red) over the grey car + the part alone (silver), from outside the part.
    python projects/porsche-gt3rs-992/tools/regcheck.py part [part ...]      (names of prep/<part>.blend)
Writes /home/user/media/work/gt3/reg/<part>_sheet.jpg (overlay | overlay close | solo)."""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image
W = "/home/user/media/porsche-gt3rs-992"; R = "/home/user/media/work/gt3/reg"
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot.py")
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(f"{W}/prep/car4.json"))["root_location"])

def view(part, cam_dir=None):
    c = np.fromfile(f"{W}/parts/{part}_2mm.stl", dtype=TRI, offset=84)["v"].reshape(-1, 3)[::7] * 0.001 + root
    lo, hi = np.percentile(c, 1, 0), np.percentile(c, 99, 0)
    ctr = (lo + hi) / 2; size = np.linalg.norm(hi - lo)
    d = np.array(cam_dir) if cam_dir else np.array([ctr[0], ctr[1] * 0.6, 0.0])
    if np.linalg.norm(d[:2]) < 0.2: d = np.array([0, -1.0 if ctr[1] < 0 else 1.0, 0])
    d = d / np.linalg.norm(d); d[2] = 0.55; d /= np.linalg.norm(d)
    return ctr, size, d

def render(part, ctr, dist, d, solo, tag):
    loc = (ctr + d * dist).tolist()
    sp = {"base": [] if solo else [f"{W}/prep/car4.blend"],
          "parts": [{"blend": f"{W}/prep/{part}.blend", **({} if solo else {"color": "red"})}],
          "camera": {"sensor": 20.25, "keys": [{"t": 0, "loc": loc, "target": ctr.tolist(), "focal": 35}]},
          "seconds": 0, "fps": 15, "res": "1080x1920", "res_pct": 25, "samples": 6, "base_color": "grey",
          "out": f"{R}/{part}_{tag}.png"}
    if solo: sp["base"] = [f"{W}/prep/{part}.blend"]; sp["parts"] = []
    p = f"{R}/{part}_{tag}.json"; json.dump(sp, open(p, "w"))
    subprocess.run(["blender", "-b", "-P", TOOL, "--", p], capture_output=True)
    im = Image.open(f"{R}/{part}_{tag}.png"); w, h = im.size
    return im.crop((0, h // 4, w, 3 * h // 4))

for part in sys.argv[1:]:
    ctr, size, d = view(part)
    ims = [render(part, ctr, max(2.0, size * 2.2), d, False, "ov"), render(part, ctr, max(0.6, size * 1.1), d, False, "ovc"),
           render(part, ctr, max(0.6, size * 1.1), d, True, "solo")]
    w, h = ims[0].size; s = Image.new("RGB", (w * 3, h))
    for i, im in enumerate(ims): s.paste(im, (i * w, 0))
    s.save(f"{R}/{part}_sheet.jpg"); print(f"{R}/{part}_sheet.jpg")
