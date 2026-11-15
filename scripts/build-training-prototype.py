"""Generate a small runtime Blueprint combat prototype using UE 5.8 graph APIs.

Run with UnrealEditor-Cmd -run=pythonscript. Python creates the assets;
all movement and combat thereafter run as normal Blueprint gameplay.
"""
import json
from pathlib import Path
import unreal as u

ROOT = '/Game/Prototype'
LIB = u.BlueprintEditorLibrary
GE = u.BlueprintGraphEditor
ASSETS = u.EditorAssetLibrary
MATH = '/Script/Engine.KismetMathLibrary.'
ENGINE = '/Script/Engine.'


def check(value, message):
    if not value:
        raise RuntimeError(message)
    return value


def inp(node, name):
    pin = node.find_input_pin(name)
    check(pin.is_valid(), 'Missing input ' + name + ' on ' + node.get_name())
    return pin


def out(node, name='ReturnValue'):
    pin = node.find_output_pin(name)
    check(pin.is_valid(), 'Missing output ' + name + ' on ' + node.get_name())
    return pin


def wire(source, dest):
    check(source.try_create_connection(dest), 'Cannot connect ' + str(source.get_pin_name()) + ' to ' + str(dest.get_pin_name()))


def val(node, name, value):
    check(inp(node, name).set_pin_value(str(value)), 'Cannot set ' + name + ' = ' + str(value))
    return node


