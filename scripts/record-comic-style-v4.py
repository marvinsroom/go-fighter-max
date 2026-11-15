"""Save built-in generation provenance and reject broken atlas layouts."""
from comic_identity_v3 import *
from isolated_sprite_atlas import extract
from PIL import Image
import json,sys,shutil,hashlib

slug,kind,source=sys.argv[1:4]
q=next(q for q in json.loads((R/'.tmp/comic-style-v4-requests.json').read_text()) if q['slug']==slug and q['kind']==kind)
target=Path(q['destination'])
override=target.with_suffix('.request.json')
if override.exists():q=json.loads(override.read_text())
assert not target.exists(),('Already recorded',target)
shutil.copy2(source,target)
target.with_suffix('.prompt.txt').write_text(q['prompt'],encoding='utf-8')
meta=dict(q,tool='built-in image_gen.imagegen',original_generated_file=source,revision='comic-style-v4',sha256=hashlib.sha256(target.read_bytes()).hexdigest())
im=Image.open(target)
try:
    assert im.mode=='RGBA' and im.getextrema()[3][0]==0,'Missing transparency'
    tiles=extract(target,q['columns'],q['rows'],count=q['count'])
    out=target.parent/'extracted';out.mkdir(exist_ok=True)
    for i,(tile,bounds) in enumerate(tiles):tile.save(out/f'{kind}-{i:02}.png')
    meta['layout_validation']=dict(status='PASS',count=len(tiles),bounds=[b for _,b in tiles])
except Exception as error:
    meta['layout_validation']=dict(status='FAIL',error=str(error))
target.with_suffix('.generation.json').write_text(json.dumps(meta,indent=2))
print(slug,kind,meta['layout_validation'])
if meta['layout_validation']['status']!='PASS':sys.exit(1)
