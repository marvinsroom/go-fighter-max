"""Install Goku's complete upstream move logic with illustrated animation banks."""
from gt_goku_model import *
import json,shutil,hashlib,sys
from gt_goku_illustrated import STRIDE
O.mkdir(exist_ok=True)

def bank_expression():
 return 'ifelse(authorname="Mikel8888(edited by InSeph and edited by RafaMugen)",(ifelse(ishelper,(root,map(goku.bank)),map(goku.bank))+1)*1000000,0)'

def adapt(text):
 # These two borrowed hurt poses assumed the opponent used Goku's sprite IDs.
 # Use the opponent's standard recovery animations during the imported throw.
 for old,new in [(5160,5080),(5022,5020)]:
  text=re.sub(r'(type\s*=\s*)ChangeAnim2(\s*\ntrigger1[^\n]*\nvalue\s*=\s*)'+str(old),lambda m:m[1]+'ChangeAnim'+m[2]+str(new),text,flags=re.I)
 # The original firing hold resets to element 3 every tick. Allow the recoil
 # drawings to play, then return to the firing loop before recovery while the
 # damaging beam helper remains active. Collision and release times stay native.
 text=re.sub(r'trigger1\s*=\s*time\s*>\s*4\s*&&\s*numhelper\((1450|1452|1453)\)\s*>\s*0',
             r'trigger1 = animelemno(0)>=5 && numhelper(\1)>0',text,flags=re.I)
 # Treat numeric animation IDs as a namespace. Expressions keep comparing the
 # source action number; rendering selects one complete illustrated form bank.
 blocks=re.split(r'(?=^\[(?:State|Statedef)\s+)',text,flags=re.I|re.M);result=[]
 for block in blocks:
  typ=re.search(r'^type\s*=\s*(\w+)',block,re.I|re.M);typ=typ[1].lower() if typ else ''
  lines=[]
  for line in block.splitlines():
   m=re.match(r'^(\s*([\w.]+)\s*=)(.*)$',line)
   if not m:lines.append(line);continue
   key=m[2].lower();value=m[3].split(';',1)[0].strip()
   if key=='type' or not value or '"' in value:lines.append(line);continue
   value=re.sub(r'\b(?:root|parent|enemynear|enemy)\s*,\s*anim\b|\banim\b',lambda m:'(('+m[0]+')%1000000)',value,flags=re.I)
   if key=='anim' or key=='value' and typ=='changeanim':
    if value.upper().startswith('F') and typ=='superpause':pass
    else:
     value=re.sub(r'^[sS](?=\d)','',value)
     if value!='-1':value=f'({value})+{bank_expression()}'
   lines.append(m[1]+' '+value)
  result.append('\n'.join(lines)+'\n')
 from goku_alignment import adapt_cns
 return adapt_cns(''.join(result),S)

files={}
for p in U.iterdir():
 if p.suffix.lower() not in ('.cns','.cmd','.def','.act','.snd','.air','.sff'):continue
 with p.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
 files[p.name]=dict(bytes=p.stat().st_size,sha256=digest)
 if p.suffix.lower()=='.cns':(O/p.name).write_text(adapt(p.read_text(encoding='cp1252')))
 elif p.suffix.lower() not in ('.sff','.air'):shutil.copy2(p,O/p.name)
