"""Merge focused native retakes only when their production build is identical."""
import hashlib,json,argparse
from rimuru_source import ROOT,SOURCE

parser=argparse.ArgumentParser();parser.add_argument('--baseline',default='runtime-effects-v4-full.json');parser.add_argument('--retakes',default='runtime-effects-v4-walks.json');options=parser.parse_args()
from pathlib import Path
assert all(Path(name).name==name for name in (options.baseline,options.retakes))
core_path=SOURCE/options.baseline
core=json.loads(core_path.read_text())
retake=json.loads((SOURCE/'runtime-validation.json').read_text())
assert core['status']==retake['status']=='Complete'
assert core['failed']==retake['failed']==0
assert core['runtime_sha256']==retake['runtime_sha256']
runtime=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru'
for name,digest in core['runtime_sha256'].items():assert hashlib.sha256((runtime/name).read_bytes()).hexdigest()==digest,name
(SOURCE/options.retakes).write_text(json.dumps(retake,indent=2),encoding='utf-8')
names={c['name'] for c in retake['checks']}
assert names<={c['name'] for c in core['checks']}
replacement={c['name']:c for c in retake['checks']}
checks=[replacement.get(c['name'],c) for c in core['checks']]
frames=[]
for report in (core,retake):
    for f in report['frames']:
        if report is core and f['case_name'] in names:continue
        frames.append(dict(f,capture_directory=f.get('capture_directory',report['capture_directory'])))
order={c['name']:i for i,c in enumerate(checks)}
frames.sort(key=lambda f:(order[f['case_name']],f['case_tick']))
core.update(checks=checks,frames=frames,passed=len(checks),failed=0,
            provenance=dict(method='Full native recording with focused real-time retakes; all production files have identical verified SHA-256 hashes.',full=options.baseline,retakes=options.retakes,replaced_cases=sorted(names)))
(SOURCE/'runtime-validation.json').write_text(json.dumps(core,indent=2),encoding='utf-8')
print('RIMURU_RETAKES',len(checks),'passed checks;',len(frames),'native frames; identical production hashes')
