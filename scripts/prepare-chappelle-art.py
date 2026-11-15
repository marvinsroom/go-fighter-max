"""Extract generated sprite cells without resampling or recoloring artwork."""
from pathlib import Path
from PIL import Image
from scipy import ndimage
import numpy as np,json,sys
ROOT=Path(__file__).resolve().parents[1]
KEYS=['idle','walk_a','walk_b','palm','kick','special','crouch','hurt','down']
for slug in sys.argv[1:] or ['prince','negan','rick','tyrone']:
    art=ROOT/'sprite-fighter/characters'/('rick' if slug=='tyrone' else slug)/'art'
    path=art/('tyrone-keyposes-v1.png' if slug=='tyrone' else 'keyposes-v1.png')
    im=Image.open(path).convert('RGBA');assert im.getchannel('A').getextrema()==(0,255)
    w,h=im.size;out=art/('tyrone-v1' if slug=='tyrone' else 'v1');out.mkdir(exist_ok=True)
    meta={}
    for i,key in enumerate(KEYS):
        row,col=divmod(i,3)
        box=(max(0,round(col*w/3-w*.035)),max(0,round(row*h/3-h*.006)),min(w,round((col+1)*w/3+w*.035)),min(h,round((row+1)*h/3+h*.006)))
        if slug=='prince' and key in ('hurt','down','special'):
            box={'hurt':(440,835,825,1254),'down':(825,1035,1254,1254),'special':(900,421,1254,840)}[key]
        if slug=='negan' and key in ('palm','kick','special','hurt','down'):
            box={'palm':(0,430,480,840),'kick':(440,430,900,840),'special':(890,390,1254,840),'hurt':(470,840,820,1254),'down':(825,1010,1254,1254)}[key]
        crop=im.crop(box);rgba=np.array(crop);labels,n=ndimage.label(rgba[:,:,3]>0)
        sizes=np.bincount(labels.ravel());sizes[0]=0;main=labels==sizes.argmax()
        nearby=ndimage.binary_dilation(main,iterations=3)
        keep=np.isin(labels,np.unique(labels[nearby & (labels>0)])) & (labels>0)
        rgba[~keep]=0;result=Image.fromarray(rgba);bounds=result.getchannel('A').getbbox();assert bounds
        result.save(out/f'{key}.png');meta[key]={'crop':box,'bounds':bounds,'source_pixels_preserved':True}
    (art/(slug+'-extraction.json')).write_text(json.dumps(meta,indent=2))
    print('CHAPPELLE_ART',slug,im.size,{k:v['bounds'] for k,v in meta.items()})
