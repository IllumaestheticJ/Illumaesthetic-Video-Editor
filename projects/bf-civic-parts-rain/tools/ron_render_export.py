"""Blender (run on Ron's 'Honda Civic Sedan 2022-render.blend'): write wing.002 (world, m) as npy tris + Camera.006 and render settings to json."""
import bpy, json, numpy as np
O = "/home/user/media/bf-civic-parts-rain/kit"
dg = bpy.context.evaluated_depsgraph_get()
def tris(name):
    o = bpy.data.objects[name].evaluated_get(dg); me = o.to_mesh(); me.calc_loop_triangles()
    v = np.array([v.co[:] for v in me.vertices]); M = np.array(o.matrix_world)
    w = v @ M[:3, :3].T + M[:3, 3]; t = np.array([lt.vertices[:] for lt in me.loop_triangles])
    return w[t]
np.save(f"{O}/ron_wing002.npy", tris("wing.002").astype(np.float32))
c = bpy.data.objects["Camera.006(L5)"]; s = bpy.context.scene
json.dump({"matrix_world": [list(r) for r in c.matrix_world], "lens": c.data.lens, "sensor_width": c.data.sensor_width,
           "sensor_fit": c.data.sensor_fit, "shift_x": c.data.shift_x, "shift_y": c.data.shift_y,
           "res": [s.render.resolution_x, s.render.resolution_y]}, open(f"{O}/ron_cam006.json", "w"), indent=1)
print("EXPORTED", np.load(f"{O}/ron_wing002.npy").shape)
