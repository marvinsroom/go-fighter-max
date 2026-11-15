"""Retain captures only after proving a sole mirrored-composition correction."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/pyowol';V=S/'validation'
old=json.loads((V/'before-framing-v5.json').read_text());new=json.loads((S/'runtime-validation.json').read_text())
assert old['status']==new['status']=='Complete' and old['failed']==new['failed']==0
needle='type=PosSet\ntrigger1=time=0\nx=-120\ny=0'
before=(V/'before-framing-v5.cns').read_text();after=(S/'pyowol.cns').read_text()
assert before.count(needle)==1
assert before.replace(needle,needle.replace('x=-120','x=-120*facing'))==after
for name,digest in old['runtime_sha256'].items():
    if name!='pyowol.cns':assert new['runtime_sha256'][name]==digest,name
assert [c['name'] for c in new['checks']]==['Ultimate facing left']
assert all(f['case_name']=='Ultimate facing left' for f in new['frames'])
for f in old['frames']:
    if f['case_name']!='Ultimate facing left':assert f['facing']==1 or f['case_name']=='Reaper of the Drifting Moon'
merged=dict(old,runtime_sha256=new['runtime_sha256'])
merged['checks']=[new['checks'][0] if c['name']=='Ultimate facing left' else c for c in old['checks']]
merged['frames']=[dict(f,capture_directory=f.get('capture_directory',old['capture_directory'])) for f in old['frames'] if f['case_name']!='Ultimate facing left']+[dict(f,capture_directory=new['capture_directory']) for f in new['frames']]
merged['compatibility']={'reason':'Only the ultimate initial X is mirrored by facing: -120 becomes -120*facing. At facing=1 all earlier values remain identical. The only case starting facing=-1 is fully recaptured. All other runtime bytes match.', 'baseline':'validation/before-framing-v5.json','retake':'validation/framing-retake-v5.json'}
merged['passed']=sum(c['passed'] for c in merged['checks']);merged['failed']=sum(not c['passed'] for c in merged['checks'])
(V/'framing-retake-v5.json').write_text(json.dumps(new,indent=2));(S/'runtime-validation.json').write_text(json.dumps(merged,indent=2))
print('FRAMING_MERGED',merged['passed'],'checks; sole left-facing retake; other runtime files identical')
