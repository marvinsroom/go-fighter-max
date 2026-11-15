"""Native command, recovery, meter and illustration capture checks."""
from pathlib import Path
import json,re,sys
from rimuru_source import ROOT,SOURCE
E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';C=E/'chars/rimuru'
capture=sys.argv[1] if len(sys.argv)>1 else 'illustrated-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=SOURCE/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Choose a fresh capture folder'
commands=['a','b','c','rimuru_flare','rimuru_hell','rimuru_lightning','SUPER1','SPECIAL 3','SPECIAL 4','SPECIAL 6','FF','rimuru_form','rimuru_slash','rimuru_predator','rimuru_blackflame','rimuru_ranga','rimuru_timestop','hold_s']
commands+=['rf_special','rf_forward','rf_back','rf_down','rf_super','rf_super_back','rf_super_forward','rf_ult','rf_form']
fixture=''
for i,name in enumerate(commands,1):fixture+=f'[State -3, Native command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
fixture+='''[State -3, Consume]
type=MapSet
trigger1=map(test.pulse)>0
map="test.pulse"
value=0
[State -3, Walking]
type=AssertCommand
trigger1=map(test.walk)=1
name="holdfwd"
[State -3, Walk input]
type=AssertInput
trigger1=map(test.walk)=1
flag=F
[State -3, Jump input]
type=AssertInput
trigger1=map(test.jump)=1
flag=U
[State -3, Held charge]
type=AssertCommand
trigger1=map(test.charge)=1
name="hold_s"
[State -3, Held crouch]
type=AssertInput
trigger1=map(test.down)=1
flag=D
[State -3, Crouch command]
type=AssertCommand
trigger1=map(test.down)=1
name="holddown"
[State -3, Back walking]
type=AssertInput
trigger1=map(test.walkback)=1
flag=B
[State -3, Back command]
type=AssertCommand
trigger1=map(test.walkback)=1
name="holdback"
'''
ai=(C/'IA.cns').read_text(encoding='utf-8');ai=re.sub(r'(?i)\[statedef -3\]',lambda m:m[0]+'\n'+fixture,ai,count=1)
(C/'test-ai.cns').write_text(ai,encoding='utf-8')
(C/'test-fixture.cns').write_text('''[Statedef -2]
[State -2, No KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Helper reset]
type=DestroySelf
triggerall=ishelper
trigger1=root,stateno=99000
ignorehitpause=1
[Statedef 99000]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 99000, Position]
type=PosSet
trigger1=1
x=map(test.startx)
y=0
[State 99000, Direction]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear]
type=RemoveExplod
trigger1=1
[State 99000, Ready]
type=ChangeState
trigger1=time>=4
value=0
ctrl=1
''',encoding='utf-8')
definition=(C/'rimuru.def').read_text(encoding='utf-8').replace('st1=IA.cns','st1=test-ai.cns').replace('st5=','st5=test-fixture.cns')
(C/'rimuru_test.def').write_text(definition,encoding='utf-8')
target=E/'chars/will_full'
(target/'rimuru-test-target.cns').write_text('''[Statedef 9005]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 9005, Position]
type=PosSet
trigger1=1
x=map(test.startx)
y=0
[State 9005, Direction]
type=Turn
trigger1=facing!=-map(test.facing)
[State 9005, Ready]
type=ChangeState
trigger1=time>=5
value=0
ctrl=1
''',encoding='utf-8')
(target/'will_rimuru_test.def').write_text((target/'will_hybrid_test.def').read_text(encoding='utf-8')+'\nst3=rimuru-test-target.cns\n',encoding='utf-8')
cases=[dict(name='Slime transformation intro',direct=190,state=190,length=160),dict(name='Idle',length=100),dict(name='Walking',walk=True,state=20,length=160),dict(name='Jump',jump=True,state=40,length=160)]
for pulse,state,name in [(1,200,'Katana combo'),(2,220,'Heavy slash'),(3,250,'Magic strike'),(4,1000,'Gluttony'),(5,1100,'Hell Flare'),(6,1400,'Black Lightning'),(8,1200,'Tempest Star Wolf'),(9,1300,'Black Flame'),(10,1500,'Time Stop'),(7,4500,'Megiddo')]:
    cases.append(dict(name=name,pulse=pulse,state=state,length=400 if pulse==7 else 500,damage=pulse not in (10,)))
for suffix,extra in [('blocked',dict(guard=True,forbid=4501)),('miss',dict(far=True,forbid=4501)),('insufficient meter',dict(meter=2999,forbid=4500)),('empty meter',dict(meter=0,forbid=4500))]:
    cases.append(dict(name='Megiddo '+suffix,pulse=7,state=None if 'meter' in suffix else 4500,length=400,**extra))
