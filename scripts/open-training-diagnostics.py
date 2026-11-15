import json
import time
from pathlib import Path
import unreal as u

started = time.monotonic()


def tick(delta):
    worlds = u.EditorLevelLibrary.get_pie_worlds(False)
    if not worlds or time.monotonic() - started < 4:
        return
    try:
        world = worlds[0]
        pc = u.GameplayStatics.get_player_controller(world, 0)
        cam = pc.get_view_target()
        manager = pc.player_camera_manager
        report = {
            'target': cam.get_name(),
            'target_position': str(cam.get_actor_location()),
            'target_rotation': str(cam.get_actor_rotation()),
            'view_position': str(manager.get_camera_location()),
            'view_rotation': str(manager.get_camera_rotation()),
            'camera_fov': manager.get_fov_angle(),
            'actors': [a.get_name() for a in u.GameplayStatics.get_all_actors_of_class(world, u.Actor)],
        }
        Path(u.Paths.project_dir(), 'Saved', 'view-diagnostics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        u.SystemLibrary.execute_console_command(world, 'viewmode unlit')
        u.log('VIEW_DIAGNOSTICS_SAVED')
    finally:
        u.unregister_slate_post_tick_callback(handle)


handle = u.register_slate_post_tick_callback(tick)
u.get_editor_subsystem(u.LevelEditorSubsystem).editor_request_begin_play()
