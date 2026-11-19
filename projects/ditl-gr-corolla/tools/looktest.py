import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cars as C, shots as W
from shots import R
a = sys.argv[sys.argv.index("--") + 1:]; which = a[0]; out = a[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
W.k.world(); W.k.lot_set() if which == "x" else W.road()
if which == "fl5":
    r, sh = C.fl5(); cams = {"side": ((6, 0, 1.0), (0, 0, 0.7)), "f34": ((3.5, -5, 1.6), (0, 0, 0.6)), "r34": ((-3.5, 5, 1.6), (0, 0, 0.6))}
else:
    g, by = C.grc(kit=True); h, hb = C.hatch(wing=True); h.location = (3.2, 0, 0); w, wb = C.wrx(); w.location = (-3.2, 0, 0)
    cams = {"f34": ((5.5, -8.5, 2.4), (0, 0, 0.6)), "r34": ((-4.5, 8, 2.2), (0, 0, 0.7))}
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 14; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
sc.render.resolution_x = sc.render.resolution_y = 540; sc.view_settings.view_transform = "Standard"
for n, (loc, look) in cams.items():
    for o in [o for o in bpy.data.objects if o.name in ("rig", "cam")]: bpy.data.objects.remove(o)
    W.rigcam(loc, look, lens=28); sc.render.filepath = f"{out}/look_{which}_{n}.png"; bpy.ops.render.render(write_still=True)
