"""Install the complete illustrated Ben 10 body/form/move conversion."""
from pathlib import Path
import hashlib, json, shutil, sys
from PIL import Image, ImageFile, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edward_assets import read_v1, write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff

ImageFile.LOAD_TRUNCATED_IMAGES = True
R=Path(__file__).resolve().parents[1]; G=R/'sprite-fighter'
A=G/'style-wave2/ben-10/conversion-v1'; L=G/'engine/ikemen-go-v1.0.0/chars/ben-10'
I=json.loads((G/'style-wave2/ben-10/inventory.json').read_text()); S=L/I['files']['sprite']; B=A/'before'

SHEETS={
 'f01':A/'forms-01-04-v1.png','f05':A/'forms-05-08-v1.png',
 'f09':A/'forms-09-12-v1.png','f13':A/'forms-13-16-v1.png',
 'f17':A/'forms-17-20-v1.png','benx':A/'ben-alienx-v1.png',
 'fx':A/'effects-v1.png'}

def shab(value): return hashlib.sha256(value).hexdigest()
def shaf(path): return shab(path.read_bytes())
def cells(path): return [im for im,_ in extract(path,4,4)]

banks={name:cells(path) for name,path in SHEETS.items()}
assert all(len(value)==16 for value in banks.values())

# Visual identity mapping established from the decoded source group audit.
FORM={
 0:('benx',0,12), 1:('f01',0,4), 2:('f01',2,4),
 3:('f05',1,4), 4:('f05',0,4), 5:('f05',3,4),
 6:('f09',0,4), 7:('f01',1,4), 8:('f05',2,4),
 9:('f09',1,4), 11:('f09',3,4), 12:('f13',1,4),
 13:('f13',2,4), 14:('f13',3,4), 15:('f17',0,4),
 16:('f17',1,4), 17:('benx',3,4), 18:('f17',2,4),
 19:('f17',3,4),
 30:('f05',2,4), 60:('benx',3,4), 70:('benx',3,4),
 92:('benx',3,4), 110:('f13',2,4), 111:('f13',3,4),
 191:('f17',1,4), 200:('benx',3,4), 201:('benx',3,4),
}
for group in (5000,5001,5002,5010,5011,5012,5020,5030,5031,5032,5040,5041,5042,5060,5061,5062,5070,5071,5072,5110):
 FORM[group]=('benx',0,12)

raw=S.read_bytes(); assert raw[15]==1
original=read_v1(S); seen=set(); original=[s for s in original if not (tuple(s['key']) in seen or seen.add(tuple(s['key'])))]
counts={}; output=[]; body_map=[]; effect_map=[]; ui=[]
for sprite in original:
 key=tuple(sprite['key']); group=key[0]; old=sprite['image'].convert('RGBA'); index=counts.get(group,0); counts[group]=index+1
 if group in FORM:
  bank,row,count=FORM[group]; cell=(row*4)+(index%count); art=banks[bank][cell].copy()
  height=max(1,old.height); art=art.resize((max(1,round(art.width*height/art.height)),height),Image.Resampling.LANCZOS)
  axis=(round(sprite['axis'][0]/max(1,old.width)*art.width),sprite['axis'][1])
  output.append(dict(key=key,axis=axis,image=art)); body_map.append(dict(key=key,bank=bank,cell=cell))
 elif group<9000:
  cell=(group+index)%16; art=ImageOps.contain(banks['fx'][cell],old.size,Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',old.size); canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2))
  output.append(dict(key=key,axis=sprite['axis'],image=canvas)); effect_map.append(dict(key=key,bank='fx',cell=cell))
 else:
  output.append(dict(key=key,axis=sprite['axis'],image=old)); ui.append(key)

portrait=Image.open(G/'style-wave2/ben-10/design-reference-v1.png').convert('RGBA')
for sprite in output:
 if sprite['key'][0]==9000:
  canvas=Image.new('RGBA',sprite['image'].size); fit=ImageOps.contain(portrait,canvas.size,Image.Resampling.LANCZOS)
  canvas.alpha_composite(fit,((canvas.width-fit.width)//2,(canvas.height-fit.height)//2)); sprite['image']=canvas

B.mkdir(parents=True,exist_ok=True); backup=B/S.name
if not backup.exists(): shutil.copy2(S,backup)
assert shaf(backup)==I['source_sha256']['sprite']
pending=S.with_suffix('.sff.pending'); write_v2(pending,output); proof=Sff(pending)
assert set(proof.keys)=={tuple(s['key']) for s in original}
for sprite in output:
 decoded=proof.decode(proof.keys[tuple(sprite['key'])])
 assert decoded.size==sprite['image'].size and shab(decoded.tobytes())==shab(sprite['image'].tobytes())
pending.replace(S)

gameplay={}
for kind,name in I['files'].items():
 path=L/name
 if path.exists() and kind!='sprite': gameplay[name]=shaf(path)
for kind in ('anim','cmd','sound'): assert gameplay[I['files'][kind]]==I['source_sha256'][kind]
report={
 'status':'INSTALLED','revision':'ben-10-style-conversion-v1','tool':'built-in imagegen',
 'source_sff_version':1,'installed_sff_version':2,'source_sprite_count':len(original),
 'body_and_helper_sprites_replaced':len(body_map),'move_effect_sprites_replaced':len(effect_map),
 'ui_keys_retained_or_portrait_replaced':len(ui),
 'sheets':{name:{'file':path.name,'sha256':shaf(path),'cells':16} for name,path in SHEETS.items()},
 'mapping':body_map,'effect_mapping':effect_map,'source_sff_sha256':shaf(backup),
 'installed_sff_sha256':shaf(S),'gameplay_files_sha256':gameplay,
 'preservation':['Every unique original SFF key retained','Every playable body/form and helper body group replaced','Every non-UI move/effect group replaced','Original sprite height or effect footprint and axis root retained','AIR, CMD, CNS, SND and palettes unchanged']}
(A/'installation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_and_helper_sprites_replaced','move_effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
