"""NC TC wing (swan short mount) for the user's request "the NC should also have ... the TC wing included".
Source: engineering Drive 'NC swan short mount assm.stp' (1mrtynCDvxFzutOrOV0R7i7iEHg-r8agt) + its drawing
'NC swan short mount.pdf' (designed on an NC scan; uprights 981 mm apart, base plates on the trunk lid's rear edge).
The STEP holds the 1700 mm element, both endplates and ONE upright + base: the other upright is mirrored.
STEP (meshed per solid, OCP BRepMesh; the element is the 47.5" = 1206 mm one). STEP frame (mm): z lateral, y fore-aft (+ = rearward), -x up -> GLB frame (m): x = z, y = y, z = -x.
Placement: base plates' rear end 40 mm ahead of the scanned lid's rear edge; height so the plate undersides sit on the lid.
    python nc_tcwing.py  -> kit_nc/part_tc_wing.stl"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl
M = "/home/user/media/bf-miata-mr2-night-meet"
T = read_stl(f"{M}/tc/nc_swan.stl")
G = np.stack([T[..., 2], T[..., 1], -T[..., 0]], -1) / 1000.0          # det +1, so winding is kept
c = G.mean(1)
up = (c[:, 0] > 0.38) & (c[:, 0] < 0.56)                                 # the one upright + base plate
mir = G[up].copy(); mir[..., 0] *= -1; mir = mir[:, ::-1]                # mirror + flip winding
G = np.concatenate([G, mir])
S = read_stl(f"{M}/dec/nc_glbframe.stl").mean(1)
base = G[np.abs(G.mean(1)[:, 0]) > 0.38].reshape(-1, 3)
base = base[base[:, 2] < base[:, 2].min() + 0.012]                       # plate underside
# lid rear edge at the upright's lateral position
b = S[np.abs(np.abs(S[:, 0]) - 0.49) < 0.02]
ys = np.arange(1.2, 1.95, 0.005); top = np.array([b[np.abs(b[:, 1] - y) < 0.006][:, 2].max() if (np.abs(b[:, 1] - y) < 0.006).any() else np.nan for y in ys])
edge = ys[np.nanargmax(-np.diff(np.nan_to_num(top, nan=top[0])) )]      # steepest drop = rear edge of the lid
dy = (edge - 0.040) - base[:, 1].max()
G[..., 1] += dy; base[:, 1] += dy
lid = np.interp(base[:, 1], ys[np.isfinite(top)], top[np.isfinite(top)])
dz = np.median(lid - base[:, 2]); G[..., 2] += dz
print(f"lid edge y {edge:.3f}; shift y {dy:+.3f} z {dz:+.3f}; wing span x {G[...,0].min():.3f}..{G[...,0].max():.3f}; top z {G[...,2].max():.3f}; base plate y {base[:,1].min():.3f}..{base[:,1].max():.3f}")
write_stl(f"{M}/kit_nc/part_tc_wing_475.stl", G)
from wing67 import stretch_x                                             # v1.8: 66.5" element (user: "the bigger 67 inch one")
G[..., 0] = stretch_x(G[..., 0], np.abs(G[..., 0]).max()); write_stl(f"{M}/kit_nc/part_tc_wing.stl", G)
