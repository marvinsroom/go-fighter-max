from pathlib import Path
import json
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(__file__).resolve().parents[1]
folder=root/'characters/will/reference-reconstruction'
bpy.ops.wm.open_mainfile(filepath=str(folder/'will-head-textured-v2.blend'))
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH')
tree=BVHTree.FromPolygons([v.co for v in obj.data.vertices],[list(p.vertices) for p in obj.data.polygons])
report={'bounds':[[min(v.co[a] for v in obj.data.vertices),max(v.co[a] for v in obj.data.vertices)] for a in range(3)],'front_samples':[],'side_samples':[]}
for z in [.08,.10,.12,.14,.16,.175,.18,.185,.19,.195,.20,.21,.22,.24,.26,.28,.30,.32]:
    row={'z':z,'points':[]}
    for x in [0,.02,.03,.035,.04,.045,.05,.055,.06,.07,.08,.09,.10]:
        hit=tree.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
        row['points'].append([x,list(hit[0]) if hit[0] else None])
    report['front_samples'].append(row)
    verts=[v.co for v in obj.data.vertices if abs(v.co.z-z)<.001]
    report['side_samples'].append({'z':z,'bounds':[[min(v[a] for v in verts),max(v[a] for v in verts)] for a in range(3)] if verts else []})
(folder/'detail-probe.json').write_text(json.dumps(report,indent=2))
print('DETAIL_PROBE_READY')
