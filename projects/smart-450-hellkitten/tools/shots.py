"""Shot specs for the Smart 450 short (scan shots A1-A3) -> JSON for tools/shot.py.

    python projects/smart-450-hellkitten/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped frame (metres, every state prepped --like asm.json, all four Artec states share one frame):
front = +Y, car's right (fuel-cap side) = +X, ground Z = 0, length 2.53 m, height 1.53 m.
Renders 15 fps (+3 tail frames for minterpolate) at 1080x1920; previews 30 % / 4 spp first-mid-last.
"""
import json
import math
import os
import sys

P = "/home/user/media/smart-hellkitten/prep"
W = "/home/user/media/work/smart-450"
SPECS = f"{W}/scan3d/specs"
MATCH = f"{W}/scan3d/match"
ASM, STR, STR2 = f"{P}/asm.blend", f"{P}/str.blend", f"{P}/str2.blend"
LIGHT = [[-0.78, -1.27, 0.0], [0.78, 1.27, 1.54]]   # asm bbox: one rig for every state (same-camera swaps)
FPS = 15
TAIL = 3 / FPS


def cam_from_json(path):
    c = json.load(open(path))
    import numpy as np
    R = np.array(c["blender"]["rotation_matrix"]); loc = np.array(c["blender"]["location"])
    fwd = -R[:, 2]
    return c, loc, fwd


def orbit(t, r, az, h, c=(0, 0, 0.6), focal=30, tz=None, ease="inout"):
    """az 0 = camera in front of the car (+Y); 90 = car's right (+X); 180 = behind."""
    a = math.radians(az)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] + r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def a1():
    """1:1 from v_1852_56 @ 26.0 s (stripped shell, 9:16 window x0=760). Slow drift forward along the car."""
    c, loc, fwd = cam_from_json(f"{MATCH}/camP_str.json")
    tgt = loc + fwd * 1.6
    secs = 2.4
    k0 = {"t": 0, "cam": f"{MATCH}/camP_str.json", "dist": 1.6}
    d = [0.0, 0.16, 0.0]          # 16 cm along the car toward the nose, camera and target together
    k1 = {"t": secs + TAIL, "loc": [loc[0] - 0.05, loc[1] + d[1], loc[2] - 0.02],
          "target": [tgt[0] + 0.02, tgt[1] + d[1] + 0.06, tgt[2]],
          "focal": c["focal_mm"], "ease": "out2"}
    # roll from the solved camera is carried by key 0; hold it on key 1 (filled in by shot.py from k0)
    return {"base": [STR], "light_bbox": LIGHT, "camera": {"sensor": c["sensor_width_mm"], "keys": [k0, k1]},
            "seconds": secs + TAIL}


def a2():
    """Body on -> body off: Assembled held, hard state swap to Fully Stripped at SWAP s, then push in on the
    door-aperture structure (diagonal braces, sill, B-pillar) with the front structure in view."""
    secs, SWAP = 4.8, 1.6
    c = (0.05, 0.05, 0.65)
    keys = [orbit(0, 3.9, 50, 1.85, c=c, focal=45, tz=0.62),
            orbit(SWAP, 3.8, 52, 1.83, c=c, focal=45, tz=0.62, ease="lin"),
            orbit(secs + TAIL, 2.5, 62, 1.5, c=(0.4, 0.2, 0.75), focal=45, tz=0.75, ease="inout")]
    return {"base": [{"blend": ASM, "vis": [0, SWAP]}, {"blend": STR, "vis": [SWAP, 99]}], "light_bbox": LIGHT,
            "camera": {"sensor": 36, "keys": keys}, "seconds": secs + TAIL, "swap_at": SWAP}


def a3():
    """Close detail on the stripped front structure (clamshell, headlamps and bumper off): slow lateral slide, 2 mm mesh."""
    secs = 2.4
    keys = [{"t": 0, "loc": [0.95, 2.35, 0.95], "target": [0.15, 1.05, 0.62], "focal": 32},
            {"t": secs + TAIL, "loc": [0.55, 2.25, 0.92], "target": [0.05, 1.05, 0.62], "focal": 34, "ease": "inout"}]
    return {"base": [STR2], "light_bbox": LIGHT, "camera": {"sensor": 36, "keys": keys}, "seconds": secs + TAIL}


SHOTS = {"a1_match_str": a1, "a2_body_on_off": a2, "a3_detail": a3}


def main():
    mode = sys.argv[1]
    names = sys.argv[2:] or list(SHOTS)
    os.makedirs(SPECS, exist_ok=True)
    for n in names:
        s = SHOTS[n]()
        s.update({"fps": FPS, "res": "1080x1920"})
        if mode == "preview":
            s.update({"res_pct": 30, "samples": 4, "frames": ["first", "mid", "last"], "out": f"{W}/scan3d/look/pv_{n}/"})
            if "swap_at" in s:
                f = int(round(s["swap_at"] * FPS)) + 1
                s["frames"] = ["first", f - 1, f, "mid", "last"]
        else:
            s.update({"res_pct": 75, "samples": 8, "out": f"{W}/renders/{n}/png/"})
        p = f"{SPECS}/{n}_{mode}.json"
        json.dump(s, open(p, "w"), indent=1)
        print(p)


if __name__ == "__main__":
    main()
