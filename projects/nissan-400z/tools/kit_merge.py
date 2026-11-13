"""Merge the Bomex x Kaido House 400Z print sections (Ron's Folder/Nissan 400Z Bomex/Kaido House/STL, design frame, mm)
into one STL per part group: kit/merged/<group>.stl.  Side Skirts/Rear Fender ship as .3mf + .stl sections; only .stl used."""
import glob, os, re, struct
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
K = "/home/user/media/nissan-400z/kit"; O = f"{K}/merged"; os.makedirs(O, exist_ok=True)
def read(p):
    n = struct.unpack("<I", open(p, "rb").read(84)[80:84])[0]
    assert os.path.getsize(p) == 84 + 50 * n, f"not binary STL: {p}"
    return np.fromfile(p, dtype=TRI, offset=84)
groups = {}
for f in sorted(glob.glob(f"{K}/STL/**/*.stl", recursive=True)):
    rel = os.path.relpath(f, f"{K}/STL"); top = rel.split("/")[0]; b = os.path.basename(f)
    if top == "Mirror":
        if not rel.startswith("Mirror/V2"): continue
        g = "mirror_" + ("driver" if b.lower().startswith("driver") else "pass")
    elif top in ("Front Fender", "Rear Fender", "Canard", "Side Skirts"):
        side = "driver" if ".Driver" in b or "Driver" in b or "_L" in b or "Left" in b else ("pass" if ("Pass" in b or "_R" in b or "Right" in b) else "x")
        part = top.lower().replace(" ", "_")
        if "Slats" in b: part += "_slats"
        if "GasCap" in b: part = "gas_cap"
        g = f"{part}_{side}"
    else:
        g = top.lower().replace(" ", "_")
    groups.setdefault(g, []).append(f)
for g, fs in groups.items():
    m = np.concatenate([read(f) for f in fs])
    with open(f"{O}/{g}.stl", "wb") as fo:
        fo.write(b"bomex kit merged".ljust(80)); fo.write(struct.pack("<I", len(m))); m.tofile(fo)
    v = m["v"].reshape(-1, 3)
    print(f"{g:28s} {len(fs):3d} files {len(m):8d} tris  bbox {v.min(0).round()} {v.max(0).round()}")
