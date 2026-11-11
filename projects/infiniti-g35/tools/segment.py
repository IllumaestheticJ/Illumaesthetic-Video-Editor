"""Split the G35 coupe full-car scan into body panels for the exploded view / trunk opening.

The coupe folder has only one part scan (G35 Trunk, outer skin, scanned without the car's aftermarket spoiler) and no
'... removed' states, so the other panels are cut out of the full-car scan along the panel seams read off orthographic
renders (reg/ortho_side*.png, ortho_top.png). Coordinates: prepped Blender metres (frame.json root), nose -Y, +X = car's left.
    segment.py frame.json car.stl trunk.stl outdir
Writes (raked mm STLs, prep them --like frame.json): base.stl (car minus every panel), base_trunk.stl (car minus lid+spoiler),
x_hood, x_door_l, x_door_r, x_fbumper, x_rbumper, x_spoiler (+ the trunk part itself is the lid)."""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(sys.argv[1]))["root_location"]) * 1000
car = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
part = np.fromfile(sys.argv[3], dtype=TRI, offset=84)
out = sys.argv[4]
c = (car["v"].mean(1) + root) / 1000.0
x, y, z = c[:, 0], c[:, 1], c[:, 2]
ax = np.abs(x)

def save(name, m):
    with open(f"{out}/{name}.stl", "wb") as f:
        f.write(b"infiniti-g35 segment".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
    print(name, len(m))

# trunk lid skin on the car (within 12 mm of the part) + spoiler (car geometry above the lid inside its footprint)
pc = (part["v"].mean(1) + root) / 1000.0
tp = cKDTree(pc[::3])
inbox = np.all((c > pc.min(0) - 0.03) & (c < pc.max(0) + [0.03, 0.03, 0.15]), 1)
d, i = tp.query(c[inbox])
lid_skin = np.zeros(len(c), bool); lid_skin[np.where(inbox)[0][d < 0.012]] = True
pxy = cKDTree(pc[::3, :2]); dxy, j = pxy.query(c[:, :2])
spoiler = inbox & ~lid_skin & (dxy < 0.02) & (z > pc[::3][j, 2] + 0.012)
spoiler |= (y > 1.55) & (z > 1.12) & (ax < 0.70) & ~lid_skin  # spoiler wings past the lid edge
# hood: top view polygon (rear seam curves -0.92 at the sides to -1.06 centre; sides converge to +-0.53 at the front)
t = np.clip((-y - 1.0) / 1.12, 0, 1)                   # 0 at rear seam .. 1 at the front edge
half = 0.78 - 0.25 * t ** 1.5
rear = -0.92 - 0.14 * (1 - (x / 0.78) ** 2).clip(0)
hood = (y < rear) & (y > -2.13) & (ax < half) & (z > 0.80) & (car["n"][:, 2] > -0.2)
# front bumper cover: ahead of the fender seam (y -1.83) below the headlights (z .845), grille area up to the hood edge
fb = ((y < -1.83) & (z < 0.845)) | ((y < -2.10) & (z < 0.98) & ~hood)
# rear bumper: behind the rear-arch seam (y 1.90) below the tail-lamp seam (z .89)
rb = (y > 1.90) & (z < 0.89) & ~lid_skin
# doors: outer skin between the A-post seam (y -.88) and the slanted rear seam (y .393 at sill -> .474 at belt), sill .47 to belt 1.19
yr = 0.393 + (z - 0.474) / (1.18 - 0.474) * (0.474 - 0.393)
door = (y > -0.88) & (y < yr) & (z > 0.47) & (z < 1.19) & (ax > 0.62)
mirror = (y > -0.90) & (y < -0.42) & (z > 1.13) & (z < 1.34) & (ax > 0.80)
door_l = (door | mirror) & (x > 0); door_r = (door | mirror) & (x < 0)
panels = {"x_hood": hood, "x_fbumper": fb & ~hood, "x_rbumper": rb, "x_door_l": door_l, "x_door_r": door_r, "x_spoiler": spoiler}
used = np.zeros(len(c), bool)
for k, m in panels.items():
    m = m & ~used; used |= m; save(k, car[m])
save("base", car[~(used | lid_skin)])
save("base_trunk", car[~(lid_skin | spoiler)])
