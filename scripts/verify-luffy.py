"""Verify installed art, original action timing, runtime evidence and review."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib
from mugen_sff import Sff
from luffy_model import FORMS,actions,source_folder,routes

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/luffy';O=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/luffy'
build=json.loads((S/'build-report.json').read_text());runtime=json.loads((S/'runtime-validation.json').read_text());audit=json.loads((S/'illustrated-build.json').read_text())
assert build['art']=='illustrated' and audit['drawings']==96 and audit['intro_drawings']==16 and audit['referenced_original_sprites']==0
assert runtime['status']=='Complete' and runtime['failed']==0 and runtime['passed']==len(runtime['checks'])
assert all(c['passed'] for c in runtime['checks']) and runtime['runtime_sha256']==build['runtime_sha256']
for name,digest in build['runtime_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
compiled=actions((O/'TC_Luffy_All_Forms.air').read_text());original=actions((source_folder(R)/'TC_Luffy_All_Forms.air').read_text(encoding='cp1252'))
for action,frames in original.items():assert [f['ticks'] for f in compiled[action]]==[f['ticks'] for f in frames],('Source timing changed',action)
archive=Sff(O/'Luffy.sff');used=set()
for action,frames in compiled.items():
 for row in frames:
  key=row['key']
  if key[0]<0:continue
  assert key in archive.keys,('Missing illustrated sprite',action,key)
  assert 62000<=key[0]<=62005 or key[0] in (63000,63200,64000),('Native raster referenced',action,key)
  used.add(key)
for form in FORMS:
 for action in (form['base'],form['base']+20):
  body=[f for f in compiled[action] if 62000<=f['key'][0]<=62005]
  assert body and all(f['key'][0]==62000+form['id'] for f in body),('Wrong form artwork',form['name'],action)
 assert len({f['key'] for f in compiled[60000+form['id']]})==2
assert any(f['key'][0]==62005 for f in compiled[9900]),'Tankman art missing'
assert [f['key'] for f in compiled[60100]]==[(63200,i) for i in range(16)]
from luffy_funny_intro import DURATIONS,LENGTH
assert [f['ticks'] for f in compiled[60100]]==DURATIONS
assert sum(f['ticks'] for f in compiled[60100])==LENGTH==256
intro=[f for f in runtime['frames'] if f['animation']==60100 and f['case_name'].startswith('Intro - ')]
assert {f['animation_element'] for f in intro}==set(range(1,17))
assert all(f['form']==0 for f in intro), 'Funny intro must remain in base Luffy'
assert any(c['name'].startswith('Intro - funny') and c['form']==0 and c['passed'] for c in runtime['checks'])
preview=(S/'art/funny-intro-v2/preview.html').read_text(encoding='utf-8')
assert json.loads(re.search(r'const duration=(\[.*?\])',preview)[1])==DURATIONS
assert all((S/'art/funny-intro-v2/poses'/f'{i}.png').is_file() for i in range(16))
page=(S/'review.html').read_text(encoding='utf-8');data=json.loads(re.search(r'window.LUFFY_REVIEW=(.*?);const data=',page,re.S)[1])
counts={k:len(v) for k,v in data['groups'].items()}
assert counts=={'Intro':1,'Charge up':5,'Basics':30,'Skills':36,'Supers':5,'Ultimates':5,'Forms':6},counts
assert len(build['routes'])==46 and len(data['clips'])==88
assert len(re.findall(r'^luffy\s*,',(O.parents[1]/'data/select.def').read_text(),re.M))==1
class Links(HTMLParser):
 def __init__(self,folder):super().__init__();self.folder=folder;self.count=0
 def handle_starttag(self,tag,attrs):
  for name,target in attrs:
   if name in ('href','src') and target and not target.startswith(('https:','http:','#','data:')):
    assert (self.folder/target.split('?')[0]).is_file(),('Missing review link',target)
    self.count+=1
links=0
for path in (S/'review.html',S/'art/illustrated-v1/design-review.html',S/'art/funny-intro-v2/preview.html'):
 parser=Links(path.parent);parser.feed(path.read_text(encoding='utf-8'));links+=parser.count
for frame in runtime['frames']:assert (S/'replays'/frame['capture_directory']/frame['file']).is_file()
result=dict(art='illustrated',passed=runtime['passed'],failed=0,forms=5,temporary_tankman=True,combat_drawings=96,intro_drawings=16,source_actions_with_preserved_timing=len(original),referenced_original_sprites=0,illustrated_sprites_referenced=len(used),intro_all_frames_verified=True,review_categories=counts,review_links=links,engine_frames=len(runtime['frames']),runtime_sha256=build['runtime_sha256'])
(S/'verification.json').write_text(json.dumps(result,indent=2));print('LUFFY_VERIFIED',runtime['passed'],'checks;',len(original),'source action timings;',len(runtime['frames']),'illustrated engine captures')
