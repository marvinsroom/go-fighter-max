"""Lossless illustrated drawings for the imported Jinwoo and four playable shadows."""
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage
import hashlib,io,json,re,statistics
from jinwoo_motion import atlas_rects

ROOT_SCALE=1.5
WORLD=4*ROOT_SCALE
FORMS=('igris','beru','iron','tank')
HEIGHTS=(350,350,390,300)
BODY_GROUPS={0,10,20,40,60,65,120,170,180,190,200,300,400,502,600,6000,6001,6002}
# Native height intent (adult-v2): Shippuden Naruto ~166 cm, Jinwoo estimated
# 180-183 cm lean adult. Roster Naruto world height is 50; Jinwoo must stay
# taller by that cm ratio — not flattened to Naruto or an arbitrary equal band.
NARUTO_CM=166.0
JINWOO_CM=182.0
NARUTO_WORLD_HEIGHT=50.0
GAMEPLAY_HEIGHT=NARUTO_WORLD_HEIGHT*(JINWOO_CM/NARUTO_CM)


def _pose_height_ratio(key):
    """Standing combat matches lore height; crouch/jump/down keep natural foreshortening."""
    name=key.split(':',1)[1]
    if name.startswith(tuple(f'{s}_' for s in FORMS)):return None  # assist aliases follow shadows
    # Dagger attack atlases always full standing height (before 'aerial' in name).
    if key.startswith('dagger:'):return 1.0
    if key.startswith('combat:air-low:'):
        return .76 if int(key.rsplit(':',1)[1]) < 4 else .77
    if key.startswith('combat:normal-locomotion:'):
        frame=int(key.rsplit(':',1)[1])
        # 0-1 idle, 2-3 walk, 4-5 run (low), 6-7 crouch, 8-11 jump.
        if frame in (4,5):return .88
        if frame in (6,7):return .76
        if frame >= 8:return .77
        return 1.0
    if key.startswith('combat:locomotion-'):
        frame=int(key.rsplit(':',1)[1])
        return .88 if frame>=4 else 1.0
    if key.startswith('combat:reactions:'):
        frame=int(key.rsplit(':',1)[1])
        if frame in (1,7,10):return .76
        if frame in (4,5,6):return .60
        if frame in (8,9):return .77
        return 1.0
    if key.startswith('combat:'):return 1.0
    if name.startswith('run'):return .88
    if name=='crouch' or name.startswith('crouch'):return .76
    if name=='down' or name.startswith('down'):return .49
    if name.startswith('jump') or name.startswith('aerial') or ':aerial' in key or key.endswith(':aerial') or 'aerial' in name:return .77
    if key.startswith('sword:') and name.startswith('aerial'):return .77
    return 1.0


def normalize_human_scale(art, cns_scale=ROOT_SCALE, target=GAMEPLAY_HEIGHT):
    """Fit every human/sword drawing to a consistent lore height family.

    Per-pose fit (not one global multiply) so slash, dagger-cycle, walk, supers
    and sword banks all share the same standing world height. Crouch/jump/down
    keep fixed foreshortening ratios. Shadow form atlases are unchanged.
    """
    idle=art['base:idle']
    before=(idle['bounds'][3]-idle['bounds'][1])*idle['scale']*cns_scale
    fitted=[];skipped=[]
    for key,m in art.items():
        if not key.startswith(('base:','sword:','dagger:','combat:')):continue
        ratio=_pose_height_ratio(key)
        if ratio is None:skipped.append(key);continue
        # scale_body = torso head-to-boot when arms/FX would inflate opaque bbox.
        body=m.get('scale_body') or (m['bounds'][3]-m['bounds'][1])
        assert body>0,key
        m['scale']=(target*ratio)/(body*cns_scale)
        fitted.append(dict(key=key,ratio=ratio,scale=m['scale'],world=(body*m['scale']*cns_scale),
                           full_bounds=m['bounds'][3]-m['bounds'][1]))
    after=(idle['bounds'][3]-idle['bounds'][1])*idle['scale']*cns_scale
    watch=('base:idle','base:slash','base:dagger-cycle_0','base:walk_0','base:crouch','base:jump_0',
           'sword:light:0','sword:heavy:0','dagger:light:0','dagger:heavy:0',
           'base:dagger-super_0','base:mutilate_0')
    samples={e['key']:round(e['world'],2) for e in fitted if e['key'] in watch}
    return dict(target=target,cns_scale=cns_scale,before=before,after=after,fitted=len(fitted),
                skipped=skipped,naruto_cm=NARUTO_CM,jinwoo_cm=JINWOO_CM,naruto_world=NARUTO_WORLD_HEIGHT,
                height_ratio=JINWOO_CM/NARUTO_CM,samples=samples)


