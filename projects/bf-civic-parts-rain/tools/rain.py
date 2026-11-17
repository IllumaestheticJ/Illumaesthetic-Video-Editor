"""Screen-space rain (v0.2, owner on v0: "too many parts that clip in and out of the screen").

Every part falls straight down the FRAME: it enters fully above the top edge, falls inside the side margins, leaves fully
below the bottom edge, and only respawns while off screen. Positions are solved per frame from the camera (matrix, lens,
shift), so camera moves and zooms never carry a part across a side edge, and depth scales with the lens so a part keeps
its apparent size. Parts are only placed behind the car (keep-out box) so nothing passes through it.
Keys are written on EVERY frame with LINEAR interpolation: no in-between frame can show a respawn jump.
"""
import math, random
import bpy
from mathutils import Vector


def build(sc, srcs, n, f_end, depth=(8.0, 14.0), xr=0.58, fall=(3.2, 4.6), gap=(0.2, 1.4), y_edge=1.32,
          keep_out=None, t_last_end=None, seed=7, prefix="rain", start_mid=True, scale=1.0):
    """srcs: list of mesh datablocks (origin at their centre). depth: metres at a 35 mm-equivalent lens.
    xr: |screen x| limit as a fraction of the half-width. y_edge: spawn/despawn height in half-heights (>1 = off screen).
    keep_out: (lo, hi) world bbox the parts must never come within (already expanded). t_last_end: no fall may end later
    than this (s) - the rain is over before the cut."""
    cam = sc.camera; fps = sc.render.fps
    pref = bpy.context.preferences.edit; old = pref.keyframe_new_interpolation_type; pref.keyframe_new_interpolation_type = "LINEAR"
    C = []
    for f in range(f_end + 1):
        sc.frame_set(f); d = cam.data
        C.append((cam.matrix_world.copy(), d.lens, d.shift_x, d.shift_y))
    ar = sc.render.resolution_y / sc.render.resolution_x

    def world(f, x, y, D0):
        M, lens, sx, sy = C[f]; D = D0 * lens / 35.0; hw = D * 18.0 / lens
        return M @ Vector(((x + 2 * sx) * hw, (y * ar + 2 * sy) * hw, -D))

    rng = random.Random(seed); made = 0
    for i in range(n):
        for _try in range(40):
            x = rng.uniform(-xr, xr); D0 = rng.uniform(*depth); T = rng.uniform(*fall)
            t = -rng.uniform(0, T) if start_mid else rng.uniform(0, 1.5)
            falls = []
            while True:
                if t + T > (t_last_end if t_last_end is not None else f_end / fps + T):
                    break
                falls.append(t); t += T + rng.uniform(*gap)
            ok = bool(falls)
            if ok and keep_out:
                lo, hi = keep_out
                for f in range(0, f_end + 1, 2):
                    tt = f / fps
                    for t0 in falls:
                        if t0 <= tt <= t0 + T:
                            p = world(f, x, y_edge - 2 * y_edge * (tt - t0) / T, D0)
                            if all(lo[k] < p[k] < hi[k] for k in range(3)):
                                ok = False; break
                    if not ok:
                        break
            if ok:
                break
        if not ok:
            continue
        ob = bpy.data.objects.new(f"{prefix}{i}", srcs[i % len(srcs)]); sc.collection.objects.link(ob); made += 1
        ob.scale = (scale, scale, scale)   # v0.4: owner 'parts are bigger'
        spin = Vector((rng.uniform(-1.2, 1.2), rng.uniform(-1.2, 1.2), rng.uniform(-2.0, 2.0)))
        rock = rng.uniform(0.35, 0.8); sway = rng.uniform(0.01, 0.03); ph = rng.uniform(0, 6.28)
        for f in range(f_end + 1):
            tt = f / fps; y = None
            for t0 in falls:
                if t0 <= tt <= t0 + T:
                    y = y_edge - 2 * y_edge * (tt - t0) / T; break
            if y is None:                       # between falls: parked above the frame
                y = y_edge + 0.6
            ob.location = world(f, x + sway * math.sin(2.1 * tt + ph), y, D0)
            ob.rotation_euler = (rock * math.sin(2.9 * tt + ph) + spin.x * tt * 0.3, rock * math.cos(2.5 * tt + 2 * ph) + spin.y * tt * 0.3, spin.z * tt)
            ob.keyframe_insert("location", frame=f); ob.keyframe_insert("rotation_euler", frame=f)
    pref.keyframe_new_interpolation_type = old
    sc.frame_set(0)
    return made
