"""Reproducible Edward Elric adapter; original release remains untouched."""
from pathlib import Path
import hashlib,json,re,shutil
from edward_assets import read_v1,write_v2
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'sprite-fighter/characters/edward';U=S/'source/upstream/Edward'
E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';O=E/'chars/edward';O.mkdir(exist_ok=True)
REFERENCE=E/'chars/edward_reference';REFERENCE.mkdir(exist_ok=True)
originals={}
for p in U.iterdir():
    if p.suffix.lower() not in ('.def','.air','.cns','.cmd','.sff','.snd','.txt','.act'):continue
    originals[p.name]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    shutil.copy2(p,O/p.name)
    shutil.copy2(p,REFERENCE/p.name)
d=(U/'Edward.def').read_text(encoding='cp1252').replace('[Files]','localcoord = 320,240\n\n[Files]')
d=d.replace('displayname  ="Edward"','displayname  ="Edward Elric"')
(REFERENCE/'edward_reference.def').write_text(d,encoding='utf-8')
(O/'Command_original.cmd').write_bytes((U/'Command.cmd').read_bytes())
(O/'Animation_original.air').write_bytes((U/'Animation.air').read_bytes())
(O/'edward_original.def').write_text(d.replace('Command.cmd','Command_original.cmd').replace('Animation.air','Animation_original.air'),encoding='utf-8')
d=d.replace('sprite  =Sprite.sff','sprite  =Edward.sff')
d=d.replace('[Files]','portraitscale = 0.125\n\n[Files]')
(O/'edward.def').write_text(d,encoding='utf-8')
sprites=read_v1(U/'Sprite.sff')
portrait=Image.open(S/'art/illustrated-v1/portrait.png').convert('RGBA')
for key,size in [((9000,0),(200,200)),((9000,1),(960,1120))]:
    from PIL import ImageOps
    im=ImageOps.fit(portrait,size,method=Image.Resampling.LANCZOS,centering=(.5,.35))
    next(s for s in sprites if s['key']==key).update(image=im,axis=(0,0))
from edward_illustrated import install
sprites,air=install(S,sprites,(U/'Animation.air').read_text(encoding='cp1252'))
write_v2(O/'Edward.sff',sprites)
(O/'Animation.air').write_text(air,encoding='utf-8')
system=(U/'System.cns').read_text(encoding='cp1252')
system=re.sub(r'(?m)^xscale\s*=.*$','xscale = .92',system,count=1)
system=re.sub(r'(?m)^yscale\s*=.*$','yscale = .92',system,count=1)
system=system.replace('[Data]','[Data]\npower = 3000',1)
system=system.replace('(command = "hold_b" && command = "hold_y")','((command = "hold_b" && command = "hold_y") || command = "ed_charge")')
system=system.replace('(command != "hold_b" || command != "hold_y")','((command != "hold_b" || command != "hold_y") && command != "ed_charge")')
(O/'System.cns').write_text(system,encoding='utf-8')
from edward_illustrated import modern_helpers
(O/'Helpers.cns').write_text(modern_helpers((U/'Helpers.cns').read_text(encoding='cp1252')),encoding='utf-8')
# Our familiar three attack buttons select punches; retain kicks on J/K/L.
cmd=(U/'Command.cmd').read_text(encoding='cp1252')
prefix=''
routes=[('ed_cannon','z',1000,0),('ed_gun','z',1100,0),('ed_pillar','z',1300,0),('ed_bat','z',1400,0),('ed_spike','z',1200,0),('ed_hand','z',1600,0),('ed_super','y',3010,1000),('ed_wall','y',3030,1000),('ed_barrage','y',3000,1000),('ed_spike_super','y',3020,1000),('ed_final','x',3100,3000),('ed_throw','d',800,0),('ed_charge','s',730,0)]
inputs={'ed_cannon':'a','ed_gun':'/$B,a','ed_pillar':'/$F,a','ed_bat':'/$D,a','ed_spike':'/$D,/$B,a','ed_hand':'/$D,/$F,a','ed_super':'b','ed_wall':'/$F,b','ed_barrage':'/$B,b','ed_spike_super':'/$D,b','ed_final':'c','ed_throw':'d','ed_charge':'/s'}
for name,_,state,cost in routes:
    prefix+=f'\n[Command]\nname="{name}"\ncommand={inputs[name]}\ntime=1\n'
prefix+='\n[Command]\nname="ed_kickshift"\ncommand=/w\ntime=1\n'
controllers=''
for name,_,state,cost in sorted(routes,key=lambda x:-len(inputs[x[0]])):
    controllers+=f'\n[State -1, {name}]\ntype=ChangeState\ntriggerall=!AILevel && command="{name}"\ntriggerall=command!="ed_kickshift"\ntriggerall=StateType!=A && RoundState=2\ntriggerall=Power>={cost}\ntrigger1=ctrl\nvalue={state}\n'
cmd=cmd.replace('[Statedef -1]',prefix+'\n[Statedef -1]\n',1)
cmd=cmd.replace('[State -1, Stand Light Punch]',controllers+'\n[State -1, Stand Light Punch]',1)
# Shifted kicks remain intentional even when an alchemy shortcut lacks meter.
parts=re.split(r'(?=\[State -1,)',cmd)
for i,block in enumerate(parts):
    value=re.search(r'(?im)^value\s*=\s*(\d+)\s*$',block)
    if value and int(value[1]) in (230,240,250,430,440,450,630,640,650) and '!AIlevel' in block:
        parts[i]=re.sub(r'(?im)^(type\s*=\s*ChangeState\s*)$',r'\1\ntriggerall=command="ed_kickshift"',block,count=1)
cmd=''.join(parts)
# Match the existing keyboard layout: Z/X/C -> a/b/c; A/S/D -> z/y/x.
for a,b in [('a','x'),('b','y'),('c','z'),('x','a'),('y','b'),('z','c')]:
    cmd=re.sub(r'(?m)^'+a+r' = '+a+r'$',a+' = '+b,cmd,count=1)
(O/'Command.cmd').write_text(cmd,encoding='utf-8')
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix.lower() in ('.sff','.snd','.cns','.cmd','.air','.def') and 'test' not in p.name.lower()}
actions=[int(x) for x in re.findall(r'\[Begin Action\s+(\d+)\]',(U/'Animation.air').read_text(encoding='cp1252'),re.I)]
report=dict(creator='Nexus Gaming',source=json.loads((S/'source/source-report.json').read_text()),original_files=originals,sprites=len(sprites),actions=len(actions),runtime_sha256=runtime,adapters=['explicit 320x240 coordinates','three punches plus W-modified kicks','A/S/D alchemy shortcuts; original motion commands retained','64 illustrated drawings, new portrait, registered construction layers','original AIR durations, action IDs and move routes retained; extreme attack boxes bounded'])
(S/'build-report.json').write_text(json.dumps(report,indent=2))
select=E/'data/select.def';text=select.read_text(encoding='utf-8')
if not re.search(r'^edward\s*,',text,re.M):select.write_text(text.replace('[Characters]','[Characters]\nedward, stages/stage0-720.def, order=1',1),encoding='utf-8')
print('EDWARD_IMPORTED',len(sprites),'sprites',len(actions),'actions')
