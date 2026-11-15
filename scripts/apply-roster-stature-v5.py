"""Apply a single calibrated native scale per body, with explicit form differences.

The only production CNS edits are Size.xscale/yscale. Form-specific changes
are isotropic AIR body scales and their collision boxes; action timings and
state controllers remain intact. Every edit is derived from an immutable backup.
"""
from pathlib import Path
import json,re,hashlib,sys
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars';O=R/'sprite-fighter/face-audit/identity-scale-v5';p=O/'profiles.json';data=json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scale_values(raw,values):
 for key,value in values.items():
  pattern=rb'(?im)^(\s*'+key.encode()+rb'\s*=\s*)[-+0-9.eE]+'
  raw,count=re.subn(pattern,lambda m:m[1]+format(value,'.10g').encode(),raw,count=1);assert count==1,key
 return raw
def form_factor(row,key):
 g,n=key;slug=row['slug']
 if slug=='baam':
  if g in (62100,62500) or g==62600 and n>=8:return 180/168
  if g==62300:return (168+(180-168)*min(n,7)/7)/168
 return row.get('form_factors',{}).get(str(g),1)
for row in data['fighters']:
 if len(sys.argv)>1 and row['slug'] not in sys.argv[1:]:continue
 n=E/row['engine'];backup=O/'archive'/row['engine'];cns=backup/row['cns'];raw=cns.read_bytes();text=raw.decode('utf-8',errors='replace');oldx=float(re.search(r'(?im)^\s*xscale\s*=\s*([\d.]+)',text)[1]);oldy=row['global_scale'];f=row['target_neutral_world_height']/row['current_neutral_world_height'];row['scale_multiplier']=f;row['native_scale']=[oldx*f,oldy*f]
 row['form_factors']={}
 # Explicit heights for different bodies; unknown transformations are visual estimates.
 form_targets={}
 if row['slug']=='gt-goku':form_targets={62004:175*.5*.94}
 if row['slug']=='rimuru':form_targets={8791:140*.5*.98,8790:40*.5,8793:40*.5}
 if row['slug']=='ichigo':
  form_targets={62000+i:181*.5*.96 for i in (1,4,6,7,8,9,10,11)};form_targets[62005]=200*.5*.96
 if row['slug']=='luffy':form_targets={62001:250*.5*.94,62002:230*.5*.94,62003:280*.5*.94,62004:174*.5*.94}
 air=(backup/row['air']).read_bytes();airtext=air.decode('utf-8',errors='replace');sprites=Sff(n/row['sff']);scales={}
 for line in airtext.splitlines():
  if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
  fields=[v.strip() for v in line.split(';',1)[0].split(',')];key=tuple(map(int,fields[:2]))
  if key not in scales:scales[key]=float(fields[8]) if len(fields)>8 and fields[8] else 1
 for group,target in form_targets.items():
  # Slime combat pose11 is its neutral, walk group is calibrated against it.
  key=(group,11 if group==8790 else 0)
  if group==8793:
   row['form_factors'][str(group)]=row['form_factors'].get('8790',1);continue
  if key not in sprites.keys:continue
  im=sprites.decode(sprites.keys[key]);b=im.getchannel('A').getbbox();world=(b[3]-b[1])*scales.get(key,row['air_scale'])*oldy*320/row['localcoord_width'];row['form_factors'][str(group)]=target/(world*f)
 row['form_height_notes']={'gt-goku':'Child120cm estimate; adult SS4 175cm reported.','rimuru':'Masked130cm and Demon Lord140cm secondary reports; slime40cm visual estimate.','ichigo':'Early174cm, later181cm; Vasto Lorde200cm silhouette including horns is a visual estimate.','luffy':'Official base174cm. Boundman250cm, Snakeman230cm, Nightmare280cm are explicit visual estimates, not published canon heights.'}.get(row['slug'],'Existing same-body form silhouettes retained.')
 changed=scale_values(raw,{'xscale':row['native_scale'][0],'yscale':row['native_scale'][1]});(n/row['cns']).write_bytes(changed)
 # Byte-level AIR processing preserves file encoding, line endings and timing.
 blocks=re.split(rb'(?=^\s*\[Begin Action )',air,flags=re.M|re.I);out=[];adjusted=0
 for block in blocks:
  factors=[];lines=block.splitlines(keepends=True)
  for line in lines:
   m=re.match(rb'^\s*(\d+)\s*,\s*(\d+)\s*,',line)
   if m:
    factor=form_factor(row,(int(m[1]),int(m[2])))
    g=int(m[1])
    if abs(factor-1)>1e-8 or 62000<=g<62700 or g in (8790,8791,8793):factors.append(factor)
  common=factors[0] if factors and max(factors)-min(factors)<1e-6 else 1
  for i,line in enumerate(lines):
   m=re.match(rb'^\s*(\d+)\s*,\s*(\d+)\s*,',line)
   if m:
    factor=form_factor(row,(int(m[1]),int(m[2])))
    if abs(factor-1)>1e-8:
     eol=b'\r\n' if line.endswith(b'\r\n') else b'\n' if line.endswith(b'\n') else b'';body=line.rstrip(b'\r\n');fields=body.split(b',')
     while len(fields)<9:fields.append(b'')
     for j in (7,8):fields[j]=format((float(fields[j]) if fields[j].strip() else 1)*factor,'.10g').encode()
     lines[i]=b','.join(fields)+eol;adjusted+=1
   elif common!=1 and re.match(rb'\s*Clsn[12]\s*\[',line,re.I):
    lhs,rhs=line.split(b'=',1);lines[i]=lhs+b'='+re.sub(rb'-?\d+(?:\.\d+)?',lambda m:str(round(float(m[0])*common)).encode(),rhs)
  out.append(b''.join(lines))
 (n/row['air']).write_bytes(b''.join(out));row['adjusted_form_frames']=adjusted
 # Jinwoo now has one canonical runtime; there is no candidate copy to sync.
 row['runtime_sha256']={name:sha(n/name) for name in json.loads((backup/'manifest.json').read_text())['runtime_sha256']}
 folder=R/'sprite-fighter/characters'/row['slug'];report=folder/'build-report.json';installed=folder/'art/comic-identity-v3/installed.json'
 for path in (report,installed):
  if not path.exists():continue
  d=json.loads(path.read_text())
  if 'runtime_sha256' in d:d['runtime_sha256']={name:sha(n/name) for name in d['runtime_sha256'] if (n/name).exists()}
  d['stature_revision']='identity-scale-v5';d['stature_profile']=str(p.relative_to(R));d['size_constants_changed']=True
  if 'unchanged_gameplay' in d:d['unchanged_gameplay']=False
  path.write_text(json.dumps(d,indent=2))
 print('STATURE_INSTALLED',row['slug'],row['height_cm'],format(f,'.4f'),adjusted,flush=True)
data['status']='Installed; native size inspection pending';p.write_text(json.dumps(data,indent=2))
