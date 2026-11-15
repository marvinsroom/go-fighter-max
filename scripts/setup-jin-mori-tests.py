"""Native input-route, guard, whiff, meter and recovery checks with captures."""
from jin_mori_assets import *
import re,sys,hashlib

capture=sys.argv[1] if len(sys.argv)>1 else 'baseline-v1'
assert re.fullmatch('[a-z0-9-]+',capture)
folder=S/'replays'/capture;folder.mkdir(parents=True,exist_ok=True)
assert not list(folder.glob('*.png')),'Use a fresh capture directory'
O=E/'chars/jin_mori'
commands=['a','b','c','mori_sword','mori_tortoise','mori_azure','mori_triple','mori_twin','mori_tempest','mori_ultimate','mori_dodge','s','FF','BB','mori_transform']
inject=''
for i,name in enumerate(commands,1):
    if '--physical' in sys.argv and (i<=12 or i==15):
        flag={1:'a',2:'b',3:'c',4:'x',5:'x',6:'y',7:'y',8:'y',9:'y',10:'z',11:'d',12:'s',15:'w'}[i]
        inject+=f'\n[State -3, Raw button]\ntype=AssertInput\ntrigger1=map(test.pulse)={i}\nflag={flag}\n'
    else:inject+=f'\n[State -3, Pulse]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{name}"\n'
for direction,flag in [(1,'B'),(2,'D'),(3,'F')]:
    inject+=f'\n[State -3, Raw direction]\ntype=AssertInput\ntrigger1=map(test.inputdir)={direction}\nflag={flag}\n'
inject+='\n[State -3, Clear]\ntype=MapSet\ntrigger1=map(test.pulse)>0\nmap="test.pulse"\nvalue=0\n'
for flag,name,button in [('walk','holdfwd','F'),('walkback','holdback','B'),('down','holddown','D'),('jump','holdup','U'),('charge','hold_s',None)]:
    inject+=f'\n[State -3, Held]\ntype=AssertCommand\ntrigger1=map(test.{flag})=1\nname="{name}"\n'
    if button:inject+=f'\n[State -3, Input]\ntype=AssertInput\ntrigger1=map(test.{flag})=1\nflag={button}\n'
cns=(O/'Jin Mori.cns').read_text(encoding='utf-8')
cns=cns.replace('[Statedef -3]','[Statedef -3]\n'+inject)
cns+='''
[Statedef -2]
[State -2, no KO]
type=AssertSpecial
trigger1=!ishelper
flag=globalnoko
[State -2, cleanup]
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
[State 99000, clear]
type=RemoveExplod
trigger1=1
[State 99000, Ready]
type=ChangeState
trigger1=time>=6
value=0
ctrl=1
'''
(O/'mori-test.cns').write_text(cns,encoding='utf-8')
(O/'mori_test.def').write_text((O/'jin_mori.def').read_text().replace('Jin Mori.cns','mori-test.cns'),encoding='utf-8')
T=E/'chars/will_full'
(T/'mori-test-target.cns').write_text((T/'rimuru-test-target.cns').read_text())
(T/'mori-test-common-target.cns').write_text((T/'hybrid-test-target.cns').read_text().replace('x=2000','x=4000'))
(T/'will_mori_test.def').write_text((T/'will_hybrid_test.def').read_text().replace('st2=hybrid-test-target.cns','st2=mori-test-common-target.cns')+'\nst3=mori-test-target.cns\n')
cases=[dict(name='Idle',length=80),dict(name='Forward walk',walk=True,state=20,length=150),dict(name='Backward walk',walkback=True,state=20,length=150),dict(name='Jump',jump=True,state=40,length=150),dict(name='Dash',pulse=13,state=100,length=180),dict(name='Evade',pulse=11,state=340,length=150)]
for i,state,label in [(1,230,'Light chain'),(2,270,'Medium chain'),(3,310,'Heavy chain')]:
    cases.append(dict(name=label,pulse=i,state=state,damage=True,length=260))
    cases.append(dict(name='Air '+label,pulse=i,state={1:630,2:660,3:680}[i],air=True,length=250))
cases.append(dict(name='Low sweep',pulse=1,state=320,down=True,length=220,damage=True))
for pulse,state,name,cost in [(4,1000,'Moonlight Sword Style',1000),(5,1500,'Black Tortoise',1000),(6,2000,'Azure Dragon Kick',1500),(7,3500,'Triple Kick',1500),(8,2500,'Twin Dragon Kick',2000),(9,3000,'Blue Dragon Tempest',2000),(10,4500,'Monkey King',3000)]:
    common=dict(name=name,pulse=pulse,state=state,length=360 if pulse==10 else 580,damage=True,counter=pulse==4)
    if pulse==10:common.update(require=4501,minDamage=500)
    cases.append(common)
    cases.append(dict(common,name=name+' facing left',facing=-1))
    cases.append(dict(common,name=name+' insufficient meter',meter=cost-1,state=None,forbid=state,damage=False,counter=False,require=None,minDamage=None,capture=False,length=140))
    cases.append(dict(common,name=name+' blocked',guard=True,damage=False,counter=False,require=None,minDamage=None,capture=False))
    cases.append(dict(common,name=name+' miss',far=True,damage=False,counter=False,require=None,minDamage=None,capture=False))