def unify_to_charge_silhouette(art, cns_scale=ROOT_SCALE, target=GAMEPLAY_HEIGHT):
    """Raster-match human poses to charge/idle pixel height (charge-up identity).

    Charge uses summon/idle — that is the correct Jinwoo. Walk.png and dagger-cycle
    were a different family. Crop+resample human/sword/dagger banks to one silhouette;
    crouch/down keep foreshortening ratios so down is a real crouch pose.
    """
    ref=art['base:idle']
    rb=ref['bounds'];ref_h=rb[3]-rb[1]
    ref_scale=target/(ref_h*cns_scale)
    # combat-v2 sheets were authored at one shared character scale.  Preserve
    # that relationship instead of fitting each opaque bbox independently:
    # doing so enlarged the low crouch from 141px to 184px while idle stayed
    # ~243px, producing a visibly giant/wide crouching Jinwoo.
    bank_ref=art.get('combat:normal-locomotion:0')
    bank_body=(bank_ref['bounds'][3]-bank_ref['bounds'][1]) if bank_ref else ref_h
    bank_scale_px=ref_h/max(1,bank_body)
    unified=[];skipped=[]
    for key,m in list(art.items()):
        if not key.startswith(('base:','dagger:','sword:','combat:')):continue
        if key.startswith('base:') and any(key.startswith(f'base:{s}_') for s in FORMS):
            skipped.append(key);continue
        ratio=_pose_height_ratio(key)
        if ratio is None:
            skipped.append(key);continue
        dest_h=max(8,int(round(ref_h*ratio)))
        dest_scale=(target*ratio)/(dest_h*cns_scale)
        b=m['bounds'];body=b[3]-b[1]
        assert body>0,key
        cropped=m['image'].crop(b)
        fixed_bank='combat-v2' in str(m.get('source','')).replace('\\','/')
        if fixed_bank:
            # Keep authored pixels intact and normalize with AIR scale. A single
            # bank-wide scale made shorter sword poses ~9% smaller than idle;
            # resizing aliases also caused stale-reference size divergence.
            m['scale']=(target*ratio)/(body*cns_scale)
            unified.append(key)
            continue
        scale_px=dest_h/body
        new_h=max(1,int(round(cropped.height*scale_px)))
        new_w=max(1,int(round(cropped.width*scale_px)))
        resized=cropped.resize((new_w,new_h),Image.Resampling.LANCZOS)
        ax=(m['axis'][0]-b[0])*scale_px
        ay=(m['axis'][1]-b[1])*scale_px
        ay=min(max(ay,new_h*0.88),new_h)
        ax=min(max(ax,0),new_w)
        art[key]=drawing(resized,[int(round(ax)),int(round(ay))],dest_scale,m['source'],m.get('rect'))
        unified.append(key)
    world=ref_h*ref_scale*cns_scale
    return dict(ref='base:idle',ref_h=ref_h,ref_scale=ref_scale,world=world,
                unified=len(unified),skipped=skipped,keys=unified)


# Back-compat alias for callers that still name the walk unify step.
unify_to_walk_silhouette=unify_to_charge_silhouette


