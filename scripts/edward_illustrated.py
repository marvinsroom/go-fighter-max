"""Register illustrated poses and transmuted props onto the imported AIR.

Source sprite IDs, offsets, hitboxes and frame durations remain available;
new containers use four texture pixels per original coordinate unit.
"""
from pathlib import Path
from PIL import Image,ImageOps
from isolated_sprite_atlas import extract
import json,re,math
import numpy as np

def install(folder,sprites,air):
    art=folder/'art/illustrated-v1';poses=art/'poses';poses.mkdir(exist_ok=True)
    banks={};meta={}
    for name in ('motion','combat','alchemy','reactions'):
        tiles=extract(art/(name+'.png'),4,4)
        ref=0 if name!='reactions' else 7
        unit=89/tiles[ref][0].height
        for i,(im,bounds) in enumerate(tiles):
            key=f'{name}:{i}';banks[key]=im
            im.save(poses/f'{name}-{i}.png')
            meta[key]=dict(file=f'art/illustrated-v1/poses/{name}-{i}.png',size=list(im.size),source_bounds=bounds,units_per_pixel=unit)
    # Human landmarks: pelvis X as a fraction of each isolated illustration.
    anchor={'motion':[.55,.55,.55,.55,.52,.50,.50,.54,.56,.55,.58,.56,.57,.52,.46,.56],
            'combat':[.52,.35,.34,.52,.52,.49,.36,.5,.52,.52,.55,.53,.34,.32,.51,.34],
            'alchemy':[.5,.52,.6,.6,.5,.38,.42,.54]}
    groups={}
    for s in sprites:groups.setdefault(s['key'][0],[]).append(s)
    replaced=set();registration=[]
    cutin=next(s for s in sprites if s['key']==(8525,0))
    portrait=Image.open(art/'portrait.png').convert('RGBA')
    cutin.update(image=ImageOps.fit(portrait,(2560,1920),method=Image.Resampling.LANCZOS,centering=(.5,.35)),axis=(1280,960))
    replaced.add((8525,0))
    def place(s,key,units=None,center=None):
        g,n=s['key'];im=banks[key];bank,i=key.split(':');i=int(i)
        units=units or meta[key]['units_per_pixel']
        w,h=max(1,round(im.width*units*4)),max(1,round(im.height*units*4))
        im=im.resize((w,h),Image.Resampling.LANCZOS)
        fraction=anchor.get(bank,[.5]*16)[i] if center is None else center
        original=s['image'];ox,oy=s['axis']
        # Hit-reaction alternate axes are required for throws and tumbling.
        shift=oy-original.height+5 if g>=5000 else 0
        s.update(image=im,axis=(round(w*fraction),h+round(shift*4)))
        replaced.add(s['key']);registration.append(dict(sprite=s['key'],pose=key,axis=s['axis'],size=im.size,units_per_pixel=units))
    def pick(g,n,keys):
        nums=sorted(x['key'][1] for x in groups[g]);index=nums.index(n)
        return keys[min(len(keys)-1,round(index*(len(keys)-1)/max(1,len(nums)-1)))]
    for s in sprites:
        g,n=s['key'];key=None
        if g==0:key=f'motion:{n%4}'
        elif g in (20,21):key=f'motion:{4+[0,1,1,2,3,3][n%6]}'
        elif g in (5,120,122,700,760,762,5940,5950):key='motion:0'
        elif g in (6,11,171,121,761):key='motion:8' if n==0 else 'motion:9'
        elif g in (41,47):key=pick(g,n,['motion:10','motion:11','motion:15'])
        elif g in (100,105):key=f'motion:{12+n%2}' if g==100 else 'motion:14'
        elif g==181:key=pick(g,n,['motion:0','reactions:6','reactions:7'])
        elif g in (191,195,730,731):key=pick(g,n,['alchemy:0','alchemy:1','alchemy:1','alchemy:0'])
        elif 200<=g<=250:
            if g in (200,210):seq=['combat:0','combat:2','combat:3'] if g==200 else ['combat:0','combat:1','combat:2','combat:3']
            elif g==220:seq=['combat:8','combat:9','combat:10','combat:11']
            else:seq=['combat:4','combat:5','combat:6','combat:7']
            key=pick(g,n,seq)
        elif 400<=g<=450:key=pick(g,n,['motion:8','combat:12' if g<430 else 'combat:13','motion:8'])
        elif 600<=g<=650:key=pick(g,n,['motion:11','combat:14' if g<630 else 'combat:15','motion:11'])
        elif g in (710,800,810):key=pick(g,n,['combat:0','combat:1','combat:2','combat:3'])
        elif 5000<=g<6000:
            if g in (5040,5041,5042):key='reactions:3'
            elif g==5300:key='reactions:1'
            elif g in (5052,5060,5061,5062,5070,5071,5072):key='reactions:2'
            else:key=pick(g,n,['reactions:0','reactions:1','reactions:2'])
        elif g==1000:key='alchemy:2' if n<2 else 'alchemy:3' if n<6 else 'motion:9'
        elif g==3100:
            seq=['reactions:8','reactions:9','reactions:10','reactions:11','reactions:12','reactions:13','reactions:14','reactions:15']
            key=pick(g,n,seq)
            place(s,key,units=133/banks['reactions:8'].height);continue
        if key:place(s,key)
    # Composite transmutations: retain their original coordinate footprint while
    # Ed stays the same anatomical scale throughout each construction sequence.
    props={1010:13,1020:10,1030:9,1040:8,1050:11,1060:15,3000:12,3010:14,3020:10}
    for g,items in groups.items():
        if g==1070:
            for s in items:place(s,pick(g,s['key'][1],['alchemy:3','alchemy:4','alchemy:5','alchemy:6','alchemy:7']))
            continue
        if g==3030:
            for s in items:place(s,'alchemy:3')
            continue
        if g not in props:continue
        for s in items:
            g,n=s['key'];original=s['image'];ox,oy=s['axis'];a=np.array(original)
            red=(a[:,:,0]>90)&(a[:,:,0]>a[:,:,1]*1.6)&(a[:,:,0]>a[:,:,2]*1.4)&(a[:,:,3]>0)
            has_ed=bool(red.any())
            # A detached gun/projectile sprite is registered independently.
            if not has_ed:
                prop=banks[f'alchemy:{props[g]}'];im=prop.resize((original.width*4,original.height*4),Image.Resampling.LANCZOS)
                s.update(image=im,axis=(ox*4,oy*4));replaced.add(s['key']);continue
            ex=-18;ey=0
            ed=banks['alchemy:3'];unit=meta['alchemy:3']['units_per_pixel']
            ed=ed.resize((round(ed.width*unit*4),round(ed.height*unit*4)),Image.Resampling.LANCZOS)
            edpos=(round(ex*4-ed.width*.60),round(ey*4-ed.height))
            # Existing right-hand construction bounds encode its rise/retreat.
            mask=a[:,:,3]>32;mask[:,:min(original.width,48)]=False
            ys,xs=np.where(mask)
            parts=[(ed,edpos)]
            if len(xs):
                box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
                prop=banks[f'alchemy:{props[g]}'].resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.LANCZOS)
                parts.append((prop,((box[0]-ox)*4,(box[1]-oy)*4)))
            left=min(pos[0] for im,pos in parts);top=min(pos[1] for im,pos in parts)
            right=max(pos[0]+im.width for im,pos in parts);bottom=max(pos[1]+im.height for im,pos in parts)
            result=Image.new('RGBA',(right-left,bottom-top))
            for im,pos in parts:result.alpha_composite(im,(pos[0]-left,pos[1]-top))
            s.update(image=result,axis=(-left,-top));replaced.add(s['key'])
            registration.append(dict(sprite=s['key'],pose='alchemy:3 + prop:'+str(props[g]),axis=s['axis'],size=result.size))
    lines=[];frame_count=0;clamped=0
    for line in air.splitlines():
        m=re.match(r'^(\s*)(-?\d+)\s*,\s*(-?\d+)\s*,',line)
        if m:
            frame_count+=1;key=(int(m[2]),int(m[3]))
            if key in replaced:
                fields=line.split(';',1)[0].split(',')
                while len(fields)<9:fields.append('')
                for i in (7,8):fields[i]=str((float(fields[i].strip()) if fields[i].strip() else 1)/4)
                line=','.join(fields)
        # Source barrage hitboxes extended beyond the visible arena. Bound
        # attack reach without moving any contact inside the playable viewport.
        m=re.match(r'(\s*Clsn1\[\d+\]\s*=\s*)(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)',line,re.I)
        if m:
            values=list(map(int,m.groups()[1:]));bounded=[max(-320,min(320,values[0])),values[1],max(-320,min(320,values[2])),values[3]]
            if bounded!=values:clamped+=1;line=m[1]+','.join(map(str,bounded))
        lines.append(line)
    (folder/'illustrated-build.json').write_text(json.dumps(dict(drawings=64,mapped_sprites=len(replaced),frame_references=frame_count,bounded_attack_boxes=clamped,poses=meta,registration=registration),indent=2))
    return sprites,'\n'.join(lines)+'\n'


def modern_helpers(source):
    panel='''[Statedef 8520]
type=A
physics=N
anim=8520
velset=0,0
[State 8520, Hide carrier]
type=AssertSpecial
trigger1=1
flag=invisible
flag2=noshadow
[State 8520, Illustrated cut-in]
type=Explod
trigger1=!Time
anim=8525
ID=208525
postype=left
pos=160,120
scale=.5,.5
sprpriority=10
ownpal=1
removetime=40
supermovetime=-1
pausemovetime=-1
[State 8520, Gentle entrance and exit]
type=ModifyExplod
trigger1=NumExplod(208525)
ID=208525
postype=left
pos=160+ifelse(Time<6,(6-Time)*3,0),120
trans=addalpha
alpha=ifelse(Time<6,Time*42,ifelse(Time>32,(40-Time)*32,256)),0
[State 8520, End]
type=DestroySelf
trigger1=Time>=40

'''
    pattern=r'\[StateDef 8520\].*?(?=\[StateDef 8530\]|\[StateDef 8600\])'
    # The following finish helper is 8600 in the upstream release.
    result,n=re.subn(pattern,panel,source,flags=re.S|re.I)
    assert n==1,'Ultimate helper boundary changed'
    return result
