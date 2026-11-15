"""Pack authored animation cells losslessly; keep original sheets unmodified."""
from PIL import Image
import hashlib,io,statistics,struct

SHADOWS=('igris','beru','iron','tank')
HEIGHTS={'walk':375,'dagger-cycle':375,'jump':375,'igris':350,'beru':350,'iron':390,'tank':300}

def gutter(profile,ideal,radius):
    """Find an empty gutter near a nominal grid boundary, without changing art."""
    start=max(1,round(ideal-radius));end=min(len(profile)-1,round(ideal+radius))
    empty=[i for i in range(start,end) if profile[i]==0]
    if empty:return min(empty,key=lambda i:abs(i-ideal))
    return min(range(start,end),key=lambda i:(profile[i],abs(i-ideal)))

def atlas_rects(source,cols,rows):
    w,h=source.size;mask=source.getchannel('A').point(lambda a:255 if a>48 else 0)
    yp=[mask.crop((0,y,w,y+1)).getbbox() is not None for y in range(h)]
    ycuts=[0]+[gutter(yp,i*h/rows,h/rows*.18) for i in range(1,rows)]+[h]
    rects=[]
    for row in range(rows):
        strip=mask.crop((0,ycuts[row],w,ycuts[row+1]))
        xp=[strip.crop((x,0,x+1,strip.height)).getbbox() is not None for x in range(w)]
        xcuts=[0]+[gutter(xp,i*w/cols,w/cols*.22) for i in range(1,cols)]+[w]
        assert all(a<b for a,b in zip(xcuts,xcuts[1:]))
        rects.extend((xcuts[i],ycuts[row],xcuts[i+1],ycuts[row+1]) for i in range(cols))
    return rects

def load(assets):
    sheets={}
    for sheet_index,(name,height) in enumerate(HEIGHTS.items()):
        filename=f'{name}.png' if name in ('walk','jump') else f'{name}-layout.png'
        path=assets.source/'art/v2'/filename
        # An unused source group preserves the exact original sheet PNG bytes.
        assets.png('sheet_'+name,path,height,sheet_index,90)
        with Image.open(path) as source:
            assert source.mode=='RGBA' and source.getchannel('A').getextrema()[0]==0
            cols,rows=(4,2) if name in ('walk','dagger-cycle','jump') else (2,2)
            w,h=source.size
            rects=atlas_rects(source,cols,rows)
            cells=[source.crop(rect) for rect in rects]
        bounds=[cell.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox() for cell in cells]
        assert all(bounds),(name,bounds)
        # Shared axes and scale across the whole cycle preserve drawn weight
        # shifts. Per-frame auto fitting would make heads/feet pop in size.
        ground=round(statistics.median(b[3] for b in bounds))
        body_height=statistics.median(b[3]-b[1] for b in bounds)
        if name=='jump':ground=bounds[7][3];body_height=bounds[7][3]-bounds[7][1]
        elif name in SHADOWS:ground=max(b[3] for b in bounds)
        scale=height/body_height
        for i,(cell,b) in enumerate(zip(cells,bounds)):
            cw,ch=cell.size
            axis_x=round((i%cols+.5)*w/cols)-rects[i][0]
            axis_y=ground if name=='jump' else b[3]
            key=f'{name}_{i}';stream=io.BytesIO();cell.save(stream,format='PNG');raw=stream.getvalue()
            offset=len(assets.payload);block=struct.pack('<I',cw*ch*4)+raw;assets.payload.extend(block)
            group=50 if sheet_index<3 else 51
            number=20+sheet_index*8+i
            assets.headers.append(struct.pack('<HHHHhhHBBIIHH',group,number,cw,ch,axis_x,axis_y,0,12,32,offset,len(block),0,0))
            assets.meta[key]={'group':group,'number':number,'axis':[axis_x,axis_y],'bounds':b,'scale':scale,
                'file':str(path.relative_to(assets.root)),'sha256':hashlib.sha256(raw).hexdigest(),
                'source_rect':list(rects[i]),
                'rgba_sha256':hashlib.sha256(cell.tobytes()).hexdigest(),'source_sheet':'sheet_'+name}
        sheets[name]={'frames':len(cells),'ground_axis':ground,'scale':scale,'source':str(path.relative_to(assets.root))}
    return sheets

def normal(assets,number,start,active,recovery,kind,guard,pose,box):
    if kind=='C':
        frames=[('crouch',2),('crouch',start-2),(pose,active),('crouch',recovery)]
        assets.action(number,frames,active=(2,),kind=kind,attack=box)
    elif kind=='A':
        frames=[('jump_3',max(1,start-3)),('dagger-cycle_2',3),(pose,active),('dagger-cycle_6',3),('jump_4',recovery-3)]
        assets.action(number,frames,active=(2,),kind=kind,attack=box)
    elif pose=='kick':
        assets.action(number,[('dagger-cycle_0',3),('dagger-cycle_1',start-3),('kick',active),
            ('dagger-cycle_6',4),('dagger-cycle_7',recovery-4)],active=(2,),attack=box)
    else:
        a=max(1,active//2)
        assets.action(number,[('dagger-cycle_0',2),('dagger-cycle_1',2),('dagger-cycle_2',start-4),
            ('dagger-cycle_3',a),('dagger-cycle_4',active-a),('dagger-cycle_5',3),
            ('dagger-cycle_6',4),('dagger-cycle_7',recovery-7)],active=(3,4),attack=box)

def shadow_actions(assets):
    for i,name in enumerate(SHADOWS):
        # Visible anticipation -> strike -> recovery, with a single hit per cast.
        box=(-90,-320,250,-65) if name!='tank' else (-105,-225,260,-20)
        assets.action(6500+i,[(f'{name}_0',4),(f'{name}_1',4),(f'{name}_2',8),(f'{name}_3',14)],
            active=(2,),attack=box,hurt=False)
        assets.action(6600+i,[(f'{name}_0',20),(f'{name}_1',6),(f'{name}_0',20)],hurt=False)
        assets.action(6700+i,[(f'{name}_0',4),(f'{name}_1',4),(f'{name}_2',10),(f'{name}_3',14)],hurt=False)
