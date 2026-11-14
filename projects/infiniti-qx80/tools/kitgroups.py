"""Merge the levelled kit STLs into animation groups (one STL per group), then decimate at 1.5 mm.
  kitgroups.py lev_dir out_dir"""
import glob, os, struct, sys, subprocess, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
G = {
 "front_bumper": ["Print_printed__Nismo_QX80_Front_Bumper_1", "Print_printed__Nismo_QX80_Front_Bumper_2", "Light_Tab"],
 "front_lip": ["Print__Nismo_QX80_Front_Lip.stl"],
 "lower_grille": ["Lower_Grille"],
 "brake_ducts": ["Print_printed_K2__Nismo_QX80_Brake_Duct_"],
 "flare_fl": ["Print_printed__Nismo_QX80_Front_Left_Fender_Flare.stl"],
 "flare_fr": ["Print_printed__Nismo_QX80_Front_Right_Fender_Flare.stl"],
 "flare_rl": ["Rear_Left_Fender_Flare"],
 "flare_rr": ["Rear_Right_Fender_Flare"],
 "skirt_l": ["Side_Skirt_Left", "Side_Skirt_Mounting_Left"],
 "skirt_r": ["Side_Skirt_Right", "Side_Skirt_Mounting_Right"],
 "vent_l": ["Fender_Vent_With_Logo_Left.stl"],
 "vent_r": ["Fender_Vent_With_Logo_Right.stl"],
 "naca": ["Hood_NACA_Duct_Frame"],
 "wing": ["Nismo_QX80_Wing"],
 "diffuser": ["Print__Nismo_QX80_Diffuser.stl", "Diffuser_Fin"],
 "exhaust": ["Exhaust_Shroud_Left_Exhaust_Hole_Fix", "Exhaust_Shroud_Right_Exhaust_Hole_Fix", "Exhaust_Shroud_Mounting"],
}
files = sorted(glob.glob(L + "/*.stl"))
# Placement fixes (v7): Ecky's 'Fender_Vent_With_Logo_Left' (the vent with the motoIQ logo) is parked ~0.5 m outside the
# car's RIGHT side (x +1.49..+1.54 m) - it rendered as a floating badge piece in v6. A pure translation onto the K2 left
# vent (min-corner to min-corner) fits at 2.0 mm median / 6.7 mm p99, the same as the right with-logo vent vs the K2 right.
FIX = {"Fender_Vent_With_Logo_Left.stl": "Print_printed_K2__Nismo_QX80_Fender_Vent_Left.stl"}
def load(f):
    a = np.fromfile(f, dtype=TRI, offset=84)
    for k, ref in FIX.items():
        if os.path.basename(f).endswith(k):
            r = np.fromfile(os.path.join(L, ref), dtype=TRI, offset=84)["v"].reshape(-1, 3)
            a["v"] += (r.min(0) - a["v"].reshape(-1, 3).min(0)).astype(np.float32)
    return a
ONLY = sys.argv[3:]   # optional: rebuild only these groups
used = set()
for g, keys in G.items():
    if ONLY and g not in ONLY: continue
    fs = [f for f in files if any(k in os.path.basename(f) for k in keys)]
    used |= set(fs)
    a = np.concatenate([load(f) for f in fs])
    tmp = f"{out}/{g}_full.stl"
    with open(tmp, "wb") as fh:
        fh.write(b"qx80 kit group".ljust(80)); fh.write(struct.pack("<I", len(a))); a.tofile(fh)
    subprocess.run(["python", "-m", "ive", "decimate", tmp, f"{out}/{g}.stl", "--cell", "1.5"], capture_output=True)
    os.remove(tmp)
    print(g, len(fs), len(a), [os.path.basename(f)[:40] for f in fs])
print("unused:", [os.path.basename(f) for f in files if f not in used])
