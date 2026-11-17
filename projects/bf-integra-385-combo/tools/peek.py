# quick workbench views of a .blend's meshes: top, side, rear-3/4
import bpy, sys, math, mathutils
argv=sys.argv[sys.argv.index('--')+1:]; out=argv[0]
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=4; sc.cycles.use_denoising=False; sc.cycles.device='CPU'; sc.render.resolution_x=800; sc.render.resolution_y=500
w=bpy.data.worlds.new('w'); w.color=(0.6,0.6,0.6); sc.world=w
cam=bpy.data.cameras.new('c'); co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
cam.type='ORTHO'; cam.ortho_scale=6
for name,loc in [('top',(0,0,20)),('side',(20,0,0.7)),('rear',(0,20,0.7))]:
    co.location=loc; d=mathutils.Vector((0,0,0.7 if name!='top' else 0))-co.location
    co.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{out}_{name}.png'; bpy.ops.render.render(write_still=True)
