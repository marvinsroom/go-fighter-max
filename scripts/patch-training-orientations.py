import unreal as u

bp = u.load_asset('/Game/Prototype/BP_Fighter')
cdo = u.get_default_object(bp.generated_class())
cdo.get_editor_property('mesh').set_relative_rotation(u.Rotator(pitch=0, yaw=-90, roll=0), False, False)
assert u.BlueprintEditorLibrary.compile_blueprint(bp)
assert u.EditorAssetLibrary.save_loaded_asset(bp)
level = u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
for actor in actors:
    if isinstance(actor, u.CameraActor):
        actor.set_actor_rotation(u.Rotator(pitch=-3, yaw=90, roll=0), False)
        actual = actor.get_actor_rotation()
        assert abs(actual.pitch + 3) < 0.01 and abs(actual.yaw - 90) < 0.01
    elif isinstance(actor, u.TextRenderActor):
        actor.set_actor_rotation(u.Rotator(pitch=0, yaw=-90, roll=0), False)
    elif isinstance(actor, u.DirectionalLight):
        actor.set_actor_rotation(u.Rotator(pitch=-40, yaw=-45, roll=0), False)
    elif actor.get_class().get_name() == 'BP_Fighter_C':
        yaw = 0 if actor.get_editor_property('FighterName') == 'WILL' else 180
        actor.set_actor_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0), False)
        actor.get_editor_property('mesh').set_relative_rotation(u.Rotator(pitch=0, yaw=-90, roll=0), False, False)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(0, -1900, 300), u.Rotator(pitch=-3, yaw=90, roll=0))
assert level.save_current_level()
u.log('TRAINING_ORIENTATION_PATCH_PASSED')
