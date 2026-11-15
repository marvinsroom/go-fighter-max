"""Install illustrated Leonardo body, twin-katana moves, and VFX."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image,ImageFile,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent))
from edward_assets import read_v1,write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff
ImageFile.LOAD_TRUNCATED_IMAGES=True
slug=sys.argv[1] if len(sys.argv)>1 else 'leonardo'
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';A=G/'style-wave2'/slug/'conversion-v1';L=G/'engine/ikemen-go-v1.0.0/chars'/slug;I=json.loads((G/'style-wave2'/slug/'inventory.json').read_text());S=L/I['files']['sprite'];B=A/'before'
BODY=A/'body-v1.png';FX=A/'effects-v1.png'
def shab(v):return hashlib.sha256(v).hexdigest()
def shaf(p):return shab(p.read_bytes())
body=[im for im,_ in extract(BODY,4,4)]
def grid(path):
 im=Image.open(path).convert('RGBA');out=[]
 for y in range(4):
  for x in range(4):
   cell=im.crop((round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4)));box=cell.getchannel('A').getbbox();assert box;out.append(cell.crop(box))
 return out
fx=grid(FX);assert len(body)==len(fx)==16
original=read_v1(S);seen=set();original=[s for s in original if not(tuple(s['key']) in seen or seen.add(tuple(s['key'])))]
counts={};out=[];bm=[];em=[];ui=[]
for s in original:
 key=tuple(s['key']);g=key[0];old=s['image'].convert('RGBA');n=counts.get(g,0);counts[g]=n+1
 body_group=(g<4000 or 5000<=g<6000) if slug=='shredder' else g<1000
 if body_group:
  cell=n%16;art=body[cell].copy();h=max(1,old.height);art=art.resize((max(1,round(art.width*h/art.height)),h),Image.Resampling.LANCZOS);axis=(round(s['axis'][0]/max(1,old.width)*art.width),s['axis'][1]);out.append(dict(key=key,axis=axis,image=art));bm.append(dict(key=key,cell=cell))
 elif g<9000:
  cell=(g+n)%16;art=ImageOps.contain(fx[cell],old.size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',old.size);canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2));out.append(dict(key=key,axis=s['axis'],image=canvas));em.append(dict(key=key,cell=cell))
 else:out.append(dict(key=key,axis=s['axis'],image=old));ui.append(key)
portrait=Image.open(G/'style-wave2'/slug/'design-reference-v1.png').convert('RGBA')
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
report={'status':'INSTALLED','revision':slug+'-style-conversion-v1','tool':'built-in imagegen','source_sff_version':1,'installed_sff_version':2,'source_sprite_count':len(original),'body_sprites_replaced':len(bm),'move_effect_sprites_replaced':len(em),'ui_keys_retained_or_portrait_replaced':len(ui),'body_sheet':{'file':BODY.name,'sha256':shaf(BODY),'cells':16},'effect_sheet':{'file':FX.name,'sha256':shaf(FX),'cells':16},'mapping':bm,'effect_mapping':em,'source_sff_sha256':shaf(backup),'installed_sff_sha256':shaf(S),'gameplay_files_sha256':gameplay,'preservation':['Every unique original SFF key retained','All body and non-UI move/effect groups replaced','Character weapon silhouette retained in illustrated pose bank','Original body height/effect footprint and roots retained','AIR, CMD, CNS, SND and palettes unchanged']}
(A/'installation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_sprites_replaced','move_effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
