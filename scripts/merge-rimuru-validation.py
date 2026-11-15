"""Combine unchanged core checks with the corrected isolated ultimate checks."""
import json
from rimuru_source import SOURCE
initial=json.loads((SOURCE/'runtime-initial.json').read_text())
ultimate=json.loads((SOURCE/'runtime-validation.json').read_text())
assert initial['status']=='Complete' and ultimate['status']=='Complete'
assert len(ultimate['checks'])==5 and ultimate['failed']==0
(SOURCE/'runtime-ultimate.json').write_text(json.dumps(ultimate,indent=2),encoding='utf-8')
core=[c for c in initial['checks'] if not c['name'].startswith('Megiddo')]
assert len(core)==13 and all(c['passed'] for c in core)
frames=[]
for report,include in [(initial,lambda n:not n.startswith('Megiddo')),(ultimate,lambda n:True)]:
    frames.extend(dict(f,capture_directory=report['capture_directory']) for f in report['frames'] if include(f['case_name']))
checks=core+ultimate['checks']
report=dict(status='Complete',passed=len(checks),failed=0,checks=checks,frames=frames,capture_directory=initial['capture_directory'],method='Native Ikemen command routes. Core recording plus five isolated ultimate reruns with opponent selfState reset.',source_reports=['runtime-initial.json','runtime-ultimate.json'])
(SOURCE/'runtime-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('RIMURU_COMBINED',len(checks),'passed;',len(frames),'native frames')
