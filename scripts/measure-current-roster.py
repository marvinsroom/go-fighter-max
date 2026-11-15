"""Measure installed neutral sprites with actual AIR/CNS/localcoord scales."""
from pathlib import Path
import json,re,collections
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars';O=R/'.tmp/size-redesign';O.mkdir(exist_ok=True)
profiles={p['slug']:p for p in json.loads((R/'sprite-fighter/face-audit/identity-scale-v5/profiles.json').read_text())['fighters']}
rows=json.loads((R/'sprite-fighter/jus-upgrade/manifest.json').read_text())['fighters'];data=[]
for row in rows:
 p=profiles.get(row['slug']);n=E/row['engine'];d=(n/row['definition']).read_text(encoding='cp1252',errors='replace');files={k.lower():v.strip().strip('"') for k,v in re.findall(r'(?im)^\s*(cns|sprite|anim)\s*=\s*([^;\r\n]+)',d)}
 c=(n/files['cns']).read_text(encoding='cp1252',errors='replace');c=re.search(r'(?ims)^\s*\[Size\](.*?)(?=^\s*\[|\Z)',c)[1];sx=float(re.search(r'(?im)^\s*xscale\s*=\s*([-\d.]+)',c)[1]);sy=float(re.search(r'(?im)^\s*yscale\s*=\s*([-\d.]+)',c)[1]);width=float(re.search(r'(?im)^\s*localcoord\s*=\s*([\d.]+)',d)[1]);key=tuple(p['neutral_key']) if p else (0,0)
 sf=n/files['sprite']
 with sf.open('rb') as stream:version=stream.read(16)[15]
 if version==1:
  from edward_assets import read_v1
  s=next(s for s in read_v1(sf) if s['key']==key);im=s['image'];axis=s['axis']
 else:
  s=Sff(sf);i=s.keys[key];im=s.decode(i);axis=s.headers[i][4:6]
 a=(n/files['anim']).read_text(encoding='cp1252',errors='replace');scales=[]
 for line in a.splitlines():
  if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
  f=[x.strip() for x in line.split(';')[0].split(',')]
  if tuple(map(int,f[:2]))==key:scales.append((float(f[7]) if len(f)>7 and f[7] else 1,float(f[8]) if len(f)>8 and f[8] else 1))
 scale=collections.Counter(scales).most_common(1)[0][0];b=im.getbbox();h=(b[3]-b[1])*scale[1]*sy*320/width
 im.save(O/(row['slug']+'.png'));result=dict(slug=row['slug'],cm=row['height_cm'],world_height=round(h,2),target=row['target_world_height'],key=key,air_scale=scale,cns_scale=[sx,sy],width=width,bounds=b,axis=axis,file=str((O/(row['slug']+'.png')).relative_to(R)),files=files);data.append(result)
 print(row['slug'],round(h,2),'target',round(row['target_world_height'],2),'AIR',scale,'CNS',sx,sy,'coord',width,flush=True)
(O/'measurements.json').write_text(json.dumps(data,indent=2))
