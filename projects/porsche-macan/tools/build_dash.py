"""Music v4 (user: "make sure all parts of the car are highlighted"): a dash-out base so the separately scanned dash
can lift out of the cabin.

    python projects/porsche-macan/tools/build_dash.py /home/user/media/porsche-macan/comp

Input: comp_explode_int.stl (build_int.py) + lev/dash_sep.stl (same levelled frame; it sits 5-9 mm off the cabin
scans where they overlap, i.e. on its visible face, so the cut radius is 30 mm).
Output: comp_explode_int_nd.stl = comp_explode_int minus every triangle within 30 mm of the dash scan (inside its
bbox + 60 mm), and x_dash.stl (the dash part, unmoved).
"""
import sys
import numpy as np
from build import L, load, save, near

out = sys.argv[1]
base = load(f"{out}/comp_explode_int.stl"); bc = base["v"].mean(1)
d = load(f"{L}/dash_sep.stl"); dc = d["v"].mean(1)
lo, hi = dc.min(0) - 60, dc.max(0) + 60
inb = np.all((bc >= lo) & (bc <= hi), 1)
sel = np.zeros(len(base), bool); sel[inb] = near(bc[inb], dc, 30)
print("dash: base tris dropped", int(sel.sum()))
save(f"{out}/x_dash.stl", d)
save(f"{out}/comp_explode_int_nd.stl", base[~sel])
