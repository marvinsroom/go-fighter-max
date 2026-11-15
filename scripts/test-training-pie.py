"""Run in a full editor via -ExecCmds='py <path>'; exercise the runtime PIE world."""
import json
import time
import traceback
from pathlib import Path
import unreal as u

started = time.monotonic()
stage = 'starting'
result = {'passed': [], 'failures': []}
out_file = Path(u.Paths.project_dir(), 'Saved', 'training-pie-tests.json')
editor_world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/Prototype/L_TrainingArena')


def verify_world(world):
    cls = u.load_class(None, '/Game/Prototype/BP_Fighter.BP_Fighter_C')
    fighters = sorted(u.GameplayStatics.get_all_actors_of_class(world, cls), key=lambda a: a.get_editor_property('FighterName'), reverse=True)
    assert len(fighters) == 2
    will, prince = fighters
    assert will.get_editor_property('FighterName') == 'WILL'
    pc = u.GameplayStatics.get_player_controller(world, 0)
    assert pc and pc.get_controlled_pawn() == will, 'Player 1 possession'
    result['passed'].append('player 1 possesses the Will placeholder')
    assert isinstance(pc.get_view_target(), u.CameraActor), 'Expected shared camera, got ' + str(pc.get_view_target())
    result['passed'].append('shared camera is the gameplay view target')
    rotation = pc.player_camera_manager.get_camera_rotation()
    assert abs(rotation.pitch + 3) < 0.1 and abs(rotation.yaw + 90) < 0.1, str(rotation)
    result['passed'].append('camera faces the arena rather than the sky')
    mesh_rotation = will.get_editor_property('mesh').get_editor_property('relative_rotation')
    assert abs(mesh_rotation.pitch) < 0.1 and abs(mesh_rotation.yaw + 90) < 0.1, str(mesh_rotation)
    result['passed'].append('mannequin mesh is upright and aligned with gameplay facing')
    assert abs(will.get_actor_location().z - 90) < 12, 'Fighter should rest on floor'
    result['passed'].append('fighter rests on arena floor')
    assert prince.get_editor_property('LeftKey').export_text().find('Left') >= 0
    result['passed'].append('player 2 has separate input bindings')

    def hp(actor):
        return actor.get_editor_property('Health')

    def reset():
        for actor in fighters:
            actor.call_method('ResetFighter')

    def near():
        will.set_actor_location(u.Vector(0, 0, 90), False, True)
        prince.set_actor_location(u.Vector(100, 0, 90), False, True)

    def strike(damage=10.0, reach=150.0):
        will.call_method('QueueAttack', args=(damage, reach, 0.1, 0.24))
        will.call_method('ReceiveTick', args=(0.11,))

    reset()
    assert hp(will) == 100 and hp(prince) == 100
    result['passed'].append('round reset restores both health values')
    will.call_method('QueueAttack', args=(10.0, 150.0, 0.1, 0.24))
    will.call_method('ResolveStrike')
    assert hp(prince) == 100 and will.get_editor_property('AttackPending')
    result['passed'].append('attack cannot deal damage before startup finishes')
    will.call_method('ReceiveTick', args=(0.11,))
    assert hp(prince) == 100
    result['passed'].append('out-of-range strike misses')
    reset()
    near()
    strike()
    assert hp(prince) == 90, 'Expected 10 damage, got ' + str(hp(prince))
    assert not will.get_editor_property('AttackPending')
    result['passed'].append('nearby light strike deals 10 damage')
    will.call_method('ResolveStrike')
    assert hp(prince) == 90
    result['passed'].append('resolved strike cannot hit twice')
    old_cooldown = will.get_editor_property('Cooldown')
    will.call_method('QueueAttack', args=(20.0, 185.0, 0.22, 0.4))
    assert will.get_editor_property('PendingDamage') == 10 and will.get_editor_property('Cooldown') == old_cooldown
    result['passed'].append('recovery prevents another queued attack')
    reset()
    near()
    prince.call_method('SetGuard', args=(True,))
    strike(20.0, 185.0)
    assert hp(prince) == 100
    result['passed'].append('guard blocks damage')
    reset()
    near()
    for _ in range(5):
        will.call_method('ReceiveTick', args=(1.0,))
        strike(20.0, 185.0)
    assert hp(prince) == 0 and not prince.get_actor_enable_collision()
    result['passed'].append('knockout clamps health and disables defeated collision')
    prince.call_method('QueueAttack', args=(20.0, 185.0, 0.22, 0.4))
    assert not prince.get_editor_property('AttackPending')
    result['passed'].append('defeated fighter cannot attack')
    reset()
    assert hp(prince) == 100 and prince.get_actor_enable_collision()
    assert abs(prince.get_actor_location().x - 270) < 1
    result['passed'].append('new round restores position and collision')
    for actor in fighters:
        actor.call_method('UpdateDisplay')
    result['passed'].append('health labels and bars update without errors')


def tick(delta):
    global stage
    try:
        worlds = u.EditorLevelLibrary.get_pie_worlds(False)
        if stage == 'starting' and worlds and time.monotonic() - started > 3:
            stage = 'testing'
            try:
                verify_world(worlds[0])
            except Exception:
                result['failures'].append(traceback.format_exc())
                u.log_error(result['failures'][-1])
            out_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
            u.log('TRAINING_PIE_TEST_RESULT: ' + str(len(result['passed'])) + ' passed, ' + str(len(result['failures'])) + ' failed')
            u.get_editor_subsystem(u.LevelEditorSubsystem).editor_request_end_play()
            stage = 'stopping'
        elif stage == 'stopping' and not worlds:
            u.unregister_slate_post_tick_callback(handle)
            u.SystemLibrary.quit_editor()
        elif time.monotonic() - started > 90:
            result['failures'].append('PIE startup/stop timeout')
            out_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
            u.unregister_slate_post_tick_callback(handle)
            u.SystemLibrary.quit_editor()
    except Exception:
        result['failures'].append(traceback.format_exc())
        out_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
        u.unregister_slate_post_tick_callback(handle)
        u.SystemLibrary.quit_editor()


if __name__ == '__main__':
    handle = u.register_slate_post_tick_callback(tick)
    u.get_editor_subsystem(u.LevelEditorSubsystem).editor_request_begin_play()
