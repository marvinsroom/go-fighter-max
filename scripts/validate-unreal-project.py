"""Run inside Unreal's Python commandlet, not system Python."""
import json
from pathlib import Path
import unreal

required_assets = [
    '/Game/Variant_SideScroller/Blueprints/BP_SideScrollingCharacter',
    '/Game/Variant_SideScroller/Blueprints/BP_SideScrollingGameMode',
    '/Game/Variant_SideScroller/Blueprints/BP_SideScrollingPlayerController',
    '/Game/Variant_SideScroller/Blueprints/BP_SideScrollingCameraManager',
    '/Game/Variant_SideScroller/Input/IMC_SideScroller',
]
results = {}
for asset_path in required_assets:
    asset = unreal.load_asset(asset_path)
    if asset is None:
        raise RuntimeError('Failed to load ' + asset_path)
    if isinstance(asset, unreal.Blueprint):
        unreal.BlueprintEditorLibrary.compile_blueprint(asset)
        if asset.get_editor_property('status') == unreal.BlueprintStatus.BS_ERROR:
            raise RuntimeError('Blueprint compile failed: ' + asset_path)
    results[asset_path] = 'loaded'

level_path = '/Game/Variant_SideScroller/Lvl_SideScrolling'
level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not level_editor.load_level(level_path):
    raise RuntimeError('Failed to load side-scrolling map')
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
results['map'] = level_path
results['actor_count'] = len(actors)
if len(actors) < 5:
    raise RuntimeError('Unexpectedly empty template level')
project_dir = Path(unreal.Paths.project_dir())
output = project_dir / 'Saved' / 'project-validation.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(results, indent=2), encoding='utf-8')
unreal.log('SITCOM_PROJECT_VALIDATION_PASSED: ' + str(output))
