"""Use normal-speed retakes without discarding the full 71-case baseline."""
from jin_mori_assets import *
import sys

baseline_path=sys.argv[1] if len(sys.argv)>1 else 'upgrade-final-v1.json'
retake_path=sys.argv[2] if len(sys.argv)>2 else 'presentation-v2.json'
baseline=json.loads((S/'validation'/baseline_path).read_text())
retake=json.loads((S/'runtime-validation.json').read_text())
assert baseline['status']==retake['status']=='Complete'
assert baseline['failed']==retake['failed']==0
assert baseline['runtime_sha256']==retake['runtime_sha256']
assert baseline['passed']==71 and retake['passed']>0
(S/'validation'/retake_path).write_text(json.dumps(retake,indent=2))
replace={c['name'] for c in retake['checks']}
assert replace<={c['name'] for c in baseline['checks']}
proof={c['name']:c for c in retake['checks']}
baseline['checks']=[proof.get(c['name'],c) for c in baseline['checks']]
frames=[]
for report in (baseline,retake):
    for f in report['frames']:
        if (report is baseline and f['case_name'] in replace) or (report is retake and f['case_name'] not in replace):continue
        frames.append(dict(f,capture_directory=f.get('capture_directory',report['capture_directory'])))
baseline['frames']=frames
baseline['presentation_retake']=dict(cases=sorted(replace),source='validation/'+retake_path,reason='Normal-speed renderer captures preserve entrance, awakening, combo and staff-strike poses',unchanged_runtime=True)
(S/'runtime-validation.json').write_text(json.dumps(baseline,indent=2))
print('MORI_MERGED',len(baseline['checks']),'checks;',len(frames),'captures')