definition=(U/'GokuGT.def').read_text(encoding='cp1252').replace('[Files]','localcoord=320,240\nportraitscale=.125\n\n[Files]').replace('[Arcade]','st10=goku-roster.cns\n\n[Arcade]')
(O/'gt_goku.def').write_text(definition)
main=(O/'GokuGT.cns').read_text()
main=re.sub(r'(?im)^(xscale|yscale)\s*=.*$',lambda m:m[1]+'=1.65',main,count=2)
intro='''[Statedef 190]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=960100
[State 190, Base form]
type=MapSet
trigger1=!time
map="goku.form"
value=0
[State 190, Greeting]
type=AssertSpecial
trigger1=time<160
flag=intro
[State 190, Voice]
type=PlaySnd
trigger1=time=20
value=S0,0
volumescale=80
[State 190, Ready]
type=ChangeState
trigger1=time>=160
value=0
ctrl=1
'''
main=re.sub(r'(?ims)^\[Statedef 190\].*?(?=^\[Statedef )',intro+'\n',main,count=1)
(O/'GokuGT.cns').write_text(main)
ia=(O/'IA.cns').read_text()
ia=ia.replace('[Statedef -2]','''[Statedef -2]
[State -2, Preserve illustrated form through borrowed hurt states]
type=ChangeAnim
triggerall=!ishelper && anim>=0
trigger1=anim<950000
trigger2=anim>=1000000 && floor(anim/1000000)!=map(goku.bank)+1
value=(anim%1000000)+(map(goku.bank)+1)*1000000
elem=AnimElemNo(0)
ignorehitpause=1
''',1)
for block in re.split(r'(?=^\[State\s+)',ia,flags=re.I|re.M):
 if re.search(r'type\s*=\s*Helper',block,re.I) and re.search(r'^stateno\s*=\s*(560|565|566|567|568|569|571|572)\s*$',block,re.I|re.M):
  ia=ia.replace(block,re.sub(r'(type\s*=\s*Helper)',r'\1\ntriggerall=0 ; replaced by the illustrated passive aura',block,count=1,flags=re.I))
# Passive auras are drawn with the new effect atlas. Keep the native helper
# identities and timings; eliminate palette-based hair recoloring of RGBA art.
for fid,states in [(1,[700]),(2,[800]),(3,[900]),(4,[1900]),(0,[705,805,905,1905])]:
 condition=' || '.join('stateno='+str(n) for n in states)
 ia+=f'\n[State -3, Native transformation]\ntype=MapSet\ntriggerall=!ishelper\ntrigger1=({condition}) && time=1\nmap="goku.form"\nvalue={fid}\n'
for f in FORMS:
 for variable,value in [(2,f['flags'][0]),(10,[0,1000,7000,9000,11000,13000,11000,11000][f['flags'][0]]),(11,[0,2000,11000,13000,15000,17000,15000,15000][f['flags'][0]]),(14,[0,24000,26000,28000,30000,32000,30000,30000][f['flags'][0]]),(15,[0,23000,25000,27000,29000,31000,29000,29000][f['flags'][0]])]:
  ia+=f'\n[State -3, Selected form variable]\ntype=VarSet\ntriggerall=!ishelper\ntrigger1=map(goku.form)={f["id"]}\nvar({variable})={value}\nignorehitpause=1\n'
 ia+=f'\n[State -3, Illustrated bank]\ntype=MapSet\ntriggerall=!ishelper\ntrigger1=map(goku.form)={f["id"]}\nmap="goku.bank"\nvalue={f["bank"]}\nignorehitpause=1\n'
ia+='''
[State -3, Change visual bank without changing the move]
type=ChangeAnim
triggerall=!ishelper && anim>=1000000
trigger1=floor(anim/1000000)!=map(goku.bank)+1
value=(anim%1000000)+(map(goku.bank)+1)*1000000
elem=AnimElemNo(0)
ignorehitpause=1
[State -3, Clear old aura]
type=RemoveExplod
triggerall=!ishelper
trigger1=map(goku.aura_form)!=map(goku.form) || !alive || roundstate!=2
ID=960820
[State -3, Stop interrupted charge sound]
type=StopSnd
triggerall=!ishelper
trigger1=stateno!=900810 && numexplod(960810)
trigger2=stateno!=900810 && prevstateno=900810 && time<=1
channel=3
ignorehitpause=1
[State -3, Clear interrupted charge aura]
type=RemoveExplod
triggerall=!ishelper
trigger1=stateno!=900810
ID=960810
[State -3, Illustrated passive aura]
type=Explod
triggerall=!ishelper && alive && roundstate=2
triggerall=map(goku.form)>0 && !numexplod(960820)
trigger1=1
anim=ifelse(var(3)>0,960308,960300+map(goku.bank))
ID=960820
pos=0,3
postype=p1
bindtime=-1
removetime=-1
sprpriority=-2
ownpal=1
[State -3, Remember aura form]
type=MapSet
triggerall=!ishelper
trigger1=1
map="goku.aura_form"
value=map(goku.form)
'''
(O/'IA.cns').write_text(ia)
cmd=(U/'GokuGT.cmd').read_text(encoding='cp1252');move_routes=routes()
inputs={r['command']:r['input'] for r in move_routes};inputs.update(goku_form='w',goku_revert='/$D,w',goku_charge='/s',goku_hold_bomb='/z')
prefix=''.join(f'\n[Command]\nname="{name}"\ncommand={buttons}\ntime=1\n' for name,buttons in inputs.items())
controllers='''
[State -1, Cycle forms]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_form" || command="goku_revert"
trigger1=ctrl
value=900800
[State -1, Charge]
type=ChangeState
triggerall=!AILevel && roundstate=2 && statetype!=A
triggerall=command="goku_charge" && power<3000
trigger1=ctrl
value=900810
'''
for r in sorted(move_routes,key=lambda r:-len(r['input'])):
 controllers+=f'\n[State -1, {r["name"]}]\ntype=ChangeState\ntriggerall=!AILevel && roundstate=2\ntriggerall=map(goku.form)={r["form"]} && power>={r["cost"]}\ntriggerall=command="{r["command"]}"\ntriggerall=statetype{"=" if r["air"] else "!="}A\n'
 if r['extra']:controllers+='triggerall='+r['extra']+'\n'
 controllers+=f'trigger1=ctrl\nvalue={r["state"]}\n'
