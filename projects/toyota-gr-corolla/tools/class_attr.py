"""Per-face surface classes (+ optional livery colours) into a prepped .blend: material slots named 'cls_<class>' and
polygon material_index from a class array; colours go to the FACE attribute 'livery'. shot.py swaps every 'cls_*' slot
for its real shader (game-model look: glass, lights, chrome, plastics, rubber...). Checks face order against the STL.
    blender -b in.blend -P class_attr.py -- src.stl class.npy names_csv out.blend [colors.npy] [alpha.npy]"""
import sys
import bpy
import numpy as np
a = sys.argv[sys.argv.index("--") + 1:]; stl, clsp, names, out = a[:4]; colp = a[4] if len(a) > 4 else None
alphap = a[5] if len(a) > 5 else None   # livery alpha = graphics mask (1 = decal/colour, 0 = white base)
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
names = names.split(","); cls = np.load(clsp).astype(np.int32)
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; me = o.data
assert len(me.polygons) == len(cls), (len(me.polygons), len(cls))
src = np.fromfile(stl, dtype=DT, offset=84)["v"].mean(1).astype(float) / 1000 + ROOT
cen = np.zeros(len(me.polygons) * 3, np.float32); me.polygons.foreach_get("center", cen); cen = cen.reshape(-1, 3)
M = np.array(o.matrix_world); cen = cen @ M[:3, :3].T + M[:3, 3]
idx = np.linspace(0, len(cen) - 1, 2000).astype(int); err = np.linalg.norm(cen[idx] - src[idx], axis=1).max()
print("CLASS face-order check (m):", err); assert err < 1e-3
me.materials.clear()
for n in names:
    me.materials.append(bpy.data.materials.get("cls_" + n) or bpy.data.materials.new("cls_" + n))
me.polygons.foreach_set("material_index", cls)
if colp:
    col = np.load(colp).astype(np.float32) / 255.0
    rgba = np.ones((len(col), 4), np.float32); rgba[:, :3] = col ** 2.2
    if alphap:
        rgba[:, 3] = np.load(alphap)
    attr = me.attributes.new("livery", "FLOAT_COLOR", "FACE"); attr.data.foreach_set("color", rgba.ravel())
me.update()
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("CLASS saved", out, np.bincount(cls, minlength=len(names)).tolist())
