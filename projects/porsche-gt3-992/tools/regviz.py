"""Visual registration check: each part scan in red over the grey full car, camera looking at the part from
outside (direction = part centroid from the car centre). Writes specs + renders one 30 % still per part.
    python regviz.py car.json partsc_dir prep_dir out_dir [name ...]"""
import json, os, subprocess, sys, glob
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
cj, pdir, prep, out = sys.argv[1:5]
names = sys.argv[5:]
J = json.load(open(cj)); s = J["unit_scale"]; r = np.array(J["root_location"])
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(f"{pdir}/*.stl")):
    n = os.path.basename(f)[:-4]
    if names and n not in names: continue
    c = np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1) * s + r
    lo, hi = np.percentile(c, 2, 0), np.percentile(c, 98, 0)
    ctr = (lo + hi) / 2; size = np.linalg.norm(hi - lo)
    d = ctr - np.array([0, 0, 0.6]); d[2] = max(d[2], 0) + 0.5; d /= np.linalg.norm(d)
    cam = ctr + d * max(2.2, size * 2.2)
    sp = {"base": [f"{prep}/car4.blend"], "base_color": "grey",
          "parts": [{"blend": f"{prep}/p_{n}.blend", "color": "red"}],
          "camera": {"keys": [{"t": 0, "loc": cam.tolist(), "target": ctr.tolist(), "focal": 30}]},
          "seconds": 0, "res": "1080x1920", "res_pct": 30, "samples": 6, "out": f"{out}/{n}.png"}
    p = f"{out}/{n}.json"; json.dump(sp, open(p, "w"))
    subprocess.run(["blender", "-b", "-P", f"{here}/shot.py", "--", p], capture_output=True)
    print(n, ctr.round(2), os.path.exists(f"{out}/{n}.png"))
