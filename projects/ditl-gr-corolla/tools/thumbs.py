"""Car thumbnails for the forum cards. blender -b --python thumbs.py -- <texdir>"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cars as C, shots as W
out = sys.argv[sys.argv.index("--") + 1]
for nm in ("fl5", "wrx", "grc"):
    bpy.ops.wm.read_factory_settings(use_empty=True); W.k.world(); W.plane("g", 60, 60, W._flat_mat("g", (0.5, 0.5, 0.52)), (0, 0, 0))
    {"fl5": C.fl5, "wrx": C.wrx, "grc": lambda: C.grc(kit=False)}[nm]()
    W.rigcam((3.6, -5.2, 1.5), (0, 0, 0.62), lens=38); sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.samples = 16; sc.cycles.use_denoising = True
    sc.render.resolution_x = sc.render.resolution_y = 256; sc.view_settings.view_transform = "Standard"; sc.render.filepath = f"{out}/thumb_{nm}.png"; bpy.ops.render.render(write_still=True)
