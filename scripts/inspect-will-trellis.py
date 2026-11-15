"""Inspect and render the actual TRELLIS GLB; preserve raw geometry and materials."""
from pathlib import Path
import bpy,json,math,argparse,sys
from mathutils import Vector
parser=argparse.ArgumentParser()
parser.add_argument('--folder',default='trellis-cel-v1')
parser.add_argument('--filename',default='will-trellis-cel-raw.glb')
parser.add_argument('--service',default='microsoft/TRELLIS.2')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
root=Path(__file__).resolve().parents[1];out=root/'characters/will'/args.folder
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(out/args.filename))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert meshes
points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
low=Vector([min(p[a] for p in points) for a in range(3)])
high=Vector([max(p[a] for p in points) for a in range(3)])
factor=1.85/(high.z-low.z);origin=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
for obj in meshes:
    matrix=obj.matrix_world.copy()
    for v in obj.data.vertices:v.co=(matrix@v.co-origin)*factor
    obj.parent=None;obj.matrix_world.identity()
    for p in obj.data.polygons:p.use_smooth=True
report={'source':args.service,'status':'Unrigged candidate for visual review',
        'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
                   'uv_layers':len(o.data.uv_layers),'materials':[m.name for m in o.data.materials if m]} for o in meshes],
        'armatures':len([o for o in bpy.data.objects if o.type=='ARMATURE']),
        'textures':[{'name':im.name,'size':list(im.size)} for im in bpy.data.images if im.type=='IMAGE'],
        'limitations':['Generated topology is not animation-ready','Likeness and cel style need user review','Not imported into Unreal']}
assert all(m['uv_layers']>0 for m in report['meshes']),'Missing UVs'
assert any(max(t['size'])>=2048 for t in report['textures']),'Missing requested texture detail'
(out/'mesh-inspection.json').write_text(json.dumps(report,indent=2))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Review world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.24,.24,.24,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
scene.view_settings.view_transform='Standard'
for name,loc,power,size in [('Key',(-2,-3,3.5),250,3),('Fill',(2,-1,2),140,2),('Rim',(0,2,3),200,2)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=loc
    obj.rotation_euler=(Vector((0,0,1))-obj.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Review camera');camera=bpy.data.objects.new('Review camera',data)
scene.collection.objects.link(camera);scene.camera=camera;data.type='ORTHO';data.ortho_scale=2.15
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-generated-cel-review.blend'))
for name,loc in [('front',(0,-4,1)),('three-quarter',(2,-4,1.2)),('back',(0,4,1))]:
    camera.location=loc;camera.rotation_euler=(Vector((0,0,.95))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('TRELLIS_MESH_REVIEW_READY',json.dumps(report),flush=True)
