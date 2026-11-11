"""Build the Macan's movable panels + "panels off" bases from Artec state scans (levelled mm frame, shared).

    python projects/porsche-macan/tools/build.py OUT_DIR

Panels (each = a part scan, or the car's own skin cut out where the part scan has holes):
  door_fl/fr/rl/rr  door scan (card + partial skin) + car triangles inside the door's YZ outline, outboard of the card
  hood              hood scan; car skin within 9 mm of it is cut
  fender            left front fender scan; car skin within 9 mm cut
  fbumper/rbumper   "(Warped)" bumper scans (verified 4.4 / 2.7 mm median from the car); car within 12 mm cut
  hatch             car triangles that moved between "Rear Hatch Closed" and "Rear Hatch Fully Open" (hinge.py)
Bases (car minus panels, plus only NEW geometry from the state scans inside the panel zones):
  comp_hood   - hood       (fill: Hood Removed)
  comp_hatch  - hatch      (fill: Rear Hatch Fully Open, minus the open hatch itself)
  comp_doors  - 4 doors    (fill: Doors and Hood Open, inboard of the door skins only - no swung-open doors)
  comp_explode- all panels (fills in order; later fills only add what earlier ones lack)
"""
import json, os, struct, sys
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = "/home/user/media/porsche-macan/lev"
H = "/home/user/media/work/macan/hinge"


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"porsche-macan build".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print("wrote", os.path.basename(p), len(m))


