"""Trunk lid = what MOVED when the lid was opened (user v8: "the rear trunk is not cut right" - the deck-only cut left the lid's
wrapped rear face, the badge garnish between the tail lights, on the body).
Car triangles (levelled mm) inside a loose rear box that are > --moved mm from the trunk-open state scan (absent there = moved),
> --bumper mm from the rear-bumper part scan, then the largest 12 mm-linked blob. Tail lights / fenders / cabin are present in
the state scan, so they stay on the body.
  lid_from_state.py car.stl state_open.stl rbumper.stl out.stl"""
import sys, struct, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car, st, rb = (np.fromfile(p, dtype=TRI, offset=84) for p in sys.argv[1:4])
cc = car["v"].mean(1)
box = (cc[:, 1] > 1400) & (cc[:, 2] > 600) & (cc[:, 0] > -560) & (cc[:, 0] < 810)
idx = np.where(box)[0]
d_st, _ = cKDTree(st["v"].mean(1)).query(cc[idx], distance_upper_bound=40)
d_rb, _ = cKDTree(rb["v"].mean(1)).query(cc[idx], distance_upper_bound=40)
cand = idx[(d_st > 8) & (d_rb > 10)]
P = cc[cand]
pairs = cKDTree(P).query_pairs(12.0, output_type="ndarray")
n, lab = connected_components(coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(P), len(P))))
big = np.bincount(lab).argmax(); keep = cand[lab == big]
k = car[keep]
with open(sys.argv[4], "wb") as f: f.write(b"miata lid_from_state".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("candidates", len(cand), "blobs", n, "lid", len(keep), "bbox", cc[keep].min(0).round(), cc[keep].max(0).round())
