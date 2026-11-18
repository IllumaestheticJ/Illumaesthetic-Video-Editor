"""Real section shot: NA1 NSX bumper scan (mesh + visible triangles) -> STEP NURBS patches -> colour deviation map.

blender -b -P render_real.py -- DATA_DIR OUT_DIR [--frames 0-131] [--res-pct 100] [--samples 48]
DATA_DIR holds scan_crop.ply and step.ply from prep_real.py (metres, front of bumper toward -Y).
Timeline (30 fps, 132 frames = 4.4 s): 0-53 scan + triangle wire; 54-89 left-to-right sweep scan -> STEP patches;
90-131 STEP patches -> deviation colours (green = on the scan, red = furthest; no legend, no numbers).
House silver look and studio world/lights come from blender/scan_render.py.
"""
import sys, math
from pathlib import Path
import bpy
from mathutils import Vector

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "blender"))
import scan_render as sr  # noqa: E402

A = sys.argv[sys.argv.index("--") + 1:]
DATA, OUT = Path(A[0]), Path(A[1])
def opt(n, d): return A[A.index(n) + 1] if n in A else d
F0, F1 = [int(v) for v in opt("--frames", "0-131").split("-")]
SWEEP0, SWEEP1, DEV0, DEV1 = 54, 89, 90, 108
X_LO, X_HI = -0.95, 0.95

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def imp(p, name):
    bpy.ops.wm.ply_import(filepath=str(p))
    o = bpy.context.selected_objects[0]; o.name = name
    return o


scan = imp(DATA / "scan_crop.ply", "SCAN_ROOT")
step = imp(DATA / "step.ply", "STEP")
for o in (scan, step):
    o.data.shade_flat() if o is scan else o.data.shade_smooth()

# visible triangles: a decimated copy of the real scan, drawn as thin cyan wire just above the surface
wire = imp(DATA / "scan_wire.ply", "WIRE")
wm = wire.modifiers.new("wire", "WIREFRAME"); wm.thickness = 0.0011; wm.use_replace = True; wm.offset = 1.0

thr = None  # shared sweep threshold driver value


def sweep_value_node(nt):
    v = nt.nodes.new("ShaderNodeValue"); v.label = "sweep"
    v.outputs[0].default_value = X_LO
    v.outputs[0].keyframe_insert("default_value", frame=SWEEP0)
    v.outputs[0].default_value = X_HI
    v.outputs[0].keyframe_insert("default_value", frame=SWEEP1)
    return v


def cut_by_x(m, keep_left):
    """Wrap material m: transparent on one side of the animated x threshold (object-space x)."""
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    src = out.inputs[0].links[0].from_socket
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    cmp = nt.nodes.new("ShaderNodeMath"); cmp.operation = "LESS_THAN"
    nt.links.new(sep.outputs["X"], cmp.inputs[0]); nt.links.new(sweep_value_node(nt).outputs[0], cmp.inputs[1])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(cmp.outputs[0], mix.inputs[0])
    # fac=1 where x < threshold: STEP visible there (keep_left), scan hidden there
    nt.links.new(src if keep_left else tr.outputs[0], mix.inputs[2])
    nt.links.new(tr.outputs[0] if keep_left else src, mix.inputs[1])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.blend_method = "HASHED" if hasattr(m, "blend_method") else None


# scan: house silver
ms = sr.mat_silver(); scan.data.materials.append(ms); cut_by_x(ms, keep_left=False)
# wire: cyan emission
mw, nt, out = sr.new_mat("wire"); e = sr.emission(nt, (0.0, 0.85, 1.0, 1), 1.8); nt.links.new(e.outputs[0], out.inputs[0])
wire.data.materials.append(mw); cut_by_x(mw, keep_left=False)
# STEP: silver tinted per NURBS patch (vertex colour B), then mixed to the deviation colour (R,G)
m, nt, out = sr.new_mat("step")
attr = nt.nodes.new("ShaderNodeVertexColor"); attr.layer_name = "Col"
sep = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(attr.outputs["Color"], sep.inputs[0])
tint = nt.nodes.new("ShaderNodeMapRange"); tint.inputs[3].default_value = 0.42; tint.inputs[4].default_value = 0.82
nt.links.new(sep.outputs[2], tint.inputs[0])
patch = nt.nodes.new("ShaderNodeCombineColor")
for k in range(3):
    nt.links.new(tint.outputs[0], patch.inputs[k])
devc = nt.nodes.new("ShaderNodeCombineColor"); nt.links.new(sep.outputs[0], devc.inputs[0]); nt.links.new(sep.outputs[1], devc.inputs[1])
mixc = nt.nodes.new("ShaderNodeMix"); mixc.data_type = "RGBA"
nt.links.new(patch.outputs[0], mixc.inputs["A"]); nt.links.new(devc.outputs[0], mixc.inputs["B"])
fac = mixc.inputs["Factor"]
fac.default_value = 0.0; fac.keyframe_insert("default_value", frame=DEV0)
fac.default_value = 1.0; fac.keyframe_insert("default_value", frame=DEV1)
p = sr.principled(nt, (0.6, 0.6, 0.6, 1), 0.35, 0.55)
nt.links.new(mixc.outputs["Result"], p.inputs["Base Color"])
nt.links.new(p.outputs[0], out.inputs[0])
step.data.materials.append(m); cut_by_x(m, keep_left=True)

lo = Vector(min(v.co[i] for v in step.data.vertices) for i in range(3)) if False else None
co = [step.matrix_world @ v.co for v in step.data.vertices]
lo = Vector((min(c.x for c in co), min(c.y for c in co), min(c.z for c in co)))
hi = Vector((max(c.x for c in co), max(c.y for c in co), max(c.z for c in co)))
sr.studio_world((0.004, 0.004, 0.005, 1), False)
sr.studio_lights(lo, hi)

# camera: 9:16, 3/4 front view of the left half, slow 14 degree orbit
cd = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.lens = 30; cd.sensor_fit = "VERTICAL"; cd.sensor_height = 36
piv = Vector((-0.50, -0.26, 0.07))
R, H = 1.0, 0.55
for f, ang in ((0, -74.0), (131, -58.0)):
    a = math.radians(ang)
    cam.location = piv + Vector((R * math.cos(a), R * math.sin(a), H))
    cam.rotation_euler = (piv - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)

r = sc.render
r.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(opt("--samples", "48")); sc.cycles.use_denoising = True
r.resolution_x, r.resolution_y = 1080, 1920; r.resolution_percentage = int(opt("--res-pct", "100"))
r.fps = 30; sc.frame_start, sc.frame_end = F0, F1
r.image_settings.file_format = "PNG"; r.filepath = str(OUT / "f_")
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.render.render(animation=True)
