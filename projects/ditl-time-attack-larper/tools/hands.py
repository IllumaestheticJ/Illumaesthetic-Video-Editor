"""Rounded 3D POV hands (from ditl-wrx-vb shots.py), with a race-glove option for the track guy."""
import bpy
from ditl_kit import box, mat, R
OPEN, FIST, POINT, FLAT = (0.12, 0.06, 0.1, 0.22), (1.3, 1.35, 1.35, 1.4), (0.0, 1.3, 1.35, 1.4), (0.02, 0.0, 0.02, 0.05)

def skinmat(name="skin_him", c1=(0.30, 0.165, 0.09), c2=(0.38, 0.22, 0.13)):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.5
    co = nt.nodes.new("ShaderNodeTexCoord"); t = nt.nodes.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = 55; t.inputs["Detail"].default_value = 6
    r = nt.nodes.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = (*c1, 1); r.color_ramp.elements[1].color = (*c2, 1); r.color_ramp.elements[0].position = 0.3; r.color_ramp.elements[1].position = 0.7
    nt.links.new(co.outputs["Object"], t.inputs["Vector"]); nt.links.new(t.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; nt.links.new(t.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def rnd_(o, w, seg=3):
    m = o.modifiers.new("bev", "BEVEL"); m.width = w; m.segments = seg
    for p in o.data.polygons: p.use_smooth = True
    return o

_S = {}
def S():
    if "s" not in _S: _S["s"] = skinmat(); _S["n"] = mat("nail", (0.62, 0.45, 0.36), 0.3); _S["p"] = mat("palmskin", (0.5, 0.31, 0.22), 0.55)
    return _S

def hand(name, parent, loc, rot, curls=OPEN, thumb=0.3, mirror=False, sleeve=None, hold=None, glove=None):
    """Rounded 3D hand. Fingers along local +Y, back of hand +Z, forearm toward -Y. glove: material for hand+wrist (race glove), sleeve covers the forearm."""
    s = dict(S()); skin = s["s"]
    if glove: s["p"] = s["n"] = glove
    hs = glove or skin; root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    root.parent = parent; root.location = loc; root.rotation_euler = rot
    if mirror: root.scale = (-1, 1, 1)
    palm = rnd_(box(name + "_palm", (0.086, 0.098, 0.03), hs, parent=root, base="y", taper=1.1), 0.012, 4)
    rnd_(box(name + "_pad", (0.07, 0.08, 0.012), s["p"], loc=(0, 0.01, -0.012), parent=root, base="y"), 0.005)
    rnd_(box(name + "_wr", (0.062, 0.05, 0.04), hs, loc=(0, -0.04, 0), parent=root, base="y", taper=1.25), 0.014, 4)
    rnd_(box(name + "_arm", (0.085, 0.4, 0.07), (sleeve if glove and sleeve else skin), loc=(0, -0.44, 0), parent=root, base="y", taper=0.7), 0.024, 4)
    if sleeve: rnd_(box(name + "_slv", (0.11, 0.22, 0.095), sleeve, loc=(0, -0.6, 0), parent=root, base="y"), 0.02)
    xs = (-0.032, -0.0105, 0.011, 0.0315); ln = (0.04, 0.045, 0.042, 0.032)
    for i in range(4):
        c = curls[i]
        k1 = rnd_(box(f"{name}_k{i}", (0.021, 0.02, 0.024), hs, loc=(xs[i], 0.092, 0.002), parent=palm), 0.008)
        s1 = rnd_(box(f"{name}_f{i}a", (0.019, ln[i], 0.019), hs, loc=(xs[i], 0.098, 0), rot=(-c, 0, 0), parent=palm, base="y"), 0.007)
        s2 = rnd_(box(f"{name}_f{i}b", (0.018, ln[i] * 0.72, 0.017), hs, loc=(0, ln[i], 0), rot=(-c * 1.15, 0, 0), parent=s1, base="y"), 0.0065)
        s3 = rnd_(box(f"{name}_f{i}c", (0.0165, ln[i] * 0.6, 0.015), hs, loc=(0, ln[i] * 0.72, 0), rot=(-c * 0.9, 0, 0), parent=s2, base="y", taper=0.8), 0.006)
        rnd_(box(f"{name}_n{i}", (0.012, ln[i] * 0.34, 0.003), s["n"], loc=(0, ln[i] * 0.22, 0.0078), parent=s3, base="y"), 0.001, 2)
    t1 = rnd_(box(name + "_t1", (0.026, 0.05, 0.026), hs, loc=(-0.044, 0.018, -0.006), rot=(0, 0, R(50) - thumb), parent=palm, base="y"), 0.009)
    t2 = rnd_(box(name + "_t2", (0.022, 0.038, 0.02), hs, loc=(0, 0.05, 0), rot=(0, 0, -thumb), parent=t1, base="y", taper=0.8), 0.007)
    rnd_(box(name + "_tn", (0.014, 0.014, 0.003), s["n"], loc=(0, 0.02, 0.0105), parent=t2, base="y"), 0.001, 2)
    if hold == "vape":
        v = rnd_(box(name + "_vape", (0.03, 0.14, 0.022), mat("vape", (0.75, 0.08, 0.5), 0.25), loc=(0, 0.03, -0.035), rot=(0, 0, R(80)), parent=root), 0.006)
        box(name + "_vtip", (0.012, 0.03, 0.012), mat("vtip", (0.03, 0.03, 0.03), 0.3), loc=(0, 0.085, 0), parent=v)
    if hold == "pen":
        box(name + "_pen", (0.011, 0.011, 0.16), mat("pen", (0.05, 0.1, 0.6), 0.3), loc=(0.0, 0.07, -0.06), rot=(R(20), 0, 0), parent=root)
    return root

