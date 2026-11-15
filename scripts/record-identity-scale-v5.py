"""Record requested likeness replacements with exact built-in prompts and layout checks."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1]
slug,kind,source=sys.argv[1:4]
q=next(x for x in json.loads((R/'.tmp/identity-scale-v5-requests.json').read_text()) if x['slug']==slug and x['kind']==kind)
p=Path(q['destination']);assert not p.exists(),p
shutil.copy2(source,p)
q.update(tool='built-in image_gen.imagegen',original_generated_file=source,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p.with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
im=Image.open(p)
try:
 assert im.mode=='RGBA' and im.getextrema()[3][0]==0,'Missing transparency'
 if kind!='portrait':
  tiles=extract(p,q['columns'],q['rows'],count=q['count'])
  out=p.parent/'extracted';out.mkdir(exist_ok=True)
  for i,(tile,bounds) in enumerate(tiles):tile.save(out/f'{kind}-{i:02}.png')
  q['layout_validation']=dict(status='PASS',count=len(tiles),bounds=[b for _,b in tiles])
 else:q['layout_validation']=dict(status='PASS',count=1)
except Exception as e:q['layout_validation']=dict(status='FAIL',error=str(e))
p.with_suffix('.generation.json').write_text(json.dumps(q,indent=2))
print(slug,kind,q['layout_validation']['status'])
if q['layout_validation']['status']!='PASS':sys.exit(1)
