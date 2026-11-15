"""Real rendered PIE checks, arena regression tests and same-scene performance comparison."""
from pathlib import Path
import importlib.util,json,time,traceback,statistics,subprocess
import unreal as u
root=Path(u.Paths.project_dir()).parent;out=root/'characters/will/integration-v1'
exec(compile((root/'scripts/apply-will-character.py').read_text(),str(root/'scripts/apply-will-character.py'),'exec'))
exec(compile((root/'scripts/patch-will-animation.py').read_text(),str(root/'scripts/patch-will-animation.py'),'exec'))
spec=importlib.util.spec_from_file_location('training_checks',root/'scripts/test-training-pie.py')
checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
result={'passed':[],'failures':[],'performance':{},'scope':'Rendered editor PIE, same fixed arena camera, uncapped, low DX11 settings. Not packaged-game performance.'}
start=time.monotonic();phase='start';phase_start=start;samples=[];last_tick=start
def save(): (out/'runtime-validation.json').write_text(json.dumps(result,indent=2))
def gpu():
    try:return subprocess.check_output(['C:/Windows/System32/nvidia-smi.exe','--query-gpu=name,memory.used,memory.total,utilization.gpu','--format=csv,noheader,nounits'],text=True,creationflags=0x08000000).strip()
    except Exception:return 'Unavailable'
def mark(name,condition):
    assert condition,name
    result['passed'].append(name)
def switch(name):
    global phase,phase_start,samples
    phase=name;phase_start=time.monotonic();samples=[];save();u.log('WILL_TEST_PHASE '+name)
def stats(label):
    vals=sorted(samples)
    result['performance'][label]={'frames':len(vals),'mean_frame_ms':statistics.mean(vals)*1000,'mean_fps':1/statistics.mean(vals),
        'p95_frame_ms':vals[min(len(vals)-1,int(len(vals)*.95))]*1000,'gpu_name_usedMiB_totalMiB_utilizationPercent':gpu()}
    save()
