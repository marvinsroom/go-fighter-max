"""Native command-route, meter, guard, whiff and recovery coverage for Edward."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/edward';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/edward'
capture=sys.argv[1] if len(sys.argv)>1 else 'baseline-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('*.png')),'Use fresh directory'
commands=['x','y','z','a','b','c','ed_cannon','ed_gun','ed_pillar','ed_bat','ed_spike','ed_hand','ed_super','ed_wall','ed_barrage','ed_spike_super','ed_final','FF','BB','ed_charge','ed_throw']
variants=[('Cannon Fire Ex',1030,500),('Machine Gun Ex',1130,500),('Stone Pillar Ex',1330,500),('Ed Bat Ex',1430,500),('Stone Spike Ex',1230,500),('Stone Hand Ex',1630,500),('Rapid Fire Cannon Max',3015,2000),('Machine Gun Barrage Max',3005,2000),('Stone Wall Max',3035,2000),('Stone Spike Barrage Max',3025,2000),('Stone Spike Medium',1201,0),('Stone Spike Strong',1202,0)]
commands += [name for name,state,cost in variants]
source=(O/'System.cns').read_text(encoding='cp1252')
inject=''
for i,name in enumerate(commands,1):inject+=f'\n[State -3, Command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
inject+='\n[State -3, Kick modifier]\ntype=AssertCommand\ntrigger1=map(test.pulse)=[4,6]\nname="ed_kickshift"\nbuffer.time=1\n'
inject+='\n[State -3, Consume]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
for flag,name,button in [('walk','holdfwd','F'),('walkback','holdback','B'),('down','holddown','D'),('jump','holdup','U'),('charge','ed_charge',None)]:
    inject+=f'\n[State -3, Held]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{name}"\n'
    if button:inject+=f'\n[State -3, Input]\ntype=AssertInput\ntrigger1=map(test.{flag})=1\nflag={button}\n'
source=source.replace('[Statedef -3]','[Statedef -3]\n'+inject)
cleanup='''
[State -2, Test no KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Test cleanup]
type=DestroySelf
triggerall=ishelper
trigger1=root,stateno=99000
ignorehitpause=1
'''
source=source.replace('[Statedef -2]','[Statedef -2]\n'+cleanup)
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
[State 99000, Direction]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear]
type=RemoveExplod
trigger1=1
[State 99000, Reset variables]
type=VarRangeSet
trigger1=1
first=0
last=57
value=0
[State 99000, Reset floats]
type=VarRangeSet
trigger1=1
first=0
last=39
fvalue=0
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'edward-test-system.cns').write_text(source,encoding='utf-8')
(O/'edward_test.def').write_text((O/'edward.def').read_text().replace('System.cns','edward-test-system.cns'))
T=E/'chars/will_full'
(T/'edward-test-target.cns').write_text((T/'rimuru-test-target.cns').read_text())
(T/'edward-test-common-target.cns').write_text((T/'hybrid-test-target.cns').read_text().replace('x=2000','x=4000'))
(T/'will_edward_test.def').write_text((T/'will_hybrid_test.def').read_text().replace('st2=hybrid-test-target.cns','st2=edward-test-common-target.cns')+'\nst3=edward-test-target.cns\n')
cases=[dict(name='Idle',length=100),dict(name='Forward walk',walk=True,state=20,length=150),dict(name='Backward walk',walkback=True,state=20,length=150),dict(name='Jump',jump=True,state=40,length=150),dict(name='Forward dash',pulse=18,state=110,length=150),dict(name='Backward evade',pulse=19,state=105,length=150)]
for kind,base in [('Standing',200),('Crouching',400),('Air',600)]:
    for i,label in enumerate(['Light punch','Medium punch','Heavy punch','Light kick','Medium kick','Heavy kick']):
        cases.append(dict(name=kind+' '+label,pulse=i+1,state=base+i*10,length=200,down=kind=='Crouching',air=kind=='Air'))
for pulse,state,name in [(7,1000,'Cannon Fire'),(8,1100,'Machine Gun'),(9,1300,'Stone Pillar'),(10,1400,'Ed Bat'),(11,1200,'Stone Spike'),(12,1600,'Stone Hand'),(13,3010,'Rapid Fire Cannon'),(14,3030,'Stone Wall'),(15,3000,'Machine Gun Barrage'),(16,3020,'Stone Spike Barrage'),(17,3100,'Elric Final')]:
    common=dict(name=name,pulse=pulse,state=state,length=600 if pulse==17 else 380,damage=True,distance=100 if pulse==12 else 40)
    cases.append(common)
    if pulse>=13:
        cost=3000 if pulse==17 else 1000
        cases.append(dict(common,name=name+' empty meter',meter=0,state=None,forbid=state,damage=False,capture=False))
        cases.append(dict(common,name=name+' blocked',guard=True,damage=False,capture=False))
        cases.append(dict(common,name=name+' miss',far=True,damage=False,capture=False))
cases += [dict(name='Elric Final facing left',pulse=17,state=3100,require=3105,length=650,damage=True,facing=-1),dict(name='Charge and release',pulse=20,charge=True,state=730,meter=0,gain=100,length=160)]
variant_cases=[]
for i,(name,state,cost) in enumerate(variants,22):
    variant_cases.append(dict(name=name,pulse=i,state=state,length=420,distance=100 if 'Hand' in name else 40))
    if cost:variant_cases.append(dict(name=name+' empty meter',pulse=i,state=None,forbid=state,meter=0,length=140,capture=False))
if '--variants' in sys.argv:cases=variant_cases
elif '--all' in sys.argv:cases+=variant_cases
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ['Idle','Standing Light punch','Cannon Fire','Elric Final','Elric Final facing left','Charge and release']]
if '--whiffs' in sys.argv:cases=[c for c in cases if c.get('far') or c['name']=='Charge and release']
if '--spikes' in sys.argv:
    cases=[c for c in cases if c['name'] in ('Stone Spike','Stone Spike Medium','Stone Spike Strong','Stone Spike Ex','Stone Spike Barrage','Stone Spike Barrage Max')]
    cases += [dict(c,name=c['name']+' facing left',facing=-1) for c in cases if c['name'] in ('Stone Spike','Stone Spike Barrage')]
    for c in cases:c['length']=220 if 'Barrage' not in c['name'] else 380
(S/'test-cases.json').write_text(json.dumps(cases,indent=2))
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
template=(ROOT/'scripts/setup-rimuru-tests.py').read_text()
code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0]
code=code.replace('rimuru','edward').replace('Rimuru','Edward').replace('RIMURU','EDWARD')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*(c.distance or 40))*4')
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','if c.forbid and c.meter and minPower~=c.meter then ok=false end')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
replacement=" player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(minLife)\n if c.capture~=false and tick>10 and caseShots<(c.pulse==17 and 80 or 24) and not pending and ((stateNo()~=0 and tick%3==0 and (key~=lastKey or tick%12==0)) or tick==12 or tick==c.length-4) then\n lastKey=key"
assert marker in code
code=code.replace(marker,replacement)
code=code.replace('player(1);pending={','caseShots=caseShots+1;player(1);pending={')
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256']
code=code.replace('local report={','local report={runtime_sha256='+lua(runtime)+',')
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
(E/'external/mods/-edward-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-edward-tests.lua'),('WindowTitle','Edward_native'),('ScreenshotFolder','../../characters/edward/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/edward-tests.ini').write_text(config)
print('EDWARD_TESTS_READY',len(cases))
