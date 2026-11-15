"""Blender-only hard-band toon/material review of the head study."""
from pathlib import Path
import bpy,bmesh,json,sys,argparse
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--study-dir',default='characters/will/sculpt-study-v1')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=root/args.study_dir
bpy.ops.wm.open_mainfile(filepath=str(out/'will-head-shape-study.blend'))
scene=bpy.context.scene
# Build real surface-material light bands; no image posterization/compositing.
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=640;scene.render.resolution_y=760;scene.render.resolution_percentage=100
scene.use_nodes=False;scene.view_settings.view_transform='Standard'
materials={m for obj in scene.objects if obj.type in {'MESH','CURVE'} for m in obj.data.materials if m}
for mat in materials:
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    principled=next((n for n in nodes if n.type=='BSDF_PRINCIPLED'),None)
    if not principled:continue
    base=principled.inputs['Base Color']
    source=base.links[0].from_socket if base.is_linked else None
    color=tuple(base.default_value)
    diffuse=nodes.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Color'].default_value=(1,1,1,1)
    light=nodes.new('ShaderNodeShaderToRGB');links.new(diffuse.outputs[0],light.inputs[0])
    bands=nodes.new('ShaderNodeValToRGB');bands.color_ramp.interpolation='CONSTANT'
    bands.color_ramp.elements[0].position=0;bands.color_ramp.elements[0].color=(.32,.32,.32,1)
    bands.color_ramp.elements[1].position=.55;bands.color_ramp.elements[1].color=(1,1,1,1)
    middle=bands.color_ramp.elements.new(.23);middle.color=(.65,.65,.65,1)
    links.new(light.outputs[0],bands.inputs[0])
    multiply=nodes.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
    if source:links.new(source,multiply.inputs[1])
    else:multiply.inputs[1].default_value=color
    links.new(bands.outputs[0],multiply.inputs[2])
    emission=nodes.new('ShaderNodeEmission');links.new(multiply.outputs[0],emission.inputs[0])
    output=next(n for n in nodes if n.type=='OUTPUT_MATERIAL');links.new(emission.outputs[0],output.inputs['Surface'])
# Inverted mesh hull produces silhouettes directly in the renderer.
outline=bpy.data.materials.new('Black inverted-hull outline');outline.use_nodes=True
outline.use_backface_culling=True
nodes=outline.node_tree.nodes;nodes.clear()
emit=nodes.new('ShaderNodeEmission');emit.inputs[0].default_value=(.004,.002,.001,1)
output=nodes.new('ShaderNodeOutputMaterial');outline.node_tree.links.new(emit.outputs[0],output.inputs[0])
head=bpy.data.objects['Will_Head_EditableCage']
deps=bpy.context.evaluated_depsgraph_get()
hull=bpy.data.objects.new('Head_outline_hull',bpy.data.meshes.new_from_object(head.evaluated_get(deps)))
scene.collection.objects.link(hull)
bm=bmesh.new();bm.from_mesh(hull.data);bm.normal_update()
for vertex in bm.verts:vertex.co+=vertex.normal*.00065
bmesh.ops.reverse_faces(bm,faces=list(bm.faces));bm.to_mesh(hull.data);bm.free()
hull.data.materials.clear();hull.data.materials.append(outline)
for poly in hull.data.polygons:poly.material_index=0
camera=scene.camera;target=Vector((0,-.044,.165));camera.data.ortho_scale=.395
camera.location=(.55,-1,.19);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
reference=bpy.data.objects.new('REFERENCE - cel design, not a skin texture',None)
scene.collection.objects.link(reference);reference.empty_display_type='IMAGE'
reference.data=bpy.data.images.load(str(root/'concepts/will-cel-design-target-v1.png'),check_existing=True)
reference.empty_display_size=.65;reference.location=(-.55,.12,.16);reference.rotation_euler=(1.57079632679,0,0)
reference.hide_render=True;reference.hide_select=True
bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active;space.region_3d.view_location=target;space.region_3d.view_distance=.60
            space.region_3d.view_rotation=camera.rotation_euler.to_quaternion();space.region_3d.view_perspective='ORTHO'
            space.shading.type='MATERIAL';space.shading.use_scene_world=True;space.shading.use_scene_lights=True
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-head-toon-review.blend'))
for name,loc in [('toon-front',(0,-1,.165)),('toon-three-quarter',(.55,-1,.19)),('toon-profile',(1,-.044,.165))]:
    camera.location=loc;camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
used={mat for obj in scene.objects if obj.type in {'MESH','CURVE'} for mat in obj.data.materials if mat}
image_nodes=[(mat.name,node.name) for mat in used for node in mat.node_tree.nodes if node.type=='TEX_IMAGE']
assert not image_nodes,'Surface material unexpectedly uses an image texture'
assert any(node.bl_idname=='ShaderNodeShaderToRGB' for mat in used for node in mat.node_tree.nodes)
assert bpy.data.objects.get('Separate_eyes') and bpy.data.objects.get('Head_outline_hull')
assert all((out/(name+'.png')).is_file() for name in ['toon-front','toon-three-quarter','toon-profile'])
report={'artifact_checks':'Passed','likeness_approved':False,'render_engine':scene.render.engine,
    'head_base_vertices':len(head.data.vertices),'surface_image_textures':image_nodes,
    'separate_eyes':True,'material_light_bands':3,'outline':'inverted mesh hull',
    'reference_image':'Unrendered empty; not a surface texture','unreal_assets_changed':False,
    'scope':'Editable local proportion and shader study; no production likeness claim'}
(out/'toon-review-validation.json').write_text(json.dumps(report,indent=2))
print('HEAD_TOON_REVIEW_READY',flush=True)
