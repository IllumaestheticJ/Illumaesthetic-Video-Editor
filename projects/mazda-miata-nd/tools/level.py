"""Level the Miata ND scan frame. The Artec export is upside down (ground at +Z, car hangs to -Z) with the
long axis on X. Pre-flip 180 deg about X, then reuse the Huracan levelling (RANSAC ground plane -> +Z,
long axis -> Y), and optionally a 180 deg yaw so the nose is at -Y (house frame: front -Y, car's right -X).
One rigid transform (R, origin; mm) for every scan so all states stay registered.
  level.py fit full.stl transform.json [--nose-neg-y-flip]
  level.py apply transform.json in.stl out.stl
"""
import json, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "huracan-evo", "tools"))
import level as H  # projects/huracan-evo/tools/level.py

TRI = H.TRI
FLIP = np.diag([1.0, -1.0, -1.0])  # 180 deg about X


def fit(path, out, yaw180=False):
    tmp = out + ".flipped.stl"
    json.dump({"R": FLIP.tolist(), "origin": [0, 0, 0]}, open(out + ".pre.json", "w"))
    H.apply(out + ".pre.json", path, tmp)
    H.fit(tmp, out)
    T = json.load(open(out))
    R = np.array(T["R"]) @ FLIP
    o = FLIP.T @ np.array(T["origin"])  # origin in raw coords: (raw - o) @ R.T == ((raw@F.T) - o') @ R'.T
    if yaw180:
        R = np.diag([-1, -1, 1.0]) @ R
    T.update({"R": R.tolist(), "origin": o.tolist(), "pre_flip_x180": True, "yaw180": yaw180})
    json.dump(T, open(out, "w"), indent=1)
    os.remove(tmp); os.remove(out + ".pre.json")
    print("wrote", out)


if __name__ == "__main__":
    if sys.argv[1] == "fit":
        fit(sys.argv[2], sys.argv[3], "--nose-neg-y-flip" in sys.argv)
    else:
        H.apply(sys.argv[2], sys.argv[3], sys.argv[4])
