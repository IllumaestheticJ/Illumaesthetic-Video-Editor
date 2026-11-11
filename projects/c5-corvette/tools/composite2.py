"""Artifact-free exploded base for the C5 (v3; reviewer 2026-11-11: "a lot of artifacts ... delete/hide the artifacts").
composite.py added every state-scan triangle > 7 mm from the trimmed car; with 2-4 mm registration noise the state
scans' own copies of the hood / cowl / glass / fenders leaked through as jagged shards on top of the car. Here:
  1. car tris within TRIM mm of a part = that panel -> removed (as composite.py)
  2. state tris must be > ADD mm (default 15) from the trimmed car AND every part (duplicate skins out)
  3. the kept state tris are welded (0.05 mm grid) and split into connected components; components smaller than
     MIN_ISLAND tris are dropped (shards / fringes), so only the exposed structure (large connected sheets) is added
  4. optional --near: a kept component must have >= 50 % of its tris within NEAR mm of the removed parts' footprint
     (structure revealed by a removal sits behind that part, not on the roof)
  composite2.py car.stl out.stl --parts p1.stl ... --states s1.stl ... [--add 15 --min-island 4000 --near 250]
"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)


def components(t):
    """connected components of an STL triangle soup (vertices welded on a 0.05 mm grid)"""
    v = np.round(t["v"].reshape(-1, 3) * 20).astype(np.int64)
    _, vid = np.unique(v, axis=0, return_inverse=True)
    vid = vid.reshape(-1, 3); n = len(t); nv = vid.max() + 1
    # bipartite tri-vertex graph -> components
    rows = np.repeat(np.arange(n), 3); cols = vid.ravel() + n
    g = coo_matrix((np.ones(len(rows), np.int8), (rows, cols)), shape=(n + nv, n + nv))
    _, lab = connected_components(g, directed=False)
    return lab[:n]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
    ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--states", nargs="*", default=[])
    ap.add_argument("--trim", type=float, default=7.0); ap.add_argument("--add", type=float, default=15.0)
    ap.add_argument("--min-island", type=int, default=4000)
    ap.add_argument("--near", type=float, default=0, help="mm; 0 = off")
    ap.add_argument("--state-zmin", type=float, default=70.0)
    ap.add_argument("--report", action="store_true", help="print the component sizes that were dropped/kept")
    a = ap.parse_args()
    car = L(a.car); cc = car["v"].mean(1)
    P = np.concatenate([L(p)["v"].mean(1) for p in a.parts]); ptree = cKDTree(P)
    d, _ = ptree.query(cc, distance_upper_bound=a.trim + 1)
    kc = car[d > a.trim]
    print(f"car {len(car)} -> trimmed {len(kc)}", flush=True)
    cell = 40.0
    key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
    u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
    ref = cKDTree(kc["v"].mean(1))
    pieces = [kc]; added = None
    for sp in a.states:
        s = L(sp); sc = s["v"].mean(1)
        d1, _ = ref.query(sc, distance_upper_bound=a.add + 1)
        d2, _ = ptree.query(sc, distance_upper_bound=a.add + 1)
        keep = (d1 > a.add) & (d2 > a.add) & (sc[:, 2] > a.state_zmin)
        ka = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
        keep &= ~((sc[:, 2] > roof + 40) & (sc[:, 1] < 0))
        if added is not None:
            d3, _ = added.query(sc, distance_upper_bound=a.add + 1); keep &= d3 > a.add
        k = s[keep]
        if len(k):
            lab = components(k); cnt = np.bincount(lab)
            big = cnt[lab] >= a.min_island
            if a.near > 0:
                dn, _ = ptree.query(k["v"].mean(1), distance_upper_bound=a.near + 1)
                frac = np.bincount(lab, weights=(dn <= a.near).astype(float)) / cnt
                big &= frac[lab] >= 0.5
            if a.report:
                sz = np.sort(cnt)[::-1]
                print(f"   components {len(cnt)}; largest {sz[:8].tolist()}; dropped tris {int((~big).sum())}")
            k = k[big]
        print(f"{sp.split('/')[-1]}: +{len(k)} of {len(s)} (raw >ADD {int(keep.sum())})", flush=True)
        pieces.append(k)
        allv = np.concatenate([p["v"].mean(1) for p in pieces[1:] if len(p)]) if any(len(p) for p in pieces[1:]) else []
        added = cKDTree(allv) if len(allv) else None
    res = np.concatenate(pieces)
    with open(a.out, "wb") as f:
        f.write(b"ive c5 composite2".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
    print(a.out, len(res))


if __name__ == "__main__":
    main()
