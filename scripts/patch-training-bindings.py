import re
import unreal as u

bindings = [
    {'LeftKey': 'A', 'RightKey': 'D', 'JumpKey': 'W', 'LightKey': 'J', 'HeavyKey': 'K', 'GuardKey': 'LeftShift'},
    {'LeftKey': 'Left', 'RightKey': 'Right', 'JumpKey': 'Up', 'LightKey': 'Comma', 'HeavyKey': 'Period', 'GuardKey': 'RightShift'},
]


def make_key(name):
    key = u.Key()
    assert key.import_text(name)
    assert key.export_text() == name
    return key


bp = u.load_asset('/Game/Prototype/BP_Fighter')
cdo = u.get_default_object(bp.generated_class())
for prop, name in bindings[0].items():
    cdo.set_editor_property(prop, make_key(name))
for graph in u.BlueprintEditorLibrary.list_graphs(bp):
    ed = u.BlueprintGraphEditor.get_graph_editor(graph)
    for node in ed.list_all_nodes():
        key_pin = node.find_input_pin('Key')
        if key_pin.is_valid() and not key_pin.list_connected_pins():
            # The only literal key in this generated Blueprint is round reset.
            assert key_pin.set_pin_value('R')
assert u.BlueprintEditorLibrary.compile_blueprint(bp)
assert u.EditorAssetLibrary.save_loaded_asset(bp)
level = u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
fighters = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'BP_Fighter_C']
assert len(fighters) == 2
for fighter in fighters:
    index = 0 if fighter.get_editor_property('FighterName') == 'WILL' else 1
    for prop, name in bindings[index].items():
        fighter.set_editor_property(prop, make_key(name))
assert level.save_current_level()
u.log('TRAINING_BINDINGS_PATCH_PASSED')
