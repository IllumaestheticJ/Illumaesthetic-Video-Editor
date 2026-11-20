"""Visibility audit (the shots.vis bug): any object whose first hide_render key is after frame 1. blender -b --python visaudit.py -- <shot>"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr_shots as G
for n in [int(sys.argv[-1])]:
    bpy.ops.wm.read_factory_settings(use_empty=True); G.SHOTS[n - 1](); bad = []; nk = 0
    for o in bpy.data.objects:
        ad = o.animation_data
        if not ad or not ad.action: continue
        fcs = []
        try: fcs = list(ad.action.fcurves)
        except Exception:
            for l in ad.action.layers:
                for s in l.strips:
                    for cb in s.channelbags: fcs += list(cb.fcurves)
        for fc in fcs:
            if fc.data_path == "hide_render":
                nk += 1; f0 = min(k.co[0] for k in fc.keyframe_points)
                if f0 > 1: bad.append((o.name, f0))
    print("VIS", n, "keyed objects", nk, "first key after frame 1:", bad)
