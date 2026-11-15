"""Review actual downloaded Hi3DGen geometry with neutral studio shading."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
root=Path(__file__).resolve().parents[1];out=root/'characters/will/hi3dgen-head-v1'
source=out/'will-head-raw.glb'
assert source.is_file(),'A real generated GLB is required'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert meshes
points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
low=Vector([min(p[i] for p in points) for i in range(3)])
high=Vector([max(p[i] for p in points) for i in range(3)])
assert high.z-low.z>0
scale=.34/(high.z-low.z);origin=(low+high)/2
report={'source':'Stable-X/Hi3DGen','source_glb':source.name,
        'raw_bounds_min':list(low),'raw_bounds_max':list(high),
        'review_transform':'Uniform scale to 34cm head height and center; no facial reshaping',
        'scale':scale,'meshes':[], 'likeness_approved':False,
        'unreal_assets_changed':False,'rigged':False,
        'limitations':['Geometry-only output','No face rig','Likeness and Guilty Gear style unproven']}
for obj in meshes:
    matrix=obj.matrix_world.copy()
    for vertex in obj.data.vertices:vertex.co=(matrix@vertex.co-origin)*scale
    obj.parent=None;obj.matrix_world.identity()
    obj.data.materials.clear()
    for polygon in obj.data.polygons:polygon.use_smooth=True;polygon.material_index=0
    report['meshes'].append({'name':obj.name,'vertices':len(obj.data.vertices),
        'triangles':sum(len(p.vertices)-2 for p in obj.data.polygons),
        'uv_layers':len(obj.data.uv_layers)})
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=640;scene.render.resolution_y=760;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.view_settings.view_transform='Standard'
shade=scene.display.shading;shade.light='STUDIO';shade.studiolight_rotate_z=.3
shade.color_type='SINGLE';shade.single_color=(.60,.60,.60)
shade.show_shadows=True;shade.show_cavity=True;shade.cavity_type='BOTH'
shade.curvature_ridge_factor=1.2;shade.curvature_valley_factor=.7
shade.background_type='WORLD';scene.world=bpy.data.worlds.new('Neutral review background');scene.world.color=(.045,.045,.045)
camera_data=bpy.data.cameras.new('Geometry review camera');camera=bpy.data.objects.new('Geometry review camera',camera_data)
scene.collection.objects.link(camera);scene.camera=camera;camera_data.type='ORTHO';camera_data.ortho_scale=.43
def orient(position):
    camera.location=position;camera.rotation_euler=(-camera.location).to_track_quat('-Z','Y').to_euler()
orient((.55,-1,.04))
bpy.ops.object.select_all(action='DESELECT')
meshes[0].select_set(True);bpy.context.view_layer.objects.active=meshes[0]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active;space.region_3d.view_location=(0,0,0)
            space.region_3d.view_distance=.60;space.region_3d.view_rotation=camera.rotation_euler.to_quaternion()
            space.region_3d.view_perspective='ORTHO';space.shading.type='SOLID';space.shading.color_type='SINGLE'
            space.shading.single_color=(.60,.60,.60)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-hi3dgen-geometry-review.blend'))
for name,position in [('clay-front',(0,-1,0)),('clay-three-quarter',(.55,-1,.04)),('clay-profile',(1,0,0)),('clay-back',(0,1,0))]:
    orient(position);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
report['render_engine']=scene.render.engine
(out/'mesh-inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('HI3DGEN_GEOMETRY_REVIEW_READY',json.dumps(report),flush=True)
