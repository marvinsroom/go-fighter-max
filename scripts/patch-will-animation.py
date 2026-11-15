"""Bypass the mannequin-specific foot Control Rig on the retargeted Will ABP."""
import unreal as u
bp=u.load_asset('/Game/Characters/WillV2/Animations/Will_ABP_Unarmed')
removed=0
for graph in u.BlueprintEditorLibrary.list_graphs(bp):
    ed=u.BlueprintGraphEditor.get_graph_editor(graph)
    for node in ed.list_all_nodes():
        if 'AnimGraphNode_ControlRig' not in node.get_class().get_name():continue
        source=node.find_input_pin('Source');target=node.find_output_pin('Pose')
        assert source.is_valid() and target.is_valid(),'Unexpected Control Rig pose pins'
        upstream=source.list_connected_pins();downstream=target.list_connected_pins()
        assert len(upstream)==1 and downstream,'Missing Control Rig pose links'
        target.break_pin_links()
        for dest in downstream:assert upstream[0].try_create_connection(dest)
        ed.remove_nodes([node]);removed+=1
assert u.BlueprintEditorLibrary.compile_blueprint(bp)
assert u.EditorAssetLibrary.save_loaded_asset(bp)
u.log('WILL_MANNEQUIN_CONTROL_RIG_BYPASSED '+str(removed))
