"""Render an orthographic source face for entirely local landmark fitting."""
from pathlib import Path
import json
import math
import bpy

root=Path(__file__).resolve().parents[1]
out=root/'characters/will/local-head-fit-v1'
out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'characters/will/v2/will.blend'))
body=bpy.data.objects['Will_FaceBody']
coords=[v.co.copy() for v in body.data.shape_keys.key_blocks[0].data]
for key in body.data.shape_keys.key_blocks[1:]:
    for i,v in enumerate(key.data):
        coords[i]+=(v.co-body.data.shape_keys.key_blocks[0].data[i].co)*key.value
bodygroup=body.vertex_groups['body'].index
indices=set(v.index for v in body.data.vertices if any(g.group==bodygroup and g.weight>.5 for g in v.groups))
H=max(coords[i].z for i in indices);s=H/1.52405
scene=bpy.context.scene
camera=scene.camera
camera.location=(0,-3,1.42*s);camera.rotation_euler=(math.pi/2,0,0)
camera.data.ortho_scale=.42*s
scene.render.resolution_x=840;scene.render.resolution_y=840
scene.cycles.samples=16
scene.render.filepath=str(out/'source-front.png')
(out/'source-geometry.json').write_text(json.dumps({
    'vertices':[list(v) for v in coords],
    'polygons':[list(p.vertices) for p in body.data.polygons if all(i in indices for i in p.vertices)],
    'skin_indices':sorted(indices),'camera_z':camera.location.z,'ortho_scale':camera.data.ortho_scale,'scale':s},indent=None))
bpy.ops.render.render(write_still=True)
print('LOCAL_SOURCE_READY',flush=True)
