"""Register illustrated hands, projectiles and beam collision paths together."""
from pathlib import Path
from PIL import Image, ImageOps
import json, re, math
import numpy as np

BEAMS = {
 'goku': {1450:1415,1452:1415,1453:1415,1470:1470,1750:1750,25640:1415,
          3150:1415,3250:1470,3450:3450,3750:3450,3950:3450,4050:3450,4150:3450,4265:1470,4350:4350,4450:4350},
 'gt-goku': {1450:1450,25450:25450,26050:26050,27450:25450,28050:25450,
             29450:25450,31450:31450,31460:31460,31470:31470,4050:4050},
}
ENDS={'goku':{1451:1450,1471:1470,1751:1750,25645:25640,3151:3150,3251:3250,3451:3450,3751:3750,4270:4265,4351:4350,4451:4450},'gt-goku':{31455:31450,31465:31460,31475:31470}}
ANGLES={'goku':{1470:45,1750:-35,3250:45,4265:45,4350:-35,4450:-35},'gt-goku':{26050:40}}
FLIGHTS={'goku':{405,625,1550,1552,31250,31550},'gt-goku':{405,625,1550,31550}}
CHARGES={'goku':{1430,1431,1432,1730,3130,31530,31531},'gt-goku':{1430}}

def blocks(text):
 return re.split(r'(?=^\[Statedef\s+)',text,flags=re.I|re.M)

def controllers(text):
 return re.split(r'(?=^\[State\s+)',text,flags=re.I|re.M)

def set_field(text,name,value):
 pattern=r'^'+re.escape(name)+r'\s*=.*$'
 return re.sub(pattern,name+' = '+value,text,flags=re.I|re.M) if re.search(pattern,text,re.I|re.M) else text+'\n'+name+' = '+value+'\n'

