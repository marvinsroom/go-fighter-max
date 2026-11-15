"""Exercise real command controllers, transformations and source finishers."""
from pathlib import Path
import json,re,sys
from ichigo_model import FORMS
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/ichigo';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/ichigo'
capture=sys.argv[1] if len(sys.argv)>1 else 'native-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
commands=['a','b','c','ichigo_form','ichigo_revert']+[f'ichigo_skill{i}' for i in range(1,7)]+['ichigo_super','ichigo_ultimate']
source=(O/'IA.cns').read_text();inject=''
for i,name in enumerate(commands,1):inject+=f'\n[State -3, Command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
inject+='\n[State -3, Consume]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
inject+='\n[State -3, Hold charge]\ntype=AssertCommand\ntrigger1=map(test.charge)=1\nname="ichigo_charge"\nbuffer.time=1\n'
for flag,command in [('jump','holdup'),('down','holddown'),('walk','holdfwd'),('walkback','holdback')]:
 inject+=f'\n[State -3, Held {flag}]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{command}"\nbuffer.time=1\n'
source=source.replace('[Statedef -3]','[Statedef -3]\n'+inject)
source=source.replace('[Statedef -2]','''[Statedef -2]
[State -2, No KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Clear fixture helpers]
type=DestroySelf
triggerall=ishelper && !ishelper(999999)
trigger1=root,stateno=99000
ignorehitpause=1
''',1)
source+='''
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
[State 99000, Facing]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear]
type=RemoveExplod
trigger1=1
[State 99000, Reset]
type=VarRangeSet
trigger1=!time
first=0
last=57
value=0
[State 99000, Form]
type=VarSet
trigger1=1
var(2)=map(ichigo.form)
[State 99000, Manual]
type=MapSet
trigger1=1
map="ichigo.manual"
value=1
[State 99000, Selected form idle]
type=ChangeAnim
trigger1=time=6
value=var(11)
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'ichigo-test-ia.cns').write_text(source)
(O/'ichigo_test.def').write_text((O/'ichigo.def').read_text().replace('IA.cns','ichigo-test-ia.cns'))
T=E/'chars/will_full'
(T/'will_ichigo_test.def').write_text((T/'will_edward_test.def').read_text())
report=json.loads((S/'build-report.json').read_text());cases=[]
# Read the actual ground/air normal routes rather than guessing state offsets.
normals={}
for block in re.split(r'(?=^\[State\s+-1,)',(O/'Ichigo.cmd').read_text(),flags=re.I|re.M):
 form=re.search(r'var\(2\)\s*=\s*(\[\s*\d+\s*,\s*\d+\s*\]|\d+)',block,re.I)
 button=re.search(r'command\s*=\s*"([abc])"',block,re.I)
 value=re.search(r'^value\s*=\s*(\d+)\s*(\+\s*var\(11\))?\s*$',block,re.I|re.M)
 if form and button and value:
  airborne=bool(re.search(r'statetype\s*=\s*A\b',block,re.I))
  ids=list(map(int,re.findall(r'\d+',form[1])))
  if len(ids)==2:ids=list(range(ids[0],ids[1]+1))
  for fid in ids:
   offset=next(f['base'] for f in FORMS if f['id']==fid) if value[2] else 0
   normals[fid,button[1].lower(),airborne]=int(value[1])+offset
for i,f in enumerate(FORMS):
 common=dict(form=f['id'],meter=10000)
 cases.append(dict(common,name=f['name']+' transform',pulse=4,state=900800,expectForm=FORMS[(i+1)%len(FORMS)]['id'],length=130))
 for airborne in (False,True):
  for pulse,(button,label) in enumerate(zip('abc',('light','medium','heavy')),1):
   state=normals.get((f['id'],button,airborne))
   assert state is not None,('Missing normal route',f['name'],button,airborne)
   cases.append(dict(common,name=f['name']+(' air ' if airborne else ' ')+label+' slash',pulse=pulse,state=state,air=airborne,direct=40 if airborne else None,length=300 if airborne else 200))
 for route in [x for x in report['shortcut_routes'] if x['form']==f['id']]:
  cases.append(dict(common,name=f['name']+' '+route['input'].replace('ichigo_',''),pulse=commands.index(route['input'])+1,state=route['state'],length=2000 if route['input']=='ichigo_ultimate' else 700))
cases.append(dict(name='Return to Shikai',form=11,pulse=5,state=900800,expectForm=0,meter=0,length=130))
cases.insert(0,dict(name='Intro - school uniform into Bankai',form=0,direct=190,state=191,expectForm=2,meter=10000,length=280,intro=True))
for f in FORMS:
 cases.append(dict(name=f['name']+' charge and release',form=f['id'],meter=0,charge=True,state=900810,gain=500,length=180))
for route in report['shortcut_routes']:
 if route['cost']>0:
  cases.append(dict(name=next(f['name'] for f in FORMS if f['id']==route['form'])+' '+route['input'].replace('ichigo_','')+' insufficient meter',form=route['form'],meter=route['cost']-1,pulse=commands.index(route['input'])+1,forbid=route['state'],length=130))
if '--utility' in sys.argv:cases=[c for c in cases if c.get('charge') or c.get('forbid')]
if '--showcase' in sys.argv:cases=[c for c in cases if c['name'].endswith('ultimate')]
if '--visual' in sys.argv:
 cases=[c for c in cases if c.get('expectForm') is not None or c['name'].endswith(('light slash','ultimate')) or c['name'].endswith('skill'+str(c['form']%6+1))]
if '--gallery-basics' in sys.argv:cases=[c for c in cases if c['name'].endswith('slash')]
if '--gallery-skills' in sys.argv:cases=[c for c in cases if 6<=c.get('pulse',0)<=11 and not c.get('forbid')]
if '--gallery-power' in sys.argv:cases=[c for c in cases if c.get('expectForm') is not None or c.get('charge') or c['name'].endswith(('super','ultimate'))]
if '--intro' in sys.argv:cases=[c for c in cases if c.get('intro')]
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Shikai transform','Hollow mask transform','True Bankai + Horn transform','Return to Shikai')]
if '--forms' in sys.argv:cases=[c for c in cases if c.get('expectForm') is not None]
if '--ultimates' in sys.argv:cases=[c for c in cases if c['name'].endswith('ultimate')]
if '--skills' in sys.argv:cases=[c for c in cases if 'skill' in c['name'] or 'slash' in c['name'] or c['name'].endswith('super')]
if '--no-capture' in sys.argv:
 for c in cases:c['capture']=False
def lua(v):
 if v is None:return 'nil'
 if isinstance(v,bool):return str(v).lower()
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
template=(R/'scripts/setup-rimuru-tests.py').read_text();code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0]
code=code.replace('rimuru','ichigo').replace('Rimuru','Ichigo').replace('RIMURU','ICHIGO')
code=code.replace('c.meter or 3000','c.meter or 10000')
code=code.replace('tick==28 and c.air','tick==40 and c.air')
# Mugetsu's source var(47) drains meter before the reset state's controllers
# clear it. Restore the next fixture's meter after that reset has completed.
code=code.replace('elseif tick==8 then player(2);','elseif tick==8 then player(1);setPower(c.meter or 10000);player(2);')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*55)*4')
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','if c.forbid and c.meter and minPower~=c.meter then ok=false end')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
replacement=" player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))\n if c.capture~=false and tick>10 and not pending and ((caseShots<8 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<18 and tick%math.max(12,math.floor(c.length/12))==0) or tick==12 or tick==c.length-4) then\n lastKey=key"
assert marker in code;code=code.replace(marker,replacement).replace('player(1);pending={','caseShots=caseShots+1;player(1);pending={')
code=code.replace('((caseShots<8 and', '((c.intro and tick%4==0) or (caseShots<8 and')
if '--gallery-basics' in sys.argv or '--gallery-skills' in sys.argv:code=code.replace('caseShots<8','caseShots<4').replace('caseShots<18','caseShots<8')
code=code.replace('local report={','local report={runtime_sha256='+lua(report['runtime_sha256'])+',')
code=code.replace('animation=anim(),','animation=anim(),animation_element=animElemNo(0),')
code=code.replace("tostring(spriteVar('group'))","tostring(spriteVar('group') or -1)").replace("tostring(spriteVar('image'))","tostring(spriteVar('image') or -1)")
# Engine spriteVar dereferences a nil sprite during source invisibility frames.
# Capture actual engine pixels; animation/state IDs are safe throughout those.
code=re.sub(r"spriteVar\('(group|image)'\)",'-1',code)
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
(E/'external/mods/-ichigo-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-ichigo-tests.lua'),('WindowTitle','Ichigo_native'),('ScreenshotFolder','../../characters/ichigo/replays/'+capture+'/'),('MasterVolume','0'),('VSync','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/ichigo-tests.ini').write_text(config)
(folder/'cases.json').write_text(json.dumps(cases,indent=2));print('ICHIGO_TESTS_READY',len(cases))
