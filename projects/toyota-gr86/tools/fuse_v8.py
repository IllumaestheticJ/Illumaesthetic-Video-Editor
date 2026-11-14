"""v8 (user on v7: "the two BRZ and GR86 bumpers are still clipping each other on the sidemarker scene";
"BRZ and GR86 rear bumpers are the same - don't need to do the splitting thing").
The at-rest bumper was the BRZ full car's bumper skin + the GR86 Bomex scan's tris > 6 mm from that skin - which kept GR86
surface lying ON or IN FRONT OF the skin: z-fighting speckle and GR86 shape poking through (sidemarker close-up, rear corners).
Fused v8 = BRZ skin + only the GR86 tris that lie BEHIND the skin by > --behind mm (signed distance along the skin's outward
normal; outward = away from the car centre), i.e. the real inner face. Nothing of the GR86 scan can show through the skin.
  front_bumper_v8m  skin of front_bumper_v4 (markers in, before m1) + GR86 front behind
  front_bumper_v8   fb_brz (markers out + recess) + GR86 front behind
  rear_bumper_v8    rb_brz + GR86 rear (lights out) behind   - the rear is one part again (no split: same bumper)
  fuse_v8.py [--behind 8]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = "/home/user/media/work/gr86/"
ap = argparse.ArgumentParser(); ap.add_argument("--behind", type=float, default=8.0); a = ap.parse_args()
L = lambda f: np.fromfile(M + f, dtype=TRI, offset=84)
car_tree = cKDTree(L("clean/car4.stl")["v"].mean(1))


def save(f, m, tag):
    with open(M + f, "wb") as o:
        o.write(("gr86 " + tag).encode().ljust(80)); o.write(struct.pack("<I", len(m))); m.tofile(o)
    print(f, len(m))


def fuse(skin, gr86, out, tag):
    sc = skin["v"].mean(1).astype(float); v = skin["v"].astype(float)
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    n[((sc - np.array([9.0, 0.0, 500.0])) * n).sum(1) < 0] *= -1          # outward = away from the car centre
    gc = gr86["v"].mean(1).astype(float)
    d, j = cKDTree(sc).query(gc, workers=-1)
    s = ((gc - sc[j]) * n[j]).sum(1)
    keep = s < -a.behind
    print(f"{out}: skin {len(skin)} + GR86 behind {int(keep.sum())} of {len(gr86)} (dropped on/in front of the skin: {int((~keep).sum())})")
    save(out, np.concatenate([skin, gr86[keep]]), tag)


fb4 = L("parts/front_bumper_v4.stl"); d, _ = car_tree.query(fb4["v"].mean(1), distance_upper_bound=0.05, workers=-1)
fb_gr86 = L("parts/fb_gr86.stl")
fuse(fb4[d < 0.05], fb_gr86, "parts/front_bumper_v8m.stl", "front bumper v8 markers in (BRZ skin + GR86 inner)")
fuse(L("parts/fb_brz.stl"), fb_gr86, "parts/front_bumper_v8.stl", "front bumper v8 (BRZ skin + GR86 inner)")
fuse(L("parts/rb_brz.stl"), L("parts/rb_gr86.stl"), "parts/rear_bumper_v8.stl", "rear bumper v8 (skin + GR86 inner)")