if '--ultimate' in sys.argv:cases=cases[-5:]
else:
    cases += [dict(name='Charge empty meter and release',pulse=18,charge=True,state=500,meter=0,gain=500,length=180),dict(name='Charge full meter',pulse=18,charge=True,forbid=500,meter=3000,length=130),dict(name='Charge reaches full meter',pulse=18,charge=True,state=500,meter=2900,gain=100,length=160),
        dict(name='Demon Lord transformation',pulse=12,state=7940,expectForm=1,length=130),dict(name='Slime transformation',pulse=12,state=7941,form=1,expectForm=2,length=130),dict(name='Return to masked human',pulse=12,state=7942,form=2,expectForm=0,length=130),dict(name='Demon Lord walking',form=1,walk=True,state=20,expectForm=1,length=160),dict(name='Slime walking',form=2,walk=True,state=20,expectForm=2,length=160),dict(name='Slime magic',form=2,pulse=4,state=1000,expectForm=2,damage=True,length=500),dict(name='Demon Lord Tempest Sever',form=1,pulse=13,state=7960,expectForm=1,damage=True,length=230)]
    for pulse,state,meter,name in [(13,7960,1000,'Tempest Sever'),(14,7970,2000,'Predator Collapse')]:
        for suffix,extra in [('hit',dict(damage=True)),('blocked',dict(guard=True)),('miss',dict(far=True)),('insufficient meter',dict(meter=meter-1,forbid=state))]:
            cases.append(dict(name=name+' '+suffix,pulse=pulse,state=None if suffix=='insufficient meter' else state,length=220,**extra))
if '--forms' in sys.argv:
    build=json.loads((SOURCE/'forms-build.json').read_text());cases=[]
    for form in [2,0,1]:
        for back in [False,True]:cases.append(dict(name=build['forms'][form]+(' backward walk' if back else ' forward walk'),form=form,walk=not back,walkback=back,state=20,expectForm=form,length=270,release=200,dense=True))
    commands_by_offset={0:1,1:2,2:3,10:1,11:2,12:3,20:1,21:2,22:3,30:19,31:20,32:21,33:22,60:23,61:24,62:25,90:26}
    for move in build['moves']:
        form,offset=move['form'],move['offset'];common=dict(form=form,expectForm=form,pulse=commands_by_offset[offset],state=move['state'],length=480 if offset==90 else 180,damage=True,down=move['kind']=='C',air=move['kind']=='A',require=move.get('confirmed'),move_name=move['name'])
        cases.append(dict(common,name=move['form_name']+' / '+move['name']+' hit'))
        if offset>=60:
            for suffix,extra in [('blocked',dict(guard=True,damage=False)),('miss',dict(far=True,damage=False)),('insufficient meter',dict(meter=move['cost']-1,state=None,forbid=move['state'],damage=False))]:
                c=dict(common,name=move['form_name']+' / '+move['name']+' '+suffix,require=None,capture=False,**extra);cases.append(c)
        if offset in (30,60,90):
            for corner in [-1,1]:cases.append(dict(common,name=move['form_name']+' / '+move['name']+(' left corner' if corner==-1 else ' right corner'),cornerX=corner*230,facing=-corner,framing=True))
    cases += [dict(name='Charge empty meter and release',pulse=18,charge=True,state=500,meter=0,gain=500,length=180),dict(name='Charge reaches full meter',pulse=18,charge=True,state=500,meter=2900,gain=100,length=160),dict(name='Demon Lord transformation',pulse=12,state=7940,expectForm=1,length=130),dict(name='Slime transformation',pulse=12,state=7941,form=1,expectForm=2,length=130),dict(name='Return to masked human',pulse=12,state=7942,form=2,expectForm=0,length=130)]
    if '--focus' in sys.argv:cases=cases[:6]+[c for c in cases[6:] if c.get('form')==2 and (c.get('framing') or c.get('air') or c.get('state')==872090)]
    if '--corners' in sys.argv:cases=[c for c in cases if c.get('framing') or (c.get('form')==2 and (c.get('walk') or c.get('walkback')))]
    if '--walks' in sys.argv:cases=[c for c in cases if c.get('form')==2 and (c.get('walk') or c.get('walkback'))]
    if '--cinematics' in sys.argv:cases=[c for c in cases if c.get('state',0) in (870090,871090,872090) or c.get('forbid',0) in (870090,871090,872090)]
    if '--showcase' in sys.argv:
        cases=[c for c in cases if c['name'].endswith(' hit') and c.get('state',0)%1000 in (60,61,62,90)]
        for c in cases:c['dense']=True
    if '--transforms' in sys.argv:cases=[c for c in cases if c['name'] in ('Demon Lord transformation','Slime transformation','Return to masked human')]
