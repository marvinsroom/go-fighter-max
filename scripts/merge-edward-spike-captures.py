"""Replace skipped spike showcases with normal-speed native captures.

No production character file changed: require identical runtime hashes.
"""
from pathlib import Path
import json
S=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/edward'
baseline=json.loads((S/'validation/before-spike-captures-v2.json').read_text())
retake=json.loads((S/'runtime-validation.json').read_text())
assert retake['status']=='Complete' and retake['failed']==0
assert baseline['runtime_sha256']==retake['runtime_sha256'],'Character changed during capture repair'
names={c['name'] for c in retake['checks']}
assert len(names)==8 and all('Stone Spike' in n for n in names)
for report in (baseline,retake):
    for f in report['frames']:f.setdefault('capture_directory',report['capture_directory'])
(S/'validation/spike-capture-retakes-v2.json').write_text(json.dumps(retake,indent=2))
checks={c['name']:c for c in baseline['checks']};checks.update({c['name']:c for c in retake['checks']})
baseline['checks']=list(checks.values())
baseline['frames']=[f for f in baseline['frames'] if f['case_name'] not in names]+retake['frames']
baseline['passed']=sum(c['passed'] for c in baseline['checks']);baseline['failed']=sum(not c['passed'] for c in baseline['checks'])
baseline['capture_repair']={'reason':'Fast capture skipped active Stone Spike drawings','retake_directory':retake['capture_directory'],'normal_speed':True,'production_runtime_unchanged':True,'replaced_clips':sorted(names)}
(S/'runtime-validation.json').write_text(json.dumps(baseline,indent=2))
print('EDWARD_SPIKE_CAPTURES_MERGED',baseline['passed'],'checks')
