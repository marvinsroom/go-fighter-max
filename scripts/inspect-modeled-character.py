from pathlib import Path
import json
import sys
import bpy
root=Path(__file__).resolve().parents[1]
name=sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=str(root/'characters'/name/'v1'/(name+'.blend')))
deps=bpy.context.evaluated_depsgraph_get()
report={}
for o in bpy.context.scene.objects:
    if o.type!='MESH' or o.name.startswith('STUDIO'):continue
    m=o.evaluated_get(deps).to_mesh()
    report[o.name]={'local_bounds':[[min(v.co[a] for v in m.vertices),max(v.co[a] for v in m.vertices)] for a in range(3)],'location':list(o.location),'scale':list(o.scale)}
    o.evaluated_get(deps).to_mesh_clear()
    if 'FaceBody' in o.name and o.data.shape_keys:
        report[o.name]['keys']=[(k.name,k.value) for k in o.data.shape_keys.key_blocks]
(root/'tooling'/(name+'-modeled-geometry.json')).write_text(json.dumps(report,indent=2))
print('INSPECT_READY')
