"""Preserve rejected drafts and prepare focused built-in imagegen repairs."""
from comic_identity_v3 import *
import json,hashlib,sys

jobs=[
 ('arthur','combat','count12','combat.rejected-extra-companions.png','Remove EVERY small black dragon/creature from this atlas, including ones near heads and shoulders. Arthur must be the ONLY actor in each cell. Keep ALL FOURTEEN original Arthur body drawings exactly, same positions, poses, sword, face, costume and flat comic rendering. Do not omit or merge any body. Do not add new poses or redraw the atlas into only twelve bodies. Make only creature removal; preserve the complete fourteen human silhouettes.'),
 ('mok-gyeongwoon','combat','touching','', 'Separate all fourteen complete bodies. The last rows have neighbouring hair, coat and foot shapes touching. Shrink EACH whole drawing by about 25 percent and recenter in its own cell. Keep all fourteen distinct poses, order, face, outfit and sword unchanged. Leave wide empty transparent gaps between rows as well as columns. No atmospheric haze or semi-opaque backdrop.'),
 ('zhuo-fan','combat','touching','', 'Separate all sixteen complete bodies. In row2 the second figure’s fingers touch the third figure’s boot. Shrink EACH whole drawing by about 25 percent and recenter in its own cell. Keep all sixteen poses, order, face, brown robe, red inner lapels, red forearm wraps, BARE hands and flat rendering unchanged. No weapons. Leave wide transparent gaps between all figures.'),
 ('jin-mori','body-03','clipped','', 'Repair the cropped hair at the top outer edge and all edge crowding. Shrink EACH whole drawing by about 25 percent and recenter in its own cell, reconstructing every missing hair tip and complete boot sole. Preserve all sixteen King poses, same youthful comic face and action-specific expressions, GOLD circlet, red wrist guards, tiger pelt, white shirt, blue pants and red sash. No green goggles or lenses. Keep all poses and their order.'),
 ('eugene','story','cape-drift','', 'Remove ONLY the hanging cape, its gold-edged outer cape tails and cape lining from ALL sixteen figures. Keep the navy tunic jacket itself with its small gold collar/cuff trim, trousers, boots, belt, sword, same silver-haired youthful face, every pose and all expressions UNCHANGED. Movement and combat sheets already have this cape-free outfit. No cloak, cape or mantle in any cell. Preserve exactly sixteen complete isolated head-to-toe bodies and their positions.'),
 ('cha-yeon-woo','story','sleeve-drift','', 'Correct ONLY the sleeves and gloves in all sixteen figures to match this character’s movement and combat outfit. His plain BLACK hooded tunic has FULL-LENGTH sleeves ending at the wrists, no exposed forearms. His hands are BARE with pale skin, no black gloves. Preserve the separate simple flowing black cloak, white expressionless mask, short dark hair, trousers, boots, compact steel dagger and pocket watch, every body pose and all positions exactly. No other costume or face changes.')
]
requests=json.loads((R/'.tmp/comic-style-v4-requests.json').read_text());repairs=[]
for slug,kind,reason,selected,instruction in jobs:
 if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
 q=next(dict(v) for v in requests if v['slug']==slug and v['kind']==kind);target=Path(q['destination'])
 rejected=target.with_name(kind+'.rejected-'+reason+'.png');suffix=1
 while rejected.exists():
  suffix+=1;rejected=target.with_name(kind+'.rejected-'+reason+f'-{suffix}.png')
 if target.exists():
  target.rename(rejected)
  meta=target.with_suffix('.generation.json')
  if meta.exists():meta.rename(rejected.with_suffix('.generation.json'))
 source=target.parent/selected if selected else rejected
 assert source.exists(),source
 q['references']=[str(source)]
 q['prompt']=f'''Precise production sprite atlas correction. The input is the EDIT TARGET. {instruction}
STRICT {q['columns']} columns x {q['rows']} rows, EXACTLY {q['count']} separate COMPLETE head-to-toe human drawings. Preserve the established simple flat comic inks and one-shadow-tone treatment, character identity, weapons and individual poses. Every hair tip, fingertip, coat hem, weapon and both feet fully inside its own cell and canvas. No touching silhouettes. No extra actors, inset heads, labels, text, floor, backdrop or effects. TRUE TRANSPARENT background.'''
 q['repair_reason']=reason;q['parent_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
 target.with_suffix('.request.json').write_text(json.dumps(q,indent=2))
 repairs.append(q)
(R/'.tmp/comic-style-v4-repair-batch.json').write_text(json.dumps(repairs,indent=2));print('Focused repairs prepared',len(repairs))
