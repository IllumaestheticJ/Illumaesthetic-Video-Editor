"""Turntable passes for the dealership-menu version (v0.2).

blender -b --factory-startup -P render_turntable.py -- <glb> <outdir> <hide,comma,list> [n_angles]
Per angle writes: b_XX.png (paint = black gloss), w_XX.png (paint = white gloss), m_XX.png (R = body paint, G = sport wing, B = lip kit / flares).
Compositing tints: out = b + mask * (w - b) * colour, so every store colour comes from two beauty passes.
Camera and lights orbit together, which looks like the car turning on a fixed stage.
"""
import bpy, sys, math, os
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
GLB, OUT, HIDE = a[0], a[1], a[2].split(',')
N = int(a[3]) if len(a) > 3 else 48
os.makedirs(OUT, exist_ok=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 10; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 720, 420
sc.render.use_persistent_data = True
sc.view_settings.view_transform = 'Standard'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)
bpy.ops.import_scene.gltf(filepath=GLB)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
for o in meshes:
    if o.name.split('.')[0] in HIDE: o.hide_render = True
wing = [o for o in meshes if o.name.split('.')[0] == 'part_sport_wing']
KIT = a[6].split(',') if len(a) > 6 else []   # lip-kit parts: shown in their standard black finish, not body paint
kit = [o for o in meshes if o.name.split('.')[0] in KIT]
# stage floor: grey disc that falls off to black
bpy.ops.mesh.primitive_circle_add(vertices=96, radius=4.2, fill_type='NGON', location=(0, 0, 0.0))
fl = bpy.context.object; fm = bpy.data.materials.new('floor'); fm.use_nodes = True
nt = fm.node_tree; nt.nodes.clear()
geo = nt.nodes.new('ShaderNodeNewGeometry'); ln = nt.nodes.new('ShaderNodeVectorMath'); ln.operation = 'LENGTH'
ramp = nt.nodes.new('ShaderNodeMapRange'); ramp.inputs[1].default_value = 0.8; ramp.inputs[2].default_value = 3.6
ramp.inputs[3].default_value = 0.035; ramp.inputs[4].default_value = 0.0
dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); outn = nt.nodes.new('ShaderNodeOutputMaterial')
nt.links.new(geo.outputs['Position'], ln.inputs[0]); nt.links.new(ln.outputs['Value'], ramp.inputs[0])
nt.links.new(ramp.outputs[0], dif.inputs[0]); nt.links.new(dif.outputs[0], outn.inputs[0])
fl.data.materials.append(fm)
piv = bpy.data.objects.new('piv', None); sc.collection.objects.link(piv)
def area(loc, size, energy):
    bpy.ops.object.light_add(type='AREA', location=loc); l = bpy.context.object
    l.data.size = size; l.data.energy = energy; l.visible_camera = False
    l.rotation_euler = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); l.parent = piv
area((0, 0, 6.5), 7, 1100); area((5, 7, 4), 4, 700); area((-6, 4, 3), 4, 350)
cam = bpy.data.cameras.new('c'); cam.lens = 85; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (0, 12.6, 4.4); co.rotation_euler = (Vector((0, 0, 0.55)) - co.location).to_track_quat('-Z', 'Y').to_euler(); co.parent = piv

def gloss(name, v):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (v, v, v, 1); b.inputs['Roughness'].default_value = 0.3
    try: b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = 0.05
    except Exception: pass
    return m
def emit(col):
    m = bpy.data.materials.new('e'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*col, 1)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); return m
slots = [(o, i, s.material) for o in meshes + [fl] for i, s in enumerate(o.material_slots)]
def is_paint(m): return m is not None and m.name.split('.')[0] == 'paint'
def assign(paintmat, wingmat, other=None):
    for o, i, m in slots:
        if is_paint(m) and o in kit: o.material_slots[i].material = eB if other else paintmat   # v0.6: kit is paint-matched; mask channel B
        elif is_paint(m): o.material_slots[i].material = wingmat if o in wing else paintmat
        else: o.material_slots[i].material = other if other else m
B, Wm = gloss('pb', 0.0), gloss('pw', 0.8)
KITMAT = gloss('kit', 0.012); KITMAT.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.42
START = int(a[4]) if len(a) > 4 else 0
eR, eG, eK, eB = emit((1, 0, 0)), emit((0, 1, 0)), emit((0, 0, 0)), emit((0, 0, 1))
PASSES = a[7] if len(a) > 7 else 'bwm'
END = int(a[5]) if len(a) > 5 else N   # N is always the full turn; START/END select a chunk
for k in range(START, END):
    if all(os.path.exists(os.path.join(OUT, f'{t}_{k:02d}.png')) for t in PASSES): continue   # resume after a restart
    piv.rotation_euler = (0, 0, math.radians(35) + 2 * math.pi * k / N)
    for tag, args, smp in (('b', (B, B), 10), ('w', (Wm, Wm), 10), ('m', (eR, eG, eK), 1)):
        if tag not in PASSES: continue
        assign(*args); sc.cycles.samples = smp; sc.cycles.use_denoising = tag != 'm'
        sc.render.filepath = os.path.join(OUT, f'{tag}_{k:02d}.png'); bpy.ops.render.render(write_still=True)
    print('ANGLE', k, flush=True)
