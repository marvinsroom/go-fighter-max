"""Read-only camera diagnostics. Run in Unreal's Cmd field: py <this file>."""
import json
from pathlib import Path
import unreal as u

editor = u.get_editor_subsystem(u.UnrealEditorSubsystem)
worlds = u.EditorLevelLibrary.get_pie_worlds(False)
world = worlds[0] if worlds else editor.get_editor_world()
report = {'playing': bool(worlds), 'world': world.get_name()}
if worlds:
    pc = u.GameplayStatics.get_player_controller(world, 0)
    if pc:
        target = pc.get_view_target()
        pawn = pc.get_controlled_pawn()
        manager = pc.player_camera_manager
        rotation = manager.get_camera_rotation()
        position = manager.get_camera_location()
        report.update({
            'controlled_pawn': pawn.get_name() if pawn else None,
            'view_target': target.get_name() if target else None,
            'camera_position': {'x': position.x, 'y': position.y, 'z': position.z},
            'camera_rotation': {'pitch': rotation.pitch, 'yaw': rotation.yaw, 'roll': rotation.roll},
            'fov': manager.get_fov_angle(),
            'expected_training_camera_direction': abs(rotation.pitch + 3) < 0.1 and abs(rotation.yaw + 90) < 0.1,
        })
    else:
        report['note'] = 'No player controller found in the play world.'
else:
    report['note'] = 'Play mode is stopped. Press Play or Alt+P to test the arena.'
report['cameras'] = [a.get_name() for a in u.GameplayStatics.get_all_actors_of_class(world, u.CameraActor)]
output = Path(u.Paths.project_dir(), 'Saved', 'view-diagnostics.json')
output.write_text(json.dumps(report, indent=2), encoding='utf-8')
u.log('TRAINING_VIEW_DIAGNOSTICS: ' + json.dumps(report))
u.log('Saved camera report: ' + str(output))