def portrait(folder,size):
 source=Image.open(folder/'art/presentation-v3/portrait.png').convert('RGBA')
 source=source.crop(source.getbbox())
 margin=round(min(size)*.08)
 fitted=ImageOps.contain(source,(size[0]-margin*2,size[1]-margin*2),Image.Resampling.LANCZOS)
 result=Image.new('RGBA',size)
 result.alpha_composite(fitted,((size[0]-fitted.width)//2,margin))
 return result

def palm(sprite):
 """Find the front palm in the complete, registered body drawing."""
 im=sprite['image'];g,n=sprite['key'];w,h=im.size
 if 62200<=g<=62207 and n in (1,2,3):
  # Cupped hands at the rear hip, before forward release.
  return (w*.24,h*.43)
 pixels=np.asarray(im).astype(np.int16);r,green,b,a=[pixels[:,:,i] for i in range(4)]
 yy,xx=np.indices((h,w))
 skin=(a>100)&(r>120)&(green>65)&(b>25)&(r>green*1.08)&(r>b*1.18)&(yy<h*.72)&(xx>w*.55)
 if skin.any():
  right=int(xx[skin].max());chosen=skin&(xx>=right-max(3,round(w*.035)))
  return (right,float(np.median(yy[chosen])))
 return (w*.91,h*.36)

def paths(folder):
 kind=folder.name
 return BEAMS[kind],FLIGHTS[kind],CHARGES[kind]

def adapt_cns(text,folder):
 kind=folder.name;beam,flights,charges=paths(folder)
 beam_states=set(beam)|set(ENDS[kind])
 hidden={410,411,420,421,626,627,1553,1554,1555,1556} if kind=='goku' else set()
 impacts={415,1551,1560,31255,31555} if kind=='goku' else {410,1551,31551}
 result=[]
 for block in blocks(text):
  match=re.match(r'\[Statedef\s+(\d+)',block,re.I)
  if not match:result.append(block);continue
  state=int(match[1]);parts=[]
  for ctl in controllers(block):
   typ=re.search(r'^type\s*=\s*(\w+)',ctl,re.I|re.M);typ=typ[1].lower() if typ else ''
   if typ=='helper':
    target=re.search(r'^stateno\s*=\s*(\d+)',ctl,re.I|re.M)
    if target and int(target[1]) in set(beam)|flights|charges|{425,635}:
     # All of these helpers are emitted directly by the fighter.
     ctl=set_field(ctl,'size.xscale','1');ctl=set_field(ctl,'size.yscale','1')
     if int(target[1]) in set(beam)|flights|{425,635}:
      ctl=set_field(ctl,'pos','map(goku.muzzle_x),map(goku.muzzle_y)')
   if state in beam_states|charges:
    if typ=='bindtoroot':
     ctl=set_field(ctl,'pos','(root,map(goku.muzzle_x)),(root,map(goku.muzzle_y))')
     if state in beam_states:ctl+='\ntriggerall=time=0 || root,map(goku.emitting)\n'
    if typ=='angledraw' and state in beam_states:ctl=set_field(ctl,'scale','1,1')
    if typ=='explod' and state in beam_states:
     anim=re.search(r'^anim\s*=\s*\(?\s*(\d+)',ctl,re.I|re.M)
     at_target=bool(re.search(r'^postype\s*=\s*p2\b',ctl,re.I|re.M))
     if at_target:
      # P2 offsets are relative to the victim's feet. Intersect the beam's
      # actual line instead of applying a fixed low spark offset.
      angle=ANGLES[kind].get(ENDS[kind].get(state,state),0)
      ctl=set_field(ctl,'pos',f'0,-p2dist y-p2dist x*({math.tan(math.radians(angle)):.8f})')
      ctl=set_field(ctl,'anim','960400')
      ctl=set_field(ctl,'scale','1,1')
      ctl=set_field(ctl,'angle','0')
     elif anim and int(anim[1]) in (1426,1427,1226,1460):
      ctl+='\ntriggerall=0 ; duplicate source beam layer replaced by the registered beam\n'
   if state in flights and typ=='velset':
    # Keep one launch vector instead of random vertical drift every update.
    if re.search(r'^y\s*=.*random',ctl,re.I|re.M):ctl=set_field(ctl,'y','12' if state in (625,1552) and kind=='goku' else '6' if state==625 else '0')
   if state in flights and typ=='angledraw':ctl=set_field(ctl,'scale','1,1')
   if state in flights and typ=='explod':
    ctl+='\ntriggerall=0 ; travelling artwork and trail are supplied by the registered core\n'
   if state in impacts:
    if typ=='posadd':ctl=set_field(ctl,'x','0')
    if typ=='posset' and state==1560:ctl=set_field(ctl,'y','0')
    if typ=='angledraw':ctl=set_field(ctl,'scale','1,1')
    if typ=='explod':
     anim=re.search(r'^anim\s*=\s*\(?\s*(\d+)',ctl,re.I|re.M)
     if anim and int(anim[1]) in ({410} if kind=='gt-goku' else {420,1460}):
      ctl=set_field(ctl,'anim','960400');ctl=set_field(ctl,'scale','1,1');ctl=set_field(ctl,'pos','0,0')
      if re.search(r'^random\s*=',ctl,re.I|re.M):ctl=set_field(ctl,'random','0,0')
   parts.append(ctl)
  block=''.join(parts)
  if state in flights:
   block+='''
[State 0, Match graphic to actual flight vector]
type=AngleSet
trigger1=1
value=ifelse(vel x<0,180+atan(vel y/max(.001,abs(vel x)))*180/pi,-atan(vel y/max(.001,abs(vel x)))*180/pi)
[State 0, Registered projectile size]
type=AngleDraw
trigger1=1
scale=1,1
[State 0, Retire missed shots outside the stage]
type=DestroySelf
trigger1=time>500
trigger2=frontedgedist < -160
trigger3=backedgedist < -160
'''
  if state in hidden:
   block+='''
[State 0, Core projectile supplies the travelling artwork]
type=AssertSpecial
trigger1=1
flag=invisible
'''
  result.append(block)
 return ''.join(result)

def compile_art(folder,sprites,air,source):
 """Use one muzzle origin for drawing, binding, rotation and collisions."""
 kind=folder.name;beam,flights,charges=paths(folder)
 assets=folder.parent/'goku/art/energy-v2'
 sheet=Image.open(assets/'beam.png').convert('RGBA');ki=Image.open(assets/'ki-impact.png').convert('RGBA')
 beam_tiles=[sheet.crop((i%4*sheet.width//4,i//4*sheet.height//4,(i%4+1)*sheet.width//4,(i//4+1)*sheet.height//4)) for i in range(16)]
 ki_tiles=[ki.crop((i%4*ki.width//4,i//4*ki.height//4,(i%4+1)*ki.width//4,(i//4+1)*ki.height//4)) for i in range(16)]
 for group,tiles in [(64900,beam_tiles),(64901,ki_tiles[:4]),(64902,ki_tiles[4:8]),(64903,ki_tiles[8:12])]:
  for index,im in enumerate(tiles):
   pixels=np.asarray(im);mask=pixels[:,:,3]>64;ys,xs=np.where(mask)
   # Beam inlet and centre are measured from actual alpha, never an atlas cell.
   if group==64900:
    inlet=xs.min();near=mask&(np.indices(mask.shape)[1]<inlet+max(4,im.width*.12))
    y=int(np.median(np.where(near)[0]));axis=(int(inlet),y)
   else:axis=(round((xs.min()+xs.max())/2),round((ys.min()+ys.max())/2))
   sprites.append(dict(key=(group,index),image=im,axis=axis))
 lookup={s['key']:s for s in sprites}
 beam_actions={a:0 for a in beam.values()}
 for state,action in beam.items():beam_actions[action]=ANGLES[kind].get(state,0)
 flight_actions={405,1550,31550} if kind=='gt-goku' else {405,1550,31550}
 charge_actions={1420,425,1430} if kind=='gt-goku' else {1420,425}
 impact_actions={415,420,421,1560} if kind=='goku' else set()
 roots=set();angles={}
 for path in source.glob('*.cns'):
  for block in blocks(path.read_text(encoding='cp1252')):
   match=re.match(r'\[Statedef\s+(\d+)',block,re.I)
   if not match:continue
   state=int(match[1])
   for ctl in controllers(block):
    if not re.search(r'^type\s*=\s*Helper',ctl,re.I|re.M):continue
    target=re.search(r'^stateno\s*=\s*(\d+)',ctl,re.I|re.M)
    if target and int(target[1]) in set(beam)|flights|charges|{425,635}:
     for expression in re.findall(r'^anim\s*=\s*(.+)',block,re.I|re.M)[:1]:
      # Root state/action numbers coincide except native common form offsets.
      roots.add(state)
      initial=re.match(r'\s*(\d+)',expression)
      if initial:
       base=int(initial[1]);roots.add(base)
       offsets=(0,2000,11000,13000,15000,17000) if 'var(11)' in expression.replace(' ','').lower() else (0,24000,26000,28000,30000,32000) if 'var(14)' in expression.replace(' ','').lower() else (0,23000,25000,27000,29000,31000) if 'var(15)' in expression.replace(' ','').lower() else (0,)
       roots.update(base+o for o in offsets)
 if kind=='goku':
  roots|={400+o for o in (0,2000,11000,13000,15000,17000)}|{620+o for o in (0,2000,11000,13000,15000,17000)}
  roots|={1400+o+i for o in (0,24000,26000,28000,30000,32000) for i in range(5)}
  roots|={1500+o for o in (0,24000,26000,28000,30000,32000)}|{1700+o+i for o in (0,24000,26000,28000,30000,32000) for i in range(2)}
 else:
  roots|={400+o for o in (0,2000,11000,13000,15000)}|{401+o for o in (0,2000,11000,13000,15000)}
 roots|={400,401,620,1400,1401,1402,1700,1701,31500}
 maps=['\n[State -3, Active release pose]\ntype=MapSet\ntrigger1=!ishelper\nmap="goku.emitting"\nvalue=0\nignorehitpause=1\n','\n[State -3, Default hand x]\ntype=MapSet\ntrigger1=!ishelper\nmap="goku.muzzle_x"\nvalue=24\nignorehitpause=1\n','\n[State -3, Default hand y]\ntype=MapSet\ntrigger1=!ishelper\nmap="goku.muzzle_y"\nvalue=-40\nignorehitpause=1\n'];registrations=[];result=[]
 for block in re.split(r'(?=^\[Begin Action\s+)',air,flags=re.I|re.M):
  match=re.match(r'\[Begin Action\s+(\d+)',block,re.I)
  if not match:result.append(block);continue
  action=int(match[1]);local=action%1000000;bank=action//1000000-1
  lines=[];anchors=[];emitting=[];index=0
  for line in block.splitlines():
   row=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
   if row:
    fields=line.split(';',1)[0].split(',')
    while len(fields)<9:fields.append('')
    key=tuple(map(int,fields[:2]));index+=1
    if key[0] in range(62000,62300) and local in roots and bank>=0:
     sprite=lookup[key];hx,hy=palm(sprite)
     flip=fields[5].strip().upper()
     x=((hx-sprite['axis'][0])*(-1 if 'H' in flip else 1)*float(fields[7] or 1)+float(fields[2]))*1.65
     y=((hy-sprite['axis'][1])*(-1 if 'V' in flip else 1)*float(fields[8] or 1)+float(fields[3]))*1.65
     if kind=='gt-goku' and local in (400,401,620):
      # Native aerial ki pose rotates fifteen degrees clockwise.
      if local==620:
       theta=math.radians(-15);x,y=x*math.cos(theta)+y*math.sin(theta),-x*math.sin(theta)+y*math.cos(theta)
     anchors.append((index,round(x,3),round(y,3)))
     if key[0] in range(62200,62208) and key[1] in (4,5,6,7) or key[0] in range(62000,62008) and key[1]==13:
      emitting.append(index)
    family=64900 if local in beam_actions else 64901 if local in flight_actions else 64902 if local in charge_actions else 64903 if local in impact_actions else None
    if family is not None and key[0]>=0:
     phase=(index-1)%4 if family!=64900 else (index-1 if index<=4 else 4+(index-5)%8)
     sprite=lookup[family,phase];im=sprite['image'];bounds=im.getbbox()
     width=300 if family==64900 else 20 if family==64901 else 32 if family==64903 else 18
     height=36 if family==64900 else 11 if family==64901 else 32 if family==64903 else 18
     fields[:4]=map(str,(family,phase,0,0));fields[5]=''
     fields[7]=str(width/(bounds[2]-bounds[0]));fields[8]=str(height/(bounds[3]-bounds[1]))
     line=','.join(fields)
   # Replace the source collision rectangles with the actual visible path.
   if local in beam_actions or local in flight_actions:
    if re.match(r'^\s*Clsn[12]',line,re.I):continue
   lines.append(line)
  if local in beam_actions:
   theta=math.radians(beam_actions[local]);boxes=[]
   for i in range(12):
    x=(i+.5)*25*math.cos(theta);y=-(i+.5)*25*math.sin(theta)
    boxes.append(f'Clsn1[{i}]={x-18:.2f},{y-10:.2f},{x+18:.2f},{y+10:.2f}')
   lines[1:1]=['Clsn1Default:12',*boxes]
  elif local in flight_actions:lines[1:1]=['Clsn1Default:1','Clsn1[0]=-7,-7,7,7']
  if anchors:
   if emitting:
    conditions=' || '.join(f'animelemno(0)={i}' for i in emitting)
    maps.append(f'\n[State -3, Keep beam on releasing palms]\ntype=MapSet\ntriggerall=!ishelper\ntrigger1=anim={action}\nmap="goku.emitting"\nvalue=({conditions})\nignorehitpause=1\n')
   def expression(dim):
    values=[(i,xy[dim]) for i,*xy in anchors];expr=str(values[-1][1])
    for i,value in reversed(values[:-1]):expr=f'ifelse(animelemno(0)={i},{value},{expr})'
    return expr
   for dim,name in enumerate(('x','y')):
    maps.append(f'\n[State -3, Illustrated hand {name}]\ntype=MapSet\ntriggerall=!ishelper\ntrigger1=anim={action}\nmap="goku.muzzle_{name}"\nvalue={expression(dim)}\nignorehitpause=1\n')
   registrations.append(dict(animation=action,anchors=anchors))
  result.append('\n'.join(lines)+'\n')
 impact=['\n[Begin Action 960400]']
 for phase in range(4):
  im=lookup[64903,phase]['image'];bounds=im.getbbox()
  impact.append(f'64903,{phase},0,0,3,,AS200D256,{32/(bounds[2]-bounds[0])},{32/(bounds[3]-bounds[1])}')
 result.append('\n'.join(impact)+'\n')
 (folder/'shot-registration.json').write_text(json.dumps(dict(beam_states=beam,beam_end_states=ENDS[kind],flight_states=sorted(flights),registrations=registrations),indent=2))
 return ''.join(result),''.join(maps)
