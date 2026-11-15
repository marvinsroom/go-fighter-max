from pathlib import Path
import json
import bpy
root=Path(__file__).resolve().parents[1]
out=root/'characters/will/integration-v1';out.mkdir(parents=True,exist_ok=True)
report={}
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/v2/will.blend'))
body=bpy.data.objects['Will_FaceBody'];deps=bpy.context.evaluated_depsgraph_get()
evaluated=body.evaluated_get(deps);mesh=evaluated.to_mesh()
report['body_neck']={str(z):[list(v.co) for v in mesh.vertices if abs(v.co.z-z)<.002 and abs(v.co.x)<.11] for z in [1.49,1.50,1.515,1.53,1.55,1.57]}
report['body_groups']=[g.name for g in body.vertex_groups]
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
report['bones']={b.name:{'head':list(b.head_local),'tail':list(b.tail_local)} for b in rig.data.bones}
report['body_modifiers']=[(m.name,m.type) for m in body.modifiers]
evaluated.to_mesh_clear()
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/reference-reconstruction/detailed-v4/will-head-detailed-export.blend'))
head=bpy.data.objects['Will_HeadSkin']
report['head_neck']={str(z):[list(v.co) for v in head.data.vertices if abs(v.co.z-z)<.002] for z in [.005,.015,.025,.035,.045]}
(out/'attachment-probe.json').write_text(json.dumps(report))
print('WILL_ATTACHMENT_PROBE_READY')
