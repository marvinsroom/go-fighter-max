"""Extract whole isolated drawings without cutting at assumed grid boundaries."""
import numpy as np
from PIL import Image
from scipy import ndimage

def extract(path,columns,rows,separation_threshold=48,count=None):
    count=columns*rows if count is None else count
    assert 0<count<=columns*rows and count>columns*(rows-1)
    image=Image.open(path).convert('RGBA');pixels=np.array(image)
    labels,_=ndimage.label(pixels[:,:,3]>separation_threshold);areas=np.bincount(labels.ravel());areas[0]=0
    ids=np.argsort(areas)[-count:];objects=ndimage.find_objects(labels)
    assert min(areas[i] for i in ids)>max(areas[i] for i in ids)*.10,('Merged or missing drawings',path)
    if separation_threshold>48:
        # Thin translucent blade trails may join otherwise isolated figures.
        # Use opaque bodies as seeds, then retain the original edge pixels by
        # assigning translucent pixels to their nearest complete drawing.
        seeds=np.where(np.isin(labels,ids),labels,0)
        nearest=ndimage.distance_transform_edt(seeds==0,return_distances=False,return_indices=True)
        labels=np.where(pixels[:,:,3]>48,seeds[tuple(nearest)],0)
        objects=ndimage.find_objects(labels)
    ids=sorted(ids,key=lambda i:sum((objects[i-1][0].start,objects[i-1][0].stop)))
    ordered=[]
    for row in range(rows):ordered+=sorted(ids[row*columns:(row+1)*columns],key=lambda i:objects[i-1][1].start)
    result=[]
    for i in ordered:
        yy,xx=objects[i-1];assert min(xx.start,yy.start,image.width-xx.stop,image.height-yy.stop)>0,('Clipped drawing',path,i)
        tile=pixels[yy.start:yy.stop,xx.start:xx.stop].copy()
        # Exclude disconnected neighbouring fragments inside the rectangle.
        tile[:,:,3]=np.where(labels[yy.start:yy.stop,xx.start:xx.stop]==i,tile[:,:,3],0)
        result.append((Image.fromarray(tile),(xx.start,yy.start,xx.stop,yy.stop)))
    return result
