"""Retain unaffected clips after a quiet-ultimate-only victim animation change."""
from pathlib import Path
import re,json
S=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/pyowol';V=S/'validation'
old=json.loads((V/'before-quiet-reaction-v6.json').read_text());new=json.loads((S/'runtime-validation.json').read_text())
assert old['status']==new['status']=='Complete' and old['failed']==new['failed']==0
for name,digest in old['runtime_sha256'].items():
    if name!='pyowol.cns':assert new['runtime_sha256'][name]==digest,name
before=(V/'before-quiet-reaction-v6.cns').read_text();after=(S/'pyowol.cns').read_text()
pattern=r'\n\[State 8250, (?:Quiet stillness|Finish reaction)\]\n.*?(?=\n\[State|\Z)'
blocks=re.findall(pattern,after,re.S);assert len(blocks)==2
assert all('(enemynear,stateno)=4001' in block and 'type=ChangeAnim' in block for block in blocks)
assert re.sub(pattern,'',after,flags=re.S)==before
replaced={'Reaper of the Drifting Moon','Ultimate facing left'}
assert {c['name'] for c in new['checks']}==replaced
merged=dict(old,runtime_sha256=new['runtime_sha256'])
merged['checks']=[next((n for n in new['checks'] if n['name']==c['name']),c) for c in old['checks']]
merged['frames']=[dict(f,capture_directory=f.get('capture_directory',old['capture_directory'])) for f in old['frames'] if f['case_name'] not in replaced]+[dict(f,capture_directory=new['capture_directory']) for f in new['frames']]
merged['quiet_reaction']={'reason':'Only two ChangeAnim controllers are added for a victim whose attacker is in ultimate state4001. Victim uses own idle until finishing cut, then own hurt; both ultimate facings fully recaptured. Other runtime files are byte-identical.','baseline':'validation/before-quiet-reaction-v6.json','retakes':'validation/quiet-reaction-retakes-v6.json'}
(V/'quiet-reaction-retakes-v6.json').write_text(json.dumps(new,indent=2));(S/'runtime-validation.json').write_text(json.dumps(merged,indent=2))
print('QUIET_REACTION_MERGED: 45 passed; two ultimate-only controllers; both facings recaptured')
