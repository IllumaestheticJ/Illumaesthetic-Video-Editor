"""Nest the lookbook kit into the scan the way the lookbook itself does it.

The GLB pairs every kit part with `body_<part>_stock` / `trim_<part>_stock`: the piece of stock body the part REPLACES
(hood skin under the vents, sill under the skirts, ...). The lookbook hides that piece when the part is shown. v3 put
the parts on top of the uncut scan, so scan skin poked through. This tool splits each scan object into
  <obj>_keep.stl                 scan that stays
  cut_<part>__<obj>.stl          scan lying on that part's stock piece (hidden when the part lands)
    python kit_nest.py [--thr 14]
Frames: dec/*_L.stl and kit/scan/*.stl share the raw-mm frame (`ive prep --like car3.json`)."""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read, write

M = "/home/user/media/toyota-mr2-spyder"; O = f"{M}/nest"; os.makedirs(O, exist_ok=True)
THR = float(sys.argv[sys.argv.index("--thr") + 1]) if "--thr" in sys.argv else 14.0
STOCK = {"hood_vents": ["body_hood_vent_stock"], "side_skirts": ["body_fender_cut_stock", "trim_fender_liner_stock"],
         "front_bumper": ["body_front_bumper_stock", "trim_front_bumper_stock"], "eyelids": ["body_eyelids_stock"],
         "duckbill": ["body_duckbill_stock"], "rear_spats": ["body_rear_spats_stock"], "tc_wing_kit": ["body_tc_wing_kit_stock"]}
SCAN = {"base": "base_L", "hood": "hood_L", "lid": "rearlid_L"}


def sample(d, step=6.0):
    """points on the triangles, ~step mm apart"""
    v = d["v"].astype(np.float64); a, b, c = v[:, 0], v[:, 1], v[:, 2]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    n = np.maximum(1, (area / (step * step)).astype(int)); idx = np.repeat(np.arange(len(v)), n)
    r = np.random.default_rng(0).random((len(idx), 2)); s = np.sqrt(r[:, 0]); u, w = 1 - s, s * r[:, 1]
    return np.vstack([a[idx] * u[:, None] + b[idx] * (s - w)[:, None] + c[idx] * w[:, None], a, b, c])


if __name__ == "__main__":
  trees = {p: cKDTree(np.vstack([sample(read(f"{M}/kit/scan/{s}.stl")) for s in ss])) for p, ss in STOCK.items()}
  rep = {}
  for obj, src in SCAN.items():
      d = read(f"{M}/dec/{src}.stl"); v = d["v"].astype(np.float64)
      owner = np.full(len(v), -1); best = np.full(len(v), THR)
      for i, (p, t) in enumerate(trees.items()):
          dist = np.max(np.stack([t.query(v[:, k], distance_upper_bound=THR * 2)[0] for k in range(3)]), axis=0)  # all 3 corners near
          m = dist < best; owner[m] = i; best[m] = dist[m]
      write(f"{O}/{obj}_keep.stl", d[owner < 0])
      for i, p in enumerate(trees):
          if (owner == i).sum() > 50:
              write(f"{O}/cut_{p}__{obj}.stl", d[owner == i]); rep[f"cut_{p}__{obj}"] = int((owner == i).sum())
      rep[f"{obj}_keep"] = int((owner < 0).sum())
  json.dump(rep, open(f"{O}/nest.json", "w"), indent=1); print(json.dumps(rep, indent=1))
