import unreal as u

lib = u.BlueprintEditorLibrary
bp = u.load_asset('/Game/Prototype/BP_Fighter')
ed = u.BlueprintGraphEditor.create_and_edit_function_graph(bp, 'SetGuard')
ed.add_graph_input_parameter('WantGuard', lib.get_basic_type_by_name('bool'), 'false')
entry = ed.find_graph_entry_pin()
want = entry.get_owning_node().find_output_pin('WantGuard')
setter = ed.add_set_member_variable_node('Blocking')
assert setter.find_input_pin('Blocking').set_pin_value('false')
assert entry.try_create_connection(setter.find_execute_pin())
p = setter.find_then_pin()


def branch(condition):
    global p
    node = ed.add_branch_node()
    assert p.try_create_connection(node.find_execute_pin())
    assert condition.try_create_connection(node.find_condition_pin())
    p = node.find_then_pin()


branch(want)
for variable, operation in [('Health', 'Greater_DoubleDouble'), ('Cooldown', 'LessEqual_DoubleDouble'), ('Hitstun', 'LessEqual_DoubleDouble')]:
    value = ed.add_get_member_variable_node(variable)
    compare = ed.add_call_function_node('/Script/Engine.KismetMathLibrary.' + operation)
    assert value.find_output_pin(variable).try_create_connection(compare.find_input_pin('A'))
    assert compare.find_input_pin('B').set_pin_value('0')
    branch(compare.find_result_pin())
set_true = ed.add_set_member_variable_node('Blocking')
assert set_true.find_input_pin('Blocking').set_pin_value('true')
assert p.try_create_connection(set_true.find_execute_pin())
assert lib.compile_blueprint(bp)
# Route normal keyboard input through the same gameplay function the test calls.
event_ed = u.BlueprintGraphEditor.get_graph_editor(lib.find_event_graph(bp))
for node in event_ed.list_all_nodes():
    value_pin = node.find_input_pin('Blocking')
    if value_pin.is_valid() and node.get_class().get_name() == 'K2Node_VariableSet':
        predecessors = node.find_execute_pin().list_connected_pins()
        successors = node.find_then_pin().list_connected_pins()
        sources = value_pin.list_connected_pins()
        assert len(predecessors) == 1 and len(sources) == 1
        call = event_ed.add_call_function_node('SetGuard')
        node.find_execute_pin().break_pin_links()
        node.find_then_pin().break_pin_links()
        assert predecessors[0].try_create_connection(call.find_execute_pin())
        assert sources[0].try_create_connection(call.find_input_pin('WantGuard'))
        for successor in successors:
            assert call.find_then_pin().try_create_connection(successor)
        event_ed.remove_nodes([node])
assert lib.compile_blueprint(bp)
assert u.EditorAssetLibrary.save_loaded_asset(bp)
u.log('GUARD_INPUT_PATCH_PASSED')
