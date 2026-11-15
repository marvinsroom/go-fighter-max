"""Promote reviewed v4 bodies through existing native packers, preserving gameplay."""
from comic_identity_v3 import *
from manhwa_fighters import PROFILES
import json,sys,shutil,hashlib,subprocess

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
requests=json.loads((R/'.tmp/comic-style-v4-requests.json').read_text())
for slug in sys.argv[1:]:
 f=C/slug;new=f/'art/comic-style-v4';active=f/'art/comic-identity-v3'
 review=json.loads((new/'visual-review.json').read_text())
 assert review['status']=='Reviewed candidate',('Missing visual review',slug)
 rows=[q for q in requests if q['slug']==slug]
 archive=f/'archive/before-comic-style-v4';saved=json.loads((archive/'manifest.json').read_text())
 for q in rows:
  p=Path(q['destination']);meta=json.loads(p.with_suffix('.generation.json').read_text())
  assert meta['layout_validation']['status']=='PASS'
  assert review['assets'][p.name]==sha(p),('Stale visual review',p)
 for q in rows:
  p=Path(q['destination'])
  for suffix in ('.png','.prompt.txt','.generation.json'):
   src=p.with_suffix(suffix);shutil.copy2(src,active/src.name)
 script='publish-comic-shared-v3.py' if slug in PROFILES else 'apply-comic-legacy-v3.py'
 args=[sys.executable,str(R/'scripts'/script),slug]+([] if slug in PROFILES else ['--refresh'])
 subprocess.run(args,cwd=R,check=True)
 native=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars'/saved['native_id']
 for p in (archive/'runtime').iterdir():
  if p.suffix in ('.cns','.cmd','.air','.snd','.zss'):assert sha(p)==sha(native/p.name),('Gameplay changed',slug,p.name)
 if slug not in PROFILES:subprocess.run([sys.executable,str(R/'scripts/record-comic-legacy-v3.py'),slug],cwd=R,check=True)
 report=f/'build-report.json'
 if report.exists():
  data=json.loads(report.read_text());data['visual_revision']='comic-style-v4';data['visual_review']=str((new/'visual-review.json').relative_to(R));report.write_text(json.dumps(data,indent=2))
 installed=dict(status='Installed; native and browser checks pending',revision='comic-style-v4',slug=slug,body_assets=review['assets'],portrait_preserved=True,gameplay_unchanged=True,native_id=saved['native_id'],runtime_sha256={p.name:sha(p) for p in native.iterdir() if p.suffix in ('.sff','.cns','.cmd','.air','.snd','.zss')})
 (new/'installed.json').write_text(json.dumps(installed,indent=2))
 progress=REF/'style-v4-progress.json';state=json.loads(progress.read_text());state['fighters'][slug]['status']=installed['status'];progress.write_text(json.dumps(state,indent=2))
 print('V4_INSTALLED',slug,flush=True)
