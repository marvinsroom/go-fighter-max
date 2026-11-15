"""Create a clothed, editable MPFB starter; this is not a finished likeness."""
from pathlib import Path
import json
import bpy
from mathutils import Vector
from bl_ext.blender_org.mpfb.services.humanservice import HumanService
from bl_ext.blender_org.mpfb.services.targetservice import TargetService
from bl_ext.blender_org.mpfb.services.locationservice import LocationService

root = Path(__file__).resolve().parents[1]
out = root / 'characters/modeling-starter'
out.mkdir(parents=True, exist_ok=True)
source = out / 'male-character-starter.blend'
if source.exists():
    raise RuntimeError('Starter already exists; refusing to overwrite edits.')
data = Path(LocationService.get_user_data())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
macro = TargetService.get_default_macro_info_dict()
macro.update(gender=1.0, age=0.28, muscle=0.55, weight=0.45)
macro['race'] = {'african': 1.0, 'asian': 0.0, 'caucasian': 0.0}
body = HumanService.create_human(scale=0.1, macro_detail_dict=macro)
body.name = 'EditableMaleBase'
rig = HumanService.add_builtin_rig(body, 'game_engine')
HumanService.set_character_skin(str(data / 'skins/young_african_male/young_african_male.mhmat'), body, skin_type='GAMEENGINE')
for relative, asset_type in [
    ('eyes/low-poly/low-poly.mhclo', 'Eyes'),
    ('hair/short01/short01.mhclo', 'Hair'),
    ('clothes/male_casualsuit01/male_casualsuit01.mhclo', 'Clothes'),
    ('clothes/shoes01/shoes01.mhclo', 'Clothes'),
]:
    HumanService.add_mhclo_asset(str(data / relative), body, asset_type=asset_type,
                               subdiv_levels=0, material_type='GAMEENGINE')

meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
for obj in meshes:
    assert any(mod.type == 'ARMATURE' and mod.object == rig for mod in obj.modifiers), obj.name
    assert len(obj.vertex_groups) > 0, obj.name
rig.show_in_front = True
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 720
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.background_type = 'WORLD'
scene.world.color = (0.075, 0.075, 0.075)
bpy.ops.object.camera_add(location=(2.5, -5.0, 2.0))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 0.95)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 2.3
scene.camera = camera
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces.active.region_3d.view_distance = 3.0
        area.spaces.active.region_3d.view_location = (0, 0, 0.95)
        area.spaces.active.region_3d.view_rotation = camera.rotation_euler.to_quaternion()
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes + [rig]:
    obj.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.wm.save_as_mainfile(filepath=str(source))
bpy.ops.export_scene.fbx(filepath=str(out / 'male-character-starter.fbx'),
    use_selection=True, object_types={'ARMATURE', 'MESH'}, add_leaf_bones=False,
    bake_anim=False, path_mode='COPY', embed_textures=True, axis_forward='-Z', axis_up='Y')
report = {'status': 'Generic clothed starter; no character likeness or Unreal retargeting yet',
          'bones': len(rig.data.bones), 'meshes': [{'name': o.name, 'vertices': len(o.data.vertices),
          'vertex_groups': len(o.vertex_groups)} for o in meshes]}
(out / 'validation.json').write_text(json.dumps(report, indent=2))
scene.render.filepath = str(out / 'starter-preview.png')
bpy.ops.render.render(write_still=True)
print('CHARACTER_STARTER_READY', str(source))
