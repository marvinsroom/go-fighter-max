"""Local head-only topology study. No image projection or landmark fitting.

Use existing human topology as a starting cage, then explicit modeling edits.
Sources are read only; save a separate study for clay/toon review.
"""
from pathlib import Path
import bpy,bmesh,json,math
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'characters/will/sculpt-study-v1'
out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/v2/will.blend'))
report={'source_objects':[(o.name,o.type) for o in bpy.data.objects]}
body=bpy.data.objects['Will_FaceBody']
for modifier in list(body.modifiers):
    if modifier.type=='ARMATURE':body.modifiers.remove(modifier)
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
bpy.ops.object.convert(target='MESH')
for obj in list(bpy.data.objects):
    if obj!=body:bpy.data.objects.remove(obj,do_unlink=True)
body.name='Will_Head_EditableCage'
bm=bmesh.new();bm.from_mesh(body.data)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.000001,
    plane_co=(0,0,1.505),plane_no=(0,0,1),clear_inner=True)
# Remove disconnected shoulder fragments below the jaw on each side.
bmesh.ops.delete(bm,geom=[v for v in bm.verts if abs(v.co.x)>.125 and v.co.z<1.61],context='VERTS')
bm.to_mesh(body.data);bm.free()
for vertex in body.data.vertices:vertex.co-=Vector((0,-.03,1.505))
body.vertex_groups.clear()
report['bounds']={axis:[min(v.co[i] for v in body.data.vertices),max(v.co[i] for v in body.data.vertices)] for i,axis in enumerate('xyz')}
report['face_samples']={str(z):{'xmin':min([v.co.x for v in body.data.vertices if abs(v.co.z-z)<.002],default=0),
    'xmax':max([v.co.x for v in body.data.vertices if abs(v.co.z-z)<.002],default=0),
    'ymin':min([v.co.y for v in body.data.vertices if abs(v.co.z-z)<.002],default=0),
    'ymax':max([v.co.y for v in body.data.vertices if abs(v.co.z-z)<.002],default=0)} for z in [.04,.06,.08,.10,.12,.14,.16,.18,.20,.22,.24,.26,.28,.30]}

def material(name,color):
    mat=bpy.data.materials.new(name);mat.use_nodes=True;mat.diffuse_color=(*color,1)
    shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(*color,1)
    shader.inputs['Roughness'].default_value=.8;return mat
clay=material('Neutral sculpt clay',(.34,.34,.34))
body.data.materials.clear();body.data.materials.append(clay)
for poly in body.data.polygons:poly.material_index=0;poly.use_smooth=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=850;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Study world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.18,.18,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard'
for name,location,power,size in [('Key',(-.4,-.6,.65),25,.5),('Fill',(.4,-.2,.35),10,.5),('Rim',(.2,.4,.6),20,.4)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=location
    obj.rotation_euler=(Vector((0,0,.16))-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Sculpt review');camera=bpy.data.objects.new('Sculpt review',data)
scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=.37
bpy.ops.wm.save_as_mainfile(filepath=str(out/'head-baseline.blend'))
(out/'baseline-report.json').write_text(json.dumps(report,indent=2))
for name,location in [('baseline-front',(0,-1,.16)),('baseline-profile',(1,0,.16))]:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.16))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('HEAD_TOPOLOGY_STUDY_READY',json.dumps(report),flush=True)
