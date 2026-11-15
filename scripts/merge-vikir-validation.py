"""Aggregate independent gameplay and native gallery runs without stale assets."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/vikir'
b=json.loads((S/'build-report.json').read_text(encoding='utf-8'))
reports=[json.loads((S/p).read_text(encoding='utf-8')) for p in sys.argv[1:]]
assert reports
checks={};case_frames={}
for r in reports:
    assert r['status']=='Complete' and r['failed']==0,r.get('failed')
    assert r['runtime_sha256']==b['runtime_sha256'],'A validation run is stale'
    for c in r['checks']:checks[c['name']]=c
    current={}
    for f in r['frames']:current.setdefault(f['case_name'],[]).append(dict(f,capture_directory=f.get('capture_directory',r['capture_directory'])))
    case_frames.update(current)
frames=[f for rows in case_frames.values() for f in rows]
out=dict(status='Complete',passed=len(checks),failed=0,checks=list(checks.values()),frames=frames,capture_directory='multiple',runtime_sha256=b['runtime_sha256'],reports=sys.argv[1:])
(S/'runtime-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('VIKIR_AGGREGATED',len(checks),'checks;',len(frames),'frames')
