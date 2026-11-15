"""Preserve the normal-speed intro recording alongside the combat galleries."""
from pathlib import Path
import json,shutil

S=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/ichigo'
intro=json.loads((S/'runtime-validation.json').read_text())
power=json.loads((S/'power-validation.json').read_text())
assert intro['status']=='Complete' and intro['passed']==1 and intro['failed']==0
assert intro['runtime_sha256']==power['runtime_sha256']
frames=[f for f in intro['frames'] if f['animation']==60100]
assert {f['animation_element'] for f in frames}==set(range(1,17)), 'All sixteen intro drawings must be captured'
(S/'intro-validation.json').write_text(json.dumps(intro,indent=2))
power['checks']=[c for c in power['checks'] if not c['name'].startswith('Intro - ')]+intro['checks']
power['frames']=[f for f in power['frames'] if not f['case_name'].startswith('Intro - ')]
for frame in intro['frames']:
 source=S/'replays'/intro['capture_directory']/frame['file']
 name='School_intro_'+frame['file']
 shutil.copy2(source,S/'replays'/power['capture_directory']/name)
 power['frames'].append(dict(frame,file=name))
power['intro_recording']=dict(report='intro-validation.json',capture_directory=intro['capture_directory'],speed='real time',drawings_verified=16)
(S/'power-validation.json').write_text(json.dumps(power,indent=2))
print('ICHIGO_SCHOOL_INTRO_VERIFIED',len(intro['frames']),'real-time engine captures; all 16 drawings')
