"""Audit saved baselines, packed animation scope, and final native evidence."""
from pathlib import Path
import json,re,hashlib,importlib.util,struct
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
data=json.loads((O/'manifest.json').read_text());checks=[];runtime={}
def check(name,ok):
 checks.append(dict(label=name,passed=bool(ok)))
 if not ok:print('FAIL',name,flush=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def actions(text):return {int(m[1]):block for block in re.split(r'(?=^\s*\[Begin Action\s+)',text,flags=re.I|re.M) if (m:=re.match(r'\s*\[Begin Action\s+(\d+)\]',block,re.I))}
allowed_changes={'ichigo/ichigo.cmd','rimuru/rimuru_forms.cns'}
compat=json.loads((O/'compatibility.json').read_text())
ichigo=O/'before/chars/ichigo/Ichigo.cmd'
text=ichigo.read_text(encoding='cp1252')
expected=re.sub(r'(?im)^(\[State -1, Shunpo\]\s*\n)',lambda m:m[0]+compat['ichigo']['guard']+'\n',text,count=1)
check('Ichigo change limited to reserved flight gesture',expected==(E/'chars/ichigo/Ichigo.cmd').read_text(encoding='cp1252'))
rimuru=O/'before/chars/rimuru/rimuru_forms.cns';parts=re.split(r'(?=^\[Statedef\s+)',rimuru.read_text(encoding='cp1252'),flags=re.I|re.M)
for i,part in enumerate(parts):
 match=re.match(r'\[Statedef\s+(\d+)\]',part,re.I)
 if match and int(match[1]) in compat['rimuru']['states']:parts[i]=re.sub(r'(?im)^(attr\s*=\s*[SCA]+\s*,\s*)HA\s*$',r'\1NA',part)
check('Rimuru change limited to normal attack classification',''.join(parts)==(E/'chars/rimuru/rimuru_forms.cns').read_text(encoding='cp1252'))
for baseline in (O/'before/chars').rglob('*'):
 if baseline.is_file() and baseline.suffix.lower() in ('.cns','.cmd','.zss'):
  rel=baseline.relative_to(O/'before/chars').as_posix();installed=E/'chars'/rel
  check('Native controller scope: '+rel,installed.exists() and (rel.lower() in allowed_changes or installed.read_bytes()==baseline.read_bytes()))
for row in data['fighters']:
 slug=row['slug'];native=E/'chars'/row['engine'];definition=native/row['definition'];text=definition.read_text(encoding='cp1252')
 check(slug+' compact localcoord',bool(re.search(r'(?im)^\s*localcoord\s*=\s*'+str(row['width'])+r'\s*,',text)))
 check(slug+' flight policy',f'jus.flight_allowed = {int(row["flight"])}' in text)
 original=(O/'before/chars'/row['engine']/row['definition']).read_text(encoding='cp1252')
 coord=f'localcoord = {row["width"]},{row["width"]*.75:g}'
 if re.search(r'(?im)^\s*localcoord\s*=',original):expected=re.sub(r'(?im)^\s*localcoord\s*=.*$',coord,original)
 else:expected=re.sub(r'(?im)^\[Info\]',lambda m:m[0]+'\n'+coord,original,count=1)
 expected+='\n; Illustrated JUS movement layer; original artwork and native moves retained.\n[Map]\njus.enabled = 1\njus.flight_allowed = '+str(int(row['flight']))+'\n'
 check(slug+' only requested definition changes',text==expected)
 packing=O/'art'/slug/'packing.json';form=O/'art'/slug/'form-cycles-packing.json'
 if not packing.exists():continue
 records=json.loads(packing.read_text());permitted=set(records['actions'])
 if form.exists():
  f=json.loads(form.read_text());permitted=set(f['changed_walk_actions']);cycles=f['cycles']
 else:cycles=[records]
 sprite_name=re.search(r'(?im)^\s*sprite\s*=\s*([^;\r\n]+)',text)[1].strip().strip('"')
 air_name=re.search(r'(?im)^\s*anim\s*=\s*([^;\r\n]+)',text)[1].strip().strip('"')
 before=O/'before/chars'/row['engine'];old=Sff(before/sprite_name);new=Sff(native/sprite_name)
 check(slug+' original sprite headers preserved',new.data[new.offset:new.offset+old.count*28]==old.data[old.offset:old.offset+old.count*28])
 check(slug+' original sprite pixels preserved',new.data[new.lo:new.lo+old.ls]==old.data[old.lo:old.lo+old.ls])
 old_pal,old_count=struct.unpack_from('<II',old.data,44);new_pal,new_count=struct.unpack_from('<II',new.data,44)
 check(slug+' original palettes preserved',new_count==old_count and new.data[new_pal:new_pal+new_count*16]==old.data[old_pal:old_pal+old_count*16])
 old_actions=actions((before/air_name).read_text(encoding='cp1252'));new_actions=actions((native/air_name).read_text(encoding='cp1252'))
 check(slug+' all native actions retained',old_actions.keys()==new_actions.keys())
 check(slug+' changes limited to walk actions',all(new_actions[k].strip()==v.strip() for k,v in old_actions.items() if k not in permitted))
 for c in cycles:
  check(slug+' eight unique packed poses '+str(c.get('source_group','base')),len({r['rgba_sha256'] for r in c['frames']})==8)
  for f in c['frames']:
   im=new.decode(new.keys[tuple(f['key'])]);check(slug+' packed raster '+str(f['key']),hashlib.sha256(im.tobytes()).hexdigest()==f['rgba_sha256'])
 del old,new
spec=importlib.util.spec_from_file_location('jus_mobility',R/'scripts/validate-jus-mobility.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
summary={};total=0
for suite,expected in [('native-mobility-validation.json',28),('native-combat-validation.json',28),('native-form-validation.json',8)]:
 report=json.loads((O/suite).read_text());fighters=report['fighters'];summary[suite]=dict(fighters=len(fighters),passed=sum(f['passed'] for f in fighters),failed=sum(f['failed'] for f in fighters))
 check(suite+' complete',report['status']=='Complete' and len(fighters)==expected and not report.get('errors'))
 for result in fighters:
  row=next(r for r in data['fighters'] if r['slug']==result['slug']);hashes=m.runtime(row);runtime[row['slug']]=hashes
  check(suite+' current '+row['slug'],result['failed']==0 and result.get('production_runtime_sha256',result.get('runtime_sha256'))==hashes and bool(result['screenshots']) and all((R/p).is_file() for p in result['screenshots']))
 total+=summary[suite]['passed']
camera=json.loads((O/'native-camera-validation.json').read_text());goku=next(r for r in data['fighters'] if r['slug']=='goku')
check('Current flight camera evidence',camera['failed']==0 and camera['runtime_sha256']==m.runtime(goku));total+=camera['passed']
browser=json.loads((O/'browser-validation.json').read_text());check('Browser evidence current',browser['status']=='PASS' and browser['review_sha256']==sha(O/'review.html'))
config=(E/'save/config.ini').read_text();check('Production has no test fixture',not any(s in config for s in ['jus-test-fixture','jus-native','jus-form-cycles-test','-jus-native']))
report=dict(status='Complete' if all(c['passed'] for c in checks) else 'In progress',scope=data['scope'],checks=checks,passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),native_checks=total,suites=summary,runtime_sha256=runtime,limitations=['Original Naruto and Saitama pixel artwork retained; new-character art is on hold.','Saitama retains his creator-defined damage immunity.','Added drawings expand walking; existing attack, hurt and cinematic artwork remains.'])
(O/'completion.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ('checks','runtime_sha256')},indent=2))
if report['failed']:raise SystemExit(1)
