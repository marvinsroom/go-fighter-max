"""Exercise creator command routes and capture native reference animation."""
from pathlib import Path
import json,re,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';C=E/'chars/cid_shadow';S=ROOT/'sprite-fighter/characters/cid'
capture=sys.argv[1] if len(sys.argv)>1 else 'baseline-v2'
assert re.fullmatch(r'[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Use a fresh capture folder for another native take'
commands=['a','b','c','z','y','SKILL 1','SKILL 2','SKILL 3','SKILL 4','SKILL 5','SKILL 6','ATOMIC','holdup','FF','cid_taunt','cid_alpha','cid_beta','cid_garden']
fixture='[Statedef -3]\n'
for i,name in enumerate(commands,1):fixture+=f'[State -3, Reference command]\ntype=AssertCommand\ntrigger1=map(cid.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
fixture+='''
[State -3, Jump input]
type=AssertInput
trigger1=map(cid.jump)>0
flag=U
[State -3, Jump direction]
type=AssertInput
trigger1=map(cid.jump)>0 && map(cid.jumpdir)=1
flag=F
[State -3, Back jump direction]
type=AssertInput
trigger1=map(cid.jump)>0 && map(cid.jumpdir)=-1
flag=B
[State -3, Consume command]
type=MapSet
trigger1=map(cid.pulse)>0
map="cid.pulse"
value=0
[State -3, Walk command]
type=AssertCommand
trigger1=map(cid.walk)>0
name="holdfwd"
[State -3, Walk input]
type=AssertInput
trigger1=map(cid.walk)>0
flag=F
[State -3, Back walk command]
type=AssertCommand
trigger1=map(cid.walkback)>0
name="holdback"
[State -3, Back walk input]
type=AssertInput
trigger1=map(cid.walkback)>0
flag=B
[State -3, Crouch command]
type=AssertCommand
trigger1=map(cid.down)>0
name="holddown"
[State -3, Crouch input]
type=AssertInput
trigger1=map(cid.down)>0
flag=D
[Statedef -2]
[State -2, Keep reference match running]
type=AssertSpecial
triggerall=!ishelper
trigger1=1
flag=globalnoko
ignorehitpause=1
[State -2, Remove attack helpers between cases]
type=DestroySelf
triggerall=ishelper
triggerall=!ishelper(99999999) && !ishelper(999999)
trigger1=root,stateno=99000
ignorehitpause=1
[Statedef 99000]
type=S
movetype=I
physics=N
anim=0
ctrl=0
velset=0,0
[State 99000, Reset position]
type=PosSet
trigger1=1
x=-25
y=0
[State 99000, Clear effects]
type=RemoveExplod
trigger1=1
[State 99000, Clear trails]
type=AfterImageTime
trigger1=1
time=0
[State 99000, Face opponent]
type=Turn
trigger1=facing!=1
[State 99000, Ready]
type=ChangeState
trigger1=time>=3
value=0
ctrl=1
'''
negative3,remaining=fixture.split('[Statedef -2]',1)
negative2,reset=remaining.split('[Statedef 99000]',1)
negative2+='\n[State -2, Observe team cleanup]\ntype=MapSet\ntriggerall=!ishelper\ntrigger1=1\nmap="garden.helpers"\nvalue='+'+'.join(f'numhelper({7950+i})' for i in range(7))+'\n'
ai=(C/'AI.cns').read_text(encoding='utf-8-sig',errors='replace')
ai=ai.replace('[Statedef -3]','[Statedef -3]\n'+negative3.split('[Statedef -3]',1)[1],1)
ai=ai.replace('[Statedef -2]','[Statedef -2]\n'+negative2,1)
(C/'cid-reference-ai.cns').write_text(ai)
(C/'cid-reference-tests.cns').write_text('[Statedef 99000]'+reset)
(C/'cid_test.def').write_text((C/'cid_shadow.def').read_text().replace('st4 = AI.cns','st4 = cid-reference-ai.cns')+'\nst7 = cid-reference-tests.cns\n')
cases=[dict(name='Idle reference',length=140,capture=True),dict(name='Ten-frame walk',walk=True,state=20,length=160,capture=True),
       dict(name='Crouch',down=True,state=11,length=120),dict(name='Jump and landing',pulse=13,jump=True,state=40,length=200),
       dict(name='Forward dash',pulse=14,state=61,length=180)]
for pulse,state,name in [(1,200,'Combo A'),(2,300,'Combo B'),(3,400,'Slash'),(4,1903,'Time-stop teleport'),(5,11230,'Magic blast'),
                         (6,1000,'Simple Hit'),(7,1100,'Back Stab'),(8,1200,'Multi Hit'),(9,1500,'Walk Counter'),(10,1005,'Directional Slash'),(11,1400,'Shadow Garden')]:
    cases.append(dict(name=name,pulse=pulse,state=state,length=600 if pulse in [5,11] else 350,capture=pulse in [1,5]))
cases += [dict(name='Atomic confirmed',pulse=12,state=3000,require=3010,length=1900,damage=True,capture=True),
          dict(name='Atomic blocked',pulse=12,state=3000,forbid=3010,length=260,guard=True),
          dict(name='Atomic insufficient meter',pulse=12,forbid=3000,meter=0,length=140),
          dict(name='All Range Atomic',pulse=12,state=3000,require=3010,lowLife=True,length=1900,damage=True,capture=True),
          dict(name='Final Atomic',pulse=12,state=4000,require=4060,targetLow=True,length=1900,damage=True,capture=True)]
cases += [dict(name='Hood taunt full meter',pulse=15,state=7900,length=200,capture=True,keepPower=3000,recover=True),
          dict(name='Hood taunt empty meter',pulse=15,state=7900,meter=0,length=200,capture=True,keepPower=0,recover=True),
          dict(name='Hood taunt interrupted',pulse=15,state=7900,interrupt=True,length=180,capture=True),
          dict(name='Forward jump proportions',pulse=13,jump=True,jumpdir=1,state=40,length=200,capture=True),
          dict(name='Back jump proportions',pulse=13,jump=True,jumpdir=-1,state=40,length=200,capture=True)]
for case in cases[:5]:case['capture']=True
anatomy='--anatomy' in sys.argv
if anatomy:cases=cases[:5]+cases[-5:]
walking='--walking' in sys.argv
if walking:
    cases=[dict(name='Forward walk and idle',walk=True,state=20,requireAnimation=20,length=300,release=220,capture=True,recover=True),
           dict(name='Backward walk and idle',walkback=True,state=20,requireAnimation=21,length=300,release=220,capture=True,recover=True),
           dict(name='Forward walk short release',walk=True,state=20,requireAnimation=20,length=140,release=53,capture=True,recover=True),
           dict(name='Backward walk short release',walkback=True,state=20,requireAnimation=21,length=140,release=53,capture=True,recover=True)]
smoke='--smoke' in sys.argv
preview='--summon-preview' in sys.argv
summons='--summons' in sys.argv or preview
if summons:
    cases=[]
    for name,pulse,state in [('Alpha',16,7910),('Beta',17,7915)]:
        for suffix,extra in [('super hit',dict(damage=True)),('super blocked',dict(guard=True)),('super misses',dict(far=True)),('super insufficient meter',dict(meter=999)),('super empty meter',dict(meter=0)),('super interrupted',dict(interrupt=True))]:
            insufficient='meter' in suffix
            cases.append(dict(name=name+' '+suffix,pulse=pulse,state=None if insufficient else state,forbid=state if insufficient else None,length=220,capture=True,recover=True,summon=True,**extra))
    if preview:cases=[dict(c,length=160) for c in cases if c['name'].endswith('super hit')]
garden_preview='--garden-preview' in sys.argv
garden='--garden' in sys.argv or garden_preview
if garden:
    cases=[]
    for suffix,extra in [('hit',dict(damage=True,require=7921)),('blocked',dict(guard=True,forbid=7921)),('misses',dict(far=True,forbid=7921)),('insufficient meter',dict(meter=2999,forbid=7920)),('empty meter',dict(meter=0,forbid=7920)),('interrupted',dict(interrupt=True,forbid=7921))]:
        cases.append(dict(name='Seven Shadows ultimate '+suffix,pulse=18,state=None if 'meter' in suffix else 7920,length=460,capture=True,recover=True,garden=True,**extra))
    if garden_preview:cases=[dict(c,length=380) for c in cases if c['name'].endswith(' hit')]
if smoke:
    cases=cases[:5]
    for case in cases:case['capture']=True
case_file='garden-preview-cases.json' if garden_preview else 'garden-test-cases.json' if garden else 'summon-preview-cases.json' if preview else 'summon-test-cases.json' if summons else 'test-cases.json'
(S/case_file).write_text(json.dumps(cases,indent=2))
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
code='''
local cases=CASES
local index,tick,total,shot=1,0,0,0
local seen,minLife,pending={},1000,nil
local seenAnimations={}
local minPower,maxPower,sufferedHit=3000,0,false
local report={method='Native engine; creator command routes through AssertCommand',capture_directory='baseline-v1',checks={},frames={}}
hook.add('loop','cid-reference-tests',function()
 if not player(1) or roundState()~=2 then return end
 local c=cases[index]
 if not c then
  report.status='Complete';report.passed=0;report.failed=0
  for _,r in ipairs(report.checks) do if r.passed then report.passed=report.passed+1 else report.failed=report.failed+1 end end
  jsonEncode(report,'../../characters/cid/runtime-validation.json');print('CID_REFERENCE_COMPLETE '..report.passed..' passed '..report.failed..' failed');os.exit()
 end
 if pending then
  local path='../../characters/cid/replays/baseline-v1/Cid_reference'..string.format('%03d',shot)..'.png'
  local f=io.open(path,'rb');if f then f:close();shot=shot+1;table.insert(report.frames,pending);pending=nil end
 end
 tick=tick+1;total=total+1
 if tick==1 then
  seen={};seenAnimations={};minLife=c.targetLow and 250 or 1000;minPower=3000;maxPower=0;sufferedHit=false
  player(1);mapSet('cid.pulse',0);mapSet('cid.walk',0);mapSet('cid.walkback',0);mapSet('cid.down',0);mapSet('cid.jump',0);mapSet('cid.jumpdir',c.jumpdir or 0);changeState(99000);setLife(c.lowLife and 400 or 1000);setPower(c.meter or 3000)
  if c.garden then for a=0,6 do mapSet('garden.actor'..a,0) end;mapSet('garden.blackout',0);mapSet('garden.finish',0) end
  player(2);mapSet('test.guard',0);mapSet('test.down',0);changeState(9000)
 elseif tick==8 then player(2);setLife(c.targetLow and 250 or 1000);mapSet('test.guard',c.guard and 1 or 0)
  if c.far then changeState(9002) end
 elseif tick==20 then
  player(1);if c.pulse then mapSet('cid.pulse',c.pulse) end
  if c.walk then mapSet('cid.walk',1) end
  if c.walkback then mapSet('cid.walkback',1) end
  if c.down then mapSet('cid.down',1) end
  if c.jump then mapSet('cid.jump',1) end
 end
 if tick==24 then player(1);mapSet('cid.jump',0) end
 if tick==((c.summon or c.garden) and 32 or 70) and c.interrupt then player(2);changeState(200) end
 if tick==(c.release or 110) then player(1);mapSet('cid.walk',0);mapSet('cid.walkback',0);mapSet('cid.down',0) end
 if tick>=20 then player(1);seen[tostring(stateNo())]=true;seenAnimations[tostring(anim())]=true;minPower=math.min(minPower,power());maxPower=math.max(maxPower,power());if life()<1000 then sufferedHit=true end;player(2);minLife=math.min(minLife,life()) end
 if c.capture and tick>10 and not pending and tick%(c.length>1000 and 24 or 4)==0 then
  player(1);local state,animation,powerNow=stateNo(),anim(),power()
  screenshot();player(2)
  pending={index=shot+1,tick=total,case_tick=tick,case_name=c.name,state=state,animation=animation,power=powerNow,target_life=life()}
  if c.garden then pending.target_state=stateNo();player(1);pending.blackout=numExplod(7940);pending.actors={};for a=0,6 do table.insert(pending.actors,tonumber(map('garden.actor'..a)) or 0) end;pending.finish=tonumber(map('garden.finish')) or 0 end
 end
 if tick>=c.length then
  player(1);local final=stateNo();local ok=true
  if c.state and not seen[tostring(c.state)] then ok=false end
  if c.requireAnimation and not seenAnimations[tostring(c.requireAnimation)] then ok=false end
  if c.require and not seen[tostring(c.require)] then ok=false end
  if c.forbid and seen[tostring(c.forbid)] then ok=false end
  if c.recover and final~=0 then ok=false end
  if c.keepPower and (minPower~=c.keepPower or maxPower~=c.keepPower) then ok=false end
  if c.interrupt and (not sufferedHit or not seen['5000']) then ok=false end
  local damage=(c.targetLow and 250 or 1000)-minLife
  player(2);local targetFinal=stateNo();player(1)
  if c.damage and damage<=0 then ok=false end
  if c.summon and not c.forbid and minPower>2000 then ok=false end
  if c.summon and c.forbid and minPower~=(c.meter or 3000) then ok=false end
  if c.guard and c.summon and (damage<=0 or damage>=100) then ok=false end
  if c.far and damage~=0 then ok=false end
  local actors={};if c.garden then
   for a=0,6 do table.insert(actors,tonumber(map('garden.actor'..a)) or 0) end
   if c.damage then
    if damage~=520 or minPower~=0 or map('garden.blackout')~=1 or map('garden.finish')~=1 then ok=false end
    for _,v in ipairs(actors) do if v~=1 then ok=false end end
   end
   if c.guard and damage~=2 then ok=false end
   if c.meter and minPower~=c.meter then ok=false end
   if numExplod(7940)~=0 then ok=false end
   if targetFinal==7929 or targetFinal==7949 then ok=false end
   if map('garden.helpers')~=0 then ok=false end
  end
  table.insert(report.checks,{name=c.name,passed=ok,damage=damage,final_state=final,target_final_state=targetFinal,seen=seen,animations=seenAnimations,min_power=minPower,max_power=maxPower,suffered_hit=sufferedHit,garden_actors=actors,blackout=tonumber(map('garden.blackout')) or 0,finish=tonumber(map('garden.finish')) or 0})
  print('CID_REFERENCE '..index..' '..c.name..' '..tostring(ok)..' damage='..damage)
  jsonEncode(report,'../../characters/cid/runtime-validation.json');index=index+1;tick=0
 end
end)
'''.replace('CASES',lua(cases)).replace('baseline-v1',capture)
if smoke:code=code.replace('runtime-validation.json','runtime-visual-smoke.json')
if anatomy:code=code.replace('runtime-validation.json','runtime-anatomy-v3.json')
if walking:code=code.replace('runtime-validation.json','runtime-walking-v4.json')
if summons:code=code.replace('runtime-validation.json','runtime-summons-v1.json')
if preview:code=code.replace('runtime-summons-v1.json','runtime-summon-preview.json').replace('or 4)==0','or 2)==0')
if garden:code=code.replace('runtime-validation.json','runtime-garden.json')
if garden_preview:code=code.replace('runtime-garden.json','runtime-garden-preview.json').replace('or 4)==0','or 2)==0')
if not anatomy and not walking:code=code.replace('or 4)==0','or 12)==0')
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in C.iterdir() if p.name in ('Cid.air','Cid.sff','Cid.cmd','Cid.cns','Normal Skill.cns','Skills.cns','Atomic.cns','AI.cns','Fx.cns','cid_taunt.cns','cid_summons.cns','cid_garden.cns','cid_shadow.def')}
code=code.replace("local report={method=",'local report={runtime='+lua(runtime)+',method=')
(E/'external/mods/-cid-reference-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-cid-reference-tests.lua'),('WindowTitle','Cid_reference'),('ScreenshotFolder','../../characters/cid/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:
    config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/cid-reference-tests.ini').write_text(config)
print('CID_REFERENCE_TESTS_READY',len(cases))
