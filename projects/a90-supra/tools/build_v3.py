"""v3 bases: the removed-STATE scan decides every seam (lessons: GR86 v4, Frontier v3, Cappuccino v3, Miata NA).

v2 carved the car "within 9 mm of the part scan" and spliced every state into one base -> leftovers where the part
scan missed skin, double skins where states overlapped. Here, per zone (a removable part + the scan of the car with
that part removed):
  removed = car tris within NEAR mm of the part scan that the state scan does NOT have (> LACK mm), where the state
            has coverage at all (< COVER mm). Speckle is voted away over 15 mm neighbourhoods.
  extra   = removed tris the part scan itself does not cover (> 6 mm): they travel WITH the part, so nothing is left
            behind and nothing vanishes.
  fill    = state tris near the removed skin, > FILL mm from the kept body and from every other zone's fill, above
            the floor, small/unattached islands dropped. One fill per zone, only in its own opening.
body = car minus every zone's removed tris. Everything stays in the car's raw frame (mm).

    python projects/a90-supra/tools/build_v3.py [zone ...]      -> /home/user/media/work/a90/v3/{body,fill_*,extra_*,part_*}.stl
"""
import json
import struct
import sys

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

W = "/home/user/media/work/a90/"
OUT = W + "v3/"
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
NEAR, LACK, COVER, FILL, FLOOR_Z = 60.0, 10.0, 80.0, 7.0, -25.0
ISL_ZONE, ISL_ANY = 4000, 300   # body islands smaller than this are scraps (inside a zone / anywhere)

R1, R2 = "/home/user/media/a90-supra/scans/", "/home/user/media/a90-supra/scans2/chassis/"
CAR = R1 + "Chassis Trimmed (8.4m).stl"     # full-resolution sources: grid-decimated meshes show stair-step contours in close-ups
DUCT = "/home/user/media/a90-supra/scans3/Supra Front Bumper Duct Removed.stl"
ZONES = {  # name: (part scans, state scan(s))
    "fbump": ([R1 + "Supra Front Bumper Outside.stl", R1 + "Supra Front Bumper Inside.stl"], [R1 + "Supra Under Front Bumper.stl"]),
    "fender": ([R1 + "Supra Fender.stl"], [R1 + "Supra Under Fender.stl"]),
    "dtrim": ([R2 + "Supra Door Trim (1.4M).stl"], [R2 + "Supra Under Door Trim (1.8M).stl"]),
    "skirts": ([R2 + "Supra Upper Skirt (5.3M).stl", R2 + "Supra Lower Skirt (2M).stl"], [R2 + "Supra Chassis Under Upper Skirt (5.7M).stl"]),
    "rbump": ([R1 + "Supra Rear Bumper Outside.stl", R1 + "Supra Rear Bumper Inside.stl"], [R2 + "Supra Under Rear Bumper (27M).stl"]),
}


def load(p):
    return np.fromfile(W + p if not p.startswith("/") else p, dtype=TRI, offset=84)


def save(m, p):
    with open(p, "wb") as f:
        f.write(b"ive build_v3".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)


def dist(src, ref_pts, ub):
    d, _ = cKDTree(ref_pts).query(src, distance_upper_bound=ub, workers=4)
    return d  # inf beyond ub


def islands(m, tol=0.05):
    """Connected components by shared (welded) vertices -> label per triangle."""
    v = np.round(m["v"].reshape(-1, 3) / tol).astype(np.int64)
    _, inv = np.unique(v, axis=0, return_inverse=True)
    f = inv.reshape(-1, 3)
    n = inv.max() + 1
    g = coo_matrix((np.ones(len(f) * 2, bool), (np.r_[f[:, 0], f[:, 1]], np.r_[f[:, 1], f[:, 2]])), shape=(n, n))
    _, lab = connected_components(g, directed=False)
    return lab[f[:, 0]]


def vote(c, flag, r=15.0):
    """Majority vote of a boolean flag over neighbours within r (removes speckle both ways)."""
    t = cKDTree(c)
    pairs = t.query_pairs(r, output_type="ndarray")
    cnt = np.bincount(np.r_[pairs[:, 0], pairs[:, 1]], minlength=len(c)).astype(float)
    yes = np.bincount(np.r_[pairs[:, 0], pairs[:, 1]], weights=np.r_[flag[pairs[:, 1]], flag[pairs[:, 0]]].astype(float), minlength=len(c))
    frac = np.where(cnt > 0, yes / np.maximum(cnt, 1), flag)
    return np.where(frac > 0.65, True, np.where(frac < 0.35, False, flag))


