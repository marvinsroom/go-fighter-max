"""Record completed face edits against current native and browser proof."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';rows=[]
for slug in ['gang-ryong','cha-yeon-woo','kim-dokja','zhuo-fan']:
 f=S/'characters'/slug;b=json.loads((f/'build-report.json').read_text());r=json.loads((f/'runtime-validation.json').read_text());v=json.loads((f/'viewer-validation.json').read_text());ai=json.loads((f/'startup-ai-validation.json').read_text())
 assert r['status']=='Complete' and r['passed']==66 and not r['failed'] and r['runtime_sha256']==b['runtime_sha256']
 assert ai['passed'] and ai['runtime_sha256']==b['runtime_sha256']
 assert v['status']=='PASS' and v['review_sha256']==hashlib.sha256((f/'review.html').read_bytes()).hexdigest()
 old=f/'archive/before-manhwa-faces-v2/build-report.json';changed=[]
 if old.exists():
  previous=json.loads(old.read_text())['runtime_sha256'];changed=[k for k,h in b['runtime_sha256'].items() if h!=previous[k]]
  assert all(k.endswith(('.sff','.def')) for k in changed),'Unexpected gameplay change'
 rows.append(dict(slug=slug,name=b['name'],gameplay_checks=r['passed'],captures=len(r['frames']),browser_assertions=v['assertions'],clips=v['clips'],changed_runtime_files=changed,runtime_sha256=b['runtime_sha256']))
report=dict(status='Complete',date='2026-10-21',reviewed_fighters=14,updated_builds=rows,tool='built-in image_gen.imagegen',face_comparison='review.html',limitations=['Generated roster adaptations; comic references and visual decisions are provided for review.','No verified downloadable Zhuo Fan MUGEN release was found; his gameplay is a custom adaptation.'])
(S/'face-audit/completion.json').write_text(json.dumps(report,indent=2));print('FACE_PASS_COMPLETE',len(rows),'builds',sum(r['gameplay_checks'] for r in rows),'native checks')
