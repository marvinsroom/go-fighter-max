"""Native AIR banks with authored poses and posture-specific shadow collisions."""
import re
from jinwoo_hybrid_art import FORMS,BODY_GROUPS
from jinwoo_hybrid_moves import PROFILES,BASE,TRANSFORM,SUMMON,FX,base


def assign(art):
    additions={};legacy_dagger_number=0
    for i,(key,m) in enumerate(art.items()):
        if key.startswith('base:'):group=61000
        elif key.startswith('sword:'):group=61005
        # 61007 = slash FX (super_motion); 61008 = super energy FX (super_power).
        # Legacy dagger light/heavy/aerial sheets remain archived for tooling,
        # but no live AIR action uses them. Do not pack dead legacy drawings.
        elif key.startswith('dagger:'):
            m['group']=61010;m['number']=legacy_dagger_number
            legacy_dagger_number+=1
            continue
        elif key.startswith('combat:'):group=61011
        else:group=61001+FORMS.index(key.split(':')[0])
        number=sum(1 for g,n in additions if g==group)
        m['group']=group;m['number']=number;additions[group,number]=m
    return additions


def boxes(form,posture='S'):
    cfg=PROFILES[FORMS[form-1]];body=cfg['body'];head=cfg['head']
    if posture=='C':
        return [(body[0],round(body[1]*.62),body[2],body[3]),(head[0],round(head[1]*.65),head[2],round(head[3]*.60))]
    if posture=='D':return [(-35,-16,37,0)] if form!=4 else [(-48,-18,42,0)]
    return [body,head]


def attack(form,posture='S',strength=1):
    reach=PROFILES[FORMS[form-1]]['reach']
    if posture=='C':return (-8,-28,reach,-2)
    if posture=='A':return (-8,-52,reach,8)
    return (-8,-55 if form!=4 else -38,reach,-10 if form!=4 else 2)


