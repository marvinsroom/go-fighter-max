"""Extract complete Shinsu motifs, including wings with disconnected halves."""
from PIL import Image
import numpy as np
from scipy import ndimage

def effect_tiles(path):
    image=Image.open(path).convert('RGBA');pixels=np.array(image);height,width=pixels.shape[:2]
    labels,_=ndimage.label(pixels[:,:,3]>180);counts=np.bincount(labels.ravel())
    seeds=np.zeros(labels.shape,dtype=np.int16)
    for component in np.flatnonzero(counts[1:]>1000)+1:
        yy,xx=np.where(labels==component);row=min(3,int(yy.mean()*4/height));col=min(3,int(xx.mean()*4/width))
        seeds[labels==component]=row*4+col+1
    assert set(np.unique(seeds))==set(range(17)),('Missing VFX motif',np.unique(seeds))
    nearest=ndimage.distance_transform_edt(seeds==0,return_distances=False,return_indices=True)
    owners=seeds[tuple(nearest)];visible=pixels[:,:,3]>3
    result=[]
    for i in range(16):
        mask=(owners==i+1)&visible;yy,xx=np.where(mask);left,right,top,bottom=int(xx.min()),int(xx.max())+1,int(yy.min()),int(yy.max())+1
        tile=pixels[top:bottom,left:right].copy();tile[:,:,3]=np.where(mask[top:bottom,left:right],tile[:,:,3],0)
        canvas=Image.new('RGBA',(tile.shape[1]+32,tile.shape[0]+32));canvas.alpha_composite(Image.fromarray(tile),(16,16))
        # Keep the former nominal cell center as the effect's origin, preserving
        # the designed placement and scale without retaining neighboring pixels.
        center=(round((i%4+.5)*width/4)-left+16,round((i//4+.5)*height/4)-top+16)
        axis=(16,center[1]) if i in (12,13) else center
        result.append((canvas,axis))
    return result
