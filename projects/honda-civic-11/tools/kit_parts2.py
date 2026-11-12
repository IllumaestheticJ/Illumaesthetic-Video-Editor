"""v5 kit parts: everything from RON'S OWN design scene, placed by registering his copy of the scan to ours.

    python kit_parts2.py
User on v4: "all the parts are placed on incorrectly/inaccurately" (v4 used the lookbook game model, body-ICP'd at 10 mm).
Ron's frame (m, front -Y, car's left +X, level): 'Civic 11th gen lip kit review.blend' holds the FE1 facelift scan and the
kit; the production STLs (mm) and 'Honda Civic Sedan 2022-render.blend' (wing.002, wheels *.001) share that frame.
kit/ron_to_scan.json = rigid ICP of Ron's 'FE1 Fl' scan onto dec/fe1_full_4mm (median 1.4 mm).
Writes kit/parts2/*.stl in RAW scan units (prep --like car4.json):
  front_lip (EP-HC11KK-FLV1-PU), rear_apron (EP-HC11SD-RLV1-PU), skirt_L/skirt_R (SSV1 LH/RH), wing (wing.002),
  {rim,tyre,brake}_{FL,FR,RL,RR} (Ron's wheels where HE put them: 47 mm up in the arch and 30 mm out vs the scanned wheels =
  his lowered, flush fitment), car_nowheels, scanwheel_{FL,FR,RL,RR} (scanned wheels cut by cylinders at the SCANNED centres).
"""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read, write  # noqa: E402

M = "/home/user/media/honda-civic-11"; K = f"{M}/kit"; O = f"{K}/parts2"
os.makedirs(O, exist_ok=True)
T = json.load(open(f"{K}/ron_to_scan.json")); R = np.array(T["R"]); t = np.array(T["t"])
root = np.array(json.load(open(f"{M}/prep/car4.json"))["root_location"])


def put(src, dst, scale):
    """Ron frame (units * scale = m) -> raw scan mm."""
    d = src if not isinstance(src, str) else read(src)
    p = (d["v"].reshape(-1, 3).astype(np.float64) * scale) @ R.T + t
    d = d.copy(); d["v"] = ((p - root) / 0.001).reshape(-1, 3, 3).astype(np.float32)
    d["n"] = (d["n"].astype(np.float64) @ R.T).astype(np.float32)
    write(f"{O}/{dst}.stl", d); print(dst, len(d), p.min(0).round(3), p.max(0).round(3))


put(f"{M}/ron/kit/EP-HC11KK-FLV1-PU.stl", "front_lip", 0.001)
put(f"{M}/ron/kit/EP-HC11SD-RLV1-PU.stl", "rear_apron", 0.001)
for f in glob.glob(f"{M}/ron/kit/Side Skirt *.stl"):
    put(f, "skirt_L" if "LH" in f else "skirt_R", 0.001)     # LH = car's left = Ron +X -> prepped -X
put(glob.glob(f"{K}/ron/wing_002__0_*.stl")[0], "wing", 1.0)
for w in ("FL", "FR", "RL", "RR"):     # Ron's FL = car's front-left
    g = {k: f for f in glob.glob(f"{K}/ron/{w}_001__*.stl") for k in [int(os.path.basename(f).split("__")[1][0])]}
    put(g[5], f"rim_{w}", 1.0); put(g[0], f"tyre_{w}", 1.0)
    put(np.concatenate([read(g[k]) for k in (1, 2, 3, 4)]), f"brake_{w}", 1.0)

# scanned wheels: cylinders about the scanned wheel centres (circle fits to the tread, Ron frame; FR's z fit was noisy -> 0.319)
CEN = {"FL": (-1.033, 0.319), "FR": (-1.050, 0.319), "RL": (1.632, 0.316), "RR": (1.630, 0.317)}
car = read(f"{M}/dec/fe1_final_4mm.stl"); A = ((car["v"].mean(1) * 0.001 + root) - t) @ R
cut = np.zeros(len(car), bool)
for w, (cy, cz) in CEN.items():
    sx = 1 if w[1] == "L" else -1
    m = (np.hypot(A[:, 1] - cy, A[:, 2] - cz) < 0.326 + (0.050 if w[0] == "F" else 0.022)) & (A[:, 0] * sx > (0.45 if w[0] == "F" else 0.55))   # fronts are steered: +50 mm   # +22 mm: the steered front tyres left a tread sliver at +12
    write(f"{O}/scanwheel_{w}.stl", car[m]); cut |= m; print("scanwheel", w, int(m.sum()))
# leftovers: scan fragments near a wheel that are not connected to the body (the steered front-left tyre left a tread
# sliver outside its cylinder). Components that lie wholly inside a wheel box go with that scanned wheel.
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
rest = np.nonzero(~cut)[0]
for w, (cy, cz) in CEN.items():
    sx = 1 if w[1] == "L" else -1
    box = (np.abs(A[rest, 1] - cy) < 0.50) & (A[rest, 0] * sx > 0.40) & (A[rest, 2] < cz + 0.45)
    idx = rest[box]
    v = car["v"][idx].reshape(-1, 3); _, inv = np.unique(v.round(1), axis=0, return_inverse=True); f = inv.reshape(-1, 3)
    n = inv.max() + 1
    g = coo_matrix((np.ones(len(f) * 2), (np.r_[f[:, 0], f[:, 1]], np.r_[f[:, 1], f[:, 2]])), shape=(n, n))
    _, lab = connected_components(g, directed=False); fl = lab[f[:, 0]]
    # a component touching the box boundary continues into the body: keep it
    edge = (np.abs(A[idx, 1] - cy) > 0.49) | (A[idx, 0] * sx < 0.41) | (A[idx, 2] > cz + 0.44)
    keep = np.isin(fl, np.unique(fl[edge]))
    extra = idx[~keep]; cut[extra] = True
    write(f"{O}/scanwheel_{w}.stl", car[np.r_[np.nonzero((np.hypot(A[:, 1] - cy, A[:, 2] - cz) < 0.326 + (0.050 if w[0] == "F" else 0.022)) & (A[:, 0] * sx > (0.45 if w[0] == "F" else 0.55)))[0], extra]])
    print("leftover fragments ->", w, len(extra))
write(f"{O}/car_nowheels.stl", car[~cut])
