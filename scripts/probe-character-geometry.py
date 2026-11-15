from pathlib import Path
import json
import bpy
import gzip
from bl_ext.blender_org.mpfb.services.targetservice import TargetService
root = Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/modeling-starter/male-character-starter.blend'))
result = {}
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
result['bones'] = {b.name: {'head':list(b.head_local),'tail':list(b.tail_local)} for b in rig.data.bones}
body = bpy.data.objects['EditableMaleBase']
deps = bpy.context.evaluated_depsgraph_get()
eval_body = body.evaluated_get(deps)
mesh = eval_body.to_mesh()
result['bounds'] = {o.name: [list(v) for v in o.bound_box] for o in bpy.data.objects if o.type == 'MESH'}
result['body_modifiers'] = [(m.name,m.type) for m in body.modifiers]
result['face_vertices'] = [list(v.co) for v in mesh.vertices if v.co.z > 1.4]
result['groups'] = [v.name for v in body.vertex_groups]
evaluated = [v.co.copy() for v in body.evaluated_get(deps).data.vertices]
result['landmarks'] = {}
for target in ['mouth-trans-up', 'nose-trans-up', 'l-eye-trans-up', 'r-eye-trans-up', 'chin-height-incr', 'l-ear-scale-incr']:
    filename = TargetService.target_full_path(target)
    with gzip.open(filename, 'rt') as handle:
        indices = [int(line.split()[0]) for line in handle if line.strip() and not line.startswith('#')]
    points = [body.data.shape_keys.key_blocks['Basis'].data[i].co for i in indices]
    # Final coordinates include macro shape keys; read without the masks changing vertex indices.
    coords = [body.data.vertices[i].co.copy() for i in indices]
    for key in body.data.shape_keys.key_blocks[1:]:
        for n,i in enumerate(indices):
            coords[n] += (key.data[i].co - body.data.shape_keys.key_blocks[0].data[i].co) * key.value
    result['landmarks'][target] = {'min':[min(p[a] for p in coords) for a in range(3)],'max':[max(p[a] for p in coords) for a in range(3)],'mean':[sum(p[a] for p in coords)/len(coords) for a in range(3)]}
eval_body.to_mesh_clear()
(root/'tooling/character-geometry.json').write_text(json.dumps(result,indent=2))
print('GEOMETRY_PROBE_READY')