(SOURCE/('ultimate-test-cases.json' if '--ultimate' in sys.argv else 'test-cases.json')).write_text(json.dumps(cases,indent=2),encoding='utf-8')
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
code='''local cases=CASES
local index,tick,shot=1,0,0
local seen,minLife,minPower,maxPower,pending={},1000,3000,3000,nil
local report={status='Running',checks={},frames={},capture_directory='CAPTURE'}
hook.add('loop','rimuru-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/rimuru/runtime-validation.json');print('RIMURU_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local f=io.open('../../characters/rimuru/replays/CAPTURE/Rimuru_native'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();shot=shot+1;pending.file='Rimuru_native'..string.format('%03d',shot-1)..'.png';table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1
 if tick==1 then
  seen={};minLife=1000;minPower=c.meter or 3000;maxPower=minPower
  player(1);mapSet('test.startx',c.cornerX or -25);mapSet('test.facing',c.facing or 1);mapSet('rimuru.form',c.form or 0);mapSet('test.charge',0);mapSet('test.down',0);mapSet('test.walkback',0);mapSet('test.pulse',0);mapSet('test.walk',0);mapSet('test.jump',0);changeState(99000);setLife(1000);setPower(c.meter or 3000)
  player(2);mapSet('test.startx',(c.cornerX or -25)*4+(c.facing or 1)*160);mapSet('test.facing',c.facing or 1);mapSet('test.guard',0);selfState(9005);setLife(1000)
 elseif tick==8 then player(2);setLife(1000);mapSet('test.guard',c.guard and 1 or 0);if c.far then selfState(9002) end;player(1);if c.down then mapSet('test.down',1) end
 elseif tick==20 then
  player(1);if c.direct then changeState(c.direct) end;if c.pulse and not c.air then mapSet('test.pulse',c.pulse) end;if c.walk then mapSet('test.walk',1) end;if c.walkback then mapSet('test.walkback',1) end;if c.jump or c.air then mapSet('test.jump',1) end;if c.charge then mapSet('test.charge',1) end
 end
 if tick==24 then player(1);mapSet('test.jump',0) end
 if tick==28 and c.air then player(1);mapSet('test.pulse',c.pulse) end
 if tick==(c.release or 90) then player(1);mapSet('test.walk',0);mapSet('test.walkback',0);mapSet('test.down',0);mapSet('test.charge',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());player(2);minLife=math.min(minLife,life()) end
 if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then
  player(1);pending={case_name=c.name,case_tick=tick,state=stateNo(),animation=anim(),power=power(),form=tonumber(map('rimuru.form')) or 0,screen_x=screenPosX(),screen_y=screenPosY(),group=spriteVar('group'),drawing=spriteVar('image'),facing=facing(),fx_count=numExplod(879100),fx_x=tonumber(map('rimuru.fx_x')) or 0};player(2);pending.target_screen=screenPosX()*.75;pending.target_y=screenPosY()*.75;pending.target_group=spriteVar('group');pending.target_drawing=spriteVar('image');pending.target_anim=anim();pending.target_facing=facing();pending.target_life=life();screenshot()
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=(not c.state or seen[tostring(c.state)]) and (not c.forbid or not seen[tostring(c.forbid)]) and final==0
  if c.meter and minPower~=c.meter then ok=false end
  if c.gain and maxPower<(c.meter or 0)+c.gain then ok=false end
  if c.expectForm and map('rimuru.form')~=c.expectForm then ok=false end
  if c.damage and minLife>=1000 then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.far and minLife<1000 then ok=false end
  player(2);local targetFinal=stateNo();player(1)
  if targetFinal==4510 then ok=false end
  table.insert(report.checks,{name=c.name,passed=ok,seen=seen,final_state=final,target_final_state=targetFinal,damage=1000-minLife,min_power=minPower,max_power=maxPower,form=tonumber(map('rimuru.form')) or 0})
  print('RIMURU '..c.name..' '..tostring(ok)..' final='..final..' damage='..(1000-minLife));jsonEncode(report,'../../characters/rimuru/runtime-validation.json');index=index+1;tick=0
 end
end)
'''.replace('CASES',lua(cases)).replace('CAPTURE',capture)
runtime=json.loads((SOURCE/'build-report.json').read_text(encoding='utf-8'))['runtime_sha256']
code=code.replace('local report={','local report={runtime_sha256='+lua(runtime)+',',1)
(E/'external/mods/-rimuru-tests.lua').write_text(code,encoding='utf-8')
config=(E/'save/prince-paired-tests.ini').read_text(encoding='utf-8')
for key,value in [('Modules','external/mods/-rimuru-tests.lua'),('WindowTitle','Rimuru_native'),('ScreenshotFolder','../../characters/rimuru/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/rimuru-tests.ini').write_text(config,encoding='utf-8');print('RIMURU_TESTS_READY',len(cases))
