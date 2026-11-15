"""Register academy sprites and grounded sword sequences to their foot roots."""
from pathlib import Path
import json,sys
import numpy as np
from isolated_sprite_atlas import extract

R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/vikir'
art=S/'art/v3'
layout=json.loads((S/'art/v2/ready.json').read_text())
layout.update(revision='academy-choreography-v3',reference='../../references/academy-manhwa.png')
for sheet,base in [('school-movement','movement'),('school-combat','combat')]:
    tiles=extract(art/(sheet+'.png'),4,4)
    layout[sheet]=[[root[0],bounds[3]] for root,(_,bounds) in zip(layout[base],tiles)]
for sheet in ['power','night-power','school-power']:
    roots=[]
    for im,bounds in extract(art/(sheet+'.png'),4,4):
        pixels=np.asarray(im);rgb=pixels[:,:,:3].astype(float)
        neutral=(pixels[:,:,3]>160)&(rgb.max(axis=2)<140)&~((rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3))
        yy,xx=np.where(neutral);bottom=int(yy.max())
        xx=np.where(neutral[max(0,bottom-7):bottom+1])[1]
        rootx=round((np.quantile(xx,.01)+np.quantile(xx,.99))/2)
        roots.append([int(bounds[0]+rootx),int(bounds[1]+bottom+1)])
    layout[sheet]=roots
(art/'ready.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
print('VIKIR_ART_REGISTERED',len(layout['school-movement'])+len(layout['school-combat'])+48,'new drawings')
