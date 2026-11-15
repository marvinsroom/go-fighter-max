"""Check installed GT source timing, illustrated rasters and native evidence."""
from gt_goku_model import *
from mugen_sff import Sff
from isolated_sprite_atlas import extract
from html.parser import HTMLParser
import json,hashlib

build=json.loads((S/'build-report.json').read_text())
runtime=json.loads((S/'runtime-validation.json').read_text())
assert runtime['status']=='Complete' and runtime['failed']==0
assert all(c['passed'] for c in runtime['checks'])
assert runtime['runtime_sha256']==build['runtime_sha256']
for name,digest in build['runtime_sha256'].items():
 with (O/name).open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==digest,name
original=actions((U/'GokuGT.air').read_text(encoding='cp1252'))
compiled=actions((O/'GokuGT.air').read_text());archive=Sff(O/'GokuGT.sff');used=set()
for bank in range(5):
 for action,rows in original.items():
  new=compiled[action+(bank+1)*1000000]
  assert [r['ticks'] for r in rows]==[r['ticks'] for r in new],(bank,action,'Source timing changed')
  for row in new:
   key=row['key']
   if key[0]<0:continue
   assert key in archive.keys,(bank,action,'Missing sprite',key)
   assert key[0] in (63000,64000,64900,64901,64902,64903) or 62000<=key[0]<=62004,key
   if 62000<=key[0]<=62004:assert key[0]==62000+bank,(bank,action,'Wrong form')
   used.add(key)
 for action in (0,20,40,500,700):
  assert all(row['key'][0]==62000+bank for row in compiled[action+(bank+1)*1000000] if row['key'][0]>=0),(bank,action,'Base body classified as an effect')
art=S/'art/illustrated-v1'
provenance=json.loads((art/'provenance.json').read_text())
assert provenance['tool']=='built-in imagegen' and not provenance['api_fallback_used']
for asset in provenance['assets'].values():assert hashlib.sha256((art/asset['file']).read_bytes()).hexdigest()==asset['sha256']
for slug in BANKS+['intro']:assert len(extract(art/(slug+'.png'),4,4))==16
assert {f['animation_element'] for f in runtime['frames'] if f['animation']==960100}==set(range(1,17))
for f in FORMS:
 for label in ['form cycle','charge and release','ground light','ground medium','ground heavy','air light','air medium','air heavy','hurt reaction','guard reaction']:
  assert any(c['name']==f['name']+' '+label and c['passed'] for c in runtime['checks']),(f['name'],label)
 for route in [r for r in routes() if r['form']==f['id']]:
  check=next(c for c in runtime['checks'] if c['name']==f['name']+' / '+route['name'])
  assert check['passed']
  if route['category'] in ('Supers','Ultimates'):assert check['damage']>0,check['name']
page=(S/'review.html').read_text(encoding='utf-8')
data=json.loads(re.search(r'window.GT_GOKU_REVIEW=(.*?);const data=',page,re.S)[1])
assert all(data['groups'].values())
for paths in data['clips'].values():
 for path in paths:assert (S/path).is_file(),path
class Links(HTMLParser):
 def __init__(self,folder):super().__init__();self.folder=folder
 def handle_starttag(self,tag,attrs):
  for name,target in attrs:
   if name in ('src','href') and target and not target.startswith(('http:','https:','#','data:')):assert (self.folder/target).is_file(),target
for path in [S/'review.html',art/'design-review.html']:
 parser=Links(path.parent);parser.feed(path.read_text(encoding='utf-8'))
select=(E/'data/select.def').read_text()
assert len(re.findall(r'^gt_goku\s*,',select,re.M))==1
result=dict(status='Complete',forms=5,move_routes=len(routes()),combat_drawings=80,intro_drawings=16,source_actions_preserved=len(original),source_rasters_used=0,engine_checks=runtime['passed'],failed=0,engine_captures=len(runtime['frames']),review_categories={k:len(v) for k,v in data['groups'].items()},runtime_sha256=build['runtime_sha256'])
(S/'verification.json').write_text(json.dumps(result,indent=2))
from runpy import run_path
run_path(str(R/'scripts/validate-gt-goku-art.py'),run_name='__main__')
print('GT_GOKU_VERIFIED',runtime['passed'],'checks;',len(original),'source timelines;',len(data['clips']),'clips')

alignment=json.loads((S/"alignment-validation.json").read_text())
assert alignment["status"]=="Complete" and alignment["runtime_sha256"]==build["runtime_sha256"]
assert alignment["max_hand_error"]<1 and alignment["max_trajectory_drift"]<.1
portrait=S/"art/presentation-v3"
meta=json.loads((portrait/"provenance.json").read_text())
assert meta["tool"]=="built-in imagegen" and hashlib.sha256((portrait/meta["file"]).read_bytes()).hexdigest()==meta["sha256"]
