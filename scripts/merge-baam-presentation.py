"""Merge normal-speed evidence only when it matches the exact full-suite build."""
from baam_model import *
import sys
baseline=json.loads((S/'validation'/sys.argv[1]).read_text())
retake=json.loads((S/'runtime-validation.json').read_text())
assert baseline['status']==retake['status']=='Complete' and baseline['failed']==retake['failed']==0
assert baseline['runtime_sha256']==retake['runtime_sha256']
assert baseline['passed']>=114
retake_path=sys.argv[2] if len(sys.argv)>2 else 'presentation-v1.json'
(S/'validation'/retake_path).write_text(json.dumps(retake,indent=2))
replacements={c['name']:c for c in retake['checks']}
old_names={c['name'] for c in baseline['checks']}
baseline['checks']=[replacements.get(c['name'],c) for c in baseline['checks']]+[c for c in retake['checks'] if c['name'] not in old_names]
frames=[]
for r in (baseline,retake):
    for f in r['frames']:
        if r is baseline and f['case_name'] in replacements:continue
        frames.append(dict(f,capture_directory=f.get('capture_directory',r['capture_directory'])))
baseline['frames']=frames;baseline['passed']=len(baseline['checks'])
baseline['presentation_retake']=dict(source='validation/'+retake_path,same_runtime=True,cases=sorted(replacements))
(S/'runtime-validation.json').write_text(json.dumps(baseline,indent=2))
print('BAAM_MERGED',baseline['passed'],'checks;',len(frames),'captures')