def tick(delta):
    global last_tick,will,prince,comp,world,head_start,walk_x,jump_z,max_jump,phase
    now=time.monotonic();elapsed=now-phase_start;dt=now-last_tick;last_tick=now
    try:
        worlds=u.EditorLevelLibrary.get_pie_worlds(False)
        if phase=='start' and worlds and now-start>5 and u.GameplayStatics.get_time_seconds(worlds[0])>3:
            world=worlds[0]
            cls=u.load_class(None,'/Game/Prototype/BP_Fighter.BP_Fighter_C')
            fighters=u.GameplayStatics.get_all_actors_of_class(world,cls)
            will=next(a for a in fighters if a.get_editor_property('FighterName')=='WILL')
            prince=next(a for a in fighters if a.get_editor_property('FighterName')=='PRINCE')
            comp=will.get_editor_property('mesh')
            mark('Will custom mesh survives BeginPlay',comp.get_skeletal_mesh_asset().get_name()=='SK_Will')
            mark('Retargeted Will animation blueprint active',comp.get_anim_instance() is not None and 'Will_ABP_Unarmed' in comp.get_anim_instance().get_class().get_name())
            mark('Prince still uses original mannequin',prince.get_editor_property('mesh').get_skeletal_mesh_asset().get_name()=='SKM_Manny_Simple')
            result['runtime_materials']=[comp.get_material(i).get_path_name() if comp.get_material(i) else None for i in range(comp.get_num_materials())]
            mark('Will has all imported material assignments',all(p and p.startswith('/Game/Characters/WillV2/Materials/') for p in result['runtime_materials']))
            result['bones']=comp.get_num_bones()
            mark('Will skeleton retains weighted body bones',result['bones']>=53)
            checks.verify_world(world);result['passed']+=checks.result['passed']
            will.call_method('ResetFighter');prince.call_method('ResetFighter')
            result['will_local_bounds']=str(comp.get_skeletal_mesh_asset().get_bounds())
            head_start=comp.get_socket_transform('head',u.RelativeTransformSpace.RTS_COMPONENT).translation
            u.SystemLibrary.execute_console_command(world,'t.MaxFPS 0')
            u.SystemLibrary.execute_console_command(world,'r.VSync 0')
            u.SystemLibrary.execute_console_command(world,'t.IdleWhenNotForeground 0')
            u.SystemLibrary.execute_console_command(world,'Slate.bAllowThrottling 0')
            switch('will_warmup')
        elif phase=='will_warmup' and elapsed>12:
            head=comp.get_socket_transform('head',u.RelativeTransformSpace.RTS_COMPONENT).translation
            result['idle_head_displacement_cm']=(head-head_start).length()
            result['idle_bone_positions_cm']={bone:str(comp.get_socket_transform(bone,u.RelativeTransformSpace.RTS_COMPONENT).translation) for bone in ['Root','pelvis','spine_03','neck_01','head','clavicle_l','hand_l','foot_l']}
            shoulder=comp.get_socket_transform('clavicle_l',u.RelativeTransformSpace.RTS_COMPONENT).translation
            mark('Head is positioned above shoulders',head.z>shoulder.z+10 and 110<head.z<190)
            switch('will_measure')
        elif phase=='will_measure':
            samples.append(dt)
            if elapsed>8 and len(samples)>120:
                stats('Will_custom');comp.set_skeletal_mesh_asset(u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple'))
                comp.set_anim_instance_class(u.load_class(None,'/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C'))
                comp.set_editor_property('override_materials',[]);switch('mannequin_warmup')
        elif phase=='mannequin_warmup' and elapsed>8:switch('mannequin_measure')
        elif phase=='mannequin_measure':
            samples.append(dt)
            if elapsed>8 and len(samples)>120:
                stats('Original_mannequin');comp.set_skeletal_mesh_asset(u.load_asset('/Game/Characters/WillV2/SK_Will'))
                comp.set_anim_instance_class(u.load_class(None,'/Game/Characters/WillV2/Animations/Will_ABP_Unarmed.Will_ABP_Unarmed_C'))
                comp.set_editor_property('override_materials',[])
                walk_x=will.get_actor_location().x;switch('walking')
        elif phase=='walking':
            will.add_movement_input(u.Vector(1,0,0),1,False)
            if elapsed>1:
                mark('Rigged fighter moves across arena',will.get_actor_location().x>walk_x+50)
                result['walking_velocity']=str(will.get_velocity())
                mark('Locomotion animation instance remains active',comp.get_anim_instance() is not None)
                jump_z=will.get_actor_location().z;max_jump=jump_z;will.jump();switch('jumping')
        elif phase=='jumping':
            max_jump=max(max_jump,will.get_actor_location().z)
            if elapsed>2:
                result['jump_height_cm']=max_jump-jump_z;mark('Rigged fighter jumps',max_jump>jump_z+30)
                mark('Rigged fighter lands again',abs(will.get_actor_location().z-jump_z)<12)
                will.call_method('ResetFighter');prince.call_method('ResetFighter')
                u.SystemLibrary.execute_console_command(world,'t.MaxFPS 60')
                u.SystemLibrary.execute_console_command(world,'stat unit')
                u.SystemLibrary.execute_console_command(world,'stat RHI')
                switch('final_capture')
        elif phase=='final_capture' and elapsed>3:
            u.SystemLibrary.execute_console_command(world,'Shot');save();switch('review_camera')
        elif phase=='review_camera' and elapsed>3:
            pc=u.GameplayStatics.get_player_controller(world,0);camera=pc.get_view_target()
            origin=will.get_actor_location()
            camera.set_actor_location(origin+u.Vector(300,160,55),False,True)
            camera.set_actor_rotation(u.MathLibrary.find_look_at_rotation(camera.get_actor_location(),origin+u.Vector(0,0,20)),False)
            switch('review_capture')
        elif phase=='review_capture' and elapsed>3:
            u.SystemLibrary.execute_console_command(world,'Shot');switch('finish')
        elif phase=='finish' and elapsed>2:
            u.get_editor_subsystem(u.LevelEditorSubsystem).editor_request_end_play();switch('stopping')
        elif phase=='stopping' and not worlds:
            result['status']='Passed' if not result['failures'] else 'Failed';save()
            u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
        if now-start>160:raise RuntimeError('Rendered PIE validation timed out')
    except Exception:
        result['failures'].append(traceback.format_exc());result['status']='Failed';save();u.log_error(result['failures'][-1])
        if worlds:u.SystemLibrary.execute_console_command(worlds[0],'t.MaxFPS 60')
        u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
handle=u.register_slate_post_tick_callback(tick)
u.get_editor_subsystem(u.LevelEditorSubsystem).editor_request_begin_play()
