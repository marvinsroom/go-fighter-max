"""Retain native evidence after a proved, non-colliding filament-origin edit."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/pyowol';V=S/'validation'
old=json.loads((V/'before-hand-v6.json').read_text());new=json.loads((S/'runtime-validation.json').read_text())
assert old['status']==new['status']=='Complete' and old['failed']==new['failed']==0
for name,digest in old['runtime_sha256'].items():
    if name!='pyowol.cns':assert new['runtime_sha256'][name]==digest,name
before=(V/'before-hand-v6.cns').read_text().splitlines();after=(S/'pyowol.cns').read_text().splitlines()
assert len(before)==len(after);changed=[]
for a,b in zip(before,after):
    if a==b:continue
    assert a.startswith(('fvar(2)=','fvar(3)=')) and b[:8]==a[:8]
    na=re.findall(r'-?\d+(?:\.\d+)?',a);nb=re.findall(r'-?\d+(?:\.\d+)?',b)
    assert len(na)==len(nb)
    assert re.sub(r'-?\d+(?:\.\d+)?','#',a)==re.sub(r'-?\d+(?:\.\d+)?','#',b)
    edits=[(float(x),float(y)) for x,y in zip(na,nb) if x!=y]
    assert edits and all(pair in ((25.,58.),(-175.,-160.)) for pair in edits),edits
    changed.append(a[:7])
assert changed.count('fvar(2)')==changed.count('fvar(3)')==3
replaced={'Thread Reel','Soul-Reaping Thread','Normal to thread cancel'}
assert {c['name'] for c in new['checks']}==replaced
merged=dict(old,runtime_sha256=new['runtime_sha256'])
merged['checks']=[next((n for n in new['checks'] if n['name']==c['name']),c) for c in old['checks']]
merged['frames']=[dict(f,capture_directory=f.get('capture_directory',old['capture_directory'])) for f in old['frames'] if f['case_name'] not in replaced]+[dict(f,capture_directory=new['capture_directory']) for f in new['frames']]
merged['passed']=sum(c['passed'] for c in merged['checks']);merged['failed']=sum(not c['passed'] for c in merged['checks'])
merged['compatibility']={'reason':'Only six helper fvar expressions change the relaxed-hand origin from (25,-175) to (58,-160). Helpers have no collision boxes or HitDefs. All other runtime files are byte-identical; all three recorded cases that reach this hand pose while tethered are recaptured.','baseline':'validation/before-hand-v6.json','retakes':'validation/hand-retakes-v6.json'}
(V/'hand-retakes-v6.json').write_text(json.dumps(new,indent=2));(S/'runtime-validation.json').write_text(json.dumps(merged,indent=2))
print('HAND_REGISTRATION_MERGED',merged['passed'],'cases; six coordinate-only expression edits; three visual retakes')
