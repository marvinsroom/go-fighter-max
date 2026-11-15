"""Real native hit/whiff/launcher/movement-interruption and stage reaction tests."""
from pathlib import Path
import importlib.util,json,concurrent.futures,sys
spec=importlib.util.spec_from_file_location('jus_mobility',Path(__file__).with_name('validate-jus-mobility.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

EXTRA='''
[Statedef 8797192]
type=S
movetype=I
physics=N
ctrl=0
anim=0
velset=0,0
[State 8797192, Target world position]
type=PosSet
trigger1=1
x=const240p(map(justest.worldx))-camerapos x
y=0
[Statedef 8797194]
type=A
movetype=A
physics=N
ctrl=0
anim=8797195
velset=0,0
[State 8797194, Test hit position]
type=PosSet
trigger1=1
x=const240p(6)-camerapos x
y=const240p(-80)
[State 8797194, Actual collision probe]
type=HitDef
trigger1=time=0
attr=A,NA
hitflag=MAF
damage=40
pausetime=0,0
animtype=Light
ground.type=High
ground.hittime=12
ground.velocity=-2,-2
air.hittime=12
air.velocity=-2,-2
fall=1
kill=0
'''

m.LUA='''local report={status='Running',slug='SLUG',checks={},cases={}}
local tick,warmup=0,0
local cases={{name='Native normal connects',x=89,targetx=101}, {name='Whiff never launches',x=0,targetx=210,up=true,whiff=true}, {name='Confirmed normal launches',x=89,targetx=101,up=true,launch=true}}
local index,phase,hit,launched,landed=1,0,false,false,false
local function save() jsonEncode(report,'PROOF') end
local function check(name,ok,actual) table.insert(report.checks,{label=name,passed=ok,actual=actual});save() end
local function reset(air,meter)
 player(1);mapSet('justest.dash',0);mapSet('justest.flight',0);mapSet('justest.up',0);mapSet('justest.worldx',0);mapSet('jus.airdash_used',0);setPower(meter or 2000);setLife(1000);changeState(air and 8797190 or 8797191)
end
local dashHit,dashEntered,flightHit,flightEntered=false,false,false,false
hook.add('loop','jus-combat-SLUG',function()
 if not player(1) or roundState()~=2 then return end
 if warmup<70 then warmup=warmup+1;return end
 if tick==0 and 'SLUG'=='rimuru' then
  table.insert(cases,{name='Demon Lord confirmed normal launches',x=89,targetx=101,up=true,launch=true,form=1})
  table.insert(cases,{name='Slime confirmed normal launches',x=89,targetx=101,up=true,launch=true,form=2})
 end
 tick=tick+1
 local c=cases[index]
 if c then
  phase=phase+1
  if phase==1 then
   reset(false);mapSet('justest.worldx',c.x)
   if 'SLUG'=='rimuru' then mapSet('rimuru.form',c.form or 0) end
   player(2);mapSet('justest.worldx',c.targetx);mapSet('jus.launched',0);mapSet('jus.launch_request',0);setLife(1000);changeState(8797192);player(1)
   hit=false;launched=false;landed=false
  end
  if phase==12 then
   if c.up then mapSet('justest.up',1) end
   changeState(ATTACK)
  end
  if phase>12 then
   player(2);if life()<1000 then hit=true end
   if stateNo()==8797103 then launched=true end
   if launched and posY()>=0 then landed=true end
   player(1)
  end
  if phase==70 then screenshot() end
  if phase==180 then
   if c.whiff then check(c.name,not hit and not launched,{hit=hit,launched=launched})
   elseif c.launch then
    check(c.name,hit and launched,{hit=hit,launched=launched})
    check('Launched victim returns to ground',not launched or landed,landed)
   else
    check(c.name,hit,hit)
    check('Arena slab reacts to actual nearby fighter hit',map('jus.prop_right')>0,map('jus.prop_right'))
   end
   table.insert(report.cases,{name=c.name,hit=hit,launched=launched,landed=landed})
   mapSet('justest.up',0);index=index+1;phase=0;save()
  end
  return
 end
 phase=phase+1
 if phase==1 then reset(true);player(2);mapSet('justest.worldx',150);changeState(8797192);player(1) end
 if phase==7 then mapSet('justest.dash',1) end
 if phase==9 then
  dashEntered=stateNo()==8797101
  mapSet('justest.dash',0);player(2);changeState(8797194);player(1)
 end
 if phase>=10 and phase<=20 and life()<1000 and stateNo()~=8797101 then dashHit=true end
 if phase==25 then
  check('Dash command entered before collision',dashEntered,dashEntered)
  if 'SLUG'~='saitama' then check('Air dash remains vulnerable to a real HitDef',dashHit,{hit=dashHit,hp=life(),state=stateNo()})
  else report.source_exception='Original Saitama source intentionally rejects damage; no added JUS invulnerability.' end
  reset(true)
 end
 if phase==32 then mapSet('justest.flight',1) end
 if phase==35 then
  flightEntered=stateNo()==8797102;mapSet('justest.flight',0)
  player(2);changeState(8797194);player(1)
 end
 if phase>=36 and phase<=50 and life()<1000 and stateNo()~=8797102 then flightHit=true end
 if phase==55 then
  if FLIGHT==1 then
   check('Flight entered before collision',flightEntered,flightEntered)
   check('Real hit interrupts flight',flightHit,{hit=flightHit,hp=life(),state=stateNo()})
  end
  screenshot()
 end
 if phase==65 then
  report.status='Complete';report.passed=0;report.failed=0
  for _,v in ipairs(report.checks) do if v.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  save();os.exit()
 end
end)
'''

def execute(row):
 original=m.LUA
 # The source uses a grounded heavy kick for Mori's existing verified normal.
 # Each worker receives its own source string; no shared mutation during runs.
 # ATTACK is evaluated in Lua from the slug to keep workers independent.
 return m.run(row,'native-combat')

if __name__=='__main__':
 m.LUA=m.LUA.replace('ATTACK',"('SLUG'=='jin-mori' and 230 or 200)")
 fixture=m.FIXTURE.replace('x=0\ny=0','x=const240p(map(justest.worldx))\ny=0')
 fixture=fixture.replace('[Statedef 8797190]','[State -4, Keep contact tests alive]\ntype=AssertSpecial\ntrigger1=1\nflag=globalnoko\n[Statedef 8797190]')
 if '--diagnose-props' in sys.argv:
  probes=''
  for key,expr in [('exists','1'),('time','time'),('enemy_dx','p2dist x'),('manual_dx','enemynear,pos x-pos x'),('parent_dx','parent,pos x-pos x'),('limit','const240p(24)'),('enemy_life','enemynear,life'),('previous_life','map(jus.prop_enemy_life)'),('hurt','enemynear,movetype=H'),('damage','map(jus.prop_damage)'),('x','pos x'),('enemy_x','enemynear,pos x')]:
   probes+=f'\n[State -4, Probe slab {key}]\ntype=ParentMapSet\ntrigger1=ishelper(8797111)\nmap="justest.prop.{key}"\nvalue={expr}\nignorehitpause=1\n'
  fixture=fixture.replace('[Statedef 8797190]',probes+'\n[Statedef 8797190]')
  observe='''if index==1 and phase>=10 and phase<=42 then
   local v={phase=phase,root_x=posX(),root_state=stateNo()}
   for _,key in ipairs({'exists','time','enemy_dx','manual_dx','parent_dx','limit','enemy_life','previous_life','hurt','damage','x','enemy_x'}) do v[key]=map('justest.prop.'..key) end
   player(2);v.target_life=life();v.target_x=posX();v.target_state=stateNo();player(1)
   report.prop_probe=report.prop_probe or {};table.insert(report.prop_probe,v)
  end
  '''
  m.LUA=m.LUA.replace('if phase==12 then',observe+'if phase==12 then')
 (m.E/'data/jus-test-fixture.cns').write_text(fixture+EXTRA)
 (m.E/'data/jus-test-fixture.air').write_text('[Begin Action 8797195]\nClsn1Default: 1\nClsn1[0]=-250,-400,250,50\nClsn2Default: 1\nClsn2[0]=-60,-300,60,0\n0,0,0,0,-1\n')
 all_rows=json.loads((m.O/'manifest.json').read_text())['fighters'];rows=[r for r in all_rows if len(sys.argv)==1 or r['slug'] in sys.argv[1:]]
 results=[];errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  jobs={pool.submit(execute,r):r['slug'] for r in rows}
  for job in concurrent.futures.as_completed(jobs):
   try:results.append(job.result())
   except Exception as e:errors.append(dict(slug=jobs[job],error=str(e)));print('FAILED',jobs[job],e,flush=True)
 combined=m.collect(all_rows,'native-combat')
 (m.O/'native-combat-validation.json').write_text(json.dumps(dict(status='Complete' if len(combined)==len(all_rows) and not errors else 'In progress',fighters=combined,errors=errors),indent=2))
 if errors or any(r['failed'] for r in results):raise SystemExit(1)
