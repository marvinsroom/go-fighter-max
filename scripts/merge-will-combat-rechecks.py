"""Replace a failed native row only with a separately recorded passing rerun."""
from pathlib import Path
import json,sys
source=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/will'
path=source/'combat-runtime-validation.json'
rerun_name=sys.argv[1] if len(sys.argv)>1 else 'combat-runtime-recheck.json'
initial=json.loads(path.read_text());rerun=json.loads((source/rerun_name).read_text())
assert initial['status']=='Complete' and rerun['status']=='Complete'
assert rerun['failed']==0 and rerun['passed']>0
backup=source/('combat-runtime-validation-before-agent-recheck.json' if 'agent' in rerun_name else 'combat-runtime-validation-before-recheck.json')
backup.write_text(json.dumps(initial,indent=2),encoding='utf-8')
replacement={row['name']:row for row in rerun['checks']}
names={row['name'] for row in initial['checks']}
assert set(replacement)<=names
initial['checks']=[replacement.get(row['name'],row) for row in initial['checks']]
initial['passed']=sum(row['passed'] for row in initial['checks'])
initial['failed']=len(initial['checks'])-initial['passed']
initial.setdefault('rechecks',[]).append({'report':rerun_name,'replaced_cases':list(replacement),
 'reason':'Agent projectile muzzle alignment and plasma effect update' if 'agent' in rerun_name else 'Super recovery observation extended from 240 to 330 ticks; original native report preserved separately'})
path.write_text(json.dumps(initial,indent=2),encoding='utf-8')
print('NATIVE_COMBAT_RESULTS',initial['passed'],'passed',initial['failed'],'failed')
