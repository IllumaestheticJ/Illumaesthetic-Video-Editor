"""Flatten the licence plates (user: plate must not be readable). Run inside Blender on a .blend:

    blender -b in.blend -P projects/lexus-is300/tools/plate.py -- [front] [rear] [--dry]

Only on meshes that carry a plate: car/car2 (both), fbumper (front), lid (rear). NOT the composites: in comp_explode the
front box holds the intercooler face and the rear box the open trunk (chk/comp_front.png, comp_rear.png).

Every mesh vertex inside a plate box (prepped frame, metres) and within TOL of the plate's robust plane is projected
onto that plane, removing the embossed characters; the plate renders as a plain satin rectangle. Saves in place.
Boxes were measured from front/rear depth maps of lv/car_2mm.stl (chk/plate_front.png, plate_rear.png)."""
import sys
import bpy
import numpy as np

PLATES = {  # name: (xmin, xmax, zmin, zmax, y side: -1 front / +1 rear, |y| min)
    "front": (-0.16, 0.25, 0.30, 0.50, -1, 2.08),
    "rear": (-0.22, 0.18, 0.69, 0.91, 1, 2.0),
}
TOL = 0.015
dry = "--dry" in sys.argv
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
want = [a for a in argv if a in PLATES] or list(PLATES)
total = 0
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world)
    w = co @ M[:3, :3].T + M[:3, 3]
    changed = 0
    for name, (x0, x1, z0, z1, s, ymin) in PLATES.items():
        if name not in want:
            continue
        m = (w[:, 0] > x0) & (w[:, 0] < x1) & (w[:, 2] > z0) & (w[:, 2] < z1) & (s * w[:, 1] > ymin)
        if m.sum() < 50:
            continue
        p = w[m]
        # robust plane y = a + b x + c z, fitted on the outermost surface (plate face) in the box
        face = p[s * p[:, 1] > np.percentile(s * p[:, 1], 40)]
        A = np.c_[np.ones(len(face)), face[:, 0], face[:, 2]]
        coef = np.linalg.lstsq(A, face[:, 1], rcond=None)[0]
        for _ in range(3):
            r = face[:, 1] - A @ coef
            k = np.abs(r) < max(3 * np.median(np.abs(r)), 0.002)
            coef = np.linalg.lstsq(A[k], face[k, 1], rcond=None)[0]
        yp = coef[0] + coef[1] * w[:, 0] + coef[2] * w[:, 2]
        sel = m & (np.abs(w[:, 1] - yp) < TOL)
        print(f"{ob.name}: {name} plate {sel.sum()} verts, plane y={coef[0]:.3f}+{coef[1]:.3f}x+{coef[2]:.3f}z")
        w[sel, 1] = yp[sel]
        changed += sel.sum()
    if changed and not dry:
        inv = np.linalg.inv(M)
        loc = w @ inv[:3, :3].T + inv[:3, 3]
        me.vertices.foreach_set("co", loc.ravel())
        me.update()
        total += changed
print("TOTAL", total)
if total and not dry:
    bpy.ops.wm.save_mainfile()