class Graph:
    def __init__(self, bp, function=None):
        self.bp = bp
        self.ed = GE.create_and_edit_function_graph(bp, function) if function else GE.get_graph_editor(LIB.find_event_graph(bp))
        self.pos = 0

    def place(self, node):
        check(node, 'Node creation failed')
        node.set_node_pos(u.IntPoint((self.pos % 7) * 320, (self.pos // 7) * 240))
        self.pos += 1
        return node

    def call(self, path, **values):
        node = self.place(self.ed.add_call_function_node(path))
        for key, value in values.items():
            if key == 'target':
                key = 'self'
            if isinstance(value, u.BlueprintGraphPin):
                wire(value, inp(node, key))
            else:
                val(node, key, value)
        return node

    def get(self, name, target=None):
        node = self.place(self.ed.add_get_member_variable_node(name, self.bp.generated_class().get_path_name() if target is not None else ''))
        if target is not None:
            wire(target, inp(node, 'self'))
        return out(node, name)

    def set(self, name, value, previous):
        node = self.place(self.ed.add_set_member_variable_node(name))
        if isinstance(value, u.BlueprintGraphPin):
            wire(value, inp(node, name))
        else:
            val(node, name, value)
        wire(previous, node.find_execute_pin())
        return node.find_then_pin()

    def branch(self, previous, condition):
        node = self.place(self.ed.add_branch_node())
        wire(previous, node.find_execute_pin())
        if isinstance(condition, u.BlueprintGraphPin):
            wire(condition, node.find_condition_pin())
        else:
            val(node, 'Condition', condition)
        return node.find_then_pin(), node.find_else_pin()

    def run(self, previous, path, **values):
        node = self.call(path, **values)
        wire(previous, node.find_execute_pin())
        return node.find_then_pin()

    def math(self, name, **values):
        return out(self.call(MATH + name, **values))

    def event(self, name):
        return self.place(LIB.add_event_override(self.bp, name, u.IntPoint(0, 0)))

    def key(self, key, pressed=False):
        pc = out(self.call(ENGINE + 'GameplayStatics.GetPlayerController', PlayerIndex=0))
        return out(self.call(ENGINE + 'PlayerController.' + ('WasInputKeyJustPressed' if pressed else 'IsInputKeyDown'), target=pc, Key=key))


def compile_save(bp):
    check(LIB.compile_blueprint(bp), 'Compile failed: ' + bp.get_path_name())
    check(bp.get_editor_property('status') != u.BlueprintStatus.BS_ERROR, 'Blueprint has errors')
    check(ASSETS.save_loaded_asset(bp), 'Cannot save ' + bp.get_name())


check(not Path(u.Paths.project_dir(), 'Saved', 'training-build.json').exists(), 'Completed prototype already exists; refusing to overwrite')
check(not ASSETS.does_asset_exist(ROOT + '/BP_Fighter'), 'Prototype draft exists; archive before retrying')
bp = check(LIB.create_blueprint_asset_with_parent(ROOT + '/BP_Fighter', u.Character), 'Create fighter')
g = Graph(bp)
key_type = inp(g.call(ENGINE + 'PlayerController.IsInputKeyDown'), 'Key').get_pin_type()
vector_type = out(g.call(MATH + 'MakeVector')).get_pin_type()
for name, kind, default in [
    ('Health', 'real', '100'), ('Cooldown', 'real', '0'), ('Hitstun', 'real', '0'),
    ('Windup', 'real', '0'), ('PendingDamage', 'real', '0'), ('PendingRange', 'real', '0'),
    ('AttackPending', 'bool', 'false'), ('Blocking', 'bool', 'false'),
    ('FighterName', 'string', 'FIGHTER'),
]:
    check(g.ed.add_member_variable(name, LIB.get_basic_type_by_name(kind), default), 'Variable ' + name)
for name, key in [('LeftKey', 'A'), ('RightKey', 'D'), ('JumpKey', 'W'), ('LightKey', 'J'), ('HeavyKey', 'K'), ('GuardKey', 'LeftShift')]:
    check(g.ed.add_member_variable(name, key_type, key), name)
check(g.ed.add_member_variable('StartPosition', vector_type, '(X=0,Y=0,Z=90)'), 'StartPosition')
check(g.ed.add_member_variable('HealthText', LIB.get_object_reference_type(u.TextRenderComponent)), 'HealthText')
check(g.ed.add_member_variable('HealthBar', LIB.get_object_reference_type(u.StaticMeshComponent)), 'HealthBar')
# Remove probe nodes before compiling the real class skeleton.
g.ed.remove_nodes(g.ed.list_all_nodes())
compile_save(bp)
g = Graph(bp)
check(g.ed.add_member_variable('Opponent', LIB.get_object_reference_type(bp.generated_class())), 'Opponent')
for name in ['LeftKey', 'RightKey', 'JumpKey', 'LightKey', 'HeavyKey', 'GuardKey', 'FighterName', 'Opponent', 'HealthText', 'HealthBar', 'StartPosition']:
    LIB.set_blueprint_variable_instance_editable(bp, name, True)
compile_save(bp)

# Define function signatures before wiring cross-function calls.
attack = Graph(bp, 'QueueAttack')
for name in ['Damage', 'Reach', 'Startup', 'Recovery']:
    attack.ed.add_graph_input_parameter(name, LIB.get_basic_type_by_name('real'), '0')
resolve = Graph(bp, 'ResolveStrike')
display = Graph(bp, 'UpdateDisplay')
reset = Graph(bp, 'ResetFighter')
guard_input = Graph(bp, 'SetGuard')
guard_input.ed.add_graph_input_parameter('WantGuard', LIB.get_basic_type_by_name('bool'), 'false')
compile_save(bp)

# Queue an attack only while ready; attack startup, one active hit check, then recovery.
p = attack.ed.find_graph_entry_pin()
ready = attack.math('LessEqual_DoubleDouble', A=attack.get('Cooldown'), B=0)
p, _ = attack.branch(p, ready)
p, _ = attack.branch(p, attack.math('Greater_DoubleDouble', A=attack.get('Health'), B=0))
p, _ = attack.branch(p, attack.math('LessEqual_DoubleDouble', A=attack.get('Hitstun'), B=0))
p, _ = attack.branch(p, attack.math('Not_PreBool', A=attack.get('Blocking')))
entry = attack.ed.find_graph_entry_pin().get_owning_node()
p = attack.set('Cooldown', attack.math('Add_DoubleDouble', A=out(entry, 'Startup'), B=out(entry, 'Recovery')), p)
for name, value in [('Windup', out(entry, 'Startup')), ('PendingDamage', out(entry, 'Damage')), ('PendingRange', out(entry, 'Reach')), ('AttackPending', 'true')]:
    p = attack.set(name, value, p)

# Apply one strike after startup, only if the two capsules are close enough.
p, _ = resolve.branch(resolve.ed.find_graph_entry_pin(), resolve.get('AttackPending'))
p, _ = resolve.branch(p, resolve.math('LessEqual_DoubleDouble', A=resolve.get('Windup'), B=0))
p = resolve.set('AttackPending', 'false', p)
p, _ = resolve.branch(p, resolve.math('Greater_DoubleDouble', A=resolve.get('Health'), B=0))
distance = out(resolve.call(ENGINE + 'Actor.GetDistanceTo', OtherActor=resolve.get('Opponent')))
p, _ = resolve.branch(p, resolve.math('LessEqual_DoubleDouble', A=distance, B=resolve.get('PendingRange')))
location = out(resolve.call(ENGINE + 'Actor.K2_GetActorLocation', target=resolve.get('Opponent')))
p = resolve.run(p, ENGINE + 'KismetSystemLibrary.DrawDebugBox', Center=location, Extent='(X=45,Y=35,Z=75)', LineColor='(R=1,G=0.5,B=0,A=1)', Duration=0.12, Thickness=3)
# ApplyDamage's causer is optional here; no editor-only function is used for game rules.
p = resolve.run(p, ENGINE + 'GameplayStatics.ApplyDamage', DamagedActor=resolve.get('Opponent'), BaseDamage=resolve.get('PendingDamage'))

# Display health in a world-space label and bar. These are deliberately simple placeholder UI.
health_string = out(display.call(ENGINE + 'KismetStringLibrary.BuildString_Double', AppendTo=display.get('FighterName'), Prefix='  HP: ', InDouble=display.get('Health')))
p = display.run(display.ed.find_graph_entry_pin(), ENGINE + 'TextRenderComponent.K2_SetText', target=display.get('HealthText'), Value=health_string)
ratio = display.math('Divide_DoubleDouble', A=display.get('Health'), B=100)
width = display.math('FMax', A=display.math('Multiply_DoubleDouble', A=ratio, B=3), B=0.001)
scale = display.math('MakeVector', X=width, Y=0.12, Z=0.12)
display.run(p, ENGINE + 'SceneComponent.SetRelativeScale3D', target=display.get('HealthBar'), NewScale3D=scale)

# R resets the one-round prototype; Esc remains Unreal's normal exit-PIE shortcut.
p = reset.ed.find_graph_entry_pin()
for name, value in [('Health', 100), ('Cooldown', 0), ('Hitstun', 0), ('Windup', 0), ('Blocking', 'false'), ('AttackPending', 'false')]:
    p = reset.set(name, value, p)
p = reset.run(p, ENGINE + 'Actor.K2_SetActorLocation', NewLocation=reset.get('StartPosition'), bTeleport='true')
movement = reset.get('CharacterMovement')
p = reset.run(p, ENGINE + 'MovementComponent.StopMovementImmediately', target=movement)
p = reset.run(p, ENGINE + 'Actor.SetActorEnableCollision', bNewActorEnableCollision='true')
reset.run(p, ENGINE + 'CharacterMovementComponent.SetMovementMode', target=movement, NewMovementMode='MOVE_Walking')

p = guard_input.set('Blocking', 'false', guard_input.ed.find_graph_entry_pin())
want_guard = out(guard_input.ed.find_graph_entry_pin().get_owning_node(), 'WantGuard')
p, _ = guard_input.branch(p, want_guard)
p, _ = guard_input.branch(p, guard_input.math('Greater_DoubleDouble', A=guard_input.get('Health'), B=0))
for timer in ['Cooldown', 'Hitstun']:
    p, _ = guard_input.branch(p, guard_input.math('LessEqual_DoubleDouble', A=guard_input.get(timer), B=0))
guard_input.set('Blocking', 'true', p)

# Runtime events.
g = Graph(bp)
begin = g.event('ReceiveBeginPlay')
g.run(begin.find_then_pin(), ENGINE + 'SceneComponent.K2_SetRelativeRotation', target=g.get('Mesh'), NewRotation=g.math('MakeRotator', Yaw=-90))
damage = g.event('ReceiveAnyDamage')
p, _ = g.branch(damage.find_then_pin(), g.math('Greater_DoubleDouble', A=g.get('Health'), B=0))
blocked, hit = g.branch(p, g.get('Blocking'))
g.set('Hitstun', 0.08, blocked)
new_hp = g.math('FClamp', Value=g.math('Subtract_DoubleDouble', A=g.get('Health'), B=out(damage, 'Damage')), Min=0, Max=100)
p = g.set('Health', new_hp, hit)
p = g.set('Hitstun', 0.2, p)
p = g.set('AttackPending', 'false', p)
ko, _ = g.branch(p, g.math('LessEqual_DoubleDouble', A=g.get('Health'), B=0))
ko = g.run(ko, ENGINE + 'Actor.SetActorEnableCollision', bNewActorEnableCollision='false')
ko = g.run(ko, ENGINE + 'CharacterMovementComponent.DisableMovement', target=g.get('CharacterMovement'))
g.run(ko, ENGINE + 'KismetSystemLibrary.PrintString', InString='KNOCKOUT - press R for a new round', Duration=4)

tick = g.event('ReceiveTick')
delta = out(tick, 'DeltaSeconds')
p = tick.find_then_pin()
for name in ['Cooldown', 'Hitstun', 'Windup']:
    p = g.set(name, g.math('FMax', A=g.math('Subtract_DoubleDouble', A=g.get(name), B=delta), B=0), p)
p = g.run(p, 'UpdateDisplay')
do_reset, p = g.branch(p, g.key('R', True))
g.run(do_reset, 'ResetFighter')
# Stop both fighters after either player's health reaches zero.
p, _ = g.branch(p, g.math('Greater_DoubleDouble', A=g.get('Health'), B=0))
opponent_active = out(g.call(ENGINE + 'Actor.GetActorEnableCollision', target=g.get('Opponent')))
p, _ = g.branch(p, opponent_active)
pending, after_pending = g.branch(p, g.get('AttackPending'))
due, _ = g.branch(pending, g.math('LessEqual_DoubleDouble', A=g.get('Windup'), B=0))
g.run(due, 'ResolveStrike')
# Movement is locked through attack startup and recovery.
p = after_pending
p, _ = g.branch(p, g.math('LessEqual_DoubleDouble', A=g.get('Hitstun'), B=0))
p, _ = g.branch(p, g.math('LessEqual_DoubleDouble', A=g.get('Cooldown'), B=0))
grounded = out(g.call(ENGINE + 'NavMovementComponent.IsMovingOnGround', target=g.get('CharacterMovement')))
guard = g.math('BooleanAND', A=g.key(g.get('GuardKey')), B=grounded)
p = g.run(p, 'SetGuard', WantGuard=guard)
p, _ = g.branch(p, g.math('Not_PreBool', A=g.get('Blocking')))

# Face the opponent, staying upright when one fighter jumps.
my_pos = out(g.call(ENGINE + 'Actor.K2_GetActorLocation'))
their_pos = out(g.call(ENGINE + 'Actor.K2_GetActorLocation', target=g.get('Opponent')))
my_x = out(g.call(MATH + 'BreakVector', InVec=my_pos), 'X')
their_x = out(g.call(MATH + 'BreakVector', InVec=their_pos), 'X')
yaw = g.math('SelectFloat', A=0, B=180, bPickA=g.math('Greater_DoubleDouble', A=their_x, B=my_x))
rotation = g.math('MakeRotator', Yaw=yaw)
p = g.run(p, ENGINE + 'Actor.K2_SetActorRotation', NewRotation=rotation)
left = g.math('SelectFloat', A=-1, B=0, bPickA=g.key(g.get('LeftKey')))
right = g.math('SelectFloat', A=1, B=0, bPickA=g.key(g.get('RightKey')))
axis = g.math('Add_DoubleDouble', A=left, B=right)
p = g.run(p, ENGINE + 'Pawn.AddMovementInput', WorldDirection='(X=1,Y=0,Z=0)', ScaleValue=axis, bForce='true')
jump, p = g.branch(p, g.key(g.get('JumpKey'), True))
g.run(jump, ENGINE + 'Character.Jump')
# Jump and attacks are separate input opportunities on successive ticks; no auto-repeat while held.
light, p = g.branch(p, g.key(g.get('LightKey'), True))
g.run(light, 'QueueAttack', Damage=10, Reach=150, Startup=0.10, Recovery=0.24)
heavy, _ = g.branch(p, g.key(g.get('HeavyKey'), True))
g.run(heavy, 'QueueAttack', Damage=20, Reach=185, Startup=0.22, Recovery=0.40)

compile_save(bp)
cdo = u.get_default_object(bp.generated_class())
mesh = cdo.get_editor_property('mesh')
mesh.set_skeletal_mesh_asset(check(u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple'), 'Mannequin'))
mesh.set_relative_location(u.Vector(0, 0, -88), False, False)
mesh.set_editor_property('relative_rotation', u.Rotator(pitch=0, yaw=-90, roll=0))
mesh.set_anim_instance_class(check(u.load_class(None, '/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C'), 'Animation BP'))
move = cdo.get_editor_property('character_movement')
for key, value in [('max_walk_speed', 340.0), ('jump_z_velocity', 520.0), ('gravity_scale', 1.6), ('orient_rotation_to_movement', False), ('run_physics_with_no_controller', True), ('constrain_to_plane', True), ('plane_constraint_normal', u.Vector(0, 1, 0))]:
    move.set_editor_property(key, value)
cdo.set_editor_property('use_controller_rotation_yaw', False)
check(ASSETS.save_loaded_asset(bp), 'Save configured fighter defaults')

# Minimal game mode and player controller: no template camera logic or spawned third pawn.
pc_bp = LIB.create_blueprint_asset_with_parent(ROOT + '/BP_TrainingController', u.PlayerController)
u.get_default_object(pc_bp.generated_class()).set_editor_property('auto_manage_active_camera_target', False)
compile_save(pc_bp)
gm_bp = LIB.create_blueprint_asset_with_parent(ROOT + '/BP_TrainingGameMode', u.GameModeBase)
gm = u.get_default_object(gm_bp.generated_class())
gm.set_editor_property('default_pawn_class', None)
gm.set_editor_property('player_controller_class', pc_bp.generated_class())
compile_save(gm_bp)

level = u.get_editor_subsystem(u.LevelEditorSubsystem)
check(level.new_level(ROOT + '/L_TrainingArena'), 'Create level')
actors = u.get_editor_subsystem(u.EditorActorSubsystem)


def spawn(cls, name, xyz, rotation=None):
    actor = check(actors.spawn_actor_from_class(cls, u.Vector(*xyz), rotation or u.Rotator()), name)
    actor.set_actor_label(name)
    return actor


def material(name, color):
    mat = u.AssetToolsHelpers.get_asset_tools().create_asset(name, ROOT + '/Materials', u.Material, u.MaterialFactoryNew())
    expr = u.MaterialEditingLibrary.create_material_expression(mat, u.MaterialExpressionConstant3Vector, -300, 0)
    expr.set_editor_property('constant', u.LinearColor(*color))
    u.MaterialEditingLibrary.connect_material_property(expr, '', u.MaterialProperty.MP_BASE_COLOR)
    u.MaterialEditingLibrary.recompile_material(mat)
    ASSETS.save_loaded_asset(mat)
    return mat


teal = material('M_Teal', (0.02, 0.55, 0.65, 1))
purple = material('M_Purple', (0.48, 0.06, 0.65, 1))
floor_mat = material('M_Floor', (0.08, 0.10, 0.15, 1))
cube = check(u.load_asset('/Engine/BasicShapes/Cube'), 'Cube')


def block(name, pos, scale, mat):
    a = spawn(u.StaticMeshActor, name, pos)
    component = a.static_mesh_component
    component.set_static_mesh(cube)
    component.set_material(0, mat)
    a.set_actor_scale3d(u.Vector(*scale))
    return a


block('Training floor', (0, 0, -25), (22, 6, 0.5), floor_mat)
block('Left boundary', (-1000, 0, 180), (0.4, 6, 4.1), teal)
block('Right boundary', (1000, 0, 180), (0.4, 6, 4.1), purple)
back = block('Backdrop', (0, -250, 300), (22, 0.2, 8), floor_mat)
back.static_mesh_component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
light_actor = spawn(u.DirectionalLight, 'Simple key light', (0, -200, 700), u.Rotator(pitch=-40, yaw=-45, roll=0))
light_actor.light_component.set_editor_property('intensity', 5.0)
light_actor.light_component.set_editor_property('cast_shadows', False)
sky = spawn(u.SkyLight, 'Soft fill', (0, 0, 400))
sky.light_component.set_editor_property('intensity', 1.0)


font_material = None


def label(name, text, pos, size=28, color=None):
    global font_material
    actor = spawn(u.TextRenderActor, name, (pos[0], 50, pos[2]), u.Rotator(pitch=0, yaw=90, roll=0))
    component = actor.get_component_by_class(u.TextRenderComponent)
    if font_material is None:
        original = component.get_editor_property('text_material')
        font_material = check(ASSETS.duplicate_asset(original.get_path_name(), ROOT + '/Materials/M_TrainingText'), 'Text material')
        font_material.set_editor_property('two_sided', True)
        u.MaterialEditingLibrary.recompile_material(font_material)
        ASSETS.save_loaded_asset(font_material)
    component.set_text_material(font_material)
    component.set_text(text)
    component.set_world_size(size)
    component.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER)
    component.set_text_render_color(color or u.Color(235, 235, 245, 255))
    return component


label('Arena title', 'SITCOM FIGHTER  /  TRAINING', (0, -50, 520), 34)
label('P1 controls', 'P1: A/D  W  J/K  LEFT SHIFT', (-430, 50, 475), 24)
label('P2 controls', 'P2: ARROWS  ,/.  RIGHT SHIFT', (430, 50, 475), 24)
label('Reset hint', 'R: NEW ROUND   |   ESC: EXIT PLAY', (0, 50, 340), 24)
fighters = []
for i, (name, x, mat) in enumerate([('WILL', -270, teal), ('PRINCE', 270, purple)]):
    fighter = spawn(bp.generated_class(), name + ' placeholder', (x, 0, 90), u.Rotator(pitch=0, yaw=0 if i == 0 else 180, roll=0))
    fighter.set_editor_property('FighterName', name)
    fighter.get_editor_property('mesh').set_material(0, mat)
    fighter.set_editor_property('StartPosition', u.Vector(x, 0, 90))
    fighter.set_editor_property('auto_possess_player', u.AutoReceiveInput.PLAYER0 if i == 0 else u.AutoReceiveInput.DISABLED)
    fighter.set_editor_property('auto_possess_ai', u.AutoPossessAI.DISABLED)
    if i:
        for prop, key in [('LeftKey', 'Left'), ('RightKey', 'Right'), ('JumpKey', 'Up'), ('LightKey', 'Comma'), ('HeavyKey', 'Period'), ('GuardKey', 'RightShift')]:
            input_key = u.Key()
            check(input_key.import_text(key), 'Parse key ' + key)
            fighter.set_editor_property(prop, input_key)
    hp_text = label(name + ' health', name + '  HP: 100', (-430 if i == 0 else 430, -50, 420), 28)
    bar = block(name + ' health bar', (-430 if i == 0 else 430, 0, 390), (3, 0.12, 0.12), mat)
    bar.static_mesh_component.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
    bar.static_mesh_component.set_mobility(u.ComponentMobility.MOVABLE)
    fighter.set_editor_property('HealthText', hp_text)
    fighter.set_editor_property('HealthBar', bar.static_mesh_component)
    fighters.append(fighter)
fighters[0].set_editor_property('Opponent', fighters[1])
fighters[1].set_editor_property('Opponent', fighters[0])
camera = spawn(u.CameraActor, 'Shared training camera', (0, 1900, 300), u.Rotator(pitch=-3, yaw=-90, roll=0))
camera.set_editor_property('auto_activate_for_player', u.AutoReceiveInput.PLAYER0)
camera.camera_component.set_editor_property('field_of_view', 60.0)
camera.camera_component.set_editor_property('aspect_ratio', 16.0 / 9.0)
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
world.get_world_settings().set_editor_property('default_game_mode', gm_bp.generated_class())
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(0, 1900, 300), u.Rotator(pitch=-3, yaw=-90, roll=0))
check(level.save_current_level(), 'Save training map')
report = {'map': ROOT + '/L_TrainingArena', 'actors': len(actors.get_all_level_actors()), 'fighters': [f.get_actor_label() for f in fighters], 'blueprints_compiled': [bp.get_path_name(), pc_bp.get_path_name(), gm_bp.get_path_name()], 'manual_gameplay_verified': False}
Path(u.Paths.project_dir(), 'Saved', 'training-build.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
u.log('TRAINING_PROTOTYPE_BUILD_PASSED')


