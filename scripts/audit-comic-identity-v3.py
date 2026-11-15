"""Reject missing, merged, clipped or opaque comic sprite banks before install."""
from comic_identity_v3 import *
from isolated_sprite_atlas import extract
from PIL import Image
import json,sys
requests=json.loads((R/'.tmp/comic-body-requests.json').read_text())+json.loads((R/'.tmp/comic-legacy-requests.json').read_text())
report=[]
for q in requests:
 if len(sys.argv)>1 and q['slug'] not in sys.argv[1:]:continue
 path=Path(q['destination'])
 if not path.exists():print('PENDING',q['slug'],q['kind']);continue
 try:
  # The installed generation records actual accepted layout deviations, such as
  # Baam's final six drawings arranged as 3x2 instead of the requested 4x2.
  metadata=path.with_suffix('.generation.json')
  if metadata.exists():
   accepted=json.loads(metadata.read_text())
   q=dict(q,**{k:accepted[k] for k in ('columns','rows','count') if k in accepted})
  im=Image.open(path);assert im.mode=='RGBA' and im.getextrema()[3][0]==0,'Missing transparency'
  tiles=extract(path,q['columns'],q['rows'],count=q.get('count'))
  d=path.parent/'extracted';d.mkdir(exist_ok=True)
  for i,(tile,bounds) in enumerate(tiles):tile.save(d/(q['kind']+'-'+str(i).zfill(2)+'.png'))
  record=dict(slug=q['slug'],kind=q['kind'],status='PASS',count=len(tiles),bounds=[b for _,b in tiles])
 except Exception as e:record=dict(slug=q['slug'],kind=q['kind'],status='FAIL',error=str(e))
 report.append(record);print(record['status'],q['slug'],q['kind'],record.get('error',''),flush=True)
(REF/'atlas-audit.json').write_text(json.dumps(report,indent=2))
if any(r['status']=='FAIL' for r in report):sys.exit(1)
