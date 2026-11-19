"""Store thumbnail of the FK8 + TC wing (rear 3/4, light grey), like the listing image. blender -b --python thumb.py -- out.png"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lookdev as L
from ditl_kit import world, camera, plane, mat
bpy.ops.wm.read_factory_settings(use_empty=True)
world((0.85, 0.86, 0.88), 1.0, sun=(2.0, 55, 150)); plane("floor", 40, 40, mat("fl", (0.8, 0.8, 0.82)), (0, 0, 0))
L.fk8((0.55, 0.56, 0.58)); L.tc_wing(); camera((-3.6, -3.2, 2.0), look=(1.6, 0, 0.8), lens=32)
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.samples = 24; sc.render.resolution_x = sc.render.resolution_y = 480
sc.view_settings.view_transform = "Standard"; sc.render.filepath = sys.argv[sys.argv.index("--") + 1]; bpy.ops.render.render(write_still=True)
