"""Project the approved reconstruction input onto the real generated head,
then bake a portable UV texture locally. No network calls or landmark fitting.
"""
from pathlib import Path
import json
import math
import bpy
import numpy as np
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/reference-reconstruction'
source=out/'will-head-textured-v2.blend'
if source.exists():raise RuntimeError('Refusing to overwrite the textured head source.')
bpy.ops.wm.open_mainfile(filepath=str(out/'will-generated-head.blend'))
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH')
mesh=obj.data
coords=np.array([list(v.co) for v in mesh.vertices])
low=coords.min(axis=0);high=coords.max(axis=0);span=high-low
image=bpy.data.images.load(str(out/'will-head-input-v1.png'))
W,H=image.size
pixels=np.asarray(image.pixels[:]).reshape(H,W,4)
ys,xs=np.where(pixels[:,:,3]>.5)
uv_min=np.array([xs.min()/W,ys.min()/H]);uv_max=np.array([(xs.max()+1)/W,(ys.max()+1)/H])
projected=mesh.uv_layers.new(name='ReferenceFrontProjection')
weight=mesh.color_attributes.new(name='FrontProjectionWeight',type='FLOAT_COLOR',domain='CORNER')
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)))
    return t*t*(3-2*t)
for loop in mesh.loops:
    p=coords[loop.vertex_index]
    normalized=np.array([(p[0]-low[0])/span[0],(p[2]-low[2])/span[2]])
    uv=uv_min+normalized*(uv_max-uv_min)
    projected.data[loop.index].uv=uv
    # A front photograph supplies front/cheek color only. The rear uses simple
    # procedural skin and fade colors; it is explicitly unfinished texture work.
    front=smooth(-.025,.015,-p[1])
    weight.data[loop.index].color=(front,front,front,1)
mat=bpy.data.materials.new('Reference projection for local bake');mat.use_nodes=True
nodes=mat.node_tree.nodes;links=mat.node_tree.links;nodes.clear()
output=nodes.new('ShaderNodeOutputMaterial')
shader=nodes.new('ShaderNodeBsdfPrincipled');shader.inputs['Roughness'].default_value=.7
shader.inputs['Specular IOR Level'].default_value=.2
links.new(shader.outputs['BSDF'],output.inputs['Surface'])
uvnode=nodes.new('ShaderNodeUVMap');uvnode.uv_map=projected.name
texture=nodes.new('ShaderNodeTexImage');texture.image=image;texture.extension='EXTEND'
links.new(uvnode.outputs['UV'],texture.inputs['Vector'])
attribute=nodes.new('ShaderNodeVertexColor');attribute.layer_name=weight.name
coordsnode=nodes.new('ShaderNodeTexCoord');separate=nodes.new('ShaderNodeSeparateXYZ')
links.new(coordsnode.outputs['Generated'],separate.inputs['Vector'])
ramp=nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.61;ramp.color_ramp.elements[0].color=(.27,.115,.054,1)
ramp.color_ramp.elements[1].position=.74;ramp.color_ramp.elements[1].color=(.007,.004,.003,1)
links.new(separate.outputs['Z'],ramp.inputs['Fac'])
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX'
alpha_mask=nodes.new('ShaderNodeMath');alpha_mask.operation='MULTIPLY'
links.new(attribute.outputs['Color'],alpha_mask.inputs[0]);links.new(texture.outputs['Alpha'],alpha_mask.inputs[1])
links.new(alpha_mask.outputs[0],mix.inputs[0]);links.new(ramp.outputs['Color'],mix.inputs[1]);links.new(texture.outputs['Color'],mix.inputs[2])
links.new(mix.outputs['Color'],shader.inputs['Base Color'])
mesh.materials.clear();mesh.materials.append(mat)
for p in mesh.polygons:p.material_index=0
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
atlas=mesh.uv_layers.new(name='HeadAtlas')
mesh.uv_layers.active=atlas;atlas.active_render=True
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.003)
bpy.ops.object.mode_set(mode='OBJECT')
baked=bpy.data.images.new('Will head base color',width=2048,height=2048,alpha=False)
bake_node=nodes.new('ShaderNodeTexImage');bake_node.image=baked;nodes.active=bake_node;bake_node.select=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1
scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False
scene.render.bake.use_pass_color=True;scene.render.bake.margin=8
print('BAKING_HEAD_TEXTURE',flush=True)
bpy.ops.object.bake(type='DIFFUSE')
baked.filepath_raw=str(out/'will-head-basecolor-v2.png');baked.file_format='PNG';baked.save();baked.pack()
final=bpy.data.materials.new('Will head - baked base color');final.use_nodes=True
principled=final.node_tree.nodes.get('Principled BSDF')
principled.inputs['Roughness'].default_value=.72;principled.inputs['Specular IOR Level'].default_value=.22
atlasnode=final.node_tree.nodes.new('ShaderNodeTexImage');atlasnode.image=baked
final.node_tree.links.new(atlasnode.outputs['Color'],principled.inputs['Base Color'])
mesh.materials.clear();mesh.materials.append(final)
# Exporters use the first UV map for ordinary base-color textures.
mesh.uv_layers.remove(mesh.uv_layers.get('ReferenceFrontProjection'))
mesh.uv_layers.active=mesh.uv_layers.get('HeadAtlas');mesh.uv_layers.active.active_render=True
scene.cycles.samples=24;scene.cycles.use_denoising=True
camera=scene.camera;camera.location=(0,-1,.17);camera.rotation_euler=(math.pi/2,0,0)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(source))
bpy.ops.export_scene.gltf(filepath=str(out/'will-head-textured-v2.glb'),export_format='GLB',use_selection=True)
report={'stage':'Generated geometry with locally projected/baked reference color; unrigged head study',
        'vertices':len(mesh.vertices),'triangles':sum(len(p.vertices)-2 for p in mesh.polygons),
        'texture_size':[2048,2048],'texture_method':'Front projection from approved reconstruction image, procedural rear skin/hair fill',
        'limitations':['Side and rear color require finishing','No facial rig','Not fitted to body or imported into Unreal']}
(out/'textured-head-report-v2.json').write_text(json.dumps(report,indent=2))
for name,location in [('textured-front',(0,-1,.17)),('textured-three-quarter',(.60,-1,.19)),('textured-profile',(1,0,.17))]:
    camera.location=location;camera.rotation_euler=(Vector((0,0,.17))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/('v2-'+name+'.png'));bpy.ops.render.render(write_still=True)
print('TEXTURED_HEAD_REVIEW_READY',flush=True)
