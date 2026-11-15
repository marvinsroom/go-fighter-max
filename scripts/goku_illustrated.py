"""Compile illustrated key poses while retaining source AIR timing and registering shot collisions."""
from goku_model import *
from luffy_illustrated import write_v2
from isolated_sprite_atlas import extract
from PIL import Image,ImageOps
import goku_energy
import goku_alignment
import json
STRIDE=1000000
ACTOR_GROUPS={0,5,6,20,40,100,120,121,122,200,2000,2200,6000,11000,11200,12000,13000,13200,14000,15000,15200,16000,17000,17200,17300,18000,5300,463,465,466}|set(range(5000,5073))
# Upstream UI action rows also name late-added body groups absent from its SFF.
# They still need illustrated bodies rather than becoming invisible FX rows.
ACTOR_GROUPS|={6010,6037,17212,17214,19000,19005,19006,19020,19030,19040,19100,19120,19122,19200,20000,21000,21005,21006,21025,21040,21100,21121,21122,21200,21201,21900,22000,22010,22020,22030,22040,22041,22060,22300}

def pose(action,index,total):
 for base in (5000,6000,12000,14000,16000,18000):
  if base<=action<=base+300:
   offset=action-base
   if offset in (110,120,150,160):return 15
   if offset in (200,201,210):return 7 if index<total*.8 else 0
   return 14
 # Source forms share common motion offsets; named attack action families retain
 # the upstream frame count and phase boundaries rather than changing state time.
 for base in (17000,15000,13000,11000,2000):
  if base<=action<base+1000:action-=base;break
 if action in (0,1,2,5):return index%2
 if action in (20,21):return 2+index%2
 if action in (60,65,70,80,100,101,102,110,111):return 3
 if action in (10,11,12,121,131,141,151):return 4
 if action in (120,122,130,132,140,142,150,152):return 1
 if action in (40,41,42,50,51):return 5 if index<total*.7 else 6
 if action in (52,53):return 7
 if 5000<=action<=5300 or action in (170,171):return 15 if action in (5110,5120,170,171) else 14
 if action in (500,501,190,191,192,700,800,900,1900,1901,1903,1906):return 12
 if action in (900810,900800):return 12
 if 180<=action<200:return 0
 sequence=[8,9,10,0]
 if action in (3000,3001,1600):sequence=[0,12,12,0]
 elif action in (400,401,620,621):sequence=[8,13,13,0]
 elif action in (1400,1700,3100,3200,3300,3400,3700,3900,4000,4100,4250,4300,4400) or action%1000 in (400,700):sequence=[8,13,13,0]
 elif action%1000 in (300,310,320,330,340,610,615,620):sequence=[8,11,11,7]
 return sequence[min(3,index*4//max(1,total))]

def install():
 art=S/'art/illustrated-v1';out=art/'poses';out.mkdir(exist_ok=True)
 sprites=[];manifest=[]
 for bank,slug in enumerate(BANKS):
  tiles=extract(art/(slug+'.png'),4,4)
  scale=52*4/tiles[0][0].height
  for pi,(im,bounds) in enumerate(tiles):
   im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
   axis=(round(im.width*(.25 if pi in (9,10,13) else .5)),im.height)
   sprites.append(dict(key=(62000+bank,pi),image=im,axis=axis));im.save(out/f'{slug}-{pi}.png')
   manifest.append(dict(bank=bank,pose=pi,bounds=bounds,size=im.size,axis=axis))
 techniques=extract(art/'techniques.png',4,4);factor=208/techniques[0][0].height
 for i,(im,bounds) in enumerate(techniques):
  im=im.resize((max(1,round(im.width*factor)),max(1,round(im.height*factor))),Image.Resampling.LANCZOS)
  axis=(im.width//2,im.height);sprites.append(dict(key=(62100,i),image=im,axis=axis));im.save(out/f'technique-{i}.png')
 energy=goku_energy.load(S/'art/energy-v2',BANKS,sprites,out)
 sheet=Image.open(art/'effects.png').convert('RGBA');fx=[]
 for i in range(16):
  x=i%4;y=i//4;tile=sheet.crop((x*sheet.width//4,y*sheet.height//4,(x+1)*sheet.width//4,(y+1)*sheet.height//4))
  fx.append(ImageOps.contain(tile,(512,512),Image.Resampling.LANCZOS))
 source=json.loads((S/'reference/sprites.json').read_text());mapping={}
 white=Image.new('RGBA',(2,2),'white');empty=Image.new('RGBA',(1,1))
 for s in source:
  g,n=s['key'];key=(g,n)
  if g in ACTOR_GROUPS or key in mapping:continue
  w,h=s['size'];w=max(w,1);h=max(h,1)
  background=w>=600 and h>=330 and 1.45<w/h<2.05 and g not in (9000,180,1030)
  motif=13 if background else 1 if w>h*3 else 6 if h>w*1.8 else 0
  motif={161:14,210:9,560:6,561:7,562:6,2560:6,15570:7,17550:8,1057:1,1030:0,8230:1,8240:1,8250:2,9022:12,950:13,9026:15,7000:0,7005:0,3350:5}.get(g,motif)
  if g in (3040,3041,3084):motif=10
  if g in (1053,1036,7035,7036):motif=12
  if g in (402,580):motif=13
  animated=goku_energy.effect_image(energy,g,n,motif)
  im=empty if w==h==1 else white if g in (9021,9022) else goku_alignment.portrait(S,(200,200)) if g in (9000,180) else animated if animated is not None else fx[motif]
  sx=w/im.width;sy=h/im.height;axis=(round(s['axis'][0]/sx),round(s['axis'][1]/sy))
  if max(map(abs,axis))>32000:im=empty;sx=sy=1;axis=(0,0)
  coverage=1
  if g not in (9021,9022,9000,180) and not background:
   limit=320 if motif in (6,7,8,9,12) else 240 if motif in (0,2,3,4,14,15) else None
   if limit:coverage=min(1,limit/max(w,h))
  alpha=48 if background else 96 if g==9022 else None
  newkey=(64000,len(mapping));mapping[key]=(newkey,sx*coverage,sy*coverage,alpha);sprites.append(dict(key=newkey,image=im,axis=axis))
 original=(U/'Goku.air').read_text(encoding='cp1252');blocks=re.split(r'(?=^\[Begin Action\s+)',original,flags=re.I|re.M);results=[];actor_rows=0;effect_rows=0
 # Native-number copies remain for foreign custom-state references. Every
 # installed controller uses a banked action, so common hurt poses match form.
 for forced_bank in (-1,*range(8)):
  for block in blocks:
   m=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
   if not m:
    if forced_bank==-1:results.append(block)
    continue
   action=int(m[1]);total=sum(bool(re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',l)) for l in block.splitlines());index=0;lines=[]
   for line in block.splitlines():
    if line.startswith('[Begin Action'):
     lines.append(f'[Begin Action {action+(forced_bank+1)*STRIDE}]');continue
    row=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
    if not row:lines.append(line);continue
    fields=line.split(';',1)[0].split(',')
    while len(fields)<9:fields.append('')
    key=tuple(map(int,fields[:2]));g,n=key
    if g in ACTOR_GROUPS:
     bank=max(forced_bank,0);newkey=(62000+bank,pose(action,index,total));sx=sy=.25;actor_rows+=1
     phase=min(3,index*4//max(1,total))
     if bank==0 and action in (3000,1600):newkey=(62100,phase)
     elif bank==0 and action==3001:newkey=(62100,[2,2,1,0][phase])
     elif bank==0 and action==1100:newkey=(62100,4+phase)
     elif bank==0 and action==1300:newkey=(62100,[8,8,8,11][phase])
     elif bank==3 and action in (3600,3601,3602):newkey=(62100,12+phase)
     energy_frame=goku_energy.body_frame(action,index,total)
     if energy_frame is not None:newkey=(62200+bank,energy_frame)
     if action in {1400+offset for offset in goku_energy.SPECIAL_OFFSETS} and index==total-2:lines.append('Loopstart')
    elif key in mapping:
     if g in (1057,1015,8230,8240) and index==4 and total>8:lines.append('Loopstart')
     newkey,sx,sy,alpha=mapping[key];effect_rows+=1
     if alpha is not None:
      old=re.fullmatch(r'\s*AS(\d+)D\d+\s*',fields[6],re.I)
      fields[6]=f'AS{min(alpha,int(old[1])) if old else alpha}D256'
    else:newkey=(-1,0);sx=sy=1
    fields[:2]=map(str,newkey)
    for dim,mult in ((7,sx),(8,sy)):fields[dim]=str((float(fields[dim].strip()) if fields[dim].strip() else 1)*mult)
    lines.append(','.join(fields));index+=1
   results.append('\n'.join(lines)+'\n')
 # Dedicated base-form greeting is drawn as a connected sixteen-frame sequence.
 intro=extract(art/'intro-v2.png',4,4);scale=208/intro[0][0].height
 intro_action='\n[Begin Action 960100]\nClsn2Default:1\nClsn2[0]=-12,-50,12,0\n'
 for i,(im,bounds) in enumerate(intro):
  im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
  sprites.append(dict(key=(63200,i),image=im,axis=(im.width//2,im.height)));im.save(out/f'intro-{i}.png')
  intro_action+=f'63200,{i},0,0,10,,,.25,.25\n'
 results.append(intro_action)
 for bank in range(8):
  results.append(f'\n[Begin Action {960200+bank}]\nClsn2Default:1\nClsn2[0]=-12,-50,12,0\n62000,12,0,0,6,,,.25,.25\n'.replace('62000',str(62000+bank)))
  motif=9 if bank in (6,7) else 8 if bank==5 else 7 if bank==4 else 6
  results.append(f'\n[Begin Action {960300+bank}]\n63000,{motif},0,0,6,,AS160D256,.16,.19\n63000,{motif},0,0,6,,AS120D256,.17,.20\n')
 for i,im in enumerate(fx):sprites.append(dict(key=(63000,i),image=im,axis=(im.width//2,im.height)))
 results.append('\n[Begin Action 960308]\n63000,7,0,0,6,,AS160D256,.16,.19\n63000,7,0,0,6,,AS120D256,.17,.20\n')
 for number,size in [(0,(200,200)),(1,(960,1120))]:sprites.append(dict(key=(9000,number),image=goku_alignment.portrait(S,size),axis=(0,0)))
 air,muzzle_maps=goku_alignment.compile_art(S,sprites,''.join(results),U)
 (S/'hand-registration.cns').write_text(muzzle_maps)
 (O/'IA.cns').write_text((O/'IA.cns').read_text()+muzzle_maps)
 write_v2(O/'Goku.sff',sprites)
 (O/'Goku.air').write_text(air)
 (S/'illustrated-build.json').write_text(json.dumps(dict(drawings=272,form_drawings=128,technique_drawings=16,energy_body_drawings=128,animated_effect_drawings=32,intro_drawings=16,effects=16,referenced_original_sprites=0,actor_rows=actor_rows,effect_rows=effect_rows,poses=manifest),indent=2))
 return len(sprites)
