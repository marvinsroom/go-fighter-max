"""Bake portable skin maps and export the detailed head without losing source edits."""
from pathlib import Path
import json
import bpy

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/reference-reconstruction/detailed-v4'
bpy.ops.wm.open_mainfile(filepath=str(out/'will-head-detailed.blend'))
head=bpy.data.objects['Will_HeadSkin']
scene=bpy.context.scene
scene.render.engine='CYCLES';scene.cycles.samples=1
scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True
scene.render.bake.margin=8
mat=head.data.materials[0]
bpy.ops.object.select_all(action='DESELECT');head.select_set(True);bpy.context.view_layer.objects.active=head
images={}
for label,kind,space in [('basecolor','DIFFUSE','sRGB'),('normal','NORMAL','Non-Color'),('roughness','ROUGHNESS','Non-Color')]:
    image=bpy.data.images.new('Will detailed '+label,width=2048,height=2048,alpha=False)
    image.colorspace_settings.name=space
    node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image
    mat.node_tree.nodes.active=node;node.select=True
    print('BAKING_DETAIL_MAP',label,flush=True)
    bpy.ops.object.bake(type=kind)
    image.filepath_raw=str(out/('will-head-'+label+'.png'));image.file_format='PNG';image.save();image.pack()
    images[label]=image
    mat.node_tree.nodes.remove(node)
portable=bpy.data.materials.new('Will detailed skin - portable maps');portable.use_nodes=True
shader=portable.node_tree.nodes.get('Principled BSDF')
shader.inputs['Specular IOR Level'].default_value=.28
if 'Subsurface Weight' in shader.inputs:
    shader.inputs['Subsurface Weight'].default_value=.07
    shader.inputs['Subsurface Radius'].default_value=(1.,.4,.2)
    shader.inputs['Subsurface Scale'].default_value=.002
for label in ['basecolor','roughness']:
    node=portable.node_tree.nodes.new('ShaderNodeTexImage');node.image=images[label]
    portable.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color' if label=='basecolor' else 'Roughness'])
normal=portable.node_tree.nodes.new('ShaderNodeTexImage');normal.image=images['normal']
decode=portable.node_tree.nodes.new('ShaderNodeNormalMap');decode.inputs['Strength'].default_value=1
portable.node_tree.links.new(normal.outputs['Color'],decode.inputs['Color'])
portable.node_tree.links.new(decode.outputs['Normal'],shader.inputs['Normal'])
head.data.materials.clear();head.data.materials.append(portable)
scene.cycles.samples=40
meshes=[o for o in scene.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes:obj.select_set(True)
bpy.context.view_layer.objects.active=head
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'will-head-detailed-export.blend'))
bpy.ops.export_scene.gltf(filepath=str(out/'will-head-detailed.glb'),export_format='GLB',use_selection=True)
expected={o.name:sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(out/'will-head-detailed.glb'))
imported=[o for o in bpy.data.objects if o.type=='MESH']
actual={o.name:sum(len(p.vertices)-2 for p in o.data.polygons) for o in imported}
assert set(expected)==set(actual),(set(expected)-set(actual),set(actual)-set(expected))
assert expected==actual,'Triangle counts changed on export'
assert sum(actual.values())>350000,'Expected detailed curl geometry'
skin=bpy.data.objects['Will_HeadSkin']
assert len(skin.data.uv_layers)>0,'Missing skin UV map'
skin_mat=skin.data.materials[0]
assert any(n.type=='NORMAL_MAP' for n in skin_mat.node_tree.nodes),'Missing exported normal map'
assert len([i for i in bpy.data.images if i.size[0]==2048 and i.size[1]==2048])>=3,'Missing skin maps'
for name in ['Will_TexturedCurlClusters','Will_CurlLoops','Will_FineFacialHair','Will_FineEyelashes']:
    assert name in actual,'Missing modeled detail '+name
report={'status':'Passed','meshes':len(imported),'triangles':sum(actual.values()),
        'modeled_hair_and_lashes':True,'skin_uv':True,'embedded_skin_maps':['basecolor 2048','normal 2048','roughness 2048'],
        'scope':'Mesh/material portability only. Head remains unrigged; likeness and animation approval pending.'}
(out/'export-validation.json').write_text(json.dumps(report,indent=2))
print('DETAILED_HEAD_EXPORT_VERIFIED',json.dumps(report),flush=True)
