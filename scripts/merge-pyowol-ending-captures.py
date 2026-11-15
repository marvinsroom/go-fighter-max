"""Merge two capture-only retakes, requiring byte-identical runtime hashes."""
from pathlib import Path
import json
S=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/pyowol';V=S/'validation'
old=json.loads((V/'before-ending-v6.json').read_text());new=json.loads((S/'runtime-validation.json').read_text())
assert old['status']==new['status']=='Complete' and old['failed']==new['failed']==0
assert old['runtime_sha256']==new['runtime_sha256']
replaced={'Light medium heavy chain','Ultimate facing left'}
assert {c['name'] for c in new['checks']}==replaced
assert replaced<={f['case_name'] for f in new['frames']}
merged=dict(old)
merged['checks']=[next((n for n in new['checks'] if n['name']==c['name']),c) for c in old['checks']]
merged['frames']=[dict(f,capture_directory=f.get('capture_directory',old['capture_directory'])) for f in old['frames'] if f['case_name'] not in replaced]+[dict(f,capture_directory=new['capture_directory']) for f in new['frames']]
merged['capture_retake']={'reason':'Full run exhausted the engine screenshot limit (000..998); final two showcases recaptured with byte-identical installed runtime.','evidence':'validation/ending-retakes-v6.json'}
(V/'ending-retakes-v6.json').write_text(json.dumps(new,indent=2));(S/'runtime-validation.json').write_text(json.dumps(merged,indent=2))
print('ENDING_CAPTURES_MERGED: runtime byte-identical; both missing showcases restored')
