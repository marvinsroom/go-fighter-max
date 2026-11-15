"""Install illustrated Guts body, Dragonslayer attacks, cannon, and VFX."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent))
from isolated_sprite_atlas import extract
from mugen_sff import Sff
from edward_assets import write_v2
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';A=G/'style-expansion/guts/conversion-v1';L=G/'engine/ikemen-go-v1.0.0/chars/guts';S=L/'Guts.sff';B=A/'before';BODY=A/'body-v1.png';FX=A/'effects-v1.png'
GAMEPLAY=['Guts.air','Guts.cmd','Guts.snd','Constants.cns','States/System.cns','States/Normal.cns','States/Specials.cns','States/Supers.cns','States/Helpers.cns','States/Customs.cns','config.txt']
def shab(v):return hashlib.sha256(v).hexdigest()
def shaf(p):return shab(p.read_bytes())
body=[im for im,_ in extract(BODY,4,4)]
def grid(path):
 im=Image.open(path).convert('RGBA');out=[]
 for y in range(4):
  for x in range(4):
   c=im.crop((round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4)));box=c.getchannel('A').getbbox();assert box;out.append(c.crop(box))
 return out
fx=grid(FX);assert len(body)==len(fx)==16
arc=Sff(S);original=[dict(key=k,axis=arc.headers[n][4:6],image=arc.decode(n)) for k,n in arc.keys.items()]
before_gameplay={name:shaf(L/name) for name in GAMEPLAY if (L/name).exists()}
counts={};out=[];bm=[];em=[];ui=[]
for sprite in original:
 key=tuple(sprite['key']);g=key[0];old=sprite['image'].convert('RGBA');n=counts.get(g,0);counts[g]=n+1
 if g<6000:
  cell=n%16;art=body[cell].copy();h=max(1,old.height);art=art.resize((max(1,round(art.width*h/art.height)),h),Image.Resampling.LANCZOS);axis=(round(sprite['axis'][0]/max(1,old.width)*art.width),sprite['axis'][1]);out.append(dict(key=key,axis=axis,image=art));bm.append(dict(key=key,cell=cell))
 elif g==9000:
  out.append(dict(key=key,axis=sprite['axis'],image=old));ui.append(key)
 else:
  cell=(g+n)%16;art=ImageOps.contain(fx[cell],old.size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',old.size);canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2));out.append(dict(key=key,axis=sprite['axis'],image=canvas));em.append(dict(key=key,cell=cell))
portrait=Image.open(G/'characters/guts/import-portrait.png').convert('RGBA')
for sprite in out:
 if sprite['key'][0]==9000:
  canvas=Image.new('RGBA',sprite['image'].size);fit=ImageOps.contain(portrait,canvas.size,Image.Resampling.LANCZOS);canvas.alpha_composite(fit,((canvas.width-fit.width)//2,(canvas.height-fit.height)//2));sprite['image']=canvas
B.mkdir(parents=True,exist_ok=True);backup=B/S.name
if not backup.exists():shutil.copy2(S,backup)
source_sha=shaf(backup);pending=S.with_suffix('.sff.pending');write_v2(pending,out);proof=Sff(pending);assert set(proof.keys)=={tuple(s['key']) for s in original}
for sprite in out:
 decoded=proof.decode(proof.keys[tuple(sprite['key'])]);assert decoded.size==sprite['image'].size and shab(decoded.tobytes())==shab(sprite['image'].tobytes())
pending.replace(S);after_gameplay={name:shaf(L/name) for name in before_gameplay};assert after_gameplay==before_gameplay
report={'status':'INSTALLED','revision':'guts-style-conversion-v1','tool':'built-in imagegen','source_sff_version':2,'installed_sff_version':2,'source_sprite_count':len(original),'body_sprites_replaced':len(bm),'move_effect_sprites_replaced':len(em),'ui_keys_retained_or_portrait_replaced':len(ui),'body_sheet':{'file':BODY.name,'sha256':shaf(BODY),'cells':16},'effect_sheet':{'file':FX.name,'sha256':shaf(FX),'cells':16},'mapping':bm,'effect_mapping':em,'source_sff_sha256':source_sha,'installed_sff_sha256':shaf(S),'gameplay_files_before_and_after_sha256':after_gameplay,'preservation':['Every unique original SFF key retained','All body and non-portrait move/effect groups replaced','Greatsword and mechanical cannon represented in illustrated pose bank','Original body height/effect footprint and roots retained','AIR, CMD, CNS, SND and config files unchanged']}
(A/'installation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_sprites_replaced','move_effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