cmd=cmd.replace('[Statedef -1]',prefix+'\n[Statedef -1]\n'+controllers,1)
(O/'GokuGT.cmd').write_text(cmd)
bomb=(O/'Supers.cns').read_text()
(O/'Supers.cns').write_text(bomb)
roster='''[Statedef 900800]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
[State 900800, Clear full power]
type=VarSet
trigger1=!time
v=3
value=0
[State 900800, Choose]
type=MapSet
trigger1=!time
map="goku.next"
value=ifelse(command="goku_revert",0,(map(goku.form)+1)%5)
[State 900800, Power stance]
type=ChangeAnim
trigger1=!time || time=13
value=960200+map(goku.bank)
[State 900800, Form]
type=MapSet
trigger1=time=12
map="goku.form"
value=map(goku.next)
[State 900800, Burst]
type=PalFX
trigger1=time=10
time=6
add=90,90,90
[State 900800, Energy]
type=Explod
trigger1=time=14
anim=ifelse(var(3)>0,960308,960300+map(goku.bank))
ID=960800
pos=0,0
postype=p1
bindtime=-1
removetime=22
sprpriority=-1
ownpal=1
[State 900800, Sound]
type=PlaySnd
trigger1=time=12
value=S5,5
volumescale=80
[State 900800, Done]
type=ChangeState
trigger1=time>=36
value=0
ctrl=1

[Statedef 900810]
type=S
movetype=I
physics=S
ctrl=0
velset=0,0
anim=960200+map(goku.bank)
[State 900810, Gather ki]
type=PowerAdd
trigger1=1
value=25
[State 900810, Sound]
type=PlaySnd
trigger1=!time
value=S5,64
channel=3
volumescale=65
[State 900810, Illustrated energy]
type=Explod
trigger1=!time
anim=960300+map(goku.bank)
ID=960810
pos=0,4
postype=p1
bindtime=-1
removetime=-1
sprpriority=-1
ownpal=1
removeongethit=1
[State 900810, Clear energy]
type=RemoveExplod
trigger1=command!="goku_charge" || power>=3000
ID=960810
[State 900810, Stop charge sound]
type=StopSnd
trigger1=command!="goku_charge" || power>=3000
channel=3
[State 900810, Return]
type=ChangeState
trigger1=command!="goku_charge" || power>=3000
value=0
ctrl=1
'''
(O/'goku-roster.cns').write_text(roster)
if '--reuse-art' not in sys.argv:
 from gt_goku_illustrated import install
 print('GOKU_ILLUSTRATED',install(),'sprites')
if '--reuse-art' in sys.argv:
 (O/'IA.cns').write_text((O/'IA.cns').read_text()+(S/'hand-registration.cns').read_text())
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix.lower() in ('.def','.cmd','.cns','.sff','.snd','.air') and 'test' not in p.name.lower()}
report=dict(art='illustrated',forms=FORMS,routes=move_routes,source=json.loads((S/'source/source-report.json').read_text()),original_files=files,runtime_sha256=runtime,original_actions=len(actions((U/'GokuGT.air').read_text(encoding='cp1252'))))
(S/'build-report.json').write_text(json.dumps(report,indent=2));print('GOKU_IMPORTED',len(FORMS),'forms;',len(move_routes),'move routes')
