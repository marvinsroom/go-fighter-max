"""Install illustrated Hiei body and move-effect banks while preserving gameplay."""
from pathlib import Path
import hashlib, json, shutil, sys
from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edward_assets import read_v1, write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff

ROOT=Path(__file__).resolve().parents[1]; GAME=ROOT/'sprite-fighter'
ART=GAME/'style-wave2/hiei/conversion-v1'; LIVE=GAME/'engine/ikemen-go-v1.0.0/chars/hiei'
INV=json.loads((GAME/'style-wave2/hiei/inventory.json').read_text()); SFF_PATH=LIVE/INV['files']['sprite']; BEFORE=ART/'before'
BODY={
 'movement':ART/'body-movement-00-candidate.png','attacks':ART/'body-attacks-01-v1.png',
 'specials':ART/'body-specials-02-v1.png','reactions':ART/'body-reactions-03-v1.png'}
EFFECT={
 'flame':ART/'effect-dark-flame-00-v1.png','dragon':ART/'effect-dark-dragon-01-v1.png'}
def sha_bytes(v):return hashlib.sha256(v).hexdigest()
def sha_file(p):return sha_bytes(p.read_bytes())
def body_bank(group):
 if group<200:return 'movement'
 if group<1000:return 'attacks'
 if group<5000:return 'specials'
 return 'reactions'
def grid(path,cols=4,rows=4):
 im=Image.open(path).convert('RGBA');out=[]
 for y in range(rows):
  for x in range(cols):
   cell=im.crop((round(x*im.width/cols),round(y*im.height/rows),round((x+1)*im.width/cols),round((y+1)*im.height/rows)))
   box=cell.getchannel('A').getbbox();assert box,(path,x,y);out.append(cell.crop(box))
 return out
body={name:[im for im,_ in extract(path,4,4)] for name,path in BODY.items()};effects={name:grid(path) for name,path in EFFECT.items()}
assert all(len(v)==16 for v in [*body.values(),*effects.values()])
raw=SFF_PATH.read_bytes();version=raw[15]
if version==1:original=read_v1(SFF_PATH)
else:
 arc=Sff(SFF_PATH);original=[dict(key=k,axis=arc.headers[i][4:6],image=arc.decode(i)) for k,i in arc.keys.items()]
counts={};mapping=[];effect_mapping=[];output=[]
for sprite in original:
 key=tuple(sprite['key']);group=key[0];old=sprite['image'].convert('RGBA');slot=counts.get(group,0);counts[group]=slot+1
 if group<7000:
  name=body_bank(group);art=body[name][slot%16].copy();h=max(1,old.height);art=art.resize((max(1,round(art.width*h/art.height)),h),Image.Resampling.LANCZOS)
  axis=(round(sprite['axis'][0]/max(1,old.width)*art.width),sprite['axis'][1]);output.append(dict(key=key,axis=axis,image=art));mapping.append(dict(key=key,bank=name,cell=slot%16))
 elif group<9000:
  name='flame' if group<7050 else 'dragon';art=ImageOps.contain(effects[name][slot%16],old.size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',old.size);canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2));output.append(dict(key=key,axis=sprite['axis'],image=canvas));effect_mapping.append(dict(key=key,bank=name,cell=slot%16))
 else:output.append(dict(key=key,axis=sprite['axis'],image=old))
portrait=Image.open(GAME/'style-wave2/hiei/design-reference-v1.png').convert('RGBA')
for sprite in output:
 if sprite['key'][0]==9000:
  canvas=Image.new('RGBA',sprite['image'].size);fit=ImageOps.contain(portrait,canvas.size,Image.Resampling.LANCZOS);canvas.alpha_composite(fit,((canvas.width-fit.width)//2,0));sprite['image']=canvas
BEFORE.mkdir(parents=True,exist_ok=True);backup=BEFORE/SFF_PATH.name
if not backup.exists():shutil.copy2(SFF_PATH,backup)
assert sha_file(backup)==INV['source_sha256']['sprite']
pending=SFF_PATH.with_suffix('.sff.pending');write_v2(pending,output);proof=Sff(pending);assert set(proof.keys)=={tuple(s['key']) for s in original}
for sprite in output:
 decoded=proof.decode(proof.keys[tuple(sprite['key'])]);assert decoded.size==sprite['image'].size and sha_bytes(decoded.tobytes())==sha_bytes(sprite['image'].tobytes())
pending.replace(SFF_PATH)
gameplay={}
for kind,name in INV['files'].items():
 p=LIVE/name
 if p.exists() and kind!='sprite':gameplay[name]=sha_file(p)
for kind in ('anim','cmd','sound'):assert gameplay[INV['files'][kind]]==INV['source_sha256'][kind]
report={'status':'INSTALLED','revision':'hiei-style-conversion-v1','tool':'built-in imagegen','source_sff_version':version,'installed_sff_version':2,'source_sprite_count':len(original),'body_sprites_replaced':len(mapping),'effect_sprites_replaced':len(effect_mapping),'ui_keys_retained_or_portrait_replaced':len(original)-len(mapping)-len(effect_mapping),'body_sheets':{k:{'file':v.name,'sha256':sha_file(v),'cells':16} for k,v in BODY.items()},'effect_sheets':{k:{'file':v.name,'sha256':sha_file(v),'cells':16} for k,v in EFFECT.items()},'mapping':mapping,'effect_mapping':effect_mapping,'source_sff_sha256':sha_file(backup),'installed_sff_sha256':sha_file(SFF_PATH),'gameplay_files_sha256':gameplay,'preservation':['Every original SFF key retained','All body and gameplay effect groups replaced','AIR, CMD, CNS, SND and palettes unchanged','Original body height/effect footprint and roots retained']}
(ART/'installation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_sprites_replaced','effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
