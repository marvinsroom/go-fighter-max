"""Distinct mechanics and cinematic blocking for the four paired Chappelle kits.

Extends the pair composer; frozen v1 components and original character art stay
reproducible. New props are code-native effects using the existing visual style.
"""
import math,re,struct

MOVES={
 'Prince':('Ankle-Breaker','Purple Skyhook'),
 'Rick James':('Couch Surfboard','Platform Pogo'),
 'Tyrone Biggums':('Pocket Sand Panic','Wrong Way!'),
 'Negan':("Lucille’s Verdict",'Dead Weight'),
}


def effects(a,form,label):
    def sand(x,y):
        # Irregular, transparent cone; dust flecks fade toward its wide edge.
        nx=x/255;ny=abs(y-63.5)/64
        if ny>.2+.8*nx or (x*17+y*31)%23>15:return (0,0,0,0)
        return (220,180+(x+y)%45,110,int(210*(1-nx*.65)))
    def crack(x,y):
        near=min(abs(y-42-12*math.sin(x*.12)),abs(y-48+18*math.sin(x*.08)))
        return (235,180,110,int(230*max(0,1-near/4))) if 8<x<312 else (0,0,0,0)
    def bill(x,y):
        if not (3<x<93 and 3<y<45):return (0,0,0,0)
        edge=x<8 or x>88 or y<8 or y>40
        return (175,220,150,245) if edge else (35,110,65,245) if abs(x-48)<13 else (75,155,85,245)
    for number,w,h,fn,axis in [(30,256,128,sand,(32,64)),(31,320,96,crack,(160,80)),(32,96,48,bill,(48,24))]:
        a.raw(number,w,h,fn,axis)
        fields=list(struct.unpack('<HHHHhhHBBIIHH',a.headers[-1]));fields[0]=7000+form
        a.headers[-1]=struct.pack('<HHHHhhHBBIIHH',*fields)
    for offset,sprite,scale,box in [(20,0,.64,(-28,-28,28,28)),(21,2,.9,None),
                                   (22,30,1,(-30,-65,190,55)),(23,31,1.6,None),(24,3,1,None),(25,32,1,None)]:
        a.air.append(f'\n[Begin Action {20000+form*1000+offset}]')
        if box:a.air.extend(['Clsn1: 1','Clsn1[0]='+','.join(map(str,box))])
        a.air.append(f'{7000+form},{sprite},0,0,-1,,,{scale},{scale}')


def animations(a,form,label):
    shift=form*10000;prefix='alt_' if form else ''
    def action(n,frames,active=(),kind='S',box=(0,-320,270,-30)):
        a.action(n+shift,[(prefix+key,duration) for key,duration in frames],active=active,kind=kind,attack=box)
    if label=='Prince':
        action(1500,[('idle',8),('crouch',6),('palm',8),('walk_b',8),('idle',18)])
        action(1510,[('special',12),('palm',6),('special',22)],kind='A')
    elif label=='Rick James':
        action(1500,[('idle',10),('kick',32),('walk_b',8),('idle',12)],active=(1,),box=(0,-180,300,0))
        # Ride the couch visually while keeping the grounded engine origin.
        start=len(a.air)
        for i in range(len(a.air)-1,-1,-1):
            if a.air[i].startswith('[Begin Action') or a.air[i].startswith('\n[Begin Action'):
                start=i;break
        drawing=0
        for i in range(start,len(a.air)):
            if re.match(r'5[01],',a.air[i]):
                if drawing==1:
                    p=a.air[i].split(',');p[3]='-130';a.air[i]=','.join(p)
                drawing+=1
        action(1510,[('crouch',6),('kick',-1)],active=(1,),kind='A',box=(-45,-200,135,20))
        action(1511,[('crouch',10),('idle',8)])
        action(1512,[('special',8),('kick',8)],kind='A')
    elif label=='Tyrone Biggums':
        action(1500,[('crouch',12),('palm',4),('walk_b',18),('idle',12)])
        action(1510,[('walk_a',12),('walk_b',12),('palm',8),('special',12)],active=(2,),kind='A',box=(0,-300,260,-30))
    else:
        action(1500,[('special',-1)])
        action(1501,[('special',8),('palm',6),('idle',30)],active=(1,),box=(0,-365,380,-30))
        action(1510,[('special',10),('palm',16),('special',-1)],active=(1,),kind='A',box=(0,-340,310,20))
        action(1511,[('crouch',20),('idle',20)])


