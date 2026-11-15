"""Import Chickennuggetprime's all-forms edit without altering its archive."""
from pathlib import Path
import hashlib,json,re,shutil,sys
from ichigo_model import FORMS,actions,source_folder,command_routes

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/ichigo';U=source_folder(R)
E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/ichigo';O.mkdir(exist_ok=True)
REF=E/'chars/ichigo_reference';REF.mkdir(exist_ok=True)
originals={}
for p in U.iterdir():
    if p.suffix.lower() not in ('.cns','.def','.sff','.snd','.cmd','.air','.act','.reb1'):continue
    originals[p.name]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    shutil.copy2(p,O/p.name);shutil.copy2(p,REF/p.name)
for name in ('Intro','ending'):
    if (U/name).exists():shutil.copytree(U/name,REF/name,dirs_exist_ok=True)
definition=(U/'Ichigo.def').read_text(encoding='cp1252',errors='replace')
definition=definition.replace('[Files]','localcoord = 320,240\n\n[Files]',1)
(REF/'ichigo_reference.def').write_text(definition,encoding='utf-8')
definition=re.sub(r'(?im)^(intro|ending)\.storyboard\s*=.*$',r'\1.storyboard =',definition)
definition=definition.replace('cns=add004basic.reb1','cns=ichigo-main.cns').replace('st=add004basic.reb1','st=ichigo-main.cns')
portrait_scale='1' if '--native' in sys.argv else '.125'
definition=definition.replace('[Files]',f'portraitscale = {portrait_scale}\n\n[Files]',1)
definition+='\nst10 = ichigo-roster.cns\n'
# st10 must remain inside [Files], before [Arcade].
definition=definition.replace('\nst10 = ichigo-roster.cns\n','').replace('[Arcade]','st10 = ichigo-roster.cns\n\n[Arcade]')
(O/'ichigo.def').write_text(definition,encoding='utf-8')
main=(U/'add004basic.reb1').read_text(encoding='cp1252',errors='replace')
main=re.sub(r'(?m)^(xscale|yscale)\s*=\s*1\s*$',lambda m:m[1]+' = 1.7',main,count=2)
before,marker,scale=main.partition('[Statedef 999999]')
assert marker
scale=scale.replace('value = 1','value = root,const(size.xscale)',1)
main=before+marker+scale
main=re.sub(r'(?ims)^\[Statedef 190\].*?(?=^\[Statedef )','''[Statedef 190]
type=S
ctrl=0
velset=0,0
[State 190, Regular attire into Bankai]
type=ChangeState
trigger1=1
value=191

''',main,count=1)
(O/'ichigo-main.cns').write_text(main,encoding='utf-8')
ia=(U/'IA.cns').read_text(encoding='cp1252',errors='replace')
# The upstream bundles an obsolete ADD004 HUD. Keep its original copy and
# omit its global controller blocks from our existing roster's presentation.
ia=re.sub(r';// add004[^\n]*-start.*?;// add004[^\n]*-end','',ia,flags=re.S|re.I)
global3='''
[State -3, Keep selected human form]
type=VarSet
triggerall=!ishelper && !AILevel
trigger1=map(ichigo.manual)=1
var(2)=map(ichigo.form)
ignorehitpause=1
'''
ia=ia.replace('[Statedef -3]','[Statedef -3]\n'+global3,1)
cleanup='''
[State -2, Clear form effects on manual transition]
type=DestroySelf
triggerall=ishelper
triggerall=!ishelper(999999)
trigger1=root,stateno=900800
ignorehitpause=1
'''
ia=ia.replace('[Statedef -2]','[Statedef -2]\n'+cleanup,1)
(O/'IA.cns').write_text(ia,encoding='utf-8')
# A real round intro: school uniform, gathering pressure, cloth transformation.
common=(U/'common1.cns').read_text(encoding='cp1252',errors='replace')
intro='''[Statedef 191]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=60100
[State 191, Hold round intro]
type=AssertSpecial
trigger1=roundstate<2
flag=intro
[State 191, Regular attire]
type=VarSet
trigger1=!time
var(2)=0
[State 191, Remember regular attire]
type=MapSet
trigger1=!time
map="ichigo.form"
value=0
[State 191, Manual forms]
type=MapSet
trigger1=!time
map="ichigo.manual"
value=1
[State 191, Bankai call]
type=PlaySnd
trigger1=time=68
value=S5,38
[State 191, Spiritual pressure]
type=Explod
trigger1=time=68
anim=60102
ID=630191
pos=0,0
postype=p1
bindtime=-1
removetime=92
sprpriority=-1
ownpal=1
[State 191, Bankai reveal]
type=VarSet
trigger1=time=132
var(2)=2
[State 191, Remember Bankai]
type=MapSet
trigger1=time=132
map="ichigo.form"
value=2
[State 191, Reveal sound]
type=PlaySnd
trigger1=time=132
value=S5,36
[State 191, Ready]
type=ChangeState
trigger1=time>=220
value=0
ctrl=1
'''
common=re.sub(r'(?ims)^\[Statedef 191\].*?(?=^\[Statedef )',intro+'\n',common,count=1)
(O/'common1.cns').write_text(common,encoding='utf-8')
cmd=(U/'Ichigo.cmd').read_text(encoding='cp1252',errors='replace')
routes=command_routes(cmd)
(S/'reference/routes.json').write_text(json.dumps(routes,indent=2))
inputs={'ichigo_form':'w','ichigo_revert':'/$D,w','ichigo_skill1':'x','ichigo_skill2':'/$B,x','ichigo_skill3':'/$F,x','ichigo_skill4':'/$D,x','ichigo_skill5':'/$D,/$F,x','ichigo_skill6':'/$D,/$B,x','ichigo_super':'y','ichigo_ultimate':'z'}
inputs['ichigo_charge']='/s'
prefix=''.join(f'\n[Command]\nname="{name}"\ncommand={value}\ntime=1\n' for name,value in inputs.items())
order=[f['id'] for f in FORMS];cycle='0'
for i,form in reversed(list(enumerate(order[:-1]))):cycle=f'ifelse(var(2)={form},{order[i+1]},{cycle})'
controllers=f'''
[State -1, Charge spiritual pressure]
type=ChangeState
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
triggerall=power<10000
trigger1=command="ichigo_charge"
value=900810
[State -1, Choose next form]
type=MapSet
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
trigger1=command="ichigo_form" || command="ichigo_revert"
map="ichigo.next"
value=ifelse(command="ichigo_revert",0,{cycle})
[State -1, Transform]
type=ChangeState
triggerall=!AILevel && StateType!=A && ctrl && RoundState=2
trigger1=command="ichigo_form" || command="ichigo_revert"
value=900800
'''
selected=[]
for form in FORMS:
    rr=[x for x in routes if x['form']==form['id']]
    for i in range(1,7):
        move=next((x for x in rr if x['command']==f'SPECIAL {i}'),None)
        if move:selected.append(dict(move,input=f'ichigo_skill{i}'))
    move=next((x for x in rr if x['command']=='SUPER2'),None) or next((x for x in rr if x['command']=='SPECIAL 5'),None)
    if move:selected.append(dict(move,input='ichigo_super'))
    move=next((x for x in rr if x['command']=='SUPER1'),None)
    if move:selected.append(dict(move,input='ichigo_ultimate'))