def build(source,mapping,art,sff):
    out=[];manifest={}
    def action(n,frames,form=0,posture='S',active=(),reach=None,hurt=True,loop=None):
        out.append(f'\n[Begin Action {n}]');manifest[str(n)]={'form':form,'frames':len(frames),'posture':posture,'active':list(active)}
        for i,(key,duration) in enumerate(frames):
            if i==loop:out.append('LoopStart')
            # Clsn stays in character units; [Size] scales it. Do not divide by
            # AIR scale or normals become stage-wide hitboxes.
            if hurt:
                h=boxes(form,posture) if form else ([(-13,-35,13,0)] if posture=='C' else [(-12,-59,12,0)])
                out.append(f'Clsn2: {len(h)}');out.extend(f'Clsn2[{j}] = '+','.join(map(str,b)) for j,b in enumerate(h))
            if i in active:
                b=reach or (attack(form,posture) if form else (0,-59,75,-3))
                out.extend(['Clsn1: 1','Clsn1[0] = '+','.join(map(str,b))])
            m=art[key];out.append(f"{m['group']},{m['number']},0,0,{duration},,,{m['scale']:.9f},{m['scale']:.9f}")
    # Bank every action that draws the player, including weapon modes and hurt
    # reactions. Keep each source duration, but replace human collision geometry.
    seen=set()
    for block in re.split(r'(?=\[Begin Action )',source,flags=re.I):
        match=re.match(r'\[Begin Action (\d+)\]',block,re.I)
        if not match:continue
        n=int(match[1])
        if n in seen:continue
        seen.add(n);rows=[];active=[];pending=False
        for line in block.splitlines():
            if re.match(r'\s*Clsn1(?:Default)?\s*:\s*[1-9]',line,re.I):pending=True
            if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
                p=[v.strip() for v in line.split(';')[0].split(',')]
                rows.append(p)
                if pending:active.append(len(rows)-1);pending=False
        if not rows or not any(tuple(map(int,p[:2])) in mapping for p in rows):continue
        native=n%10000
        for form,name in enumerate(FORMS,1):
            frames=[];posture='S'
            for i,p in enumerate(rows):
                if native in (20,21,60,65):pose=f'movement:{1+(i*6//len(rows))%6}'
                elif native in (7,10,11,12):pose='movement:7';posture='C'
                elif native in (40,41,42,43,44,45,50):pose='movement:'+str(8 if i<len(rows)//2 else 9);posture='A'
                elif 5000<=native<=5090:pose='movement:10'
                elif 5100<=native<=5190 or native in (170,175):pose='movement:11';posture='D'
                elif native in (0,5,120,121,122,130,131,132,140,141,142,180,181,182,190,191,192,193,194,195):pose='movement:0'
                elif native in (500,501):pose='combat:8'
                else:pose='combat:'+str(min(4,i*5//len(rows)))
                frames.append((name+':'+pose,int(p[4])))
            action(form*1000000+n,frames,form,posture,active)
    for form in range(5):
        prefix='base:' if not form else FORMS[form-1]+':'
        idle='base:idle' if not form else prefix+'movement:0'
        charge='combat:special:8' if not form else prefix+'combat:8'
        ritual='base:summon' if not form else charge
        action(base(form)+500,[(charge,12),(charge,12)],form,loop=0)
        action(TRANSFORM+form*100,[(ritual,18),(ritual,12),(idle,12)],form)
        for summon in range(4):action(SUMMON+summon+form*10000,[(ritual,14),(ritual,20),(idle,32)],form)
        for offset,start in ((300,12),(320,24)):
            if form and offset==300:
                poses={1:((9,8),(9,6),(2,6),(3,6),(4,8),(11,24)),
                  2:((0,4),(1,3),(2,6),(3,6),(4,6),(5,7),(6,8),(7,8)),
                  3:((9,12),(9,14),(10,8),(6,8),(7,10),(11,16)),
                  4:((0,6),(5,8),(6,14),(7,10),(4,10),(11,14))}[form]
                active={1:(2,4),2:(2,3,4,5),3:(2,),4:(2,)}[form]
                action(base(form)+offset,[(prefix+'combat:'+str(p),t) for p,t in poses],form,active=active)
                continue
            wind='combat:special:0' if not form else prefix+'combat:9'
            strike='combat:special:2' if not form else prefix+'combat:10'
            recover='combat:special:3' if not form else prefix+'combat:11'
            reach=(-115,-90,200,3) if offset==320 else (-10,-65,95,3)
            action(base(form)+offset,[(wind,start),(strike,8),(recover,28)],form,active=(1,),reach=reach)
            if not form:
                cycle=[('combat:special:'+str(i),3 if offset==320 else 2) for i in range(12)]
                frames=[(charge,32)]+cycle*(12 if offset==320 else 9)+[(charge,40),(idle,60)]
            else:
                # Sword arcs, claw flurries, deliberate axe blows and bear charges
                # have different rhythms and anticipation instead of one shared loop.
                beats={1:(9,5,3,6),2:(0,1,2,2),3:(9,10,11,10),4:(5,6,7,6)}[form]
                durations={1:(8,4,3,6),2:(2,2,2,3),3:(18,6,8,16),4:(8,7,7,8)}[form]
                cycle=[(prefix+'combat:'+str(p),t) for p,t in zip(beats,durations)]
                frames=[(charge,32)]+cycle*(16 if offset==320 else 8)+[(prefix+'combat:10',20),(prefix+'combat:11',24),(idle,60)]
            action(base(form)+offset+1,frames,form,loop=1)
        # Native source weapon arcs, claw streaks, impact and ice. Keep these
        # additive and compact, anchored at the impact rather than a second body.
        fxgroup={0:2036,1:1993,2:1989,3:2021,4:2043}[form]
        keys=sorted(k for k in sff.keys if k[0]==fxgroup)[:8]
        out.append(f'\n[Begin Action {FX+form}]')
        for group,number in keys:
            h=sff.headers[sff.keys[group,number]];scale=52/max(1,h[2])
            out.append(f'{group},{number},{(h[4]-h[2]/2)*scale:.4f},{(h[5]-h[3]/2)*scale:.4f},2,,A,{scale:.8f},{scale:.8f}')
    for form,name in enumerate(FORMS,1):
        cfg=PROFILES[name];prefix=name+':combat:'
        # Dedicated horizontal A / B / Y (and matching crouch / air) instead of
        # one shared 0-4 combat loop for every strength.
        standing={
            200:((0,1,2,3,4),(2,3)),          # light horizontal
            210:((5,6,7,4,11),(2,3)),         # medium horizontal
            220:((9,10,2,3,11),(2,3)),        # heavy horizontal
            400:((0,1,2,3,4),(2,3)),
            410:((5,6,7,4,11),(2,3)),
            420:((9,10,6,7,11),(2,3)),
            600:((0,1,2,3,4),(2,3)),
            610:((5,6,7,4,11),(2,3)),
            620:((9,10,2,3,11),(2,3)),
        }
        for offset,(poses,active) in standing.items():
            strength={200:0,210:1,220:2,400:0,410:1,420:2,600:0,610:1,620:2}[offset]
            start=cfg['startup'][strength];posture='C' if offset in (400,410,420) else 'A' if offset>=600 else 'S'
            recovery=9+strength*4
            ticks=(max(1,start-3),3,3,5,recovery)
            frames=[(prefix+str(p),t) for p,t in zip(poses,ticks)]
            action(base(form)+offset,frames,form,posture,active)
        for offset in (1000,1010):
            start=8 if offset==1010 else 12 if name=='beru' else 20
            action(base(form)+offset,[(prefix+'5',start),(prefix+'6',8),(prefix+'7',10),(prefix+'4',15)],form,'A' if offset==1010 else 'S',(1,2))
        special_prefix=name+':special:'
        special_sequences={
            1100:((0,1,2,3,4),(1,2,3)),
            1110:((9,10,6,7,11),(1,2,3)),
            1120:((5,6,2,3,11),(1,2,3)),
        }
        for offset,(poses,active) in special_sequences.items():
            ticks=(5,4,4,6,16) if offset==1100 else (7,5,5,7,18) if offset==1110 else (4,4,5,7,20)
            action(base(form)+offset,[(special_prefix+str(p),t) for p,t in zip(poses,ticks)],form,active=active)
        # Assists use the same transform combat bank/size as playable shadows.
        assist_sets=(
            (((2,4),(3,4),(4,8),(11,14)),(2,)),
            (((5,6),(6,5),(7,8),(11,14)),(1,2)),
            (((9,5),(10,5),(2,5),(3,5),(11,14)),(1,3)),
        )
        logical=attack(form)
        for variant,(poses,active) in enumerate(assist_sets):
            frames=[(special_prefix+str(p),t) for p,t in poses]
            action(870700+form-1+variant*20,frames,form,active=active,reach=logical,hurt=False)
        action(870710+form-1,[(prefix+'0',20),(prefix+'2',6),(prefix+'0',20)],form,hurt=False,loop=0)
    return '\n'.join(out)+'\n',manifest
