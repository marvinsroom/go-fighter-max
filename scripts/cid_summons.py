"""Reproducible illustrated Alpha/Beta meter assists; source resources untouched."""
from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy import ndimage
from mugen_sff import Sff
from jinwoo_hybrid_art import drawing

SPECS={
 'alpha':dict(group=7911,height=55,xs=(165,500,850,1250,175,520,870,1370)),
 'beta':dict(group=7916,height=53,xs=(160,530,895,1295,170,540,895,1350))}

def art(root):
 folder=Path(root)/'sprite-fighter/characters/cid/art/summons-v1';out={};meta={}
 for name,cfg in SPECS.items():
  path=folder/(name+'.png')
  with Image.open(path) as im:pixels=np.array(im.convert('RGBA'))
  labels,n=ndimage.label(pixels[:,:,3]>48);areas=np.bincount(labels.ravel());objects=ndimage.find_objects(labels)
  ids=sorted(range(1,n+1),key=lambda i:areas[i],reverse=True)[:8]
  assert min(areas[i] for i in ids)>25000
  ids.sort(key=lambda i:sum((objects[i-1][0].start,objects[i-1][0].stop)))
  ids=[i for start in (0,4) for i in sorted(ids[start:start+4],key=lambda i:objects[i-1][1].start)]
  neutral=objects[ids[0]-1][0];scale=cfg['height']/(neutral.stop-neutral.start)
  for j,i in enumerate(ids):
   sy,sx=objects[i-1];tile=pixels[sy,sx].copy();tile[:,:,3]=np.where(labels[sy,sx]==i,tile[:,:,3],0)
   axis=(cfg['xs'][j]-sx.start,sy.stop-sy.start-1)
   frame=drawing(Image.fromarray(tile),axis,scale,str(path.relative_to(root)))
   out[cfg['group'],j]=frame
   meta[f"{cfg['group']},{j}"]={k:v for k,v in frame.items() if k not in ('image','png')}
 im=Image.new('RGBA',(320,80));d=ImageDraw.Draw(im);d.line((10,40,290,40),fill=(65,185,255,255),width=7);d.polygon([(260,24),(315,40),(260,56)],fill=(165,235,255,255));d.line((15,40,305,40),fill='white',width=2)
 im=Image.alpha_composite(im.filter(ImageFilter.GaussianBlur(6)),im)
 out[7917,0]=drawing(im,(20,40),.15,'procedural magic arrow: scripts/cid_summons.py')
 return out,meta

