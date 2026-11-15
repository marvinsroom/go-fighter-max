"""Verify the quiet execution and fine-silk integration against native evidence."""
from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter/characters/pyowol'
r=json.loads((S/'runtime-validation.json').read_text());build=json.loads((S/'build-report.json').read_text())
assert r['status']=='Complete' and r['failed']==0
for name in ('Silk Finger','Ankle Thread','Air Silk','Thread Reel','Soul-Reaping Thread','Heavenly Silk Prison','Reaper of the Drifting Moon','Ultimate facing left'):
    case=next(c for c in r['checks'] if c['name']==name)
    assert case['passed'] and case.get('max_threads',0)>=1,(name,'filament missing')
for name in ('Reaper of the Drifting Moon','Ultimate facing left'):
    frames=[f for f in r['frames'] if f['case_name']==name and f['state']==4001]
    lives={f['target_life'] for f in frames}
    assert {990,520}<=lives and lives<={1000,990,520},(name,'damage must wait for one finishing cut',lives)
    first=min(f['case_tick'] for f in frames)
    assert all(f['case_tick']<=first+2 for f in frames if f['target_life']==1000),(name,'opening damage delayed')
    assert {f['facing'] for f in frames}=={-1,1},(name,'single pass must face the victim')
    case=next(c for c in r['checks'] if c['name']==name)
    assert case['damage']==480 and case['target_final_state']==0,(name,'damage/release')
for i in range(6):
    im=Image.open(S/f'art/thread-v6/silk-{i}.png');alpha=im.getchannel('A')
    ratio=sum(a>30 for a in alpha.tobytes())/(im.width*im.height)
    assert ratio<.08,(i,'filament is too thick',ratio)
old=json.loads((S/'validation/before-thread-v6/build-report.json').read_text())
for key,pose in old['poses'].items():
    if pose['group'] in (50,9000):assert build['poses'][key]['sha256']==pose['sha256'],key
out=dict(native_cases=r['passed'],thread_moves=8,quiet_execution_orientations=2,clean_hit_damage=480,character_and_portrait_preserved=True)
(S/'silk-validation.json').write_text(json.dumps(out,indent=2))
print('SILK_VERIFIED: 8 moves emit fine filaments; both ultimate facings deliver one finishing cut; model/portrait unchanged')
