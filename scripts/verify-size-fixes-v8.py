"""Check current size policy, packed walks, preservation and display scale."""
from pathlib import Path
import json,re,statistics,hashlib,collections
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';O=G/'size-fix-v8';J=G/'jus-upgrade';E=G/'engine/ikemen-go-v1.0.0/chars'
policy=json.loads((O/'policy.json').read_text());measurements=json.loads((R/'.tmp/size-redesign/measurements.json').read_text());manifest={r['slug']:r for r in json.loads((J/'manifest.json').read_text())['fighters']};preview={r['slug']:r for r in json.loads((J/'review-data.json').read_text())['fighters']};checks=[];walk_count=0
def check(name,value):
 checks.append(dict(label=name,passed=bool(value)))
 if not value:print('FAIL',name,flush=True)
def timeline(raw):
 text=raw.decode('latin1');actions=re.findall(r'(?im)^\s*\[Begin Action\s+(\d+)\]',text);frames=[]
 for line in text.splitlines():
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=[s.strip() for s in line.split(';')[0].split(',')];frames.append((f[:7],f[9:]))
 return actions,frames
def scrub_size(raw):
 for field in ['xscale','yscale']:raw=re.sub(rb'(?im)^(\s*'+field.encode()+rb'\s*=\s*)[-+0-9.eE]+',lambda m:m[1]+b'SIZE',raw,count=1)
 return raw
for r in measurements:
 slug=r['slug'];row=manifest[slug];n=E/row['engine'];names=r['files'];before=O/'before'/row['engine']
 check(slug+' standing gameplay height',abs(r['world_height']-policy['neutral_world_height'][slug])<.03)
 actual=r['air_scale'][1]*r['cns_scale'][1]*320/r['width'];check(slug+' viewer uses native scale once',abs(preview[slug]['preview']['scale']-actual)<1e-8)
 check(slug+' state logic preserved',scrub_size((n/names['cns']).read_bytes())==scrub_size((before/names['cns']).read_bytes()))
 air=(n/names['anim']).read_bytes();check(slug+' animation IDs, timings, positions and flags preserved',timeline(air)==timeline((before/names['anim']).read_bytes()))
 check(slug+' definition/controls registration preserved',(n/row['definition']).read_bytes()==(before/row['definition']).read_bytes())
 p=J/'art'/slug/'packing.json';form=J/'art'/slug/'form-cycles-packing.json'
 if not p.exists():continue
 cycles=json.loads(form.read_text())['cycles'] if form.exists() else [json.loads(p.read_text())];sff=Sff(n/names['sprite']);scales={}
 for line in air.decode('latin1').splitlines():
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=[v.strip() for v in line.split(';')[0].split(',')];scales.setdefault(tuple(map(int,f[:2])),[]).append(float(f[8]) if len(f)>8 and f[8] else 1)
 for cycle in cycles:
  heights=[]
  for frame in cycle['frames']:
   key=tuple(frame['key']);header=sff.headers[sff.keys[key]];scale=collections.Counter(scales[key]).most_common(1)[0][0];heights.append(header[3]*scale*r['cns_scale'][1]*320/r['width'])
  check(slug+' packed walk matches body '+str(cycle.get('source_group','base')),abs(statistics.median(heights)-cycle['gameplay_world_height'])<.03);walk_count+=1
 del sff
items=json.loads((O/'review-data.json').read_text())['items']
for item in items:
 if item['role']!='alternate body':continue
 group=Path(item['neutral']['file']).stem.split('-')[-1];target=policy['forms'][item['slug']].get(group)
 if target is not None:check(item['label']+' alternate body size',abs(item['neutral']['height']-target)<.03)
check('46 additional walk cycles checked',walk_count==46)
art=G/'characters/cid/art/redesign-v7';installed=json.loads((art/'installation.json').read_text());current=E/'cid_shadow/Cid.sff'
check('Cid installed archive matches verified redraw',hashlib.sha256(current.read_bytes()).hexdigest()==installed['installed_sff_sha256'])
check('Cid redraw preserves original animation timeline',timeline((E/'cid_shadow/Cid.air').read_bytes())==timeline((art/'before/Cid.air').read_bytes()))
source_config=(E.parent/'save/config.ini').read_text();modules=re.search(r'(?im)^Modules[ \t]*=[ \t]*(.*)$',source_config)[1].split(';')[0].strip();check('Production has no recording modules',not modules)
report=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),fighters=len(measurements),body_references=len(items),additional_walk_cycles=walk_count,cid_drawings=installed['drawings'],checks=checks,recordings='Deferred at user request; no new gameplay footage generated')
(O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
if report['failed']:raise SystemExit(1)
