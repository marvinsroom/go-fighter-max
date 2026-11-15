"""Build explicit, non-destructive comic-identity edits for playable body banks."""
from comic_identity_v3 import *
from manhwa_expansion import BATCH
from manhwa_fighters import PROFILES
import json,shutil,sys
requests=[]
for slug in PROFILES:
 if len(sys.argv)>1 and slug not in sys.argv[1:]:continue
 p=SPECS[slug];old=C/slug/'art/illustrated-v1';new=C/slug/'art/comic-identity-v3';new.mkdir(exist_ok=True)
 for kind in ('movement','combat','story'):
  layout=PROFILES[slug].get('art_layouts',{}).get(kind,{})
  cols=layout.get('columns',4);rows=layout.get('rows',4);count=cols*rows
  prompt='Use case: precise-object-edit. Image1 is ORIGINAL COMIC IDENTITY reference. '+('Image2 is an additional original comic appearance reference. ' if len(p['refs'])>1 else '')+'LAST image is the existing game POSE/LAYOUT TEMPLATE ONLY; its current face and invented costume are WRONG. Redraw all '+str(count)+' existing FULL-BODY poses as '+p['name']+' exactly as drawn in the original comic panel. '+p['identity']+' Copy the reference artist\'s face contours, eyes, brows, nose, mouth, hair clumps and clothing construction faithfully, using simple comic linework and flat cel shading. No glossy generic anime beautification, no ornate additions, no new armor. Preserve EXACT pose order, facing, limb gestures, combat weapons and personality props from the last image; change face/hair/clothing to the comic. '+('For story pose13 keep ONE tiny black Sylvie on shoulder; do not duplicate her elsewhere. ' if slug=='arthur' and kind=='story' else '')+'STRICT '+str(cols)+' columns by '+str(rows)+' rows, EXACTLY '+str(count)+' separate COMPLETE head-to-toe drawings. Every hair tip, coat tail, weapon and both boots fully inside its cell with huge transparent gutters and outer margins. Shrink figures to fit instead of cropping; no torso portraits. No touching figures, no giant baked effects or blade trails, no text or scenery. TRUE TRANSPARENT background.'
  (new/(kind+'.prompt.txt')).write_text(prompt,encoding='utf-8')
  requests.append(dict(slug=slug,kind=kind,columns=cols,rows=rows,prompt=prompt,references=[str(REF/(n+'.png')) for n in p['refs']]+[str(old/(kind+'.png'))],destination=str(new/(kind+'.png')),active=str(old/(kind+'.png'))))
(R/'.tmp/comic-body-requests.json').write_text(json.dumps(requests,indent=2));print('COMIC_BODY_EDITS',len(requests))
