"""Replace Cid's drawings in place, preserving his installed gameplay files."""
from pathlib import Path
import json,re,statistics,io,hashlib,shutil
import numpy as np
from PIL import Image,ImageOps
from mugen_sff import Sff
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1];C=R/'sprite-fighter/characters/cid';A=C/'art/redesign-v7';N=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/cid_shadow';B=A/'before';B.mkdir(exist_ok=True)
for name in ['Cid.sff','Cid.air','Cid.cns','cid_shadow.def']:
 if not (B/name).exists():shutil.copy2(N/name,B/name)
def sha(data):return hashlib.sha256(data).hexdigest()
art={};reports={}
for name in ['movement-a','movement-b','combat','cinematic','taunt']:
 frames=extract(A/(name+'.png'),4,2 if name=='taunt' else 3);sheet=Image.open(A/(name+'.png'));cell=sheet.width/4
 reference={'movement-a':[0,1,2,3],'movement-b':[0,1],'combat':[5],'cinematic':[4,5,6,7,8],'taunt':[0,1]}[name]
 reference_height=statistics.median(frames[i][0].height for i in reference)
 root=[]
 for i in reference:
  im,b=frames[i];pixels=np.asarray(im)[:,:,3]>128;yy,xx=np.where(pixels);feet=xx[yy>im.height*.83]
  root.append(b[0]-(i%4)*cell+float(np.median(feet)))
 anchor=statistics.median(root);records=[]
 for i,(im,b) in enumerate(frames):
  scale=55/reference_height
  if name=='movement-a' and i>=4:scale=55/statistics.median(f[0].height for f in frames[4:])
  axis=(round((i%4)*cell+anchor-b[0]),im.height)
  buffer=io.BytesIO();im.save(buffer,format='PNG');key=f'{name}:{i}'
  art[key]=dict(image=im,png=buffer.getvalue(),axis=axis,scale=scale,rgba_sha256=sha(im.tobytes()))
  dest=A/'extracted'/name;dest.mkdir(parents=True,exist_ok=True);im.save(dest/f'{i:02d}.png')
  records.append(dict(pose=key,axis=axis,scale=scale,bounds=b,size=im.size,rgba_sha256=art[key]['rgba_sha256']))
 reports[name]=dict(frames=records,source_sha256=sha((A/(name+'.png')).read_bytes()),method='Fixed scale per complete pose sequence; fixed horizontal root from standing references; no per-frame height fitting')
old=json.loads((C/'illustrated-build-report.json').read_text())['replaced_sprite_keys']
original=Sff(B/'Cid.sff');replacements={};scales={}
for identity,meta in old.items():
 key=tuple(map(int,identity.split(',')))
 if key[0]==9000:continue
 pose=meta['pose']
 if pose not in art:continue
 replacements[key]=art[pose];scales[key]=art[pose]['scale']
for i in range(8):replacements[(7900,i)]=art[f'taunt:{i}'];scales[(7900,i)]=art[f'taunt:{i}']['scale']
portrait=Image.open(A/'portrait.png').convert('RGBA')
for key in [(9000,0),(9000,1)]:
 header=original.headers[original.keys[key]];im=Image.new('RGBA',header[2:4]);fit=ImageOps.contain(portrait,header[2:4],Image.Resampling.LANCZOS);im.alpha_composite(fit,((im.width-fit.width)//2,0));buffer=io.BytesIO();im.save(buffer,format='PNG')
 replacements[key]=dict(image=im,png=buffer.getvalue(),axis=header[4:6],rgba_sha256=sha(im.tobytes()))
derived=original.derive(replacements,{})
pending=N/'Cid.sff.pending';pending.write_bytes(derived);pending.replace(N/'Cid.sff')
fresh=Sff(N/'Cid.sff')
for key,frame in replacements.items():assert sha(fresh.decode(fresh.keys[key]).tobytes())==frame['rgba_sha256'],key
air=(B/'Cid.air').read_bytes();changed=0
def patch(match):
 global changed
 line=match[0];fields=line.split(b';')[0].split(b',');key=tuple(int(f.strip()) for f in fields[:2])
 if key not in scales:return line
 while len(fields)<9:fields.append(b'')
 for index in [7,8]:
  if not fields[index].strip() or float(fields[index])!=0:fields[index]=format(scales[key],'.10f').encode()
 tail=b';'+line.split(b';',1)[1] if b';' in line else b'';changed+=1
 return b','.join(fields)+tail
air=re.sub(rb'(?m)^[ \t]*\d+[ \t]*,[ \t]*\d+[ \t]*,[^\r\n]*',patch,air)
(N/'Cid.air').write_bytes(air)
assert (N/'Cid.cns').read_bytes()==(B/'Cid.cns').read_bytes()
report=dict(status='Installed; size calibration next; recordings deferred',sheets=reports,drawings=56,replaced_headers=len(replacements),rewritten_air_rows=changed,original_sff_sha256=sha(original.data),installed_sff_sha256=sha(derived),installed_air_sha256=sha(air),preserved='Move controls, CNS state logic, damage, voices, frame durations, AIR action IDs and collision geometry; supporting characters and effects retained.',tool='built-in imagegen',prompts='requests.json',reference='official-references.json')
(A/'installation.json').write_text(json.dumps(report,indent=2));print('CID_REDESIGN_INSTALLED',len(replacements),'sprite keys;',changed,'AIR rows; 56 drawings and new portrait; gameplay preserved')
