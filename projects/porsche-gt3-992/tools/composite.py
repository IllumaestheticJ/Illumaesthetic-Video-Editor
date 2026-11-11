"""(copied from projects/ferrari-296/tools/composite.py) Build a "panels off" base for exploded / opening shots from Artec state scans (raw mm, shared frame).

    python projects/ferrari-296/tools/composite.py out.stl --car car4_clean.stl \
        --remove hood_combined_2mm.stl --fill front_fully_removed_2_2mm.stl [--zone-pad 40] [--zmax 950]

1. Delete car triangles within --cut mm of any removed panel (the panel's skin on the car).
2. From each fill (state) scan keep only NEW geometry: triangles > --new mm from the original car,
   inside the removed panels' bbox (+ --zone-pad), below --zmax (raw mm; drops e.g. the propped-open
   hood captured in "Front Fully Removed").
The panels themselves are animated separately and land back exactly where they were cut out.
"""
import argparse
import struct

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"ferrari-296 composite".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--car", required=True)
    ap.add_argument("--remove", nargs="+", required=True)
    ap.add_argument("--fill", nargs="*", default=[])
    ap.add_argument("--cut", type=float, default=9.0)
    ap.add_argument("--new", type=float, default=7.0)
    ap.add_argument("--zone-pad", type=float, default=40.0)
    ap.add_argument("--zmax", type=float, default=1e9, help="raw mm; applies to the fill zone")
    ap.add_argument("--fill-zmax", nargs="*", default=[], help="per-fill zmax overrides 'index:mm'")
    a = ap.parse_args()
    car = load(a.car)
    cc = car["v"].mean(1)
    keep = np.ones(len(car), bool)
    zones = []  # one bbox per removed panel: fills only add geometry that was under *some* panel
    for r in a.remove:
        v = load(r)["v"].reshape(-1, 3)
        zlo, zhi = v.min(0) - a.zone_pad, v.max(0) + a.zone_pad
        zhi[2] = min(zhi[2], a.zmax)
        zones.append((zlo, zhi))
        d, _ = cKDTree(v[:: max(1, len(v) // 1_500_000)]).query(cc, distance_upper_bound=a.cut)
        keep &= ~(d < a.cut)
    print("car", len(car), "-> removed", int((~keep).sum()))
    pieces = [car[keep]]
    tcar = cKDTree(cc[:: 2])
    acc = None  # fills are applied in order; later fills only add what earlier ones lack (no double skins)
    for f in a.fill:
        m = load(f)
        c = m["v"].mean(1)
        inz = np.zeros(len(c), bool)
        for zlo, zhi in zones:
            inz |= np.all((c >= zlo) & (c <= zhi), axis=1)
        for spec in a.fill_zmax:
            i, z = spec.split(":")
            if a.fill.index(f) == int(i):
                inz &= c[:, 2] < float(z)
        d, _ = tcar.query(c[inz], distance_upper_bound=a.new * 2)
        ok = d > a.new
        if acc is not None:
            d2, _ = cKDTree(acc).query(c[inz], distance_upper_bound=a.new * 2)
            ok &= d2 > a.new
        sel = np.zeros(len(m), bool)
        sel[np.where(inz)[0][ok]] = True
        acc = c[sel] if acc is None else np.concatenate([acc, c[sel]])
        print(f, "fill +", int(sel.sum()))
        pieces.append(m[sel])
    save(a.out, np.concatenate(pieces))
    print("out", a.out, sum(len(p) for p in pieces))


if __name__ == "__main__":
    main()
