"""Pack source textures and verify the exported FBX can be reimported."""
from pathlib import Path
import json
import bpy

out = Path(__file__).resolve().parents[1] / 'characters/modeling-starter'
bpy.ops.wm.open_mainfile(filepath=str(out / 'male-character-starter.blend'))
bpy.ops.file.pack_all()
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(out / 'male-character-starter.blend'))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(out / 'male-character-starter.fbx'))
rigs = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
assert len(rigs) == 1
assert len(rigs[0].data.bones) == 53
assert len(meshes) == 5
for obj in meshes:
    assert any(mod.type == 'ARMATURE' and mod.object == rigs[0] for mod in obj.modifiers), obj.name
    assert any(vertex.groups for vertex in obj.data.vertices), obj.name
report = json.loads((out / 'validation.json').read_text())
report['fbx_roundtrip'] = 'Passed: 53 bones, 5 meshes, armature modifiers and vertex weights retained'
report['source_textures'] = 'Packed into .blend'
(out / 'validation.json').write_text(json.dumps(report, indent=2))
print('FBX_ROUNDTRIP_PASSED')
