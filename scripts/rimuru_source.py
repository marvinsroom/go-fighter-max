"""Read the preserved SoulFire SFF v1 archive without changing its files."""
from pathlib import Path
import struct
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sprite-fighter/characters/rimuru'
UP=SOURCE/'source/upstream/Rimuru Demon Lord'

def sprites():
    data=(UP/'Rimuru Demon Lord.sff').read_bytes();offset=512;result=[];palette=None
    for i in range(struct.unpack_from('<I',data,20)[0]):
        nxt,size,x,y,g,n,link,shared=struct.unpack_from('<IIhhHHHB',data,offset)
        if size:
            raw=data[offset+32:offset+32+size]
            xmin,ymin,xmax,ymax=struct.unpack_from('<4H',raw,4)
            w,h=xmax-xmin+1,ymax-ymin+1
            planes=raw[65];stride=struct.unpack_from('<H',raw,66)[0]
            if not shared and planes==1:palette=raw[-768:]
            pixels=bytearray();j=128;needed=h*stride*planes
            while len(pixels)<needed:
                c=raw[j];j+=1
                if c>=192:
                    count=c&63;c=raw[j];j+=1
                else:count=1
                pixels.extend(bytes([c])*count)
            arr=np.frombuffer(pixels[:needed],dtype=np.uint8).reshape(h,planes,stride)[:,:,:w]
            rgba=np.empty((h,w,4),dtype=np.uint8)
            if planes==1:
                rgba[:,:,:3]=np.frombuffer(palette,dtype=np.uint8).reshape(256,3)[arr[:,0,:]]
                rgba[:,:,3]=np.where(arr[:,0,:]==0,0,255)
            else:rgba[:,:,:3]=arr[:,:3,:].transpose(0,2,1);rgba[:,:,3]=255
            im=Image.fromarray(rgba)
        else:im=result[link]['image'].copy()
        result.append(dict(group=g,number=n,axis=(x,y),image=im));offset=nxt
        if i%100==0:print('Decoded source sprite',i,flush=True)
    return result

if __name__=='__main__':
    from PIL import ImageDraw
    rows=sprites();sel=[r for r in rows if r['number']==0]
    out=Image.new('RGB',(1000,((len(sel)+9)//10)*110),(40,43,54));d=ImageDraw.Draw(out)
    for j,r in enumerate(sel):
        im=r['image'].copy();im.thumbnail((94,84));x=j%10*100;y=j//10*110
        out.paste(im,(x+(100-im.width)//2,y),im);d.text((x+4,y+87),str((r['group'],r['number'])),fill='white')
    out.save(SOURCE/'source/groups.jpg');print('Decoded',len(rows))
