"""Save built-in face edits with their exact request and sprite atlas checks."""
from pathlib import Path
import json,sys,hashlib,shutil
from PIL import Image
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1]
slug,kind,source=sys.argv[1:4]
requests=json.loads((R/'.tmp/comic-face-v6-requests.json').read_text())
q=next(x for x in requests if x['slug']==slug and x['kind']==kind)
a=R/'sprite-fighter/characters'/slug/'art/comic-face-v6';a.mkdir(parents=True,exist_ok=True)
p=a/(kind+'.png');assert not p.exists();shutil.copy2(source,p)
q.update(tool='built-in image_gen.imagegen',original_generated_file=source,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),revision='comic-face-v6')
p.with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
try:
 im=Image.open(p);assert im.mode=='RGBA' and im.getextrema()[3][0]==0,'Transparency missing'
 if kind!='portrait':
  tiles=extract(p,q['columns'],q['rows'],count=16);out=a/'extracted';out.mkdir(exist_ok=True)
  for i,(tile,bounds) in enumerate(tiles):tile.save(out/f'{kind}-{i:02}.png')
  q['layout_validation']=dict(status='PASS',count=len(tiles),bounds=[b for _,b in tiles])
 else:q['layout_validation']=dict(status='PASS',count=1)
except Exception as e:q['layout_validation']=dict(status='FAIL',error=str(e))
p.with_suffix('.generation.json').write_text(json.dumps(q,indent=2))
print(slug,kind,q['layout_validation'])
if q['layout_validation']['status']!='PASS':sys.exit(1)
