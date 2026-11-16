"""Nametag proof: both characters front-on, medium shot (run via partA_scene.py --exec)."""
os.makedirs(OUT, exist_ok=True)
reset()
pose(GUS, loc=(-0.45, -1.9, 0), rz=8)
pose(PIP, loc=(0.55, -2.15, 0), rz=-8)
set_eyes(GUS, 0, 0); set_eyes(PIP, 0, 0)
look(cam, (0.05, -4.6, 1.15), (0.05, -2.0, 0.95), 34)
scn.render.filepath = os.path.join(OUT, "tags_medium")
bpy.ops.render.render(write_still=True)