def scrub_huge_body_replacements(sff, mapping, art, max_h=None):
    """Force true oversized BODY_GROUPS leftovers onto charge-family art.

    After charge unify, idle/slash/crouch are ~1k–1.5k px by design (tiny AIR scale).
    Only rewrite slots taller than unified idle — never flatten slash/lunge/kick/crouch
    additions into idle (that made every attack look like one frozen sprite).
    """
    safe=art['base:idle']
    crouch=art.get('base:crouch',safe)
    limit=max_h if max_h is not None else safe['image'].size[1]+32
    forced=0
    for h in sff.headers:
        key=h[:2]
        if h[0] not in BODY_GROUPS:continue
        pose=mapping.get(key)
        frame=art.get(pose) if pose else None
        if key[0] in (10,11,12) or (pose and 'crouch' in str(pose)):
            if frame is None or frame['image'].size[1]>limit:
                mapping[key]='base:crouch' if 'base:crouch' in art else 'base:idle'
                forced+=1
            continue
        if frame is None or frame['image'].size[1]>limit:
            mapping[key]='base:idle'
            forced+=1
        elif key not in mapping:
            mapping[key]=pose or 'base:idle'
            forced+=1
    # Standing full-canvas leftovers only — do not overwrite crouch (10,*).
    for key in ((0,0),(0,1),(0,2)):
        if key[0] in BODY_GROUPS:
            mapping[key]='base:idle';forced+=1
    return dict(forced=forced,safe_size=safe['image'].size,crouch_size=crouch['image'].size,limit=limit)


def shadow_mapping(sff):
    """Actual actor sprites only: keep sword parts and unrelated canonical summons."""
    poses={}
    poses.update({n:'igris:'+p for n,p in {0:'movement:0',1:'movement:8',2:'combat:9',3:'combat:0',4:'combat:9',5:'combat:10',6:'combat:6',7:'combat:2',8:'combat:3',9:'combat:4',10:'movement:11',51:'combat:2'}.items()})
    poses.update({n:'beru:'+p for n,p in {11:'movement:0',12:'combat:1',13:'combat:2',14:'movement:7',15:'combat:9',16:'combat:8',17:'movement:0',18:'combat:6',19:'combat:10'}.items()})
    poses.update({n:'iron:'+p for n,p in {23:'movement:0',24:'combat:5',25:'combat:6',26:'combat:7',260:'combat:10',261:'combat:3'}.items()})
    poses.update({n:'tank:'+p for n,p in {35:'movement:0',36:'combat:5',37:'combat:6'}.items()})
    return {key:poses[key[1]] for key in sff.keys if key[0] in (1000,1001) and key[1] in poses}


def drawing(im,axis,scale,source,rect=None):
    im=im.convert('RGBA');stream=io.BytesIO();im.save(stream,format='PNG')
    bounds=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();assert bounds,source
    return dict(image=im,png=stream.getvalue(),axis=axis,scale=scale,source=source,rect=rect,bounds=bounds,
                rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())


def complete_atlas_figures(source, cols=4, rows=3, alpha_min=16):
    """Extract whole figures, never rectangular grid fragments.

    Generated atlas poses often extend across an ideal cell boundary.  The 12
    actors are nevertheless separate alpha components, so retain each complete
    component and order them by its center (top-to-bottom, left-to-right).
    """
    rgba=np.asarray(source.convert('RGBA'))
    labels,count=ndimage.label(rgba[:,:,3]>alpha_min)
    objects=ndimage.find_objects(labels)
    ranked=[]
    for component,obj in enumerate(objects,1):
        if obj is None:continue
        area=int((labels[obj]==component).sum())
        if area<1000:continue
        y1,y2=obj[0].start,obj[0].stop;x1,x2=obj[1].start,obj[1].stop
        ranked.append(dict(component=component,area=area,rect=(x1,y1,x2,y2),cx=(x1+x2)/2,cy=(y1+y2)/2))
    ranked=sorted(ranked,key=lambda item:item['area'],reverse=True)[:cols*rows]
    assert len(ranked)==cols*rows,(len(ranked),source.size)
    row_height=source.height/rows
    ranked.sort(key=lambda item:(min(rows-1,int(item['cy']/row_height)),item['cx']))
    assert all(len(ranked[row*cols:(row+1)*cols])==cols for row in range(rows))
    figures=[]
    for item in ranked:
        x1,y1,x2,y2=item['rect'];tile=rgba[y1:y2,x1:x2].copy()
        tile[:,:,3]=np.where(labels[y1:y2,x1:x2]==item['component'],tile[:,:,3],0)
        figures.append((Image.fromarray(tile),item['rect']))
    return figures


