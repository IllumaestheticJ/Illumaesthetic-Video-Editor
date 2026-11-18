# close-ups of the wing foot and trunk-lip edge on the CGI car (shot 9 set-up) and the scan (shot 8 end state)
import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]; out = argv[0]; which = argv[1]
sys.argv = [sys.argv[0], '--', '--shot', '9' if which == 'cgi' else '8', '--out', '/tmp/x', '--frames', '71-71']
src = open('/home/user/Illumaesthetic-Video-Editor/projects/bf-integra-385-combo/tools/shots.py').read()
src = src.replace("bpy.ops.render.render(animation=True)", "pass")
if which == 'scan': src = src.replace("REG = A.reg_dir", "REG = '/home/user/media/bf-integra-385-combo/work/reg3'")
exec(compile(src, 'shots.py', 'exec'))
sc = bpy.context.scene; sc.frame_set(140 if which != 'cgi' else 140); sc.render.resolution_percentage = 40; sc.cycles.samples = 16
cam = sc.camera
for nm, loc, tgt in [('foot', (-0.95, 2.85, 1.15), (-0.55, 2.15, 1.02)), ('lip', (0.0, 3.05, 1.25), (0.0, 2.25, 0.99)), ('lipside', (0.95, 2.75, 1.05), (0.45, 2.25, 1.0))]:
    cam.animation_data_clear(); cam.data.lens = 70
    cam.location = Vector(loc); cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f'{out}_{which}_{nm}.png'; bpy.ops.render.render(write_still=True)