def command_routes(data):
    definitions='''
[Command]
name="signature"
command=x+c
time=1
[Command]
name="holdskill"
command=/x
time=1
[Command]
name="holdheavy"
command=/c
time=1
'''
    routes=''
    for form,info in enumerate(data):
        for air in [False,True]:
            routes+=f'''
[State -1, {MOVES[info['label']][int(air)]}]
type=ChangeState
triggerall=roundstate=2
triggerall=var(45)={form}
triggerall=ctrl
triggerall=statetype{'=' if air else '!='}A
trigger1=command="{'skill' if air else 'signature'}"
value={form*10000+(1510 if air else 1500)}
ctrl=0
'''
    return definitions,routes


def states(form,label):
    shift=form*10000;fx=20000+form*1000;parts=[]
    def state(n,anim=None,kind='S',move='A',**params):
        parts.append(f'\n[Statedef {n+shift}]\ntype={kind}\nmovetype={move}\nphysics=N\nctrl=0\n')
        if anim is not None:parts.append(f'anim={anim+shift}\n')
        for k,v in params.items():parts.append(f'{k}={v}\n')
    def ctl(n,label,typ,triggers='1',**params):
        parts.append(f'\n[State {n+shift}, {label}]\ntype={typ}\n')
        for t in triggers if isinstance(triggers,list) else [triggers]:parts.append(f'trigger1={t}\n')
        for k,v in params.items():parts.append(f'{k.replace("__",".")}={v}\n')
    def end(n,time,air=False):ctl(n,'Recover','ChangeState',f'time>={time}',value=50+shift if air else shift,ctrl=1)
    def hit(n,t,damage,air=False,guard='MA',boxfall=True,**kw):
        params=dict(attr=('A' if air else 'S')+',SA',damage=f'{damage},3',guardflag=guard,hitflag='MAF',
            pausetime='5,8',sparkno=2,sparkxy='-10,-150',hitsound='S0,1',guardsound='S0,2',
            ground__type='High',ground__hittime=24,ground__velocity='-5,-8',air__velocity='-5,-8',
            fall=int(boxfall),getpower='35,10',givepower='20,10')
        params.update(kw);ctl(n,'Signature contact','HitDef',f'time={t}',**params)
    def landing(n,target=52):
        ctl(n,'Gravity','VelAdd',y=.55)
        ctl(n,'Landing','ChangeState',['vel y>0','pos y>=0'],value=target+shift)
    def ball(n,t,helper):
        ctl(n,'Authored bouncing ball','Helper',f'time={t}',helpertype='normal',name='"Royal ricochet"',ID=helper+shift,
            stateno=helper+shift,pos='100,-170',postype='p1',ownpal=1,keyctrl=0)
    if label=='Prince':
        state(1500,1500,velset='0,0');ball(1500,14,7600)
        ctl(1500,'Crossover retreat','VelSet','time=[8,16]',x=-3)
        ctl(1500,'Chase the bounce','VelSet','time=[17,28]',x=4)
        ctl(1500,'Plant feet','VelSet','time>=29',x=0);end(1500,47)
        state(1510,1510,kind='A');ctl(1510,'Hang for skyhook','VelSet','time=0',x=1,y=-2);ball(1510,12,7601)
        landing(1510);end(1510,39,True)
        for n,air in [(7600,False),(7601,True)]:
            state(n,kind='A',velset='7,-6' if not air else '8,4')
            ctl(n,'Ball drawing','ChangeAnim','time=0',value=fx+20)
            ctl(n,'Bounce counter','VarSet','time=0',**{'var(0)':0})
            hit(n,0,95 if not air else 100,air,guard='H' if air else 'MA',attr=('A' if air else 'S')+',SP')
            ctl(n,'Ball gravity','VelAdd',y=.5)
            if not air:
                ctl(n,'Count floor bounce','VarAdd',['vel y>0','pos y>=-30'],**{'var(0)':1})
                ctl(n,'Bounce off court','VelSet',['vel y>0','pos y>=-30'],y=-8)
                ctl(n,'Expire after two bounces','DestroySelf','var(0)>=3')
            else:ctl(n,'Skyhook floor','DestroySelf',['vel y>0','pos y>=-25'])
            ctl(n,'Ball hit cleanup','DestroySelf','movecontact || time>=110 || parent,stateno=3900')
    elif label=='Rick James':
        state(1500,1500,velset='0,0')
        ctl(1500,'Surf the couch','VelSet','time=[10,41]',x=7)
        ctl(1500,'Stop the couch','VelSet','time>=42',x=0)
        ctl(1500,'Moving couch','Explod','time=10',anim=fx+21,ID=6901,postype='p1',pos='0,0',bindtime=-1,removetime=32,sprpriority=-1,ownpal=1)
        hit(1500,10,105,guard='L');end(1500,61)
        state(1510,1510,kind='A');ctl(1510,'Platform dive','VelSet','time=6',x=3,y=14)
        hit(1510,6,95,True,guard='H');ctl(1510,'Pogo off confirmed hit','ChangeState','movehit',value=1512+shift)
        landing(1510,1511)
        state(1512,1512,kind='A');ctl(1512,'Spring upward','VelSet','time=0',x=-2,y=-10);landing(1512);end(1512,15,True)
        state(1511,1511,velset='0,0');ctl(1511,'Floor','PosSet',y=0);end(1511,17)
    elif label=='Tyrone Biggums':
        state(1500,1500,velset='0,0')
        ctl(1500,'Pocket sand','Projectile','time=12',projid=1500+shift,projanim=fx+22,projhitanim=-1,projremanim=-1,
            projremove=1,projremovetime=24,velocity='7,0',offset='90,-190',attr='S,SP',damage='55,2',
            guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=42,
            ground__velocity=-2,air__velocity='-3,-5',fall=0,getpower='35,10',givepower='20,10',hitsound='S0,0',
            palfx__time=24,palfx__add='45,30,0',palfx__mul='256,230,190')
        ctl(1500,'Panic retreat','VelSet','time=[14,31]',x=-5)
        ctl(1500,'Stop retreat','VelSet','time>=32',x=0);end(1500,45)
        state(1510,1510,kind='A')
        for t,x,y in [(0,6,-3),(12,-7,-2),(24,8,6)]:ctl(1510,'Wrong way air dash','VelSet',f'time={t}',x=x,y=y)
        ctl(1510,'Scramble afterimages','AfterImage','time=0',time=33,length=8,timegap=2,framegap=2,trans='add')
        hit(1510,24,90,True,guard='H');landing(1510);end(1510,43,True)
    else:
        state(1500,1500,velset='0,0')
        ctl(1500,'Store charge','VarSet',**{'var(50)':'min(time,48)'})
        ctl(1500,'Bat charge glint','Explod','time%8=0',anim=fx+24,ID=6902,pos='150,-230',scale='.3+time*.015,.3+time*.015',
            removetime=8,sprpriority=3,ownpal=1)
        ctl(1500,'Release Lucille','ChangeState','time>=48 || (time>=18 && (command!="holdskill" || command!="holdheavy"))',value=1501+shift)
        state(1501,1501,velset='0,0')
        hit(1501,8,'90+55*max(0,var(50)-18)/30',guard='H',ground__velocity='-7,-11')
        ctl(1501,'Heavy impact','EnvShake','movehit && time=9',time=12,ampl=6,freq=75);end(1501,43)
        state(1510,1510,kind='A');ctl(1510,'Deliberate drop','VelSet','time=10',x=2,y=14)
        hit(1510,10,130,True,guard='H',ground__velocity='-4,-11');landing(1510,1511)
        state(1511,1511,velset='0,0');ctl(1511,'Floor','PosSet',y=0)
        ctl(1511,'Heavy landing','EnvShake','time=0',time=12,ampl=7,freq=65)
        ctl(1511,'Cracked floor','Explod','time=0',anim=fx+23,ID=6903,pos='100,0',removetime=24,sprpriority=1,ownpal=1);end(1511,39)
    return ''.join(parts)


