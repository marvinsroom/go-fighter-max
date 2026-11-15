"""Retain unaffected captures only after proving the exact recovery-only edit."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/pyowol';C=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/pyowol';V=S/'validation'
old=json.loads((V/'before-recovery.json').read_text());new=json.loads((S/'runtime-validation.json').read_text())
assert old['status']==new['status']=='Complete' and new['failed']==0
before=(V/'before-recovery.air').read_text();after=(C/'pyowol.air').read_text()
def blocks(s):return {int(re.match(r'\[Begin Action (\d+)\]',b)[1]):b for b in re.split(r'(?=\[Begin Action )',s) if re.match(r'\[Begin Action (\d+)\]',b)}
ba,aa=blocks(before),blocks(after);changed=[k for k in ba if ba[k]!=aa[k]]
assert ba.keys()==aa.keys() and changed==[12],changed
assert ba[12].replace(',0,0,-1,',',0,0,6,')==aa[12]
for name,digest in old['runtime_sha256'].items():
    if name!='pyowol.air':assert digest==new['runtime_sha256'][name],name
replaced={c['name'] for c in new['checks']}
assert replaced=={'Low Fang','Ankle Thread','Rising Fang'}
for c in old['checks']:
    if c['name'] not in replaced:assert c['passed'] and not c['seen'].get('12'),c
merged=dict(old,runtime_sha256=new['runtime_sha256'],checks=[next((n for n in new['checks'] if n['name']==c['name']),c) for c in old['checks']])
merged['frames']=[dict(f,capture_directory=old['capture_directory']) for f in old['frames'] if f['case_name'] not in replaced]+[dict(f,capture_directory=new['capture_directory']) for f in new['frames']]
merged['passed']=sum(c['passed'] for c in merged['checks']);merged['failed']=sum(not c['passed'] for c in merged['checks'])
merged['compatibility']={'changed_actions':changed,'reason':'Crouch-to-stand duration changed from infinite to six ticks. Every other animation and all CNS, CMD, SFF, SND and DEF bytes are identical. Only the three crouching cases used action 12; all three were recaptured after the fix.','baseline':'validation/before-recovery.json','retakes':'validation/recovery-retakes.json'}
(V/'recovery-retakes.json').write_text(json.dumps(new,indent=2));(S/'runtime-validation.json').write_text(json.dumps(merged,indent=2));assert merged['failed']==0
print('PYOWOL_MERGED',merged['passed'],'passed; only action 12 changed')
