"""Register isolated guest/bow poses at the midpoint of their grounded feet."""
from pathlib import Path
import json
import numpy as np
from isolated_sprite_atlas import extract

art=Path(__file__).resolve().parents[1]/'sprite-fighter/characters/vikir/art/guests-v1'
layout={'revision':'manhwa-guests-and-anubis-v1','thresholds':{}}
for name in ['dolores','camu','aiyen','sinclair','anubis']:
    roots=[]
    for im,bounds in extract(art/(name+'.png'),4,2):
        pixels=np.asarray(im);rgb=pixels[:,:,:3].astype(float)
        dark=(pixels[:,:,3]>160)&(rgb.max(axis=2)<150)
        yy,xx=np.where(dark);bottom=int(yy.max())
        # Include both soles when a wide stance puts one foot slightly higher.
        # A thin bottom strip follows just one boot and makes the actor jump.
        xx=np.where(dark[max(0,bottom-60):bottom+1])[1]
        rootx=round((np.quantile(xx,.02)+np.quantile(xx,.98))/2)
        roots.append([int(bounds[0]+rootx),int(bounds[1]+bottom+1)])
    layout[name]=roots
(art/'ready.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
print('VIKIR_GUEST_ART_REGISTERED',sum(len(layout[n]) for n in ['dolores','camu','aiyen','sinclair','anubis']))
