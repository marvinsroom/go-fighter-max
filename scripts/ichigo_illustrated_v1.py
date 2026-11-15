"""Register distinct illustrated form banks; preserve source effect payloads."""
from pathlib import Path
from PIL import Image,ImageOps
import re,hashlib,io,json
from isolated_sprite_atlas import extract
from mugen_sff import Sff
from ichigo_model import FORMS
from ichigo_animation_map import build
from stable_body_scale import stabilize

def install(root,output,air):
 folder=root/'sprite-fighter/characters/ichigo';art=folder/'art/illustrated-v1';poses=art/'poses';poses.mkdir(exist_ok=True)
 source=Sff(output/'Ichigo.sff');mapping,audit=build(root);banks={};meta={}
 for form in FORMS:
  tiles=extract(art/(form['slug']+'.png'),4,4);unit=55/((tiles[0][0].height+tiles[1][0].height)/2)
  for i,(im,bounds) in enumerate(tiles):
   w,h=round(im.width*unit*4),round(im.height*unit*4);im=im.resize((w,h),Image.Resampling.LANCZOS)
   # Sword contact poses extend rightward: anchor the planted hips, rather
   # than centering the entire sword silhouette and shifting the fighter.
   anchor=[.48,.48,.48,.48,.48,.48,.48,.52,.48,.35,.48,.48,.50,.38,.48,.5][i]
   axis=(round(w*anchor),h);buf=io.BytesIO();im.save(buf,format='PNG')
   banks[form['id'],i]=dict(image=im,axis=axis,png=buf.getvalue(),rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())
   im.save(poses/f'{form["slug"]}-{i}.png');meta[f'{form["id"]}:{i}']=dict(bounds=bounds,size=[w,h],axis=axis,units_per_pixel=unit)
 # Audited body groups. Other groups remain the author's projectiles,
 # auras, slash trails, impact flashes, cinematics and scenery.
 groupforms={g:0 for g in [0,5,6,20,40,100,120,121,122,200,5000,5010,5020,5030,5040,5041,5060,5300]}
 for form,groups in {
  2:[11000,11200,12000],3:[13000,13200,14000],4:[15000,15006,15020,15040,15120,15122,15200,16000],
  5:[17000,17006,17020,17040,17100,17120,17190,17200,18000],6:[19000,19005,19006,19020,19040,19100,19120,19200,20000,20020],
  7:[21000,21200,22000,22022],8:[23000,23006,23020,23040,23120,23121,23122,23201,24000],
  9:[23001,23007,23021,23041,23123,23124,23125,26000],10:[23002,23008,23022,23042,23126,23127,26001],
  11:[23003,23009,23023,23043,23128,23129,23202,26002]}.items():
  groupforms.update({g:form for g in groups})
 replaced={};registration=[]
 for h in source.headers:
  key=h[:2];g,n=key
  if g not in groupforms:continue
  form=groupforms[g];pose=mapping.get(key,(form,0))[1]
  if g==15200 and n>=70:continue # Source silhouette and transient Mugetsu art.
  if g in (5041,):pose=15
  if g in (20,19020,20020,23020,23021,23022,23023):pose=2+n%2
  if g in (100,15020,17020,22022):pose=6
  frame=dict(banks[form,pose]);ox,oy=h[4:6]
  # Retain floating and tumbling source registration in hurt animations.
  if g in (5000,5010,5020,5030,5040,5041,5060,12000,14000,16000,18000,20000,22000,24000,26000,26001,26002):
   ax,ay=frame['axis'];frame['axis']=(ax,ay+(oy-h[3])*4)
  replaced[key]=frame;registration.append(dict(sprite=key,form=form,pose=pose,axis=frame['axis']))
 # Portraits use the roster's illustrated key art.
 portrait=Image.open(art/'portrait.png').convert('RGBA')
 for key,size in [((9000,0),(200,200)),((9000,1),(960,1120))]:
  im=ImageOps.fit(portrait,size,Image.Resampling.LANCZOS,centering=(.5,.25));b=io.BytesIO();im.save(b,format='PNG')
  replaced[key]=dict(image=im,axis=(0,0),png=b.getvalue(),rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())
 additions={};lines=[];current=None
 for form in FORMS:
  for n,pose in enumerate((12,13,0)):
   additions[61000+form['id'],n]=banks[form['id'],pose]
  pattern=r'\[Begin Action '+str(60000+form['id'])+r'\][\s\S]*?(?=\[Begin Action|\Z)'
  block=f'[Begin Action {60000+form["id"]}]\nClsn2Default: 1\nClsn2[0]=-10,-50,10,0\n'
  for n,ticks in enumerate((8,8,14)):block+=f'{61000+form["id"]},{n},0,0,{ticks},,,.25,.25\n'
  air=re.sub(pattern,block+'\n',air,flags=re.I)
  air+=f'\n[Begin Action {60020+form["id"]}]\nClsn2Default: 1\nClsn2[0]=-10,-50,10,0\n{61000+form["id"]},0,0,0,-1,,,.25,.25\n'
 for line in air.splitlines():
  m=re.match(r'\[Begin Action\s+(\d+)\]',line,re.I)
  if m:current=int(m[1])
  m=re.match(r'^\s*(-?\d+)\s*,\s*(-?\d+)\s*,',line)
  if m and (int(m[1]),int(m[2])) in replaced:
   fields=line.split(';',1)[0].split(',')
   while len(fields)<9:fields.append('')
   for i in (7,8):fields[i]=str((float(fields[i].strip()) if fields[i].strip() else 1)/4)
   line=','.join(fields)
  lines.append(line)
 air,changes=stabilize('\n'.join(lines)+'\n',set(replaced))
 (output/'Ichigo.sff').write_bytes(source.derive(replaced,additions))
 (folder/'illustrated-build.json').write_text(json.dumps(dict(drawings=len(banks),mapped_sprites=len(replaced),poses=meta,registration=registration,scale_interpolations=changes,audit=audit),indent=2))
 return air
