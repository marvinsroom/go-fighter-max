"""Replace every imported AIR raster reference with illustrated actors/FX."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,re,io,struct
from isolated_sprite_atlas import extract
from luffy_model import FORMS
BANKS=FORMS+[dict(id=5,slug='tankman',name='Tankman finisher',base=9900,height=96)]

def write_v2(path,sprites):
 """Encode shared illustrated FX once, retaining each registration point."""
 headers=[];payload=bytearray();keys=set();images={}
 for sprite in sprites:
  key=sprite['key']
  if key in keys:continue
  keys.add(key);im=sprite['image'];identity=id(im)
  if identity in images:offset=length=0;link=images[identity]
  else:
   buffer=io.BytesIO();im.save(buffer,format='PNG');raw=struct.pack('<I',im.width*im.height*4)+buffer.getvalue()
   offset=len(payload);length=len(raw);link=0;images[identity]=len(headers);payload.extend(raw)
  headers.append(struct.pack('<HHHHhhHBBIIHH',*key,im.width,im.height,*sprite['axis'],link,12,32,offset,length,0,0))
 header=bytearray(512);header[:12]=b'ElecbyteSpr\0';header[12:16]=bytes((0,0,1,2));lo=512+28*len(headers)
 struct.pack_into('<IIIIIIII',header,36,512,len(headers),lo,0,lo,len(payload),lo+len(payload),0)
 Path(path).write_bytes(header+b''.join(headers)+payload)

def body_form(key):
 g,n=key
 if g==300:return 1 if n>=20 else 0
 if g==0:
  if n<6:return 0
  if n<100 or 640<=n<670:return 2
  if 700<=n<1160 or 1240<=n<1320 or 1360<=n<1400:return 3
  if 1440<=n<1760 and n!=1480:return 4
  if 2080<=n<2160:return 1
  return None
 if g in (5,6,20,40,100,111,120,121,122,200,5300) or 5000<=g<=5072:return 0
 return None

def pose(action,form,index,total):
 base=BANKS[form]['base'];offset=action-base
 if offset in (0,1,5):return index%2
 if offset in (20,21):return 2+index%2
 if 40<=offset<50 or offset==80:return 5 if index<total*.7 else 7
 if 100<=offset<=155:return 4
 if offset in (60,65,70,100):return 3
 if action in (500,4500,6500,70499) or action>=60020 and action<=60024:return 12
 if 5000<=action<=5300 or 5000<=offset<=5300:return 15 if action in (5110,5120) else 6 if index<total/2 else 14
 if action in (170,6171,70171):return 15
 if action in (190,191,900,901,5999,69999):return 12
 sequence=[8,9,10,0]
 if action in (1400,1700,43000,41649,71350):sequence=[8,13,13,0]
 elif action in (400,610,800,2400,2620,4400,4630,6400,6610,70235,70236,71150):sequence=[8,11,11,7]
 return sequence[min(3,int(index*4/max(1,total)))]

def install(folder,air):
 art=folder/'art/illustrated-v1';out=art/'poses';out.mkdir(exist_ok=True)
 frames=[];banks={};metadata=[]
 for form in BANKS:
  tiles=extract(art/(form['slug']+'.png'),4,4);scale=form['height']*4/tiles[0][0].height
  for i,(im,bounds) in enumerate(tiles):
   im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
   anchor=.25 if i in (9,10,13) else .5
   entry=dict(key=(62000+form['id'],i),image=im,axis=(round(im.width*anchor),im.height));frames.append(entry);banks[form['id'],i]=entry
   im.save(out/f'{form["slug"]}-{i}.png');metadata.append(dict(form=form['id'],pose=i,bounds=bounds,size=im.size,axis=entry['axis']))
 sheet=Image.open(art/'effects.png').convert('RGBA');fx=[]
 for i in range(16):
  x=i%4;y=i//4;tile=sheet.crop((x*sheet.width//4,y*sheet.height//4,(x+1)*sheet.width//4,(y+1)*sheet.height//4))
  im=ImageOps.contain(tile,(512,512),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(512,512));canvas.alpha_composite(im,((512-im.width)//2,(512-im.height)//2));fx.append(canvas);canvas.save(art/f'fx-{i}.png')
 original=json.loads((folder/'reference/sprites.json').read_text());sizes={tuple(s['key']):s for s in original};mapped_fx={};effect_rows=0;actor_rows=0
 # Every effect gets the source coordinate footprint and registration.
 for s in original:
  key=tuple(s['key']);g,n=key
  if body_form(key) is not None or key in mapped_fx:continue
  w,h=s['size'];w=max(w,1);h=max(h,1)
  if w<=1 and h<=1:
   im=Image.new('RGBA',(1,1))
  elif g==9021:
   # Upstream uses this neutral white field with subtractive transparency to
   # darken the arena. A painted impact here would obscure the whole screen.
   im=Image.new('RGBA',(2,2),(255,255,255,255))
  elif g==9000 or g in (950,9018):
   portrait=Image.open(art/'portrait.png').convert('RGBA');im=ImageOps.fit(portrait,(800,600),Image.Resampling.LANCZOS,centering=(.5,.3))
  else:
   motif=3 if g in (7017,8230,8216) else 12 if g in (9022,7042) else 8 if g in (7052,7053,1055) else 11 if g in (1065,8400) else 2 if g in (1050,1051,1054,1058) else 4 if g in (3051,8240) else 0 if w<100 and h<100 else 7 if w>h*3 else 10 if h>w*2 else 1
   if g==0:
    if 1760<=n<1800:motif=13
    elif 1800<=n<1880:motif=10
    elif 1160<=n<1240 or 1320<=n<1440:motif=11
    elif 200<=n<240:motif=3
    elif 280<=n<640:motif=8 if n<360 else 2
    elif 1924<=n<=1930:motif=12
   im=fx[motif]
  # New sprite numbers are dense and isolated from source IDs.
  newkey=(64000,len(mapped_fx));mapped_fx[key]=(newkey,w/im.width,h/im.height)
  sx=w/im.width;sy=h/im.height;axis=(round(s['axis'][0]/sx),round(s['axis'][1]/sy))
  while max(map(abs,axis))>32000:
   im=im.resize((max(1,im.width//2),max(1,im.height//2)));sx=w/im.width;sy=h/im.height;axis=(round(s['axis'][0]/sx),round(s['axis'][1]/sy))
  mapped_fx[key]=(newkey,sx,sy);frames.append(dict(key=newkey,image=im,axis=axis))
 result=[]
 for block in re.split(r'(?=^\[Begin Action\s+)',air,flags=re.I|re.M):
  match=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
  if not match:result.append(block);continue
  action=int(match[1]);lines=block.splitlines();total=sum(bool(re.match(r'^\s*\d+\s*,\s*\d+\s*,',l)) for l in lines);index=0;new=[]
  for line in lines:
   row=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
   if not row:new.append(line);continue
   fields=line.split(';',1)[0].split(',')
   while len(fields)<9:fields.append('')
   key=tuple(map(int,fields[:2]));form=body_form(key)
   if form is not None:
    if 9900<=action<10000 and key[0]==300:form=5
    # Imported common hurt poses use the source base bank; render selected form
    # with per-form custom common actions installed by the roster controller.
    pose_id=pose(action,form,index,total);newkey=(62000+form,pose_id);sx=sy=.25;actor_rows+=1
   elif key in mapped_fx:newkey,sx,sy=mapped_fx[key];effect_rows+=1
   else:newkey=(-1,0);sx=sy=1
   fields[:2]=map(str,newkey)
   for dim,mult in ((7,sx),(8,sy)):fields[dim]=str((float(fields[dim].strip()) if fields[dim].strip() else 1)*mult)
   new.append(','.join(fields));index+=1
  result.append('\n'.join(new)+'\n')
 air=''.join(result)
 # Portraits used by character select, separate from cut-in remapping.
 portrait=Image.open(art/'portrait.png').convert('RGBA')
 for n,size in [(0,(200,200)),(1,(960,1120))]:frames.append(dict(key=(9000,n),image=ImageOps.fit(portrait,size,Image.Resampling.LANCZOS,centering=(.5,.3)),axis=(0,0)))
 for form in FORMS:
  fid=form['id']
  for action,poses in [(60000+fid,[(0,10),(1,10)]),(60020+fid,[(12,6),(12,6)]),(60040+fid,[(6,8),(14,8)]),(60060+fid,[(4,8)])]:
   air+=f'\n[Begin Action {action}]\nClsn2Default:1\nClsn2[0]=-12,-60,12,0\n'
   for pi,ticks in poses:air+=f'{62000+fid},{pi},0,0,{ticks},,,.25,.25\n'
 from luffy_funny_intro import install as funny_intro,LENGTH
 air+=funny_intro(folder,frames,out)
 for i in (2,3,12):frames.append(dict(key=(63000,i),image=fx[i],axis=(256,512)))
 air+='\n[Begin Action 60101]\n63000,3,0,0,6,,AS150D256,.18,.18\n63000,12,0,0,6,,AS130D256,.18,.18\n'
 output=folder.parents[1]/'engine/ikemen-go-v1.0.0/chars/luffy';write_v2(output/'Luffy.sff',frames)
 (folder/'illustrated-build.json').write_text(json.dumps(dict(drawings=96,intro_drawings=16,intro_art='art/funny-intro-v2',intro_kind='funny meat gag',starting_form=0,effects=16,referenced_original_sprites=0,actor_rows=actor_rows,effect_rows=effect_rows,poses=metadata,intro_duration=LENGTH),indent=2))
 return air
