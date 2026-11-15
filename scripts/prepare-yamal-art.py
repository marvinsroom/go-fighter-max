"""Losslessly extract generated key poses; preserve generated alpha and pixels."""
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage
import json
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'sprite-fighter/characters/yamal/art'
im=Image.open(ART/'yamal-keyposes-v1.png').convert('RGBA')
assert im.getchannel('A').getextrema()==(0,255)
# The generator arranged poses on a 3x3 sheet but allowed the lying pose to
# extend sideways. These disjoint crop windows retain every figure in full.
boxes={'idle':(40,0,410,440),'walk_a':(450,0,825,440),'walk_b':(870,0,1254,438),
       'kick':(0,440,440,840),'crouch':(410,560,880,825),'volley':(815,438,1254,800),
       'hurt':(0,840,405,1254),'down':(405,1100,970,1254),'jump':(880,805,1220,1170)}
out=ART/'v1';out.mkdir(exist_ok=True)
manifest={}
for key,box in boxes.items():
    # Crop coordinates are expressed in the displayed sheet's 1254px space.
    box=tuple(round(v*im.width/1254) for v in box)
    crop=im.crop(box)
    # Neighboring poses cross nominal grid boundaries. Select the main connected
    # silhouette, retaining its nearby antialias fragments without recoloring
    # or synthesizing any pixels. Other figures and isolated alpha noise drop.
    rgba=np.array(crop);labels,n=ndimage.label(rgba[:,:,3]>0)
    sizes=np.bincount(labels.ravel());sizes[0]=0;main=labels==sizes.argmax()
    nearby=ndimage.binary_dilation(main,iterations=3)
    keep=np.isin(labels,np.unique(labels[nearby & (labels>0)])) & (labels>0)
    rgba[~keep]=0;crop=Image.fromarray(rgba)
    bounds=crop.getchannel('A').getbbox();assert bounds,key
    crop.save(out/f'{key}.png')
    manifest[key]={'crop':box,'bounds':bounds,'pixels_preserved':True}
(ART/'extraction.json').write_text(json.dumps(manifest,indent=2))
print('YAMAL_ART',im.size,manifest)
