"""Check each generated atlas before it becomes a native fighter package."""
from manhwa_expansion import BATCH
from pathlib import Path
from isolated_sprite_atlas import extract
from baam_vfx import effect_tiles
from PIL import Image
import json,sys
ROOT=Path(__file__).resolve().parents[1]
kinds=next((a.split('=')[1].split(',') for a in sys.argv[1:] if a.startswith('--kind=')),['movement','combat','story','effects','portrait'])
for slug in [a for a in sys.argv[1:] if not a.startswith('--')] or BATCH:
 art=ROOT/'sprite-fighter/characters'/slug/'art/illustrated-v1';report={}
 for name in kinds:
  path=art/(name+'.png')
  if not path.exists():continue
  with Image.open(path) as im:
   assert im.mode=='RGBA' and im.getextrema()[3][0]==0,(slug,name,'Missing transparency')
   report[name]=dict(size=im.size,alpha=im.getextrema()[3])
  if name in ('movement','combat','story'):
   layout=BATCH[slug].get('art_layouts',{}).get(name,{})
   tiles=extract(path,layout.get('columns',4),layout.get('rows',4));report[name]['drawings']=len(tiles)
   report[name]['bounds']=[bounds for _,bounds in tiles]
  elif name=='effects':report[name]['motifs']=len(effect_tiles(path))
 (art/'atlas-audit.json').write_text(json.dumps(report,indent=2))
 print('ATLAS_AUDIT',slug,','.join(report),flush=True)
