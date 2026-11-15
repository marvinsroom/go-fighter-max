"""Map illustrated pose atlases onto Cid's original sprite IDs and AIR timing.

Source archives and generated sheets stay unchanged. Only the derived runtime
container, per-drawing scale, display size and effect anchors are adapted.
"""
from pathlib import Path
import hashlib,io,json,re,statistics,struct,os,math
from PIL import Image,ImageOps
from jinwoo_motion import atlas_rects
import numpy as np
from scipy import ndimage

SHEETS={'movement-a':(0,1,2,3),'movement-b':(0,1),'combat':(2,5),'cinematic':(4,5,7,8)}
SIZE=1.65


def cells(root):
    folder=root/'sprite-fighter/characters/cid/art/illustrated-v1';result={};sources={}
    calibration=json.loads((folder.parent/'anatomy-v3.json').read_text())
    sheets=dict(SHEETS)
    if (folder.parent/'taunt-v1/taunt.png').exists():sheets['taunt']=tuple(range(8))
    for name,standing in sheets.items():
        path=folder/(name+'.png') if name!='taunt' else folder.parent/'taunt-v1/taunt.png'
        raw=path.read_bytes();rows=2 if name=='taunt' else 3
        with Image.open(path) as im:
            assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0 and im.getchannel('A').getextrema()[1]>=250
            w,h=im.size;rects=atlas_rects(im,4,rows);tiles=[im.crop(r) for r in rects]
        # A few gutter crops contain isolated pixels from an adjacent pose.
        # Measure the connected fighter, not those fragments. Original RGBA
        # tiles remain untouched; this corrects only scale/ground registration.
        bounds=[]
        for tile in tiles:
            labels,_=ndimage.label(np.array(tile.getchannel('A'))>48)
            areas=np.bincount(labels.ravel());areas[0]=0
            sy,sx=ndimage.find_objects(labels)[int(areas.argmax())-1]
            bounds.append((sx.start,sy.start,sx.stop,sy.stop))
        assert all(bounds),(name,'empty cell')
        reference=statistics.median(bounds[j][3]-bounds[j][1] for j in standing)
        # Calibrate anatomy using head landmarks, rather than a pose's full
        # silhouette (which also includes raised swords and extended coattails).
        scale=55/reference
        for j,(tile,rect,bound) in enumerate(zip(tiles,rects,bounds)):
            key=f'{name}:{j}';stream=io.BytesIO();tile.save(stream,format='PNG')
            segment=calibration['landmarks'][key]
            head_length=math.hypot(segment[2]-segment[0],segment[3]-segment[1])
            target=calibration['unhooded_head_logical'] if key in calibration['unhooded'] else calibration['hood_head_logical']
            scale=target/head_length
            if name=='taunt':scale=55/reference
            axis=(round((j%4+.5)*w/4)-rect[0],bound[3])
            result[key]={'image':tile,'png':stream.getvalue(),'axis':axis,'scale':scale,
                         'source':str(path.relative_to(root)),'rect':rect,'bounds':bound,
                         'head_landmarks':segment,'head_length':head_length,'logical_head_size':target,
                         'rgba_sha256':hashlib.sha256(tile.tobytes()).hexdigest()}
        sources[name]={'file':str(path.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest(),
                       'size':[w,h],'standing_height':reference,'calibration':'Per-pose head landmarks; fixed skeleton scale for taunt','cells':len(tiles)}
    from cid_proportions import calibrate
    calibrate(result)
    for source in sources.values():source['calibration']='Fixed sequence scale and connected-figure ground registration; upright cinematic references match idle height'
    return result,sources


def pose(group,n):
    a=lambda i:f'movement-a:{i}'
    b=lambda i:f'movement-b:{i}'
    c=lambda i:f'combat:{i}'
    d=lambda i:f'cinematic:{i}'
    # Keep the whole stride on one authored skeleton. The final two frames
    # from movement-b had longer legs despite matching head size. Two passing
    # poses hold for an extra beat, retaining the original ten-frame timing.
    if group==69:return a((4,5,6,6,7,8,9,10,10,11)[n])
    if group==40:return {0:b(10),1:b(11),10:b(11),2:c(0),3:c(0)}.get(n,b(10))
    if group in (120,121,122):return b(7) if group==121 else d(5)
    if group==6:return b(6) if n==0 else c(1)
    if group==19 and n!=24:return d(8+(n-19)%3)
    if 5000<=group<=5300:
        if group in (5040,5041,5042):return d(2 if n%2==0 else 3)
        if group>=5060:return d(1)
        return [c(10),c(11),d(0),d(1)][n%4]
    if group==1:
        return {0:a(0),1:d(9),2:d(6),4:c(9),7:c(0),8:d(10),9:c(4),10:c(7),15:c(9)}.get(n,a(0))
    if group!=0 or n in (144,895,896):return None
    if 32<=n<=35:return a(n-32)
    if 20<=n<=25:return a((n-20)%4)
    if 40<=n<=43:return a(n-40)
    mapping={0:a(0),1:a(1),2:a(2),3:a(3),4:d(10),5:c(6),6:c(7),7:c(0),8:d(9),
      9:d(5),10:d(4),11:d(5),12:c(9),13:d(9),14:c(6),15:c(7),16:d(6),17:c(8),18:c(9),19:b(7),
      26:b(6),27:b(7),28:b(7),29:b(8),30:b(8),31:c(0),39:d(5),44:d(8),45:d(6),46:c(6),47:c(9),
      48:c(2),49:c(3),50:c(6),51:c(7),52:c(4),53:c(8),54:c(9),55:c(5),56:c(6),57:c(8),58:c(9),
      59:c(7),60:b(2),61:c(6),62:c(6),63:c(7),64:d(5),65:a(0),66:a(1),67:a(2),68:a(3),69:a(2),70:a(1),
      71:b(2),72:c(8),88:d(9),888:d(9),889:d(9),890:d(10),891:d(10),893:c(8),894:c(9),897:d(10),
      898:d(11),899:d(11),145:d(8)}
    return mapping.get(n,a(0))


def install(root,out):
    root=Path(root);out=Path(out);source=root/'sprite-fighter/characters/cid';up=source/'source/upstream/.Cid'
    art,sheets=cells(root)
    portrait=source/'art/illustrated-v1/portrait.png'
    if portrait.exists():
        for n,size,axis in [(0,(224,200),(16,0)),(1,(960,1120),(0,0))]:
            with Image.open(portrait) as im:
                tile=Image.new('RGBA',size);fit=ImageOps.contain(im.convert('RGBA'),size,Image.Resampling.LANCZOS)
                tile.alpha_composite(fit,((size[0]-fit.width)//2,0))
            stream=io.BytesIO();tile.save(stream,format='PNG')
            art[f'portrait:{n}']={'image':tile,'png':stream.getvalue(),'axis':axis,'scale':.125,
                'source':str(portrait.relative_to(root)),'rect':(0,0,*size),
                'rgba_sha256':hashlib.sha256(tile.tobytes()).hexdigest()}
    archive=bytearray((up/'Cid.sff').read_bytes());header,count=struct.unpack_from('<II',archive,36)
    lo,ls,to,ts=struct.unpack_from('<IIII',archive,52);assert ts==0 and lo+ls==len(archive)
    descriptors=[list(struct.unpack_from('<HHHHhhHBBIIHH',archive,header+i*28)) for i in range(count)]
    first_pose={};replaced={};sprite_meta={}
    for i,h in enumerate(descriptors):
        group,n=h[:2];key=f'portrait:{n}' if group==9000 and n in (0,1) and portrait.exists() else pose(group,n)
        if key is None and h[10]==0 and h[6] in replaced:key=replaced[h[6]]
        if key is None:continue
        frame=art[key];w,hh=frame['image'].size
        if key in first_pose:offset=length=0;linked=first_pose[key]
        else:
            block=struct.pack('<I',w*hh*4)+frame['png'];offset=len(archive)-lo;length=len(block);archive.extend(block)
            linked=0;first_pose[key]=i
        new=[group,n,w,hh,*frame['axis'],linked,12,32,offset,length,0,0]
        struct.pack_into('<HHHHhhHBBIIHH',archive,header+i*28,*new)
        replaced[i]=key
        sprite_meta.setdefault(f'{group},{n}',dict(pose=key,scale=frame['scale'],axis=frame['axis'],source=frame['source'],rect=frame['rect'],rgba_sha256=frame['rgba_sha256']))
    # Extra taunt drawings extend the contiguous sprite header table. Offsets
    # inside lData stay relative, so original compressed resources are intact.
    extra=[]
    for n in range(8) if 'taunt:0' in art else ():
        key=f'taunt:{n}';frame=art[key];w,hh=frame['image'].size
        block=struct.pack('<I',w*hh*4)+frame['png'];offset=len(archive)-lo;archive.extend(block)
        extra.append(struct.pack('<HHHHhhHBBIIHH',7900,n,w,hh,*frame['axis'],0,12,32,offset,len(block),0,0))
        sprite_meta[f'7900,{n}']=dict(pose=key,scale=frame['scale'],axis=frame['axis'],source=frame['source'],rect=frame['rect'],rgba_sha256=frame['rgba_sha256'])
    if extra:
        archive[lo:lo]=b''.join(extra);lo+=28*len(extra)
        struct.pack_into('<I',archive,40,count+len(extra))
    archive[12:16]=bytes((0,0,1,2))
    struct.pack_into('<IIII',archive,52,lo,len(archive)-lo,len(archive),0)
    (out/'Cid.sff').write_bytes(archive)
    lines=(up/'Cid.air').read_text(encoding='utf-8-sig',errors='replace').splitlines();changed=0
    for i,line in enumerate(lines):
        if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
        content,mark,comment=line.partition(';');parts=[x.strip() for x in content.split(',')]
        key=','.join(parts[:2]);meta=sprite_meta.get(key)
        if not meta:continue
        while len(parts)<9:parts.append('')
        for j in (7,8):
            original=float(parts[j]) if parts[j] else 1
            # Imported squash/stretch compensated for the old pixel drawings.
            # New drawings already carry the pose; retain only deliberate hides.
            if original!=0:original=1
            parts[j]=f'{meta["scale"]*original:.9f}'
        lines[i]=','.join(parts)+((';'+comment) if mark else '');changed+=1
    from stable_body_scale import stabilize
    stable_air,scale_blends=stabilize('\n'.join(lines)+'\n',{tuple(map(int,k.split(','))) for k in sprite_meta})
    (out/'Cid.air').write_text(stable_air,encoding='utf-8')
    cns=(up/'Cid.cns').read_text(encoding='cp1252')
    cns=re.sub(r'(?im)^(xscale|yscale)\s*=\s*1\s*$',lambda m:m[1]+f' = {SIZE}',cns,count=2)
    (out/'Cid.cns').write_text(cns,encoding='utf-8')
    skills=(up/'Normal Skill.cns').read_text(encoding='cp1252')
    before,block=skills.split('[Statedef 999999]',1)
    block=block.replace('value = 1','value = root,const(size.xscale)',1)
    (out/'Normal Skill.cns').write_text(before+'[Statedef 999999]'+block,encoding='utf-8')
    from cid_scale import install as install_scale
    scale_adapters=install_scale(up,out)
    # A comparison definition reads the untouched native resources directly.
    definition=(up/'.Cid.def').read_text(encoding='utf-8-sig')
    for filename in [p.name for p in up.iterdir() if p.suffix.lower() in {'.sff','.snd','.cmd','.air','.cns'}]:
        relative=os.path.relpath(up/filename,out).replace('\\','/')
        definition=re.sub(r'(?m)(=\s*)'+re.escape(filename)+r'\s*$',lambda m:m[1]+relative,definition)
    (out/'cid_original.def').write_text(definition,encoding='utf-8')
    if portrait.exists():
        live=(out/'cid_shadow.def').read_text(encoding='utf-8')
        live=live.replace('[Files]','portraitscale = 0.125\n\n[Files]')
        (out/'cid_shadow.def').write_text(live,encoding='utf-8')
    taunt=None
    if extra:
        from cid_taunt import install as install_taunt
        taunt=install_taunt(out,art)
    report={'revision':6,'status':'Built; native validation pending','display_size_scale':SIZE,'scale_adapters':scale_adapters,'taunt':taunt,'stable_body_scale':scale_blends,
      'walking':{'sheet':'movement-a','pose_order':[4,5,6,6,7,8,9,10,10,11],'frames':10,'distinct_drawings':8,'ticks_per_frame':8,'forward_action':20,'backward_action':21},
      'anatomy_calibration':'scripts/cid_proportions.py',
      'pose_anatomy':{key:{k:v for k,v in frame.items() if k in ('head_landmarks','head_length','logical_head_size','scale','previous_scale','calibration')} for key,frame in art.items() if not key.startswith('portrait:')},
      'original_logical_standing_height':55,'viewport_height_estimate':55*SIZE*4,'sheets':sheets,'drawings':48+len(extra),'portraits':2 if portrait.exists() else 0,
      'replaced_sprite_keys':sprite_meta,'replaced_sprite_headers':len(replaced)+len(extra),'rewritten_air_rows':changed,
      'preserved':'Original state timing, input routes, voices, damage and cinematic event timing; original source archive retained',
      'original_sff_sha256':hashlib.sha256((up/'Cid.sff').read_bytes()).hexdigest(),
      'runtime_sff_sha256':hashlib.sha256(archive).hexdigest()}
    (source/'illustrated-build-report.json').write_text(json.dumps(report,indent=2))
    if (source/'art/summons-v1/alpha.png').exists() and (source/'art/summons-v1/beta.png').exists():
        from cid_summons import install as install_summons
        summons=install_summons(root,out)
        report['summons']={'build':'summon-build.json','drawings':16,'sprite_headers':17,'meter_cost':1000}
        report['runtime_sff_sha256']=hashlib.sha256((out/'Cid.sff').read_bytes()).hexdigest()
        (source/'illustrated-build-report.json').write_text(json.dumps(report,indent=2))
    if (source/'art/garden-ultimate-v1/gamma-delta-epsilon.png').exists() and (source/'art/garden-ultimate-v1/zeta-eta.png').exists():
        from cid_garden import install as install_garden
        garden=install_garden(root,out)
        report['garden']={'build':'garden-build.json','drawings':20,'sprite_headers':garden['sprite_headers'],'air_rows':garden['air_rows']}
        report['runtime_sff_sha256']=hashlib.sha256((out/'Cid.sff').read_bytes()).hexdigest()
        (source/'illustrated-build-report.json').write_text(json.dumps(report,indent=2))
        summons['runtime']={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in summons['runtime']}
        (source/'summon-build.json').write_text(json.dumps(summons,indent=2))
    print('CID_ILLUSTRATED_BUILT',len(art)-(2 if portrait.exists() else 0),'drawings;',len(replaced)+len(extra),'sprite headers;',changed,'AIR rows')
    return report
