"""Exploded-view base for the Sera: full car with every flying panel removed, plus what the state scans saw under them.

    explode_base.py out.stl

Panels (all in the full car's frame, verified in reg/ overlays):
  hood, door, door2   outer skins from tools/hinge_fit.py masks (<name>_masks.npz)
  front bumper        'front bumper' part scan     -> car tris within CUT mm of it are removed
  rear bumper         'rear bumper only' part scan -> same
  + inside each bumper's bbox, car tris the matching bumper-removed state lacks (licence plates mounted on the bumper)
Fills, in order (state scans as captured; each adds only triangles > NEW mm from everything kept so far, so no double
skins, and never within KEEP_OUT mm of any panel's closed position - e.g. 'Hood open' still has the front bumper on):
  front_bumper_removed, rear_bumper_removed (the byte-identical 'No Tail Lights' copy is the same file), hood_open
  (its open hood dropped), door_open (both open doors dropped).
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/toyota-sera/clean/"
CUT, NEW, KEEP_OUT = 9.0, 8.0, 12.0


def load(n):
    return np.fromfile(C + n, dtype=TRI, offset=84)


def main():
    out = sys.argv[1]
    car = load("car3.stl"); cc = car["v"].mean(1)
    keep = np.ones(len(car), bool)
    for n in ("hood", "door", "door2"):
        keep &= ~np.load(C + n + "_masks.npz")["outer"]
    panel_pts = [load(n + "_panel.stl")["v"].mean(1) for n in ("hood", "door", "door2")]
    for p, st in (("front_bumper_3mm.stl", "front_bumper_removed_3mm.stl"), ("rear_bumper_only_3mm.stl", "rear_bumper_removed_3mm.stl")):
        v = load(p)["v"].mean(1); panel_pts.append(v)
        d, _ = cKDTree(v).query(cc, distance_upper_bound=CUT + 1)
        keep &= d > CUT
        # things mounted on the bumper but not in its part scan (licence plates): inside the bumper's bbox, car tris
        # the bumper-removed state doesn't have go too
        lo, hi = v.min(0) - 30, v.max(0) + 30; hi[2] -= 60  # stay below the bumper's top edge (lamps, body panels)
        inb = np.all((cc >= lo) & (cc <= hi), axis=1)
        ds, _ = cKDTree(load(st)["v"].mean(1)).query(cc[inb], distance_upper_bound=30)
        idx = np.where(inb)[0][ds > 15]; keep[idx] = False
        print(p, "bumper-mounted extras removed", len(idx))
    print("car kept", int(keep.sum()), "of", len(car))
    tpanel = cKDTree(np.concatenate(panel_pts))
    pieces = [car[keep]]; acc = cc[keep]
    drops = {"hood_open_3mm.stl": np.load(C + "hood_masks.npz")["drop"],
             "door_open_3mm.stl": np.load(C + "door_masks.npz")["drop"] | np.load(C + "door2_masks.npz")["drop"]}
    for f in ("front_bumper_removed_3mm.stl", "rear_bumper_removed_3mm.stl", "hood_open_3mm.stl", "door_open_3mm.stl"):
        m = load(f); c = m["v"].mean(1)
        ok = np.ones(len(m), bool) if f not in drops else ~drops[f]
        d, _ = cKDTree(acc).query(c, distance_upper_bound=NEW * 2); ok &= d > NEW
        dp, _ = tpanel.query(c, distance_upper_bound=KEEP_OUT * 2); ok &= dp > KEEP_OUT
        pieces.append(m[ok]); acc = np.concatenate([acc, c[ok]])
        print(f, "adds", int(ok.sum()))
    res = np.concatenate(pieces)
    with open(out, "wb") as fh:
        fh.write(b"toyota-sera explode base".ljust(80)); fh.write(struct.pack("<I", len(res))); res.tofile(fh)
    print(out, len(res))


if __name__ == "__main__":
    main()
