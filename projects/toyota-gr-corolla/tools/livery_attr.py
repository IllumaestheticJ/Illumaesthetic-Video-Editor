"""Write livery.py's per-face colours into the prepped car .blend as a FACE colour attribute 'livery'
(alpha 0 = no livery there -> the shot keeps the house silver). Checks face order against the source STL.
    blender -b car9nw.blend -P livery_attr.py -- car9nw.stl colors.npy out.blend"""
import sys
import bpy
import numpy as np
a = sys.argv[sys.argv.index("--") + 1:]; stl, colp, out = a
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.2036251425743103, 0.9911584854125977, 0.5780090689659119])
col = np.load(colp)
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; me = o.data
assert len(me.polygons) == len(col), (len(me.polygons), len(col))
src = np.fromfile(stl, dtype=DT, offset=84)["v"].mean(1).astype(float) / 1000 + ROOT
cen = np.zeros(len(me.polygons) * 3, np.float32); me.polygons.foreach_get("center", cen); cen = cen.reshape(-1, 3)
M = np.array(o.matrix_world); cen = cen @ M[:3, :3].T + M[:3, 3]
idx = np.linspace(0, len(cen) - 1, 2000).astype(int); err = np.linalg.norm(cen[idx] - src[idx], axis=1).max()
print("LIVERY face-order check, max centroid error (m):", err); assert err < 1e-3
rgba = np.zeros((len(col), 4), np.float32)
ok = col[:, 0] >= 0
rgba[ok, :3] = (col[ok] / 255.0) ** 2.2; rgba[ok, 3] = 1.0
attr = me.color_attributes.new("livery", "FLOAT_COLOR", "FACE")
attr.data.foreach_set("color", rgba.ravel())
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print("LIVERY saved", out, int(ok.sum()))
