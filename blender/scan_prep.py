"""Import raw scan data into a normalized Blender scene.

Run either way:
    blender -b -P blender/scan_prep.py -- --scan car.stl --out work/scene.blend
    python blender/scan_prep.py --scan car.stl --out work/scene.blend      # with `pip install bpy`

Normalization (recorded in <out>.json so every later step uses the same space):
  * unit detection: scans exported in millimetres are scaled to metres
  * optional decimation (raw scans are often 5-50M tris; renders rarely need >3M)
  * the scan is centered on X/Y and sat on the Z=0 floor, +Y forward is NOT assumed
All match-cut landmark coordinates (`xyz` in matchpoints.json) must be taken from
THIS normalized scene, never from the raw file.
"""
import argparse
import json
import os
import sys

import bpy
from mathutils import Vector

IMPORTERS = {
    ".stl": lambda p: bpy.ops.wm.stl_import(filepath=p),
    ".obj": lambda p: bpy.ops.wm.obj_import(filepath=p),
    ".ply": lambda p: bpy.ops.wm.ply_import(filepath=p),
    ".fbx": lambda p: bpy.ops.import_scene.fbx(filepath=p),
    ".glb": lambda p: bpy.ops.import_scene.gltf(filepath=p),
    ".gltf": lambda p: bpy.ops.import_scene.gltf(filepath=p),
}


def argv():
    a = sys.argv
    return a[a.index("--") + 1:] if "--" in a else a[1:]


def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", required=True, nargs="+", help="one or more scan files (.stl .obj .ply .fbx .glb .blend)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--units", choices=["auto", "m", "mm", "cm", "in"], default="auto")
    ap.add_argument("--decimate", type=float, default=1.0, help="collapse ratio, e.g. 0.2 keeps 20%% of faces")
    ap.add_argument("--max-faces", type=int, default=0, help="auto-decimate to at most this many faces")
    ap.add_argument("--no-center", action="store_true", help="keep original placement (e.g. scans pre-aligned to a car model)")
    ap.add_argument("--like", help="reuse unit scale + offset from another prep's .json so separately-scanned states line up")
    ap.add_argument("--floor-cut", type=float, default=0.0, help="delete geometry below this height (m) after normalising - removes scanned ground scraps")
    ap.add_argument("--drop-islands", type=int, default=0, help="delete disconnected pieces with fewer faces than this (scan debris, ground paint)")
    ap.add_argument("--smooth", action="store_true", help="shade smooth (good for clay; keep flat for raw-scan look)")
    return ap.parse_args(argv())


def import_any(path):
    before = set(bpy.data.objects)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".blend":
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.objects = [n for n in src.objects]
        for o in dst.objects:
            if o is not None and o.type == "MESH":
                bpy.context.scene.collection.objects.link(o)
    elif ext in IMPORTERS:
        IMPORTERS[ext](path)
    else:
        raise SystemExit(f"Unsupported scan format: {ext}")
    return [o for o in bpy.data.objects if o not in before and o.type == "MESH"]


def world_bbox(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def main():
    args = parse()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = []
    for s in args.scan:
        objs += import_any(os.path.abspath(s))
    if not objs:
        raise SystemExit("No mesh objects imported.")

    root = bpy.data.objects.new("SCAN_ROOT", None)
    bpy.context.scene.collection.objects.link(root)
    for o in objs:
        o.parent = root
        o["ive_scan"] = True

    lo, hi = world_bbox(objs)
    extent = max(hi - lo)
    like = json.load(open(args.like)) if args.like else None
    scale = {"m": 1.0, "mm": 0.001, "cm": 0.01, "in": 0.0254}.get(args.units)
    if like:
        scale = like["unit_scale"]
    if scale is None:  # auto: anything larger than 50 units is almost certainly millimetres
        scale = 0.001 if extent > 50 else 1.0
    root.scale = (scale, scale, scale)
    bpy.context.view_layer.update()

    if like:
        root.location = like["root_location"]
        bpy.context.view_layer.update()
    elif not args.no_center:
        lo, hi = world_bbox(objs)
        c = (lo + hi) / 2
        root.location = (-c.x, -c.y, -lo.z)
        bpy.context.view_layer.update()

    faces = sum(len(o.data.polygons) for o in objs)
    ratio = args.decimate
    if args.max_faces and faces > args.max_faces:
        ratio = min(ratio, args.max_faces / faces)
    if ratio < 1.0:
        for o in objs:
            m = o.modifiers.new("ive_decimate", "DECIMATE")
            m.ratio = ratio
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.modifier_apply(modifier=m.name)
    if args.floor_cut > 0:
        import bmesh
        for o in objs:
            bm = bmesh.new()
            bm.from_mesh(o.data)
            mw = o.matrix_world
            kill = [v for v in bm.verts if (mw @ v.co).z < args.floor_cut]
            bmesh.ops.delete(bm, geom=kill, context="VERTS")
            bm.to_mesh(o.data)
            bm.free()
        bpy.context.view_layer.update()
    if args.drop_islands:
        bpy.ops.object.select_all(action="DESELECT")
        for o in list(objs):
            bpy.context.view_layer.objects.active = o
            o.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.remove_doubles(threshold=0.0005)
            bpy.ops.mesh.separate(type="LOOSE")
            bpy.ops.object.mode_set(mode="OBJECT")
        parts = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.get("ive_scan")]
        kept = []
        for o in parts:
            zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
            flat_on_floor = max(zs) < 0.15  # islands that never rise above 15 cm: paint, wheel stops, debris
            if len(o.data.polygons) < args.drop_islands or flat_on_floor:
                bpy.data.objects.remove(o, do_unlink=True)
            else:
                kept.append(o)
        bpy.ops.object.select_all(action="DESELECT")
        for o in kept:
            o.select_set(True)
        bpy.context.view_layer.objects.active = kept[0]
        if len(kept) > 1:
            bpy.ops.object.join()
        objs = [bpy.context.view_layer.objects.active]
    for o in objs:
        for p in o.data.polygons:
            p.use_smooth = args.smooth

    lo, hi = world_bbox(objs)
    meta = {
        "sources": [os.path.abspath(s) for s in args.scan],
        "unit_scale": scale,
        "root_location": list(root.location),
        "faces_in": faces,
        "faces_out": sum(len(o.data.polygons) for o in objs),
        "bbox_min": list(lo),
        "bbox_max": list(hi),
        "objects": [o.name for o in objs],
        "has_color_attribute": any(len(o.data.color_attributes) for o in objs),
        "has_uv_texture": any(len(o.data.uv_layers) and o.active_material for o in objs),
    }
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    with open(os.path.splitext(out)[0] + ".json", "w") as f:
        json.dump(meta, f, indent=2)
    print("IVE_PREP", json.dumps(meta))


if __name__ == "__main__":
    main()
