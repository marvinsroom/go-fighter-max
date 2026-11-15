from pathlib import Path
import bpy, math
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'characters/will/integration-v1'
bpy.ops.wm.open_mainfile(filepath=str(out/'will-runtime.blend'))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16
scene.render.resolution_x=850;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Review world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.13,.13,.13,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
for name,loc,power,size in [('Key',(-2,-3,3),350,3),('Fill',(2,-1,2),180,2),('Rim',(1,2,3),260,2)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=loc
    obj.rotation_euler=(Vector((0,0,1))-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Review camera');camera=bpy.data.objects.new('Review camera',data)
scene.collection.objects.link(camera);scene.camera=camera
camera.location=(1,-3.8,1.5);camera.rotation_euler=(Vector((0,0,.95))-camera.location).to_track_quat('-Z','Y').to_euler()
data.type='ORTHO';data.ortho_scale=2.15
scene.render.filepath=str(out/'full-body-review.png');bpy.ops.render.render(write_still=True)
