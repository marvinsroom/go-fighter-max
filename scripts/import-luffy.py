"""Reproducible illustrated roster adapter for TheCube's all-forms Luffy."""
from pathlib import Path
import hashlib,json,re,shutil,sys
from luffy_model import FORMS,FLAGS,routes,source_folder,actions

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/luffy';U=source_folder(R)
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/luffy';REF=E/'chars/luffy_reference'
O.mkdir(exist_ok=True);REF.mkdir(exist_ok=True)
reuse_air=(O/'TC_Luffy_All_Forms.air').read_text() if '--reuse-art' in sys.argv else None
originals={}
for p in U.iterdir():
 if p.suffix.lower() not in ('.cns','.def','.sff','.snd','.cmd','.air','.act'):continue
 originals[p.name]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if reuse_air is None or p.suffix.lower() not in ('.air','.sff'):shutil.copy2(p,O/p.name)
 shutil.copy2(p,REF/p.name)
definition=(U/'TC_Luffy_All_Forms.def').read_text(encoding='cp1252').replace('[Files]','localcoord = 320,240\n\n[Files]',1)
(REF/'luffy_reference.def').write_text(definition)
definition=definition.replace('sprite =TC_Luffy_All_Forms.sff','sprite =Luffy.sff').replace('displayname ="Luffy"','displayname ="Monkey D. Luffy"')
definition=definition.replace('[Files]','portraitscale = .125\n\n[Files]',1).replace('[Arcade]','st7=luffy-roster.cns\n\n[Arcade]')
(O/'luffy.def').write_text(definition)
main=(U/'TC_Luffy_All_Forms.cns').read_text(encoding='cp1252')
main=re.sub(r'(?im)^(xscale|yscale)\s*=.*$',lambda m:m[1]+' = 1.4',main,count=2)
intro='''[Statedef 190]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=60100
[State 190, Hold animated intro]
type=AssertSpecial
trigger1=roundstate<2
flag=intro
[State 190, Manual form control]
type=MapSet
trigger1=!time
map="luffy.manual"
value=1
[State 190, Normal pirate attire]
type=MapSet
trigger1=!time
map="luffy.form"
value=0
[State 190, Playful pirate greeting]
type=PlaySnd
trigger1=time=194
value=S0,60
volumescale=80
[State 190, Ready]
type=ChangeState
trigger1=time>=256
value=0
ctrl=1
'''
if re.search(r'^\[Statedef 190\]',main,re.I|re.M):main=re.sub(r'(?ims)^\[Statedef 190\].*?(?=^\[Statedef )',intro+'\n',main,count=1)
else:main+='\n'+intro
(O/'TC_Luffy_All_Forms.cns').write_text(main)
ia=(U/'IA.cns').read_text(encoding='cp1252')
blocks=re.split(r'(?=^\[State\s+)',ia,flags=re.I|re.M)
for i,b in enumerate(blocks):
 if re.search(r'type\s*=\s*ChangeState',b,re.I) and re.search(r'^value\s*=\s*(2905|62905|69995)\s*$',b,re.I|re.M):
  blocks[i]=re.sub(r'(?im)^(type\s*=\s*ChangeState\s*)$',r'\1\ntriggerall=map(luffy.manual)!=1',b,count=1)
 # The new Gear 5 drawings already include their attached cloud ribbon.
 # Source passive cloud helpers use huge padded images and would duplicate it.
 if re.search(r'type\s*=\s*Helper',b,re.I) and re.search(r'^stateno\s*=\s*(68[2389]|69[012567])\s*$',b,re.I|re.M):
  blocks[i]=re.sub(r'(?im)^(type\s*=\s*Helper\s*)$',r'\1\ntriggerall=0 ; steam is included in the illustrated actor',blocks[i],count=1)
 if re.search(r'type\s*=\s*AngleDraw',b,re.I) and re.search(r'var\(14\)\s*=\s*1',b,re.I):
  blocks[i]=re.sub(r'(?im)^scale\s*=\s*1\.56\s*,\s*1\.56\s*$', 'scale = 1,1 ; illustrated Nightmare bank already includes its larger proportions',blocks[i])
ia=''.join(blocks)
# Apply the selected form after upstream appearance controllers. Source flags
# depend on temporary helpers, so manual roster forms must restore them here.
for variable,expression in [(2,'ifelse(map(luffy.form)=1,2,0)'),(13,'ifelse(map(luffy.form)=2,1,0)'),(14,'ifelse(map(luffy.form)=3,1,0)'),(16,'ifelse(map(luffy.form)=4,1,0)'),(6,'0'),(11,'ifelse(map(luffy.form)=4,70000,map(luffy.form)*2000)'),(10,'ifelse(map(luffy.form)=4,70000,ifelse(map(luffy.form)=3,60000,ifelse(map(luffy.form)=2,40000,ifelse(map(luffy.form)=1,20000,0))))')]:
 ia+=f'\n[State -3, Selected form {variable}]\ntype=VarSet\ntriggerall=!ishelper && map(luffy.manual)=1\ntrigger1=1\nvar({variable})={expression}\nignorehitpause=1\n'