for move in sorted(selected,key=lambda x:-len(inputs[x['input']])):
    controllers+=f'\n[State -1, {move["input"]}]\ntype=ChangeState\ntriggerall=!AILevel && RoundState=2 && StateType!=A\ntriggerall=var(2)={move["form"]} && Power>={move["cost"]}\ntriggerall=command="{move["input"]}"\ntrigger1=ctrl\nvalue={move["state"]}\n'
cmd=re.sub(r'(?i)(\[Statedef\s+-1\])',prefix+'\n'+r'\1'+'\n'+controllers,cmd,count=1)
# The original flash-step command gets its own Q button; D is the finisher.
cmd=re.sub(r'(?im)(name\s*=\s*"z"[^\n]*\ncommand\s*=\s*)z\b',r'\1d',cmd)
(O/'Ichigo.cmd').write_text(cmd,encoding='utf-8')
roster='''[Statedef 900800]
type=S
movetype=I
physics=N
ctrl=0
velset=0,0
anim=60000+map(ichigo.next)
[State 900800, Select form]
type=VarSet
trigger1=!Time
var(2)=map(ichigo.next)
[State 900800, Remember form]
type=MapSet
trigger1=!Time
map="ichigo.form"
value=var(2)
[State 900800, Manual control]
type=MapSet
trigger1=!Time
map="ichigo.manual"
value=1
[State 900800, Finish]
type=ChangeState
trigger1=Time>=30
value=0
ctrl=1
'''
roster+='''
[Statedef 900810]
type=S
movetype=I
physics=N
ctrl=0
velset=0,0
anim=60020+var(2)
[State 900810, Gather spiritual pressure]
type=PowerAdd
trigger1=1
value=35
[State 900810, Charge aura]
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
[State 900810, Clear released aura]
type=RemoveExplod
trigger1=command!="ichigo_charge" || power>=10000
ID=630810
[State 900810, Release]
type=ChangeState
trigger1=command!="ichigo_charge" || power>=10000
value=0
ctrl=1
'''
(O/'ichigo-roster.cns').write_text(roster,encoding='utf-8')
air=(U/'Ichigo.air').read_text(encoding='cp1252',errors='replace');parsed=actions(air)
for form in FORMS:
    frames=parsed[form['base']][:3]
    air+=f'\n[Begin Action {60000+form["id"]}]\nClsn2Default: 1\nClsn2[0]=-10,-50,10,0\n'
    for frame in frames:air+=f'{frame["key"][0]},{frame["key"][1]},0,0,10\n'
    air+=f'\n[Begin Action {60020+form["id"]}]\nClsn2Default: 1\nClsn2[0]=-10,-50,10,0\n'
    for frame in frames:air+=f'{frame["key"][0]},{frame["key"][1]},0,0,10\n'
if '--native' not in sys.argv:
    from ichigo_illustrated import install
    air=install(R,O,air)
(O/'Ichigo.air').write_text(air,encoding='utf-8')
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix.lower() in ('.def','.cmd','.cns','.sff','.snd','.air') and 'test' not in p.name.lower()}
report=dict(source=json.loads((S/'source/source-report.json').read_text()),original_files=originals,forms=FORMS,routes=routes,shortcut_routes=selected,runtime_sha256=runtime,art='native' if '--native' in sys.argv else 'illustrated',original_actions=len(parsed),source_sprites=5531)
(S/'build-report.json').write_text(json.dumps(report,indent=2))
print('ICHIGO_IMPORTED',len(FORMS),'forms;',len(parsed),'source actions;',len(routes),'source skill/super routes')