def choreography(block,label,form):
    """Replace shared teleport pursuit with each character's own stage action."""
    if not re.match(r'\s*\[Statedef (?:13010|13210|3010|3210|4410|4510)\]',block):return block
    n=int(re.search(r'Statedef (\d+)',block)[1]);ult=n%10000 in (3210,4510);last=350 if ult else 190
    fraction=f'min(1,time/{last}.0)'
    if label=='Prince':
        # Baseline crossover -> a high arc beside the hoop -> finish at the rim.
        x=f'camerapos x+var(44)*(-280+540*{fraction})'
        y=f'-230*sin(pi*{fraction})'
        target_x='camerapos x+var(44)*210'
        target_y=f'-80-230*abs(sin(time*pi/{last}))'
    elif label=='Rick James':
        # Stay on the couch, deliver repeated platform stomps, finish seated.
        x='camerapos x-var(44)*180';y='-180-80*abs(sin(time*.08))'
        target_x='camerapos x+var(44)*120';target_y='-45-120*abs(sin(time*.08))'
    elif label=='Tyrone Biggums':
        # Low frantic run around the target; no Monarch-style teleport hops.
        x='camerapos x+var(44)*260*sin(time*.055)';y='-25*abs(sin(time*.22))'
        target_x='camerapos x+var(44)*60*sin(time*.11)';target_y='-40-120*abs(sin(time*.16))'
    else:
        # Slow walk-up and a deliberate repeated bat launch, planted on floor.
        x=f'camerapos x-var(44)*(300-180*{fraction})';y='0'
        target_x='camerapos x+var(44)*150';target_y='-40-230*abs(sin(time*.045))'
    chunks=re.split(r'(?=\[State\b)',block)
    for i,c in enumerate(chunks):
        if re.search(r', Pursuit\]',c):
            chunks[i]=re.sub(r'^trigger1=.*$',f'trigger1=time<{last}',c,flags=re.M)
            chunks[i]=re.sub(r'^x=.*$',f'x={x}',chunks[i],flags=re.M)
            chunks[i]=re.sub(r'^y=.*$',f'y={y}',chunks[i],flags=re.M)
        elif re.search(r', Final stance\]',c):chunks[i]=re.sub(r'^trigger1=.*$',f'trigger1=time>={last}',c,flags=re.M)
        elif re.search(r', Hold target\]',c):chunks[i]=re.sub(r'^pos=.*$',f'pos=({target_x}-pos x)*facing,{target_y}-pos y',c,flags=re.M)
        elif label=='Rick James' and re.search(r', Signature prop\]',c):chunks[i]=re.sub(r'^pos=.*$','pos=640-var(44)*180,660',c,flags=re.M)
        elif label=='Tyrone Biggums' and re.search(r', Signature prop\]',c):
            chunks[i]=re.sub(r'^anim=.*$',f'anim={20022+form*1000}',c,flags=re.M)
            chunks[i]=re.sub(r'^pos=.*$','pos=390,570',chunks[i],flags=re.M)
        elif label=='Tyrone Biggums' and ('anim=20006' in c or 'anim=20002' in c):
            chunks[i]=re.sub(r'^anim=.*$',f'anim={20025+form*1000}',c,flags=re.M)
    return ''.join(chunks)


