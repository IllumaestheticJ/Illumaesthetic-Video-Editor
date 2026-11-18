"""turkey.py : a cute, stylised low-poly cartoon turkey built procedurally in Blender (no third-party model, no licence).

build_turkey(collection) -> dict of rig handles (empties) to animate:
  root  : position on the road + heading (local front = -Y, up = +Z)
  body  : waddle roll / bob / puff scale
  head  : neck-base pivot (yaw / tilt)
  eye_l, eye_r : eye pivots (scale z for blinks, uniform for 'huge eyes')
  leg_l, leg_r : hip pivots (pitch swing)
  tail  : tail-fan pivot (wobble / spread)
Sizes in metres: about 0.85 m to the top of the tail fan, head at ~0.9 m.
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix, Euler


def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1,)


_M = {}


def toon(name, hexcol, rough=0.6, emit=0.0, spec=0.3):
    if name in _M:
        return _M[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
    c = srgb(hexcol); p.inputs['Base Color'].default_value = c; p.inputs['Roughness'].default_value = rough
    p.inputs['Specular IOR Level'].default_value = spec
    if emit:
        p.inputs['Emission Color'].default_value = c; p.inputs['Emission Strength'].default_value = emit
    _M[name] = m
    return m


def _obj(name, mesh, coll, mat, parent, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), smooth=False):
    o = bpy.data.objects.new(name, mesh); coll.objects.link(o)
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = smooth
    o.parent = parent; o.location = loc; o.rotation_euler = rot; o.scale = scale
    return o


def _sphere(name, seg=10, rings=7):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0); bm.to_mesh(me); bm.free(); return me


def _ico(name, sub=1):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0); bm.to_mesh(me); bm.free(); return me


def _cone(name, r1, r2, d, seg=8):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r1, radius2=r2, depth=d)
    bm.to_mesh(me); bm.free(); return me


def feather_mesh(name='feather'):
    """A single flat, leaf-shaped feather: length 1 along +Z from the origin (quill end), width ~0.32, thin."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    prof = [(0.0, 0.0), (0.10, 0.12), (0.16, 0.35), (0.16, 0.65), (0.11, 0.88), (0.0, 1.0)]
    top, bot = [], []
    for s in (1, -1):
        for x, z in prof[1:-1]:
            pass
    ring = [(x, z) for x, z in prof] + [(-x, z) for x, z in reversed(prof[1:-1])]
    vf = [bm.verts.new((x, 0.02, z)) for x, z in ring]
    vb = [bm.verts.new((x, -0.02, z)) for x, z in ring]
    bm.faces.new(vf); bm.faces.new(list(reversed(vb)))
    n = len(ring)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((vf[i], vb[i], vb[j], vf[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free(); return me


TAIL_COLS = ['#9a4520', '#d9772f', '#efb257', '#d9772f', '#9a4520']


def build_turkey(coll, name='TURKEY'):
    E = lambda n, parent=None, loc=(0, 0, 0): _empty(coll, f'{name}_{n}', parent, loc)
    root = E('root')
    body = E('body', root, (0, 0, 0.0))
    brown = toon('t_brown', '#7a4a2a', 0.7); dark = toon('t_dark', '#4a2a18', 0.7); chest = toon('t_chest', '#8c5a34', 0.7)
    skin = toon('t_head', '#e9c9ae', 0.55); red = toon('t_red', '#d8322e', 0.45); beak = toon('t_beak', '#f4ad2f', 0.45)
    white = toon('t_eyewhite', '#ffffff', 0.25, emit=0.15); black = toon('t_pupil', '#121212', 0.15, spec=0.8)
    orange = toon('t_leg', '#f08a24', 0.5); cream = toon('t_cream', '#f2dcae', 0.6)
    # body: chubby egg, chest bulge forward
    _obj(f'{name}_torso', _sphere('torso', 12, 8), coll, brown, body, (0, 0.02, 0.44), scale=(0.30, 0.36, 0.29))
    _obj(f'{name}_chest', _sphere('chest', 10, 7), coll, chest, body, (0, -0.15, 0.42), scale=(0.24, 0.22, 0.24))
    for s in (1, -1):   # wings
        _obj(f'{name}_wing{s}', _sphere('wing', 9, 6), coll, dark, body, (s * 0.25, 0.05, 0.46),
             rot=(math.radians(-15), 0, math.radians(s * 8)), scale=(0.07, 0.26, 0.17))
    # tail fan: pivot at the back of the body, feathers fanned in the XZ plane, tipped back a little
    tail = E('tail', body, (0, 0.24, 0.48))
    fm = feather_mesh('tailfeather')
    nf = 11
    for i in range(nf):
        a = math.radians(-78 + 156 * i / (nf - 1))
        col = TAIL_COLS[i % len(TAIL_COLS)]
        piv = E(f'tf{i}', tail, (0, 0, 0)); piv.rotation_euler = (math.radians(-10), a, 0)
        _obj(f'{name}_tailf{i}', fm, coll, toon(f't_tail{col}', col, 0.65), piv, (0, 0.01 * (i % 2), 0.05), scale=(0.78, 1.0, 0.64))
        _obj(f'{name}_tailtip{i}', fm, coll, cream, piv, (0, 0.012 * (i % 2) + 0.006, 0.55), scale=(0.52, 1.0, 0.16))
    # neck + head on a pivot at the neck base
    head = E('head', body, (0, -0.2, 0.62))
    _obj(f'{name}_neck', _cone('neck', 0.075, 0.06, 0.24), coll, skin, head, (0, -0.03, 0.10), rot=(math.radians(-12), 0, 0))
    _obj(f'{name}_skull', _sphere('skull', 12, 8), coll, skin, head, (0, -0.07, 0.27), scale=(0.135, 0.14, 0.13))
    _obj(f'{name}_beak', _cone('beak', 0.04, 0.0, 0.09, 6), coll, beak, head, (0, -0.225, 0.255), rot=(math.radians(90), 0, 0))
    _obj(f'{name}_snood', _sphere('snood', 8, 6), coll, red, head, (0.012, -0.215, 0.26), rot=(math.radians(-20), 0, 0), scale=(0.022, 0.022, 0.07))
    _obj(f'{name}_wattle', _sphere('wattle', 8, 6), coll, red, head, (0, -0.175, 0.2), scale=(0.03, 0.028, 0.045))
    eyes = {}
    for s, k in ((1, 'l'), (-1, 'r')):
        ep = E(f'eye_{k}', head, (s * 0.062, -0.165, 0.315))
        _obj(f'{name}_eyew_{k}', _sphere('eyew', 12, 8), coll, white, ep, (0, 0, 0), scale=(0.06, 0.038, 0.068))
        _obj(f'{name}_pupil_{k}', _sphere('pupil', 10, 7), coll, black, ep, (-s * 0.006, -0.028, -0.004), scale=(0.028, 0.014, 0.034))
        _obj(f'{name}_glint_{k}', _sphere('glint', 6, 4), coll, white, ep, (s * 0.004, -0.041, 0.016), scale=(0.008, 0.004, 0.009))
        eyes[k] = ep
    # cheeks (blush) for cuteness
    for s in (1, -1):
        _obj(f'{name}_blush{s}', _sphere('blush', 8, 5), coll, toon('t_blush', '#f08c8c', 0.6), head, (s * 0.10, -0.15, 0.25), scale=(0.03, 0.01, 0.02))
    # legs on hip pivots
    legs = {}
    for s, k in ((1, 'l'), (-1, 'r')):
        hp = E(f'leg_{k}', body, (s * 0.1, 0.0, 0.22))
        _obj(f'{name}_shin_{k}', _cone('shin', 0.026, 0.022, 0.2), coll, orange, hp, (0, 0, -0.1))
        for j, a in enumerate((-30, 0, 30)):
            _obj(f'{name}_toe_{k}{j}', _cone('toe', 0.016, 0.006, 0.09, 6), coll, orange, hp, (0, 0, -0.205),
                 rot=(math.radians(90), 0, math.radians(a)), scale=(1, 1, 1))
        legs[k] = hp
    # small leg offsets: toes point forward (-Y): cones along -Y need origin at heel
    for o in coll.objects:
        if '_toe_' in o.name:
            o.location = o.location + Vector((0, -0.04, 0)) if o.location.length < 1 else o.location
    return dict(root=root, body=body, head=head, eye_l=eyes['l'], eye_r=eyes['r'], leg_l=legs['l'], leg_r=legs['r'], tail=tail)


def _empty(coll, name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); coll.objects.link(e); e.parent = parent; e.location = loc
    e.rotation_mode = 'XYZ'
    return e
