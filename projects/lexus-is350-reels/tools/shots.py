"""Vertical (9:16) scan shots for the IS350 reels -> JSON specs for projects/smart-450-hellkitten/tools/shot.py.

    python projects/lexus-is350-reels/tools/shots.py preview|check|final [shot ...]

Pairs reuse the long-form's solved 16:9 cameras, cropped to a 608x1080 window at x0 (1920 coords) with
projects/lexus-is350-scan-process/tools/portrait.py (sensor narrowed to the window, offset -> lens shift_x): frame 1 of each
render is exactly that window of the solved view. Same prepped car as the long-form (4 mm, plates flattened, nose -Y, left +X).
15 fps renders (+0.3 s handle), 810x1440 (75 %), 8 spp + denoise, encoded to 1080x1920 with a 30 fps minterpolated preview.
"""
import json
import math
import os
import sys

CAR = "/home/user/media/lexus-is350/prep/car.blend"
W = "/home/user/media/work/is350-reels"
SPECS = f"{W}/scan3d/specs"
MATCH = f"{W}/scan3d/match"
LIGHT = [[-0.975, -2.362, 0.0], [0.975, 2.362, 1.426]]
FPS = 15
HANDLE = 0.3

PAIRS = {  # id: (crop camera, push distance along the view axis in m, fraction pushed)
    "V_MATCH_FRONT": (f"{MATCH}/cam_V_MATCH_FRONT.json", 4.2, 0.08),
    "V_PAIR_3": (f"{MATCH}/cam_V_PAIR_3.json", 2.4, 0.08),
    "V_MATCH_REAR": (f"{MATCH}/cam_V_MATCH_REAR.json", 2.3, 0.10),
    "V_PAIR_2": (f"{MATCH}/cam_V_PAIR_2.json", 2.4, 0.08),
}


def push(cam, dist, amount, secs):
    c = json.load(open(cam))
    R = c["blender"]["rotation_matrix"]; loc = c["blender"]["location"]
    fwd = [-R[i][2] for i in range(3)]
    tgt = [loc[i] + fwd[i] * dist for i in range(3)]
    return c, [{"t": 0, "cam": cam, "dist": dist},
               {"t": secs, "loc": [loc[i] + fwd[i] * dist * amount for i in range(3)], "target": tgt,
                "focal": c["focal_mm"], "ease": "inout"}]


def orbit(t, r, az, h, c, focal, tz, ease="inout"):
    """az 0 = in front of the nose (-Y); 90 = car's LEFT (+X)."""
    a = math.radians(az)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h], "target": [c[0], c[1], tz],
            "focal": focal, "ease": ease}


def shots():
    S = {}
    for n, (cam, dist, amt) in PAIRS.items():
        secs = 2.5 + HANDLE
        c, keys = push(cam, dist, amt, secs)
        S[n] = {"base": [CAR], "light_bbox": LIGHT, "seconds": secs,
                "camera": {"sensor": c["sensor_width_mm"], "shift_x": c["shift_x"], "shift_y": c.get("shift_y", 0.0), "keys": keys}}
    # full-car hero: left-front 3/4 (clean front-left wheel; rear-left well kept small/far), car in the middle ~53 % of the height
    secs = 4.0 + HANDLE
    cc = (0.0, -0.25, 0.62)
    S["V_RES_FULL"] = {"base": [CAR], "light_bbox": LIGHT, "seconds": secs,
                       "camera": {"sensor": 36, "keys": [orbit(0, 8.6, 28, 1.55, cc, 45, 0.62),
                                                         orbit(secs, 8.0, 34, 1.45, cc, 45, 0.62, ease="out2")]}}
    return S


def main():
    mode = sys.argv[1]; want = sys.argv[2:]
    os.makedirs(SPECS, exist_ok=True)
    for n, s in shots().items():
        if want and n not in want:
            continue
        s.update({"fps": FPS, "res": "1080x1920"})
        if mode == "preview":
            s.update({"res_pct": 30, "samples": 4, "frames": ["first", "mid", "last"], "out": f"{W}/scan3d/look/pv_{n}/"})
        elif mode == "check":
            s.update({"res_pct": 100, "samples": 8, "frames": ["first"], "out": f"{W}/scan3d/look/ck_{n}/"})
        else:
            s.update({"res_pct": 75, "samples": 8, "out": f"{W}/renders/{n}/png/"})
        p = f"{SPECS}/{n}_{mode}.json"; json.dump(s, open(p, "w"), indent=1); print(p)


if __name__ == "__main__":
    main()
