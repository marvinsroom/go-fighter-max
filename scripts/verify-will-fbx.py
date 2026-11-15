from pathlib import Path
import bpy,json
root=Path(__file__).resolve().parents[1];out=root/'characters/will/integration-v1'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(out/'will-runtime.fbx'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
meshes=[o for o in bpy.data.objects if o.type=='MESH']
report={'bones':len(rig.data.bones),'meshes':len(meshes),'triangles':sum(len(p.vertices)-2 for o in meshes for p in o.data.polygons),
    'armature_object_scale':list(rig.scale),'head_rest_position':list(rig.matrix_world@rig.data.bones['head'].head_local),
    'all_meshes_weighted':all(o.vertex_groups and any(m.type=='ARMATURE' for m in o.modifiers) for o in meshes)}
assert report['bones']==53 and report['meshes']==10 and report['triangles']==96376,report
assert report['all_meshes_weighted'] and 1.6<report['head_rest_position'][2]<1.7,report
(out/'fbx-validation.json').write_text(json.dumps(report,indent=2));print('WILL_FBX_VERIFIED',report)
