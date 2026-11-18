"""Hero-part falls (v0.2). Owner on v0: "I don't want the parts to 'home' onto the car - it needs to naturally fall on the
car as if that was the entire plan".

A part keeps its final orientation the whole way (no tumble, no straightening) and falls along ONE straight line with
constant speed (v0.6; was gravity from rest), from outside the frame, landing exactly on its seat on the beat. The line is the steepest
one (vertical first, then tilted outward in 5 deg steps toward `side`) along which the part never comes within 5 mm of the
scan - the lip and skirts tuck under the body, so a pure vertical drop can pass through it. Keys on every frame, LINEAR.
"""
import math
import bpy
import numpy as np
from mathutils import Vector, kdtree
from bpy_extras.object_utils import world_to_camera_view

_CAR = {}
V_RAIN = 10.0   # m/s, constant fall speed for the hero parts (v0.6)


def _car_tree(car, lo, hi):
    key = (tuple(np.round(lo, 1)), tuple(np.round(hi, 1)))
    if key in _CAR:
        return _CAR[key]
    n = len(car.data.vertices); co = np.empty(n * 3, np.float32); car.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    m = np.all((co > lo) & (co < hi), 1); pts = co[m]
    kd = kdtree.KDTree(len(pts))
    for i, p in enumerate(pts):
        kd.insert(p, i)
    kd.balance(); _CAR[key] = kd
    return kd


def _hits(kd, P, off, tol=0.005):
    return sum(1 for p in P if kd.find(Vector(p + off))[2] < tol)


def animate(sc, ob, car, f_seat, side, f_last, fps=30, name=None):
    """the fall line comes from kit/fall_dirs.json (tools/fall_dirs.py, scipy - the in-Blender search was too slow)"""
    import json
    fd = json.load(open("/home/user/media/bf-civic-parts-rain/kit/fall_dirs.json"))[name or ob.name]
    e, worst, d = fd["elev_deg"], fd["hits_on_path"], np.array(fd["dir"])
    n = len(ob.data.vertices); co = np.empty(n * 3, np.float32); ob.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    # start: from rest, outside the frame at the moment the fall begins
    cam = sc.camera; corners = [Vector(c) for c in (co.min(0), co.max(0))]
    bb = [Vector((x, y, z)) for x in (corners[0].x, corners[1].x) for y in (corners[0].y, corners[1].y) for z in (corners[0].z, corners[1].z)]
    # v0.6 (owner: "fall at constant speed so it looks like natural rain"): no acceleration, one constant speed per part,
    # at least v_min so the last frame before landing still clears the body
    v = max(fd.get("v_min", 0), V_RAIN)
    L = 3.0
    while True:
        nfr = max(8, math.floor(L / v * fps)); f0 = f_seat - nfr   # floor: actual speed never drops below v_min
        sc.frame_set(max(f0, 0)); off = Vector(d * L)
        vis = False
        for c in bb:
            uv = world_to_camera_view(sc, cam, c + off)
            if uv.z > 0 and -0.02 < uv.x < 1.02 and -0.02 < uv.y < 1.02:
                vis = True; break
        if not vis or L > 30:
            break
        L += 0.5
    L = max(L, v * nfr / fps)   # the 8-frame minimum must not slow the part below v
    v = L / (nfr / fps)   # exact speed for the whole-frame count
    pref = bpy.context.preferences.edit; old = pref.keyframe_new_interpolation_type; pref.keyframe_new_interpolation_type = "LINEAR"
    park = Vector((0, 0, 60))
    for f in range(0, f_last + 1):
        if f < f0:
            ob.location = park
        elif f < f_seat:
            t = (f - f0) / fps; rem = L - v * t
            ob.location = Vector(d * rem)
        else:
            ob.location = Vector((0, 0, 0))
        ob.keyframe_insert("location", frame=f)
    pref.keyframe_new_interpolation_type = old
    sc.frame_set(0)
    prev = v / fps
    return {"prev_frame_dist_m": round(prev, 3), "contact_extent_m": fd.get("contact_extent_m"), "elev_deg": e, "hits_on_path": worst, "start_dist_m": round(L, 2), "fall_s": round(nfr / fps, 2),
            "speed_mps": round(v, 1)}
