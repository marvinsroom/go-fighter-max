"""Combine core form coverage with final edge-recoil and walk recordings."""
import json,re
from pathlib import Path
from rimuru_source import SOURCE,ROOT
core=json.loads((SOURCE/'runtime-forms-core.json').read_text());edge=json.loads((SOURCE/'runtime-validation.json').read_text())
assert core['status']==edge['status']=='Complete' and core['failed']==edge['failed']==0
assert len(core['checks'])==116 and len(edge['checks'])==20
old=(SOURCE/'source/forms-v3-before-edge-snap.cns').read_text(encoding='utf-8')
new=(ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/rimuru/rimuru_forms.cns').read_text(encoding='utf-8')
assert re.sub(r'(?m)^snap=.*\n','',new)==old,'Only contact framing may differ from the core-tested state file'
for name,digest in core['runtime_sha256'].items():
    if name!='rimuru_forms.cns':assert edge['runtime_sha256'][name]==digest,name
(SOURCE/'runtime-forms-corners.json').write_text(json.dumps(edge,indent=2),encoding='utf-8')
replace={c['name']:c for c in edge['checks']};checks=[replace.get(c['name'],c) for c in core['checks']]
frames=[]
for report,predicate in [(core,lambda n:n not in replace),(edge,lambda n:True)]:frames.extend(dict(f,capture_directory=report['capture_directory']) for f in report['frames'] if predicate(f['case_name']))
result=dict(status='Complete',passed=116,failed=0,checks=checks,frames=frames,capture_directory=core['capture_directory'],runtime_sha256=edge['runtime_sha256'],source_reports=['runtime-forms-core.json','runtime-forms-corners.json'],method='116 native gameplay gates. Edge-only contact framing was then tightened; all 18 corner gates and both slime walking cycles rerun in real time. Other production files are byte-identical; non-edge state logic is unchanged.')
(SOURCE/'runtime-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('RIMURU_FORM_COVERAGE',len(checks),'checks;',len(frames),'captures')
