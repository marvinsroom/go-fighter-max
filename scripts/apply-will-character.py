"""Replace only Will's level-instance visual; preserve the playable fighter logic."""
from pathlib import Path
import json
import unreal as u
out=Path(u.Paths.project_dir()).parent/'characters/will/integration-v1'
level=u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
will=next(a for a in actors if a.get_class().get_name()=='BP_Fighter_C' and a.get_editor_property('FighterName')=='WILL')
mesh=will.get_editor_property('mesh')
model=u.load_asset('/Game/Characters/WillV2/SK_Will')
anim=u.load_class(None,'/Game/Characters/WillV2/Animations/Will_ABP_Unarmed.Will_ABP_Unarmed_C')
assert model and anim,'Import and retarget must finish before changing the level'
for slot in model.materials:
    mat=slot.material_interface
    if mat:
        mat.set_editor_property('used_with_skeletal_mesh',True)
        u.EditorAssetLibrary.save_loaded_asset(mat)
backup=out/'level-visual-backup.json'
if not backup.exists():
    backup.write_text(json.dumps({'mesh':mesh.get_skeletal_mesh_asset().get_path_name(),
        'anim_class':mesh.get_editor_property('anim_class').get_path_name(),
        'override_materials':[m.get_path_name() if m else None for m in mesh.get_editor_property('override_materials')]},indent=2))
mesh.set_skeletal_mesh_asset(model);mesh.set_editor_property('override_materials',[])
mesh.set_anim_instance_class(anim)
mesh.set_editor_property('relative_rotation',u.Rotator(pitch=0,yaw=-90,roll=0))
mesh.set_relative_location(u.Vector(0,0,-88),False,False)
fill=next((a for a in actors if a.get_actor_label()=='Character face fill'),None)
if not fill:
    fill=u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(u.DirectionalLight,u.Vector(0,300,400),u.Rotator(pitch=-20,yaw=135,roll=0))
    fill.set_actor_label('Character face fill')
fill.light_component.set_editor_property('intensity',1.8)
fill.light_component.set_editor_property('cast_shadows',False)
fill.light_component.set_mobility(u.ComponentMobility.MOVABLE)
assert level.save_current_level()
probe={'mesh_bounds':str(model.get_bounds()),
       'animation_api':{name:str(getattr(u.AnimSequence,name).__doc__) for name in dir(u.AnimSequence) if 'bone' in name or 'pose' in name},
       'animation_helpers':[n for n in dir(u) if 'AnimationPose' in n or 'AnimPose' in n]}
(out/'level-visual-integration.json').write_text(json.dumps(probe,indent=2))
u.log('WILL_LEVEL_VISUAL_APPLIED')
