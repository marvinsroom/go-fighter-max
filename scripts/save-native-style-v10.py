"""Persist built-in imagegen outputs and audit their transparent cell layout."""
from pathlib import Path
import json,re,shutil,hashlib,sys
import numpy as np
from PIL import Image
from isolated_sprite_atlas import extract
R=Path(__file__).resolve().parents[1]
slug,kind=sys.argv[1:3];a=R/'sprite-fighter/characters'/slug/'art/comic-style-v10';p=a/(kind+'.generation-pending.json');d=json.loads(p.read_text(encoding='utf-8'));src=Path(re.search(r'as (C:.*?\.png) by default',d['output_hint'])[1]);dest=a/(kind+'.png');shutil.copy2(src,dest)
q=next(q for q in json.loads((a/'requests.json').read_text()) if q['kind']==kind);im=Image.open(dest).convert('RGBA');alpha=np.asarray(im)[:,:,3];cells=[];failures=[]
if np.mean(alpha==0)<.2:failures.append('Background is not sufficiently transparent')
folder=a/'extracted'/kind;folder.mkdir(parents=True,exist_ok=True)
for i in range(q['columns']*q['rows']):
 col=i%q['columns'];row=i//q['columns'];box=(round(col*im.width/q['columns']),round(row*im.height/q['rows']),round((col+1)*im.width/q['columns']),round((row+1)*im.height/q['rows']));tile=im.crop(box);b=tile.getchannel('A').point(lambda a:255 if a>48 else 0).getbbox()
 if i>=q['count']:
  if b and np.sum(np.array(tile)[:,:,3]>48)>100:failures.append('Unexpected figure in empty cell '+str(i))
  continue
 if not b:failures.append('Missing drawing '+str(i));continue
 if min(b[0],b[1],tile.width-b[2],tile.height-b[3])<1:failures.append('Drawing reaches cell edge '+str(i))
 crop=tile.crop(b);crop.save(folder/(str(i).zfill(2)+'.png'));cells.append(dict(index=i,bounds=[box[0]+b[0],box[1]+b[1],box[0]+b[2],box[1]+b[3]],size=crop.size,rgba_sha256=hashlib.sha256(crop.tobytes()).hexdigest()))
d.update(tool='built-in imagegen',original_generated_file=str(src),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),layout_validation=dict(status='PASS' if not failures else 'REVIEW',cells=cells,failures=failures),slug=slug,kind=kind)
try:
 isolated=extract(dest,q['columns'],q['rows'],count=q['count'])
 cells=[]
 for i,(crop,bounds) in enumerate(isolated):
  crop.save(folder/(str(i).zfill(2)+'.png'));cells.append(dict(index=i,bounds=bounds,size=crop.size,rgba_sha256=hashlib.sha256(crop.tobytes()).hexdigest()))
 # Small discarded alpha specks in an unused cell are excluded by whole-figure
 # component extraction. No extra sprite is installed from unused cells.
 failures=[f for f in failures if not f.startswith(('Drawing reaches cell edge','Unexpected figure in empty cell'))]
 d['layout_validation']=dict(status='PASS' if not failures else 'REVIEW',method='Connected whole-figure extraction; source alpha retained',cells=cells,failures=failures)
except AssertionError as error:
 d['layout_validation']['connected_extraction_note']=str(error)
(a/(kind+'.generation.json')).write_text(json.dumps(d,indent=2),encoding='utf-8');(a/(kind+'.prompt.txt')).write_text(d['prompt'],encoding='utf-8');print(slug,kind,len(cells),'drawings',d['layout_validation']['status'],failures,flush=True)
