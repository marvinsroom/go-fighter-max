"""Verify the final Goku assets, source timings, roster, review and runtime evidence."""
from goku_model import *
from mugen_sff import Sff
from html.parser import HTMLParser
from isolated_sprite_atlas import extract
import json,hashlib
build=json.loads((S/'build-report.json').read_text());audit=json.loads((S/'illustrated-build.json').read_text());runtime=json.loads((S/'runtime-validation.json').read_text())
art=S/'art/illustrated-v1';provenance=json.loads((art/'provenance.json').read_text());accepted=[a for a in provenance['assets'].values() if a['accepted']]
assert provenance['tool']=='built-in imagegen' and not provenance['api_fallback_used'] and len(accepted)==11
for asset in accepted:assert hashlib.sha256((art/asset['file']).read_bytes()).hexdigest()==asset['sha256'],asset['file']
assert build['art']=='illustrated' and len(build['forms'])==11 and len(build['routes'])==113
assert audit['drawings']==272 and audit['technique_drawings']==16 and audit['energy_body_drawings']==128 and audit['animated_effect_drawings']==32 and audit['intro_drawings']==16 and audit['referenced_original_sprites']==0
energy=S/'art/energy-v2'
energy_provenance=json.loads((energy/'provenance.json').read_text())
assert energy_provenance['tool']=='built-in imagegen' and not energy_provenance['api_fallback_used']
assert len(energy_provenance['assets'])==10
for asset in energy_provenance['assets'].values():assert hashlib.sha256((energy/asset['file']).read_bytes()).hexdigest()==asset['sha256']
for slug in BANKS:assert len(extract(energy/energy_provenance['assets']['body-'+slug]['file'],4,4))==16
assert runtime['status']=='Complete' and runtime['failed']==0 and runtime['passed']==len(runtime['checks'])
assert all(c.get('passed') for c in runtime['checks']) and runtime['runtime_sha256']==build['runtime_sha256']
for name,digest in build['runtime_sha256'].items():assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,name
original=actions((U/'Goku.air').read_text(encoding='cp1252'));compiled=actions((O/'Goku.air').read_text());archive=Sff(O/'Goku.sff');used=set()
for bank in range(8):
 for action,rows in original.items():
  new=compiled[action+(bank+1)*1000000]
  assert [r['ticks'] for r in rows]==[r['ticks'] for r in new],('Changed source timeline',bank,action)
  for row in new:
   key=row['key']
   if key[0]<0:continue
   assert key in archive.keys,('Missing illustrated sprite',bank,action,key)
   assert key[0] in (62100,63000,63200,64000,64900,64901,64902,64903) or 62000<=key[0]<=62007 or 62200<=key[0]<=62207,('Source raster referenced',key)
   if 62000<=key[0]<=62007:assert key[0]==62000+bank,('Wrong form',bank,action,key)
   if 62200<=key[0]<=62207:assert key[0]==62200+bank,('Wrong energy pose form',bank,action,key)
   if key[0]==62100:assert bank==0 and key[1]<12 or bank==3 and key[1]>=12,('Wrong technique form',bank,action,key)
   used.add(key)
assert [f['key'] for f in compiled[960100]]==[(63200,i) for i in range(16)]
for bank in range(8):
 for action in (1400,1401,400,620):
  body=[r['key'] for r in compiled[action+(bank+1)*1000000] if r['key'][0]==62200+bank]
  assert len(set(body))>=3,('Missing energy motion phases',bank,action)
for action in (410,420,1415,1420,1422):
 pixels={archive.decode(archive.keys[r['key']]).tobytes() for r in compiled[1000000+action] if r['key'][0]>=0}
 assert len(pixels)>=4,('Static energy animation',action)
for action,motif in [(3650,5)]:
 expected=archive.decode(archive.keys[(63000,motif)]).tobytes()
 actual=[archive.decode(archive.keys[r['key']]).tobytes() for r in compiled[1000000+action] if r['key'][0]>=0]
 assert actual and all(pixels==expected for pixels in actual),('Wrong illustrated effect motif',action)
