"""GD trio shot specs: five camera moves, each rendered on bugeye / blobeye / hawkeye (direction.md sections 3-4).

    python projects/subaru-gd-trio/tools/shots_trio.py preview|final [segment ...]     # segments: F1_bug, F1_blob, ...

All three scans share one frame, so the same camera gives a pixel-aligned hard cut between cars. Each move is one linear
segment; a car's spec covers its own beats plus 3 source frames of tail (camera keeps moving at the same rate).
The light rig is pinned to the blobeye bbox (light_bbox) so brightness does not step at the cuts.
"""
import json
import os
import sys

W = "/home/user/media/work/gd3"
CARS = {"bug": f"{W}/prep/bug4.blend", "blob": f"{W}/prep/blob4.blend", "hawk": f"{W}/prep/hawk4.blend"}
LIGHT_BBOX = [[-0.9729, -2.2018, 0.0], [0.9729, 2.2018, 1.3880]]   # blobeye (car4.json)
CUTS = [0, 51, 103, 154, 180, 206, 257, 283, 309, 334, 360, 386, 411, 437, 463, 514]   # output frames at 30 fps
# move: (start key, end key, beats per car); key = (loc, target, focal)
MOVES = {
    "F1": (((3.35, -5.55, 1.05), (-0.17, -0.25, 0.52), 32), ((1.80, -5.60, 1.20), (-0.12, -0.45, 0.52), 35), (4, 4, 4)),
    "F2": (((1.25, -5.15, 1.75), (0.04, -1.20, 0.66), 36), ((0.30, -4.85, 2.25), (0.00, -1.20, 0.66), 38), (2, 2, 4)),
    "R1": (((3.75, 4.95, 1.15), (-0.12, 0.35, 0.52), 30), ((2.45, 5.60, 1.35), (-0.06, 0.50, 0.52), 32), (2, 2, 2)),
    "R2": (((1.10, 5.35, 1.80), (-0.03, 1.20, 0.72), 37), ((0.30, 5.00, 2.35), (-0.05, 1.20, 0.72), 38), (2, 2, 2)),
    "T1": (((0.00, 1.75, 6.70), (0.00, 0.25, 0.60), 38), ((0.00, 1.67, 6.20), (0.00, 0.25, 0.60), 38), (4 / 2, 4 / 2, 4)),
}
BEAT = 0.42862


def pose(a, b, u):
    mix = lambda x, y: [x[i] + (y[i] - x[i]) * u for i in range(3)]
    return {"loc": mix(a[0], b[0]), "target": mix(a[1], b[1]), "focal": a[2] + (b[2] - a[2]) * u}


SEG = {}   # name -> (blend, seconds, keys, out frames)
k = 0
for m, (a, b, beats) in MOVES.items():
    tot = sum(beats); t = 0.0
    for car, nb in zip(CARS, beats):
        out_frames = CUTS[k + 1] - CUTS[k]
        T = out_frames / 30 + 3 / 15                      # 3 source frames of tail
        u0 = t / tot; u1 = u0 + (T / BEAT) / tot          # same linear rate through the tail
        SEG[f"{m}_{car}"] = (CARS[car], T, [dict(t=0, ease="lin", **pose(a, b, u0)), dict(t=T, ease="lin", **pose(a, b, u1))], out_frames)
        t += nb; k += 1


def spec(name, mode):
    base, T, keys, _ = SEG[name]
    sp = {"base": [base], "camera": {"keys": keys}, "seconds": T, "fps": 15, "res": "1080x1920", "out": f"{W}/renders/{mode}/{name}",
          "exposure": -0.5, "persistent": True, "parts": [], "light_bbox": LIGHT_BBOX}
    sp.update(dict(res_pct=30, samples=8, frames=["first", "mid", "last"]) if mode == "preview" else dict(res_pct=75, samples=12))
    return sp


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(f"{W}/specs", exist_ok=True)
    for n in sys.argv[2:] or list(SEG):
        json.dump(spec(n, mode), open(f"{W}/specs/{mode}_{n}.json", "w"), indent=1)
        print(n, round(SEG[n][1], 3), SEG[n][3])
