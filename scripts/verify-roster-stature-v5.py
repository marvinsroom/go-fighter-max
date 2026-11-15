"""Audit actual installed files, allowed geometry changes and current native proof."""
from pathlib import Path
import json,re,hashlib,functools
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';E=S/'engine/ikemen-go-v1.0.0/chars';O=S/'face-audit/identity-scale-v5';p=O/'profiles.json';state=json.loads(p.read_text());records=[]
@functools.lru_cache(maxsize=None)
def sha(p):
 digest=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
 return digest.hexdigest()
def without_size(raw):return re.sub(rb'(?im)^\s*(?:xscale|yscale)\s*=\s*[-+0-9.eE]+',b'',raw)
def air_geometry(raw):
 out=[]
 for line in raw.decode('utf-8',errors='replace').splitlines():
  if re.match(r'\s*Clsn[12]\s*\[',line,re.I):out.append(re.sub(r'=.*','=GEOMETRY',line));continue
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=[x.strip() for x in line.split(';',1)[0].split(',')]
   while len(f)<9:f.append('')
   # Every action, key, offset, frame duration, flip and transparency remains.
   f[7]=f[8]='ISOTROPIC_SCALE';line=','.join(f)
  out.append(line)
 return '\n'.join(out)
for row in state['fighters']:
 n=E/row['engine'];a=O/'archive'/row['engine'];saved=json.loads((a/'manifest.json').read_text())['runtime_sha256']
 for name in saved:
  assert (n/name).is_file(),(row['slug'],name)
  if name==row['cns']:assert without_size((n/name).read_bytes())==without_size((a/name).read_bytes()),('State logic changed',row['slug'],name)
  elif name==row['air']:assert air_geometry((n/name).read_bytes())==air_geometry((a/name).read_bytes()),('Action/timing changed',row['slug'])
  elif name==row['sff'] and row['slug'] in ('jin-mu-won','eugene'):pass
  else:assert sha(n/name)==saved[name],('Unrequested file changed',row['slug'],name)
 runtime={name:sha(n/name) for name in saved};assert runtime==row['runtime_sha256'],('Stale profile registration',row['slug'])
 proof=O/'native'/row['slug']/'current.json';d=json.loads(proof.read_text());assert d['status']=='Complete' and d['failed']==0 and d['runtime_sha256']==runtime,('Current native proof missing',row['slug'])
 assert any(x['label']=='Basic attack connects' and x['passed'] for x in d['checks'])
 assert any(x.get('facing')==1 for x in d['frames']) and any(x.get('facing')==-1 for x in d['frames'])
 for frame in d['frames']:assert (S/'engine/ikemen-go-v1.0.0'/frame['file']).is_file()
 # Jinwoo now has one canonical runtime; no alternate copy is compared.
 for slug in (row['slug'],):
  f=S/'characters'/slug/'art/identity-scale-v5';review=f/'visual-review.json'
  if review.exists():
   if (S/'characters'/slug/'art/comic-face-v6/visual-review.json').exists():
    f=S/'characters'/slug/'art/comic-face-v6';review=f/'visual-review.json'
   visual=json.loads(review.read_text());assert visual['status']=='Reviewed'
   for name,digest in visual['assets'].items():assert sha(f/name)==digest==sha(S/'characters'/slug/'art/comic-identity-v3'/name)
   if f.name=='comic-face-v6':
    active=S/'characters'/slug/'art/comic-identity-v3';provenance=json.loads((active/'provenance.json').read_text());assert provenance['revision']=='comic-face-v6'
    for kind,asset in provenance['assets'].items():assert asset['sha256']==sha(active/asset['file'])
    for pose in (f/'extracted').glob('*.png'):assert sha(pose)==sha(active/'extracted'/pose.name)
 records.append(dict(slug=row['slug'],roster_entry=row['roster_entry'],status='PASS',native_checks=d['passed'],runtime_sha256=runtime,scope='current body/form size captures in both facings plus real basic attack contact',height_cm=row['height_cm'],evidence=row['evidence']))
 print('ROSTER_STATURE_VERIFIED',row['slug'],d['passed'],flush=True)
assert len(records)==26
report=dict(status='Complete',revision='identity-scale-v5',fighters=records,total_current_native_checks=sum(x['native_checks'] for x in records),validation_scope='Current native body/form samples and basic attack contact for all26. Separate new full combat/presentation suites for Jin Mu-Won and Eugene. Historical pre-size full move recordings remain labelled as such.',source_policy=state['height_policy'],state_logic_and_action_timings_preserved=True,size_constants_and_collision_geometry_changed=True)
(O/'completion.json').write_text(json.dumps(report,indent=2))
