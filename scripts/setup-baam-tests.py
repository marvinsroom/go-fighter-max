"""Native physical-input tests, including form continuity and connected combos."""
from baam_model import *
from baam_combat_v3 import ULTIMATE_BASE,ULTIMATE_VIOLE
import re,sys

capture=sys.argv[1] if len(sys.argv)>1 else 'native-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Choose a fresh capture directory'
O=E/'chars/baam';inject=''
buttons=['a','b','c','x','x','x','x','y','y','y','z','w','d','s']
for i,flag in enumerate(buttons,1):inject+=f'\n[State -3, Physical button]\ntype=AssertInput\ntrigger1=map(test.pulse)={i}\nflag={flag}\n'
for name,flag in [('walk','F'),('walkback','B'),('down','D'),('jump','U')]:inject+=f'\n[State -3, Held direction]\ntype=AssertInput\ntrigger1=map(test.{name})=1\nflag={flag}\n'
for n,flag in [(1,'B'),(2,'D'),(3,'F')]:inject+=f'\n[State -3, Skill direction]\ntype=AssertInput\ntrigger1=map(test.inputdir)={n}\nflag={flag}\n'
inject+='\n[State -3, Held charge]\ntype=AssertInput\ntrigger1=map(test.charge)=1\nflag=s\n[State -3, Consume input]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
cns=(O/'baam.cns').read_text().replace('[Statedef -3]','[Statedef -3]\n'+inject)
cns+='''
[Statedef -2]
[State -2, No KO in fixture]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, Remove fixture projectiles]
type=DestroySelf
triggerall=ishelper
trigger1=root,stateno=99000
ignorehitpause=1
[Statedef 99000]
type=S
movetype=I
physics=N
anim=0+1000000*map(baam.form)
ctrl=0
velset=0,0
[State 99000, Place]
type=PosSet
trigger1=1
x=map(test.startx)
y=0
[State 99000, Direction]
type=Turn
trigger1=facing!=map(test.facing)
[State 99000, Clear effects]
type=RemoveExplod
trigger1=1
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'baam-test.cns').write_text(cns)
(O/'baam_test.def').write_text((O/'baam.def').read_text().replace('st=baam.cns','st=baam-test.cns'))
T=E/'chars/will_full'
(T/'baam-test-target.cns').write_text((T/'rimuru-test-target.cns').read_text())
(T/'baam-test-common.cns').write_text((T/'hybrid-test-target.cns').read_text().replace('x=2000','x=4000'))
(T/'will_baam_test.def').write_text((T/'will_hybrid_test.def').read_text().replace('st2=hybrid-test-target.cns','st2=baam-test-common.cns')+'\nst3=baam-test-target.cns\n')
cases=[]
for form in (0,1):
    prefix='Base / ' if not form else 'Viole / '
    for name,params in [('Idle',{}),('Walk',dict(walk=True,state=20)),('Back walk',dict(walkback=True,state=20)),('Jump',dict(jump=True,state=40)),('Evade',dict(pulse=13,state=900,meter=0)),('Charge',dict(pulse=14,charge=True,meter=0,gain=500,state=700))]:cases.append(dict(name=prefix+name,length=160,form=form,expectForm=form,**params))
    for name,pulse,n in [('Light',1,200),('Medium',2,230),('Heavy',3,260),('Low light',1,400),('Low medium',2,410),('Low heavy',3,420),('Air light',1,600),('Air medium',2,610),('Air heavy',3,620)]:
        exact={200:35,230:45,260:80,400:30,410:50,420:70}.get(n)
        cases.append(dict(name=prefix+name,pulse=pulse,state=n,form=form,expectForm=form,down=name.startswith('Low'),air=name.startswith('Air'),damage=not name.startswith('Air'),minDamage=exact,maxDamage=exact,length=200))
    for name,pulse,inputs,states,damage in [('Z Z Z',1,[(36,1),(52,1)],[200,210,220],140),('X X X',2,[(36,2),(53,2)],[230,240,250],170),('Z X C',1,[(36,2),(52,3)],[200,230,260],160)]:
        cases.append(dict(name=prefix+name,pulse=pulse,inputs=[dict(tick=t,pulse=p) for t,p in inputs],requireStates=states,minDamage=damage,form=form,expectForm=form,length=220))
    for i,(name,key,n,cost,label) in enumerate(MOVES,4):
        rawdir={5:3,6:1,7:2,9:1,10:3}.get(i,0)
        common=dict(pulse=i,state=n,form=form,expectForm=form,rawdir=rawdir,length=360 if n==3000 else 250,counter=n in (1200,2100))
        cases.append(dict(common,name=prefix+label,damage=True,require=n+1 if n in (1200,2100,3000) else None,minDamage=(ULTIMATE_VIOLE if form else ULTIMATE_BASE) if n==3000 else 1))
        cases.append(dict(common,name=prefix+label+' facing left',facing=-1,damage=True,require=n+1 if n in (1200,2100,3000) else None,capture=n==3000))
        cases.append(dict(common,name=prefix+label+' insufficient meter',meter=cost-1,state=None,forbid=n,counter=False,capture=False,length=120))
        if n not in (1200,2100):
            cases.append(dict(common,name=prefix+label+' blocked',guard=True,capture=False,maxDamage=50))
            cases.append(dict(common,name=prefix+label+' miss',far=True,capture=False))
cases += [dict(name='Entrance',direct=190,state=190,length=170),dict(name='Transform into Viole',pulse=12,state=800,expectForm=1,length=190),dict(name='Return to base',pulse=12,state=800,form=1,expectForm=0,length=190),dict(name='Viole facing left',pulse=12,state=800,expectForm=1,facing=-1,length=190),dict(name='Interrupted awakening',pulse=12,state=800,probe=35,hurt=True,expectForm=0,length=190),dict(name='Viole survives damage',form=1,probe=40,hurt=True,expectForm=1,length=190),dict(name='Chain on guard',pulse=1,inputs=[dict(tick=36,pulse=1),dict(tick=52,pulse=1)],guard=True,requireStates=[200,210,220],maxDamage=20,length=220),dict(name='Whiff cannot chain',pulse=1,inputs=[dict(tick=36,pulse=1)],forbid=210,far=True,length=180)]
cases += [dict(c,name=c['name']+' facing left',facing=-1) for c in cases if c.get('requireStates') and c['name'].startswith(('Base / ','Viole / '))]
for form in (0,1):
    for facing in (-1,1):
        cases.append(dict(name=('Viole / ' if form else 'Base / ')+'Shinwonryu '+('left wall' if facing<0 else 'right wall'),pulse=11,state=3000,require=3001,damage=True,minDamage=ULTIMATE_VIOLE if form else ULTIMATE_BASE,form=form,expectForm=form,cornerX=80*facing,facing=facing,length=360))
for form in (0,1):
    for facing in (-1,1):
        cases.append(dict(name=('Viole / ' if form else 'Base / ')+'Light into Shinwonryu'+(' facing left' if facing<0 else ''),pulse=1,inputs=[dict(tick=36,pulse=11)],requireStates=[200,3000,3001],minDamage=(ULTIMATE_VIOLE if form else ULTIMATE_BASE)+35,form=form,expectForm=form,facing=facing,length=400))
if '--ultimate' in sys.argv:cases=[c for c in cases if 'Shinwonryu' in c['name']]
if '--impact-check' in sys.argv:cases=[c for c in cases if c['name'] in ('Base / Flow Piercer','Viole / Thorn Wave')]
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Base / Idle','Base / Z Z Z','Base / Shinsu Baang','Base / Shinwonryu','Base / Reverse Flow Control','Transform into Viole','Return to base','Viole survives damage')]
if '--counters' in sys.argv:cases=[c for c in cases if c.get('counter')]
if '--form-start' in sys.argv:cases=[c for c in cases if c['name'] in ('Viole / Idle','Return to base','Viole survives damage')]
if '--presentation' in sys.argv:cases=[c for c in cases if (c.get('requireStates') and c['name'].endswith(' facing left')) or c['name'] in ('Entrance','Transform into Viole','Return to base','Base / Z Z Z','Base / X X X','Base / Z X C') or any(c['name']==prefix+move[4] for prefix in ('Base / ','Viole / ') for move in MOVES) or ('Shinwonryu' in c['name'] and not any(tag in c['name'] for tag in ('blocked',' miss','insufficient')))]
if '--case' in sys.argv:
    selected=sys.argv[sys.argv.index('--case')+1]
    cases=[c for c in cases if c['name']==selected]
    assert cases,('Unknown capture case',selected)
(S/'test-cases.json').write_text(json.dumps(cases,indent=2))
def lua(v):
    if v is None:return 'nil'
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
    if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
    return str(v)
template=(ROOT/'scripts/setup-rimuru-tests.py').read_text()
code=template.split("code='''",1)[1].split("'''.replace('CASES'",1)[0].replace('rimuru','baam').replace('Rimuru','Baam').replace('RIMURU','BAAM')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*40)*(1280/192)')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('if c.meter and minPower~=c.meter','if c.forbid and c.meter and minPower~=c.meter')
code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.damage and minLife>=1000 then ok=false end\n  if c.minDamage and 1000-minLife<c.minDamage then ok=false end\n  if c.maxDamage and 1000-minLife>c.maxDamage then ok=false end\n  for _,s in ipairs(c.requireStates or {}) do if not seen[tostring(s)] then ok=false end end\n  if c.hurt and life()>=1000 then ok=false end')
code=code.replace('passed=ok,seen=seen,','passed=not not ok,seen=seen,final_life=life(),')
code=code.replace("mapSet('test.pulse',0);","mapSet('test.pulse',0);mapSet('test.inputdir',0);")
code=code.replace(' if tick==24 then'," if c.inputs then for _,input in ipairs(c.inputs) do if tick==input.tick then player(1);mapSet('test.pulse',input.pulse) end end end\n if c.probe and tick==c.probe then player(2);selfState(9004) end\n if tick==18 then player(1);mapSet('test.inputdir',c.rawdir or 0) end\n if tick==24 then player(1);mapSet('test.inputdir',0) end\n if tick==36 and c.counter then player(2);selfState(9004) end\n if tick==24 then",1)
code=code.replace('targetFinal==4510','(targetFinal==3050 or targetFinal==3051 or targetFinal==3052)')
code=code.replace("if not player(1) or roundState()~=2 then return end", "if not player(1) then return end\n if roundState()<2 and (stateNo()==190 or stateNo()==191) then report.natural_intro_seen=true;if spriteVar('group')==62200 and spriteVar('image')==2 then report.cuff_adjustment_seen=true end end\n if roundState()~=2 then return end")
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
code=code.replace(marker," player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(minLife)\n if c.capture~=false and tick>10 and caseShots<40 and not pending and ((stateNo()~=0 and tick%4==0 and (stateNo()==800 or key~=lastKey or tick%16==0)) or tick==12 or tick==c.length-4) then\n lastKey=key;caseShots=caseShots+1")
code=code.replace('jsonEncode(report,',"os.remove('../../characters/baam/runtime-validation.json');jsonEncode(report,")
code=code.replace("fx_count=numExplod(879100)","cinematic_tick=time(),fx_count=numExplod(9108)+numExplod(9109)+numExplod(9110)+numExplod(9111)+numExplod(9112)+numExplod(9113)+numExplod(9114)+numExplod(9115),beam_count=numExplod(9112)+numExplod(9113)")
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256']
code=code.replace('local report={','local report={runtime_sha256='+lua(runtime)+',',1)
(E/'external/mods/-baam-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-baam-tests.lua'),('WindowTitle','Baam_native'),('ScreenshotFolder','../../characters/baam/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/baam-tests.ini').write_text(config)
print('BAAM_TESTS_READY',len(cases))
