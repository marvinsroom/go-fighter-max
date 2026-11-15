"""Small source-specific fixes required by the shared mechanics, with bounded diffs."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/jus-upgrade'
path=E/'chars/rimuru/rimuru_forms.cns';original=(O/'before'/path.relative_to(E)).read_bytes();text=original.decode('cp1252');changes=[]
parts=re.split(r'(?=^\[Statedef\s+)',text,flags=re.M|re.I)
for i,part in enumerate(parts):
 match=re.match(r'\[Statedef\s+(\d+)\]',part,re.I)
 if not match:continue
 state=int(match[1]);offset=state%1000
 if state//1000 in (870,871,872) and offset in (0,1,2,10,11,12,20,21,22):
  patched,count=re.subn(r'(?im)^(attr\s*=\s*[SCA]+\s*,\s*)HA\s*$',r'\1NA',part)
  assert count==1,(state,count)
  parts[i]=patched;changes.append(state)
assert len(changes)==27
path.write_bytes(''.join(parts).encode('cp1252'))
(O/'compatibility.json').write_text(json.dumps(dict(rimuru=dict(reason='Authored normal attacks were tagged HA (hyper attack), preventing normal-only launcher and air cancel rules. Correct only the 27 stand/crouch/air normals across three forms to NA; preserve special/super attributes and all damage/timing.',states=changes)),indent=2))
print('Rimuru: corrected normal attack classification in 27 form-aware normal states.')

# Reserve the shared aerial flight gesture without removing ordinary Shunpo.
path=E/'chars/ichigo/ichigo.cmd'
baseline=O/'before'/path.relative_to(E)
if not baseline.exists():
 import shutil
 baseline.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(path,baseline)
text=baseline.read_bytes().decode('cp1252')
pattern=r'(?ims)(^\[State -1, Shunpo\]\s*\n)(.*?)(?=^\[State|\Z)'
match=re.search(pattern,text)
assert match and '19480' in match[2]
guard='triggerall = !(map(jus.enabled) && statetype = A && command = "jus.up")\n'
text=text[:match.start()]+match[1]+guard+match[2]+text[match.end():]
path.write_bytes(text.encode('cp1252'))
report=json.loads((O/'compatibility.json').read_text())
report['ichigo']=dict(reason='Reserve Up+Q in the air for shared flight; ordinary Q Shunpo remains available.',state=19480,guard=guard.strip())
(O/'compatibility.json').write_text(json.dumps(report,indent=2))
print('Ichigo: reserved shared aerial Up+Q flight gesture; normal Shunpo retained.')
