"""Install only separately inspected v5 likeness corrections through the native packer."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1]
for slug in sys.argv[1:]:
 f=R/'sprite-fighter/characters'/slug;a=f/'art/identity-scale-v5'
 if (f/'art/comic-face-v6/visual-review.json').exists():a=f/'art/comic-face-v6'
 active=f/'art/comic-identity-v3';review=json.loads((a/'visual-review.json').read_text());assert review['status']=='Reviewed'
 for kind in ('movement','combat','story','portrait'):
  p=a/(kind+'.png');assert review['assets'][p.name]==hashlib.sha256(p.read_bytes()).hexdigest()
  assert json.loads(p.with_suffix('.generation.json').read_text())['layout_validation']['status']=='PASS'
  for suffix in ('.png','.prompt.txt','.generation.json'):shutil.copy2(p.with_suffix(suffix),active/(kind+suffix))
 subprocess.run([sys.executable,str(R/'scripts/publish-comic-shared-v3.py'),slug],cwd=R,check=True)
 report=f/'build-report.json';d=json.loads(report.read_text());d['visual_revision']=a.name;d['visual_review']=str((a/'visual-review.json').relative_to(R));report.write_text(json.dumps(d,indent=2))
 subprocess.run([sys.executable,str(R/'scripts/publish-current-likeness-metadata.py'),slug],cwd=R,check=True)
 print('LIKENESS_INSTALLED',slug,a.name,flush=True)
