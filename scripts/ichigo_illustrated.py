"""Compile illustrated actors and effects into the imported combat timing.

Each AIR action selects its own drawings. All source raster references are
replaced; state logic, hit boxes, velocities and sound remain source-authored.
"""
from collections import Counter
import hashlib,io,json,re
import numpy as np
from PIL import Image,ImageOps,ImageDraw
from isolated_sprite_atlas import extract
from mugen_sff import Sff
from ichigo_model import FORMS

BODY={0:0,5:0,6:0,20:0,40:0,100:0,120:0,121:0,122:0,200:0,201:0,206:3,
 **{g:0 for g in range(5000,5080)},5300:0,
 11000:2,11200:2,12000:2,13000:3,13200:3,14000:3,
 15000:4,15005:4,15006:4,15020:4,15040:4,15120:4,15122:4,15200:4,16000:4,
 17000:5,17006:5,17020:5,17040:5,17100:5,17120:5,17190:5,17200:5,18000:5,
 19000:6,19005:6,19006:6,19020:6,19040:6,19100:6,19120:6,19200:6,20000:6,20020:6,
 21000:7,21200:7,22000:7,22022:7,
 23000:8,23006:8,23020:8,23040:8,23120:8,23121:8,23122:8,23201:8,24000:8,
 23001:9,23007:9,23021:9,23041:9,23123:9,23124:9,23125:9,26000:9,
 23002:10,23008:10,23022:10,23042:10,23126:10,23127:10,26001:10,
 23003:11,23009:11,23023:11,23043:11,23128:11,23129:11,23202:11,26002:11}
HURT=set(range(5000,5080))|{5300,12000,14000,16000,18000,20000,22000,24000,26000,26001,26002}
BACKDROPS={8000,8100,8560,8561,8989,8990,10002,10003,10010,10011,10012,10013,10021,10025,10026}
CYAN={1053,1054,1057,1075,1808,1818,1829,1842,19300,2000,2001,2005,2009,2010,2011,2250,2350,23500,7000,7006,7008,7022,7200,7201,9200,10200}
RED={300,1055,1064,1550,1551,1552,15520,11550,51550,2455,2467,2482,2514,2534,2551,2555,7357}
BEAMS={1550,1551,1552,15520,11550,51550,1575,7052,7053,7054,7600,7601}
PILLARS={1050,1060,10620,3008,3009,7021,8345,8500,2367,2368,23680}

PAYLOADS={}
def packed(im,axis):
 if id(im) not in PAYLOADS:
  b=io.BytesIO();im.save(b,format='PNG')
  PAYLOADS[id(im)]=dict(image=im,png=b.getvalue(),rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())
 return dict(PAYLOADS[id(im)],axis=axis)

def actor_form(source,key):
 g,n=key
 if g not in BODY:return None
 if g==0:return 0 if n<287 else None
 if g==15200 and n>=70:return 12
 if g in (23000,23001,23002,23003):
  if n==95:return BODY[g] # White-haired source transition silhouette.
  # Later-series banks mix actors with FX. Actor-sized bounds plus orange
  # hair separate them; large energy pillars must never become idle bodies.
  h=source.headers[source.keys[key]]
  if h[2]>220 or h[3]>150:return None
  px=np.asarray(source.decode(source.keys[key])).astype(np.int16)
  r,gc,b,a=[px[:,:,i] for i in range(4)]
  hair=(a>128)&(r>110)&(gc>45)&(gc<220)&(r>gc*1.2)&(gc>b*1.3)
  if np.count_nonzero(hair)<3:return None
 return BODY[g]