def load(root):
    root=Path(root);s=root/'sprite-fighter/characters/jinwoo';art={};report={}
    old=json.loads((s/'source/art-registration.json').read_text())['sprites']
    for key,m in old.items():
        if key.startswith('sheet_'):continue
        path=root/m['file']
        # Outfit-only edits preserve the existing canvas, registration and scale.
        # Keep all legacy summon drawings on their original sources.
        with Image.open(path) as im:
            tile=im.crop(m['source_rect']) if 'source_rect' in m else im.copy()
        art['base:'+key]=drawing(tile,m['axis'],m['scale']/WORLD,str(path.relative_to(root)),m.get('source_rect'))
    for form,name in enumerate(FORMS,1):
        scales={}
        for kind in ('movement','combat','special'):
            if kind == 'special':
                path=s/'art/shadows'/f'{name}-special-v3.png'
            else:
                versioned=s/'art/shadows'/f'{name}-{kind}-v2.png'
                path=versioned if versioned.exists() else s/'art/shadows'/f'{name}-{kind}.png'
            with Image.open(path) as im:
                assert im.mode=='RGBA' and im.getchannel('A').getextrema()[0]==0,path
                w,h=im.size;figures=complete_atlas_figures(im,4,3)
                tiles=[item[0] for item in figures];rects=[item[1] for item in figures]
            if kind=='movement':
                bound=tiles[0].getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
                # Neutral stance only: raised axes, plumes and attack extensions
                # must never resize an entire movement cycle.
                # Body landmarks exclude plumes, antennae and shadow flames.
                body_pixels={'igris':245,'beru':275,'iron':275,'tank':215}[name]
                scales[kind]=HEIGHTS[form-1]/WORLD/body_pixels
            else:
                bound=tiles[4].getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
                # Shared anatomy across sheets; account only for atlas cell size.
                scales[kind]=scales['movement']*movement_cell_height/(h/3)
            bias={'igris':.61,'beru':.46,'iron':.52,'tank':.5}[name]
            for n,(tile,rect) in enumerate(zip(tiles,rects)):
                b=tile.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();assert b
                axis=(round((n%4+bias)*w/4)-rect[0],b[3])
                art[f'{name}:{kind}:{n}']=drawing(tile,axis,scales[kind],str(path.relative_to(root)),rect)
            report[f'{name}-{kind}']={'file':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scale':scales[kind],'drawings':12,'height':HEIGHTS[form-1]}
            if kind=='movement':movement_cell_height=h/3
    return art,report


def body_mapping(sff,air,art):
    candidates={};priority={};action=0;rows=[]
    blocks=re.split(r'(?=\[Begin Action )',air,flags=re.I)
    for block in blocks:
        header=re.match(r'\[Begin Action (\d+)\]',block,re.I)
        if not header:continue
        action=int(header[1]);base=action%10000
        rows=[]
        for line in block.splitlines():
            if not re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):continue
            p=[x.strip() for x in line.split(';',1)[0].split(',')];key=tuple(map(int,p[:2]))
            if key in sff.keys and key[0] in BODY_GROUPS:rows.append(key)
        for n,key in enumerate(rows):
            weight=1;pose='idle'
            # Charge-up family (idle/summon/slash/lunge/kick/crouch) — not walk.png.
            if base in (0,5,181,182,183,190,191,192,193,194,195):pose='idle';weight=8
            if base==0:pose='idle';weight=20
            elif base in (20,21):pose='summon' if (n%2) else 'idle';weight=10
            elif base in (10,11,12,40,47,52,121,131,141,151,153):pose='jump_0' if base==40 else 'crouch';weight=9
            elif base in (41,42,43,44,45,50):pose='jump_2' if n==0 else 'jump_3' if n<len(rows)//2 else 'jump_4';weight=9
            elif 5000<=base<=5090:pose='hurt';weight=10
            elif base in (170,175,5100,5110,5120,5140,5150,5160,5170):pose='down';weight=10
            elif base in (120,122,130,132,140,142):pose='idle';weight=9
            elif base in (500,501,502):pose='summon';weight=8
            # Attack remaps use charge-family slash/lunge/kick (authored AIR overrides play).
            elif 200<=base<=450 or base in (180,260,600,610,620,630,650):
                attack_poses=('slash','lunge','kick')
                pose=attack_poses[min(2,base//100-2)] if 200<=base<500 else 'slash'
                if base in (200,210,220,260):pose='slash'
                elif base in (300,310,320,350):pose='lunge'
                elif base in (400,410,420,430,440,450):pose='kick'
                elif base in (600,610,620,630,650):pose='slash'
                weight=14
            combat_pose = None
            if 5000<=base<=5090:combat_pose=f'combat:reactions:{2 if base<5050 else 3}'
            elif base in (170,175,5100,5110,5140,5150,5160,5170):combat_pose='combat:reactions:6'
            elif base==5120:combat_pose='combat:reactions:7'
            elif base in (120,122,130,132,140,142):combat_pose='combat:reactions:0'
            elif base in (40,41,42,43,44,45,47,50,52):combat_pose=f'combat:reactions:{8 + min(2, n % 3)}'
            selected=combat_pose if combat_pose in art else 'base:'+pose
            if selected not in art:selected='base:idle'
            if weight>priority.get(key,-1):candidates[key]=selected;priority[key]=weight
    for h in sff.headers:
        if h[0] not in BODY_GROUPS:continue
        if h[0] in (10,11,12):candidates.setdefault(h[:2],'base:crouch' if 'base:crouch' in art else 'base:idle')
        else:candidates.setdefault(h[:2],'base:hurt' if h[0] in (501,502) else 'base:idle')
    for i,h in enumerate(sff.headers):
        if h[10]==0 and h[:2] not in candidates and sff.headers[h[6]][:2] in candidates:
            candidates[h[:2]]=candidates[sff.headers[h[6]][:2]]
    return candidates


def write_air(source,mapping,art):
    """Rewrite body drawing scales only.

    Ikemen applies [Size] to Clsn, not the per-frame AIR scale. Inflating Clsn
    by 1/AIR_scale made sword/dagger normals hit across the whole stage.
    Keep upstream Clsn coordinates so reach stays native (~weapon length).
    """
    out=[];action=None
    for line in source.splitlines():
        header=re.match(r'\s*\[Begin Action\s+(\d+)',line,re.I)
        if header:action=int(header[1])
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            raw,mark,comment=line.partition(';');p=[x.strip() for x in raw.split(',')]
            key=tuple(map(int,p[:2]))
            if key in mapping:
                while len(p)<9:p.append('')
                scale=art[mapping[key]]['scale']
                for j in (7,8):p[j]='0' if p[j]=='0' else f'{scale:.9f}'
                line=','.join(p)+((';'+comment) if mark else '')
            if action==99950:
                # Native P1/P2 arrow helper is presentation only. Retain its
                # frames and timing while hiding the imported player labels.
                while len(p)<9:p.append('')
                p[7]=p[8]='0'
                line=','.join(p)+((';'+comment) if mark else '')
        out.append(line)
    from stable_body_scale import stabilize
    return stabilize('\n'.join(out)+'\n',mapping)[0]