cases.append(dict(name='Charge and release',pulse=12,charge=True,state=400,meter=0,gain=100,length=200))
cases += [dict(name='Entrance',direct=190,state=190,length=180),dict(name='Transform into Monkey King',pulse=15,state=980500,expectForm=1,length=180),dict(name='Return to Jin Mori',pulse=15,state=980500,form=1,expectForm=0,length=180),dict(name='Transformation facing left',pulse=15,state=980500,expectForm=1,facing=-1,length=180),dict(name='Transformation interrupted',pulse=15,state=980500,expectForm=0,probe=35,length=200,hurt=True),dict(name='Monkey King takes a hit',form=1,expectForm=1,probe=40,hurt=True,length=200)]
for name,pulse,inputs,required,damage in [('Z Z Z chain',1,[(36,1),(52,1)],[230,240,250],140),('X X X chain',2,[(36,2),(53,2)],[270,280,290],190),('Z X C chain',1,[(36,2),(52,3)],[230,260,310],160),('Normal to Azure Dragon',1,[(36,2),(52,6)],[230,260,2000],350)]:
    common=dict(name=name,pulse=pulse,inputs=[dict(tick=t,pulse=p) for t,p in inputs],requireStates=required,minDamage=damage,damage=True,length=580 if 'Azure' in name else 240)
    cases.append(common)
    cases.append(dict(common,name=name+' facing left',facing=-1))
cases += [dict(name='Chain on guard',pulse=1,inputs=[dict(tick=36,pulse=1),dict(tick=52,pulse=1)],requireStates=[230,240,250],guard=True,maxDamage=20,length=240),dict(name='Chain whiff cannot cancel',pulse=1,inputs=[dict(tick=36,pulse=1)],forbid=240,far=True,length=180)]
for c in [dict(name='Monkey King idle',length=100),dict(name='Monkey King walking',walk=True,state=20,length=150),dict(name='Monkey King jump',jump=True,state=40,length=180),dict(name='Monkey King Z X C chain',pulse=1,inputs=[dict(tick=36,pulse=2),dict(tick=52,pulse=3)],requireStates=[230,260,310],minDamage=160,length=240),dict(name='Monkey King Azure Dragon',pulse=6,state=2000,damage=True,length=580),dict(name='Monkey King ultimate',pulse=10,state=4500,require=4501,minDamage=500,length=360)]:
    cases.append(dict(c,form=1,expectForm=1))
if '--smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Idle','Light chain','Azure Dragon Kick','Monkey King','Charge and release')]
if '--counters' in sys.argv:
    cases=[dict(c,require=1001) for c in cases if c['name'] in ('Moonlight Sword Style','Moonlight Sword Style facing left')]
if '--adapter-smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Azure Dragon Kick','Twin Dragon Kick insufficient meter','Blue Dragon Tempest insufficient meter','Monkey King','Monkey King facing left','Moonlight Sword Style','Moonlight Sword Style facing left')]
if '--upgrade-smoke' in sys.argv:cases=[c for c in cases if c['name'] in ('Entrance','Transform into Monkey King','Return to Jin Mori','Z Z Z chain','X X X chain','Z X C chain','Monkey King Z X C chain','Monkey King','Monkey King facing left','Transformation interrupted','Monkey King takes a hit')]
if '--presentation' in sys.argv:
    cases=[c for c in cases if c['name'] in ('Entrance','Transform into Monkey King','Return to Jin Mori','Z Z Z chain','X X X chain','Z X C chain','Normal to Azure Dragon','Monkey King Z X C chain','Monkey King','Monkey King facing left','Monkey King ultimate')]
    for c in cases:c['length']=240 if c.get('pulse')==10 else min(c['length'],300)
if '--physical' in sys.argv:
    for c in cases:
        c['rawdir']={5:1,7:2,8:3,9:1}.get(c.get('pulse'),0)
        if c.get('counter'):c['require']=1001