def main():
    want = sys.argv[1:] or list(ZONES)
    car = load(CAR)
    cc = car["v"].mean(1)
    rem_all = np.zeros(len(car), bool)
    rep, zinfo = {}, {}
    for z in want:
        parts, states = ZONES[z]
        part = np.concatenate([load(p) for p in parts])
        pl = islands(part); ps = np.bincount(pl); pk = ps[pl] >= max(300, 0.002 * len(part))
        print(z, "part scan islands dropped:", int((~pk).sum()), "tris in", int((ps < max(300, 0.002 * len(part))).sum()), "islands"); part = part[pk]
        state = np.concatenate([load(s) for s in states])
        pp, sp = part["v"].reshape(-1, 3), state["v"].mean(1)
        cand = np.flatnonzero(np.isfinite(dist(cc, pp, NEAR)))
        ds = dist(cc[cand], sp, COVER)
        lack = ds > LACK
        unknown = ~np.isfinite(ds)          # state never scanned here: keep the car skin
        on_part = np.isfinite(dist(cc[cand], pp, 4.0))   # the car's copy of the part's own skin always goes with the part;
        rem = vote(cc[cand], (lack & ~unknown) | on_part)  # real structure that close is restored by the state fill
        rem = (rem & ~unknown) | on_part
        idx = cand[rem]
        rem_all[idx] = True
        dpart = dist(cc[idx], pp, 6.0)
        zinfo[z] = dict(part=part, state=state, idx=idx, extra=idx[~np.isfinite(dpart)])
        rep[z] = dict(candidates=int(len(cand)), removed=int(len(idx)), no_state_coverage=int(unknown.sum()),
                      extra_moves_with_part=int((~np.isfinite(dpart)).sum()))
        print(z, rep[z], flush=True)
    body = car[~rem_all]
    lab = islands(body)
    size = np.bincount(lab)
    bcc = body["v"].mean(1)
    inzone = np.zeros(len(body), bool)
    for z in want:
        inzone |= np.isfinite(dist(bcc, zinfo[z]["part"]["v"].reshape(-1, 3)[::2], 120.0))
    scrap = (size[lab] < ISL_ANY) | (inzone & (size[lab] < ISL_ZONE))
    rep["body"] = dict(tris=int(len(body)), scrap_dropped=int(scrap.sum()), scrap_islands=int(len(np.unique(lab[scrap]))))
    print("body", rep["body"], flush=True)
    save(body[scrap], OUT + "scrap.stl")
    body = body[~scrap]
    save(body, OUT + "body.stl")
    bc = body["v"].mean(1)
    used = [bc[::3]]
    for z in want:
        zi = zinfo[z]
        state = zi["state"]
        sc = state["v"].mean(1)
        near_open = np.isfinite(dist(sc, np.r_[cc[zi["idx"]], zi["part"]["v"].mean(1)], 60.0))
        far_body = ~np.isfinite(dist(sc, np.concatenate(used), FILL))
        sel = near_open & far_body & (sc[:, 2] > FLOOR_Z)
        fill = state[sel]
        if z == "fbump":   # second front state (user upload 2026-11-12): bumper AND brake ducts removed -> 1:1 swap fill
            s2 = load(DUCT); c2 = s2["v"].mean(1)
            k2 = np.isfinite(dist(c2, np.r_[cc[zi["idx"]], zi["part"]["v"].mean(1)], 60.0)) & ~np.isfinite(dist(c2, np.concatenate(used), FILL)) & (c2[:, 2] > FLOOR_Z)
            f2 = s2[k2]; l2 = islands(f2); z2 = np.bincount(l2)
            a2 = np.bincount(l2, weights=np.isfinite(dist(f2["v"].mean(1), bc, 25.0)), minlength=len(z2)) > 0
            f2 = f2[(z2[l2] >= 400) & a2[l2]]; save(f2, OUT + "fill_fduct.stl"); rep[z]["fill_duct_removed"] = int(len(f2))
        if len(fill):
            lab = islands(fill)
            size = np.bincount(lab)
            fc = fill["v"].mean(1)
            att = np.isfinite(dist(fc, bc, 25.0))          # island touches the kept body somewhere
            att_isl = np.bincount(lab, weights=att, minlength=len(size)) > 0
            keep = (size[lab] >= 400) & att_isl[lab]
            rep[z].update(fill=int(keep.sum()), fill_dropped_islands=int((~keep).sum()))
            fill = fill[keep]
        used.append(fill["v"].mean(1))
        save(fill, OUT + f"fill_{z}.stl")
        save(car[zi["extra"]], OUT + f"extra_{z}.stl")
        save(np.concatenate([zi["part"], car[zi["extra"]]]), OUT + f"part_{z}.stl")
        if z == "skirts":   # upper and lower skirt come off separately: split part + extras by nearest source scan
            up, lo = load(ZONES[z][0][0]), load(ZONES[z][0][1])
            ex = car[zi["extra"]]; ec = ex["v"].mean(1)
            du = dist(ec, up["v"].mean(1), 200.0); dl = dist(ec, lo["v"].mean(1), 200.0)
            save(np.concatenate([up, ex[du <= dl]]), OUT + "part_uskirt.stl"); save(np.concatenate([lo, ex[du > dl]]), OUT + "part_lskirt.stl")
        print(z, "fill", rep[z].get("fill"), "dropped", rep[z].get("fill_dropped_islands"), flush=True)
    json.dump(rep, open(OUT + "build_v3.json", "w"), indent=1)


if __name__ == "__main__":
    main()
