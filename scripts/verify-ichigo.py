"""Verify installed illustrated art, imported animation timing and review assets."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
from ichigo_model import FORMS,actions,source_folder
from mugen_sff import Sff

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/ichigo'
O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/ichigo'
build=json.loads((S/'build-report.json').read_text())
runtime=json.loads((S/'runtime-validation.json').read_text())
assert build['art']=='illustrated'
assert runtime['status']=='Complete' and runtime['failed']==0
assert runtime['runtime_sha256']==build['runtime_sha256']
assert len(runtime['checks'])==runtime['passed'] and all(c['passed'] for c in runtime['checks'])
for name,digest in build['runtime_sha256'].items():
 assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
compiled=actions((O/'Ichigo.air').read_text())
original=actions((source_folder(R)/'Ichigo.air').read_text(encoding='cp1252',errors='replace'))
for action,rows in original.items():
 assert [f['ticks'] for f in compiled[action]]==[f['ticks'] for f in rows],('Timing changed',action)
archive=Sff(O/'Ichigo.sff');referenced=set()
for action,rows in compiled.items():
 for row in rows:
  key=row['key']
  if key[0]<0:continue
  assert key in archive.keys,('Missing installed sprite',action,key)
  assert 62000<=key[0]<=62012 or key[0] in (63000,63200,64000),('Source raster reference',action,key)
  referenced.add(key)
for form in FORMS:
 group=62000+form['id']
 for action in (form['base'],form['base']+20,form['base']+200):
  actor_rows=[f for f in compiled[action] if 62000<=f['key'][0]<=62012]
  assert actor_rows and all(f['key'][0]==group for f in actor_rows),('Incorrect form art',form['name'],action)
 assert {f['key'][0] for f in compiled[60000+form['id']]}=={group}
 assert {f['key'][0] for f in compiled[60020+form['id']]}=={group}
 assert len({f['key'] for f in compiled[form['base']+200]})>=2,('Static attack',form['name'])
assert any(f['key'][0]==62012 for f in compiled[153000]),'Mugetsu artwork missing'
assert [f['key'] for f in compiled[60100]]==[(63200,i) for i in range(16)]
from ichigo_school_intro import DURATIONS,REVEAL,LENGTH
assert [f['ticks'] for f in compiled[60100]]==DURATIONS
assert REVEAL==132 and LENGTH==220
assert any(c['name'].startswith('Intro - ') and c.get('form')==2 and c['passed'] for c in runtime['checks'])
intro_frames=[f for f in runtime['frames'] if f['case_name'].startswith('Intro - ') and f['animation']==60100]
assert {f['animation_element'] for f in intro_frames}==set(range(1,17)), 'Capture every school-to-Bankai drawing'
assert all(f['form']==0 for f in intro_frames if f['animation_element']<10)
assert all(f['form']==2 for f in intro_frames if f['animation_element']>11)
page_text=(S/'review.html').read_text(encoding='utf-8')
review_data=json.loads(re.search(r'window.ICHIGO_REVIEW=(.*?);const data=',page_text,re.S)[1])
counts={name:len(clips) for name,clips in review_data['groups'].items()}
assert counts=={'Intro':1,'Charge up':11,'Basics':66,'Skills':66,'Supers':11,'Ultimates':11,'Forms':12},counts
roster=(O.parents[1]/'data/select.def').read_text()
assert len(re.findall(r'^ichigo\s*,',roster,re.M))==1
class Links(HTMLParser):
 def __init__(self,folder):super().__init__();self.folder=folder;self.count=0
 def handle_starttag(self,tag,attrs):
  for name,target in attrs:
   if name in ('src','href') and target and not target.startswith(('http:','https:','#','data:')):
    assert (self.folder/target.split('?')[0]).exists(),('Missing review asset',target)
    self.count+=1
link_count=0
for page in (S/'review.html',S/'art/illustrated-v2/design-review.html',S/'art/school-intro-v4/design-review.html'):
 parser=Links(page.parent);parser.feed(page.read_text(encoding='utf-8'));link_count+=parser.count
for frame in runtime['frames']:
 assert (S/'replays'/frame.get('capture_directory',runtime['capture_directory'])/frame['file']).is_file()
result=dict(art='illustrated',runtime_checks=runtime['passed'],failed=0,source_actions_with_preserved_timing=len(original),
            referenced_original_sprites=0,referenced_illustrated_sprites=len(referenced),forms_verified=len(FORMS),
            mugetsu_verified=True,intro_bankai_verified=True,review_categories=counts,review_links=link_count,engine_frames=len(runtime['frames']),runtime_sha256=build['runtime_sha256'])
(S/'verification.json').write_text(json.dumps(result,indent=2))
print('ICHIGO_VERIFIED',runtime['passed'],'runtime checks;',len(original),'source action timings;',len(runtime['frames']),'illustrated engine captures')
