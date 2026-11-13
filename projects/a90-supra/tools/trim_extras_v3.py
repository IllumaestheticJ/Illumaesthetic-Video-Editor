"""Trim the car-skin 'extras' that ride with each removed part (build_v3.py) to what actually closes gaps in the part scan:
keep extra tris within 25 mm of the part scan, drop islands < 500 tris. Ragged strips beyond the scan's edge (under-lip skin)
looked like loose fragments hanging off the parked bumper. Rewrites part_<zone>.stl (+ lite copies are re-made by prep_v3.sh)."""
import struct, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from build_v3 import TRI, OUT, islands

RAW = {"part_uskirt": 5339371, "part_lskirt": 2049703}
for name, ex in (("part_fbump", "extra_fbump"), ("part_fender", "extra_fender"), ("part_dtrim", "extra_dtrim"), ("part_rbump", "extra_rbump"),
                 ("part_uskirt", None), ("part_lskirt", None)):
    m = np.fromfile(OUT + name + ".stl", dtype=TRI, offset=84)
    ne = RAW[name] and len(m) - RAW[name] if ex is None else len(np.fromfile(OUT + ex + ".stl", dtype=TRI, offset=84))
    part, extra = m[:len(m) - ne], m[len(m) - ne:]
    d, _ = cKDTree(part["v"].mean(1)[::3]).query(extra["v"].mean(1), distance_upper_bound=25.0, workers=4)
    e = extra[np.isfinite(d)]
    if len(e):
        lab = islands(e); e = e[np.bincount(lab)[lab] >= 500]
    out = np.concatenate([part, e])
    with open(OUT + name + ".stl", "wb") as f:
        f.write(b"ive trim_extras".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
    print(name, "extras", len(extra), "->", len(e))
