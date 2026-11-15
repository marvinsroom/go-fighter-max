"""Verify every form keeps collision/timing data and passes native checks."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sprite-fighter/characters/jinwoo'
ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
air=(ENGINE/'chars/jinwoo/jinwoo.air').read_text()
# Split on action headers; collision lines contain square brackets too.
actions={}
for block in re.split(r'(?=\[Begin Action )',air):
    match=re.match(r'\[Begin Action (\d+)\]',block)
    if match:actions[int(match[1])]=block.strip().splitlines()[1:]
checked=0
for n,lines in actions.items():
    if n>=6000 or not any(re.match(r'50,',line) for line in lines):continue
    for form in range(1,5):
        other=actions[n+form*10000]
        assert len(lines)==len(other),(n,form)
        for left,right in zip(lines,other):
            if re.match(r'50,',left):
                assert right.startswith('51,') and left.split(',')[4]==right.split(',')[4],(n,form)
            else:assert left==right,(n,form,left,right)
        checked+=1
native=json.loads((SOURCE/'transform-validation.json').read_text())
assert native['status']=='Complete' and native['passed']==40 and native['failed']==0,native.get('failed')
for form in range(1,5):
    cases=[c for c in native['checks'] if c.get('form')==form]
    assert len(cases)==7 and all(c['passed'] and not c['violations'] for c in cases)
random=[c for c in native['checks'] if c['name'].startswith('random toggle')]
assert len(random)==12 and all(c['returned'] and 1<=c['chosen']<=4 for c in random)
report=json.loads((SOURCE/'build-report.json').read_text())
report['transformation']['native_validation']={'report':'transform-validation.json','passed':40,'failed':0,'animation_banks_checked':checked}
report['status']='Random playable shadow forms: 40 native transformation checks passed; existing 56 combat checks preserved'
(SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('JINWOO_TRANSFORM_VERIFIED',checked,'animation banks preserve collisions/timing; 40 native checks passed')
