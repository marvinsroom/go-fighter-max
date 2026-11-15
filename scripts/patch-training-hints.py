import unreal as u
level = u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
changes = {
    'P1 controls': ('P1: A/D  W  J/K  LEFT SHIFT', -430, 475),
    'P2 controls': ('P2: ARROWS  ,/.  RIGHT SHIFT', 430, 475),
    'Reset hint': ('R: NEW ROUND   |   ESC: EXIT PLAY', 0, 340),
}
for actor in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if actor.get_actor_label() in changes:
        text, x, z = changes[actor.get_actor_label()]
        actor.set_actor_location(u.Vector(x, 50, z), False, True)
        comp = actor.get_component_by_class(u.TextRenderComponent)
        comp.set_text(text)
        comp.set_world_size(24)
assert level.save_current_level()
u.log('TRAINING_HINTS_PATCH_PASSED')
