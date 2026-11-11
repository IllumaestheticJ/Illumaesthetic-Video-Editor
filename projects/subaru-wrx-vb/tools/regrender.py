"""Visual registration check: each part/state scan in red over the grey full car, camera aimed at the part from
outside the car (direction = part centre - car centre, lifted), distance from the part's size. Writes specs for
projects/ferrari-296/tools/shot.py and prints them.
    python projects/subaru-wrx-vb/tools/regrender.py name1 name2 ...   (names of prep/p_<name>.blend)"""
import json, sys
import numpy as np
P = "/home/user/media/subaru-wrx-vb/prep"
OUT = "/home/user/media/work/wrx/chk/reg"
for n in sys.argv[1:]:
    j = json.load(open(f"{P}/p_{n}.json"))
    lo, hi = np.array(j["bbox_min"]), np.array(j["bbox_max"])
    c = (lo + hi) / 2
    d = np.array([c[0], c[1], 0.0])
    d = d / (np.linalg.norm(d) + 1e-9) if np.linalg.norm(d) > 0.2 else np.array([-1.0, 0, 0])
    size = max(np.linalg.norm(hi - lo), 0.8)
    dist = 1.4 * size + 1.2
    loc = c + d * dist + np.array([0, 0, 0.45 * dist])
    sp = {"base": [f"{P}/car4.blend"], "base_color": "grey",
          "parts": [{"blend": f"{P}/p_{n}.blend", "color": "red"}],
          "camera": {"sensor": 20.25, "keys": [{"t": 0, "loc": loc.tolist(), "target": c.tolist(), "focal": 24}]},
          "seconds": 0, "fps": 15, "res": "1080x1920", "res_pct": 30, "samples": 8, "out": f"{OUT}/{n}.png"}
    p = f"/home/user/media/work/wrx/specs/reg_{n}.json"
    json.dump(sp, open(p, "w"))
    print(p)