intro=[f for f in runtime['frames'] if f['animation']==960100]
assert {f['animation_element'] for f in intro}==set(range(1,17)) and all(f['form']==0 for f in intro)
for slug in BANKS+['intro-v2','techniques']:assert len(extract(S/'art/illustrated-v1'/(slug+'.png'),4,4))==16
for f in FORMS:
 for suffix,field,expected in [('hurt reaction','hurt_animation',14),('guard reaction','guard_animation',1)]:
  check=next(c for c in runtime['checks'] if c['name']==f['name']+' '+suffix)
  animation=check[field]
  body=[r['key'] for r in compiled[animation] if 62000<=r['key'][0]<=62007]
  assert body and all(k==(62000+f['bank'],expected) for k in body),('Wrong reaction artwork',f['name'],suffix,animation,body)
page=(S/'review.html').read_text(encoding='utf-8');data=json.loads(re.search(r'window.GOKU_REVIEW=(.*?);const data=',page,re.S)[1])
assert set(data['groups'])=={'Intro','Charge up','Basics','Skills','Supers','Ultimates','Forms'}
assert all(data['groups'].values())
assert len(data['groups']['Basics'])==88
assert len(data['groups']['Charge up'])==11 and len(data['groups']['Forms'])==12
assert len(data['groups']['Skills'])==76 and len(data['groups']['Supers'])==25 and len(data['groups']['Ultimates'])==12
assert any(c['name'].endswith('full gather and release') and c['damage']>0 for c in runtime['checks'])
for f in FORMS:
 prefix=f['name']+' / Kamehameha'
 primary=next(c for c in runtime['checks'] if c['name']==prefix)
 guarded=next(c for c in runtime['checks'] if c['name']==prefix+' guard')
 missed=next(c for c in runtime['checks'] if c['name']==prefix+' miss')
 contact=json.loads((S/'contact-validation.json').read_text())
 observed=next(c for c in contact['checks'] if c['name']==prefix+' guard')
 assert primary['damage']>0 and observed.get('guarded') and missed['damage']==0,('Beam contact',f['name'])
select=(E/'data/select.def').read_text();assert len(re.findall(r'^goku\s*,',select,re.M))==1
assert not (S.parent/'miles').exists() and not (E/'chars/miles').exists()
class Links(HTMLParser):
 def __init__(self,folder):super().__init__();self.folder=folder;self.count=0
 def handle_starttag(self,tag,attrs):
  for name,target in attrs:
   if name in ('src','href') and target and not target.startswith(('http:','https:','#','data:')):
    assert (self.folder/target).is_file(),('Broken link',target);self.count+=1
links=0
for path in (S/'review.html',S/'art/illustrated-v1/design-review.html'):
 parser=Links(path.parent);parser.feed(path.read_text(encoding='utf-8'));links+=parser.count
for paths in data['clips'].values():
 for path in paths:assert (S/path).is_file()
result=dict(status='Complete',forms=11,move_routes=113,combat_drawings=272,intro_drawings=16,effect_motifs=16,animated_energy_drawings=32,engine_checks=runtime['passed'],failed=0,source_actions_preserved=len(original),source_rasters_used=0,illustrated_sprites_referenced=len(used),review_categories={k:len(v) for k,v in data['groups'].items()},engine_captures=len(runtime['frames']),review_links=links,runtime_sha256=build['runtime_sha256'])
(S/'verification.json').write_text(json.dumps(result,indent=2));print('GOKU_VERIFIED',runtime['passed'],'checks;',len(original),'source timelines; all 11 forms')

alignment=json.loads((S/"alignment-validation.json").read_text())
assert alignment["status"]=="Complete" and alignment["runtime_sha256"]==build["runtime_sha256"]
assert alignment["max_hand_error"]<1 and alignment["max_trajectory_drift"]<.1
portrait=S/"art/presentation-v3"
meta=json.loads((portrait/"provenance.json").read_text())
assert meta["tool"]=="built-in imagegen" and hashlib.sha256((portrait/meta["file"]).read_bytes()).hexdigest()==meta["sha256"]
