"""v1.5 (user: "the nc fender cuts don't line up well").
1. Local fit: rigid trimmed ICP of the lookbook body around the fender-cut area (door front, fender arch, sill; within
   25 cm of the part, excluding the part's own footprint) onto the scan -> transform applied to part_fender_cuts.
   Written as kit_nc/part_fender_cuts_fit.stl (the shot uses it in place of the global-fit part).
2. Zone = scan triangles inside the FITTED part's footprint (normal -60/+25 mm, lateral 3 mm) -> nc_fender_idx.npy, so
   the hole in the scan is exactly the part's outline.
    python nc_fender_fit.py"""
import sys, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl, umeyama
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; K = f"{M}/kit_nc"
S = read_stl(f"{D}/nc_glbframe.stl"); C = S.mean(1)
Pt = read_stl(f"{K}/part_fender_cuts.stl"); Pp = Pt.reshape(-1, 3)
B = read_stl(f"{K}/body.stl"); Bc = B.mean(1)
lo, hi = Pp.min(0) - 0.25, Pp.max(0) + 0.25
near = ((Bc > lo) & (Bc < hi)).all(1)
dpart, _ = cKDTree(Pp).query(Bc[near]); ring = Bc[near][dpart > 0.03]
ring = ring[np.abs(ring[:, 0]) > 0.55]                       # outer skin only (both sides)
tree = cKDTree(C)
R, t = np.eye(3), np.zeros(3)
d0, _ = tree.query(ring); print(f"ring {len(ring)} pts; before median {np.median(d0)*1e3:.1f} mm p90 {np.percentile(d0,90)*1e3:.1f}")
for keep, it in ((0.7, 30), (0.8, 30)):
    for _ in range(it):
        P = ring @ R.T + t; d, j = tree.query(P); m = d <= np.quantile(d, keep)
        _, R, t = umeyama(ring[m], C[j[m]], False)
d1, _ = tree.query(ring @ R.T + t); print(f"after median {np.median(d1)*1e3:.1f} mm p90 {np.percentile(d1,90)*1e3:.1f}; shift {np.round(t*1e3,1)} mm")
F = (Pp @ R.T + t).reshape(-1, 3, 3); write_stl(f"{K}/part_fender_cuts_fit.stl", F)
# part-to-scan gap at the part's rim (how flush it sits)
rimd, _ = tree.query(F.reshape(-1, 3)); print(f"part verts to scan: median {np.median(rimd)*1e3:.1f} mm")
# footprint zone from the fitted part: dense samples (3 mm) so the lateral limit can be tight (4 mm)
import importlib.util
sp = importlib.util.spec_from_file_location("cp_samples", __file__.rsplit("/", 1)[0] + "/cutparts.py")
src = open(sp.origin).read().split("def main():")[0]; ns = {"__file__": sp.origin}; exec(src, ns)
write_stl("/tmp/_fit_part.stl", F); Fc, n = ns["samples"](["/tmp/_fit_part.stl"])
lo2, hi2 = Fc.min(0) - 0.07, Fc.max(0) + 0.07
cand = np.where(((C > lo2) & (C < hi2)).all(1))[0]
d, j = cKDTree(Fc).query(C[cand], k=8, distance_upper_bound=0.08)
m = np.zeros(len(cand), bool)
for k in range(8):
    okk = np.isfinite(d[:, k]); jj = np.where(okk, j[:, k], 0)
    v = C[cand] - Fc[jj]; sn = (v * n[jj]).sum(1); dl = np.sqrt(np.maximum((v * v).sum(1) - sn * sn, 0))
    m |= okk & (sn >= -0.060) & (sn <= 0.025) & (dl <= 0.004)
np.save(f"{D}/nc_fender_idx.npy", cand[m]); print("fender zone tris", int(m.sum()))
