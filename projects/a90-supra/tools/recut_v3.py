"""v3.1 re-cut of the fender section and rear bumper (reviewer: "not cut correctly").

build_v3 also removed car skin the removed-state scan lacked, which reached past the panel's real shut lines (above the
fender's top seam, into the trunk lid edge and around the tail lamps) and left ragged openings. Both panels were scanned
loose with clean, complete outlines, so the panel scan itself is the cut: a car triangle leaves the body only if it lies
on the panel scan (<= ON mm), with a 12 mm majority vote to close pin-holes and speckle. Nothing else is removed.
    python projects/a90-supra/tools/recut_v3.py fender rbump     (rewrites v3/body.stl, skin_<z>.stl, fill_<z>.stl, part_<z>.stl)"""
import os, struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from build_v3 import TRI, OUT, ZONES, FLOOR_Z, islands
ON = 5.0
STRICT = {"fender"}

def save(m, p):
    with open(p, "wb") as f:
        f.write(b"ive recut_v3".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)

if not os.path.exists(OUT + "body_v30.stl"):
    save(np.fromfile(OUT + "body.stl", dtype=TRI, offset=84), OUT + "body_v30.stl")
body = np.fromfile(OUT + "body_v30.stl", dtype=TRI, offset=84)      # always start from the v3.0 body (re-runnable)
for z in sys.argv[1:]:
    part = np.concatenate([np.fromfile(p, dtype=TRI, offset=84) for p in ZONES[z][0]])
    lab = islands(part); part = part[np.bincount(lab)[lab] >= 2000]
    if not os.path.exists(OUT + f"skin_{z}_v30.stl"):
        save(np.fromfile(OUT + f"skin_{z}.stl", dtype=TRI, offset=84), OUT + f"skin_{z}_v30.stl")
    old_skin = np.fromfile(OUT + f"skin_{z}_v30.stl", dtype=TRI, offset=84)
    allm = np.concatenate([body, old_skin]); c = allm["v"].mean(1).astype(np.float32)
    pt = cKDTree(part["v"].mean(1).astype(np.float32))
    dp = pt.query(c, distance_upper_bound=40.0, workers=2)[0]
    cand = np.flatnonzero(np.isfinite(dp)); on = dp[cand] <= ON
    state = np.concatenate([np.fromfile(p, dtype=TRI, offset=84) for p in ZONES[z][1]]); sc = state["v"].mean(1).astype(np.float32)
    if z == "rbump":
        # the loose bumper scan spreads at its flanks (5-15 mm off the car skin): on side-facing skin within 16 mm of the
        # panel, the bumper-off scan decides - bumper flank skin is absent there, the quarter panel beyond the seam is present
        e1 = allm["v"][cand, 1] - allm["v"][cand, 0]; e2 = allm["v"][cand, 2] - allm["v"][cand, 0]
        n = np.cross(e1, e2); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
        fl = np.flatnonzero((np.abs(n[:, 1]) > 0.6) & (dp[cand] <= 24.0) & ~on)
        lo, hi = c[cand][fl].min(0) - 90, c[cand][fl].max(0) + 90
        sub = sc[np.all((sc > lo) & (sc < hi), axis=1)]
        ds = cKDTree(sub).query(c[cand][fl], distance_upper_bound=80.0, workers=2)[0]
        add = fl[(ds > 5.0) & np.isfinite(ds)]; on[add] = True
        print(z, "flank skin the bumper-off scan lacks:", len(add), "of", len(fl), flush=True)
    t = cKDTree(c[cand]); n_all = t.query_ball_point(c[cand], 12.0, workers=2, return_length=True)
    n_on = cKDTree(c[cand][on]).query_ball_point(c[cand], 12.0, workers=2, return_length=True)
    frac = n_on / np.maximum(n_all, 1)
    rem = np.where(frac > 0.6, True, np.where(frac < 0.4, False, on))
    off = np.zeros(len(allm), bool); off[cand[rem]] = True
    kept = allm[~off]
    # body scraps the panel leaves hanging in its own zone (lip fragments) go with the fitted skin, not the stripped car
    lab = islands(kept); size = np.bincount(lab); kc = kept["v"].mean(1).astype(np.float32)
    dk = pt.query(kc, distance_upper_bound=120.0, workers=2)[0]
    far = np.bincount(lab, weights=~(dk <= 45.0), minlength=len(size))        # tris of each island NOT under the panel
    enclosed = (far[lab] == 0) & (size[lab] < 60000)                          # e.g. the number plate: wholly under the panel
    scrap = ((size[lab] < 4000) & np.isfinite(dk)) | enclosed
    if z in STRICT:   # v3.2 (user: "the fender removed scan took too much of the chassis off with it"): only the panel's own skin
        scrap = (size[lab] < 300) & (dk <= 20.0)             # leaves; chassis pieces near / behind it stay; only specks on the panel go
    print(z, "islands wholly under the panel:", int(enclosed.sum()), "tris", flush=True)
    skin = np.concatenate([allm[off], kept[scrap]]); body = kept[~scrap]
    save(skin, OUT + f"skin_{z}.stl"); save(part, OUT + f"part_{z}.stl")
    print(z, "on-panel", int(on.sum()), "removed", int(off.sum()), "scrap islands tris", int(scrap.sum()), "skin", len(skin), "(was", len(old_skin), ")", flush=True)
    near = np.isfinite(cKDTree(skin["v"].mean(1).astype(np.float32)).query(sc, distance_upper_bound=60.0, workers=2)[0])
    bt = cKDTree(body["v"].mean(1).astype(np.float32))
    fill = state[near & ~np.isfinite(bt.query(sc, distance_upper_bound=3.0, workers=2)[0]) & (sc[:, 2] > FLOOR_Z)]
    lab = islands(fill); size = np.bincount(lab)
    att = np.bincount(lab, weights=np.isfinite(bt.query(fill["v"].mean(1).astype(np.float32), distance_upper_bound=25.0, workers=2)[0]), minlength=len(size)) > 0
    fill = fill[(size[lab] >= 400) & att[lab]]
    save(fill, OUT + f"fill_{z}.stl"); print(z, "fill", len(fill), flush=True)
    del bt, state, sc
save(body, OUT + "body.stl"); print("body", len(body))
