"""Epsilon+ rear-plate layer for the turntables (v0.10, owner: "put epsilon plates on all the rear of the cars").

blender -b --factory-startup -P render_plate.py -- <glb> <outdir> <hide,list> <plate.png> <z_centre> [N=48] [START] [END]
Same camera / lights / pivot as render_turntable.py. The car is a holdout, so each p_XX.png is an RGBA image of only the
visible part of the plate; the compositor lays it over the tinted car. The plate (US size 305 x 152 mm) is put on the rear
surface found by ray casts at z_centre (rear of these GLBs is +Y), tilted to that surface, 8 mm proud.
"""
import bpy, sys, math, os
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "blender")); import ive_gpu  # noqa: E402  (GPU when present, else CPU)
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
GLB, OUT, HIDE, TEX, ZC = a[0], a[1], a[2].split(','), a[3], float(a[4])
N = int(a[5]) if len(a) > 5 else 48; START = int(a[6]) if len(a) > 6 else 0; END = int(a[7]) if len(a) > 7 else N
os.makedirs(OUT, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; ive_gpu.use(sc); sc.cycles.samples = 16; sc.cycles.use_denoising = False
sc.render.resolution_x, sc.render.resolution_y = 720, 420
sc.render.use_persistent_data = True; sc.render.film_transparent = True
sc.render.image_settings.color_mode = 'RGBA'; sc.view_settings.view_transform = 'Standard'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)
bpy.ops.import_scene.gltf(filepath=GLB)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
for o in meshes:
    if o.name.split('.')[0] in HIDE: o.hide_render = True; o.hide_viewport = True
bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
def hit(x, z):
    ok, loc, *_ = sc.ray_cast(dg, Vector((x, 6.0, z)), Vector((0, -1, 0)))
    return loc.y if ok else None
PW, PH = 0.305, 0.152
top = [hit(x, ZC + PH * 0.4) for x in (-0.1, 0.1)]; bot = [hit(x, ZC - PH * 0.4) for x in (-0.1, 0.1)]
print('HITS', top, bot, flush=True)
yt, yb = max(top), max(bot); tilt = math.atan2(yt - yb, PH * 0.8)   # +tilt = top further back (leans away from the viewer)
yc = (yt + yb) / 2 + 0.008
if tilt > 0: tilt = 0.0; yc = max(yt, yb) + 0.006      # recess with an overhanging top edge (Civic hatch): hang the plate vertical
tilt = max(tilt, math.radians(-20))
print('PLATE y', round(yc, 3), 'tilt deg', round(math.degrees(tilt), 1), flush=True)
me = bpy.data.meshes.new('plate'); hw, hh = PW / 2, PH / 2
dy = math.sin(tilt) * hh; dz = math.cos(tilt) * hh
me.from_pydata([(hw, yc - dy, ZC - dz), (-hw, yc - dy, ZC - dz), (-hw, yc + dy, ZC + dz), (hw, yc + dy, ZC + dz)], [], [(0, 1, 2, 3)])
uv = me.uv_layers.new(name='uv')
for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = c   # +X is the viewer's left from behind
pl = bpy.data.objects.new('plate', me); sc.collection.objects.link(pl)
pm = bpy.data.materials.new('plate'); pm.use_nodes = True; nt = pm.node_tree; bs = nt.nodes['Principled BSDF']
tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(TEX)
nt.links.new(tx.outputs['Color'], bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = 0.35
try: nt.links.new(tx.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = 0.25   # keeps the wordmark legible in shade
except Exception: pass
pl.data.materials.append(pm)
ho = bpy.data.materials.new('holdout'); ho.use_nodes = True; nt = ho.node_tree; nt.nodes.clear()
h = nt.nodes.new('ShaderNodeHoldout'); o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(h.outputs[0], o_.inputs[0])
for o in meshes:
    for s in o.material_slots: s.material = ho
piv = bpy.data.objects.new('piv', None); sc.collection.objects.link(piv)
def area(loc, size, energy):
    bpy.ops.object.light_add(type='AREA', location=loc); l = bpy.context.object
    l.data.size = size; l.data.energy = energy; l.visible_camera = False
    l.rotation_euler = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); l.parent = piv
area((0, 0, 6.5), 7, 1100); area((5, 7, 4), 4, 700); area((-6, 4, 3), 4, 350)
cam = bpy.data.cameras.new('c'); cam.lens = 85; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (0, 12.6, 4.4); co.rotation_euler = (Vector((0, 0, 0.55)) - co.location).to_track_quat('-Z', 'Y').to_euler(); co.parent = piv
for k in range(START, END):
    f = os.path.join(OUT, f'p_{k:02d}.png')
    if os.path.exists(f): continue
    piv.rotation_euler = (0, 0, math.radians(35) + 2 * math.pi * k / N)
    sc.render.filepath = f; bpy.ops.render.render(write_still=True); print('ANGLE', k, flush=True)
