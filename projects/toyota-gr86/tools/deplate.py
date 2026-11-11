"""Make the rear licence plate unreadable (lessons.md [text]/[story]: flatten the plate, don't blur the video).
The BRZ scan carries a legible plate in car4 and rear_bumper (NOT comp_explode: its base is the rear-bumper-removed state,
so the box only holds the crash beam - never run this on it). Box from an orthographic depth map of the tail
(rear_bumper, Blender frame, 1 mm/px): plate face x -0.055..0.235, z 0.595..0.730, rearmost surface y > 1.9.
Fits a robust plane to the plate face and projects every vertex within 10 mm of it onto the plane, so the embossed
characters flatten while the recess, frame and bumper around them stay as scanned. Saves the blend in place
(the caller keeps a .orig copy).
  blender -b X.blend -P deplate.py"""
import bpy, numpy as np

BOX = (-0.055, 0.235, 1.90, 2.20, 0.595, 0.730)
for o in bpy.data.objects:
    if o.type != "MESH":
        continue
    me = o.data
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get("co", v); v = v.reshape(-1, 3)
    M = np.array(o.matrix_world); w = v @ M[:3, :3].T + M[:3, 3]
    b = BOX
    sel = np.where((w[:, 0] > b[0]) & (w[:, 0] < b[1]) & (w[:, 1] > b[2]) & (w[:, 1] < b[3]) & (w[:, 2] > b[4]) & (w[:, 2] < b[5]))[0]
    if len(sel) < 200:
        print("DEPLATE", o.name, "no plate", len(sel)); continue
    P = w[sel]
    # plate face = the dominant sheet near the rearmost surface; iterate plane on inliers
    cen = np.array([np.median(P[:, 0]), np.percentile(P[:, 1], 70), np.median(P[:, 2])]); n = np.array([0, 1.0, 0])
    inl = np.abs((P - cen) @ n) < 0.02
    for tol in (0.015, 0.012, 0.010, 0.010):
        Q = P[inl]; cen = Q.mean(0); n = np.linalg.svd(Q - cen, full_matrices=False)[2][2]
        if n[1] < 0: n = -n
        inl = np.abs((P - cen) @ n) < tol
    d = (P - cen) @ n
    spread = np.percentile(np.abs(d[inl]), 95)
    w2 = w.copy(); w2[sel[inl]] = P[inl] - d[inl][:, None] * n
    loc = (w2 - M[:3, 3]) @ np.linalg.inv(M[:3, :3]).T
    me.vertices.foreach_set("co", loc.ravel()); me.update()
    print("DEPLATE", o.name, "moved", int(inl.sum()), "verts; centre", cen.round(3), "normal", n.round(3), "95% |d| before", round(spread * 1000, 1), "mm")
bpy.ops.wm.save_mainfile()
