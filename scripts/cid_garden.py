"""Seven Shadows team ultimate: fixed-scale actors, ordered strikes, brief blackout."""
from pathlib import Path
import re,json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFilter
from mugen_sff import Sff
from jinwoo_hybrid_art import drawing
from jinwoo_motion import atlas_rects
from cid_summons import art as summon_art

MEMBERS=('alpha','beta','gamma','delta','epsilon','zeta','eta')
NEW=(('gamma-delta-epsilon.png',('gamma','delta','epsilon'),((144,508,840,1240),(140,506,835,1260),(140,510,850,1235))),('zeta-eta.png',('zeta','eta'),((185,555,950,1330),(185,550,865,1280))))

def art(root):
 folder=Path(root)/'sprite-fighter/characters/cid/art/garden-ultimate-v1';out={};meta={}
 for file,names,axes in NEW:
  with Image.open(folder/file) as source:
   source=source.convert('RGBA');rects=atlas_rects(source,4,len(names));tiles=[source.crop(r) for r in rects]
  for row,name in enumerate(names):
   cells=[]
   for j in range(4):
    pixels=np.array(tiles[row*4+j]);labels,_=ndimage.label(pixels[:,:,3]>48);areas=np.bincount(labels.ravel());areas[0]=0;identity=int(areas.argmax());assert areas[identity]>5000,(name,j)
    sy,sx=ndimage.find_objects(labels)[identity-1];pixels[:,:,3]=np.where(labels==identity,pixels[:,:,3],0)
    cells.append((Image.fromarray(pixels),(sx.start,sy.start,sx.stop,sy.stop)))
   scale=55/(cells[0][1][3]-cells[0][1][1]);group=7922+MEMBERS.index(name)-2
   for j,(tile,bounds) in enumerate(cells):
    rect=rects[row*4+j];axis=(axes[row][j]-rect[0],bounds[3]);m=drawing(tile,axis,scale,str((folder/file).relative_to(root)))
    out[group,j]=m;meta[f'{group},{j}']={k:v for k,v in m.items() if k not in ('image','png')}
 black=Image.new('RGBA',(16,16),(0,0,0,255));out[7938,0]=drawing(black,(0,0),1,'procedural opaque blackout')
 for j in range(4):
  im=Image.new('RGBA',(640,480));d=ImageDraw.Draw(im);color=(225,180,255,255-j*25)
  for shift in (-50,0,50):
   d.line((70,360+shift,540,60+shift),fill=color,width=16);d.line((70,360+shift,540,60+shift),fill=(255,250,255,255-j*25),width=4)
  im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(8)),im);out[7938,j+1]=drawing(im,(320,240),.22,'procedural team impact slashes')
 return out,meta