# The source ends in Statedef -3; do not append controllers to another state.
assert list(re.finditer(r'^\[Statedef\s+(-?\d+)\]',ia,re.I|re.M))[-1][1]=='-3'
ia=ia.replace('[Statedef -2]','''[Statedef -2]
[State -2, Clear helpers during form selection]
type=DestroySelf
triggerall=ishelper
trigger1=root,stateno=900800
ignorehitpause=1
''',1)
(O/'IA.cns').write_text(ia)
cmd=(U/'TC_Luffy_All_Forms.cmd').read_text(encoding='cp1252');move_routes=routes()
inputs={r['command']:r['input'] for r in move_routes};inputs.update(luffy_form='w',luffy_revert='/$D,w',luffy_charge='/s')
prefix=''.join(f'\n[Command]\nname="{name}"\ncommand={buttons}\ntime=1\n' for name,buttons in inputs.items())
controllers='''
[State -1, Hold charge]
type=ChangeState
triggerall=!AILevel && command="luffy_charge" && power<3000
triggerall=statetype!=A && roundstate=2
trigger1=ctrl
value=900810
[State -1, Cycle form]
type=ChangeState
triggerall=!AILevel && (command="luffy_form" || command="luffy_revert") && roundstate=2
triggerall=statetype!=A
trigger1=ctrl
value=900800
'''
for route in sorted(move_routes,key=lambda r:-len(r['input'])):
 controllers+=f'\n[State -1, {route["name"]}]\ntype=ChangeState\ntriggerall=!AILevel && command="{route["command"]}"\ntriggerall=map(luffy.form)={route["form"]} && power>={route["cost"]}\ntriggerall=roundstate=2 && statetype!=A\ntrigger1=ctrl\nvalue={route["state"]}\n'
cmd=cmd.replace('[Statedef -1]',prefix+'\n[Statedef -1]\n'+controllers,1)
(O/'TC_Luffy_All_Forms.cmd').write_text(cmd)
roster='''[Statedef 900800]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
[State 900800, Enable manual forms]
type=MapSet
trigger1=!time
map="luffy.manual"
value=1
[State 900800, Remember form]
type=MapSet
trigger1=!time
map="luffy.next_form"
value=ifelse(command="luffy_revert",0,(map(luffy.form)+1)%5)
[State 900800, Apply form]
type=MapSet
trigger1=time=12
map="luffy.form"
value=map(luffy.next_form)
[State 900800, Illustrated transition]
type=ChangeAnim
trigger1=!time || time=13
value=60020+map(luffy.form)
[State 900800, Clear old effects]
type=RemoveExplod
trigger1=!time
[State 900800, Complete]
type=ChangeState
trigger1=time>=30
value=0
ctrl=1
[Statedef 900810]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=60020+map(luffy.form)
[State 900810, Gather Haki]
type=PowerAdd
trigger1=1
value=25
[State 900810, Steam]
type=Explod
trigger1=!time
anim=60101
ID=630810
pos=0,0
postype=p1
bindtime=-1
removetime=-1
sprpriority=-1
ownpal=1
[State 900810, Clear aura]
type=RemoveExplod
trigger1=command!="luffy_charge" || power>=3000
ID=630810
[State 900810, Release]
type=ChangeState
trigger1=command!="luffy_charge" || power>=3000
value=0
ctrl=1
'''
(O/'luffy-roster.cns').write_text(roster)
from luffy_illustrated import install
air=reuse_air if reuse_air is not None else install(S,(U/'TC_Luffy_All_Forms.air').read_text(encoding='cp1252'))
(O/'TC_Luffy_All_Forms.air').write_text(air)
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix.lower() in ('.def','.cmd','.cns','.sff','.snd','.air') and 'test' not in p.name.lower()}
report=dict(art='illustrated',forms=FORMS,routes=move_routes,source=json.loads((S/'source/source-report.json').read_text()),original_files=originals,runtime_sha256=runtime,original_actions=len(actions((U/'TC_Luffy_All_Forms.air').read_text(encoding='cp1252'))))
(S/'build-report.json').write_text(json.dumps(report,indent=2));print('LUFFY_IMPORTED',len(FORMS),'selectable forms;',len(move_routes),'skill/super/ultimate routes')
