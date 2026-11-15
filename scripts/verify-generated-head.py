"""Verify the portable GLB contains geometry, UVs and its base-color texture."""
from pathlib import Path
import json
import bpy

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/reference-reconstruction'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(out/'will-head-textured-v2.glb'))
meshes=[o for o in bpy.data.objects if o.type=='MESH']
assert meshes,'No mesh in exported GLB'
triangles=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in meshes)
assert 85000<=triangles<=95000,triangles
assert all(len(o.data.uv_layers)>0 for o in meshes),'Missing UV coordinates'
assert any(i.size[0]==2048 and i.size[1]==2048 for i in bpy.data.images),'Missing 2048px texture'
assert all(o.data.materials for o in meshes),'Missing material'
(out/'export-validation.json').write_text(json.dumps({'status':'Passed','triangles':triangles,
    'uv_coordinates':True,'embedded_texture':[2048,2048],
    'limitation':'Geometry/texture portability only; not a likeness or animation approval'},indent=2))
print('GENERATED_HEAD_GLB_VERIFIED',triangles,flush=True)
