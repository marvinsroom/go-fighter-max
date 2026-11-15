"""Open the saved training arena and leave it playable for the user."""
import unreal as u
level=u.get_editor_subsystem(u.LevelEditorSubsystem)
assert level.load_level('/Game/Prototype/L_TrainingArena')
u.SystemLibrary.execute_console_command(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(),'t.MaxFPS 60')
level.editor_request_begin_play()
u.log('TRAINING_ARENA_READY_FOR_USER')
