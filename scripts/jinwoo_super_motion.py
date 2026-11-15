"""Register and pack the dedicated whole-body human super drawings."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy import ndimage
from jinwoo_hybrid_art import drawing


SPECS={
 'dagger':dict(file='art/daggers/super-identity-v12-separated.png',head_pixels=70,columns=4,
               xs=(165,565,965,1378,225,585,1010,1388),ys=(505,498,500,508,955,933,953,970)),
 'sword':dict(file='art/greatsword/animations/super-identity-v12.png',head_pixels=62,columns=2,
              xs=(250,780,300,805,195,750,280,800),ys=(380,386,818,814,1106,1128,1507,1518))
}

# The generated attack sheets have shorter limb proportions than the stance.
# A fixed sequence-wide correction preserves bends without fitting each pose.
COMBAT_SCALE = 1.12


def register(root):
    folder=Path(root)/'sprite-fighter/characters/jinwoo';out={}
    master=json.loads((folder/'source/art-registration.json').read_text())['sprites']['idle']
    master_head=master['head_units']*master['scale']/6
    for name,spec in SPECS.items():
        with Image.open(folder/spec['file']) as im:pixels=np.array(im)
        assert pixels.shape[2]==4 and pixels[:,:,3].min()==0
        labels,n=ndimage.label(pixels[:,:,3]>16);areas=np.bincount(labels.ravel());objects=ndimage.find_objects(labels)
        ids=sorted(range(1,n+1),key=lambda i:areas[i],reverse=True)[:8]
        assert min(areas[i] for i in ids)>30000
        ids.sort(key=lambda i:(objects[i-1][0].start+objects[i-1][0].stop)/2)
        columns=spec['columns']
        ids=[i for start in range(0,8,columns) for i in sorted(ids[start:start+columns],key=lambda i:objects[i-1][1].start)]
        frames=[]
        for j,i in enumerate(ids):
            sy,sx=objects[i-1];rect=[sx.start,sy.start,sx.stop,sy.stop]
            frames.append(dict(rect=rect,components=[i],axis=[spec['xs'][j]-sx.start,spec['ys'][j]-sy.start]))
        out[name]=dict(file=spec['file'],body_height=62.5/(master_head/spec['head_pixels']*COMBAT_SCALE),
                      combat_scale=COMBAT_SCALE,
                      head_pixels=spec['head_pixels'],reference_head_height=master_head,
                      identity_reference='art/daggers/idle.png',alpha_min=16,frames=frames)
    (folder/'source/super-motion-registration.json').write_text(json.dumps(out,indent=2))
    return out


def load(root,art):
    folder=Path(root)/'sprite-fighter/characters/jinwoo'
    for name,sheet in json.loads((folder/'source/super-motion-registration.json').read_text()).items():
        path=folder/sheet['file']
        with Image.open(path) as im:pixels=np.array(im)
        labels,_=ndimage.label(pixels[:,:,3]>sheet['alpha_min'])
        for i,frame in enumerate(sheet['frames']):
            x1,y1,x2,y2=frame['rect'];tile=pixels[y1:y2,x1:x2].copy()
            tile[:,:,3]=np.where(np.isin(labels[y1:y2,x1:x2],frame['components']),tile[:,:,3],0)
            key=f'base:dagger-super_{i}' if name=='dagger' else f'sword:super:{i}'
            art[key]=drawing(Image.fromarray(tile),frame['axis'],62.5/sheet['body_height'],str(path.relative_to(root)),frame['rect'])


def mutilate_air(text, mapping, art):
    """Retain native timing/boxes, replace the older oversized attack bodies."""
    import re
    out=[]
    for block in re.split(r'(?=^\[Begin Action )',text,flags=re.I|re.M):
        action=re.match(r'\[Begin Action (\d+)\]',block,re.I)
        if action and int(action[1]) in (3000,3010,3020):
            lines=[]
            for line in block.splitlines():
                if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
                    fields=line.split(',');key=tuple(int(x.strip()) for x in fields[:2])
                    pose=mapping.get(key,'')
                    if pose.startswith('base:dagger-cycle_'):
                        old=int(pose.rsplit('_',1)[1])
                        frame=(0,0,2,4,4,6,0,7)[old]
                        m=art[f'base:dagger-super_{frame}']
                        fields+=['']*max(0,9-len(fields))
                        fields[:2]=[str(m['group']),str(m['number'])]
                        fields[7:9]=[f"{m['scale']:.9f}"]*2
                        line=','.join(fields)
                lines.append(line)
            block='\n'.join(lines)+'\n'
        out.append(block)
    return ''.join(out)


def effects():
    """Weapon-only arcs: visible on the swing, even when it misses."""
    out={}
    for weapon in range(2):
        color=(185,65,255) if weapon==0 else (30,175,255)
        for frame in range(6):
            im=Image.new('RGBA',(640,480));d=ImageDraw.Draw(im)
            start=-130+frame*12;end=start+(120 if weapon==0 else 205)
            bounds=(45,50,600,430) if weapon==0 else (70,8,550,472)
            alpha=255-frame*30
            d.arc(bounds,start,end,fill=(*color,alpha),width=18)
            d.arc(bounds,start+8,end-8,fill=(220,245,255,alpha),width=5)
            if weapon==0:
                d.line((60,360,560,100),fill=(*color,alpha),width=10)
                d.line((60,360,560,100),fill=(245,225,255,alpha),width=3)
            glow=im.filter(ImageFilter.GaussianBlur(12));im=Image.alpha_composite(glow,im)
            out[61007,weapon*6+frame]=drawing(im,(190,240),.20,'procedural weapon slash: scripts/jinwoo_super_motion.py')
    return out


def effects_air():
    out=[]
    for weapon in range(2):
        out.append(f'[Begin Action {879820+weapon}]')
        for frame in range(6):out.append(f'61007,{weapon*6+frame},0,0,2,,A,0.20,0.20')
    return '\n'+'\n'.join(out)+'\n'


if __name__=='__main__':
    register(Path(__file__).resolve().parents[1]);print('SUPER_MOTION_REGISTERED: 8 dagger and 8 sword poses')
