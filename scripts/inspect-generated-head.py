"""Open the actual downloaded Hunyuan mesh and render review views in Blender."""
from pathlib import Path
import json
import math
import bpy
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/reference-reconstruction'
result=json.loads((out/'generation-result.json').read_text())
if 'error' in result:raise RuntimeError(result['error'])
paths=[]
def collect(value):
    if isinstance(value,str) and value.lower().endswith(('.glb','.gltf','.obj')) and Path(value).is_file():
        paths.append(Path(value))
    elif isinstance(value,(list,tuple)):
        for child in value:collect(child)
    elif isinstance(value,dict):
        for child in value.values():collect(child)
collect(result['result'])
if not paths:raise RuntimeError('No downloaded mesh found in generation result.')
# generation_all returns the untextured mesh before its textured counterpart.
mesh_path=paths[-1]
print('IMPORTING_ACTUAL_MESH',str(mesh_path),flush=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
if mesh_path.suffix.lower() in ('.glb','.gltf'):
    bpy.ops.import_scene.gltf(filepath=str(mesh_path))
else:bpy.ops.wm.obj_import(filepath=str(mesh_path))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
assert meshes,'Downloaded file contained no mesh objects'
raw_counts={o.name:sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes}
for obj in meshes:
    triangles=raw_counts[obj.name]
    if triangles>100000:
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
        bpy.context.view_layer.objects.active=obj
        decimate=obj.modifiers.new('Working mesh reduction','DECIMATE')
        decimate.ratio=90000/triangles
        bpy.ops.object.modifier_apply(modifier=decimate.name)
points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
low=Vector([min(p[a] for p in points) for a in range(3)])
high=Vector([max(p[a] for p in points) for a in range(3)])
span=high-low
assert span.z>1e-5
factor=.34/span.z
origin=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
for obj in meshes:
    world=obj.matrix_world.copy()
    for vertex in obj.data.vertices:vertex.co=(world@vertex.co-origin)*factor
    obj.parent=None;obj.matrix_world.identity()
    for polygon in obj.data.polygons:polygon.use_smooth=True
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.color=(.07,.07,.07)
scene.view_settings.view_transform='AgX'
for name,location,power,size in [('Key',(-.5,-.7,.7),35,.6),('Fill',(.5,-.3,.45),18,.5),('Rim',(.2,.5,.6),45,.4)]:
    light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size
    obj=bpy.data.objects.new(name,light);bpy.context.collection.objects.link(obj);obj.location=location
    obj.rotation_euler=(Vector((0,0,.18))-obj.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(0,-1,.17))
camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=.40;scene.camera=camera
camera.rotation_euler=(math.pi/2,0,0)
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_location=(0,0,.17)
        area.spaces.active.region_3d.view_distance=.65
        area.spaces.active.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
        area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes:obj.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-generated-head.blend'))
report={'source_mesh':str(mesh_path),'stage':'Unrigged generated head for likeness review; no body fitting or game integration',
        'original_triangles':raw_counts,
        'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons),
                   'uv_layers':len(o.data.uv_layers),'materials':[m.name for m in o.data.materials if m]} for o in meshes],
        'texture_images':[{'name':i.name,'size':list(i.size)} for i in bpy.data.images if i.type=='IMAGE']}
(out/'mesh-inspection.json').write_text(json.dumps(report,indent=2))
for name,location in [('front',(0,-1,.17)),('three-quarter',(.60,-1,.19)),('profile',(1,0,.17))]:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.17))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
print('GENERATED_HEAD_REVIEW_READY',flush=True)
