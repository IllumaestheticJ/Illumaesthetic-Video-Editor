"""Trunk lid panel from the full car via filled masks (the Trunk Open extract is patchy, like the hood's was).
Deck: top-view (x,y) mask of the glass-trimmed extract on a 20 mm grid, closed + hole-filled + largest component;
car tris in the mask with z > 700 mm within 40 mm of the column top, behind the glass line (lid_trim.py output already
starts there). Rear face: rear-view (x,z) mask of extract tris with y > 1850 mm, same morphology; car tris in it within
40 mm of the column's rearmost y. Lid = deck | rear face.
Edges: inside each mask eroded by 3 cells (60 mm) everything is lid; in the outer band only car tris > 6 mm from the
Trunk Open scan count (tail lamps / quarters ARE in that scan), so the edge follows the real panel gap, not the grid.
  lid_mask.py car.stl lid_trimmed_extract.stl trunk_open.stl[,trunk_open_bumper_off.stl] out.stl"""
import struct, sys
import numpy as np
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = car["v"].mean(1)
e = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].mean(1)
g = 20.0


def mask(p2, lo, shape):
    M = np.zeros(shape, bool); k = ((p2 - lo) / g).astype(int)
    ok = (k[:, 0] >= 0) & (k[:, 0] < shape[0]) & (k[:, 1] >= 0) & (k[:, 1] < shape[1]); M[k[ok, 0], k[ok, 1]] = True
    M = ndimage.binary_closing(M, iterations=3); M = ndimage.binary_fill_holes(M); M = ndimage.binary_opening(M, iterations=1)
    lab, n = ndimage.label(M); return lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)


def core(p2, M, lo):
    C = ndimage.binary_erosion(M, iterations=3); k = ((p2 - lo) / g).astype(int)
    ok = (k[:, 0] >= 0) & (k[:, 0] < M.shape[0]) & (k[:, 1] >= 0) & (k[:, 1] < M.shape[1])
    r = np.zeros(len(p2), bool); r[ok] = C[k[ok, 0], k[ok, 1]]; return r


def pick(p2, M, lo, depth, tol=40):
    k = ((p2 - lo) / g).astype(int); ok = (k[:, 0] >= 0) & (k[:, 0] < M.shape[0]) & (k[:, 1] >= 0) & (k[:, 1] < M.shape[1])
    inm = np.zeros(len(p2), bool); inm[ok] = M[k[ok, 0], k[ok, 1]]
    key = k[:, 0] * 10000 + k[:, 1]; best = {}
    for kk, d in zip(key[inm], depth[inm]): best[kk] = max(best.get(kk, -1e9), d)
    bd = np.array([best.get(kk, 1e9) for kk in key]); return inm & (depth > bd - tol)


lo1 = np.array([-1100.0, 1000.0]); M1 = mask(e[e[:, 2] > 700][:, :2], lo1, (110, 60))
top = (c[:, 2] > 700) & (c[:, 1] > e[:, 1].min() - 5)
deck = np.zeros(len(c), bool); deck[top] = pick(c[top][:, :2], M1, lo1, c[top][:, 2])
er = e[e[:, 1] > 1850]; lo2 = np.array([-1100.0, 500.0]); M2 = mask(er[:, [0, 2]], lo2, (110, 40))
rear = c[:, 1] > 1850
face = np.zeros(len(c), bool); face[rear] = pick(c[rear][:, [0, 2]], M2, lo2, c[rear][:, 1])
from scipy.spatial import cKDTree
cand = np.where(deck | face)[0]
d = np.full(len(cand), np.inf)
for f in sys.argv[3].split(","):   # every open-lid state: a tri near ANY of them is body (tail lamps), not lid
    st = np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1)
    d = np.minimum(d, cKDTree(st).query(c[cand], distance_upper_bound=30)[0])
inner = np.zeros(len(c), bool)
inner[top] |= core(c[top][:, :2], M1, lo1); inner[rear] |= core(c[rear][:, [0, 2]], M2, lo2)
inner &= np.abs(c[:, 0]) < 430   # tail lamps start outboard of this; there only the scan distance decides
sel = np.zeros(len(c), bool); sel[cand] = inner[cand] | (d > 6)
# Trunk Open also misses bits of the tail lamps next to the raised lid: hard width limits (rear face between the lamps)
sel &= np.where((face & ~deck) | (c[:, 1] > 1750), np.abs(c[:, 0]) < 470, np.abs(c[:, 0]) < 640)
outer = np.abs(c[:, 0]) > 380; sel[cand] &= ~(outer[cand] & (d < 6))   # tail-lamp tops next to the deck
print("deck mask cells", M1.sum(), "rear mask cells", M2.sum(), "deck tris", deck.sum(), "face tris", face.sum(), "lid", sel.sum(),
      "bbox", c[sel].min(0).round(), c[sel].max(0).round())
with open(sys.argv[4], "wb") as f:
    f.write(b"gr86 trunk lid mask".ljust(80)); f.write(struct.pack("<I", int(sel.sum()))); car[sel].tofile(f)
