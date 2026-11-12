"""Build the Epsilon-kit part meshes for the scan car (raw scan units, to be prepped --like car4.json).

    python kit_parts.py
From kit/scan/*.stl (lookbook model fitted to the scan by align_kit.py) and dec/fe1_final_4mm.stl:
  kit/parts/car_nowheels.stl      scan car minus its scanned wheels (cylinder around each fitted axle)
  kit/parts/scanwheels_{L,R}.stl  the scanned wheels that were cut out (slide off before the new wheels go on)
  kit/parts/{rims,tyres,brakes}_{L,R}.stl   new wheels by material;  front_lip / side_skirts / rear_lip / sport_wing copied.
"""
import json, os, shutil, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read, write  # noqa: E402

M = "/home/user/media/honda-civic-11"; K = f"{M}/kit"
os.makedirs(f"{K}/parts", exist_ok=True)
T = json.load(open(f"{K}/model_to_scan.json")); R = np.array(T["R"]); axle = R @ np.array([1.0, 0, 0])
root = np.array(json.load(open(f"{M}/prep/car4.json"))["root_location"])
car = read(f"{M}/dec/fe1_final_4mm.stl"); c = car["v"].mean(1) * 0.001 + root
cut = {"L": np.zeros(len(car), bool), "R": np.zeros(len(car), bool)}
for w in ("FL", "FR", "RL", "RR"):
    t = read(f"{K}/scan/wheel_{w}_tyre.stl")["v"].reshape(-1, 3) * 0.001 + root
    cen = (t.min(0) + t.max(0)) / 2
    ax = (t - cen) @ axle; rad = np.linalg.norm((t - cen) - np.outer(ax, axle), axis=1)
    r, half = rad.max(), np.abs(ax).max()
    d = c - cen; a = d @ axle; rr = np.linalg.norm(d - np.outer(a, axle), axis=1)
    m = (rr < r + 0.012) & (np.abs(a) < half + 0.10)
    side = "R" if cen[0] > 0 else "L"   # prepped +X = car's right
    cut[side] |= m
    print(w, "centre", cen.round(3), "r %.3f half-width %.3f" % (r, half), "scan tris cut", int(m.sum()))
both = cut["L"] | cut["R"]
write(f"{K}/parts/car_nowheels.stl", car[~both])
for s in "LR":
    write(f"{K}/parts/scanwheels_{s}.stl", car[cut[s]])
for kind in ("rim", "tyre", "brake"):
    for s, ws in (("L", ("FL", "RL")), ("R", ("FR", "RR"))):
        # model left (+x) lands on prepped -X = the car's left; file names follow the model's own FL/FR
        parts = [read(f"{K}/scan/wheel_{w}_{kind}.stl") for w in ws]
        cen = np.concatenate([p["v"].reshape(-1, 3) for p in parts]).mean(0) * 0.001 + root
        side = "R" if cen[0] > 0 else "L"
        write(f"{K}/parts/{kind}s_{side}.stl", np.concatenate(parts))
for p in ("front_lip", "side_skirts", "rear_lip", "sport_wing"):
    shutil.copy(f"{K}/scan/{p}.stl", f"{K}/parts/{p}.stl")
print(sorted(os.listdir(f"{K}/parts")))
