"""Keep current accepted faces, runtime and evidence before comic-face replacement."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';O=S/'face-audit/identity-scale-v5';archive=O/'archive/before-comic-face-v6';archive.mkdir(exist_ok=True)
for name in ('profiles.json','completion.json','native-validation.json','browser-validation.json','review.html','roster-lineup.jpg'):
 target=archive/name
 if not target.exists():shutil.copy2(O/name,target)
if not (archive/'global-completion.json').exists():shutil.copy2(O.parent/'completion.json',archive/'global-completion.json')
state=json.loads((O/'profiles.json').read_text())
for slug in ('jin-mu-won','eugene'):
 f=S/'characters'/slug;out=f/'archive/before-comic-face-v6';out.mkdir(exist_ok=True);row=next(x for x in state['fighters'] if x['slug']==slug)
 for name in ('review.html','build-report.json','runtime-validation.json','viewer-validation.json','comic-viewer-validation.json','review-data.js'):
  if (f/name).exists() and not (out/name).exists():shutil.copy2(f/name,out/name)
 runtime=out/'runtime';runtime.mkdir(exist_ok=True)
 for name in row['runtime_sha256']:
  if not (runtime/name).exists():shutil.copy2(S/'engine/ikemen-go-v1.0.0/chars'/row['engine']/name,runtime/name)
 if not (out/'stature-native.json').exists():shutil.copy2(O/'native'/slug/'current.json',out/'stature-native.json')
(O.parent/'completion.json').write_text(json.dumps(dict(status='In progress',revision='comic-face-v6',scope='Original comic faces for both Jin Mu-Won and older silver-haired Eugene; existing all-roster stature retained',report='identity-scale-v5/completion.json',review='identity-scale-v5/review.html'),indent=2))
with (R/'PROJECT_MEMORY.md').open('ab') as stream:stream.write(b'\n\n## Comic face v6 IN PROGRESS (2026-10-21)\nUser explicitly requested COMIC FACE for BOTH Jin Mu-Won and Eugene, confirming async question. Correct faces against original published panels, across portraits and all body sheets, retaining v5 all-roster stature. New art staged at art/comic-face-v6; exact requests .tmp/comic-face-v6-requests.json. Previous accepted runtime/review proofs backed up by prepare-comic-face-v6.py. Current global completion marked In progress until installation and current proofs finish.\n')
print('COMIC_FACE_V6_BACKED_UP')
