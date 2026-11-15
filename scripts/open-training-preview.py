"""Open a playable training preview in the editor; Esc stops normal PIE."""
import unreal

level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
settings = unreal.GameUserSettings.get_game_user_settings()
settings.set_overall_scalability_level(0)
settings.set_resolution_scale_value_ex(70)
settings.set_frame_rate_limit(60)
settings.apply_non_resolution_settings()
level.editor_request_begin_play()
unreal.log('TRAINING_PREVIEW_REQUESTED')
