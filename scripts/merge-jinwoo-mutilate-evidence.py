"""Retain byte-proven unaffected cases; replace Mutilate and add its pose checks."""
import json
from jinwoo_mutilate_evidence import SOURCE,prove

proof=prove();v=SOURCE/'validation'
core=json.loads((v/'pre-mutilate-v15-current.json').read_text())
focus=json.loads((v/'mutilate-v15-focus.json').read_text())
assert focus['status']=='Complete' and focus['passed']==1 and focus['failed']==0
assert focus['checks'][0]['name']=='Mutilate ultimate' and focus['checks'][0]['rendered_drawings']>=8
checks=[focus['checks'][0] if c['name']=='Mutilate ultimate' else c for c in core['checks']]
frames=[]
for report in (core,focus):
    for f in report['frames']:
        if report is core and f['case_name']=='Mutilate ultimate':continue
        if report is core:assert f['animation'] not in proof['changed_actions'],f['case_name']
        frames.append(dict(f,src=f.get('src',f"replays/{report['capture_directory']}/Jinwoo_hybrid{f['index']-1:03d}.png")))
core.update(checks=checks,frames=frames,passed=len(checks),failed=0,status='Complete',provenance=dict(compatibility='mutilate-v15-compatibility.json',baseline='pre-mutilate-v15-current.json',retake='mutilate-v15-focus.json',method='Only Mutilate AIR actions changed; all controller and existing sprite bytes verified identical. Mutilate case replaced with a fresh native recording.'))
(v/'current.json').write_text(json.dumps(core,indent=2),encoding='utf-8')
old=json.loads((v/'pre-mutilate-v15-proportions.json').read_text())
new=json.loads((v/'proportions-native.json').read_text())
assert new['status']=='Complete' and new['passed']==18 and new['failed']==0
assert all(c['key'].startswith('base:mutilate_') or c['key']=='base:idle' for c in new['checks'])
(v/'mutilate-v15-proportions.json').write_text(json.dumps(new,indent=2),encoding='utf-8')
replaced={(c['key'],c['facing']) for c in new['checks']}
kept_checks=[c for c in old['checks'] if (c['key'],c['facing']) not in replaced]
kept_frames=[f for f in old['frames'] if (f['key'],f['facing']) not in replaced]
new.update(checks=kept_checks+new['checks'],frames=kept_frames+new['frames'],passed=len(kept_checks)+new['passed'],provenance=dict(compatibility='mutilate-v15-compatibility.json',baseline='pre-mutilate-v15-proportions.json',retake='mutilate-v15-proportions.json',method='All old sprite headers, images and registration metadata are identical; append both-facing checks of eight new poses and refresh both stance references. Each pose settles for 24 ticks after round warmup before capture.'))
(v/'proportions-native.json').write_text(json.dumps(new,indent=2),encoding='utf-8')
print('MUTILATE_EVIDENCE',len(checks),'combat cases;',new['passed'],'native pose checks; native Mutilate damage',focus['checks'][0]['damage'])
