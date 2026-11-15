"""Split the stock-wheel scan (one mesh, 4 wheels) into per-corner blends so each wheel can animate off on its own.
  blender -b -P split_wheels.py -- stock_wheels.blend out_dir xc"""
import bpy, bmesh, os, sys
import numpy as np
a = sys.argv[sys.argv.index("--") + 1:]; SRC, OUT, XC = a[0], a[1], float(a[2])
for k, (sx, sy) in {"fl": (1, -1), "fr": (-1, -1), "rl": (1, 1), "rr": (-1, 1)}.items():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    ob = [o for o in bpy.data.objects if o.type == "MESH"][0]; me = ob.data
    M = np.array(ob.matrix_world); n = len(me.polygons); c = np.empty(n * 3); me.polygons.foreach_get("center", c)
    c = c.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
    keep = ((c[:, 0] - XC) * sx > 0) & ((c[:, 1] - 0.06) * sy > 0)
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in np.where(~keep)[0]], context="FACES")
    bm.to_mesh(me); bm.free(); ob.name = f"stock_{k}"
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"stock_w_{k}.blend")); print("wrote", k, int(keep.sum()))
