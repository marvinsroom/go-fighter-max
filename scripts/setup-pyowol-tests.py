"""Generate native command and recovery checks for Pyo Wol."""
from pathlib import Path
import re,json,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/pyowol';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';C=E/'chars/pyowol'
capture=sys.argv[1] if len(sys.argv)>1 else 'native-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True);assert not list(folder.glob('*.png'))
commands=['L','M','H','snare','daggers','reel','step','veil','super','rain','prison','ultimate','hold_charge']
fixture='[Statedef -3]\n'
for i,name in enumerate(commands,1):fixture+=f'[State -3, Command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\nbuffer.time=1\n'
fixture+='[State -3, Consume]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
for flag,name,button in [('walk','holdfwd','F'),('walkback','holdback','B'),('down','holddown','D'),('jump','holdup','U'),('charge','hold_charge',None)]:
    fixture+=f'[State -3, Held]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{name}"\n'
    if button:fixture+=f'[State -3, Input]\ntype=AssertInput\ntrigger1=map(test.{flag})=1\nflag={button}\n'
fixture+='''[State -3, No KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
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
[State 99000, Face]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear]
type=RemoveExplod
trigger1=1
[State 99000, Cooldowns]
type=VarSet
trigger1=1
var(10)=0
[State 99000, Cooldown]
type=VarSet
trigger1=1
var(11)=0
[State 99000, Ready]
type=ChangeState
trigger1=time>=5
value=0
ctrl=1
'''
(C/'pyowol-tests.cns').write_text(fixture,encoding='utf-8')
(C/'pyowol_test.def').write_text((C/'pyowol.def').read_text()+'\nst1=pyowol-tests.cns\n')
target=E/'chars/will_full'
(target/'pyowol-test-target.cns').write_text((target/'rimuru-test-target.cns').read_text())
(target/'will_pyowol_test.def').write_text((target/'will_hybrid_test.def').read_text()+'\nst3=pyowol-test-target.cns\n')
cases=[dict(name='Thread arrival intro',direct=190,state=190,length=145),dict(name='Idle',length=100),dict(name='Forward walk',walk=True,state=20,length=150),dict(name='Backward walk',walkback=True,state=21,length=150),dict(name='Jump',jump=True,state=40,length=150),dict(name='Charge and release',charge=True,state=500,meter=0,gain=500,length=160)]
build=json.loads((S/'build-report.json').read_text())
for m in build['normal_moves']:
    cases.append(dict(name=m['name'],pulse=1+(m['state']%100)//10,state=m['state'],length=160,damage=True,down=m['kind']=='C',air=m['kind']=='A'))
for p,n,name,cost in [(4,1000,'Silk Snare',250),(5,1100,'Ghost Daggers',500),(6,1120,'Thread Reel',500),(7,1200,'Silent Step',500),(8,1300,'Silken Veil',0),(9,3000,'Soul-Reaping Thread',1000),(10,3100,'Ghost Dagger Rain',1500),(11,3200,'Heavenly Silk Prison',2000),(12,4000,'Reaper of the Drifting Moon',3000)]:
    c=dict(name=name,pulse=p,state=n,length=360 if n==4000 else 240 if n==3200 else 200,damage=n not in (1200,1300))
    cases.append(c)
    if cost:cases.append(dict(c,name=name+' insufficient meter',state=None,forbid=n,meter=cost-1,damage=False,capture=False))
    if n in (1120,3000,3100,3200,4000):
        cases.append(dict(c,name=name+' blocked',guard=True,damage=False,forbid={1120:1121,3200:3201,4000:4001}.get(n),capture=False))
        cases.append(dict(c,name=name+' miss',far=True,damage=False,capture=False))
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Hidden Fang','Silk Snare','Thread Reel','Soul-Reaping Thread','Heavenly Silk Prison','Reaper of the Drifting Moon')]
if '--recovery' in sys.argv:cases=[c for c in cases if c.get('down')]
if '--animation' in sys.argv:
    cases += [
        dict(name='Light medium heavy chain',pulse=1,state=200,length=170,damage=True,chain=[dict(tick=35,pulse=2),dict(tick=53,pulse=3)],require_states=[200,210,220]),
        dict(name='Normal to thread cancel',pulse=1,state=200,length=180,damage=True,chain=[dict(tick=35,pulse=6)],require_states=[200,1120,1121]),
        dict(name='Ultimate facing left',pulse=12,state=4000,length=240,damage=True,facing=-1,require_states=[4000,4001]),
    ]
if '--framing' in sys.argv:cases=[c for c in cases if c['name']=='Ultimate facing left']
if '--hand-retake' in sys.argv:cases=[c for c in cases if c['name'] in ('Thread Reel','Soul-Reaping Thread','Normal to thread cancel')]
if '--ending-retake' in sys.argv:cases=[c for c in cases if c['name'] in ('Light medium heavy chain','Ultimate facing left')]
if '--quiet-retake' in sys.argv:cases=[c for c in cases if c['name'] in ('Reaper of the Drifting Moon','Ultimate facing left')]
if '--silk' in sys.argv:
    for c in cases:
        if c['name'] in ('Silk Finger','Ankle Thread','Air Silk','Thread Reel','Soul-Reaping Thread','Heavenly Silk Prison','Reaper of the Drifting Moon','Ultimate facing left'):
            c['require_threads']=1
(S/('recovery-test-cases.json' if '--recovery' in sys.argv else 'test-cases.json')).write_text(json.dumps(cases,indent=2))
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
template=(ROOT/'scripts/setup-rimuru-tests.py').read_text(encoding='utf-8')
code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0]
code=code.replace('rimuru','pyowol').replace('Rimuru','PyoWol').replace('RIMURU','PYOWOL')
code=code.replace("c.cornerX or -25","c.cornerX or -120").replace("(c.cornerX or -120)*4+(c.facing or 1)*160","(c.cornerX or -120)+(c.facing or 1)*240")
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','if c.forbid and c.meter and minPower~=c.meter then ok=false end')
code=code.replace("name='Running'","name='Running'").replace('tick%(c.dense and 4 or c.direct and 4 or 12)','tick%4')
if '--animation' in sys.argv:
    code=code.replace('tick%4','tick%2')
    code=code.replace('if tick==24 then',"for _,event in ipairs(c.chain or {}) do if tick==event.tick then player(1);mapSet('test.pulse',event.pulse) end end\n if tick==24 then")
    code=code.replace('if c.require and not seen[tostring(c.require)] then ok=false end','if c.require and not seen[tostring(c.require)] then ok=false end\n for _,required in ipairs(c.require_states or {}) do if not seen[tostring(required)] then ok=false end end')
if '--silk' in sys.argv:
    code=code.replace('seen={};minLife=1000',"seen={};maxThreads=0;caseShots=0;lastCaptureKey='';minLife=1000")
    code=code.replace("seen[tostring(stateNo())]=true;", "seen[tostring(stateNo())]=true;maxThreads=math.max(maxThreads,numHelper(8600)+numHelper(8601)+numHelper(8602));")
    code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.damage and minLife>=1000 then ok=false end\n if c.require_threads and maxThreads<c.require_threads then ok=false end')
    code=code.replace('facing=facing(),fx_count=', 'facing=facing(),thread_count=numHelper(8600)+numHelper(8601)+numHelper(8602),fx_count=')
    code=code.replace('damage=1000-minLife,min_power=', 'damage=1000-minLife,max_threads=maxThreads,min_power=')
    # This engine only writes screenshot indices 000..998. Capture pose/life
    # changes plus a periodic hold sample, with <=32 shots per showcase (27
    # showcases => <=864 files), instead of exhausting the counter on idle.
    sample_period=2 if '--animation' in sys.argv else 4
    marker=f" if c.capture~=false and tick>10 and tick%{sample_period}==0 and (tick<450 or c.pulse==7) and not pending then"
    replacement=" player(1);local captureKey=tostring(stateNo())..':'..tostring(spriteVar('image'))..':'..tostring(facing())..':'..tostring(minLife)\n if c.capture~=false and tick>10 and caseShots<32 and not pending and (captureKey~=lastCaptureKey or tick%12==0) then\n  caseShots=caseShots+1;lastCaptureKey=captureKey"
    assert marker in code,'Expected capture hook missing'
    code=code.replace(marker,replacement)
code=code.replace("local report={","local report={runtime_sha256="+lua(build['runtime_sha256'])+',',1)
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
(E/'external/mods/-pyowol-tests.lua').write_text(code,encoding='utf-8')
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-pyowol-tests.lua'),('WindowTitle','PyoWol_native'),('ScreenshotFolder','../../characters/pyowol/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/pyowol-tests.ini').write_text(config);print('PYOWOL_TESTS_READY',len(cases))