def pose_for(action,form,group,index,count):
 base=next((f['base'] for f in FORMS if f['id']==form),15000)
 off=action-base;t=index/max(1,count-1)
 def seq(items):return items[min(len(items)-1,int(t*len(items)))]
 if 60000<=action<60020:return seq([12,13,0])
 if 60020<=action<60040:return 12
 if group in HURT:return 15 if action%1000>=70 else 14
 if off in (0,5):return index%2
 if off in (10,11,12):return 4
 if off in (20,21):return 2+index%2
 if off in (40,41,42,43,44,45,47,50,51):return 5
 if off==52:return 7
 if off in (100,105):return 6
 if 120<=off<=159:return 11
 if off in (170,175,180,185,190,195):return seq([12,13,0])
 if off in (500,501):return 12
 move=action%10000 if action>=100000 else off
 if action>=100000 and move>=3000:return seq([12,8,13,13,11])
 if 400<=move<500:return seq([4,8,10,4])
 if 600<=move<700:return seq([5,8,9,5])
 sequences=[[8,9,10,11],[8,9,13,11],[4,8,9,7],[6,9,10,11],[12,13,13,11],[8,10,9,11]]
 return seq(sequences[(move//100)%len(sequences)])

def install(root,output,air):
 folder=root/'sprite-fighter/characters/ichigo';old=folder/'art/illustrated-v1';art=folder/'art/illustrated-v2'
 poses=art/'poses';poses.mkdir(exist_ok=True)
 source=Sff(output/'Ichigo.sff');banks={};meta={};additions={};replaced={}
 all_forms=FORMS+[dict(id=12,slug='mugetsu',name='Mugetsu')]
 for form in all_forms:
  slug=form['slug'];path=art/(slug+'.png')
  if not path.exists():path=old/(slug+'.png')
  tiles=extract(path,4,4);unit=55/((tiles[0][0].height+tiles[1][0].height)/2)
  for i,(im,bounds) in enumerate(tiles):
   w,h=max(1,round(im.width*unit*4)),max(1,round(im.height*unit*4))
   im=im.resize((w,h),Image.Resampling.LANCZOS)
   anchor=[.48,.48,.48,.48,.48,.48,.48,.52,.48,.35,.48,.48,.50,.38,.48,.5][i]
   frame=packed(im,(round(w*anchor),h));banks[form['id'],i]=frame
   additions[62000+form['id'],i]=frame;im.save(poses/f'{slug}-{i}.png')
   meta[f'{form["id"]}:{i}']=dict(source=path.relative_to(folder).as_posix(),bounds=bounds,size=[w,h],axis=frame['axis'])
 # Retain disconnected particles within each generated FX cell.
 sheet=Image.open(art/'effects.png').convert('RGBA');fx=[]
 for i in range(16):
  x=i%4;y=i//4;tile=sheet.crop((round(x*sheet.width/4),round(y*sheet.height/4),round((x+1)*sheet.width/4),round((y+1)*sheet.height/4)))
  tile=ImageOps.contain(tile,(512,512),Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',(512,512));canvas.alpha_composite(tile,((512-tile.width)//2,(512-tile.height)//2));fx.append(canvas)
  canvas.save(art/f'fx-{i}.png')
 # Arena-resolution geometric pressure field replaces source screen captures.
 backdrop=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(backdrop)
 for y in range(720):d.line((0,y,1280,y),fill=(5+int(10*y/720),8+int(5*y/720),20+int(13*y/720),238))
 for i in range(22):
  y=(i*139)%720;x=(i*211)%900
  d.polygon([(x,y),(x+300,y-3),(x+380,y),(x+50,y+2)],fill=(100+4*i,25,40,90))
 backdrop.save(art/'spiritual-pressure.png')
 portrait=Image.open(old/'portrait.png').convert('RGBA')
 for h in source.headers:
  if h[0]==9000:
   size=(200,200) if h[1]==0 else (960,1120)
   replaced[h[:2]]=packed(ImageOps.fit(portrait,size,Image.Resampling.LANCZOS,centering=(.5,.25)),(0,0))
 forms={key:actor_form(source,key) for key in source.keys};fx_keys={};fx_scale={};usage=Counter();action_audit=[]
 for key,index in source.keys.items():
  if forms[key] is not None:continue
  g,n=key;h=source.headers[index];w,height=h[2:4]
  if not w or not height:continue
  if g in BACKDROPS:im=backdrop
  elif g in (10000,771,9000):im=ImageOps.fit(portrait,(960,540),Image.Resampling.LANCZOS,centering=(.5,.32))
  elif g in (9021,9023):im=Image.new('RGBA',(1280,720),(245,244,255,255))
  else:
   if g in BEAMS:motif=15
   elif g in PILLARS:motif=13 if g in RED else 12
   elif g in CYAN:motif=n%4
   elif g in RED:motif=4+n%4
   elif w>height*3:motif=8
   elif height>w*2.5:motif=13 if g%2 else 12
   else:motif=[10,11,14,9][(g+n//4)%4]
   im=fx[motif]
  # Dissipating source particles can be only a few pixels wide with distant
  # registration points. Keep their SFF signed axes representable.
  while abs(h[4]*im.width/w)>32000 or abs(h[5]*im.height/height)>32000:
   im=im.resize((max(1,im.width//2),max(1,im.height//2)),Image.Resampling.LANCZOS)
  newkey=(64000,len(fx_keys));fx_keys[key]=newkey
  sx=w/im.width;sy=height/im.height;fx_scale[key]=(sx,sy)
  additions[newkey]=packed(im,(round(h[4]/sx),round(h[5]/sy)))
 out=[]
 for block in re.split(r'(?=^\[Begin Action\s+)',air,flags=re.I|re.M):
  match=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
  if not match:out.append(block);continue
  action=int(match[1]);lines=block.splitlines();body_count=0
  for line in lines:
   row=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
   if row and forms.get(tuple(map(int,row.groups()))) is not None:body_count+=1
  body_index=0;newlines=[];drawings=[]
  for line in lines:
   row=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
   if not row:
    if body_count and re.match(r'^\s*Interpolate\s+Scale',line,re.I):continue
    newlines.append(line);continue
   fields=line.split(';',1)[0].split(',')
   while len(fields)<9:fields.append('')
   key=tuple(map(int,fields[:2]));form=forms.get(key)
   if form is not None:
    if 60000<=action<60020:form=action-60000
    elif 60020<=action<60040:form=action-60020
    pose=pose_for(action,form,key[0],body_index,body_count);body_index+=1
    newkey=(62000+form,pose);scale=(.25,.25);usage['body_frames']+=1;drawings.append([form,pose])
   elif key in fx_keys:newkey=fx_keys[key];scale=fx_scale[key];usage['effect_frames']+=1
   else:
    assert key[0]<0 or key not in source.keys,key
    fields[0:2]=['-1','0'];newlines.append(','.join(fields));continue
   fields[0:2]=map(str,newkey)
   for dim,multiplier in zip((7,8),scale):fields[dim]=str((float(fields[dim].strip()) if fields[dim].strip() else 1)*multiplier)
   newlines.append(','.join(fields))
  if drawings:action_audit.append(dict(action=action,drawings=drawings))
  out.append('\n'.join(newlines)+'\n')
 for i in (12,13):additions[63000,i]=packed(fx[i],(256,512))
 from ichigo_school_intro import install as school_intro
 result=''.join(out)+school_intro(folder,additions)
 (output/'Ichigo.sff').write_bytes(source.derive(replaced,additions))
 result+='\n[Begin Action 60101]\n63000,12,0,0,6,,AS140D256,.12,.12\n63000,13,0,0,6,,AS110D256,.12,.12\n'
 for line in result.splitlines():
  m=re.match(r'^\s*(\d+)\s*,\s*(\d+)\s*,',line)
  if m:assert int(m[1])>=62000,('Unconverted source sprite',line)
 audit=dict(revision=3,art='illustrated',drawings=len(banks),intro_drawings=16,intro_art='art/school-intro-v4',effects=16,mapped_effect_sprites=len(fx_keys),referenced_original_sprites=0,poses=meta,actions=action_audit,**usage)
 (folder/'illustrated-build.json').write_text(json.dumps(audit,indent=2))
 return result
