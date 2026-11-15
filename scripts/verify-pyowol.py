"""Verify installed source hashes, scales, captures and native body extents."""
from pathlib import Path
import hashlib,json,re
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/pyowol';C=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/pyowol'
b=json.loads((S/'build-report.json').read_text());r=json.loads((S/'runtime-validation.json').read_text())
assert r['status']=='Complete' and r['failed']==0
assert r['runtime_sha256']==b['runtime_sha256']
expected=[m['name'] for m in b['normal_moves']]+['Thread arrival intro','Idle','Forward walk','Backward walk','Jump','Charge and release','Silk Snare','Ghost Daggers','Thread Reel','Silent Step','Silken Veil','Soul-Reaping Thread','Ghost Dagger Rain','Heavenly Silk Prison','Reaper of the Drifting Moon']
expected += [name for name in ('Light medium heavy chain','Normal to thread cancel','Ultimate facing left') if any(c['name']==name for c in r['checks'])]
assert set(expected)<={f['case_name'] for f in r['frames']},('Missing native showcase captures',set(expected)-{f['case_name'] for f in r['frames']})
for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,name
body=[v for v in b['poses'].values() if v['group']==50]
for bank in {v.get('bank','legacy') for v in body}:assert len({v['scale'] for v in body if v.get('bank','legacy')==bank})==1,bank
lookup={(v['group'],v['number']):v for v in body}
checks=[];failures=[]
for f in r['frames']:
    with Image.open(S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']) as im:im.verify()
    m=lookup.get((f['group'],f['drawing']))
    if not m:continue
    box=m['bounds'];axis=m['axis'];scale=m['scale'];face=f['facing']
    xs=[f['screen_x']*3+(x-axis[0])*scale*face for x in (box[0],box[2])]
    ys=[f['screen_y']*3+(y-axis[1])*scale for y in (box[1],box[3])]
    bounds=[min(xs),min(ys),max(xs),max(ys)]
    ok=bounds[0]>=-1 and bounds[1]>=-1 and bounds[2]<=1281 and bounds[3]<=721
    check=dict(case=f['case_name'],tick=f['case_tick'],bounds=[round(x,2) for x in bounds],passed=ok);checks.append(check)
    if not ok:failures.append(check)
result=dict(native_combat_passed=r['passed'],body_frames=len(checks),failures=failures,shared_scale_banks=len({v.get('bank','legacy') for v in body}),runtime_sha256=b['runtime_sha256'])
(S/'proportion-validation.json').write_text(json.dumps(result,indent=2));assert not failures,failures[:5]
print('PYOWOL_VERIFIED',r['passed'],'native cases;',len(checks),'complete body frames; runtime hashes match')