def install(root,out):
 root=Path(root);out=Path(out);frames,meta=art(root)
 archive=Sff(out/'Cid.sff');assert not any(k in archive.keys for k in frames)
 (out/'Cid.sff').write_bytes(archive.derive({},frames))
 command=(out/'Cid.cmd').read_text(encoding='utf-8')
 at=command.lower().index('[statedef -1]')
 defs='[Command]\nname="cid_alpha"\ncommand=/$D,y\ntime=12\n[Command]\nname="cid_beta"\ncommand=/$B,y\ntime=12\n'
 command=command[:at]+defs+command[at:];at=command.lower().index('[statedef -1]')+len('[statedef -1]')
 routes=''
 for name,state in [('alpha',7910),('beta',7915)]:
  routes+=f'\n[State -1, {name} summon super]\ntype=ChangeState\ntriggerall=!AILevel && statetype!=A && ctrl\ntriggerall=power>=1000\ntriggerall=numhelper(7911)=0 && numhelper(7916)=0\ntrigger1=command="cid_{name}"\nvalue={state}\n'
 (out/'Cid.cmd').write_text(command[:at]+routes+command[at:],encoding='utf-8')
 air=[]
 for name,cfg in SPECS.items():
  air.append(f"[Begin Action {cfg['group']}]")
  for j in range(8):
   m=frames[cfg['group'],j];air.extend(['Clsn2: 1','Clsn2[0]=-14,-52,14,0'])
   if name=='alpha' and j in (3,4,6):air.extend(['Clsn1: 1','Clsn1[0]=-6,-50,74,-8'])
   air.append(f"{cfg['group']},{j},0,0,6,,,{m['scale']:.9f},{m['scale']:.9f}")
 air+=['[Begin Action 7917]','Clsn1Default: 1','Clsn1[0]=-2,-5,44,5','7917,0,0,0,-1,,A,.15,.15']
 with (out/'Cid.air').open('a',encoding='utf-8') as f:f.write('\n'+'\n'.join(air)+'\n')
 states=''
 for name,n,helper in [('alpha',7910,7911),('beta',7915,7916)]:
  states+=f"""
[Statedef {n}]
type=S
movetype=A
physics=S
anim=0
ctrl=0
velset=0,0
poweradd=-1000
[State {n}, Super anticipation]
type=SuperPause
trigger1=!time
time=8
movetime=0
anim=-1
sound=-1
darken=0
unhittable=0
[State {n}, Gather shadow magic]
type=Explod
trigger1=!time
anim=550
pos=0,0
postype=p1
scale=.3,.3
sprpriority=-2
ownpal=1
removetime=30
supermovetime=8
[State {n}, Call {name}]
type=Helper
trigger1=time=8
name="{name} summon"
ID={helper}
stateno={helper}
postype=p1
pos={12 if name=='alpha' else -30},0
ownpal=1
keyctrl=0
size.xscale=1.65
size.yscale=1.65
[State {n}, Cast sound]
type=PlaySnd
trigger1=time=8
value=S10,6
channel=7
volumescale=70
[State {n}, Recover]
type=ChangeState
trigger1=time>=56
value=0
ctrl=1
[Statedef {helper}]
type=S
movetype=A
physics=N
anim={helper}
ctrl=0
velset=0,0
sprpriority=3
[State {helper}, Spell actor]
type=NotHitBy
trigger1=1
value=SCA
time=1
[State {helper}, Fade in and out]
type=Trans
trigger1=1
trans=addalpha
alpha=cond(time<4,time*64,cond(time>42,(48-time)*42,256)),cond(time<4,256-time*64,cond(time>42,256-(48-time)*42,0))
[State {helper}, Cancel when interrupted]
type=DestroySelf
trigger1=root,movetype=H
trigger2=root,life<=0
[State {helper}, Finish]
type=DestroySelf
trigger1=time>=48
"""
  if name=='alpha':
   states+=f"""
[State {helper}, Rush]
type=VelSet
trigger1=time<16
x=min(4,max(0,p2dist x-24))
[State {helper}, Plant]
type=VelSet
trigger1=time>=16
x=0
[State {helper}, Sword combo]
type=HitDef
trigger1=time=18
trigger2=time=24
trigger3=time=36
attr=S,HA
ID=7911
affectteam=E
hitflag=MAF
guardflag=MA
animtype=Hard
damage=70,7
getpower=0,0
pausetime=3,5
sparkno=-1
guard.sparkno=-1
ground.type=High
ground.slidetime=12
ground.hittime=20
ground.velocity=-2,0
air.velocity=-2,-3
fall=time>=36
kill=1
[State {helper}, Impact]
type=EnvShake
trigger1=movehit=1
time=6
ampl=-2
freq=60
"""
  else:
   states+=f"""
[State {helper}, Mana arrows]
type=Helper
trigger1=time=24
trigger2=time=30
trigger3=time=36
name="Beta magic arrow"
ID=7917
stateno=7917
postype=p1
pos=52,-38
ownpal=1
keyctrl=0
size.xscale=1.65
size.yscale=1.65
"""
 states+="""
[Statedef 7917]
type=A
movetype=A
physics=N
anim=7917
ctrl=0
velset=7,0
sprpriority=4
[State 7917, Arrow]
type=HitDef
trigger1=!time
attr=S,HP
ID=7917
affectteam=E
hitflag=MAF
guardflag=MA
animtype=Hard
damage=65,6
getpower=0,0
pausetime=0,5
sparkno=-1
guard.sparkno=-1
ground.type=High
ground.slidetime=10
ground.hittime=16
ground.velocity=-2,0
air.velocity=-2,-3
fall=0
[State 7917, End]
type=DestroySelf
trigger1=movecontact
trigger2=time>=45
trigger3=root,movetype=H
trigger4=root,life<=0
"""
 (out/'cid_summons.cns').write_text(states,encoding='utf-8')
 definition=(out/'cid_shadow.def').read_text(encoding='utf-8')
 (out/'cid_shadow.def').write_text(definition+'\nst8 = cid_summons.cns\n',encoding='utf-8')
 report=dict(status='Built; awaiting native checks',meter_cost=1000,alpha=dict(state=7910,helper=7911,input='Down + S',attack='Rushing sword combo'),beta=dict(state=7915,helper=7916,input='Back + S',attack='Three-shot mana-arrow volley'),art=meta,runtime={n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in ['Cid.sff','Cid.air','Cid.cmd','cid_summons.cns']})
 (root/'sprite-fighter/characters/cid/summon-build.json').write_text(json.dumps(report,indent=2))
 return report