def install(root,out):
 root=Path(root);out=Path(out);frames,meta=art(root);old,oldmeta=summon_art(root);registered={**old,**frames}
 sff=Sff(out/'Cid.sff');assert not any(k in sff.keys for k in frames)
 (out/'Cid.sff').write_bytes(sff.derive({},frames))
 cmd=(out/'Cid.cmd').read_text(encoding='utf-8');at=cmd.lower().index('[statedef -1]')
 cmd=cmd[:at]+'[Command]\nname="cid_garden"\ncommand=/$D,~x\ntime=30\n'+cmd[at:];at=cmd.lower().index('[statedef -1]')+len('[statedef -1]')
 route='\n[State -1, Seven Shadows ultimate]\ntype=ChangeState\ntriggerall=!AILevel && statetype!=A && ctrl\ntriggerall=power>=3000\ntriggerall=numhelper(7911)=0 && numhelper(7916)=0\ntrigger1=command="cid_garden"\nvalue=7920\n'
 (out/'Cid.cmd').write_text(cmd[:at]+route+cmd[at:],encoding='utf-8')
 body=json.loads((root/'sprite-fighter/characters/cid/illustrated-build-report.json').read_text())['replaced_sprite_keys']
 air=[]
 air+=['[Begin Action 7920]']
 for key,ticks,active in [('0,65',8,False),('0,48',8,False),('0,52',6,True),('0,65',12,False)]:
  m=body[key];air+=['Clsn2: 1','Clsn2[0]=-16,-55,16,0']
  if active:air+=['Clsn1: 1','Clsn1[0]=12,-50,95,-5']
  air.append(f"{key},0,0,{ticks},,,{m['scale']:.9f},{m['scale']:.9f}")
 m=body['0,10'];air+=['[Begin Action 7921]',f"0,10,0,0,-1,,,{m['scale']:.9f},{m['scale']:.9f}"]
 for i,name in enumerate(MEMBERS):
  group=7911 if i==0 else 7916 if i==1 else 7922+i-2
  poses=(1,3,4,6) if i==0 else (2,3,4,6) if i==1 else (0,1,2,3)
  m=registered[group,0];air += [f'[Begin Action {7950+i*2}]',f"{group},0,0,0,-1,,,{m['scale']:.9f},{m['scale']:.9f}",f'[Begin Action {7951+i*2}]']
  for pose in poses:
   m=registered[group,pose];air.append(f"{group},{pose},0,0,6,,,{m['scale']:.9f},{m['scale']:.9f}")
 air+=['[Begin Action 7940]','7938,0,0,0,-1','[Begin Action 7941]']
 for j in range(4):air.append(f'7938,{j+1},0,0,3,,A,.22,.22')
 with (out/'Cid.air').open('a',encoding='utf-8') as f:f.write('\n'+'\n'.join(air)+'\n')
 states="""
[Statedef 7920]
type=S
movetype=A
physics=S
anim=7920
ctrl=0
velset=0,0
poweradd=-3000
[State 7920, Power pause]
type=SuperPause
trigger1=!time
time=10
movetime=0
anim=-1
sound=-1
darken=0
unhittable=0
[State 7920, Advance]
type=VelSet
trigger1=time=[8,19]
x=3
[State 7920, Stop]
type=VelSet
trigger1=time>=20
x=0
[State 7920, Opening sword catch]
type=HitDef
trigger1=time=16
attr=S,HA
damage=20,2
getpower=0,0
hitflag=MAF
guardflag=MA
animtype=Hard
pausetime=0,5
ground.type=High
ground.hittime=20
ground.velocity=0,0
air.velocity=0,0
p2stateno=7929
sparkno=-1
guard.sparkno=-1
[State 7920, Confirm team assault]
type=ChangeState
trigger1=movehit && numtarget>0
value=7921
[State 7920, Block or miss recovery]
type=ChangeState
trigger1=time>=34
value=0
ctrl=1
[Statedef 7921]
type=S
movetype=A
physics=N
anim=7921
ctrl=0
velset=0,0
sprpriority=10
[State 7921, Give the formation room]
type=PosAdd
trigger1=!time
x=-60
[State 7921, Hold captured opponent]
type=TargetBind
trigger1=time<200 && numtarget>0
time=1
pos=120,0
[State 7921, Cinematic protection]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State 7921, Arena contrast]
type=BGPalFX
trigger1=!time
time=232
mul=85,75,120
add=0,0,0
[State 7921, Formation voice]
type=PlaySnd
trigger1=!time
value=S10,6
channel=7
[State 7921, Blackout]
type=Explod
trigger1=time=188
ID=7940
anim=7940
postype=left
pos=0,0
scale=screenwidth/16,screenheight/16
sprpriority=99999
ontop=1
bindtime=-1
removetime=24
ownpal=1
supermovetime=999
pausemovetime=999
[State 7921, Blackout evidence]
type=MapSet
trigger1=time=188
map="garden.blackout"
value=1
[State 7921, Heavy finishing hit]
type=TargetLifeAdd
trigger1=time=200 && numtarget>0
value=-220
kill=1
absolute=1
[State 7921, Finisher evidence]
type=MapSet
trigger1=time=200
map="garden.finish"
value=1
[State 7921, Finisher impact]
type=EnvShake
trigger1=time=200
time=18
ampl=-8
freq=60
[State 7921, Finisher sound]
type=PlaySnd
trigger1=time=200
value=S5,49
volumescale=100
[State 7921, Release opponent]
type=TargetState
trigger1=time=200 && numtarget>0
value=7949
[State 7921, Clear blackout]
type=RemoveExplod
trigger1=time>=212
ID=7940
[State 7921, Finish]
type=ChangeState
trigger1=time>=232
value=0
ctrl=1
[Statedef 7929]
type=S
movetype=H
physics=N
anim=5000
ctrl=0
velset=0,0
[State 7929, Safe victim timeout]
type=SelfState
trigger1=time>=265
value=0
ctrl=1
[Statedef 7949]
type=A
movetype=H
physics=N
anim=5000
ctrl=0
velset=-3,-6
[State 7949, Finisher fall]
type=VelAdd
trigger1=1
y=.4
[State 7949, Land]
type=SelfState
trigger1=pos y>=0 && time>3
value=5100
[State 7949, Safety recovery]
type=SelfState
trigger1=time>=120
value=0
ctrl=1
"""
 # Evidence is reset for every attempt, including blocked/missed starters.
 reset=''
 for key in ['blackout','finish']+[f'actor{i}' for i in range(7)]:reset+=f'\n[State 7920, Reset evidence]\ntype=MapSet\ntrigger1=!time\nmap="garden.{key}"\nvalue=0\n'
 at=states.index('[State 7920, Power pause]');states=states[:at]+reset+states[at:]
 positions=((-50,-8),(-10,-8),(30,-8),(70,-8),(-30,0),(10,0),(50,0))
 for i,name in enumerate(MEMBERS):
  n=7950+i;x,y=positions[i];attack=48+i*18
  states+=f"""
[State 7921, {name} enters]
type=Helper
trigger1=time={i*4}
name="{name} Seven Shadows"
ID={n}
stateno={n}
postype=p1
pos={x},{y}
ownpal=1
keyctrl=0
size.xscale=1.65
size.yscale=1.65
[State 7921, Observe {name}]
type=MapSet
trigger1=numhelper({n})>0
map="garden.actor{i}"
value=1
"""
  # These controllers belong to 7921, before the victim state definitions.
  block=states[states.rfind(f'[State 7921, {name} enters]'):];states=states[:states.rfind(f'[State 7921, {name} enters]')]
  at=states.index('[Statedef 7929]');states=states[:at]+block+states[at:]
  strikes=''
  for tick in (attack+12,attack+16):strikes+=f'\n[State 7921, {name} strike]\ntype=TargetLifeAdd\ntrigger1=time={tick} && numtarget>0\nvalue=-20\nkill=0\nabsolute=1\n[State 7921, {name} hit count]\ntype=HitAdd\ntrigger1=time={tick} && numtarget>0\nvalue=1\n'
  strikes+=f'\n[State 7921, {name} visible impact]\ntype=Explod\ntrigger1=time={attack+12}\nanim=7941\npostype=p1\npos=120,-35\nscale=1,1\nsprpriority=15\nownpal=1\nremovetime=-2\n'
  at=states.index('[Statedef 7929]');states=states[:at]+strikes+states[at:]
  states+=f"""
[Statedef {n}]
type=S
movetype=I
physics=N
anim={7950+i*2}
ctrl=0
velset=0,0
sprpriority={2+i%3}
[State {n}, Spell actor]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State {n}, Enter from shadow]
type=Trans
trigger1=time<8
trans=addalpha
alpha=time*32,256-time*32
[State {n}, Move to strike]
type=BindToRoot
trigger1=parent,time>={attack} && parent,time<{attack+24}
pos=75,0
[State {n}, Play attack]
type=ChangeAnim
trigger1=parent,time={attack}
value={7951+i*2}
[State {n}, Return to formation]
type=BindToRoot
trigger1=parent,time<{attack} || parent,time>={attack+24}
pos={x},{y}
[State {n}, Recover stance]
type=ChangeAnim
trigger1=parent,time={attack+24}
value={7950+i*2}
[State {n}, End]
type=DestroySelf
trigger1=root,stateno!=7921
trigger2=root,time>=184
"""
 (out/'cid_garden.cns').write_text(states,encoding='utf-8')
 definition=(out/'cid_shadow.def').read_text(encoding='utf-8');(out/'cid_shadow.def').write_text(definition+'\nst9 = cid_garden.cns\n',encoding='utf-8')
 report=dict(status='Built; awaiting native verification',members=list(MEMBERS),cost=3000,damage=520,starter=7920,cinematic=7921,actor_scale=1.65,blackout_ticks=[188,212],art=meta,air_rows=sum(bool(re.match(r'^\d+,\d+,',line)) for line in air),sprite_headers=len(frames),runtime={n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in ['Cid.air','Cid.sff','Cid.cmd','cid_garden.cns','cid_shadow.def']})
 (root/'sprite-fighter/characters/cid/garden-build.json').write_text(json.dumps(report,indent=2))
 return report
