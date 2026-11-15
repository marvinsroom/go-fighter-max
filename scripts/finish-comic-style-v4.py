"""Record completion only after separate visual, installed-native and browser review."""
from comic_identity_v3 import *
import json,sys,hashlib,subprocess

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
statepath=REF/'style-v4-progress.json';state=json.loads(statepath.read_text())
for slug in sys.argv[1:]:
 f=C/slug;new=f/'art/comic-style-v4';active=f/'art/comic-identity-v3'
 review=json.loads((new/'visual-review.json').read_text());installed=json.loads((new/'installed.json').read_text())
 assert review['status']=='Reviewed candidate' and review.get('native_review',{}).get('status')=='Reviewed',('Separate visual/native review required',slug)
 assert all(sha(new/name)==digest==sha(active/name) for name,digest in review['assets'].items()),('Stale visual assets',slug)
 assert sha(active/'portrait.png')==sha(f/'archive/before-comic-style-v4/art/portrait.png'),('Portrait unexpectedly changed',slug)
 if (active/'runtime-templates.json').exists():
  p=REF/'form-review.json';forms=json.loads(p.read_text());row=next(v for v in forms['fighters'] if v['slug']==slug)
  row.update(status='Reviewed',assets=review['assets'],style_v4_review=str((new/'visual-review.json').relative_to(R)))
  forms['style_v4_method']='Current body hashes are registered only after full-sheet visual inspection, separate form checks and fresh native-size inspection recorded in each v4 visual-review.json. Gameplay checks do not establish likeness.'
  p.write_text(json.dumps(forms,indent=2))
 subprocess.run([sys.executable,str(R/'scripts/verify-comic-installation.py'),slug],cwd=R,check=True)
 proof=json.loads((active/'verification.json').read_text())
 installed.update(status='Complete',native_checks=proof['native_checks'],captures=proof['captures'],browser_assertions=proof['browser_assertions'],review_sha256=proof['review_sha256'],runtime_sha256=proof['runtime_sha256'])
 (new/'installed.json').write_text(json.dumps(installed,indent=2))
 state['fighters'][slug].update(status='Complete',native_checks=proof['native_checks'],captures=proof['captures'],browser_assertions=proof['browser_assertions'])
 statepath.write_text(json.dumps(state,indent=2));print('V4_COMPLETE',slug,flush=True)
if all(v['status']=='Complete' for v in state['fighters'].values()):
 state['status']='Complete';statepath.write_text(json.dumps(state,indent=2))
