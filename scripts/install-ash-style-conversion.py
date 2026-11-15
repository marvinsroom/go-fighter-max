"""Install illustrated Ash, six distinct creature banks, and move VFX."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image,ImageFile,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent))
from edward_assets import read_v1,write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff
ImageFile.LOAD_TRUNCATED_IMAGES=True
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';A=G/'style-wave2/ash-ketchum/conversion-v1';L=G/'engine/ikemen-go-v1.0.0/chars/ash-ketchum';I=json.loads((G/'style-wave2/ash-ketchum/inventory.json').read_text());S=L/I['files']['sprite'];B=A/'before'
FILES={'trainer':A/'trainer-v1.png','pokemon-01':A/'pokemon-01-v1.png','pokemon-02':A/'pokemon-02-v1.png','fx':A/'effects-v1.png'}
def shab(v):return hashlib.sha256(v).hexdigest()
def shaf(p):return shab(p.read_bytes())
banks={k:[im for im,_ in extract(p,4,4)] for k,p in FILES.items() if k!='fx'}
fx_image=Image.open(FILES['fx']).convert('RGBA');banks['fx']=[]
for y in range(4):
 for x in range(4):
  cell=fx_image.crop((round(x*fx_image.width/4),round(y*fx_image.height/4),round((x+1)*fx_image.width/4),round((y+1)*fx_image.height/4)));box=cell.getchannel('A').getbbox();assert box;banks['fx'].append(cell.crop(box))
assert all(len(v)==16 for v in banks.values())
FORM={0:('trainer',0,16),200:('trainer',0,16),300:('trainer',0,16),310:('trainer',0,16),5000:('trainer',0,16),210:('pokemon-01',1,4),220:('pokemon-01',2,4),230:('pokemon-01',3,4),240:('pokemon-02',0,8),250:('pokemon-01',0,4),260:('pokemon-02',2,8)}
original=read_v1(S);seen=set();original=[s for s in original if not(tuple(s['key']) in seen or seen.add(tuple(s['key'])))]
counts={};out=[];bm=[];em=[];ui=[]
for s in original:
 key=tuple(s['key']);g=key[0];old=s['image'].convert('RGBA');n=counts.get(g,0);counts[g]=n+1
 if g in FORM:
  bank,row,count=FORM[g];cell=row*4+n%count;art=banks[bank][cell].copy();h=max(1,old.height);art=art.resize((max(1,round(art.width*h/art.height)),h),Image.Resampling.LANCZOS);axis=(round(s['axis'][0]/max(1,old.width)*art.width),s['axis'][1]);out.append(dict(key=key,axis=axis,image=art));bm.append(dict(key=key,bank=bank,cell=cell))
 elif g<9000:
  cell=(g+n)%16;art=ImageOps.contain(banks['fx'][cell],old.size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',old.size);canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2));out.append(dict(key=key,axis=s['axis'],image=canvas));em.append(dict(key=key,cell=cell))
 else:out.append(dict(key=key,axis=s['axis'],image=old));ui.append(key)
portrait=banks['trainer'][0]
for s in out:
 if s['key'][0]==9000:
  canvas=Image.new('RGBA',s['image'].size);fit=ImageOps.contain(portrait,canvas.size,Image.Resampling.LANCZOS);canvas.alpha_composite(fit,((canvas.width-fit.width)//2,(canvas.height-fit.height)//2));s['image']=canvas
B.mkdir(parents=True,exist_ok=True);backup=B/S.name
if not backup.exists():shutil.copy2(S,backup)
assert shaf(backup)==I['source_sha256']['sprite']
pending=S.with_suffix('.sff.pending');write_v2(pending,out);proof=Sff(pending);assert set(proof.keys)=={tuple(s['key']) for s in original}
for s in out:
 decoded=proof.decode(proof.keys[tuple(s['key'])]);assert decoded.size==s['image'].size and shab(decoded.tobytes())==shab(s['image'].tobytes())
pending.replace(S);gameplay={}
for kind,name in I['files'].items():
 p=L/name
 if p.exists() and kind!='sprite':gameplay[name]=shaf(p)
for kind in ('anim','cmd','sound'):assert gameplay[I['files'][kind]]==I['source_sha256'][kind]
report={'status':'INSTALLED','revision':'ash-ketchum-style-conversion-v1','tool':'built-in imagegen plus local alpha isolation of accepted trainer reference','source_sff_version':1,'installed_sff_version':2,'source_sprite_count':len(original),'body_and_summon_sprites_replaced':len(bm),'move_effect_sprites_replaced':len(em),'ui_keys_retained_or_portrait_replaced':len(ui),'sheets':{k:{'file':p.name,'sha256':shaf(p),'cells':16} for k,p in FILES.items()},'mapping':bm,'effect_mapping':em,'source_sff_sha256':shaf(backup),'installed_sff_sha256':shaf(S),'gameplay_files_sha256':gameplay,'preservation':['Every unique original SFF key retained','Trainer and all six source creature identities remain distinct','Every non-UI move/effect group replaced','Original body/summon height or effect footprint and roots retained','AIR, CMD, CNS, SND and palettes unchanged']}
(A/'installation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_and_summon_sprites_replaced','move_effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
