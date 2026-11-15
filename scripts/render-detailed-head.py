"""Render the latest saved detailed head without regenerating or overwriting it."""
from pathlib import Path
import bpy
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
out=root/'characters/will/reference-reconstruction/detailed-v4'
bpy.ops.wm.open_mainfile(filepath=str(out/'will-head-detailed.blend'))
scene=bpy.context.scene
scene.cycles.samples=32
scene.render.resolution_x=1100;scene.render.resolution_y=1100
camera=scene.camera
for name,location in [('three-quarter',(.50,-1,.19)),('front',(0,-1,.17)),('profile',(1,0,.17))]:
    path=out/(name+'.png')
    if path.exists():continue
    camera.location=location
    camera.rotation_euler=(Vector((0,0,.17))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(path)
    bpy.ops.render.render(write_still=True)
print('DETAILED_REVIEW_VIEWS_READY',flush=True)