if '--awakening' in sys.argv:cases=[c for c in cases if c['name'] in ('Transform into Monkey King','Return to Jin Mori')]
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
code=code.replace('rimuru','jin-mori').replace('Rimuru','Mori').replace('RIMURU','MORI').replace('jin-mori.form','mori.form')
code=code.replace('(c.cornerX or -25)*4+(c.facing or 1)*160','((c.cornerX or -25)+(c.facing or 1)*40)*(1280/192)')
code=code.replace('if c.meter and minPower~=c.meter then ok=false end','if c.forbid and c.meter and minPower~=c.meter then ok=false end')
code=code.replace('and final==0','and (final==0 or final==11)')
code=code.replace('passed=ok,','passed=not not ok,')
code=code.replace('if c.damage and minLife>=1000 then ok=false end','if c.damage and minLife>=1000 then ok=false end\n  if c.minDamage and 1000-minLife<c.minDamage then ok=false end')
code=code.replace('if c.minDamage and 1000-minLife<c.minDamage then ok=false end','if c.minDamage and 1000-minLife<c.minDamage then ok=false end\n  if c.maxDamage and 1000-minLife>c.maxDamage then ok=false end\n  for _,s in ipairs(c.requireStates or {}) do if not seen[tostring(s)] then ok=false end end\n  if c.hurt and life()>=1000 then ok=false end')
code=code.replace(' if tick==24 then'," if c.inputs then for _,input in ipairs(c.inputs) do if tick==input.tick then player(1);mapSet('test.pulse',input.pulse) end end end\n if c.probe and tick==c.probe then player(2);selfState(9004) end\n if tick==24 then",1)
code=code.replace('passed=not not ok,seen=seen,','passed=not not ok,seen=seen,final_life=life(),')
code=code.replace("mapSet('test.pulse',0);", "mapSet('test.pulse',0);mapSet('test.inputdir',0);")
code=code.replace(' if tick==24 then'," if tick==18 then player(1);mapSet('test.inputdir',c.rawdir or 0) end\n if tick==24 then player(1);mapSet('test.inputdir',0) end\n if tick==24 then")
code='''local function encode(v)
 local t=type(v)
 if t=='nil' then return 'null' end
 if t=='boolean' or t=='number' then return tostring(v) end
 if t=='string' then return '"'..v:gsub('\\\\','\\\\\\\\'):gsub('"','\\\\"'):gsub('\\n','\\\\n'):gsub('\\r','\\\\r')..'"' end
 if t=='table' then
  local r={};local array=#v>0
  if array then for i=1,#v do r[#r+1]=encode(v[i]) end
  else for k,item in pairs(v) do r[#r+1]=encode(tostring(k))..':'..encode(item) end end
  return (array and '[' or '{')..table.concat(r,',')..(array and ']' or '}')
 end
 error('Unsupported report value '..t)
end
local function saveReport(v,path) os.remove(path);local f=assert(io.open(path,'w'));f:write(encode(v));f:close() end
'''+code.replace('jsonEncode(','saveReport(')
code=code.replace(' if tick==24 then'," if tick==60 and c.counter then player(2);selfState(9004) end\n if tick==24 then")
code=code.replace('local seen,minLife',"local caseShots,lastKey=0,''\nlocal seen,minLife").replace('seen={};minLife=1000',"seen={};caseShots=0;lastKey='';minLife=1000")
marker=' if c.capture~=false and tick>10 and tick%(c.dense and 4 or c.direct and 4 or 12)==0 and (tick<450 or c.pulse==7) and not pending then'
replacement=" player(1);local key=tostring(stateNo())..':'..tostring(spriteVar('group'))..':'..tostring(spriteVar('image'))..':'..tostring(minLife)\n if c.capture~=false and tick>10 and caseShots<(c.pulse==10 and 60 or 32) and not pending and ((stateNo()~=0 and tick%4==0 and (key~=lastKey or tick%16==0)) or tick==12 or tick==c.length-4) then\n lastKey=key;caseShots=caseShots+1"
assert marker in code;code=code.replace(marker,replacement)
code=code.replace('(key~=lastKey or tick%16==0)','(stateNo()==980500 or key~=lastKey or tick%16==0)')
code=code.replace('CASES',lua(cases)).replace('CAPTURE',capture)
runtime=json.loads((S/'build-report.json').read_text())['runtime_sha256']
code=code.replace('local report={','local report={runtime_sha256='+lua(runtime)+',',1)
(E/'external/mods/-mori-tests.lua').write_text(code)
config=(E/'save/prince-paired-tests.ini').read_text()
for key,value in [('Modules','external/mods/-mori-tests.lua'),('WindowTitle','Mori_native'),('ScreenshotFolder','../../characters/jin-mori/replays/'+capture+'/'),('MasterVolume','0'),('VSync','1')]:config=re.sub(r'^'+key+r'\s*=.*$',key+' = '+value,config,flags=re.M)
(E/'save/mori-tests.ini').write_text(config)
print('MORI_TESTS_READY',len(cases))
