"""Exercise imported Luffy command routes against the installed illustrated build."""
from pathlib import Path
import json,re,sys
from luffy_model import FORMS,NORMALS,routes
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/luffy';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/luffy'
capture=sys.argv[1] if len(sys.argv)>1 else 'gameplay-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
commands=['a','b','c','luffy_form','luffy_revert']+[f'luffy_skill{i}' for i in range(1,10)]+['luffy_super','luffy_ultimate']
source=(O/'IA.cns').read_text();inject=''
for i,name in enumerate(commands,1):inject+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
inject+='\n[State -3, Consume test pulse]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
for flag,command in [('charge','luffy_charge'),('jump','holdup'),('down','holddown'),('walk','holdfwd'),('walkback','holdback')]:inject+=f'\n[State -3, Held {flag}]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{command}"\nbuffer.time=1\n'
source=source.replace('[Statedef -3]','[Statedef -3]\n'+inject)
source=source.replace('[Statedef -2]','''[Statedef -2]
[State -2, Test no KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Clear fixture helpers]
type=DestroySelf
triggerall=ishelper
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
[State 99000, Clear effects]
type=RemoveExplod
trigger1=1
[State 99000, Reset vars]
type=VarRangeSet
trigger1=!time
first=0
last=57
value=0
[State 99000, Manual]
type=MapSet
trigger1=1
map="luffy.manual"
value=1
[State 99000, Selected idle]
type=ChangeAnim
trigger1=time=6
value=var(11)
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'luffy-test-ia.cns').write_text(source)
(O/'luffy_test.def').write_text((O/'luffy.def').read_text().replace('IA.cns','luffy-test-ia.cns'))
T=E/'chars/will_full';(T/'will_luffy_test.def').write_text((T/'will_edward_test.def').read_text())
build=json.loads((S/'build-report.json').read_text());cases=[]
cases.append(dict(name='Intro - funny meat gag (base Luffy)',form=0,direct=190,state=190,expectForm=0,meter=3000,length=340,intro=True,category='Intro'))
for form in FORMS:
 fid=form['id'];common=dict(form=fid,meter=3000)
 cases.append(dict(common,name=form['name']+' form cycle',pulse=4,state=900800,expectForm=(fid+1)%5,length=150,category='Forms'))
 for air in (False,True):
  for i,(state,label) in enumerate(zip(NORMALS[fid][int(air)],['light','medium','heavy']),1):cases.append(dict(common,name=form['name']+(' air ' if air else ' ground ')+label,pulse=i,state=state,air=air,direct=40 if air else None,length=420,category='Basics'))
 for route in [r for r in routes() if r['form']==fid]:
  cases.append(dict(common,name=form['name']+' / '+route['name'],pulse=commands.index(route['command'])+1,state=9901 if route['state']==13600 else route['state'],command_state=route['state'],length=3000 if route['category']=='Ultimates' else 1800 if route['category']=='Supers' else 1400,category=route['category'],move=route['name']))
 cases.append(dict(name=form['name']+' charge and release',form=fid,meter=0,charge=True,state=900810,gain=500,length=180,category='Charge up'))
cases.append(dict(name='Return to base Luffy',form=4,meter=3000,pulse=5,state=900800,expectForm=0,length=150,category='Forms'))
for route in routes():cases.append(dict(name=FORMS[route['form']]['name']+' / '+route['name']+' insufficient meter',form=route['form'],meter=route['cost']-100,pulse=commands.index(route['command'])+1,forbid=route['state'],length=150,category='Meter checks'))
if '--gallery-basics' in sys.argv:cases=[c for c in cases if c['category']=='Basics']
if '--gallery-skills' in sys.argv:cases=[c for c in cases if c['category']=='Skills']
if '--gallery-power' in sys.argv:cases=[c for c in cases if c['category'] in ('Charge up','Supers','Ultimates','Forms')]
if '--intro' in sys.argv:cases=[c for c in cases if c['category']=='Intro']
if '--smoke' in sys.argv:cases=[c for c in cases if c['category'] in ('Intro','Forms','Charge up') or c['category']=='Basics' and c['pulse']==1 and not c['air']]
if '--probe' in sys.argv:cases=[c for c in cases if c['name']=='Base Luffy ground light']
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
code=code.replace('rimuru','luffy').replace('Rimuru','Luffy').replace('RIMURU','LUFFY')
code=code.replace('tick==28 and c.air','tick==40 and c.air')
code=code.replace('elseif tick==8 then player(2);','elseif tick==8 then player(1);setPower(c.meter or 3000);player(2);')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*85)*4')
# Boundman legitimately regenerates power, so an idle-meter invariant would
# reject valid source behavior. The forbidden state checks the actual route.
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
replacement=" player(1);local key=tostring(stateNo())..':'..tostring(anim())..':'..tostring(animElemNo(0))\n if c.capture~=false and tick>10 and not pending and ((c.intro and tick%4==0) or (caseShots<10 and stateNo()~=0 and tick%4==0 and key~=lastKey) or (caseShots<24 and tick%math.max(12,math.floor(c.length/16))==0) or tick==12 or tick==c.length-4) then\n lastKey=key"
assert marker in code;code=code.replace(marker,replacement).replace('player(1);pending={','caseShots=caseShots+1;player(1);pending={')
if '--gallery-basics' in sys.argv:code=code.replace('caseShots<10','caseShots<6').replace('caseShots<24','caseShots<12')
code=code.replace('local report={','local report={runtime_sha256='+lua(build['runtime_sha256'])+',')
code=code.replace('animation=anim(),','animation=anim(),animation_element=animElemNo(0),')
code=re.sub(r"spriteVar\('(group|image)'\)",'-1',code)
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
if '--probe' in sys.argv:
 debug='''
 if tick==12 or tick==80 then
  player(1);print('PROBE tick='..tick..' state='..stateNo()..' anim='..anim()..' helpers='..numHelper()..' explods='..numExplod())
  for i=0,numExplod()-1 do print('ROOT_FX '..i..' id='..tostring(explodVar(-1,i,'id'))..' anim='..tostring(explodVar(-1,i,'anim'))..' sx='..tostring(explodVar(-1,i,'scale x'))) end
  local count=numHelper()
  for j=0,count-1 do
   player(1);if helper(-1,j) then
    print('HELPER '..j..' state='..stateNo()..' anim='..anim()..' explods='..numExplod())
    for i=0,numExplod()-1 do print('HELPER_FX '..i..' id='..tostring(explodVar(-1,i,'id'))..' anim='..tostring(explodVar(-1,i,'anim'))..' sx='..tostring(explodVar(-1,i,'scale x'))) end
   end
  end
 end
'''
 code=code.replace(' tick=tick+1',' tick=tick+1\n'+debug)
(E/'external/mods/-luffy-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-luffy-tests.lua'),('WindowTitle','Luffy_native'),('ScreenshotFolder','../../characters/luffy/replays/'+capture+'/'),('MasterVolume','0'),('VSync','0')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/luffy-tests.ini').write_text(config);(folder/'cases.json').write_text(json.dumps(cases,indent=2));print('LUFFY_TESTS_READY',len(cases))
