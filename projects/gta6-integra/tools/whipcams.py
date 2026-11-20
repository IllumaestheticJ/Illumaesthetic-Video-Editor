"""Cameras for the game's 8-frame whip between two views: an orbit about the car, linear in time.

    python projects/gta6-integra/tools/whipcams.py M A 8   -> projects/gta6-integra/whip_M_A/cam_00.json ...

The capture's whip (0.27 s, constant speed by its frame differences) swings round the car's left side.
Position is interpolated in cylindrical coordinates about the car, direction as pitch plus yaw relative to
"looking at the car". It is not solved per frame: eight motion-blurred frames do not need it.
"""
import json, sys
from pathlib import Path
import numpy as np

P = Path(__file__).resolve().parents[1]


def decompose(c):
    loc = np.array(c["blender"]["location"]); M = np.array(c["blender"]["rotation_matrix"])
    fwd = -M[:, 2]
    az = np.arctan2(loc[1], loc[0]); r = np.hypot(loc[0], loc[1])
    yaw = np.arctan2(fwd[1], fwd[0]) - np.arctan2(-loc[1], -loc[0])
    yaw = (yaw + np.pi) % (2 * np.pi) - np.pi
    pitch = np.arcsin(fwd[2])
    return az, r, loc[2], yaw, pitch


def compose(az, r, z, yaw, pitch, like):
    loc = np.array([r * np.cos(az), r * np.sin(az), z])
    h = np.arctan2(-loc[1], -loc[0]) + yaw
    fwd = np.array([np.cos(h) * np.cos(pitch), np.sin(h) * np.cos(pitch), np.sin(pitch)])
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    c = json.loads(json.dumps(like))
    c["blender"] = {"location": loc.round(5).tolist(), "rotation_matrix": np.stack([right, up, -fwd], 1).round(8).tolist()}
    c.pop("notes", None)
    return c


def main():
    a, b, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    ca, cb = json.load(open(P / f"cam_{a}.json")), json.load(open(P / f"cam_{b}.json"))
    pa, pb = np.array(decompose(ca)), np.array(decompose(cb))
    d_az = (pb[0] - pa[0] + np.pi) % (2 * np.pi) - np.pi          # short way round
    out = P / f"whip_{a}_{b}"; out.mkdir(exist_ok=True)
    for i in range(n):
        t = (i + 1) / (n + 1)
        p = pa + (pb - pa) * t; p[0] = pa[0] + d_az * t
        p[1] = p[1] - 0.6 * np.sin(np.pi * t)                     # the capture's camera passes closer to the car's side mid-way
        json.dump(compose(*p, ca), open(out / f"cam_{i:02d}.json", "w"), indent=1)
    print(out, "az", np.degrees(pa[0]).round(1), "->", np.degrees(pa[0] + d_az).round(1))


if __name__ == "__main__":
    main()
