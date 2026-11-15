"""Install illustrated Itachi body, ninjutsu, crow/genjutsu and Susanoo banks."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent))
from edward_assets import read_v1,write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';A=G/'style-wave2/itachi/conversion-v1';L=G/'engine/ikemen-go-v1.0.0/chars/itachi'
I=json.loads((G/'style-wave2/itachi/inventory.json').read_text());S=L/I['files']['sprite'];B=A/'before'
BODY={'movement':A/'body-movement-00-v1.png','attacks':A/'body-attacks-01-v1.png','specials':A/'body-specials-02-v1.png','reactions':A/'body-reactions-03-v1.png'}
EFFECT={'fire':A/'effect-fire-00-v1.png','crows-genjutsu':A/'effect-crows-genjutsu-01-v1.png','susanoo':A/'effect-susanoo-02-v1.png'}
def shab(v):return hashlib.sha256(v).hexdigest()
def shaf(p):return shab(p.read_bytes())
def bodybank(g):return 'movement' if g<200 else 'attacks' if g<1000 else 'specials' if g<5000 else 'reactions'
def effectbank(g):
 if g<6600:return 'fire'
 if g<7000:return 'susanoo'
 if g<7500:return 'crows-genjutsu'
 return 'susanoo'
def grid(path):
 im=Image.open(path).convert('RGBA');out=[]
 for y in range(4):
  for x in range(4):
   c=im.crop((round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4)));box=c.getchannel('A').getbbox();assert box,(path,x,y);out.append(c.crop(box))
 return out
body={k:[im for im,_ in extract(p,4,4)] for k,p in BODY.items()};effects={k:grid(p) for k,p in EFFECT.items()};assert all(len(v)==16 for v in [*body.values(),*effects.values()])
raw=S.read_bytes();version=raw[15]
if version==1:original=read_v1(S)
else:
 arc=Sff(S);original=[dict(key=k,axis=arc.headers[n][4:6],image=arc.decode(n)) for k,n in arc.keys.items()]
# MUGEN archives may contain duplicate headers for one (group, number). The
# writer and engine resolve the first occurrence; preserve that exact rule.
seen=set();original=[s for s in original if not (tuple(s['key']) in seen or seen.add(tuple(s['key'])))]
counts={};bm=[];em=[];output=[]
for s in original:
 key=tuple(s['key']);g=key[0];old=s['image'].convert('RGBA');n=counts.get(g,0);counts[g]=n+1
 if g<6000:
  name=bodybank(g);art=body[name][n%16].copy();h=max(1,old.height);art=art.resize((max(1,round(art.width*h/art.height)),h),Image.Resampling.LANCZOS);axis=(round(s['axis'][0]/max(1,old.width)*art.width),s['axis'][1]);output.append(dict(key=key,axis=axis,image=art));bm.append(dict(key=key,bank=name,cell=n%16))
 elif g<9000:
  name=effectbank(g);art=ImageOps.contain(effects[name][n%16],old.size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',old.size);canvas.alpha_composite(art,((old.width-art.width)//2,(old.height-art.height)//2));output.append(dict(key=key,axis=s['axis'],image=canvas));em.append(dict(key=key,bank=name,cell=n%16))
 else:output.append(dict(key=key,axis=s['axis'],image=old))
portrait=Image.open(G/'style-wave2/itachi/design-reference-v1.png').convert('RGBA')
for s in output:
 if s['key'][0]==9000:
  c=Image.new('RGBA',s['image'].size);f=ImageOps.contain(portrait,c.size,Image.Resampling.LANCZOS);c.alpha_composite(f,((c.width-f.width)//2,0));s['image']=c
B.mkdir(parents=True,exist_ok=True);backup=B/S.name
if not backup.exists():shutil.copy2(S,backup)
assert shaf(backup)==I['source_sha256']['sprite']
pending=S.with_suffix('.sff.pending');write_v2(pending,output);proof=Sff(pending);assert set(proof.keys)=={tuple(s['key']) for s in original}
for s in output:
 d=proof.decode(proof.keys[tuple(s['key'])]);assert d.size==s['image'].size and shab(d.tobytes())==shab(s['image'].tobytes())
pending.replace(S)
gameplay={}
for kind,name in I['files'].items():
 p=L/name
 if p.exists() and kind!='sprite':gameplay[name]=shaf(p)
for kind in ('anim','cmd','sound'):assert gameplay[I['files'][kind]]==I['source_sha256'][kind]
report={'status':'INSTALLED','revision':'itachi-style-conversion-v1','tool':'built-in imagegen','source_sff_version':version,'installed_sff_version':2,'source_sprite_count':len(original),'body_sprites_replaced':len(bm),'effect_sprites_replaced':len(em),'ui_keys_retained_or_portrait_replaced':len(original)-len(bm)-len(em),'body_sheets':{k:{'file':p.name,'sha256':shaf(p),'cells':16} for k,p in BODY.items()},'effect_sheets':{k:{'file':p.name,'sha256':shaf(p),'cells':16} for k,p in EFFECT.items()},'mapping':bm,'effect_mapping':em,'source_sff_sha256':shaf(backup),'installed_sff_sha256':shaf(S),'gameplay_files_sha256':gameplay,'preservation':['Every unique original SFF key retained','All body and gameplay effect groups replaced','Fire, crow/genjutsu and Susanoo banks remain distinct','AIR, CMD, CNS, SND and palettes unchanged','Original body height/effect footprint and roots retained']}
(A/'installation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','source_sprite_count','body_sprites_replaced','effect_sprites_replaced','ui_keys_retained_or_portrait_replaced','installed_sff_sha256')},indent=2))
