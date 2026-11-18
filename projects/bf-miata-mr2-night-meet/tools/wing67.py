"""User 2026-11-18: "the TC wing needs to be the bigger 67 inch one". Stretch a 47.5" (1206 mm) TC wing mesh to the
66.5" element (engineering Drive 'BMS-S420C-1700mm.stp' = 1700 mm span; store variant 66.5"): endplates move rigidly out to
the new tips, element vertices beyond the uprights stretch linearly, uprights/bases (|x| <= INNER) stay where they are.
    python wing67.py in.stl out.stl            (GLB frame, x lateral)"""
import sys
import numpy as np

TIP0, TIP1, INNER, PLATE = 0.606, 0.850, 0.56, 0.590   # m: old/new half-span, last upright vertex, endplate inner face


def stretch_x(x, tip0=TIP0):
    a, s = np.abs(x), np.sign(x); d = TIP1 - tip0
    out = a.copy()
    mid = (a > INNER) & (a < PLATE)
    out[mid] = INNER + (a[mid] - INNER) * (PLATE + d - INNER) / (PLATE - INNER)
    out[a >= PLATE] += d
    return s * out


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from scan_to_glb import read_stl, write_stl
    T = read_stl(sys.argv[1]); T[..., 0] = stretch_x(T[..., 0])
    write_stl(sys.argv[2], T); print(sys.argv[2], "span", round(T[..., 0].min(), 3), round(T[..., 0].max(), 3))