def install(assets,data):
    for form,info in enumerate(data):
        label=info['label'];effects(assets,form,label);animations(assets,form,label)
        info['positive']=[choreography(b,info['label'],form) for b in info['positive']]
        # Different rhythm and body poses as well as different world paths.
        rhythm={'Prince':[('crouch',6),('palm',6),('special',10),('kick',4)],
                'Rick James':[('kick',10),('idle',5),('palm',5)],
                'Tyrone Biggums':[('walk_a',3),('palm',3),('walk_b',3),('crouch',3),('kick',3)],
                'Negan':[('special',24),('palm',6),('idle',10)]}[label]
        for base,total in [(4410 if label=='Tyrone Biggums' else 3010,240),(4510 if label=='Tyrone Biggums' else 3210,420)]:
            n=info['anims'][base];frames=[];remaining=total
            while remaining:
                for key,duration in rhythm:
                    duration=min(duration,remaining)
                    if not duration:break
                    frames.append((('alt_' if form else '')+key,duration));remaining-=duration
            before=len(assets.air);assets.action(n,frames)
            replacement='\n'.join(assets.air[before:]);del assets.air[before:]
            for i,block in enumerate(assets.air):
                if re.match(r'\s*\[Begin Action '+str(n)+r'\]',block):assets.air[i]=replacement;break
    return {info['label']:{'ground':MOVES[info['label']][0],'air':MOVES[info['label']][1],
            'ground_state':1500+form*10000,'air_state':1510+form*10000} for form,info in enumerate(data)}