def near(c, pts, r):
    pts = pts[:: max(1, len(pts) // 1_500_000)]
    d, _ = cKDTree(pts).query(c, distance_upper_bound=r)
    return d < r


def door_mask(car_c, door_c):
    """Car triangles inside the door's YZ silhouette (10 mm grid, closed + hole-filled), outboard of the card."""
    side = np.sign(np.median(door_c[:, 0]))
    ax = np.abs(door_c[:, 0]); xin = np.percentile(ax, 1) - 10
    g = 10.0
    lo = door_c[:, 1:].min(0) - 30
    ij = np.floor((door_c[:, 1:] - lo) / g).astype(int)
    shp = ij.max(0) + 4
    m = np.zeros(shp, bool); m[ij[:, 0], ij[:, 1]] = True
    m = ndimage.binary_closing(m, iterations=4); m = ndimage.binary_fill_holes(m)
    m = ndimage.binary_erosion(m, iterations=1)  # keep the cut just inside the shut line
    cij = np.floor((car_c[:, 1:] - lo) / g).astype(int)
    ok = np.all((cij >= 0) & (cij < shp), 1)
    sel = np.zeros(len(car_c), bool)
    sel[ok] = m[cij[ok, 0], cij[ok, 1]]
    return sel & (np.sign(car_c[:, 0]) == side) & (np.abs(car_c[:, 0]) > xin), xin, side


def zone(c, pad=40.0):
    return c.min(0) - pad, c.max(0) + pad


def fill_new(fill, car_c, zones, acc, extra=None, new=7.0):
    c = fill["v"].mean(1)
    inz = np.zeros(len(c), bool)
    for zlo, zhi in zones:
        inz |= np.all((c >= zlo) & (c <= zhi), 1)
    if extra is not None:
        inz &= extra(c)
    idx = np.where(inz)[0]
    d, _ = cKDTree(car_c[::2]).query(c[idx], distance_upper_bound=new * 2)
    ok = d > new
    if len(acc):
        d2, _ = cKDTree(np.concatenate(acc)).query(c[idx], distance_upper_bound=new * 2)
        ok &= d2 > new
    sel = idx[ok]
    acc.append(c[sel])
    return fill[sel]


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    car = load(f"{L}/car4_clean.stl"); cc = car["v"].mean(1)
    panels = {}  # name -> (car-removal mask, part mesh, zone)
    for d in ("fl", "fr", "rl", "rr"):
        door = load(f"{L}/door_{d}_3mm.stl"); dc = door["v"].mean(1)
        sel, xin, side = door_mask(cc, dc)
        part = np.concatenate([door, car[sel]])
        z = zone(part["v"].mean(1), 30)
        panels[f"door_{d}"] = (sel, part, z, {"xin": float(xin), "side": float(side)})
        print(d, "car skin cut", int(sel.sum()), "xin", round(xin))
    for name, f, cut in (("hood", "hood_3mm", 9), ("fender", "fender_3mm", 9),
                         ("fbumper", "fbumper_warped_3mm", 12), ("rbumper", "rbumper_warped_3mm", 12)):
        p = load(f"{L}/{f}.stl"); pc = p["v"].mean(1)
        sel = near(cc, pc, cut)
        panels[name] = (sel, p, zone(pc), {})
        print(name, "car cut", int(sel.sum()))
    if os.path.exists(f"{H}/hatch.json.panel.npy"):
        hp = np.load(f"{H}/hatch.json.panel.npy")
        # keep only points the fitted hinge really carries onto the captured open hatch (drops coverage noise:
        # wheel-arch / quarter fragments that differ between the two state scans)
        hj = json.load(open(f"{H}/hatch.json")); like = json.load(open("/home/user/media/porsche-macan/prep/car4.json"))
        piv = (np.array(hj["pivot"]) - np.array(like["root_location"])) / like["unit_scale"]
        from scipy.spatial.transform import Rotation as Rot
        R = Rot.from_rotvec(np.radians(hj["open_deg"]) * np.array(hj["axis"])).as_matrix()
        d, _ = cKDTree(np.load(f"{H}/hatch.json.open.npy")).query((hp - piv) @ R.T + piv, distance_upper_bound=30)
        print("hatch panel pts", len(hp), "-> movers", int((d < 12).sum()))
        hp = hp[d < 12]
        sel = near(cc, hp, 15)
        panels["hatch"] = (sel, car[sel], zone(cc[sel]), {})
        print("hatch car cut", int(sel.sum()))
    for n, (sel, part, z, meta) in panels.items():
        save(f"{out}/x_{n}.stl", part)
    json.dump({n: {"zone": [z[0].tolist(), z[1].tolist()], **meta} for n, (s, p, z, meta) in panels.items()},
              open(f"{out}/panels.json", "w"), indent=1)

    fills = {
        "hood": [("hood_removed_clean", None)],
        "fender": [("fenders_removed_clean", lambda c: c[:, 0] > 0)],
        "fbumper": [("fbumper_off_clean", None)],
        "rbumper": [("rbumper_removed_clean", None)],
        "hatch": [("hatch_open_4mm", "open_hatch")],
    }
    for d in ("fl", "fr", "rl", "rr"):
        m = panels[f"door_{d}"][3]
        # inboard of the door skin only: the swung-open doors in the state scan stay out
        fills[f"door_{d}"] = [("doors_hood_open_clean",
                               (lambda xin, s: (lambda c: (np.sign(c[:, 0]) == s) & (np.abs(c[:, 0]) < xin + 260)))(m["xin"], m["side"]))]
    cache = {}

    def get(f):
        if f not in cache:
            cache[f] = load(f"{L}/{f}.stl")
        return cache[f]

    openh = np.load(f"{H}/hatch.json.open.npy") if os.path.exists(f"{H}/hatch.json.open.npy") else None
    sets = {"comp_hood": ["hood"], "comp_hatch": ["hatch"], "comp_doors": [f"door_{d}" for d in ("fl", "fr", "rl", "rr")],
            "comp_explode": ["hood", "fender", "fbumper", "rbumper", "hatch"] + [f"door_{d}" for d in ("fl", "fr", "rl", "rr")]}
    for sname, names in sets.items():
        names = [n for n in names if n in panels]
        keep = np.ones(len(car), bool)
        for n in names:
            keep &= ~panels[n][0]
        pieces, acc = [car[keep]], []
        for n in names:
            for f, extra in fills.get(n, []):
                if extra == "open_hatch":
                    ex = (lambda c: ~near(c, openh, 40)) if openh is not None else None
                else:
                    ex = extra
                add = fill_new(get(f), cc, [panels[n][2]], acc, ex)
                print(sname, n, f, "+", len(add))
                pieces.append(add)
        save(f"{out}/{sname}.stl", np.concatenate(pieces))


if __name__ == "__main__":
    main()
