import unreal as u

bp = u.load_asset('/Game/Prototype/BP_Fighter')
lib = u.BlueprintEditorLibrary
ed = u.BlueprintGraphEditor.get_graph_editor(lib.find_event_graph(bp))
begin = lib.add_event_override(bp, 'ReceiveBeginPlay', u.IntPoint(-500, -500))
mesh_get = ed.add_get_member_variable_node('Mesh')
rot = ed.add_call_function_node('/Script/Engine.KismetMathLibrary.MakeRotator')
assert rot.find_input_pin('Yaw').set_pin_value('-90')
set_rot = ed.add_call_function_node('/Script/Engine.SceneComponent.K2_SetRelativeRotation')
assert begin.find_then_pin().try_create_connection(set_rot.find_execute_pin())
assert mesh_get.find_output_pin('Mesh').try_create_connection(set_rot.find_self_pin())
assert rot.find_result_pin().try_create_connection(set_rot.find_input_pin('NewRotation'))
assert lib.compile_blueprint(bp)
cdo_mesh = u.get_default_object(bp.generated_class()).get_editor_property('mesh')
cdo_mesh.set_editor_property('relative_rotation', u.Rotator(pitch=0, yaw=-90, roll=0))
assert u.EditorAssetLibrary.save_loaded_asset(bp)
level = u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
font_material = None
for actor in actors:
    label = actor.get_actor_label()
    if isinstance(actor, u.CameraActor):
        actor.set_actor_location(u.Vector(0, 1900, 300), False, True)
        actor.set_actor_rotation(u.Rotator(pitch=-3, yaw=-90, roll=0), False)
    elif label == 'Backdrop':
        actor.set_actor_location(u.Vector(0, -250, 300), False, True)
    elif isinstance(actor, u.TextRenderActor):
        pos = actor.get_actor_location()
        actor.set_actor_location(u.Vector(pos.x, 50, pos.z), False, True)
        actor.set_actor_rotation(u.Rotator(pitch=0, yaw=90, roll=0), False)
        component = actor.get_component_by_class(u.TextRenderComponent)
        if font_material is None:
            original = component.get_editor_property('text_material')
            font_material = u.EditorAssetLibrary.duplicate_asset(original.get_path_name(), '/Game/Prototype/Materials/M_TrainingText')
            assert font_material
            font_material.set_editor_property('two_sided', True)
            u.MaterialEditingLibrary.recompile_material(font_material)
            assert u.EditorAssetLibrary.save_loaded_asset(font_material)
        component.set_text_material(font_material)
    elif actor.get_class().get_name() == 'BP_Fighter_C':
        mesh = actor.get_editor_property('mesh')
        mesh.set_editor_property('relative_rotation', u.Rotator(pitch=0, yaw=-90, roll=0))
        mat = u.load_asset('/Game/Prototype/Materials/M_Teal' if actor.get_editor_property('FighterName') == 'WILL' else '/Game/Prototype/Materials/M_Purple')
        mesh.set_material(0, mat)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(0, 1900, 300), u.Rotator(pitch=-3, yaw=-90, roll=0))
assert level.save_current_level()
u.log('TRAINING_PRESENTATION_PATCH_PASSED')
